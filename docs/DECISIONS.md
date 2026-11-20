# Decision record

Every decision here was made against code, not against a README. Where a documented guarantee
turned out to be prose, that is recorded rather than quietly fixed — the point of the record is that
the next person does not re-derive it.

## D1 — Base: deepdive, not a composition

Candidates inspected in code: deepdive, hyperresearch, academic-writing-toolkit, PaperTeam,
Interceptor, sm-lifecycle, plus seven frameworks (gpt-researcher, open_deep_research, Tonga
DeepResearch, PaperQA2, STORM, MiroThinker, Skywork). deepdive won on the things it *enforces*:

- `MIN_READ = {medium: 25, deep: 35}` and `MIN_CANDIDATES = {medium: 60, deep: 100}`, both in
  `NON_WAIVABLE` — a run cannot talk its way out of breadth.
- `TYPE_QUOTAS` (academic ≥2, primary ≥3, media ≥2, expert ≥2, forum ≥2) and `MIN_CONTRADICTING = 3`.
- a confidence ceiling computed by `score_claims.py --write`, where the model may only lower a label.
- roots/`discovery_path` independence counting.

**Correction to the first draft of this record:** the entailment gate was cited as an inherited
asset. It is not implemented — `validate_phases.py:327-354` grades only the shape of
`.verify/faithfulness.json`, `finish.py` never reads a verdict, and `runner/orchestrator.py:385` says
`faithfulness not implemented`. Entailment is work in this fork, not a feature of the base.

## D2 — Ledger stays CSV; locators are a column, never embedded text

`claims.csv` is read by seven real parsers, all `DictReader` + name access (the "14 consumers" in an
earlier draft counted mentions, not parsers). Column order is enforced by `header_violation`, and
`score_claims.py --write` re-renders in canonical order.

- **Anchor columns:** `anchor` = `<source id>:<line>`, `quote_sha256` = first 16 hex of
  `sha256(normalize(card_line))`, using the same normaliser the base uses for quote comparison
  (`eval/check_quotes.py::normalize`). `overlay/tests/test_gate.py::test_normalize_parity_with_upstream`
  fails if the two drift.
- **No quote text in a cell.** Six parsers use `read_text().splitlines()`, so a multi-line cell
  silently becomes a doubled line — verified, not assumed.
- **Header is an allowlist** (`CLAIMS_OPTIONAL`), so a new column is rejected outright until declared:
  `ERROR: claims.csv off-contract: unknown column(s) anchor, quote_sha256 … rc=1`. Patch 1 extends the
  allowlist; with that, the `--write` round trip is lossless.
- **Rejected alternatives:** JSONL (no verification gain, and the repo already ships JSONL elsewhere —
  the "column order" argument was wrong), SQLite (binary, no reviewable diffs, needs a query layer).

**What a hash proves:** the quoted text at that locator is byte-identical after normalisation. It
therefore catches card edits, anchor drift, transcription typos and post-hoc paraphrase.
**What it does not prove:** that the quote supports the claim. It is self-attested by the same agent
in the same turn, so it is an integrity check, not an honesty check. Support remains the job of the
adversarial pass — and, where it can be made to work, the LLM faithfulness layer.

## D3 — `depth:` is canonical, and a missing declaration fails closed

The base's plan template writes `depth: shallow | medium | deep` (`references/plan_template.md:18`)
while the validator reads `mode:` (`MODE_RE`, read from the dated report *before* plan.md). A plan
declaring `depth: deep` validated as **shallow**, and `check_source_breadth` early-returns on shallow
— skipping `MIN_READ`, `MIN_CANDIDATES`, all five `TYPE_QUOTAS` and `MIN_CONTRADICTING`.

Patches 2 and 3: `MODE_RE` accepts `depth:` (canonical) and `mode:` (legacy alias, warned about), and
a missing declaration becomes an **error** instead of an inference to shallow.

The three-class "reason" enum proposed in planning was rejected in review because it collapses
("migrate now or later" fits both `answer-exists` and `reversible-cheap`). Replaced by **three
orthogonal facts** in `plan.md` — `reversibility`, `cost_of_error`, `answer_exists` — from which the
minimum depth is derived and compared against the declaration. A shallow claim in a run that declares
`irreversible` or `high` cost is an error.

## D4 — Read scope is a per-source field, and an abstract cannot triangulate

`read_scope: full_text | sections | abstract_only` on `sources.csv` (patch 4). A claim marked
`triangulated` whose sources are all `abstract_only` is an error. The base's `access:` axis (paywall
states, including `paywalled-abstract-only`) stays as a separate field — it answers a different
question, and conflating them loses information.

Not implemented in v0.1: "you may not criticise a method you did not read at `full_text`". It needs a
reliable way to recognise method criticism in prose; faking it would be worse than not having it.

## D5 — Adjudication: verdict and declined list, on top of the existing severity register

The base's red team produces findings with HIGH/MED/LOW severity and blocks the final on HIGH, but no
run-level verdict and no record of what the reviewer could not judge. Added `VERDICT: PASS | REVISE |
BLOCK` and a required `## DECLINED TO JUDGE` section; BLOCK fails the run. Deliberately narrow: the
remediation body check already exists upstream (`check_remediation_in_body`).

## D6 — Executors: mapping recorded, prose not yet rewritten

`references/model_routing.md` routes to Claude Code agent types (`deepdive-fetcher`,
`deepdive-redteam`, `deepdive-synthesizer`) and to Opus/Sonnet/Haiku by hard-coded name. The repo does
not ship those agent definitions. On pi they map to Agent types, and the tier abstraction that does
the real work lives in `runner/providers.py` (`TIERS = strong/mid/cheap`, `OpenAICompatProvider(base_url=…,
model_override=…)`), which is provider-agnostic and already supports vLLM-style endpoints. Mapping:
`strong` → a large-window model for planning and synthesis, `mid`/`cheap` → the fan-out. The prose is
flagged in place with a translator note rather than rewritten speculatively.

## D7 — Gates live inside the finish chain, not beside it

Four reviews of the migration plan converged on this: a sidecar script re-creates the seam the design
exists to close. Both upstream and hyperresearch have the incident on record — hyperresearch's own
source comment: "Bench Q62 shipped with 24 hallucinated-quote errors because the orchestrator ran the
lint separately and re-interpreted the failures as false positives."

So: seven idempotent patches (`overlay/apply_patches.py`), each asserting its anchor string, and
`knowing_gate.py` appended to `finish.py::STEPS` after `validate_phases`. A failed patch is a loud
error, not a silent skip.

## D8 — Translation is a coupled change

The validator matches Russian string literals: `гипотез … вердикт`, `по умолчанию|берите|выбирайте`,
`## Разбор`, and the readout frame `Ответ`/`Делать`/`Не делать`/`уверенность`. Translating prose
without those patterns turns gates into no-ops that report nothing — indistinguishable from success.
Hence `docs/TRANSLATION.md`'s glossary is a contract, and every translated gate needs a test that
proves it still fires. v0.1 translates the floor; the backlog is ordered by the load profile.

## D9 — Model tiers are hardware, not model names

Upstream's `runner/providers.py` already asks for `strong/mid/cheap` and never names a model — that
abstraction was the reason this base was worth patching rather than replacing. What it lacked was a
mapping to *more than one endpoint*: `OpenAICompatProvider` pins one `base_url` per process.

`overlay/tier_routing.py` adds `TierMapProvider`: one client per endpoint, a config layer
(`KNOWING_TIERS` JSON / `KNOWING_TIERS_FILE` / per-tier env vars), and a `strong → mid → cheap`
fallback that *records* which tier actually answered (`routed`). A run whose config silently degraded
still finishes, but the degradation is auditable.

**Revised after review.** The first cut bound each tier to a single endpoint, which makes a dead
cluster an outage and a second box unusable. It is now a **pool**: candidates are tried in rotation,
a transient failure (connection error, timeout, 408/409/425/429/5xx) cools that endpoint down for
30 s doubling to 300 s, and the call moves on. A non-transient failure (400, auth) is *not* retried
elsewhere — trying a second endpoint would only hide a bug behind a second failure.

Rotation is per tier because the right behaviour differs: `rr` for the fan-out, where calls are
independent and no prefix cache survives; `sticky` for planning and synthesis, where switching models
mid-run loses the cache and can change quality between two steps that must agree. Round-robin spreads
*load*; it does not balance *quality*. Two endpoints in one tier are a claim that they are
interchangeable, and a weaker model in the pool means half the runs get it silently — so a different
model gets a different tier and an explicit `fallback` entry, where the downgrade is recorded.

Endpoints are declared once as named providers and referenced `provider/model`, with credentials from
a literal, an env var, or a command (`api_key_cmd` — the same `!command` convention pi uses), resolved
lazily. Dialects: `openai` (vLLM, Ollama, llama.cpp, LM Studio, TGI, OpenRouter, Together, Groq,
OpenAI) and `anthropic`. Anything else is a gateway away, and gateways speak OpenAI.

Deliberately out of scope: active health probes (spend and noise; passive failure detection answers
the only question that matters), weighted or latency-based balancing (needs measurements you do not
have on call one), rate limiting and cross-run queueing (a gateway's job), and `search()` (upstream's
is Anthropic-specific). A skill that guesses about load is a skill that hides a 429.
