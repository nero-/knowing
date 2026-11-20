#!/usr/bin/env python3
"""Tier routing: map deepdive's model *tiers* onto concrete endpoints.

Upstream's runner asks for a tier — `strong`, `mid`, `cheap` — and never names a model. This module
answers that request with an endpoint, and it does so with three rules:

1. **A tier is a pool, not a machine.** Each tier holds one or more interchangeable candidates.
   A cluster going down rotates to the next candidate instead of turning the run red.
2. **Health is passive, not polled.** An endpoint is marked unhealthy only by a request that failed
   in a way that means "try elsewhere": connection error, timeout, 429, 5xx. No probe calls, no
   surprise spend. Recovery is automatic after a cooldown that doubles while it keeps failing.
3. **Every decision is recorded.** `routed` names the tier, the endpoint, the model, and why the
   call landed there. A degraded run is auditable; a hidden one is not.

Rotation policy is per tier, because the right answer differs:

    rotate: "rr"      round-robin per call — right for the fan-out, where calls are independent and
                      no prefix cache survives anyway
    rotate: "sticky"  one candidate for the whole process — right for planning/synthesis, where
                      switching models mid-run loses the prompt cache and can change quality
                      between two steps that must agree

Config, first match wins: KNOWING_TIERS (inline JSON) → KNOWING_TIERS_FILE → per-tier env vars.

    {"strong": {"endpoints": [{"base_url": "...", "model": "..."},
                              {"base_url": "...", "model": "..."}],
                "rotate": "sticky",
                "fallback": ["mid"]},
     "cheap":  {"endpoints": [{"base_url": "...", "model": "..."}]}}

Back-compatible: a tier may also be a single `{"base_url", "model", "api_key"}` object, or a bare
list of such objects.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

TIERS = ("strong", "mid", "cheap")
DEFAULT_FALLBACK = {"strong": ("mid", "cheap"), "mid": ("cheap",), "cheap": ()}
TRANSIENT_STATUS = {408, 409, 425, 429, 500, 502, 503, 504}
TRANSIENT_NAMES = ("RateLimit", "Timeout", "APIConnection", "Overloaded", "ServiceUnavailable",
                   "InternalServer", "ConnectionError")
COOLDOWN_BASE = 30.0
COOLDOWN_MAX = 300.0


class TierConfigError(RuntimeError):
    pass


def _candidate(raw: dict, tier: str, env: dict[str, str]) -> dict[str, str]:
    base = (raw.get("base_url") or "").rstrip("/")
    model = raw.get("model") or ""
    if not base:
        raise TierConfigError(
            f"tier {tier!r}: a candidate has no base_url — set KNOWING_TIER_{tier.upper()}_BASE_URL "
            f"or add it to KNOWING_TIERS")
    if not model:
        raise TierConfigError(
            f"tier {tier!r}: a candidate has no model — set KNOWING_TIER_{tier.upper()}_MODEL "
            f"or add it to KNOWING_TIERS")
    return {"base_url": base, "model": model,
            "api_key": raw.get("api_key") or env.get("OPENAI_API_KEY") or "vllm"}


def load_tiers(env: dict[str, str] | None = None) -> dict[str, dict]:
    """Resolve tier -> {endpoints: [...], rotate: str, fallback: [...]}.

    A config file wins (providers + tiers, see overlay/config.py); otherwise the KNOWING_TIERS
    environment JSON is used, which keeps the earlier shape working.
    """
    env = dict(os.environ if env is None else env)
    try:
        from overlay import config as _config
    except ModuleNotFoundError:
        import config as _config
    if _config.find_config(env) is not None:
        return _config.load(env)
    raw: dict[str, object] = {}
    blob = env.get("KNOWING_TIERS") or ""
    if not blob and env.get("KNOWING_TIERS_FILE"):
        path = Path(env["KNOWING_TIERS_FILE"]).expanduser()
        if not path.is_file():
            raise TierConfigError(f"KNOWING_TIERS_FILE points at a missing file: {path}")
        blob = path.read_text(encoding="utf-8")
    if blob:
        try:
            parsed = json.loads(blob)
        except json.JSONDecodeError as exc:
            raise TierConfigError(f"tier config is not valid JSON ({exc.msg})") from exc
        if not isinstance(parsed, dict):
            raise TierConfigError("tier config must be an object of tier -> endpoints")
        for tier, cfg in parsed.items():
            if tier not in TIERS:
                raise TierConfigError(f"unknown tier {tier!r} (expected one of {TIERS})")
            raw[tier] = cfg
    for tier in TIERS:  # per-tier env vars add or extend
        prefix = f"KNOWING_TIER_{tier.upper()}_"
        base, model = env.get(prefix + "BASE_URL"), env.get(prefix + "MODEL")
        if base or model:
            if tier in raw:
                raise TierConfigError(
                    f"tier {tier!r} is configured twice (config file and {prefix}* vars) — pick one")
            raw[tier] = {"base_url": base or "", "model": model or "",
                         "api_key": env.get(prefix + "API_KEY") or ""}
    out: dict[str, dict] = {}
    for tier, cfg in raw.items():
        rotate, fallback, endpoints = "rr", list(DEFAULT_FALLBACK[tier]), None
        if isinstance(cfg, dict) and "endpoints" in cfg:
            endpoints = cfg["endpoints"]
            rotate = str(cfg.get("rotate") or rotate)
            if "fallback" in cfg:
                fallback = list(cfg["fallback"] or [])
        elif isinstance(cfg, list):
            endpoints = cfg
        elif isinstance(cfg, dict):
            endpoints = [cfg]
        else:
            raise TierConfigError(f"tier {tier!r} must be an object, a list, or {{endpoints: [...]}}")
        if not isinstance(endpoints, list) or not endpoints:
            raise TierConfigError(f"tier {tier!r} has no endpoints")
        if rotate not in ("rr", "sticky"):
            raise TierConfigError(f"tier {tier!r}: rotate must be 'rr' or 'sticky', got {rotate!r}")
        for t in fallback:
            if t not in TIERS:
                raise TierConfigError(f"tier {tier!r}: unknown fallback tier {t!r}")
            if t == tier:
                raise TierConfigError(f"tier {tier!r} lists itself as a fallback")
        cands = [_candidate(c, tier, env) if isinstance(c, dict) else
                 (_ for _ in ()).throw(TierConfigError(f"tier {tier!r}: candidate must be an object"))
                 for c in endpoints]
        out[tier] = {"endpoints": cands, "rotate": rotate, "fallback": fallback}
    if not out:
        raise TierConfigError(
            "no tiers configured — set KNOWING_TIERS (JSON), KNOWING_TIERS_FILE, or "
            "KNOWING_TIER_STRONG_BASE_URL / _MODEL and their mid/cheap counterparts")
    return out


def is_transient(exc: BaseException) -> bool:
    """Would trying a *different* endpoint plausibly help?"""
    status = getattr(exc, "status_code", None) or getattr(exc, "status", None)
    if isinstance(status, int) and status in TRANSIENT_STATUS:
        return True
    if isinstance(exc, (ConnectionError, TimeoutError, OSError)):
        return True
    return any(name in type(exc).__name__ for name in TRANSIENT_NAMES)


class TierMapProvider:
    """An LLMProvider that pools endpoints per tier and fails over between them.

    Delegates the call shape to upstream's `OpenAICompatProvider`, so request formatting, JSON
    handling and per-endpoint concurrency stay in one place. One client per endpoint, reused.
    """

    name = "tiers"

    def __init__(self, tiers: dict[str, dict] | None = None, *, max_concurrency: int = 5,
                 client_factory=None, clock=time.monotonic):
        self.tiers = _normalise(tiers if tiers is not None else load_tiers())
        self.max_concurrency = max_concurrency
        self._client_factory = client_factory
        self._clock = clock
        self._providers: dict[tuple[str, str], object] = {}
        self._cursor: dict[str, int] = {}
        self._sticky: dict[str, tuple[int, str]] = {}  # tier -> (index, key)
        self._down: dict[tuple[str, str], tuple[float, int]] = {}  # key -> (until, streak)
        self.routed: list[dict] = []

    # -- health ---------------------------------------------------------------
    def _key(self, cfg: dict[str, str]) -> tuple[str, str, str]:
        return (cfg.get("kind") or "openai", cfg["base_url"], cfg["api_key"])

    def _available(self, cfg: dict[str, str]) -> bool:
        until, _ = self._down.get(self._key(cfg), (0.0, 0))
        return self._clock() >= until

    def _mark_down(self, cfg: dict[str, str]) -> None:
        key = self._key(cfg)
        _, streak = self._down.get(key, (0.0, 0))
        streak += 1
        cooldown = min(COOLDOWN_BASE * (2 ** (streak - 1)), COOLDOWN_MAX)
        self._down[key] = (self._clock() + cooldown, streak)

    def _mark_up(self, cfg: dict[str, str]) -> None:
        self._down.pop(self._key(cfg), None)

    # -- selection -------------------------------------------------------------
    def _order(self, tier: str) -> list[tuple[int, dict[str, str]]]:
        """Candidates for a tier in the order this call should try them."""
        if tier not in self.tiers:
            raise TierConfigError(f"no endpoint for tier {tier!r} and no configured fallback")
        spec = self.tiers[tier]
        cands = spec["endpoints"]
        if spec["rotate"] == "sticky" and tier in self._sticky:
            idx, _ = self._sticky[tier]
            order = [idx] + [i for i in range(len(cands)) if i != idx]
        else:
            start = self._cursor.get(tier, 0) % len(cands)
            order = [(start + i) % len(cands) for i in range(len(cands))]
            if spec["rotate"] == "rr":
                self._cursor[tier] = (start + 1) % len(cands)
        healthy = [(i, cands[i]) for i in order if self._available(cands[i])]
        return healthy or [(i, cands[i]) for i in order]  # all cooling down: try anyway, in order

    def _provider(self, cfg: dict[str, str]):
        """Build (once) the right client class for this endpoint's dialect."""
        from runner.providers import ClaudeProvider, OpenAICompatProvider  # upstream, unchanged

        key = self._key(cfg)
        if key not in self._providers:
            kind = cfg.get("kind") or "openai"
            if self._client_factory is not None:
                client = self._client_factory(cfg["base_url"], cfg["api_key"])
            else:
                client = _anthropic_client(cfg) if kind == "anthropic" else _openai_client(cfg)
            if kind == "anthropic":
                self._providers[key] = ClaudeProvider(client=client,
                                                      model_override=cfg["model"],
                                                      max_concurrency=self.max_concurrency)
            else:
                self._providers[key] = OpenAICompatProvider(
                    client=client, base_url=cfg["base_url"],
                    model_override=cfg["model"], max_concurrency=self.max_concurrency)
        return self._providers[key]

    def _attempt(self, tier: str, fn) -> object:
        """Try candidates of `tier` in order, then its fallback tiers. One try each."""
        if tier not in self.tiers:
            raise TierConfigError(f"no endpoint for tier {tier!r} and no configured fallback")
        errors: list[str] = []
        for tier_name in (tier, *self.tiers[tier].get("fallback", ())):
            try:
                order = self._order(tier_name)
            except TierConfigError as exc:
                errors.append(str(exc))
                continue
            for idx, cfg in order:
                try:
                    result = fn(self._provider(cfg))
                except BaseException as exc:  # noqa: BLE001 — classified below
                    if not is_transient(exc):
                        self.routed.append({"tier": tier_name, "index": idx, "model": cfg["model"],
                                            "base_url": cfg["base_url"], "reason": "error",
                                            "error": type(exc).__name__})
                        raise
                    self._mark_down(cfg)
                    errors.append(f"{tier_name}[{idx}] {cfg['model']}: {type(exc).__name__}")
                    self.routed.append({"tier": tier_name, "index": idx, "model": cfg["model"],
                                        "base_url": cfg["base_url"], "reason": "failover",
                                        "error": type(exc).__name__})
                    continue
                self._mark_up(cfg)
                if self.tiers[tier_name]["rotate"] == "sticky":
                    self._sticky.setdefault(tier_name, (idx, cfg["base_url"]))
                self.routed.append({"tier": tier_name, "index": idx, "model": cfg["model"],
                                    "base_url": cfg["base_url"],
                                    "reason": "ok" if tier_name == tier else f"fallback-from-{tier}"})
                return result
        raise RuntimeError(
            f"no endpoint answered for tier {tier!r} (tried {len(errors)}): {'; '.join(errors)}")

    # -- LLMProvider surface ---------------------------------------------------
    def _model_for(self, tier: str) -> str:
        return self._order(tier)[0][1]["model"]

    def complete(self, prompt: str, *, system: str = "", model_tier: str = "mid") -> str:
        return self._attempt(model_tier,
                             lambda p: p.complete(prompt, system=system, model_tier="mid"))

    def fanout(self, tasks: list[str], *, model_tier: str = "cheap") -> list[str]:
        return self._attempt(model_tier, lambda p: p.fanout(tasks, model_tier="cheap"))

    def score(self, sources: list[dict], hypotheses: list[str], *,
              model_tier: str = "cheap") -> dict:
        return self._attempt(model_tier, lambda p: p.score(sources, hypotheses,
                                                           model_tier="cheap"))

    def search(self, subquery: str, *, subquestion_id: str = "Q0", model_tier: str = "cheap") -> dict:
        raise NotImplementedError(
            "web_search is Anthropic-specific; TierMapProvider routes completions only. "
            "Run the fan-out with a search-capable provider, or supply your own fetcher.")


def _normalise(tiers: dict[str, dict]) -> dict[str, dict]:
    """Give every candidate a base_url/model/api_key, whatever shape the caller passed."""
    out: dict[str, dict] = {}
    for tier, spec in tiers.items():
        endpoints = spec.get("endpoints") or []
        cleaned = []
        for cand in endpoints:
            base = str(cand.get("base_url") or "").rstrip("/")
            model = str(cand.get("model") or "")
            if not base or not model:
                raise TierConfigError(f"tier {tier!r}: every candidate needs base_url and model")
            cleaned.append({"base_url": base, "model": model,
                            "provider": cand.get("provider") or "inline",
                            "kind": cand.get("kind") or "openai",
                            "api_key": cand.get("api_key") or os.environ.get("OPENAI_API_KEY") or "vllm"})
        out[tier] = {"endpoints": cleaned,
                     "rotate": spec.get("rotate") or "rr",
                     "fallback": list(spec.get("fallback") or [])}
    return out


def _openai_client(cfg: dict[str, str]):
    import openai
    return openai.OpenAI(base_url=cfg["base_url"], api_key=cfg["api_key"])


def _anthropic_client(cfg: dict[str, str]):
    import anthropic
    return anthropic.Anthropic(api_key=cfg["api_key"])


def build_from_env() -> TierMapProvider:
    return TierMapProvider(load_tiers())
