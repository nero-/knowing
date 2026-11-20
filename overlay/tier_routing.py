#!/usr/bin/env python3
"""Tier routing: map deepdive's model *tiers* onto concrete endpoints.

Upstream's runner asks for a tier — `strong`, `mid`, `cheap` — and never names a model.
`OpenAICompatProvider` maps tiers to one endpoint with hard-coded model names. That is the wrong
shape when the tiers live on *different machines*: a 1M-context box for planning and synthesis, a
256k box for the fan-out, each with its own queue and its own cost.

This module is the mapping layer, and nothing more:

    strong  ->  the long-context, expensive endpoint   (planning, synthesis, adjudication)
    mid     ->  the everyday endpoint                  (reads, verification)
    cheap   ->  the high-volume endpoint               (fan-out, screening, extraction)

Configuration, first match wins:

    KNOWING_TIERS            inline JSON, e.g. {"strong": {"base_url": "...", "model": "..."}, ...}
    KNOWING_TIERS_FILE       path to the same JSON
    KNOWING_TIER_<TIER>_BASE_URL / _MODEL / _API_KEY     per-tier env vars

A tier that is not configured falls back to the next cheaper tier that is (strong -> mid -> cheap),
so a partial configuration still runs and says so. Nothing here reads a credential file or guesses a
default endpoint: a missing base URL is an error that names the variable.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

TIERS = ("strong", "mid", "cheap")
FALLBACK = {"strong": ("mid", "cheap"), "mid": ("cheap",), "cheap": ()}


class TierConfigError(RuntimeError):
    pass


def load_tiers(env: dict[str, str] | None = None) -> dict[str, dict[str, str]]:
    """Resolve tier -> {base_url, model, api_key}. Returns only configured tiers."""
    env = dict(os.environ if env is None else env)
    raw: dict[str, dict[str, str]] = {}
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
            raise TierConfigError("tier config must be an object of tier -> {base_url, model}")
        for tier, cfg in parsed.items():
            if tier not in TIERS:
                raise TierConfigError(f"unknown tier {tier!r} (expected one of {TIERS})")
            if not isinstance(cfg, dict):
                raise TierConfigError(f"tier {tier!r} must be an object")
            raw[tier] = {k: str(v) for k, v in cfg.items() if v is not None}
    for tier in TIERS:
        prefix = f"KNOWING_TIER_{tier.upper()}_"
        for key, field in (("BASE_URL", "base_url"), ("MODEL", "model"), ("API_KEY", "api_key")):
            val = env.get(prefix + key)
            if val:
                raw.setdefault(tier, {})[field] = val
    out: dict[str, dict[str, str]] = {}
    for tier, cfg in raw.items():
        base = (cfg.get("base_url") or "").rstrip("/")
        model = cfg.get("model") or ""
        if not base:
            raise TierConfigError(
                f"tier {tier!r} has no base_url — set KNOWING_TIER_{tier.upper()}_BASE_URL "
                f"or add it to KNOWING_TIERS")
        if not model:
            raise TierConfigError(
                f"tier {tier!r} has no model — set KNOWING_TIER_{tier.upper()}_MODEL "
                f"or add it to KNOWING_TIERS")
        out[tier] = {"base_url": base, "model": model,
                     "api_key": cfg.get("api_key") or env.get("OPENAI_API_KEY") or "vllm"}
    if not out:
        raise TierConfigError(
            "no tiers configured — set KNOWING_TIERS (JSON), KNOWING_TIERS_FILE, or "
            "KNOWING_TIER_STRONG_BASE_URL / _MODEL and their mid/cheap counterparts")
    return out


def resolve_tier(tier: str, tiers: dict[str, dict[str, str]]) -> tuple[str, dict[str, str]]:
    """Return (effective tier, config), walking down the fallback chain."""
    if tier not in TIERS:
        raise TierConfigError(f"unknown tier {tier!r} (expected one of {TIERS})")
    for candidate in (tier, *FALLBACK[tier]):
        if candidate in tiers:
            return candidate, tiers[candidate]
    raise TierConfigError(
        f"no endpoint for tier {tier!r}: configure it or one of {FALLBACK[tier] or ('—',)}")


class TierMapProvider:
    """An LLMProvider that sends each tier to its own endpoint.

    Delegates the actual call shape to upstream's OpenAICompatProvider, so request formatting,
    concurrency and JSON handling stay in one place. One client per (base_url, api_key), so a
    fan-out of twenty cheap tasks shares a connection pool instead of opening twenty.
    """

    name = "tiers"

    def __init__(self, tiers: dict[str, dict[str, str]] | None = None, *,
                 max_concurrency: int = 5, client_factory=None):
        self.tiers = tiers if tiers is not None else load_tiers()
        self.max_concurrency = max_concurrency
        self._client_factory = client_factory
        self._providers: dict[tuple[str, str], object] = {}
        self.routed: list[tuple[str, str, str]] = []  # (tier, base_url, model) per call

    def _provider(self, tier: str):
        from runner.providers import OpenAICompatProvider  # upstream, unchanged

        effective, cfg = resolve_tier(tier, self.tiers)
        api_key = cfg.get("api_key") or os.environ.get("OPENAI_API_KEY") or "vllm"
        key = (cfg["base_url"], api_key)
        if key not in self._providers:
            client = None
            if self._client_factory is not None:
                client = self._client_factory(cfg["base_url"], api_key)
            else:
                import openai
                client = openai.OpenAI(base_url=cfg["base_url"], api_key=api_key)
            self._providers[key] = OpenAICompatProvider(
                client=client, base_url=cfg["base_url"],
                model_override=cfg["model"], max_concurrency=self.max_concurrency)
        self.routed.append((effective, cfg["base_url"], cfg["model"]))
        return self._providers[key]

    def _model_for(self, tier: str) -> str:
        _, cfg = resolve_tier(tier, self.tiers)
        return cfg["model"]

    def complete(self, prompt: str, *, system: str = "", model_tier: str = "mid") -> str:
        return self._provider(model_tier).complete(prompt, system=system, model_tier="mid")

    def fanout(self, tasks: list[str], *, model_tier: str = "cheap") -> list[str]:
        return self._provider(model_tier).fanout(tasks, model_tier="cheap")

    def score(self, sources: list[dict], hypotheses: list[str], *,
              model_tier: str = "cheap") -> dict:
        return self._provider(model_tier).score(sources, hypotheses, model_tier="cheap")

    def search(self, subquery: str, *, subquestion_id: str = "Q0", model_tier: str = "cheap") -> dict:
        raise NotImplementedError(
            "web_search is Anthropic-specific; TierMapProvider routes completions only. "
            "Run the fan-out with a search-capable provider, or supply your own fetcher.")


def build_from_env() -> TierMapProvider:
    return TierMapProvider(load_tiers())
