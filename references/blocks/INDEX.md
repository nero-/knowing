<!-- translated from upstream/references/blocks/INDEX.md @ e233797 — see docs/TRANSLATION.md -->
# Block Library — INDEX

<!--gen:count:blocks-->106<!--/gen--> blocks in 10 categories. Composable sections for the final report.

## How to use

1. The skill determines the genre (see `../genres.md`) or assembles a custom one.
2. The skill loads only the needed categories `blocks/<category>.md` (progressive loading).
3. Each category file holds a Markdown template for every block, ready to copy.
4. In the final report the blocks go in the order from the `plan.md` → `blocks:` list.

## Categories

| Cat | File | Blocks | Purpose |
|---|---|---|---|
| FRAME | [frame.md](frame.md) | F1-F10 | Report frame: TL;DR, scope, background, claim, metadata |
| EXPLAIN | [explain.md](explain.md) | E1-E14 | Explaining the structure: mental model, glossary, mechanism |
| COMPARE | [compare.md](compare.md) | C1-C13 | Comparison and choice: matrices, scoring, trade-offs |
| MAP | [map.md](map.md) | M1-M12 | Mapping: profiles, positioning, trends |
| VALIDATE | [validate.md](validate.md) | V1-V10 | Truth verification: falsification, evidence grades |
| ANALYZE | [analyze.md](analyze.md) | A1-A13 | Structured analysis: SWOT, timeline, root cause |
| CLOSE | [close.md](close.md) | Z1-Z12 | Closing: counter-args, open Q, next research |
| PEOPLE | [people.md](people.md) | P1-P7 | People, teams, behavior: persona, journey, incentives |
| NUMBERS | [numbers.md](numbers.md) | N1-N8 | Quantitative: metrics, market sizing, forecasts |
| CONTEXT | [context.md](context.md) | X1-X7 | External context: regulation, geo, culture |

## Full table of all <!--gen:count:blocks-->106<!--/gen--> blocks

### FRAME

| ID | Slug | What | When |
|---|---|---|---|
| F1 | `tldr` | TL;DR 2-4 lines with confidence | Always |
| F2 | `decision-context` | What we are deciding, options, constraints, stakes | Decision, custom-decision |
| F3 | `scope` | What is in/out of scope, cut as of a date | Landscape, validation, any boundaries |
| F4 | `claim-precise` | Precise formulation of the claim under test | Validation |
| F5 | `metadata` | Author/date/depth/version/status footer | Always |
| F6 | `key-finding-callout` | The main single insight, highlighted | Long reports |
| F7 | `executive-summary` | 1-page TL;DR for stakeholders | Decision/landscape for non-technical readers |
| F8 | `glossary-link` | Link to an external/shared glossary | If there is a project glossary |
| F9 | `background` | Why the question is posed this way — background, causes, 5-10 lines | Medium/deep, all genres (default) |
| F10 | `verification-header` | Four axes: liveness × faithfulness × qualifiers × constructs + independence of sources | Medium/deep, after Phase 6.5 verify |

### EXPLAIN

| ID | Slug | What | When |
|---|---|---|---|
| E1 | `mental-model` | ASCII diagram of the structure + 3-5 entities | Explainer, technical |
| E2 | `glossary-mini` | 5-10 terms with definitions | Explainer always, complex vocabulary |
| E3 | `glossary-full` | Extended glossary with examples | Custom if the terminology is critical |
| E4 | `stepwise` | Step-by-step mechanism (1, 2, 3...) | Explainer, sequential processes |
| E5 | `variants` | Implementation variants + where they occur | Explainer |
| E6 | `worked-example` | A real case with a walkthrough of the scenario | Explainer, education |
| E7 | `common-confusions` | What X does NOT mean, what it is confused with | Explainer, validation |
| E8 | `prerequisites` | What you need to know before reading | Technical with a complex background |
| E9 | `analogy` | An analogy from a familiar field | Complex technical topics |
| E10 | `failure-modes` | How and why it breaks | Technical explainer, debugging |
| E11 | `edge-cases` | Edge cases and how they are handled | Technical explainers |
| E12 | `design-rationale` | Why it is designed this way, design alternatives | Architecture explainer |
| E13 | `flow-diagram` | Data/process flow (ASCII or Mermaid) | Process explainer |
| E14 | `state-machine` | States + transitions + triggers | Technical systems with state |

### COMPARE

| ID | Slug | What | When |
|---|---|---|---|
| C1 | `options-matrix` | Table of options × criteria (no weights) | Decision |
| C2 | `weighted-score` | Options × criteria with weights + total | Decision when the criteria are not equally weighted |
| C3 | `best-fit-when` | For each option — «take it if X» | Decision always |
| C4 | `reversibility-stakes` | One-way vs two-way door + stakes | Decision |
| C5 | `trade-offs` | What you lose by choosing each option | Decision always |
| C6 | `recommendation-conditional` | «Take X if Y, otherwise Z» | Decision final |
| C7 | `pre-mortem` | «A year later X has failed, why» | Decision high-stakes |
| C8 | `cost-benefit` | Cost vs benefit, structured | Custom for financial ones |
| C9 | `pros-cons-each` | Pro/Con lists for each option | Quick decision, light-weight |
| C10 | `feature-matrix` | Features × Options (yes/no/partial) | Product comparison |
| C11 | `migration-path` | How to do the migration A→B | Decision with reversibility |
| C12 | `decision-tree` | Tree of «if X — Y, otherwise W» | Complex multi-condition |
| C13 | `kill-criteria` | When to abandon each option | Decision risky ones |

### MAP

| ID | Slug | What | When |
|---|---|---|---|
| M1 | `categories` | Dividing the field into categories with definitions | Landscape |
| M2 | `profile-card` | Player card: founded/scale/strength/weakness | Landscape ×N, competitor analysis |
| M3 | `positioning-map` | 2×2 ASCII map with justification of the axes | Landscape |
| M4 | `trends` | What is growing/dying/appearing | Landscape, market analysis |
| M5 | `white-spaces` | Where the empty niches are | Landscape for product strategy |
| M6 | `genealogy` | Who came out of where, who forked whom | Custom for academic/tech |
| M7 | `ranked-list` | Top-N with justification | Custom for «top X» |
| M8 | `value-chain` | Value chain: who sits at which link | Industry analysis |
| M9 | `network-graph` | Who is connected to whom | Relationships in field |
| M10 | `funding-tree` | Investment ties, ownership | Startup ecosystem |
| M11 | `geographic-distribution` | Where the players are located | Geo-distributed |
| M12 | `lifecycle-stage` | Who is at which stage (early/growth/mature/decline) | Industry maturity |

### VALIDATE

| ID | Slug | What | When |
|---|---|---|---|
| V1 | `falsification-criteria` | What would force us to call it false (in advance) | Validation always |
| V2 | `evidence-graded` | Evidence FOR/AGAINST with quality A/B/C | Validation |
| V3 | `conflicting-evidence` | Contradictory data + why they diverge | Validation, anything with conflicts |
| V4 | `base-rates` | Apriori probability / prior | Validation of medical/scientific claims |
| V5 | `verdict-conditional` | «True under X, false under Y» | Validation always |
| V6 | `what-would-change-verdict` | What data would shift the verdict | Validation |
| V7 | `replication-status` | Whether it has been reproduced, by whom, how many times | Scientific validation |
| V8 | `sample-size-analysis` | Sample size, statistical power | Quantitative validation |
| V9 | `methodology-critique` | Critique of the source's methodology | Validation of scientific claims |
| V10 | `bayesian-update` | Prior + evidence → posterior | Probabilistic validation |

### ANALYZE

| ID | Slug | What | When |
|---|---|---|---|
| A1 | `data-table` | Parametric table object × indicator | Custom «by indicators» |
| A2 | `timeline` | Chronology of events with dates | Custom historical / sequential |
| A3 | `qa-list` | Q→A atomic pairs with confidence + sources | Q&A always |
| A4 | `hypotheses-outcome` | Hypothesis table: confirmed / partial / contradicted | Q&A, validation |
| A5 | `swot` | Strengths/Weaknesses/Opportunities/Threats | Business/product analysis |
| A6 | `risk-register` | Risk list: probability × impact | Custom risky ones |
| A7 | `dependency-graph` | What depends on what, critical path | Project planning, system |
| A8 | `bottleneck-analysis` | Where the bottlenecks are and why | Performance, ops |
| A9 | `force-field` | Forces FOR vs AGAINST change | Change analysis, Lewin |
| A10 | `5-whys` | Chain of «why» down to the root cause | Root cause |
| A11 | `swot-extended` | SWOT + actionable output from each quadrant | Strategic analysis |
| A12 | `pestle` | Political/Economic/Social/Tech/Legal/Environmental | Macro analysis |
| A13 | `before-after` | Before and after the change, with metrics | Impact analysis |

### CLOSE

| ID | Slug | What | When |
|---|---|---|---|
| Z1 | `counter-arguments` | Steel-man counter-arguments | Medium/deep always |
| Z2 | `open-questions` | What is not closed, what to dig into | Always |
| Z3 | `next-research` | 2-3 follow-up research runs | Always |
| Z4 | `actionable-next-steps` | What to do NOW (the first 3 actions) | Decision, validation |
| Z5 | `map-of-sources` | Sources by type + opposition voices | Always |
| Z6 | `findings-index` | Links to findings/FN.md | If there are major findings |
| Z7 | `confidence-summary` | Summary of confidence across all findings | Long reports |
| Z8 | `assumptions-log` | List of assumptions | Any research with assumptions |
| Z9 | `glossary-final` | Final glossary from the report | Long ones with abundant terminology |
| Z10 | `update-triggers` | What must happen for an update | All research (life cycle) |
| Z11 | `refresh-targets` (separate file) | What exactly to check on update — entities, numbers, hypotheses | Medium/deep — mandatory |
| Z12 | `so-what-for-you` | Projection of the findings onto the user's case: action + trade-off + kill-criteria | Medium/deep — mandatory |

### PEOPLE

| ID | Slug | What | When |
|---|---|---|---|
| P1 | `persona` | User profiles: needs/behaviors/pain | UX, product |
| P2 | `team-org` | Team/organization structure, roles | Competitor analysis, due diligence |
| P3 | `key-people` | Cards for key people (founder, lead) | Competitors, industry |
| P4 | `user-journey` | Journey scenario: steps + emotions + friction | UX, product design |
| P5 | `behavioral-patterns` | Behavioral patterns of the participants | Behavioral analysis |
| P6 | `incentive-structure` | Who gets what, what the incentives are | Game theory, market design |
| P7 | `expert-opinion` | Expert opinion card with conflict of interest | Expert-driven validation |

### NUMBERS

| ID | Slug | What | When |
|---|---|---|---|
| N1 | `metric-tracker` | Specific metrics with numbers | «by metrics», «by KPI» |
| N2 | `market-sizing` | TAM/SAM/SOM | Market research |
| N3 | `growth-rates` | YoY/CAGR with sources | Growth analysis |
| N4 | `unit-economics` | CAC, LTV, payback period, margin | SaaS/business analysis |
| N5 | `cost-breakdown` | Cost structure | Financial analysis, due diligence |
| N6 | `benchmark-numbers` | Industry benchmarks for comparison | Performance analysis |
| N7 | `forecast` | Forecasts of future values with ranges | Forecasting, planning |
| N8 | `historical-data` | Time series of historical values | Data analysis, trend |

### CONTEXT

| ID | Slug | What | When |
|---|---|---|---|
| X1 | `regulatory` | Regulatory context: laws, compliance | Fintech, medtech, regulated |
| X2 | `geo-context` | Differences by country/region | Global markets, jurisdictions |
| X3 | `cultural-context` | Cultural specifics | Cross-cultural topics |
| X4 | `historical-context` | What came before and why it matters now | Historical, deep explainer |
| X5 | `political-context` | Political factors | Geopolitics, sanctions |
| X6 | `tech-stack-context` | The underlying technologies, dependencies | Tech research |
| X7 | `ecosystem` | Ecosystem around the topic: neighbors | Platform analysis |

## Progressive loading discipline

With <!--gen:count:blocks-->106<!--/gen--> blocks it is critical not to load everything into context.

```
Main thread:
1. Reads SKILL.md (the frame)
2. After reframing → reads references/genres.md
3. Determines the genre or the assembly
4. Reads blocks/INDEX.md (index only — this file)
5. For a standard genre → reads 2-4 category files
6. For custom → block selection by heuristic, reads only their categories
```

Do not load INDEX.md and a category file at the same time — INDEX.md contains enough to decide which blocks to take.

## Block composition

Each category file contains, for each block, a **Composition** section — which blocks it works well with, which it duplicates, which are mutually exclusive.

Base rules:
- `tldr` is written LAST (after the other blocks).
- `counter-arguments` goes after the main content, before closing.
- `metadata` always at the very end as a footer.
- `map-of-sources` is always present, even if short.
- Duplicating blocks are mutually exclusive: `glossary-mini` OR `glossary-full`, not both.
