<!-- translated from upstream/references/evidence_filter.md @ e233797 — see docs/TRANSLATION.md -->
# Evidence Filter — Phase 5.5

## Contents

- What this does NOT touch
- When it fires — depth_gate
- Mechanics — CRAG evaluator + relevant-only extraction
- Axis 2 — authority: is the source entitled to assert this
- Output — the `evidence/` layer
- Relation to `findings/` (deep)
- Anti-patterns
- Phase 5.5 checklist

A filter on the **input** of synthesis, along two axes. Between Phase 5 (claims ledger ready) and Phase 6 (synthesis), for every (claim, source) pair it is decided:

1. **relevance** — *does the fragment concern exactly this claim* (the whole pool of pairs);
2. **authority** — *is this source entitled to assert such a thing* (only load-bearing pairs, see below).

Relevant quotes are carried out into a separate `evidence/` layer, authority verdicts into `.verify/authority.json`; synthesis is fed neither the whole pool of sources at once, nor a source that is not entitled to carry a claim on its own.

**Why.** Feeding everything found into synthesis naively *lowers* quality instead of raising it: Search-o1 showed a drop of 33%→24% on LiveCodeBench when irrelevant retrieved context went into the reasoning chain without a filter. CRAG (retrieval evaluator + decompose-then-recompose) consistently beats naive RAG on 4 datasets (e.g. Biography FActScore 59.2→74.1). The mechanics: a lightweight relevance classifier discards noise BEFORE it blurs the synthesis.

**Symmetry with 6.5.** Phase 6.5 (Verify) checks the **output** of synthesis — whether the source really supports the written thesis (faithfulness). Phase 5.5 filters the **input** — which fragments are worth carrying into synthesis at all (relevance). Together they close both sides: not dragging the superfluous in, and not letting the unconfirmed out.

## What this does NOT touch

- **`sources/NN.md` are untouchable.** They are archival memory for reuse between researches (`source_scoring.md` explicitly forbids compressing/rewriting them). Phase 5.5 only reads them.
- **It does not duplicate scoring (Phase 5).** `total` (credibility/recency/bias) is the quality of the source *as a whole*. 5.5 is the relevance of *a fragment to a specific claim*. Different axes: an authoritative source may contain a quote unrelated to this claim; and vice versa.
- **It does not duplicate `hypothesis_evidence`.** That one classifies the relation to a hypothesis (supports/contradicts/partial/neutral). 5.5 gives a binary keep/drop under a claim and cuts the volume of text.

## When it fires — depth_gate

| Mode | Behaviour |
|---|---|
| **shallow** | **Skip.** 5–7 sources — there is nothing to filter, there is no context overload. |
| **medium** | **Mandatory.** 25–30 sources — noise already blurs the synthesis. |
| **deep** | **Mandatory.** 25–35+ — without the filter the synthesis drowns; here the effect is maximal. |

## Mechanics — CRAG evaluator + relevant-only extraction

Executor: the subagent (medium effort from the frontmatter, as in the `model_routing.md` matrix): two paired classifications over verbatim quotes; on low effort it skips the checks.

**Input:** the finished `claims.csv` (Phase 5) + `sources/NN.md` with `used: Y`.

For every row of `claims.csv` (a claim) and each of its sources from the `sources` column:

1. **Relevance classifier (CRAG evaluator).** Read the source's `Key quotes` and ask: «does at least one quote from this source support exactly this claim?» Three outcomes with an explicit threshold:
   - **Correct (relevant)** — there is ≥1 quote directly concerning the claim → keep, extract those quotes.
   - **Ambiguous** — the quotes touch the topic but do not confirm/refute the claim directly → keep with the mark `weak`, extract as context, not as evidence.
   - **Incorrect (irrelevant)** — no quote concerns the claim → **drop** this (claim, source) pair. The source stays in `sources/` but does not go into synthesis *under this claim*.

2. **Relevant-only extraction (Search-o1 Reason-in-Documents / CRAG recompose).** For keep pairs — carry into `evidence/` only the relevant quotes, not the whole file. «Decompose-then-recompose»: out of all the source's `Key quotes`, keep the subset that actually works for the claim.

3. **Correction trigger (optional, if the budget allows).** If after the filter a claim has **not a single relevant source left** (all dropped) — that is a signal that the claim rested on noise. Action: mark the claim `status: data-insufficient` in `claims.csv` OR (if the Phase 5 gap budget is not yet exhausted) one targeted follow-up search. Do not silently leave a claim without support.

**Calibration (important — a limitation of the method).** An LLM-as-evaluator in prompt mode systematically *overstates* relevance (self-grading bias, acknowledged in CRAG). Countermeasures: (a) the classifier judges by the verbatim `Key quotes`, not by the summary; (b) in doubt — `Ambiguous`, not `Correct`; (c) drop requires an explicit «no quote concerns it», not «it relates weakly».

## Axis 2 — authority: is the source entitled to assert this

Relevance asks «is this fragment about this claim?». Authority asks **«is this source entitled
to assert such a thing?»**. These are different questions, and the second was nowhere
in the skill: three verification layers (6.5 liveness / faithfulness / qualifiers) check
that the source **said** what is quoted, and none checks **who it is and where it
got it from**. A content farm with a verbatim quote passes faithfulness perfectly.

The only defence so far is the `credibility` scale, and it is set by the very agent
that found the source and has already spent work on it (H7). A taste-based scale plus
a conflict of interest plus the absence of a re-check. The 5.5 classifier did not look for the source —
independence here comes for free.

**The verdict is issued RELATIVE to the claim, not absolutely.** A forum is entitled to assert
«practitioners complain about X» and not entitled to «market share 34%». One and the same source
gets different verdicts under different claims.

### Perimeter — only load-bearing pairs (otherwise the layer gets switched off)

Running authority on all pairs is expensive and harmful: the layer would drown in firings and
would be switched off — exactly as the Layer 3 calibration in `runtime_verification.md` warns.
Run **only** pairs where the source actually carries weight:

- the claim goes into `memo.md`, F1 (TL;DR) or F9; **or**
- the claim contains a number; **or**
- the source is the claim's only root (`roots` without a second value); **or**
- the source already has a `caveat` ≠ `-`.

For medium this is usually 3–8 sources. Model — the configured model, low effort.

### Checklist (checkable signs, NOT a scale)

Judge by signs that can be put on the table, not by impression — the taste-based scale
is the very cause of the inflation:

1. Is the author named and is their affiliation checkable?
2. For a quantitative assertion — are the methodology/sample described?
3. Is there a link to a primary source, and is it live? (reuse `eval/check_citations.py`, do not check by hand)
4. No signs of sponsored material / partner content / affiliate?
5. For an academic one — has the work been retracted? (Crossref / Retraction Watch — free)
6. No signs of a content farm / machine generation: no author, no date, template structure, a stream of identical pages?
7. Does the declared `origin_kind` match what is visible in the text (a retelling of a report cannot be `measurement`)?

### Verdicts and fail-closed

| Verdict | When | Consequence |
|---|---|---|
| `qualified` | the signs are in place, the source is entitled to assert it | goes into synthesis as full support |
| `unqualified-for-this-claim` | for this claim the source is not competent (a forum on market share, a vendor on its own figure) | cannot be the **only** support of the claim; it lands in `evidence/` as context, not as evidence |
| `unknown` | there are not enough signs to decide | **quarantine, not a pass** |

**`unknown` is quarantine.** The source stays in `sources/` but cannot be the only
support of the claim and does not give `confidence: high`. A defence that on a mismatch
«quietly passes» is not a defence; that is exactly how checks have already died in this
skill. Symmetric to the primary-first rule.

**The calibration asymmetry — as in relevance, but mirrored.** There doubt → `Ambiguous`
(do not drop). Here doubt → `unknown` (do not issue `qualified`). The general rule:
**doubt never gives a source more rights than it has proved, and never takes away more than
has been proved against it.** The right to discard is more dangerous than the right to keep —
and the more dangerous the more capable the model: a rise in capability yields more confident action,
not sounder judgement (Anthropic Frontier Red Team, 13.08.2026).

### Output — `.verify/authority.json`

The same I/O contract as 6.5: one file is the single source of truth, it is read by
the F10 header and the phase gate, and no one recomputes it.

```json
{
  "generated_at": "2026-08-16",
  "scope": "load-bearing pairs only",
  "pairs": [
    {"claim_id": "C1", "source": "s07", "verdict": "qualified",
     "checks": {"named_author": true, "methodology": true, "primary_link_live": true,
                "sponsored": false, "retracted": false, "content_farm": false,
                "origin_kind_matches": true}, "note": "SEC filing, methodology in appendix B"},
    {"claim_id": "C1", "source": "s11", "verdict": "unknown",
     "checks": {"named_author": false, "methodology": false, "primary_link_live": null,
                "sponsored": null, "retracted": false, "content_farm": true,
                "origin_kind_matches": false},
     "note": "no author, no date, template structure; origin_kind claimed measurement but text retells s07"}
  ],
  "quarantined": ["s11"],
  "qualified_share": 0.71
}
```

## Output — the `evidence/` layer

A new folder `<slug>/evidence/`. One file per claim (not per source — the claim here is the axis of grouping):

```
evidence/
├── C1.md        # relevant-only quotes under claim C1, grouped by source
├── C2.md
└── ...
```

Template `evidence/CN.md`:

```markdown
---
claim_id: C1
claim: "<claim text from claims.csv>"
kept_sources: [03, 07, 12]      # ids of the sources that passed the filter
dropped_sources: [05, 09]        # filtered out as irrelevant under this claim
status: relevant | weak | data-insufficient
---

## C1 — <short claim>

### s03 (relevance: Correct · authority: qualified)
> «<verbatim relevant quote>» — [source](../sources/03_slug.md)

### s07 (relevance: Ambiguous · authority: unknown → quarantine)
> «<contextual quote>» — [source](../sources/07_slug.md)
```

The authority axis is filled only for pairs that fell inside the perimeter (load-bearing); for the rest
the field is omitted — a missing mark means «not checked», not «qualified».

**Synthesis (Phase 6) reads `evidence/CN.md`, not the whole pool of `sources/`** — for medium/deep. For shallow (5.5 is skipped) synthesis reads `sources/NN.md` as before. Spot-checking against `sources/NN.md` on contested places remains (Phase 6 step 1 already requires it).

**`evidence/CN.md` is also the input for Phase 6.5 Layer 2 (faithfulness).** The claim↔quote linkage that 5.5 makes is exactly the pairs the faithfulness check needs («does the source really support the thesis»). Phase 6.5 reads `evidence/CN.md` instead of rescanning `sources/` to decide which quote belongs to which claim (that would be duplicating 5.5's work). `claim_id` is the shared join key. Thus one artifact of 5.5 serves both synthesis (input) and verification (6.5). See `references/runtime_verification.md` → Layer 2.

## Relation to `findings/` (deep)

The existing `findings/` layer (deep, Phase 6) is an aggregation of *conclusions* (atomic theses). `evidence/` is filtered *raw material* (relevant-only quotes) under a claim. The order for deep: `sources/` → **5.5 evidence/** → synthesis → `findings/`. For medium: `sources/` → **5.5 evidence/** → synthesis (without findings/). `evidence/` makes the findings synthesis cleaner; it does not replace it.

## Anti-patterns

- ❌ Rewriting/trimming `sources/NN.md`. It is an archive. The filter writes into `evidence/`, it does not touch the source.
- ❌ Filtering by credibility/`total` instead of relevance. An authoritative source ≠ relevant to this claim.
- ❌ Dropping a pair on «relates weakly». Drop only on «no quote concerns the claim»; doubt → Ambiguous/keep.
- ❌ Silently leaving a claim whose sources were all filtered out. → `data-insufficient` or a follow-up search.
- ❌ Running 5.5 on shallow. Few sources — nothing to filter, only friction.
- ❌ Classifying by the summary. Judge by the verbatim `Key quotes` (self-grading on a retelling inflates even more).
- ❌ **Treating `unknown` in authority as «good enough».** It is quarantine: not the only support, not `high`. A check that silently passes when the signs are missing is equivalent to its absence.
- ❌ **Running authority on all pairs.** The perimeter is load-bearing pairs. A layer with a high false-firing rate gets switched off entirely, and then neither it nor the thing it was installed for works.
- ❌ Issuing an authority verdict «in general», with no tie to a claim. A source is sometimes fit under one thesis and unfit under the neighbouring one.
- ❌ Recomputing the verdicts in F10 or the rubric. The single source is `.verify/authority.json`, as `citations.json`/`faithfulness.json` for 6.5.
- ❌ Fixing `unqualified` by lowering the requirements on the claim instead of finding a proper source.

## Phase 5.5 checklist

- [ ] Mode medium/deep (shallow → skip)
- [ ] For every (claim, source) pair — the relevance classifier Correct/Ambiguous/Incorrect over verbatim quotes
- [ ] Irrelevant pairs dropped under this claim (the source stayed in `sources/`)
- [ ] Relevant-only quotes carried into `evidence/CN.md` (per claim)
- [ ] A claim with not a single relevant source → `data-insufficient` or a targeted follow-up search
- [ ] The perimeter of load-bearing pairs defined (memo/F1/F9, numbers, sole root, `caveat` ≠ `-`)
- [ ] For every load-bearing pair — an authority verdict by the signs checklist (not by impression)
- [ ] Verdicts written to `.verify/authority.json`, quarantines listed in `quarantined`
- [ ] No claim rests alone on a source with `unknown`/`unqualified-for-this-claim`
- [ ] `sources/NN.md` not modified
- [ ] Synthesis (Phase 6) directed to read `evidence/`, not the whole pool of sources
