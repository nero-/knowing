# Model tiers → endpoint pools

Upstream's runner never names a model. It asks for a **tier** (`strong` / `mid` / `cheap`) and the
provider answers with an endpoint. `overlay/tier_routing.py` is that layer.

A tier is a **pool, not a machine**. One cluster going down rotates to the next candidate instead of
turning the run red, and the rotation is recorded so a degraded run is auditable.

## Config: declare an endpoint once, reference it as `provider/model`

`~/.config/knowing/tiers.toml` (or `$KNOWING_CONFIG`, or JSON if you prefer):

```toml
# --- endpoints, declared once -------------------------------------------------
[providers.sparks]                    # local vLLM box
base_url = "http://100.120.4.113:8015/v1"
models = ["DeepSeek-V4.1-Flash"]

[providers.tp2]
base_url = "http://100.97.112.71:8000/v1"

[providers.ollama]                    # local llama.cpp / LM Studio / Ollama: any /v1
base_url = "http://localhost:11434/v1"

[providers.openrouter]                # cloud, OpenAI-compatible
base_url = "https://openrouter.ai/api/v1"
api_key_env = "OPENROUTER_API_KEY"

[providers.anthropic]                 # cloud, different dialect
kind = "anthropic"
base_url = "https://api.anthropic.com"
api_key_cmd = "pass show anthropic/key"

# --- tiers reference endpoints ------------------------------------------------
[tiers.strong]
endpoints = ["sparks/DeepSeek-V4.1-Flash", "anthropic/claude-opus-5"]
rotate = "sticky"
fallback = ["mid"]

[tiers.mid]
endpoints = ["tp2/Qwen3.8-Flash-Next"]

[tiers.cheap]
endpoints = ["tp2/Qwen3.8-Flash-Next", "ollama/qwen3:8b", "openrouter/deepseek/deepseek-v4"]
```

Then `--provider tiers`. Local servers (vLLM, Ollama, llama.cpp, LM Studio) need no key — any value is
accepted by them, so the default `"vllm"` is fine. Cloud endpoints take one of:

| credential | when |
|---|---|
| `api_key = "..."` | throwaway/testing; not recommended for a repo |
| `api_key_env = "VAR"` | standard; resolved when the endpoint is first used |
| `api_key_cmd = "..."` | a secret manager or a file you already keep (`pass`, `op read`, `grep …`) — the same `!command` convention pi's own `models.json` uses |

Credentials resolve **lazily**, on first use, so rotating a key is not a config edit. A missing
variable is an error naming the variable, never a silent fallback.

### Mixing dialects

`kind = "openai"` (default) covers vLLM, Ollama, llama.cpp, LM Studio, TGI, OpenRouter, Together,
Groq, Fireworks, DeepInfra, and OpenAI itself. `kind = "anthropic"` uses the Anthropic SDK. That is the
whole list on purpose: anything else (Bedrock, Vertex) is a gateway away, and the gateway is
OpenAI-compatible.

### Check it before you run

```bash
python3 overlay/config.py check             # tiers, endpoints, and whether each key resolves
python3 overlay/config.py check --probe     # + GET <base_url>/models, flag a model the server
                                            #   does not actually serve
python3 overlay/config.py from-pi ~/.pi/agent/models.json > ~/.config/knowing/tiers.toml
```

`from-pi` turns your existing pi provider list into a starting config (including `!command` keys),
which is the fastest path from "these are my endpoints" to "the skill uses them". Edit the
`[tiers.*]` plan it emits — it puts everything in all three tiers as a placeholder.

## Two rotation policies, on purpose

| `rotate` | behaviour | use for |
|---|---|---|
| `"rr"` (default) | next candidate on every call | the fan-out, screening, extraction — independent calls, no prefix cache survives anyway |
| `"sticky"` | one candidate for the life of the process | planning, synthesis, adjudication — switching models mid-run loses the prompt cache and can change quality between two steps that must agree |

**Round-robin is not a quality balancer.** It spreads load across candidates you declared
interchangeable. If two endpoints serve *different* models and one is weaker, putting them in the same
tier means half your synthesis runs get the weaker model and nothing says so. If they are not
interchangeable, they belong in different tiers — that is what the tiers are for.

## Health is passive, and classified

A candidate is marked unhealthy only by a request that failed in a way that means *try elsewhere*:

- connection error, timeout, `OSError`
- HTTP 408, 409, 425, 429, 500, 502, 503, 504
- exception class names containing `RateLimit`, `Timeout`, `APIConnection`, `Overloaded`,
  `ServiceUnavailable`, `InternalServer`

Anything else — a 400, an auth error, a malformed request — **is not retried on another endpoint**,
because trying elsewhere would only hide the bug behind a second failure. It propagates.

Cooldown starts at 30 s and doubles per consecutive failure up to 300 s; a success clears it. No
probe calls, so a dead cluster costs nothing until something asks for it. If every candidate is
cooling down they are all tried anyway, in order — a stale cooldown must never be able to fail a run.

## Fallback between tiers, and the audit trail

`fallback` names the tiers to try when a tier's whole pool refuses (default `strong → mid → cheap`,
empty for `cheap`). Every attempt appends to `TierMapProvider.routed`:

```python
[{"tier": "strong", "index": 0, "model": "DeepSeek-V4.1-Flash",
  "base_url": "http://100.120.4.113:8015/v1", "reason": "failover", "error": "ConnectionError"},
 {"tier": "strong", "index": 1, "model": "DeepSeek-V4.1-Flash",
  "base_url": "http://backup-box:8015/v1", "reason": "ok"},
 {"tier": "cheap",  "index": 0, "model": "Qwen3.8-Flash-Next",
  "base_url": "http://100.97.112.71:8000/v1", "reason": "fallback-from-strong"}]
```

The third entry is the one that matters: the run *degraded a tier*, and said so. `finish.py` output is
where to look when a report feels thin.

## What this deliberately does not do

- **No active health checks.** A probe loop is spend and noise; passive failure detection answers the
  only question that matters — did a call fail in a way another endpoint would survive.
- **No weighted or latency-based balancing.** Those need measurements you do not have on the first
  call, and a skill that guesses at load hides a 429.
- **No cross-run queueing.** If several runs share two boxes, fairness belongs in the gateway
  (litellm or equivalent). A per-process pool can only be fair to itself.
- **No `search()`.** Upstream's web search is Anthropic-specific; tier routing covers completions,
  fan-out and scoring.

## Choosing the mapping

1. **Context window decides `strong`.** Planning and synthesis hold the fan-in; a synthesis step that
   gets compacted mid-way is worse than a slow one.
2. **Headroom decides `cheap`.** That is where parallelism lands (`MIN_CANDIDATES` of 60–100 at
   medium, 3–6 fetchers). Check what the server advertises on `/v1/models`.
3. **Interchangeability decides pool membership.** Same model, same quantisation, same context window
   → same pool. Anything else gets its own tier and an explicit `fallback` entry, so the downgrade is
   visible instead of statistical.
