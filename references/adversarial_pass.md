<!-- translated from upstream/references/adversarial_pass.md @ e233797 — see docs/TRANSLATION.md -->
# Adversarial pass — multi-angle red team (Phase 6)

## Contents

- 0. Scope (fixed honestly)
- 1. Orchestration
- 2. Roles
- 3. Severity triage (structural verdicts, NOT 1–5 scores)
- 4. Ties to the rest of the skill

Replaces a single self-critique. Principle: critique is more reliable than voting and
works inside one model family, because it is the ROLE that varies, not the weights
(multi-agent debate; devil's advocate against sycophancy). We do NOT use 1–5
scores — LLM judges have length/position/self-preference bias.

## 0. Scope (fixed honestly)

All roles are one model family, shared blind spots remain.
- CATCHES: overclaim (the source does not prove the thesis), theses with <3 independent
  sources, coverage holes, an ignored counter-hypothesis, selection bias,
  fitting to the user, numbers without a comparison anchor, conclusions without a projection onto
  the user's case (Z12), recommendations without trade-off/kill-criteria.
- DOES NOT CATCH: general factual hallucinations (correlated). Those are held by
  triangulation (Phase 5) and optional cross-vendor 6.5.
→ the red team SUPPLEMENTS triangulation, does not replace it.

## 1. Orchestration

1. Draft: the synthesis model writes `<date>_<genre>.md`.
2. Claim ledger: write out the key falsifiable theses + their references to sources/NN.md.
3. Launch IN PARALLEL (in one message), one sub-agent per role:
   - subagent_type = deepdive-redteam (read-only, Opus, effort high; a judgement task,
     not a search task — finder ≠ fixer: makes no edits to files).
   - input: path to the draft + sources/ folder + role prompt + output schema.
   - the roles do NOT see each other (independent context).
   - model: `deepdive-redteam` (Opus, high) for medium and deep; shallow — R1 inline on `main`.
4. Triage: merge defects, dedup, severity (section 3). Log `findings/redteam_<date>.md`, one line per finding: `HIGH-1 <role>: <defect>`, `MED-2 …`, `LOW-3 …`. Then a snapshot of the draft: `cp <date>_<genre>.md findings/draft_pre_remediation.md`.
5. Remediation — ONE round (a cap against an endless loop):
   - HIGH → an edit of the body section where the wrong thesis stands, and of all places where it is repeated (TL;DR/`Answer`, verdict table, confidence), — via a targeted extra search (Phase 4 on these subquestions only) or an explicit caveat in the section itself.
   - MED → into counter-arguments / caveats.
   - LOW → optional.
   There is NO recursive re-teaming of the edits; the closing of a HIGH is visible from the diff of the report.
   **A postscript «amendments below take priority over the text» is forbidden.** N4 and N6 (2026-10-28) appended the remediation to the end and left the TL;DR and the verdicts old: the report contradicted its own audit, the reader of the first page received a refuted claim.
6. Finder ≠ fixer: the synthesis model (chairman) fixes, not the same role.
7. Output: the section `## Adversarial review` in the report — a register only, without new statements: `- HIGH-1 → §<section heading>[, §<more>]: what was changed` or `- HIGH-2 → Open Questions: why not closed`. `validate_phases.py` checks each HIGH from the log against this register and checks that the named section differs from `findings/draft_pre_remediation.md`.

## 2. Roles

Gate: shallow = only R1 inline (without a sub-agent); medium = R1+R2+R4+R5 (R5 — if `claims.csv` has at least one row with `dissent` ≠ `-` or status `contested`); deep = R1+R2+R3+R4+R5 mandatory.

R1 — Skeptic / fact-checker:
  «A hostile reviewer. For each key thesis find: (a) support by <3
  independent sources of different types; (b) overclaim; (c) numbers/dates/names without
  a reference to sources/NN.md; (d) differences derived from a SINGLE run
  of one's own measurement and presented as established («X is 60 times more expensive than Y»), without
  a confidence interval or an explicit «single run» mark; (e) if one's own measurement
  entered the conclusions — read the CODE of the experiment, not only its
  result: the figure may be an artifact of the harness itself (a constant inside
  the block being measured, a detector tuned to its own fixtures). Lines:
  thesis → defect → severity → how to close. Do not praise.»

R2 — Advocate of the opposite hypothesis:
  «Build the strongest case AGAINST the main conclusion. What would refute it? Did we
  look for that? Which alternative explains the facts no worse? Finish with CONCRETE
  opposition queries — they go into stop-criteria.»

R3 — Gap hunter + anti-sycophancy:
  «What is missing but relevant to the decision? Check: (a) fitting to the user's
  expectations; (b) selection bias (all sources of one type/camp);
  (c) uncovered stakeholders/scenarios/costs/risks; (d) whether there are numbers without
  a comparison anchor (a bare "$4.5B" without a base), conclusions without a projection onto the user's
  case (block Z12 so-what-for-you empty or formal), recommendations
  without trade-off/kill-criteria.»

R4 — Executor (a test for applicability, not for the text):
  «You are the consumer from the Decision Spec (plan.md §0: who reads and what they do
  afterwards). EXECUTE the decision using ONLY the report and memo.md: go through
  every if-then fork and try to make a choice. Every place where you got stuck — a finding:
  the needed number is missing; there is no recommendation; a recommendation without conditions of
  applicability; the fork is unresolvable from the collected data. Plus a hedge lint on memo.md and the TL;DR:
  every occurrence of hedging formulations («may help», «worth considering»,
  «in some cases», «potentially», «depends on circumstances» without
  resolved conditions) — a finding: either make it concrete (direction + magnitude
  + condition + date), or honestly into Open Questions. Do not judge style — judge whether
  the consumer's next step can be DONE from this document.»
  Difference from R3(d): R3 looks for gaps in the text; R4 simulates execution — it goes from
  the Decision Spec forks, not from the report, so it catches non-executability that
  reading does not show.

R5 — Advocate of the minority (mandatory for deep, recommended for medium):
  «You defend a lone source against the consensus. Read `claims.csv` and take
  every row where `dissent` ≠ `-`, plus every source whose position did NOT enter
  the report. For each: (a) build the strongest version of the minority position; (b) name
  what must be true for it, and not the majority, to be right; (c) check whether the
  majority reduces to one root or one discovery path — then it is not a
  majority but one voice in three copies; (d) separately check numerical theses:
  whose source is closer to the producer of the number (`origin_kind`, `chain_len`), rather than to its
  retelling. Your directive: **the group's consensus is not an argument**, and your
  private information may be decisive. Do not soften: if after the check
  the minority is right — say outright that the report's conclusion has to change.»
  Why a separate role. R1 (Skeptic) is tuned against credulity — it demands MORE
  confirmation. But there are two epistemic failures, and they are opposite: the first punishes
  excessive credulity, the second requires believing a lone voice against the majority
  (Anthropic Frontier Red Team, 13.08.2026: the «hidden profile» task is not saturated
  even by top models — the discussion converges on what everyone already knows). One
  skepticism regulator fixes one and breaks the other; R1 and R5 are two regulators with
  opposite settings, and they cannot be combined in one agent.

## 3. Severity triage (structural verdicts, NOT 1–5 scores)

| Severity | Criterion | Action |
|---|---|---|
| HIGH | a load-bearing thesis with <3 sources; OR an overclaim; OR a strong unrebutted counter-finding | blocks the final → 1 round of extra search or an explicit caveat |
| MED  | a secondary thesis with weak support; selection bias; an uncovered cost/stakeholder | into counter-arguments / caveats |
| LOW  | wording, a weak hedge, a minor hole | optional |

## 4. Ties to the rest of the skill

- stop-criteria: R2's opposition queries = fulfilment of «≥1 targeted search for the opposition».
- blocks/close.md: defects → counter-arguments + Open Questions (a HIGH without closure → Open Questions «data insufficient»); numbers-without-anchor/empty-Z12/recommendations-without-trade-off from R3(d) → edits of blocks F9/Z12 or of the corresponding N/A blocks of the synthesis, not a separate section.
- plan.md risk register: unresolved HIGHs.
- refresh_targets.md: R2's counter-hypotheses → hypotheses-to-track.
- claims.csv: HIGH defects about overclaim/<3 sources overlap with status ≠ triangulated — the red team may highlight a row that the gap wave (Phase 5) did not close.
- R5 findings: a confirmed minority position → the `claims.csv` row is moved to `contested`, both positions go into the report with an explicit basis for the choice (see the dissent rule in `source_scoring.md`). If R5 showed that the majority reduces to one root or one discovery path, — that is HIGH: the status was issued erroneously, recompute the triangulation rather than appending a caveat. **Fixing the ledger to suit the report is forbidden, and in the other direction too:** lowering the `credibility` of a dissenting source so that the dissent rule does not fire is fitting.
- R4 findings: a Decision Spec fork unresolvable from the data → HIGH (targeted extra search or an explicit blocked); hedge language in memo/TL;DR → MED (make concrete or into Open Questions). Phase 8 (`decision_walkthrough.md`) inherits unclosed R4 findings as candidates for `blocked` — the walkthrough must not «discover» them anew.
