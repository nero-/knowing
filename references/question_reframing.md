<!-- translated from upstream/references/question_reframing.md @ e233797 — see docs/TRANSLATION.md -->
# Question Reframing — Phase 1 deepdive

Goal: before any search, make sure we are searching for the right thing. Most bad research is badly posed questions, not bad search.

## What the phase does

1. **Rewrite the question in your own words.** Start with «I understand the task as: …». This is not politeness, it is a check: are you seeing the same thing the user said?

2. **Assemble a Decision Spec — a structural contract instead of a single line saying «decision».** Rationale: the main failure of research is not bad search but a report that leads nowhere, because the author does not know what they will do with the answer. Three mandatory fields (they go into `plan.md` §0, are shown at gate 3.7, and are executed in Phase 8):
   - **Decision/action**: verb + object + deadline («choose a payment provider by 15.08»). Not «understand the topic».
   - **Consumer and their next step**: who reads the report and what they physically do afterwards (commits the choice themselves / an investor reads 1 page / a colleague pastes it into their own document).
   - **If-then forks** (≥1, falsifiable): «if the research shows X — I do A; if Y — I do B».

   **The fork test is hard.** Not a single if-then fork ⇒ the research will change nothing ⇒ an honest downgrade to shallow «curiosity» mode with an explicit note in plan.md — no heavy pipeline. This is not a punishment but a saving: the deep budget is not spent on a doc that leads nowhere. A vague answer (no verb/artifact/deadline) → one push-back, then an assumption with the note «the application is the agent's hypothesis, not confirmed by the user».

   **Ledger check.** If `~/.claude/research/applications_ledger.csv` exists — read the latest rows before reframing. ≥2 unapplied runs in a row (status `unused`/`deferred`) → show the pattern to the user: «the last N research runs led to no decision — here are their unarticulated specs; how is this one different?»

3. **Formulate hypotheses.** 2–4 of them. A hypothesis is a statement that data can refute. Not «study the topic» (that is not a hypothesis), but «X is better than Y on criterion Z» (refutable).

3.5. **Multi-perspective decomposition (STORM) — for coverage.** In addition to the hypotheses, generate N perspectives-personas; each looks at the topic from its own angle and yields its own set of subquestions. Different perspectives → different questions → broader coverage BEFORE the search. This is *proactive* coverage: it complements the post-hoc gap-hunter (R3 from Phase 6) and does not duplicate it. Gate: shallow — skip; medium — 2–3 personas; deep — 3–5. Examples of personas: practitioner-implementer / skeptic-critic / economist (cost) / historian of the field (how it came to the current state) / adherent of the opposing school. The personas' subquestions go into Phase 3 (plan → subtopic↔blocks) and Phase 4 (search). Anti-pattern: clone personas asking the same question — if the perspectives do not yield DIFFERENT subquestions, there are fewer of them than it seems.

3.6. **Router by question profile — classify the type, it directs the decomposition.** Do not choose the splitting method «by feel» — first determine which type the question gravitates to, because the type dictates both the form of the decomposition and the priority channels. This is a heuristic, not a rigid tree: a question can mix types — then take the dominant one and mark the admixture.

   | Question type | Signal | Decomposition | Channel emphasis |
   |---|---|---|---|
   | **Factual** | «how many / when / what is X» — a point fact | Flat: 1–3 independent subquestions, in parallel. Least-to-most is NOT needed | primary + academic |
   | **Multi-step** | «how X will affect Y, **given** Z» / «what follows from A for B» — the answer of an early link is needed by a later one | **Least-to-most (F6)**: levels L1→L2 with carried context accumulating. NOT a flat parallel list | depends on the links |
   | **Relational** | «how X and Y are related», «who influences whom», networks/hierarchies/dependencies | Subquestions around *relations*, not entities; look for explicit graphs/relationship tables | code-github, industry-reports, primary |
   | **Comparative** | «X vs Y», «what to choose», «the best of N» | Subquestions = comparison axes (the same for all candidates) → C1/C7 matrix; opposition-queries for each are mandatory | competitive-signals + independent reviews |
   | **Landscape/mapping** | «map of field X», «who are the players», «how the market is structured» | Subquestions = segments/dimensions of the field; profiles M1-M12 | broad multi-channel, discovery patterns |

   Announce the chosen type in one line in the reframing («the question is multi-step → least-to-most L1→L2»). The type also hints at the **depth mode**: a purely factual one tends toward shallow, a multi-step/comparative high-stakes one toward deep. The router does NOT replace `source_dispatch.md` (Phase 4.0, matches the subtopic topic to channels) — the router chooses the *decomposition method* BEFORE the subquestions exist; dispatch spreads the already-formed subquestions across channels.

4. **Formulate stopping criteria.** What counts as a «sufficient answer». Without them the research drifts into infinity.

5. **Clarification triage — decide whether questions are needed, by criteria (not «always ask»).** This is the first step of the Plan-review gate (Phase 3.7, see `plan_gate.md`). Ask 1–3 questions ONLY if: the decision-it-supports cannot be derived; a key term is ambiguous and changes the scope; the framing is unclear (time/geo/audience/industry) and that changes the search; «compare/choose» is requested without a criterion. Otherwise — say «the scope is clear, I'm starting» and ask no questions: an extra question on an unambiguous request is friction. If the user says «I don't know» — move on with an explicit assumption: «Then I'll assume that …». Maximum 3 questions, then — an assumption.

   **The fifth criterion is mandatory and independent of the four above:** if neither the request nor the context yields a single if-then fork of the Decision Spec (item 2) — ask «What will you do differently depending on the answer?» even when the other criteria are silent. You can pass all four (the decision seems derivable, the term is unambiguous) and still not understand how the result will connect to action — that is exactly how unapplicable reports are born. This question does not count as «extra friction»: without a fork the research by definition changes nothing.

## Reframing templates

**Bad:** «Tell me about data warehouse solutions.»
**Good:** «I understand the task as: you want to compare 4–5 leading data warehouse platforms in order to choose a stack for a new analytics project. Hypotheses: (1) Snowflake's main advantage is separation of compute/storage, (2) BigQuery's is serverless and GCP integration, (3) ClickHouse's is cost at large volumes. Stopping criterion: 3 independent confirmations for each hypothesis. The decision this supports: which platform to take as the baseline.»

**Bad:** «What's up with edge computing?»
**Good:** «I understand it as: you want a map of the edge computing industry — who the players are, which use cases dominate, where the boundary with cloud lies. Hypotheses: (1) the «AI inference at edge» niche is consolidating around three vendors, (2) the IoT segment is fragmented by vertical, (3) the telecom 5G driver matters more than industrial. Decision: where it makes sense to build a product.»

## Push-back scenarios

If the user gave too general a request without an explicit decision — do NOT start the research right away. Answer like this:

> Before we dig — two questions (or three at once, if needed).
>
> 1. What decision must this research support? (If it's just curiosity — say so, I'll do a shallow one in 15 minutes.)
> 2. Is there already a hypothesis we are testing? Or do you want a map of the field without a priority?
> 3. (If applicable) What is the project context — is this for a specific project/decision, or a standalone topic?

If the user does not answer — do not get stuck in a loop. Move on with an explicit assumption and the note «the assumption was made unilaterally and may be revised».

## Anti-patterns

- ❌ Silently start googling because «it's obvious anyway».
- ❌ Ask 6+ clarifying questions and wait. The user will not fill all that in.
- ❌ Formulate hypotheses «positively» («X is good because …») — that is not a hypothesis, it is a conclusion. A hypothesis must be falsifiable.
- ❌ Not record a stopping criterion. Then the research keeps going until the model gets tired.
- ❌ Accept a vague «I'll understand better / I'll make a decision» as a Decision Spec. Without verb+object+deadline and at least one if-then fork it is not a decision but an excuse — one push-back, then an explicit assumption.
- ❌ Launch medium/deep without a single if-then fork «out of respect for the request». No fork — no application; an honest shallow is cheaper than a dead deep report.

## Phase 1 checklist

- [ ] Rewrote the question in my own words
- [ ] Assembled a Decision Spec: decision (verb+object+deadline) + consumer and their next step + ≥1 if-then fork — OR an explicit downgrade to shallow «curiosity»
- [ ] Checked applications_ledger.csv (if present) for a pattern of unapplied runs
- [ ] Formulated 2–4 falsifiable hypotheses
- [ ] (medium/deep) Generated 2–5 perspectives-personas and their subquestions for coverage
- [ ] Defined the stopping criteria
- [ ] Clarification triage: asked ≤ 3 clarifications OR explicitly decided «the scope is clear, I'm not asking»
- [ ] Assembled user context (who, why, what baseline knowledge — for section 0 of plan.md)
- [ ] Ready to move to phase 2 (genre selection — choosing the report genre)

After phase 2 — phase 3 (the plan), into which we carry everything assembled here + the genre + blocks. Everything assembled here (reframing + hypotheses + personas + stop criterion) is what **Plan-review gate (Phase 3.7, `plan_gate.md`)** will show the user before launching the search.
