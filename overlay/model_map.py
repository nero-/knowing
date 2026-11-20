#!/usr/bin/env python3
"""Model mapping: answer "which endpoint serves this model?" — no tiers, no policy list.

The question this module answers is narrow on purpose. Who decides *which* model does a piece of work?

1. **The methodology.** `phases.yaml` already declares a model per phase (`opus`, `sonnet`, …). That is
   the real routing table, written by a human, in the file that defines the work.
2. **The agent**, per call, when it has a reason: pass a model name and it is honoured.
3. **The config's `default`**, when nobody said anything.

What this module adds underneath is the boring part nobody should have to think about: a name resolves
to one or more interchangeable endpoints, a dead endpoint fails over, a transient failure cools down,
and every decision is recorded. There is no tier list — the keys are whatever names you use.

    [providers.sparks]
    base_url = "http://100.120.4.113:8015/v1"

    [providers.tp2]
    base_url = "http://100.97.112.71:8000/v1"

    [models.opus]                       # a name you (and phases.yaml) already use
    endpoints = ["sparks/DeepSeek-V4.1-Flash", "openrouter/anthropic/claude-opus-5"]
    rotate = "sticky"                   # sticky: one model per process, prompt cache survives
    fallback = ["sonnet"]

    [models.sonnet]
    endpoints = ["tp2/Qwen3.8-Flash-Next"]

    [models.haiku]                       # fan-out; rr: spread load across the pool
    endpoints = ["tp2/Qwen3.8-Flash-Next", "ollama/qwen3:8b"]
    rotate = "rr"

    default = "sonnet"

    [phases."6"]                         # optional: pin a phase, by its phases.yaml id
    model = "opus"

Resolution order: explicit name → phase override → `default` → error naming the names you do have.
An unknown name is an error, never a silent guess: a typo must not quietly reroute a synthesis step.
"""

from __future__ import annotations

import time

TRANSIENT_STATUS = {408, 409, 425, 429, 500, 502, 503, 504}
TRANSIENT_NAMES = ("RateLimit", "Timeout", "APIConnection", "Overloaded", "ServiceUnavailable",
                   "InternalServer", "ConnectionError")
COOLDOWN_BASE = 30.0
COOLDOWN_MAX = 300.0


class ModelConfigError(RuntimeError):
    """Raised for an unresolvable name, a bad pool, or an exhausted set of endpoints."""


class _Exhausted(RuntimeError):
    """Internal: every candidate for a name failed transiently."""


def is_transient(exc: BaseException) -> bool:
    """Would trying a *different* endpoint plausibly help?"""
    status = getattr(exc, "status_code", None) or getattr(exc, "status", None)
    if isinstance(status, int) and status in TRANSIENT_STATUS:
        return True
    if isinstance(exc, (ConnectionError, TimeoutError, OSError)):
        return True
    return any(name in type(exc).__name__ for name in TRANSIENT_NAMES)


class ModelMap:
    """Resolves a model name to an endpoint, with failover, cooldown and an audit trail.

    Implements upstream's `LLMProvider` protocol, so the runner cannot tell the difference between
    this and a single-endpoint provider. `model_tier` is upstream's parameter name; here its value is
    a model name from your config (or "" for the default).
    """

    name = "models"

    def __init__(self, cfg: dict, *, max_concurrency: int = 5, client_factory=None,
                 clock=time.monotonic):
        self.models: dict[str, dict] = cfg["models"]
        self.default: str = cfg.get("default") or next(iter(self.models), "")
        self.phases: dict[str, str] = cfg.get("phases") or {}
        self.max_concurrency = max_concurrency
        self._client_factory = client_factory
        self._clock = clock
        self._providers: dict[tuple[str, str, str], object] = {}
        self._cursor: dict[str, int] = {}
        self._sticky: dict[str, int] = {}
        self._down: dict[tuple[str, str, str], tuple[float, int]] = {}
        self.routed: list[dict] = []

    # -- naming ----------------------------------------------------------------
    def names(self) -> list[str]:
        return sorted(self.models)

    def resolve(self, requested: str = "", *, phase: str | None = None) -> str:
        """Name → configured name. Explicit wins, then phase, then default. Never guesses."""
        if requested:
            if requested not in self.models:
                raise ModelConfigError(
                    f"unknown model {requested!r} — configured names: {', '.join(self.names())}")
            return requested
        if phase and phase in self.phases:
            pinned = self.phases[phase]
            if pinned not in self.models:
                raise ModelConfigError(
                    f"phase {phase!r} pins model {pinned!r}, which is not configured "
                    f"({', '.join(self.names())})")
            return pinned
        if self.default in self.models:
            return self.default
        raise ModelConfigError(
            "no model requested and no usable `default` — set `default = \"<name>\"` in the config, "
            f"or name one of: {', '.join(self.names())}")

    # -- health ----------------------------------------------------------------
    def _key(self, cfg: dict[str, str]) -> tuple[str, str, str]:
        return (cfg.get("kind") or "openai", cfg["base_url"], cfg["api_key"])

    def _available(self, cfg: dict[str, str]) -> bool:
        until, _ = self._down.get(self._key(cfg), (0.0, 0))
        return self._clock() >= until

    def _mark_down(self, cfg: dict[str, str]) -> None:
        key = self._key(cfg)
        _, streak = self._down.get(key, (0.0, 0))
        streak += 1
        self._down[key] = (self._clock() + min(COOLDOWN_BASE * 2 ** (streak - 1), COOLDOWN_MAX), streak)

    def _mark_up(self, cfg: dict[str, str]) -> None:
        self._down.pop(self._key(cfg), None)

    # -- selection -------------------------------------------------------------
    def _order(self, name: str) -> list[tuple[int, dict[str, str]]]:
        spec = self.models[name]
        cands = spec["endpoints"]
        if spec["rotate"] == "sticky" and name in self._sticky:
            idx = self._sticky[name]
            order = [idx] + [i for i in range(len(cands)) if i != idx]
        else:
            start = self._cursor.get(name, 0) % len(cands)
            order = [(start + i) % len(cands) for i in range(len(cands))]
            if spec["rotate"] == "rr":
                self._cursor[name] = (start + 1) % len(cands)
        healthy = [(i, c) for i, c in ((i, cands[i]) for i in order) if self._available(c)]
        return healthy or [(i, cands[i]) for i in order]

    def _provider(self, cfg: dict[str, str]):
        from runner.providers import ClaudeProvider, OpenAICompatProvider  # upstream, unchanged

        key = self._key(cfg)
        if key not in self._providers:
            if self._client_factory is not None:
                client = self._client_factory(cfg["base_url"], cfg["api_key"])
            else:
                client = _anthropic_client(cfg) if cfg.get("kind") == "anthropic" else _openai_client(cfg)
            if cfg.get("kind") == "anthropic":
                self._providers[key] = ClaudeProvider(client=client, model_override=cfg["model"],
                                                      max_concurrency=self.max_concurrency)
            else:
                self._providers[key] = OpenAICompatProvider(
                    client=client, base_url=cfg["base_url"], model_override=cfg["model"],
                    max_concurrency=self.max_concurrency)
        return self._providers[key]

    def _attempt(self, requested: str, fn, *, phase: str | None = None):
        start = self.resolve(requested, phase=phase)
        errors: list[str] = []
        queue: list[tuple[str, str]] = [(start, "ok")]
        seen = {start}
        while queue:
            name, reason = queue.pop(0)
            for idx, cfg in self._order(name):
                try:
                    result = fn(self._provider(cfg))
                except BaseException as exc:  # noqa: BLE001 — classified below
                    if not is_transient(exc):
                        self.routed.append({"name": name, "index": idx, "model": cfg["model"],
                                            "base_url": cfg["base_url"], "reason": "error",
                                            "error": type(exc).__name__})
                        raise
                    self._mark_down(cfg)
                    errors.append(f"{name}[{idx}] {cfg['model']}: {type(exc).__name__}")
                    self.routed.append({"name": name, "index": idx, "model": cfg["model"],
                                        "base_url": cfg["base_url"], "reason": "failover",
                                        "error": type(exc).__name__})
                    continue
                self._mark_up(cfg)
                if self.models[name]["rotate"] == "sticky":
                    self._sticky.setdefault(name, idx)
                self.routed.append({"name": name, "index": idx, "model": cfg["model"],
                                    "base_url": cfg["base_url"], "reason": reason})
                return result
            for alt in self.models[name]["fallback"]:
                if alt not in seen:
                    seen.add(alt)
                    queue.append((alt, f"fallback-from-{name}"))
        raise _Exhausted(
            f"no endpoint answered for model {start!r} (tried {len(errors)}): {'; '.join(errors)}")

    # -- LLMProvider surface ---------------------------------------------------
    def _model_for(self, name: str) -> str:
        return self._order(self.resolve(name))[0][1]["model"]

    def complete(self, prompt: str, *, system: str = "", model_tier: str = "") -> str:
        return self._attempt(model_tier, lambda p: p.complete(prompt, system=system,
                                                             model_tier="mid"))
    def fanout(self, tasks: list[str], *, model_tier: str = "") -> list[str]:
        return self._attempt(model_tier, lambda p: p.fanout(tasks, model_tier="cheap"))

    def score(self, sources: list[dict], hypotheses: list[str], *, model_tier: str = "") -> dict:
        return self._attempt(model_tier, lambda p: p.score(sources, hypotheses, model_tier="cheap"))

    def search(self, subquery: str, *, subquestion_id: str = "Q0", model_tier: str = "") -> dict:
        raise NotImplementedError(
            "web_search is Anthropic-specific; ModelMap routes completions only. "
            "Run the fan-out with a search-capable provider, or supply your own fetcher.")


def _openai_client(cfg: dict[str, str]):
    import openai
    return openai.OpenAI(base_url=cfg["base_url"], api_key=cfg["api_key"])


def _anthropic_client(cfg: dict[str, str]):
    import anthropic
    return anthropic.Anthropic(api_key=cfg["api_key"])


def build_from_env() -> ModelMap:
    import config as _config
    return ModelMap(_config.load())
