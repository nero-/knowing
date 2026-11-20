---
name: knowing
description: "Evidence-disciplined web research for a decision (fork: knowing, from deepdive): a report with a source and a quote behind every fact, counter-arguments, a recommendation. Invoke: «deepdive», «do research», «investigate», «dig deep», «back it with data». NOT for: a single fact, brainstorming, an answer from the project."
---
<!-- translated from upstream/SKILL.md @ e233797 — see docs/TRANSLATION.md -->

# Deepdive — meta-research with discipline

A source = a file with verbatim quotes, the report = Q&A. Run the scripts from this skill's own directory (the folder holding `SKILL.md`), with plain `python3 scripts/X.py` under pi or `uv run scripts/X.py` if you use uv. The checks print the first 15 errors and 5 warnings; `--verbose` — only when you are fixing a specific one. N competitors by a fixed matrix — an ordinary table, not deepdive.

## Depth

By default **medium**; shallow or deep — only if the topic is explicitly trivial or the decision is high-stakes. Announce the depth with a rationale, after Genre+Plan — with one model routing line (phases by model, price, how to override: «everything on `big`» / «cheap mode»); `model_routing.md`.

**Depth is declared, derived and checked.** `plan.md` must carry four lines, and `overlay/knowing_gate.py` fails the run if they are missing, out of range, or contradict the declared depth:

```
depth: shallow | medium | deep
reversibility: reversible | irreversible
cost_of_error: low | high
answer_exists: yes | no
```

Derivation: `irreversible` **or** `cost_of_error: high` ⇒ at least `medium`. `answer_exists: yes` with the other two clean ⇒ `shallow` is allowed. Anything else ⇒ `medium`. A declared depth below what the facts imply is an error, and so is omitting a fact — the harness will not infer a depth, because the only inference it used to make was «shallow», which silently switched the breadth floors off.

| Mode | Sources | Fetcher agents | Sub-agents total per run |
|---|---|---|---|
| shallow | 5–7 | 0 | 0 |
| medium | 25–30 (out of 60–100 candidates) | 3–4 | ≈14–17 (scout, candidate pool, the small model passes, synthesizer, red team) |
| deep | 35–45 (out of ≥100 candidates) | 5–6 | ≈22–27 |

A sub-agent is not launched for what the main thread will close in a few calls or what a script computes.

## Before the start

1. Find the target folder and list its contents; a similar slug — ask «is this an update?»; read `AGENTS.md` and `memory/MEMORY.md`: do not duplicate what is already done.
2. Wiki of past runs: `uv run scripts/wiki_query.py --topic "<вопрос>"`; an unresolved contradiction goes into `plan.md` as a question. `wiki.md`.
3. Folder: the research folder from AGENTS.md or `research/`, `06_Деск-ресёрч/`, `docs/research/`; otherwise `research/` (there is a manifest), `06_Деск-ресёрч/` (documents only), `~/knowing/<slug>/` (not a git repo). The slug is latin, with hyphens. Show the path once.

## Workflow — <!--gen:count:phases-->13<!--/gen--> phases

The composition and the gates — `phases.yaml` (step 6.9 is not a gate phase: the artifact `readout.md` is checked). The details of a phase — its own file under `references/phases/`, table of contents in `workflow.md`; on entering a phase read only its file. Executor: `main` — the main thread, `sub` — a sub-agent.

1. **Reframing** [`main`] — Decision Spec: the decision, the consumer→their next step, ≥1 fork «will show X → I do A» (no fork ⇒ downgrade to shallow out loud); 2–4 falsifiable hypotheses. `question_reframing.md`
2. **Genre & blocks** [`main`] — the genre and the blocks, confirm with one line. `genres.md`, `blocks/INDEX.md`
3. **Plan** [`main`] — `plan.md` §0–16. `plan_template.md`
3.5. **Capability Discovery** [`sub: explore-`small``] (deep) — keys, API, fallback. `capability_discovery.md`
3.7. **Plan-review gate** [`main`] (shallow skips) — show the plan before the expensive Phase 4; deep waits for «Ok», because this is the only human point, and a sub-agent cannot ask. `plan_gate.md`
4. **Search** [`main` + `sub: explore-`small`` + `subagent_type: knowing-fetcher`] — channels per Source Dispatch; a candidate pool `candidates.csv` by the «sphere × stance» matrix and ≥1 academic API, selection for reading by sphere quotas, a second round by the decision variable (gate `validate_phases.py`, `phases/p4_search.md` 4.1); numbers first through registry/API; give fetchers non-overlapping id ranges and different search axes; a thin WebFetch answer (<500 characters, no quote) ⇒ `fetch_source.py`; `state.md` is overwritten before every round (≤6 KB), otherwise the context accumulates the transcript. `source_dispatch.md`, `subagents_v2.md`
5. **Claims-ledger** [`sub: explore-`small``] — `claims.csv`; status and confidence ceiling are computed by `score_claims.py --write`, not by the model (it overstates). `source_scoring.md`
5.5. **Evidence filter** [`sub: explore-`small``] (medium/deep) — relevance×authority; `unknown` — quarantine. `evidence_filter.md`
5.7. **Cross-check with the wiki** [`sub: explore-`small``] (medium/deep) — before synthesis; a conflict with past research = both positions in the report. `wiki.md`
6. **Synthesis + red team** [`sub: the synthesis subagent` + `sub: knowing-redteam`; shallow — `main`] — `outline.md` → report by sections → `numbers.csv` → hostile roles → one round of HIGH remediation → `memo.md`. The synthesizer reads the sources and the blocks, the main thread — only its summary and `memo.md`. Finder ≠ fixer. `phases/p6_synthesis.md` «Оркестрация», `adversarial_pass.md`
6.5. **Verify** [`sub: explore-`small``, effort medium] (medium/deep) — four axes → `.verify/*.json`; what gets fixed is the report, not the ledger. `runtime_verification.md`
6.9. **Human version** [`main`] (medium/deep) — `readout.md`, then a humanising pass, then `uv run scripts/build_report.py <run>`. `report_export.md`
7. **Refresh targets + swarm post-processing** [`main`] (medium/deep) — `refresh_targets.md`, then `collect_observations.py` → `update_priors.py` → `promote_candidates.py --track`; the order and the flags are in `swarm_postprocess.md`, read it before the first call.
8. **Decision walkthrough** [`main`] (always) — walk the user through the forks of `memo.md`; do not answer the forks for them. The outcome → `application.md`. `decision_walkthrough.md`

## Stop-criteria — by content, not by budget

**Stop**: the hypotheses are confirmed or refuted by ≥3 sources of different types or are marked «data is thin»; ≥1 search for the opposition has been worked through («X criticism / problems with X»); 4+ types of sources; saturation — 5 sources in a row without a new `claim_id` and a new `root:` (count by the files).
**Not stop**: the sources contradict each other (dig for the cause), all of one type, a counter-argument without analysis.
**Budget**: on medium/deep the red team (6), Verify (6.5), `readout.md` (6.9) and `finish.py` are not skipped and not merged into one agent. If a money limit is set (`--max-budget-usd`) — before Phase 4 set aside ~40% for phases 6–Finish and cut the search rounds and the number of fetchers, not the late phases; the cut is a line in `Урезано:` of the memo. N9 (2026-10-28) spent the budget on search and stopped before the red team with `Урезано: —`.
**Dead end**: the third search in a row returns sources with `total < 8` ⇒ stop, in Open Questions «the literature is weak», propose an interview or an experiment.

## Finish-up

0. **Run `python3 scripts/finish.py --research-dir <root>/<slug>`** (`--offline` without the network): it builds `sources.csv` itself, reconciles the ledger, runs liveness, writes to the wiki and runs `validate_phases.py --strict`, then `overlay/knowing_gate.py --strict` last. Red ⇒ a phase was skipped: finish it, rerun, do not report «done» until it is green. Do not run the steps one by one — skipping a flag is exactly skipping a phase.
1. To the human — one link to `<date>_<slug>.html` (desktop: `SendUserFile`), below it the PDF and the run folder; do not bring `memo.md` and the technical report into the chat.
2. A 5–8 line summary in the language of `readout.md`, without ledger codes: Answer · What would change the decision · the main counter-argument · what we did not find · the walkthrough outcome.
3. Propose 2–3 next research projects; if there is `memory/` — 1–3 candidates for memory.

## What not to do

The full statements and the run artifacts — `phases/rules.md`.
- Do not skip 5.5, 5.7, the red team (medium/deep) and Phase 8; do not start medium/deep without an if-then fork; do not write a finale of «it depends».
- Do not report a confidence higher than `score_claims.py` gives: without a primary — not higher than `medium`, an unresolved `dissent` from a strong source = `contested`, do not copy `root:`/`discovery_path:`.
- A number without a producer and `data_as_of` does not go into `memo.md`; percentages and shares — only in `numbers.csv` with `formula`: the axes of 6.5 do not check arithmetic.
- Bypass WebFetch only through `fetch_source.py`, not `curl`: it reads robots.txt and cleans the page of prompt injection.
- Do not raise fetch agents to `big` «for quality» (the confidence of error grows, not the quality); into the second round — only the holes, not the neighbours' findings.
- Do not quote >25 words verbatim from one source; a fact from memory is taken without a web check only if the chance that it has changed is <10%.
- Do not skip a humanising pass over `readout.md`, do not clean the technical report with it; do not give `memo.md` to the human instead of the page.

## Update mode

`update <slug>` / «update research X» — a delta, not a replay: `diffs/<date>_delta.md`, a new report only if the delta is substantial (the user decides), after the delta `wiki_ingest.py` and `wiki_pair.py build`. `refresh_protocol.md`

## References — read on entering a phase, not in advance

The files are named above by phase. Base ones for medium/deep: the file of the current phase from `phases/`, `question_reframing.md`, `plan_gate.md`, `genres.md` (<!--gen:count:genres-->6<!--/gen--> genres), `blocks/INDEX.md` (<!--gen:count:blocks-->106<!--/gen--> blocks), `channels.md` (<!--gen:count:channels-->29<!--/gen--> channels), `source_dispatch.md`, `model_routing.md`, `wiki.md`. By condition: `awesome_lists_registry.md` (3.5), `stat_sources/INDEX.md` and `api_sources/INDEX.md` (<!--gen:count:api-->47<!--/gen-->+ endpoints; when the subquestion is quantitative, keys — through env vars), `fetch_ladder.md` (4.2), `NOTES_dated.md` (dated facts).
