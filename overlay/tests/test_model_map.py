"""Tests for model naming: resolution order, pools, failover, cooldown, dialects.

There is no tier vocabulary in knowing — a "model" here is just a name the config defines, and the
resolution rules are the whole policy: explicit name, then phase pin, then default, else an error.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "overlay"))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "runner"))

import config as cfg  # noqa: E402
import model_map as mm  # noqa: E402

A = {"provider": "a", "kind": "openai", "base_url": "http://a/v1", "model": "model-a", "api_key": "k"}
B = {"provider": "b", "kind": "openai", "base_url": "http://b/v1", "model": "model-b", "api_key": "k"}


class FakeClock:
    def __init__(self):
        self.t = 1000.0

    def __call__(self):
        return self.t

    def advance(self, s):
        self.t += s


class Resp:
    def __init__(self, text):
        self.choices = [type("Ch", (), {"message": type("M", (), {"content": text})()})()]


class Client:
    def __init__(self, base_url, fail, sink):
        self.base_url, self.fail, self.sink = base_url, fail, sink
        self.chat = type("C", (), {"completions": type("Comp", (), {"create": self._create})()})()

    def _create(self, *, model, messages, **kw):
        if (err := self.fail.get(self.base_url)) is not None:
            self.sink.append(("fail", self.base_url))
            raise err
        self.sink.append(("ok", self.base_url, model))
        return Resp(f"{self.base_url}|{model}")


def build(models, *, default=None, phases=None, fail=None, clock=None):
    spec = {"models": {}, "default": default or next(iter(models)), "phases": phases or {}}
    for name, m in models.items():
        spec["models"][name] = {"endpoints": m.get("endpoints", []),
                                "rotate": m.get("rotate", "rr"),
                                "fallback": m.get("fallback", [])}
    sink: list = []
    p = mm.ModelMap(spec, client_factory=lambda url, key: Client(url, fail or {}, sink),
                    clock=clock or FakeClock())
    p.sink = sink
    return p


def one(endpoint, **kw):
    return {"endpoints": [endpoint], **kw}


# ------------------------------------------------------------------ naming
def test_explicit_name_wins():
    p = build({"opus": one(A), "sonnet": one(B)}, default="sonnet")
    assert p.resolve("opus") == "opus"


def test_default_when_nothing_named():
    p = build({"opus": one(A), "sonnet": one(B)}, default="sonnet")
    assert p.resolve("") == "sonnet"
    assert p.resolve("", phase="9") == "sonnet"


def test_phase_pin_beats_default():
    p = build({"opus": one(A), "sonnet": one(B)}, default="sonnet", phases={"6": "opus"})
    assert p.resolve("", phase="6") == "opus"


def test_unknown_name_is_an_error_listing_names():
    p = build({"opus": one(A)}, default="opus")
    with pytest.raises(mm.ModelConfigError, match=r"unknown model 'opuss'.*opus"):
        p.resolve("opuss")


def test_unknown_phase_pin_is_an_error():
    p = build({"opus": one(A)}, default="opus", phases={"6": "nope"})
    with pytest.raises(mm.ModelConfigError, match="pins model 'nope'"):
        p.resolve("", phase="6")


def test_no_default_and_nothing_named_is_an_error():
    with pytest.raises(cfg.ConfigError, match="not a configured model"):
        cfg.normalise({"providers": {"a": {"base_url": "http://a/v1"}},
                       "models": {"x": {"endpoints": ["a/m"]}}, "default": "missing"}, {})


# ------------------------------------------------------------------- pools
def test_round_robin_spreads_calls():
    p = build({"fast": {"endpoints": [A, B]}})
    for _ in range(4):
        p.complete("x", model_tier="fast")
    assert [s[1] for s in p.sink] == ["http://a/v1", "http://b/v1", "http://a/v1", "http://b/v1"]


def test_sticky_holds_one_endpoint():
    p = build({"smart": {"endpoints": [A, B], "rotate": "sticky"}})
    for _ in range(3):
        p.complete("x", model_tier="smart")
    assert {s[1] for s in p.sink} == {"http://a/v1"}


def test_empty_name_uses_default_endpoint():
    p = build({"sonnet": one(B)}, default="sonnet")
    assert p.complete("x").startswith("http://b/v1")


# ---------------------------------------------------------------- failover
def test_dead_endpoint_fails_over():
    p = build({"fast": {"endpoints": [A, B]}}, fail={"http://a/v1": ConnectionError("down")})
    assert p.complete("x", model_tier="fast").startswith("http://b/v1")
    assert [r["reason"] for r in p.routed] == ["failover", "ok"]


def test_429_cools_down_and_skips_next_time():
    clock = FakeClock()
    p = build({"fast": {"endpoints": [A, B]}},
              fail={"http://a/v1": type("RateLimitError", (Exception,), {"status_code": 429})("slow")},
              clock=clock)
    p.complete("x", model_tier="fast")
    p.complete("y", model_tier="fast")
    assert [s for s in p.sink if s[0] == "fail"] == [("fail", "http://a/v1")]  # only once


def test_bad_request_propagates_without_trying_another_endpoint():
    err = type("BadRequestError", (Exception,), {"status_code": 400})("malformed")
    p = build({"fast": {"endpoints": [A, B]}}, fail={"http://a/v1": err})
    with pytest.raises(Exception, match="malformed"):
        p.complete("x", model_tier="fast")
    assert p.sink == [("fail", "http://a/v1")]


def test_named_fallback_is_used_and_recorded():
    p = build({"smart": {"endpoints": [A], "fallback": ["cheap"]}, "cheap": one(B)},
              fail={"http://a/v1": ConnectionError("down")})
    assert p.complete("x", model_tier="smart").startswith("http://b/v1")
    assert p.routed[-1]["reason"] == "fallback-from-smart"


def test_fallback_does_not_loop_forever():
    p = build({"smart": {"endpoints": [A], "fallback": ["cheap"]},
               "cheap": {"endpoints": [B], "fallback": ["smart"]}},
              fail={"http://a/v1": ConnectionError("a"), "http://b/v1": ConnectionError("b")})
    with pytest.raises(RuntimeError, match="no endpoint answered for model 'smart'"):
        p.complete("x", model_tier="smart")
    assert len(p.sink) == 2  # each endpoint tried once, then it stops


def test_all_down_error_names_every_attempt():
    p = build({"fast": {"endpoints": [A, B]}},
              fail={"http://a/v1": ConnectionError("a"), "http://b/v1": ConnectionError("b")})
    with pytest.raises(RuntimeError, match=r"tried 2.*fast\[0\].*fast\[1\]"):
        p.complete("x", model_tier="fast")


# --------------------------------------------------------------- dialects
def test_anthropic_provider_used_for_kind(toml_config):
    data = cfg.normalise(cfg._read(toml_config), {"ANTHROPIC_API_KEY": "sk"})
    p = mm.ModelMap(data, client_factory=lambda url, key: {"url": url})
    cand = [c for c in data["models"]["opus"]["endpoints"] if c["kind"] == "anthropic"][0]
    assert type(p._provider(cand)).__name__ == "ClaudeProvider"


def test_build_provider_accepts_the_new_name(monkeypatch, tmp_path):
    import providers
    f = tmp_path / "c.toml"
    f.write_text('[providers.a]\nbase_url = "http://a/v1"\n\n[models.m]\nendpoints = ["a/x"]\n')
    monkeypatch.setenv("KNOWING_CONFIG", str(f))
    p = providers.build_provider("models")
    assert p.name == "models" and p.default == "m"
    assert providers.build_provider("tiers").name == "models"  # legacy name still accepted


# ---------------------------------------------------------------- fixtures
TOML = """
default = "sonnet"

[providers.sparks]
base_url = "http://100.120.4.113:8015/v1"

[providers.anthropic]
kind = "anthropic"
base_url = "https://api.anthropic.com"
api_key_env = "ANTHROPIC_API_KEY"

[models.opus]
endpoints = ["sparks/DeepSeek-V4.1-Flash", "anthropic/claude-opus-5"]
rotate = "sticky"
fallback = ["sonnet"]

[models.sonnet]
endpoints = ["sparks/DeepSeek-V4.1-Flash"]

default = "sonnet"

[phases."6"]
model = "opus"
"""


@pytest.fixture()
def toml_config(tmp_path):
    p = tmp_path / "models.toml"
    p.write_text(TOML)
    return p
