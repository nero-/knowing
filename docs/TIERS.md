# Model tiers → endpoints

Upstream's runner never names a model. It asks for a **tier** (the methodology says "strong/mid/cheap"),
and the provider maps the tier to whatever hardware you have. That means the same skill runs on one
big box, two small ones, or a mixture — and the split is a config file, not a fork.

`overlay/tier_routing.py` does the mapping. Three ways to configure it, first match wins:

```bash
# 1. inline JSON
export KNOWING_TIERS='{
  "strong": {"base_url": "http://100.120.4.113:8015/v1", "model": "DeepSeek-V4.1-Flash"},
  "mid":    {"base_url": "http://100.97.112.71:8000/v1",  "model": "Qwen3.8-Flash-Next"},
  "cheap":  {"base_url": "http://100.97.112.71:8000/v1",  "model": "Qwen3.8-Flash-Next"}
}'

# 2. a file (same JSON), easier to keep out of your shell history
export KNOWING_TIERS_FILE=~/.config/knowing/tiers.json

# 3. per-tier environment variables
export KNOWING_TIER_STRONG_BASE_URL=http://100.120.4.113:8015/v1
export KNOWING_TIER_STRONG_MODEL=DeepSeek-V4.1-Flash
export KNOWING_TIER_CHEAP_BASE_URL=http://100.97.112.71:8000/v1
export KNOWING_TIER_CHEAP_MODEL=Qwen3.8-Flash-Next
export OPENAI_API_KEY=vllm          # used for every tier that has no api_key of its own
```

Then `--provider tiers`. The provider is an ordinary OpenAI-compatible client per endpoint: vLLM,
Ollama, OpenRouter, a gateway — anything speaking `/v1`.

## Why tiers, not per-phase model names

The methodology's own routing table is the authority on *which* work is expensive: reframing, the
plan gate, and the adversarial pass are `strong`; search fan-out and mechanical scoring are `cheap`.
Encoding that as hardware means the split survives a model change, and re-balancing is a config edit.

The two things that should drive your mapping, in order:

1. **Context window.** Planning and synthesis hold the fan-in. If one endpoint has a materially
   larger window, that is the `strong` tier regardless of speed — a synthesis step that gets compacted
   mid-way is worse than a slow one.
2. **Queue depth.** The `cheap` tier is where a run's parallelism lands (`MIN_CANDIDATES` of 60–100 at
   medium, the fetcher pool at 3–6 agents). Put it on the endpoint with the most headroom, and check
   what its server advertises — vLLM-style gateways often publish a concurrency limit you can read
   from `/v1/models`.

## Fallback, and what it tells you

A tier that is not configured falls back down the chain `strong → mid → cheap`, and the provider
records which tier actually answered (`TierMapProvider.routed`). A run that quietly routes everything
to `cheap` still completes — that is what the fallback is for — but `routed` is the honest audit: it
shows whether the split you configured is the split that ran.

A tier with **no** endpoint anywhere is an error naming the missing variable, not a default.

## What this does not do

- It does not do per-provider rate limiting or cross-process queueing. If several runs share two boxes,
  the fairness belongs in the gateway (litellm or equivalent), not in the skill.
- It does not route *within* a tier. One tier, one endpoint — anything cleverer is a load balancer's
  job, and a skill that guesses is a skill that hides a 429.
- `search()` is not implemented here: upstream's web search is Anthropic-specific. Tier routing covers
  completions, fan-out and scoring; bring your own fetcher for the search phase.
