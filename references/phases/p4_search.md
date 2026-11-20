<!-- translated from upstream/references/phases/p4_search.md @ e233797 — see docs/TRANSLATION.md -->
## Phase 4. Search

**Model:** main thread `sonnet` / `medium`. Sub-agents — **different models** by subtask type (see `model_routing.md`, section «Routing for sub-agents»): web/news/api-direct → `haiku`, academic/long-source → `sonnet`, heavy reasoning subtask → `opus`.

**Phase 4 is an orchestrator-driven loop, not a single salvo.** Round 1 executes the
approved plan (Phase 4.0 dispatch). After *every* round the orchestrator evaluates the
aggregated results and may spend a bounded *deviation* to launch another round. The
plan stays authoritative as the starting point; deviations are bounded and recorded.

**Phase 4 = 4 steps in a strict order (Round 1):** Dispatch → Candidates and selection → Fetch → Save. Do not skip Dispatch — without it Launch will be chaotic.

### 4.0 Source Dispatch (NEW mandatory step)

**Before launching sub-agents**, run every subquestion from plan.md section 11 (Subtopic ↔ Blocks mapping) through `source_dispatch.md`:

1. Open `source_dispatch.md` → find the row in the Matrix matching the subquestion's signal
2. Write the **primary / secondary / fallback channels** into `plan.md` section 12 in the format given at the end of `source_dispatch.md`
3. If the topic is narrow or does not match — run the Discovery patterns (GitHub topics, awesome-lists registry, HuggingFace, PyPI/npm, data portals) and **record what you found** in the «Discovery executed» section
4. If the decomposition recipe in `source_dispatch.md` adds subquestions that plan.md does not have — **go back to Phase 3** and extend the decomposition, then continue

**Output 4.0:** a filled section 12 of plan.md with the per-subquestion sourcing strategy. Without it 4.1 does not start.

### 4.1 Candidates → selection → reading (medium/deep)

We select wide and cheap, read narrow and deep. Benchmark 2026-10-28: 6 of 6 runs read 16–19 sources from their first queries, Academic 0, 3–4 types.

1. **Query matrix** before searching: rows — spheres (academic, primary, media, expert, practice), columns — stance toward the leading hypothesis (for / against / neutral). Queries in EN and in the user's market language. One cell — 1–2 queries.
2. **Candidate pool** — `explore-haiku`, WebSearch and API only, no WebFetch: 60–100 rows (deep ≥100) in `candidates.csv`, columns `url,title,snippet,channel,sphere,stance,vendor,round,target,selected`. At least 1 academic API call is mandatory (`api_sources/academic/`: openalex, semantic_scholar, arxiv, crossref; `channel` = the API name). Snowball goes here too: links and "cited by" of the 2–3 best candidates via OpenAlex/Semantic Scholar.
3. **Selection for reading** — the main thread, by the table, not by the texts: medium 25–30, deep 35–45, `selected=Y`. Read quotas (gate `validate_phases.py`):

   | Sphere | source `type` | Minimum |
   |---|---|---|
   | science | Academic | 2 |
   | primary (docs, standards, regulators) | Primary | 3 |
   | media | Industry-media / General-media | 2 |
   | expert articles and blogs | Expert-blog | 2 |
   | practitioners (incidents, forums, issues) | Forum | 2 |
   | against the hypothesis | `hypothesis_evidence: contradicts` | 3 |
   | vendor (`caveat: vendor`, including competitor marketing) | — | no more than half |

   Retellings of a single `root:` count as one source for quotas. If a quota cannot be met honestly (the topic has no science) — a `quota_waiver: <key> — <why>` in `plan.md`, written **after** selection: the reason refers to something that is not in `candidates.csv`. Budget is not a reason. `count`, `candidates`, `round2` are never waived at all; the validator prints the remaining keys. The gate then warns instead of blocking, and the caveat goes into «What we don't know».

4. **Reading** — `deepdive-fetcher` (haiku) receives the list of selected URLs and an id range, not the topic: it searches only to replace a dead URL. Then `sonnet`/low, in batches of 5–8 files, appends into each `## Source dissection` (`source_scoring.md`, file template); without the card the validator warns.
5. **A second round is mandatory**: after the first reading, name the variable the decision depends on (from the Decision Spec forks: price at our volume, latency, headcount), and gather ≥5 more candidates with `round=2`, `target=<variable>`. If a measurement surfaced, read it outside the quotas.

Shallow: the main thread does WebSearch+WebFetch itself and writes `sources/NN.md`, without `candidates.csv` and quotas.

### 4.2 Fetch & Dedup

- Use the built-in WebFetch and WebSearch.
- For APIs from `api_sources/` — Bash + curl + jq if the response is large, otherwise WebFetch.
- If WebFetch returned «unable to fetch from …» — this is most often a robots.txt exclusion for AI agents, not a dead page. Before writing a source off into `gaps`, run it through the fetch ladder — `references/fetch_ladder.md` (two-tier `fetch_source.py`, exit codes, feed fallback, PDF handling).
- If a source is behind a paywall — the paywall fallback protocol in `channels.md` (preprint → archive → researchgate → …; pirate mirrors are not used).
- Cover ≥3 channels of different types for diversity of methodology (a Phase 5 triangulation requirement).
- Dedup by URL and by content (if two links lead to the same report — keep the one with the better scoring).

#### Fetch ladder — when WebFetch is not enough

Two-tier `fetch_source.py` (http → browser), exit codes, feed fallback instead of dead
HTML, PDF handling, `main_content_only` as a prompt-injection sanitizer — the whole of it
in `references/fetch_ladder.md`. Read it when WebFetch actually failed to return content, not in advance.

### 4.3 Save sources

- Every source found → its own file in `sources/SNN_<slug>.md` with a filled frontmatter: `channel:`, `access:`, `subquestion_ids: [Q1, Q3]`, `credibility/recency/bias`.
- No «we'll collect it at the end» — write immediately after dedup.
- If a source covers several subquestions — list all of them in the frontmatter via `subquestion_ids:`, do not duplicate the file.

**Output Phase 4 (Round 1):** a filled `sources/` folder + an updated `sources.csv` + «open gaps» flags in plan.md for subquestions where ≥3 sources of different types could not be gathered.

### Round structure

1. **Round 1 = the plan.** Run Phase 4.0 (Source Dispatch) → Phase 4.1 (candidate pool,
   selection by quotas, fetchers on the selected URLs) → 4.2 (dedup) → 4.3 (save sources). This always runs.
2. **Each sub-agent emits a `signals` block** in its JSON (in addition to sources):

   ```json
   {
     "subquestion_id": "Q3",
     "round": 1,
     "sources": [ ... ],
     "signals": {
       "empty_result":       { "fired": true,  "detail": "0 relevant hits on `academic`" },
       "unexpected_finding": { "fired": false, "detail": null },
       "contradiction":      { "fired": false, "detail": null },
       "citation_lead":      { "fired": true,  "detail": "S07 cites Gartner 2024, no link" }
     }
   }
   ```

   Sub-agents signal **generously** (high recall). They report observations; they do
   NOT decide to deviate.

3. **Cheap goal-check (after every round, `haiku` / low — before the Opus pass):** a
   non-thinking evaluator scores each subquestion against its *goal*, not its sources.
   For every `subquestion_id` it emits a one-line `goal_status`:

   ```json
   { "subquestion_id": "Q3", "goal_status": "partial",
     "missing": "have the 2024 figure, no primary source and no pre-2020 baseline to compare" }
   ```

   `goal_status ∈ {met, partial, unmet}`; `missing` is a concrete gap phrase when not
   `met`. This is deer-flow's non-thinking evaluator: a Haiku pass that *names the gap*
   so the expensive Opus evaluation below works from a diagnosis instead of deriving one
   from scratch, and so the next round's dispatch targets the named gap rather than
   re-searching the whole subquestion. It decides nothing — it only labels. The Opus
   pass and the circuit breaker read these labels; a round where every subquestion is
   `met` and no trigger is justified ends the loop.

4. **Orchestrator evaluation (after every round, `strong` tier / Opus):**
   - Aggregate all sub-agent JSON for the round.
   - **Cross-agent contradiction scan** (cheap tier): scan the whole pool for sources
     that conflict — this catches contradictions no single sub-agent can see (each
     sees only its own subquestion).
   - Opus reviews flags + scan + aggregated output and selects which triggers are
     *justified* (strict precision — a sub-agent's `unexpected_finding` is a candidate,
     not an automatic spend).
   - **Trajectory sanity-check (cheap tier):** before pursuing an `unexpected_finding`
     or `citation_lead`, verify the *intermediate claim* that triggered it is itself
     backed by a real source. A round seeded by an unsupported intermediate claim
     compounds hallucination downstream (trajectory error) — drop the trigger and flag
     the originating source instead of spawning a search on a phantom.
   - **Query mutation (cheap tier):** aggregate the sub-agents' `query_performance`
     rows (see `subagents_v2.md`). For subquestions whose queries came back
     noise/empty, the next round's dispatch mutates the wording deliberately —
     RU↔EN language switch (Russian-relevant topics are invisible to English-only
     queries and vice versa), operators (`site:`, `filetype:pdf` for reports, quoted
     exact phrases, date ranges), practitioner vs academic terminology — instead of
     re-running the wording that already failed.
   - **Novelty rate (saturation signal):** share of the round's take that is
     genuinely new to the pool — new URL AND new `root:` AND new claim. Record the
     number in `deviations.md`. Novelty below ~20% is saturation: prefer ending the
     loop over spawning another round even if a justified trigger remains (record it
     as `not_pursued: saturation`). This is the graded companion to the binary
     no-progress circuit breaker below.
   - For each justified trigger, if budget for its class remains AND depth < limit:
     classify cheap/expensive, debit the counter, write a `deviations.md` record,
     and launch the next round. Otherwise write a `not_pursued` record.
5. **The loop ends** when no justified trigger remains, OR both budgets are exhausted,
   OR the depth limit is reached, OR the novelty rate signals saturation (step 4),
   OR the **no-progress circuit breaker** fires (see below). Then proceed to Phase 5.

### Round workspace — rebuild, not accumulation (`state.md`, medium/deep)

Sub-agents write to files, only index rows reach the main thread — but between rounds
the orchestrator keeps dragging the whole history along (agent JSON, goal-check, triggers,
contradiction scan) and by the third round decides «where next» in a window where past
rounds have pushed out the current instruction.

**Rule:** before each next round the main thread REWRITES (does not append to) `state.md` —
`## Known` (subquestion statuses with links to `claim_id`/`[sNN]`) · `## Gaps` ·
`## Next`, budget ≤6 KB — and plans the round from it, not from the transcript. The
archive does not vanish anywhere: `sources/`, `deviations.md`, `plan.md` §15. It does
not lift the ban on sharing findings: the next round's agent gets its own hole from
`Gaps`, not someone else's `Known`. Template and anti-patterns —
`subagents_v2.md` («Round workspace»).

### Triggers (4) and their classes

| Trigger | Class | Meaning |
|---|---|---|
| `empty_result` | cheap (self-correction) | a planned channel returned nothing relevant |
| `citation_lead` | cheap (self-correction) | a source cites an unreachable primary source |
| `unexpected_finding` | expensive (scope-expansion) | an important angle outside the plan surfaced |
| `contradiction` | expensive (scope-expansion) | sources conflict |

*Self-correction finishes already-planned work (doesn't change scope) → generous
budget. Scope-expansion departs from the approved plan → hard ceiling.*

### Budget & depth (by research depth)

| Depth | cheap | expensive | depth (nesting) limit |
|---|---|---|---|
| shallow | 2 | 0 | 1 |
| medium | 4 | 1 | 1 |
| deep | 8 | 3 | 2 |

- `shallow expensive = 0`: a shallow `unexpected_finding`/`contradiction` is recorded
  `not_pursued: budget_exhausted`, never run. Self-correction still works on shallow.
- **Depth** = how many deviation-spawned rounds deep the current round is (Round 1 =
  depth 0). A deviation from a depth-limit round cannot spawn another.
- Debit is atomic, orchestrator-only, before launching the next round.

### No-progress circuit breaker

Budget/depth bound *how much* the loop may spend; the circuit breaker bounds *spinning
in place*. A deviation round can fire a trigger, cost budget, and return nothing the
pool didn't already have — two of those in a row means the loop is stuck, not
progressing. Stop before it drains the rest of the budget on a phantom.

**Rule:** after each deviation round the orchestrator (cheap tier) computes that round's
**progress delta**. A round makes progress if it added ≥1 *new* source (a URL not
already in `sources.csv`) OR resolved a triggering signal (an `empty_result` that now
has hits, a `citation_lead` whose primary was reached, a `contradiction` now
adjudicated). A round that adds only duplicate/near-duplicate sources and resolves
nothing is a **no-progress round**. **Two consecutive no-progress rounds → break the
loop immediately**, regardless of remaining budget or depth.

On break: record it in `deviations.md` (`type: circuit_breaker`, which rounds stalled,
which triggers were left unpursued) and carry the unresolved triggers into **Open
Questions** in the report (they are genuine gaps, not silent skips). Do not keep
re-launching the same starved subquestion hoping for a different result — one honest
"could not resolve within budget" beats three identical empty rounds.

Round 1 never counts toward the breaker (it *is* the plan, always executed). The
counter resets on any progress round, so alternating progress/no-progress does not
trip it — only a genuine two-round stall does.

### `deviations.md`

Written beside `plan.md` / `sources/`. One record per *considered* trigger (both
`pursued` and `not_pursued` — **exhausted budget/depth still leaves a record; never a
silent skip**), plus a `type: circuit_breaker` record if the no-progress breaker fired.
Phase 6 audits it; Phase 7 reads `not_pursued`/`carry_forward`.

### Dynamic outline revision (ScaffoldAgent)

The plan's block/outline (Phase 2 genre + `plan.md` §8) is the *starting* structure,
not a cage. If a round's aggregated evidence shows the planned outline no longer fits —
a whole dimension surfaced that no block covers, or a planned subtopic came back empty
across rounds — the orchestrator may spend **one expensive-class** deviation to revise
the outline: add/drop/reorder blocks, update `plan.md` §8 + §11, and record it in
`deviations.md` (`type: outline_revision`, before/after, reason). Gate: medium ≤1,
deep ≤2, shallow never (fixed outline). Don't silently rewrite structure — every
revision is a recorded, budgeted decision, same as any deviation. This keeps the report
shape adaptive to what the evidence actually is, not what we guessed at Phase 2.
