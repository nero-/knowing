"""Tests for tier routing: pools, rotation, failover, cooldown.

The negative and failure cases carry the value here — a pool that cannot survive a dead cluster is
a single endpoint with extra config.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "overlay"))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "runner"))

import tier_routing as tr  # noqa: E402

A = {"base_url": "http://a/v1", "model": "model-a"}
B = {"base_url": "http://b/v1", "model": "model-b"}
C = {"base_url": "http://c/v1", "model": "model-c"}


class FakeClock:
    def __init__(self):
        self.t = 1000.0

    def __call__(self):
        return self.t

    def advance(self, seconds):
        self.t += seconds


class Resp:
    def __init__(self, text):
        self.choices = [type("Ch", (), {"message": type("M", (), {"content": text})()})()]


class Client:
    """Records calls; fails with whatever `fail` says for its endpoint."""

    def __init__(self, base_url, fail, sink):
        self.base_url, self.fail, self.sink = base_url, fail, sink
        self.chat = type("C", (), {"completions": type("Comp", (), {"create": self._create})()})()

    def _create(self, *, model, messages, **kw):
        if base_url_fails := self.fail.get(self.base_url):
            self.sink.append(("fail", self.base_url))
            raise base_url_fails
        self.sink.append(("ok", self.base_url, model))
        return Resp(f"{self.base_url}|{model}")


def provider(tiers, *, fail=None, clock=None):
    sink: list = []
    calls = {"n": 0}

    def factory(base_url, api_key):
        calls["n"] += 1
        return Client(base_url, fail or {}, sink)

    p = tr.TierMapProvider(tiers, client_factory=factory, clock=clock or FakeClock())
    p.sink = sink
    p.client_count = lambda: calls["n"]
    return p


def single(base, rotate="rr", fallback=None):
    spec = {"endpoints": [base], "rotate": rotate}
    if fallback is not None:
        spec["fallback"] = fallback
    return {"cheap": spec}


# --------------------------------------------------------------------- config
def test_config_accepts_single_object_list_and_pool():
    assert tr.load_tiers({"KNOWING_TIERS": '{"cheap": {"base_url": "http://x/v1", "model": "m"}}'})[
        "cheap"]["endpoints"][0]["model"] == "m"
    assert len(tr.load_tiers({"KNOWING_TIERS": '{"cheap": [{"base_url": "http://x/v1", "model": "m"}]}'})[
        "cheap"]["endpoints"]) == 1
    pool = tr.load_tiers({"KNOWING_TIERS": '{"cheap": {"endpoints": [{"base_url": "http://x/v1", '
                                           '"model": "m"}, {"base_url": "http://y/v1", "model": "n"}]}}'})
    assert [c["model"] for c in pool["cheap"]["endpoints"]] == ["m", "n"]


def test_config_rejects_bad_rotation_and_self_fallback():
    with pytest.raises(tr.TierConfigError, match="rotate must be"):
        tr.load_tiers({"KNOWING_TIERS": '{"cheap": {"endpoints": [{"base_url": "http://x/v1", '
                                       '"model": "m"}], "rotate": "random"}}'})
    with pytest.raises(tr.TierConfigError, match="lists itself"):
        tr.load_tiers({"KNOWING_TIERS": '{"cheap": {"endpoints": [{"base_url": "http://x/v1", '
                                       '"model": "m"}], "fallback": ["cheap"]}}'})


def test_config_conflict_between_file_and_env_is_an_error():
    with pytest.raises(tr.TierConfigError, match="configured twice"):
        tr.load_tiers({"KNOWING_TIERS": '{"cheap": {"base_url": "http://x/v1", "model": "m"}}',
                       "KNOWING_TIER_CHEAP_MODEL": "n"})


def test_documented_default_fallback_chain():
    tiers = tr.load_tiers({"KNOWING_TIERS": '{"cheap": {"base_url": "http://x/v1", "model": "m"}}'})
    assert tiers["cheap"]["fallback"] == []


# ------------------------------------------------------------------ rotation
def test_round_robin_spreads_calls_across_the_pool():
    p = provider({"cheap": {"endpoints": [A, B], "rotate": "rr", "fallback": []}})
    for _ in range(4):
        p.complete("x", model_tier="cheap")
    assert [s[1] for s in p.sink] == ["http://a/v1", "http://b/v1", "http://a/v1", "http://b/v1"]


def test_sticky_keeps_one_endpoint_for_the_process():
    p = provider({"strong": {"endpoints": [A, B], "rotate": "sticky", "fallback": []}})
    for _ in range(4):
        p.complete("x", model_tier="strong")
    assert {s[1] for s in p.sink} == {"http://a/v1"}


def test_one_client_per_endpoint_even_under_round_robin():
    p = provider({"cheap": {"endpoints": [A, B], "rotate": "rr", "fallback": []}})
    for _ in range(6):
        p.complete("x", model_tier="cheap")
    assert p.client_count() == 2


# ------------------------------------------------------------------ failover
def test_dead_cluster_fails_over_to_the_next_candidate():
    p = provider({"cheap": {"endpoints": [A, B], "rotate": "rr", "fallback": []}},
                 fail={"http://a/v1": ConnectionError("cluster down")})
    out = p.complete("x", model_tier="cheap")
    assert out.startswith("http://b/v1")
    reasons = [r["reason"] for r in p.routed]
    assert reasons == ["failover", "ok"]


def test_429_is_transient_and_rotates_away():
    err = type("RateLimitError", (Exception,), {"status_code": 429})("slow down")
    p = provider({"cheap": {"endpoints": [A, B], "rotate": "rr", "fallback": []}},
                 fail={"http://a/v1": err})
    assert p.complete("x", model_tier="cheap").startswith("http://b/v1")


def test_bad_request_is_not_retried_elsewhere():
    err = type("BadRequestError", (Exception,), {"status_code": 400})("malformed")
    p = provider({"cheap": {"endpoints": [A, B], "rotate": "rr", "fallback": []}},
                 fail={"http://a/v1": err})
    with pytest.raises(Exception, match="malformed"):
        p.complete("x", model_tier="cheap")
    assert [s for s in p.sink] == [("fail", "http://a/v1")]  # B was never tried


def test_cooldown_skips_a_failing_endpoint_on_the_next_call():
    clock = FakeClock()
    p = provider({"cheap": {"endpoints": [A, B], "rotate": "rr", "fallback": []}},
                 fail={"http://a/v1": ConnectionError("down")}, clock=clock)
    p.complete("x", model_tier="cheap")          # A fails, B answers
    p.complete("y", model_tier="cheap")          # A is cooling down -> B first
    assert [s[1] for s in p.sink if s[0] == "ok"] == ["http://b/v1", "http://b/v1"]
    assert [s for s in p.sink if s[0] == "fail"] == [("fail", "http://a/v1")]


def test_endpoint_becomes_eligible_again_after_cooldown():
    clock = FakeClock()
    p = provider({"cheap": {"endpoints": [A, B], "rotate": "rr", "fallback": []}},
                 fail={"http://a/v1": ConnectionError("down")}, clock=clock)
    cfg_a = p.tiers["cheap"]["endpoints"][0]
    p.complete("x", model_tier="cheap")
    assert not p._available(cfg_a)                     # cooling down
    clock.advance(tr.COOLDOWN_BASE + 1)
    assert p._available(cfg_a)                          # eligible again
    p.fail = {}                                         # cluster came back
    p._providers.clear()
    p = provider({"cheap": {"endpoints": [A], "rotate": "rr", "fallback": []}}, clock=clock)
    p.complete("y", model_tier="cheap")
    assert p.sink and p.sink[-1][0] == "ok"


def test_cooldown_doubles_while_the_endpoint_keeps_failing():
    clock = FakeClock()
    p = provider({"cheap": {"endpoints": [A], "rotate": "rr", "fallback": ["mid"]},
                  "mid": {"endpoints": [B], "rotate": "rr", "fallback": []}},
                 fail={"http://a/v1": ConnectionError("down")}, clock=clock)
    key = p._key(p.tiers["cheap"]["endpoints"][0])
    p.complete("x", model_tier="cheap")
    _, streak1 = p._down[key]
    clock.advance(tr.COOLDOWN_BASE + 1)
    p.complete("y", model_tier="cheap")
    until, streak2 = p._down[key]
    assert streak2 == streak1 + 1
    assert until - clock() > tr.COOLDOWN_BASE


# ------------------------------------------------------------------ fallback
def test_tier_falls_back_down_the_chain_and_says_so():
    p = provider({"cheap": {"endpoints": [A], "rotate": "rr", "fallback": ["mid"]},
                  "mid": {"endpoints": [B], "rotate": "rr", "fallback": []}},
                 fail={"http://a/v1": ConnectionError("down")})
    assert p.complete("x", model_tier="cheap").startswith("http://b/v1")
    assert p.routed[-1]["reason"] == "fallback-from-cheap"


def test_all_endpoints_down_raises_with_every_attempt_named():
    p = provider({"cheap": {"endpoints": [A, B], "rotate": "rr", "fallback": []}},
                 fail={"http://a/v1": ConnectionError("a down"), "http://b/v1": ConnectionError("b down")})
    with pytest.raises(RuntimeError, match="no endpoint answered for tier 'cheap'.*2"):
        p.complete("x", model_tier="cheap")


def test_unknown_tier_raises():
    p = provider({"cheap": {"endpoints": [A], "rotate": "rr", "fallback": []}})
    with pytest.raises(tr.TierConfigError, match="no endpoint for tier 'enormous'"):
        p.complete("x", model_tier="enormous")


def test_search_is_explicitly_unsupported():
    p = provider({"cheap": {"endpoints": [A], "rotate": "rr", "fallback": []}})
    with pytest.raises(NotImplementedError, match="Anthropic-specific"):
        p.search("q")


def test_build_provider_knows_the_tiers_backend(monkeypatch):
    import providers  # upstream runner/providers.py, via the knowing patch
    monkeypatch.setenv("KNOWING_TIERS", '{"mid": {"endpoints": [{"base_url": "http://m/v1", "model": "M"}]}}')
    p = providers.build_provider("tiers")
    assert p.name == "tiers"
    assert p.tiers["mid"]["endpoints"][0]["model"] == "M"
