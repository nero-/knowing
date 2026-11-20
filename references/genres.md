<!-- translated from upstream/references/genres.md @ e233797 — see docs/TRANSLATION.md -->
# Genres — block presets

## Contents

- How to use
- Search channels by genre
- Stat sources by genre
- Genre selection heuristics
- qa — open-ended research
- explainer — «how X is built»
- decision — «what to choose, X or Y»
- landscape — «map of the field»
- validation — «is X true»
- custom — assembled for the question
- Composition rules

Six genres of the final report. Five standard ones are block presets. The sixth is custom (assembled for the question).

## How to use

1. After reframing (Phase 1) the skill determines the genre from the wording of the question.
2. The skill announces it in ONE line: «Genre: <genre>. Blocks: <list>. OK?».
3. The user confirms / edits the set.
4. The final `<date>_<genre>.md` is built from the blocks in the stated order.

## Search channels by genre

See `channels.md` for the full catalog of <!--gen:count:channels-->28<!--/gen--> channels. Here — the recommended mix per genre.

| Genre | Primary channels | Secondary | Use sparingly |
|---|---|---|---|
| **explainer** | web-general, academic, wikipedia-references, code-github | books-literature, video-talks, expert-individual | social-twitter |
| **decision** | web-general, forum-discussion, industry-reports, code-github (tech) | expert-individual, surveys-polls, podcasts | conference-proceedings |
| **landscape** | competitive-signals, news-current, industry-reports, product-analytics | patents, forum-discussion, trade-associations, industry-specific | social-twitter |
| **validation** | academic, preprint-servers, conference-proceedings | forum-discussion (opposition), expert-individual, surveys-polls, archive-historical | patents |
| **qa** | web-general + 2-3 by subtopic | varies | — |
| **custom** | for the chosen blocks | varies | — |

## Stat sources by genre

See `stat_sources/INDEX.md`. Relevant categories:

| Genre | Relevant stat_sources categories |
|---|---|
| **explainer** | core/science.md, core/gov_macro.md (if macro), industries/<industry>.md (if industry) |
| **decision** | core/consulting_industry.md, core/consumer_digital.md (for tech), industries/<industry>.md, core/companies_public.md (for evaluating a public co) |
| **landscape** | core/companies_private.md, core/companies_public.md, core/consulting_industry.md, industries/<industry>.md |
| **validation** | core/science.md (retractions, replications), core/health.md (if medical), core/gov_macro.md (for quantitative claims) |
| **qa** | varies by subtopic |
| **custom** | for the chosen blocks (`data-table` → numbers categories, `risk-register` → relevant industry, etc.) |

## Genre selection heuristics

The skill looks at the wording of the question. Signals:

| Signals in the question | Genre |
|---|---|
| «how it is built», «how it works», «what is», «tell me about the design of», «mental model» | **explainer** |
| «what to choose», «X or Y», «which is better», «should I take it», «where to invest», «which one to buy» | **decision** |
| «map», «who makes», «players in», «landscape», «competitive», «who writes about» | **landscape** |
| «is it true», «does it work», «is it effective», «is it harmful», «really», «myth or fact» | **validation** |
| «study it», «break it down», «dig in», an open question without an explicit genre, a series of related Qs | **qa** |
| «by indicators», «by metrics», «by criteria», a mix of genres, non-standard | **custom** |

If the heuristic yields several genres — choose the dominant one and offer custom as an alternative.

**The consumer overrides the topic.** Signals from the wording are only the first filter; the final form is dictated by the Decision Spec from Phase 1 (`plan.md` §0): **form = a function of the consumer's process, not of the topic type**. The same question «map of market X», for an investor reading one page before a meeting, is a decision memo with a compare matrix, not a 40-page landscape; for yourself-as-archive it is a full landscape. Check before fixing the genre: «will the consumer from the Decision Spec be able to take their next step having received a document of this form?» If not — the genre was chosen for the topic, not for the application; change it.

---

## qa — open-ended research

**When:** A series of related questions, meta-research, a topic without an explicit genre.

**Required blocks:** `tldr`, `qa-list`, `map-of-sources`, `metadata`. For medium/deep — additionally mandatory: `background` [F9], `so-what-for-you` [Z12], `actionable-next-steps` [Z4], `confidence-summary` [Z7].

**Recommended order:**
```
1.  tldr                      [F1]
2.  background                [F9]
3.  decision-context          [F2]   (if there is a decision)
4.  qa-list                   [A3]   ← main section
5.  hypotheses-outcome        [A4]   (if there were hypotheses in the plan)
6.  counter-arguments         [Z1]   (medium/deep)
7.  open-questions            [Z2]
8.  next-research             [Z3]
9.  confidence-summary        [Z7]
10. so-what-for-you           [Z12]  (before Z4)
11. actionable-next-steps     [Z4]
12. map-of-sources            [Z5]
13. findings-index            [Z6]   (if present)
14. metadata                  [F5]
```

**Optional additions:**
- `key-finding-callout` [F6] if there is one dominant insight

---

## explainer — «how X is built»

**When:** To understand the structure of the topic, a mental model, not a decision.

**Required blocks:** `tldr`, `mental-model`, `stepwise`, `map-of-sources`, `metadata`. For medium/deep — additionally mandatory: `background` [F9], `so-what-for-you` [Z12], `actionable-next-steps` [Z4], `confidence-summary` [Z7].

**Recommended order:**
```
1.  tldr                      [F1]
2.  background                [F9]
3.  prerequisites             [E8]   (if the reader needs them)
4.  glossary-mini             [E2]   ← terms before the diagram
5.  mental-model              [E1]   ← the structural diagram
6.  stepwise                  [E4]   ← how it works
7.  variants                  [E5]   (if there are implementation variants)
8.  worked-example            [E6]   (for education-style)
9.  common-confusions         [E7]
10. failure-modes             [E10]  (for technical topics)
11. edge-cases                [E11]  (optional)
12. design-rationale          [E12]  (for an architecture explainer)
13. counter-arguments         [Z1]
14. open-questions            [Z2]
15. next-research             [Z3]
16. confidence-summary        [Z7]
17. so-what-for-you           [Z12]  (before Z4)
18. actionable-next-steps     [Z4]
19. map-of-sources            [Z5]
20. metadata                  [F5]
```

**Subset for deep technical:**
- + `flow-diagram` [E13] or `state-machine` [E14] instead of stepwise
- + `analogy` [E9] for very complex topics
- + `tech-stack-context` [X6] for a tech foundation

**Optional additions:**
- `historical-context` [X4] if «how we got here» matters

---

## decision — «what to choose, X or Y»

**When:** Comparing options to make a decision. With an explicit recommendation.

**Required blocks:** `tldr`, `decision-context`, `options-matrix`, `recommendation-conditional`, `map-of-sources`, `metadata`. For medium/deep — additionally mandatory: `background` [F9], `so-what-for-you` [Z12], `confidence-summary` [Z7].

**Recommended order:**
```
1.  tldr                      [F1]
2.  background                [F9]
3.  executive-summary         [F7]   (optional, for stakeholders)
4.  decision-context          [F2]   ← the decision frame
5.  options-matrix            [C1]
6.  weighted-score            [C2]   (if the criteria are not equally weighted)
7.  feature-matrix            [C10]  (for product decisions)
8.  pros-cons-each            [C9]   (alternative to a matrix for quick)
9.  best-fit-when             [C3]
10. trade-offs                [C5]
11. reversibility-stakes      [C4]
12. cost-benefit              [C8]   (for financial ones)
13. risk-register             [A6]   (for risky ones)
14. pre-mortem                [C7]   (high-stakes)
15. migration-path            [C11]  (if reversible)
16. decision-tree             [C12]  (for complex multi-condition ones)
17. kill-criteria             [C13]
18. counter-arguments         [Z1]
19. recommendation-conditional [C6]  ← final recommendation
20. confidence-summary        [Z7]
21. so-what-for-you           [Z12]  (before Z4)
22. actionable-next-steps     [Z4]
23. assumptions-log           [Z8]
24. open-questions            [Z2]
25. next-research             [Z3]
26. map-of-sources            [Z5]
27. metadata                  [F5]
```

**Subsets:**
- **Quick decision (shallow):** tldr + decision-context + pros-cons-each + best-fit-when + recommendation-conditional + sources + metadata
- **High-stakes (deep):** all blocks + pre-mortem + kill-criteria

---

## landscape — «map of the field»

**When:** Players/solutions in a field, without a priority of choice.

**Required blocks:** `tldr`, `scope`, `categories`, `profile-card`, `map-of-sources`, `metadata`. For medium/deep — additionally mandatory: `background` [F9], `so-what-for-you` [Z12], `actionable-next-steps` [Z4], `confidence-summary` [Z7].

**Recommended order:**
```
1.  tldr                      [F1]
2.  background                [F9]
3.  scope                     [F3]   ← boundaries of the map
4.  categories                [M1]   ← division of the field
5.  profile-card × N          [M2]   ← player cards by category
6.  key-people                [P3]   (for deep landscapes)
7.  positioning-map           [M3]
8.  value-chain               [M8]   (industry analysis)
9.  network-graph             [M9]   (relationships)
10. funding-tree              [M10]  (startup ecosystem)
11. geographic-distribution   [M11]  (geo-distributed)
12. lifecycle-stage           [M12]
13. trends                    [M4]
14. white-spaces              [M5]   (for product strategy)
15. ecosystem                 [X7]   (broader context)
16. counter-arguments         [Z1]
17. open-questions            [Z2]
18. next-research             [Z3]
19. update-triggers           [Z10]  ← a landscape goes stale fast
20. confidence-summary        [Z7]
21. so-what-for-you           [Z12]  (before Z4)
22. actionable-next-steps     [Z4]
23. map-of-sources            [Z5]
24. metadata                  [F5]
```

**Subsets:**
- **Minimal landscape:** tldr + scope + categories + profile-cards + trends + sources + metadata
- **Investment-focused:** + funding-tree + key-people + lifecycle-stage + white-spaces

---

## validation — «is X true»

**When:** Verifying a claim. With a verdict.

**Required blocks:** `tldr`, `claim-precise`, `falsification-criteria`, `evidence-graded`, `verdict-conditional`, `map-of-sources`, `metadata`. For medium/deep — additionally mandatory: `background` [F9], `so-what-for-you` [Z12], `confidence-summary` [Z7].

**Recommended order:**
```
1.  tldr                      [F1]
2.  background                [F9]
3.  claim-precise             [F4]   ← the precise formulation
4.  scope                     [F3]   ← where it applies
5.  base-rates                [V4]   (for probabilistic claims)
6.  falsification-criteria    [V1]   ← BEFORE evidence
7.  evidence-graded           [V2]   ← FOR/AGAINST
8.  conflicting-evidence      [V3]   (if present)
9.  replication-status        [V7]   (for scientific claims)
10. sample-size-analysis      [V8]   (for quantitative)
11. methodology-critique      [V9]   (deep)
12. expert-opinion            [P7]   (if expert-driven)
13. bayesian-update           [V10]  (for probabilistic)
14. verdict-conditional       [V5]   ← the main verdict
15. what-would-change-verdict [V6]
16. common-confusions         [E7]   (a claim is often confused with X)
17. counter-arguments         [Z1]
18. confidence-summary        [Z7]
19. so-what-for-you           [Z12]  (before Z4)
20. actionable-next-steps     [Z4]   (what to do with this verdict)
21. assumptions-log           [Z8]
22. open-questions            [Z2]
23. next-research             [Z3]
24. map-of-sources            [Z5]
25. metadata                  [F5]
```

**Subsets:**
- **Quick validation:** tldr + claim-precise + falsification-criteria + evidence-graded + verdict-conditional + sources + metadata
- **Scientific validation:** all + methodology-critique + replication-status + sample-size

---

## custom — assembled for the question

**When:** The question fits no standard genre. Hybrid questions. Specific analytical tasks.

**Required (always):** `tldr`, `map-of-sources`, `metadata`. For medium/deep — additionally mandatory: `background` [F9], `so-what-for-you` [Z12], `actionable-next-steps` [Z4], `confidence-summary` [Z7].

**Block selection heuristics:**

The skill looks at the signals in the question:

| Signal | Add block |
|---|---|
| «by indicators / metrics / KPI» | `data-table` [A1], `metric-tracker` [N1] |
| «top N», «the best», «rank them» | `ranked-list` [M7] |
| «how X evolved», «the history of X» | `timeline` [A2], `historical-context` [X4], `genealogy` [M6] |
| «risks of X», «dangers» | `risk-register` [A6], `failure-modes` [E10] |
| «SWOT X», «strengths/weaknesses» | `swot` [A5] or `swot-extended` [A11] |
| «macro environment», «environment» | `pestle` [A12] |
| «is it worth investing», «cost / benefit» | `cost-benefit` [C8], `unit-economics` [N4] |
| «competitors + indicators» (like mine) | `data-table` + `profile-card` + `trends` + `competitors` mix |
| «team», «who works there», «structure» | `team-org` [P2], `key-people` [P3] |
| «users / customers» | `persona` [P1], `user-journey` [P4] |
| «why is it like this / root cause» | `5-whys` [A10], `dependency-graph` [A7] |
| «bottlenecks», «bottleneck» | `bottleneck-analysis` [A8] |
| «forces for and against the change» | `force-field` [A9] |
| «before and after» | `before-after` [A13] |
| «forecast / projection» | `forecast` [N7] + `historical-data` [N8] |
| «market size / TAM» | `market-sizing` [N2] |
| «regulatory / laws» | `regulatory` [X1] |
| «culturally / by cultures» | `cultural-context` [X3] + `geo-context` [X2] |
| «politics / sanctions / geopolitics» | `political-context` [X5] |
| «ecosystem» | `ecosystem` [X7] |
| «mental model / design» (as part of a hybrid) | + `mental-model` [E1] + `glossary-mini` [E2] |
| «choice» (as part of a hybrid) | + `options-matrix` [C1] + `recommendation-conditional` [C6] |

**Base scaffolding for custom:**
```
1. tldr [F1]
2. background [F9]
3. scope [F3] (if boundaries matter)
4. <blocks chosen by the heuristic>
5. counter-arguments [Z1]
6. open-questions [Z2]
7. next-research [Z3]
8. confidence-summary [Z7]
9. so-what-for-you [Z12] (before actionable-next-steps)
10. actionable-next-steps [Z4]
11. map-of-sources [Z5]
12. metadata [F5]
```

**User confirmation:** the skill outputs in one line:
```
"Custom report. Blocks: tldr, scope, data-table, profile-card×N, trends,
counter-args, open-q, sources. OK? (yes / remove X / add Y)"
```

### Examples of ready-made custom sets

**Competitors by indicators:**
```
[tldr, scope, data-table, profile-card×N, trends, counter-args, open-q, next-research, sources, metadata]
```

**Hybrid explainer + decision (something like «how X works and what to choose»):**
```
[tldr, mental-model, glossary-mini, stepwise, options-matrix, best-fit-when,
recommendation-conditional, counter-args, sources, metadata]
```

**Risk analysis for a decision:**
```
[tldr, decision-context, risk-register, failure-modes, force-field, pre-mortem,
actionable-next-steps, sources, metadata]
```

**Cost-benefit personal decision:**
```
[tldr, scope, cost-benefit, pros-cons-each, decision-tree, recommendation-conditional,
actionable-next-steps, sources, metadata]
```

**Historical deep-dive:**
```
[tldr, scope, timeline, historical-context, genealogy, key-people, mental-model,
counter-args, open-q, sources, metadata]
```

**Behavioral analysis:**
```
[tldr, scope, persona, user-journey, behavioral-patterns, incentive-structure,
counter-args, open-q, sources, metadata]
```

---

## Composition rules

### What is always present
- `tldr` [F1] — the first block (but written LAST)
- `map-of-sources` [Z5] — mandatory
- `metadata` [F5] — the last one (footer)
- For medium/deep in ALL genres — mandatory: `background` [F9], `so-what-for-you` [Z12], `actionable-next-steps` [Z4], `confidence-summary` [Z7] (see the genre sections above).

### Mutually exclusive (do not use together)
- `glossary-mini` OR `glossary-full` OR `glossary-link` — choose ONE
- `swot` OR `swot-extended` — not both
- `options-matrix` without weights OR `weighted-score` — usually one (but both are acceptable for a full decision)
- `mental-model` OR `flow-diagram` OR `state-machine` — choose by the type of system

### Dependency order
- `glossary-*` goes BEFORE `mental-model` (terms before the diagram)
- `background` [F9] goes IMMEDIATELY AFTER `tldr`/before `scope` — the «why this question» context before the frame and the content
- `scope` BEFORE the main blocks (frame before content)
- `claim-precise` BEFORE `falsification-criteria` BEFORE `evidence-graded`
- `base-rates` BEFORE `evidence-graded` (prior before update)
- `counter-arguments` AFTER the main content, BEFORE closing
- `recommendation-conditional` AFTER all comparison blocks
- `so-what-for-you` [Z12] AFTER the `confidence-summary`/`map-of-sources` sections, but BEFORE `actionable-next-steps` [Z4] — first the projection onto the case, then concrete actions

### Density rules
- Shallow report: 5-9 blocks
- Medium report: 9-15 blocks
- Deep report: 15-25 blocks
- Do not multiply blocks for plumage. Only if each answers a specific part of the question.
