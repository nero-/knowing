"""Tests for endpoint config: named providers, model names, defaults, phase pins, credentials."""

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

import config as cfg  # noqa: E402

TOML = """
default = "sonnet"

[providers.sparks]
base_url = "http://100.120.4.113:8015/v1"

[providers.tp2]
base_url = "http://100.97.112.71:8000/v1"
api_key = "vllm"

[providers.ollama]
base_url = "http://localhost:11434/v1"

[providers.anthropic]
kind = "anthropic"
base_url = "https://api.anthropic.com"
api_key_env = "ANTHROPIC_API_KEY"

[models.opus]
endpoints = ["sparks/DeepSeek-V4.1-Flash", "anthropic/claude-opus-5"]
rotate = "sticky"
fallback = ["sonnet"]

[models.sonnet]
endpoints = ["tp2/Qwen3.8-Flash-Next"]

[models.haiku]
endpoints = ["tp2/Qwen3.8-Flash-Next", "ollama/qwen3:8b"]

default = "sonnet"

[phases."6"]
model = "opus"
"""


@pytest.fixture()
def toml_config(tmp_path):
    p = tmp_path / "models.toml"
    p.write_text(TOML)
    return p


def env_with_key(**extra):
    base = {"ANTHROPIC_API_KEY": "sk-ant"}
    base.update(extra)
    return base


# ------------------------------------------------------------------- parsing
def test_toml_loads_providers_models_default_and_phases(toml_config):
    conf = cfg.normalise(cfg._read(toml_config), env_with_key())
    assert {"models", "default", "phases"} <= set(conf)
    assert set(conf["models"]) == {"opus", "sonnet", "haiku"}
    assert conf["default"] == "sonnet"
    assert conf["phases"] == {"6": "opus"}
    opus = conf["models"]["opus"]
    assert [c["model"] for c in opus["endpoints"]] == ["DeepSeek-V4.1-Flash", "claude-opus-5"]
    assert [c["kind"] for c in opus["endpoints"]] == ["openai", "anthropic"]
    assert opus["rotate"] == "sticky" and opus["fallback"] == ["sonnet"]
    assert opus["endpoints"][1]["api_key"] == "sk-ant"


def test_json_works_too(tmp_path):
    p = tmp_path / "c.json"
    p.write_text(json.dumps({"providers": {"x": {"base_url": "http://x/v1"}},
                             "models": {"m": {"endpoints": ["x/model-x"]}}}))
    conf = cfg.normalise(cfg._read(p), {})
    assert conf["models"]["m"]["endpoints"][0]["model"] == "model-x"
    assert conf["default"] == "m"  # single model becomes the default


def test_legacy_tiers_section_still_loads(tmp_path):
    p = tmp_path / "old.json"
    p.write_text(json.dumps({"providers": {"x": {"base_url": "http://x/v1"}},
                             "tiers": {"cheap": {"endpoints": ["x/m"], "rotate": "rr"}}}))
    conf = cfg.normalise(cfg._read(p), {})
    assert conf["models"]["cheap"]["rotate"] == "rr"


def test_inline_endpoint_object_still_loads():
    conf = cfg.normalise({"models": {"m": {"endpoints": [{"base_url": "http://i/v1", "model": "m1"}]}}}, {})
    assert conf["models"]["m"]["endpoints"][0]["provider"] == "inline"


# ------------------------------------------------------------------ errors
def test_unknown_provider_lists_declared_ones():
    with pytest.raises(cfg.ConfigError, match=r"unknown provider 'nope'.*sparks"):
        cfg.normalise({"providers": {"sparks": {"base_url": "http://s/v1"}},
                       "models": {"m": {"endpoints": ["nope/x"]}}}, {})


def test_model_ref_without_provider_is_explained():
    with pytest.raises(cfg.ConfigError, match="must be 'provider/model'"):
        cfg.normalise({"providers": {"a": {"base_url": "http://a/v1"}},
                       "models": {"m": {"endpoints": ["just-a-model"]}}}, {})


def test_missing_env_key_names_the_variable():
    with pytest.raises(cfg.ConfigError, match="ANTHROPIC_API_KEY is not set"):
        cfg.normalise({"providers": {"anthropic": {"base_url": "https://a",
                                                    "api_key_env": "ANTHROPIC_API_KEY"}},
                       "models": {"m": {"endpoints": ["anthropic/x"]}}}, {})


def test_unknown_kind_rejected():
    with pytest.raises(cfg.ConfigError, match="unknown kind 'bedrock'"):
        cfg.normalise({"providers": {"b": {"base_url": "http://b", "kind": "bedrock"}},
                       "models": {"m": {"endpoints": ["b/x"]}}}, {})


def test_self_fallback_rejected():
    with pytest.raises(cfg.ConfigError, match="lists itself"):
        cfg.normalise({"providers": {"a": {"base_url": "http://a/v1"}},
                       "models": {"m": {"endpoints": ["a/x"], "fallback": ["m"]}}}, {})


def test_fallback_must_name_a_configured_model():
    with pytest.raises(cfg.ConfigError, match="fallback 'ghost' is not configured"):
        cfg.normalise({"providers": {"a": {"base_url": "http://a/v1"}},
                       "models": {"m": {"endpoints": ["a/x"], "fallback": ["ghost"]}}}, {})


def test_default_must_be_a_configured_model():
    with pytest.raises(cfg.ConfigError, match="`default = 'ghost'`"):
        cfg.normalise({"providers": {"a": {"base_url": "http://a/v1"}},
                       "models": {"m": {"endpoints": ["a/x"]}}, "default": "ghost"}, {})


def test_phase_pin_must_name_a_configured_model():
    with pytest.raises(cfg.ConfigError, match=r"phases.6 pins 'ghost'"):
        cfg.normalise({"providers": {"a": {"base_url": "http://a/v1"}},
                       "models": {"m": {"endpoints": ["a/x"]}},
                       "phases": {"6": {"model": "ghost"}}}, {})


def test_rotate_validation():
    with pytest.raises(cfg.ConfigError, match="rotate must be"):
        cfg.normalise({"providers": {"a": {"base_url": "http://a/v1"}},
                       "models": {"m": {"endpoints": ["a/x"], "rotate": "wobbly"}}}, {})


def test_missing_file_is_named():
    with pytest.raises(cfg.ConfigError, match="missing file"):
        cfg.find_config({"KNOWING_CONFIG": "/nope/models.toml"})


def test_missing_config_says_what_to_create():
    with pytest.raises(cfg.ConfigError, match="no config found"):
        cfg.load({})


# -------------------------------------------------------------- credentials
def test_api_key_cmd_resolves_and_caches():
    spec = {"name": "p", "api_key_cmd": "printf 'sk-from-cmd\\n'"}
    cache: dict[str, str] = {}
    assert cfg.resolve_key(spec, {}, cache) == "sk-from-cmd"
    assert cache
    with pytest.raises(cfg.ConfigError, match="api_key_cmd exited"):
        cfg.resolve_key({"name": "q", "api_key_cmd": "false"}, {})


def test_local_server_needs_no_key():
    conf = cfg.normalise({"providers": {"ollama": {"base_url": "http://localhost:11434/v1"}},
                          "models": {"local": {"endpoints": ["ollama/qwen3:8b"]}}}, {})
    assert conf["models"]["local"]["endpoints"][0]["api_key"] == "vllm"


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
    assert 'api_key_cmd = "grep ' in out
    import tomllib
    conf = cfg.normalise(tomllib.loads(out), {})
    assert conf["models"]["default"]["endpoints"][0]["provider"] == "sparks"


# ---------------------------------------------------------------------- probe
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

    def log_message(self, *a):
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


def test_probe_marks_unreachable_without_raising():
    out = cfg.probe([{"base_url": "http://127.0.0.1:1", "model": "m", "api_key": "x",
                      "kind": "openai", "provider": "dead"}], timeout=0.3)
    assert out[0]["status"] is None and out[0]["error"]


# ------------------------------------------------------------------------ CLI
def test_cli_check_exit_codes(monkeypatch, toml_config, capsys):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant")
    assert cfg.main(["check", "--config", str(toml_config)]) == 0
    out = capsys.readouterr().out
    assert "opus" in out and "default=sonnet" in out
    bad = toml_config.parent / "bad.toml"
    bad.write_text("[models.cheap]\nendpoints = []\n")
    assert cfg.main(["check", "--config", str(bad)]) == 2


def test_default_written_under_a_model_table_is_recovered_with_a_note():
    """TOML puts `default = x` inside the preceding table; honour it and say so."""
    conf = cfg.normalise({"providers": {"a": {"base_url": "http://a/v1"}},
                          "models": {"m": {"endpoints": ["a/x"], "default": "m"},
                                     "n": {"endpoints": ["a/y"]}}}, {})
    assert conf["default"] == "m"
    assert conf["warnings"] and "belongs above the first table" in conf["warnings"][0]


def test_two_stray_defaults_is_an_error():
    with pytest.raises(cfg.ConfigError, match="appears inside several model tables"):
        cfg.normalise({"providers": {"a": {"base_url": "http://a/v1"}},
                       "models": {"m": {"endpoints": ["a/x"], "default": "m"},
                                  "n": {"endpoints": ["a/y"], "default": "n"}}}, {})
