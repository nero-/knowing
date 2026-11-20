<!-- translated from upstream/references/plan_template.md @ e233797 — see docs/TRANSLATION.md -->
# plan.md template

## Contents

Template sections (inside the code block): §0 User context · §1 Time-box · §2 Main question · §3 Decision Spec · §4 Acceptance criteria · §5 Discovered existing · §6 Glossary · §7 Genre · §8 Blocks with rationale · §9 Hypotheses · §10 Risk register · §11 Subtopic ↔ Blocks (+ least-to-most) · §12 Information sourcing strategy · §13 Opposition queries · §14 Stop-criteria · §15 Notes · §16 Update changelog

A supplement to `phases/p3_plan.md`. Read it **on entering Phase 3**, not earlier — until
that moment the run needs only the structure (5 sections HEADER → SCOPE → STRUCTURE →
EXECUTION → TRACKING), not the template's literal text.

**plan.md template:**

```markdown
---
slug: <slug>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
depth: shallow | medium | deep
# knowing: the three facts that derive the depth. The gate fails the run if any of them
# is missing, is out of range, or implies a deeper run than the one declared above.
reversibility: reversible | irreversible
cost_of_error: low | high
answer_exists: yes | no
report_type: qa | explainer | decision | landscape | validation | custom
blocks: [tldr, scope, mental-model, stepwise, counter-arguments, sources, metadata]
status: planning | searching | synthesizing | completed | superseded
version: initial | update-1 | update-2
parent: <YYYY-MM-DD>_<genre>.md   # null if initial
time_box_target: ~<X hours>
time_box_hard: <Y hours>
---

# Plan — <topic>

## 0. User context

- **Who is asking / for whom:** <user role, audience for report, ...>
- **Why (business/personal motive):** <real underlying motivation>
- **What they already know:** <baseline knowledge level — beginner / informed / expert>
- **How the report will be used:** <make a decision by <date> / include in a pitch / share with the team / personal understanding>
- **Constraints on the report:** <language, format, length, confidentiality>

## 1. Time-box

- **Target completion:** ~<N hours> (matches depth `<level>`)
- **Hard deadline:** <YYYY-MM-DD HH:MM or N hours from the start>
- **If the hard deadline is exceeded:** synthesize with what there is, mark confidence: low on unresolved theses

---

# SCOPE

## 2. Main question
<after reframing — rewritten in your own words>

## 3. The decision it supports (Decision Spec)
- **What we decide:** <verb + object + deadline>
- **Consumer → next step:** <who reads the report and what they physically do afterwards>
- **If-then forks:** if <X> → <A>; if <Y> → <B>  (≥1, falsifiable)
- **If there is not a single fork:** this is not research, this is curiosity — downgrade to shallow with an explicit mark, or refuse

## 4. Acceptance criteria (what counts as «done»)

Concretely, what the output must contain for the research to count as finished:

- [ ] `<date>_<genre>.md` contains all the genre's required blocks
- [ ] Every hypothesis H1-H4 got a status (confirmed / contradicted / partial / insufficient)
- [ ] `<specific deliverable 1>` (e.g. a list of 5+ competitors with profile cards)
- [ ] `<specific deliverable 2>` (e.g. answers to the user's 4 specific Qs)
- [ ] `<specific deliverable 3>`
- [ ] Counter-arguments ≥2 for medium / ≥3 for deep
- [ ] Multi-angle red team passed (for medium/deep)
- [ ] All sources/NN.md have channel + access fields

## 5. Discovered existing

What already exists on the topic in the project — found in the discover phase.

**Existing research folders:**
- `<existing slug>` from <date> — <relation: same topic? adjacent? update target?>
- (or: «nothing there, initial research»)

**Memory entries:**
- `<memory file>` mentions <fact> — <accept / reconsider / not relevant>
- (or: «memory is empty or not relevant»)

**AGENTS.md project context:**
- <relevant project info from AGENTS.md / project notes>
- (or: «AGENTS.md does not mention the topic»)

**Decision:** initial research | update of `<slug>` | re-investigation (with reason)

## 6. Research glossary (terms and definitions)

Terms that will be used during the research and in the report. Agreed between the skill and the user BEFORE the search starts.

- **<Term 1>** — <definition, as we use it here>
- **<Term 2>** — <definition>
- **<Term 3>** — do NOT confuse with <similar term>, the important difference <X>

If during the search it turns out that a term needs refining — update it here and record it in `notes` (section 17).

---

# STRUCTURE

## 7. Report genre
**<genre>** — why this one: <justification by the heuristic / user input>

## 8. Report blocks with rationale

For a standard genre — the preset from `genres.md`. For custom — you must justify EVERY block.

| Order | Block [ID] | Why it is here |
|---|---|---|
| 1 | tldr [F1] | (always) |
| 2 | scope [F3] | (always) |
| 3 | mental-model [E1] | <under H1, explains how X works> |
| 4 | data-table [A1] | <we collect <metric>×<entity> to answer Q2> |
| 5 | counter-arguments [Z1] | (always medium/deep) |
| 6 | ... | ... |

## 9. Hypotheses

- **H1:** <falsifiable statement>
- **H2:** ...
- **H3:** ...
- **H4:** ... (optional)

## 10. Risk register (pre-mortem before the start)

Where it can go wrong before we have started:

| ID | Risk | Probability | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Topic poorly documented (few sources total≥12) | medium | high | plan an interviews fallback in advance, lower the confidence ceiling |
| R2 | Closed info (private financials) — most claims are not verifiable | high | medium | admit it honestly, use indirect signals |
| R3 | Politically charged — bias in the sources | medium | high | deliberately triangulate across multiple political perspectives |

---

# EXECUTION

## 11. Subtopic ↔ Blocks mapping

Which subtopic gathers evidence for which blocks. Without this the agents do not know what they are working for.

| Subtopic | Feeds which blocks | Level (depends on) | Assigned to (agent # + source range / main thread) |
|---|---|---|---|
| ST1: <name> | F3, E1, E4 | L1 (—) | Agent #1 (`general-purpose`, s01-s09) |
| ST2: <name> | A1 (data-table rows), M2 (profile cards) | L1 (—) | Agent #2 (`general-purpose`, s10-s19) |
| ST3: <name> | V2 (evidence FOR/AGAINST), Z1 (counter-args) | L2 (ST1) | Agent #3 (`general-purpose`, s20-s29) |
| ST4: <name> | E10 (failure modes), Z2 (open questions) | L2 (ST1, ST2) | main thread |

### Least-to-most: when subquestions form a chain

Most subquestions are **independent** — all `L1`, all searched in parallel in Round 1.
Do not impose a chain where there is none: if the answer to ST-B does not change from
what you learned in ST-A, both are L1. A flat decomposition is the norm, not a defect.

But **multi-step** questions (of the form «how will X affect Y, **given** Z», «what follows
from A for B») contain subquestions that cannot be meaningfully searched until the
preceding one is answered — the early answer is an **input** into the wording/queries of
the late one. For them a flat parallel fan-out searches blindly: the late agent does not
know the specifics the early one would have supplied. Least-to-most solves this with a
giant gain on multi-step questions (SCAN 99% vs 16%): you lay the subquestions out by
**levels** and accumulate context between them.

**Mechanics (only for questions with a real dependency):**
1. Set `Level` in the table above. `L1` — independent (start immediately). `L2` depends on
   one/several L1s; `L3` — on L2. Keep the depth small (usually ≤2 levels) — a deep
   chain = either the question is genuinely cascading, or you have over-split it.
2. **Round 1 = all L1** in parallel (the usual fan-out by ranges). The level does not break
   parallelism — inside a level everything is just as parallel.
3. After L1, fix the **carried context** — 2-4 concrete facts/numbers/entities from the
   L1 answers that the next level needs (not the whole dump — exactly what feeds the
   dependent subquestion). Write them into the dispatch (section 12) of the dependent STs.
4. **Launch L2** with the queries now made concrete. Repeat for L3 if there is one.
5. Cycles (accumulation) run **before** the round's deviation loop, not instead of it:
   first the planned chain of levels runs through, then — orchestrator-evaluation/deviations
   on the aggregated result.

If after L1 it turns out the dependency was imaginary (the carried context was not needed) —
collapse the chain, run the remainder in parallel, record it in `deviations.md`
(`type: decomposition_flatten`). Flat is more honest than staging a cascade.

## 12. Information sourcing strategy

**Filled at the Phase 4.0 Source Dispatch step** via `source_dispatch.md` — every subquestion/subtopic is run through the matrix «signal → primary/secondary/fallback channels». **Transparency: the user sees where we look and why.**

### ST1: <name>

**Feeds blocks:** F3, E1, E4 (see the mapping above)

**Dispatch (primary / secondary / fallback):**

- **Primary** — `<channel-name>` (from the `source_dispatch.md` matrix, the row matching the «...» signal)
  - Specific queries: `<query template 1>`, `<query template 2>`
  - What we are looking for: <specific evidence type>
  - Concrete sources: `stat_sources/<path>.md` or `api_sources/<category>/<api>.md`

- **Secondary** — `<channel-name>` (an independent check of primary)
  - Specific queries: `<...>`
  - Concrete sources: `<path>`

- **Fallback** — `<channel-name>` (only if primary/secondary are unavailable)
  - Queries: `<...>`

**API endpoints (if api-direct is primary or secondary):**
1. **`api_sources/<category>/<api>.md`** → the specific API
   - Endpoint: `<url>`
   - Auth: `<env var name>` / no-auth
   - Query template: `<sample query>`

**Capabilities check (Phase 3.5):**
- ✅/⚠/❌/❓ FRED API: authenticated / fallback / unavailable / to-discover
- ✅ Semantic Scholar: open-no-auth, will use directly
- ⚠ Brave Search: no key → fallback to standard WebSearch

**Discovery executed (Phase 4.0):**
- Awesome-lists registry: <which Tier we checked + what we found>
- GitHub topic search: <topic:keyword found N repos/awesome-lists>
- HuggingFace / Kaggle / PyPI / data portals: <if applicable>
- If nothing was needed — write «N/A — the catalogue was enough»

**Critical gaps to address:**
- Opposition voice → `forum-discussion` channel + `<source>` industry
- Recent data → `news-current` for the last <N months>

### ST2: <name>
(the same template — primary / secondary / fallback from `source_dispatch.md`)

### ST3, ST4, ...

**Acceptance for section 12:** Filled for **every** subquestion from section 11. If even one subquestion has no dispatch — do not launch Phase 4.1 (launch sub-agents), go back to step 4.0.

## 13. Critical opposition queries

Targeted queries specifically for finding the contrarian voice:
- `<topic> criticism`
- `<topic> "doesn't work" OR "failed"`
- `<topic> "myth" OR "misconception"`
- `against <topic> / counter-evidence`

One dedicated round of these queries is mandatory. If nothing is found — try a different wording or admit «consensus very strong, no opposition found».

## 14. Stop-criteria (of the search)

- All H1-H4 covered by ≥3 sources each
- ≥4 source types covered
- ≥3 channels covered (see channels.md) — diversity of methodology
- The targeted opposition search is done
- NO new information in the last 3-5 sources
- All acceptance criteria (section 4) can be met with the gathered material

**Do not confuse with the acceptance criteria (section 4) — those are about the report, these are about the search.**

---

# TRACKING

## 15. Notes during research

A place for notes during the search. Updated as the work goes, not at the end.

- **<YYYY-MM-DD HH:MM>** — found that <observation>, relevant for ST2
- **<date>** — found the opposition in [s09], H2 confidence lowered to medium
- **<date>** — gap: data up to 2022 only, nothing recent; see risk R1
- ...

## 16. Update changelog (update mode only)

Fill in only if `version: update-N`.

**Update context:** <why an update was needed>

**Delta vs the previous version:**
- What was added: <new subtopics, new blocks, new hypotheses>
- What went stale: <which H/blocks are no longer relevant>
- What we re-check: <findings to validate in the light of new evidence>

**What we do not repeat:**
- <areas already deeply covered in the parent, which we build on>

---

## Slug
<slug>
```
