"""Tests for endpoint config: named providers, credentials, dialects, and the check CLI."""

from __future__ import annotations

import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "overlay"))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "runner"))

import config as cfg  # noqa: E402
import tier_routing as tr  # noqa: E402

TOML = """
[providers.sparks]
base_url = "http://100.120.4.113:8015/v1"
models = ["DeepSeek-V4.1-Flash"]

[providers.tp2]
base_url = "http://100.97.112.71:8000/v1"
api_key = "vllm"

[providers.ollama]
base_url = "http://localhost:11434/v1"

[providers.anthropic]
kind = "anthropic"
base_url = "https://api.anthropic.com"
api_key_env = "ANTHROPIC_API_KEY"

[tiers.strong]
endpoints = ["sparks/DeepSeek-V4.1-Flash", "anthropic/claude-opus-5", "ollama/qwen3:32b"]
rotate = "sticky"
fallback = ["mid"]

[tiers.mid]
endpoints = ["tp2/Qwen3.8-Flash-Next"]

[tiers.cheap]
endpoints = ["tp2/Qwen3.8-Flash-Next", "ollama/qwen3:8b"]
"""


@pytest.fixture()
def toml_config(tmp_path):
    p = tmp_path / "tiers.toml"
    p.write_text(TOML)
    return p


def test_toml_loads_providers_and_tiers(toml_config):
    tiers = cfg.normalise(cfg._read(toml_config), {"ANTHROPIC_API_KEY": "sk-ant"})
    assert set(tiers) == {"strong", "mid", "cheap"}
    strong = tiers["strong"]
    assert [c["model"] for c in strong["endpoints"]] == ["DeepSeek-V4.1-Flash", "claude-opus-5", "qwen3:32b"]
    assert strong["rotate"] == "sticky" and strong["fallback"] == ["mid"]
    assert [c["kind"] for c in strong["endpoints"]] == ["openai", "anthropic", "openai"]
    assert strong["endpoints"][1]["api_key"] == "sk-ant"


def test_json_works_too(tmp_path):
    p = tmp_path / "tiers.json"
    p.write_text(json.dumps({"providers": {"x": {"base_url": "http://x/v1"}},
                             "tiers": {"cheap": {"endpoints": ["x/m"]}}}))
    tiers = cfg.normalise(cfg._read(p), {})
    assert tiers["cheap"]["endpoints"][0]["model"] == "m"


def test_earlier_shape_still_loads(tmp_path):
    p = tmp_path / "old.json"
    p.write_text(json.dumps({"cheap": {"endpoints": [{"base_url": "http://x/v1", "model": "m"}],
                                      "rotate": "rr", "fallback": []}}))
    tiers = cfg.normalise(cfg._read(p), {})
    assert tiers["cheap"]["endpoints"][0]["provider"] == "inline"


def test_unknown_provider_error_lists_declared_ones(toml_config):
    with pytest.raises(cfg.ConfigError, match=r"unknown provider 'nope'.*sparks"):
        cfg.normalise({"providers": {"sparks": {"base_url": "http://s/v1"}},
                       "tiers": {"cheap": {"endpoints": ["nope/m"]}}}, {})


def test_model_ref_without_provider_is_explained():
    with pytest.raises(cfg.ConfigError, match="must be 'provider/model'"):
        cfg.normalise({"providers": {"a": {"base_url": "http://a/v1"}},
                       "tiers": {"cheap": {"endpoints": ["just-a-model"]}}}, {})


def test_missing_env_key_names_the_variable():
    with pytest.raises(cfg.ConfigError, match="ANTHROPIC_API_KEY is not set"):
        cfg.normalise({"providers": {"anthropic": {"base_url": "https://a",
                                                    "api_key_env": "ANTHROPIC_API_KEY"}},
                       "tiers": {"strong": {"endpoints": ["anthropic/m"]}}}, {})


def test_api_key_cmd_resolves_and_caches():
    spec = {"name": "p", "api_key_cmd": "printf 'sk-from-cmd\\n'"}
    cache: dict[str, str] = {}
    assert cfg.resolve_key(spec, {}, cache) == "sk-from-cmd"
    assert cache  # cached
    spec2 = {"name": "q", "api_key_cmd": "false"}
    with pytest.raises(cfg.ConfigError, match="api_key_cmd exited"):
        cfg.resolve_key(spec2, {})


def test_local_server_needs_no_key():
    tiers = cfg.normalise({"providers": {"ollama": {"base_url": "http://localhost:11434/v1"}},
                           "tiers": {"cheap": {"endpoints": ["ollama/qwen3:8b"]}}}, {})
    assert tiers["cheap"]["endpoints"][0]["api_key"] == "vllm"


def test_unknown_kind_is_rejected():
    with pytest.raises(cfg.ConfigError, match="unknown kind 'bedrock'"):
        cfg.normalise({"providers": {"b": {"base_url": "http://b", "kind": "bedrock"}},
                       "tiers": {"cheap": {"endpoints": ["b/m"]}}}, {})


def test_self_fallback_rejected():
    with pytest.raises(cfg.ConfigError, match="lists itself"):
        cfg.normalise({"providers": {"a": {"base_url": "http://a/v1"}},
                       "tiers": {"cheap": {"endpoints": ["a/m"], "fallback": ["cheap"]}}}, {})


def test_rotate_validation():
    with pytest.raises(cfg.ConfigError, match="rotate must be"):
        cfg.normalise({"providers": {"a": {"base_url": "http://a/v1"}},
                       "tiers": {"cheap": {"endpoints": ["a/m"], "rotate": "wobbly"}}}, {})


def test_default_config_path_is_discovered(monkeypatch, tmp_path):
    monkeypatch.setenv("KNOWING_CONFIG", str(tmp_path / "nope.toml"))
    with pytest.raises(cfg.ConfigError, match="missing file"):
        cfg.find_config({"KNOWING_CONFIG": str(tmp_path / "nope.toml")})


def test_missing_config_says_what_to_create():
    with pytest.raises(cfg.ConfigError, match="no config found"):
        cfg.load({})


# ------------------------------------------------------------- anthropic dialect
def test_anthropic_endpoint_gets_the_claude_client(toml_config):
    tiers = cfg.normalise(cfg._read(toml_config), {"ANTHROPIC_API_KEY": "sk-ant"})
    p = tr.TierMapProvider(tiers, client_factory=lambda url, key: {"base_url": url, "key": key})
    cfg_anthropic = [c for c in tiers["strong"]["endpoints"] if c["kind"] == "anthropic"][0]
    provider = p._provider(cfg_anthropic)
    assert type(provider).__name__ == "ClaudeProvider"
    assert provider.model_override == "claude-opus-5"


# -------------------------------------------------------------------- from-pi
def test_from_pi_models_emits_usable_config(tmp_path):
    pi = tmp_path / "models.json"
    pi.write_text(json.dumps({"providers": {
        "sparks": {"baseUrl": "http://100.120.4.113:8015/v1", "apiKey": "vllm",
                   "models": [{"id": "DeepSeek-V4.1-Flash"}]},
        "litellm": {"baseUrl": "https://gw/v1",
                    "apiKey": "!grep '^k=' $HOME/key.env | cut -d= -f2-",
                    "models": [{"id": "Qwen3.8-Flash-Next"}]},
    }}))
    out = cfg.from_pi_models(pi)
    assert "[providers.sparks]" in out and "[providers.litellm]" in out
    assert 'api_key_cmd = "grep ' in out            # pi's !cmd form becomes api_key_cmd
    assert "[tiers.strong]" in out
    parsed = cfg.normalise(__import__("tomllib").loads(out), {})
    assert parsed["cheap"]["endpoints"][0]["provider"] == "sparks"


# ----------------------------------------------------------------------- probe
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        if self.path.endswith("/models"):
            body = json.dumps({"data": [{"id": "model-a"}, {"id": "model-b"}]}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404)

    def log_message(self, *a):  # silence
        pass


def test_probe_reports_served_models():
    srv = HTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        url = f"http://127.0.0.1:{srv.server_address[1]}"
        out = cfg.probe([{"base_url": url, "model": "model-a", "api_key": "x", "kind": "openai",
                          "provider": "local"}])
        assert out[0]["status"] == 200 and out[0]["served"] == ["model-a", "model-b"]
    finally:
        srv.shutdown()


def test_probe_marks_an_unreachable_endpoint_without_raising():
    out = cfg.probe([{"base_url": "http://127.0.0.1:1", "model": "m", "api_key": "x",
                      "kind": "openai", "provider": "dead"}], timeout=0.3)
    assert out[0]["status"] is None and out[0]["error"]


def test_cli_check_exit_codes(monkeypatch, toml_config, capsys):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant")
    assert cfg.main(["check", "--config", str(toml_config)]) == 0
    assert "strong" in capsys.readouterr().out
    bad = toml_config.parent / "bad.toml"
    bad.write_text("[tiers.cheap]\nendpoints = []\n")
    assert cfg.main(["check", "--config", str(bad)]) == 2
