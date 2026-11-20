<!-- translated from upstream/references/phases/p6_synthesis.md @ e233797 — see docs/TRANSLATION.md -->
## Phase 6. Synthesis + multi-angle red team

### Orchestration (the main thread reads only this section)

Medium/deep: the synthesis runs in the `deepdive-synthesizer` sub-agent, so that sources, `evidence/` and `blocks/*.md` do not settle in the main thread's window. Shallow: the main thread performs the «Order» below itself.

1. `deepdive-synthesizer`, mode `draft`; brief: run path, depth, date. The main thread does not open `sources/`, `evidence/` and `blocks/` itself.
2. Run the verification command from the synthesizer's answer. Red ⇒ another `draft` with the error text in the brief.
3. Red team per `adversarial_pass.md`: roles — `deepdive-redteam` with the path to the draft. Findings are triaged by the main thread, which writes the log `findings/redteam_<date>.md` (lines `HIGH-1 …`, `MED-2 …`), then a snapshot `cp <date>_<genre>.md findings/draft_pre_remediation.md`.
4. `deepdive-synthesizer`, mode `remediate`, with the path to the log: one remediation of HIGH in the body of the report (not as a postscript) and `memo.md`. The verification command again: it checks each HIGH against the changed section.
5. Of the Phase 6 artifacts the main thread reads only `memo.md`: it is needed for 6.9 and Phase 8.

Steps 1–5 and 7 of the «Order» below are an instruction to the synthesizer, step 6 — to the main thread.

**Input from 5.7:** `same-claim-conflict` verdicts are a divergence from a PREVIOUS research, and it must reach the report: both positions with their `as_of` and roots, `confidence` no higher than `medium`, without an arbiter — `contested`. The mechanics are the same as for `dissent` in Phase 5, only the opposing side lies in the wiki, not in this run. A triggered cut by `MAX_ADJUDICATED` — as a line in the memo's `Урезано:`. See `wiki.md`.

**Model:** red-team sub-agents — `opus` / `high` **(mandatory for deep)**, `sonnet` / `high` for medium. Synthesis assembly — `sub: deepdive-synthesizer` (`opus` / `high`, its own context). Do not economise on the red team — this is where Haiku/Sonnet do soft pushback without a real attack on the hypotheses.

**Order:**
1. Re-read ALL `sources/NN.md` with `used: Y`. Do not synthesise from memory. For **deep**: the `findings/` layer is mandatory — the synthesis goes from `findings/` + `claims.csv`, with `sources/NN.md` spot-checked only at contested places. For shallow/medium — as before, re-read the used sources in full.
2. Re-read `plan.md` (genre, blocks, hypotheses, section 0 User context) and `claims.csv` (status/confidence of each thesis).
3. Load the needed category files `blocks/*.md` (only those needed for the chosen blocks). Progressively — not all at once.
4. For each hypothesis — gather supporting/refuting quotes. Optionally move the large ones out into `findings/FN.md` (see `blocks/close.md` block Z6).
4.5. **Fix `outline.md`** (medium/deep) — the table `| section | block | claims |` from `plan.md` §8/§11 plus the actual `claims.csv`, that is, from what was really found. It is also the index for targeted retrieval at step 5 and the input of three machine checks (`validate_phases.py`: a section without a claim, a non-existent `claim_id`, **a `triangulated`/`contested` claim outside the report** = synthesis gap). Template and rules — `synthesis_outline.md`.
5. Assemble the draft `<date>_<genre>.md` **section by section per `outline.md`**: under each section pull in only its `claim_id` from `claims.csv` and its `evidence/CN.md`, not the whole pool (citation precision drops where there is the most context — the same principle by which 5.5 does not hand the synthesis irrelevant quotes, but at the level of a section). Each block — per the template from its category file. Three cross-cutting synthesis rules (apply to all blocks, not only the TL;DR):
   - **Numbers with a comparison anchor.** A key number without a comparison base is forbidden: «Market $4.5B» — not enough. «Market $4.5B — three times smaller than the neighbouring segment X, growing three times faster than the industry average» — good enough. Anchor: vs base / vs neighbour / vs dynamics over time.
   - **Conditions of applicability.** Every conclusion — with an explicit «when it holds, when it does not», not a bare statement.
   - **A single run is not a difference.** A number from one run of one's own measurement is not reported as an established difference («60 times more expensive») without a confidence interval or an explicit «single run, no CI» mark. One's own measurement that entered the conclusions carries `caveat: self-reported` (confidence ceiling — `medium`, see `source_scoring.md`), and all its files — one shared `root` (one measurement = one voice, not three).
   - **Confidence from claims.csv.** Each TL;DR item (F1) carries its own `confidence` (high/medium/low), taken from the corresponding `claims.csv` row — not invented by eye during synthesis.
   - **Verdict table by hypotheses** (medium/deep, gate `validate_phases.py`): in the report the table `| Hypothesis | Verdict | Support |`, one row per H from `plan.md`; verdict — supported | refuted | partial | data insufficient.
   - **Anti-bias: no measurement — no default.** If a variable the choice depends on (price at our volume, latency, headcount) is not measured by a single source, there is no `by default` recommendation: only conditional forks + the cheapest way to learn the variable. Each option is described in its strongest form, the way its proponent would describe it. Gate: `by default` in the `Answer` or in the `Recommendation` line without `[sNN]` in the same sentence — a `validate_phases.py` error. Benchmark 2026-10-28: 6 of 6 runs advised «Fivetran by default» without a single price figure — this is the model's prior opinion, not a conclusion.
   - **Ban on the «it depends» ending.** Research ending with «depends on circumstances» is useless by definition. If an unambiguous recommendation is impossible — a conditional one is mandatory, mapped to Decision Spec forks: «priority — cost → X; speed → Y». «It depends» without resolved conditions = an unmet acceptance criterion, not an ending.
   - Block Z12 `so-what-for-you` (see `blocks/close.md`) is assembled at this same step from `plan.md` section 0 (Decision Spec + User context) + `claims.csv` — key claims are mapped to the decision forks, the applicability ratio is computed; projection of the conclusions onto the user's case, up to `actionable-next-steps`.
6. **Multi-angle red team** (see `adversarial_pass.md`) — draft → claim ledger (an internal list of falsifiable theses for the red team, not to be confused with the `claims.csv` file) → N hostile roles (Skeptic/Contrarian/Gap-hunter/Executor) as `general-purpose` sub-agents → severity triage → ONE round of HIGH remediation → final. Depth gate: shallow=R1 inline, medium=R1+R2+R4, deep=R1+R2+R3+R4. Defects → counter-arguments (`Z1`) + Open Questions; log in `findings/redteam_<date>.md`. Do not mask disagreement. The 5th adversarial question (see `adversarial_pass.md`): are there numbers without a comparison anchor, conclusions without a Z12 projection, recommendations without trade-off/kill-criteria?
7. **Assemble `memo.md` — a one-page decision memorandum.** What enters the consumer's process is not a 40-page report but one page; the report is the evidence base underneath it. Composition: recommendation (unambiguous or conditional by forks), resolution of the Decision Spec if-then forks, 3 key numbers with [sNN] and `as_of`, the main risk, next actions, the **«what we cut» line**.

   **The «what we cut» line — mandatory if the run narrowed itself.** Research has two legal ways to quietly reduce the task: a downgrade to shallow (not a single if-then fork) and the no-progress circuit breaker (2 rounds with no new information). Both are correct — and both must be loud, otherwise the user gets a lighter version of their question without knowing it. Format — one line:

   ```
   Урезано: circuit breaker на раунде 3 (Q4 «стоимость перехода» без данных) · режим остался medium.
   ```

   Nothing was cut — write exactly that, `Урезано: —`. A metric that can be improved by stopping doing the work is not a metric: the share of `triangulated` grows if hard claims are dumped into Open Questions, so it is read only paired with coverage, and the narrowing is announced out loud.

   Numbers in the memo obey the fail-closed provenance rule: a number with `origin_kind: unknown`, `chain_len ≥ 2` or without `data_as_of` does not get in here (see `source_scoring.md` «Provenance of a number»); `check_number_provenance.py` checks this by machine. It is written AFTER the red team (HIGH remediation already accounted for). Always mandatory; in shallow — tiny (5–10 lines). A Phase 6 artifact, checked by the phase-gate.
8. If the system has `anthropic-skills:humanizer-ru` — run the final report through it.
9. Save the final report.
