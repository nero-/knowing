"""Tests for tier routing — the layer that puts different model tiers on different endpoints."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "overlay"))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "runner"))

import tier_routing as tr  # noqa: E402

SPARKS = {"base_url": "http://tp4.example:8015/v1", "model": "DeepSeek-V4.1-Flash"}
TP2 = {"base_url": "http://tp2.example:8000/v1", "model": "Qwen3.8-Flash-Next"}


class FakeChoice:
    def __init__(self, text):
        self.message = type("M", (), {"content": text})()


class FakeResponse:
    def __init__(self, text):
        self.choices = [FakeChoice(text)]


class FakeCompletions:
    def __init__(self, sink):
        self.sink = sink

    def create(self, *, model, messages, **kw):
        self.sink.append(model)
        return FakeResponse(f"ok:{model}")


class FakeClient:
    def __init__(self, base_url, sink):
        self.base_url = base_url
        self.chat = type("C", (), {"completions": FakeCompletions(sink)})()


def make(sink):
    def factory(base_url, api_key):
        sink.append(("client", base_url))
        return FakeClient(base_url, sink)
    return factory


# ---------------------------------------------------------------------- config
def test_env_json_config():
    tiers = tr.load_tiers({"KNOWING_TIERS": '{"strong": {"base_url": "http://a/", "model": "A"},'
                                             ' "cheap": {"base_url": "http://b/", "model": "B"}}'})
    assert tiers["strong"]["base_url"] == "http://a"  # trailing slash normalised
    assert set(tiers) == {"strong", "cheap"}


def test_per_tier_env_vars():
    tiers = tr.load_tiers({
        "KNOWING_TIER_STRONG_BASE_URL": "http://a/v1", "KNOWING_TIER_STRONG_MODEL": "A",
        "KNOWING_TIER_CHEAP_BASE_URL": "http://b/v1", "KNOWING_TIER_CHEAP_MODEL": "B",
        "OPENAI_API_KEY": "sk-shared",
    })
    assert tiers["cheap"]["model"] == "B"
    assert tiers["strong"]["api_key"] == "sk-shared"


def test_config_file(tmp_path):
    f = tmp_path / "tiers.json"
    f.write_text('{"mid": {"base_url": "http://m/v1", "model": "M"}}')
    assert tr.load_tiers({"KNOWING_TIERS_FILE": str(f)})["mid"]["model"] == "M"


def test_missing_file_is_named():
    with pytest.raises(tr.TierConfigError, match="missing file"):
        tr.load_tiers({"KNOWING_TIERS_FILE": "/nope/tiers.json"})


def test_no_config_names_the_variables():
    with pytest.raises(tr.TierConfigError, match="KNOWING_TIER_STRONG_BASE_URL"):
        tr.load_tiers({})


def test_missing_model_is_an_error():
    with pytest.raises(tr.TierConfigError, match="no model"):
        tr.load_tiers({"KNOWING_TIER_MID_BASE_URL": "http://m/v1"})


def test_unknown_tier_rejected():
    with pytest.raises(tr.TierConfigError, match="unknown tier"):
        tr.load_tiers({"KNOWING_TIERS": '{"heavy": {"base_url": "http://x/", "model": "X"}}'})


# ------------------------------------------------------------------- fallback
def test_resolve_falls_back_down_a_tier():
    tiers = {"cheap": TP2}
    eff, cfg = tr.resolve_tier("strong", tiers)
    assert eff == "cheap" and cfg["model"] == "Qwen3.8-Flash-Next"


def test_resolve_prefers_the_configured_tier():
    tiers = {"strong": SPARKS, "cheap": TP2}
    eff, cfg = tr.resolve_tier("strong", tiers)
    assert eff == "strong" and cfg["model"] == "DeepSeek-V4.1-Flash"


def test_no_endpoint_at_all_is_an_error():
    with pytest.raises(tr.TierConfigError, match="no endpoint for tier 'cheap'"):
        tr.resolve_tier("cheap", {})


# --------------------------------------------------------------------- routing
def test_each_tier_hits_its_own_endpoint():
    sink: list = []
    p = tr.TierMapProvider({"strong": SPARKS, "mid": TP2, "cheap": TP2},
                           client_factory=make(sink))
    p.complete("plan this", model_tier="strong")
    p.complete("read this", model_tier="mid")
    p.fanout(["a", "b"], model_tier="cheap")
    assert [r[1] for r in p.routed] == [SPARKS["base_url"], TP2["base_url"], TP2["base_url"]]
    assert p.routed[0][2] == "DeepSeek-V4.1-Flash"


def test_one_client_per_endpoint():
    sink: list = []
    p = tr.TierMapProvider({"strong": SPARKS, "mid": TP2, "cheap": TP2},
                           client_factory=make(sink))
    for _ in range(3):
        p.complete("x", model_tier="cheap")
    p.complete("y", model_tier="mid")  # mid and cheap share one endpoint -> no second client
    clients = [s for s in sink if isinstance(s, tuple)]
    assert len(clients) == 1
    p.complete("z", model_tier="strong")  # a different endpoint -> exactly one more
    assert len([s for s in sink if isinstance(s, tuple)]) == 2


def test_unconfigured_tier_falls_back_and_is_reported():
    p = tr.TierMapProvider({"cheap": TP2}, client_factory=make([]))
    p.complete("synthesise", model_tier="strong")
    assert p.routed[0][0] == "cheap"


def test_unknown_tier_raises_at_call_time():
    p = tr.TierMapProvider({"cheap": TP2}, client_factory=make([]))
    with pytest.raises(tr.TierConfigError, match="unknown tier"):
        p.complete("x", model_tier="huge")


def test_search_is_explicitly_unsupported():
    p = tr.TierMapProvider({"cheap": TP2}, client_factory=make([]))
    with pytest.raises(NotImplementedError, match="Anthropic-specific"):
        p.search("q")


def test_build_provider_knows_the_tiers_backend(monkeypatch):
    """Upstream's build_provider must accept name='tiers' after the knowing patch."""
    import providers  # upstream runner/providers.py
    monkeypatch.setenv("KNOWING_TIERS", '{"mid": {"base_url": "http://m/v1", "model": "M"}}')
    p = providers.build_provider("tiers")
    assert p.name == "tiers"
    assert p.tiers["mid"]["model"] == "M"
