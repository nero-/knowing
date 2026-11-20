#!/usr/bin/env python3
"""Endpoint configuration: named providers, then model names that point at them.

Two tables. Providers say *where* an endpoint is; models give that endpoint a name you actually say
out loud, with a pool for failover behind it.

    [providers.sparks]
    base_url = "http://100.120.4.113:8015/v1"

    [providers.tp2]
    base_url = "http://100.97.112.71:8000/v1"

    [providers.openrouter]
    base_url = "https://openrouter.ai/api/v1"
    api_key_env = "OPENROUTER_API_KEY"

    [providers.anthropic]
    kind = "anthropic"
    base_url = "https://api.anthropic.com"
    api_key_cmd = "pass show anthropic/key"

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

There is no tier vocabulary here: the names are yours, and `phases.yaml` (which already declares a
model per phase) can be mapped onto them with a `[phases]` entry. Credentials are never required
inline — `api_key`, `api_key_env`, or `api_key_cmd` (the same `!command` convention pi's models.json
uses), resolved when an endpoint is first used.

    python3 overlay/config.py check            # models, endpoints, and whether each key resolves
    python3 overlay/config.py check --probe    # + GET <base_url>/models on each endpoint
    python3 overlay/config.py from-pi ~/.pi/agent/models.json > ~/.config/knowing/models.toml
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

KINDS = ("openai", "anthropic")
DEFAULT_CONFIG_PATHS = (
    "~/.config/knowing/models.toml",
    "~/.config/knowing/models.json",
    "~/.config/knowing/tiers.toml",
    "~/.config/knowing/tiers.json",
    "~/.knowing/models.toml",
)
RESERVED = ("providers", "models", "tiers", "default", "phases")


class ConfigError(RuntimeError):
    pass


# ------------------------------------------------------------------ reading
def _read(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".toml":
        try:
            import tomllib
        except ModuleNotFoundError as exc:  # pragma: no cover - py<3.11
            raise ConfigError(
                f"{path} is TOML but this Python has no tomllib (3.11+); write JSON instead"
            ) from exc
        try:
            return tomllib.loads(text)
        except tomllib.TOMLDecodeError as exc:
            raise ConfigError(f"{path}: invalid TOML ({exc})") from exc
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ConfigError(f"{path}: invalid JSON ({exc.msg})") from exc


def find_config(env: dict[str, str] | None = None) -> Path | None:
    env = dict(os.environ if env is None else env)
    for var in ("KNOWING_CONFIG", "KNOWING_TIERS_FILE"):
        if env.get(var):
            p = Path(env[var]).expanduser()
            if not p.is_file():
                raise ConfigError(f"{var} points at a missing file: {p}")
            return p
    for cand in DEFAULT_CONFIG_PATHS:
        p = Path(cand).expanduser()
        if p.is_file():
            return p
    return None


def resolve_key(provider: dict, env: dict[str, str] | None = None,
                _cache: dict[str, str] | None = None) -> str:
    """literal → env var → command. Resolved lazily; commands are cached per command string."""
    env = dict(os.environ if env is None else env)
    _cache = {} if _cache is None else _cache
    name = provider.get("name", "?")
    if provider.get("api_key"):
        return str(provider["api_key"])
    if provider.get("api_key_env"):
        var = str(provider["api_key_env"])
        val = env.get(var)
        if not val:
            raise ConfigError(f"provider {name!r}: {var} is not set")
        return val
    if provider.get("api_key_cmd"):
        cmd = str(provider["api_key_cmd"])
        if cmd in _cache:
            return _cache[cmd]
        try:
            out = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=20)
        except (OSError, subprocess.SubprocessError) as exc:
            raise ConfigError(f"provider {name!r}: api_key_cmd failed ({exc})") from exc
        if out.returncode != 0 or not out.stdout.strip():
            raise ConfigError(
                f"provider {name!r}: api_key_cmd exited {out.returncode} with "
                f"{'no output' if not out.stdout.strip() else 'output'}: {out.stderr.strip()[:120]}")
        _cache[cmd] = out.stdout.strip()
        return _cache[cmd]
    # local servers (vLLM, Ollama, llama.cpp) accept any key; cloud ones fail loudly on first use
    return env.get("OPENAI_API_KEY") or "vllm"


def normalise(raw: dict, env: dict[str, str] | None = None) -> dict:
    """Validate a parsed config into {models, default, phases}, providers resolved."""
    env = dict(os.environ if env is None else env)
    providers = raw.get("providers") or {}
    if not isinstance(providers, dict):
        raise ConfigError("`providers` must be a table of name -> endpoint")
    prepared: dict[str, dict] = {}
    for name, spec in providers.items():
        if not isinstance(spec, dict):
            raise ConfigError(f"provider {name!r} must be a table")
        kind = str(spec.get("kind") or "openai")
        if kind not in KINDS:
            raise ConfigError(f"provider {name!r}: unknown kind {kind!r} (expected {KINDS})")
        base = str(spec.get("base_url") or "").rstrip("/")
        if not base:
            raise ConfigError(f"provider {name!r}: base_url is required")
        prepared[name] = {**spec, "name": name, "kind": kind, "base_url": base}

    # `models` is canonical; `tiers` was the earlier spelling and still loads.
    if "models" in raw:
        section = raw["models"]
    elif "tiers" in raw:
        section = raw["tiers"]
    else:
        section = {k: v for k, v in raw.items() if k not in RESERVED}
    if not isinstance(section, dict) or not section:
        raise ConfigError("no models configured — add a [models.<name>] table")

    models: dict[str, dict] = {}
    for name, spec in section.items():
        if not isinstance(spec, dict):
            raise ConfigError(f"model {name!r} must be a table")
        endpoints = spec.get("endpoints") or spec.get("endpoint") or []
        if isinstance(endpoints, str):
            endpoints = [endpoints]
        if not isinstance(endpoints, list) or not endpoints:
            raise ConfigError(f"model {name!r}: endpoints must be a non-empty list")
        rotate = str(spec.get("rotate") or "rr")
        if rotate not in ("rr", "sticky"):
            raise ConfigError(f"model {name!r}: rotate must be 'rr' or 'sticky'")
        models[name] = {"endpoints": [_candidate(e, name, prepared, env) for e in endpoints],
                        "rotate": rotate,
                        "fallback": list(spec.get("fallback") or [])}

    for name, spec in models.items():
        for alt in spec["fallback"]:
            if alt == name:
                raise ConfigError(f"model {name!r} lists itself as a fallback")
            if alt not in models:
                raise ConfigError(
                    f"model {name!r}: fallback {alt!r} is not configured (have: {', '.join(models)})")

    warnings: list[str] = []
    default = str(raw.get("default") or "")
    if not default:
        # TOML assigns a key to the table above it, so `default = "x"` written after
        # `[models.foo]` ends up inside that table. Honour it, and say so.
        strays = [(n, s.get("default")) for n, s in section.items()
                  if isinstance(s, dict) and s.get("default")]
        if len(strays) == 1:
            default = str(strays[0][1])
            warnings.append(
                f"`default` was read from inside [models.{strays[0][0]}] — in TOML it belongs "
                f"above the first table; move it to the top of the file")
        elif len(strays) > 1:
            raise ConfigError(
                f"`default` appears inside several model tables ({', '.join(n for n, _ in strays)}) "
                f"— put it once at the top of the file")
    if not default:
        default = next(iter(models))
    if default not in models:
        raise ConfigError(f"`default = {default!r}` is not a configured model ({', '.join(models)})")

    phases: dict[str, str] = {}
    raw_phases = raw.get("phases") or {}
    if not isinstance(raw_phases, dict):
        raise ConfigError("`phases` must be a table of phase id -> {model = \"<name>\"}")
    for pid, spec in raw_phases.items():
        model = spec.get("model") if isinstance(spec, dict) else str(spec)
        if not model:
            raise ConfigError(f'phases.{pid}: expected `model = "<name>"` or a bare name')
        if model not in models:
            raise ConfigError(
                f"phases.{pid} pins {model!r}, which is not configured ({', '.join(models)})")
        phases[str(pid)] = str(model)

    return {"models": models, "default": default, "phases": phases, "warnings": warnings}


def _candidate(entry, name: str, providers: dict[str, dict], env: dict[str, str]) -> dict[str, str]:
    if isinstance(entry, str):
        if "/" not in entry:
            raise ConfigError(
                f"model {name!r}: {entry!r} must be 'provider/model' "
                f"(providers available: {sorted(providers) or 'none'})")
        pname, model = entry.split("/", 1)
        if pname not in providers:
            raise ConfigError(
                f"model {name!r}: unknown provider {pname!r} in {entry!r} "
                f"(declared: {sorted(providers) or 'none'})")
        p = providers[pname]
        return {"provider": pname, "kind": p["kind"], "base_url": p["base_url"], "model": model,
                "api_key": resolve_key(p, env)}
    if isinstance(entry, dict):
        if "base_url" in entry and "model" in entry:  # inline one-off, still supported
            return {"provider": entry.get("provider", "inline"),
                    "kind": str(entry.get("kind") or "openai"),
                    "base_url": str(entry["base_url"]).rstrip("/"), "model": str(entry["model"]),
                    "api_key": resolve_key({"name": "inline", **entry}, env)}
        if entry.get("provider") and entry.get("model"):
            return _candidate(f"{entry['provider']}/{entry['model']}", name, providers, env)
    raise ConfigError(
        f"model {name!r}: an endpoint must be 'provider/model' or an object with base_url+model")


def load(env: dict[str, str] | None = None) -> dict:
    env = dict(os.environ if env is None else env)
    path = find_config(env)
    if path is None:
        raise ConfigError(
            "no config found — create ~/.config/knowing/models.toml (see docs/MODELS.md) "
            "or set KNOWING_CONFIG")
    return normalise(_read(path), env)


# ------------------------------------------------------------------ helpers
def from_pi_models(path: str | Path) -> str:
    """Turn pi's models.json into a starting knowing config."""
    data = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    provs = data.get("providers") or {}
    lines = ["# generated from pi models.json — edit the [models.*] section before using\n"]
    for name, spec in provs.items():
        lines.append(f"[providers.{name}]")
        lines.append(f'base_url = "{spec.get("baseUrl", "")}"')
        if spec.get("api") and not str(spec.get("api")).startswith("openai"):
            lines.append(f'kind = "{spec["api"]}"  # not openai-compatible: check this')
        key = spec.get("apiKey") or ""
        if key.startswith("!"):
            lines.append(f'api_key_cmd = {json.dumps(key[1:].strip())}')
        elif key:
            lines.append(f'api_key = {json.dumps(key)}')
        models = [m.get("id") for m in (spec.get("models") or []) if m.get("id")]
        if models:
            lines.append("models = [" + ", ".join(json.dumps(m) for m in models) + "]")
        lines.append("")
    first, first_models = next(iter(provs.items()), (None, {}))
    if first:
        ids = [m.get("id") for m in (first_models.get("models") or []) if m.get("id")]
        ref = f"{first}/{ids[0]}" if ids else f"{first}/MODEL"
        lines += ['[models.default]', f'endpoints = ["{ref}"]', "", "default = \"default\"", "",
                  "# optional: pin a phase from phases.yaml",
                  '# [phases."6"]', '# model = "default"', ""]
    return "\n".join(lines)


def probe(candidates: list[dict], timeout: float = 3.0) -> list[dict]:
    """GET <base_url>/models for each candidate. Facts only; no judgement."""
    import urllib.error
    import urllib.request

    out = []
    for c in candidates:
        url = c["base_url"].rstrip("/") + "/models"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {c['api_key']}"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:  # noqa: S310
                body = r.read(4000).decode("utf-8", "replace")
            ids = []
            try:
                ids = [m.get("id") for m in json.loads(body).get("data", []) if m.get("id")]
            except Exception:  # noqa: BLE001
                pass
            out.append({**c, "status": r.status, "served": ids})
        except urllib.error.HTTPError as exc:
            out.append({**c, "status": exc.code, "served": [], "error": exc.reason})
        except Exception as exc:  # noqa: BLE001
            out.append({**c, "status": None, "served": [], "error": type(exc).__name__})
    return out


# ---------------------------------------------------------------------- CLI
def main(argv: list[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description="knowing endpoint configuration")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="show configured models and whether keys resolve")
    c.add_argument("--probe", action="store_true", help="GET <base_url>/models on every endpoint")
    c.add_argument("--config", type=Path, help="config path (default: $KNOWING_CONFIG or ~/.config/knowing/models.toml)")
    f = sub.add_parser("from-pi", help="emit a starting config from pi's models.json")
    f.add_argument("path", type=Path)
    args = ap.parse_args(argv)

    if args.cmd == "from-pi":
        print(from_pi_models(args.path))
        return 0

    try:
        env = dict(os.environ)
        path = args.config or find_config(env)
        if path is None:
            raise ConfigError("no config found — see docs/MODELS.md")
        cfg = normalise(_read(path), env)
    except ConfigError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"config: {path}   default={cfg['default']}")
    for w in cfg.get("warnings") or []:
        print(f"note: {w}")
    for name, spec in cfg["models"].items():
        fb = f" → {','.join(spec['fallback'])}" if spec["fallback"] else ""
        pinned = [p for p, m in cfg["phases"].items() if m == name]
        pin = f"  pinned by phase {','.join(pinned)}" if pinned else ""
        print(f"\n{name}  (rotate={spec['rotate']}{fb}){pin}")
        rows = spec["endpoints"]
        if args.probe:
            rows = probe(rows)
        for r in rows:
            tail = ""
            if "status" in r:
                tail = f"  [{r['status']}]"
                if r["served"]:
                    tail += f" serves {len(r['served'])} model(s)"
                    if r["model"] not in r["served"]:
                        tail += f" — WARNING: {r['model']!r} not in the list"
                elif r.get("error"):
                    tail += f" {r['error']}"
            print(f"  {r['provider']:<12} {r['model']:<28} {r['base_url']}{tail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
