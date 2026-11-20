<!-- translated from upstream/references/decision_walkthrough.md @ e233797 — see docs/TRANSLATION.md -->
# Decision Walkthrough — Phase 8

## Contents

- Mechanics
- The artifact `<slug>/application.md`
- The global ledger — `~/.knowing/research/applications_ledger.csv`
- Anti-patterns
- Phase 8 checklist

The final phase: the report is not «discussed», it is **executed right now**. Applicability
is not surveyed — it is tested by doing: the agent walks the user through the if-then forks
of the Decision Spec (Phase 1, `plan.md` §0), and either a decision gets made or it becomes
visible what is missing. This is the answer to the main failure of research: a methodologically clean
report that led nowhere, because no one tried to apply it.

**Mandatory at ALL depths** (`depth_gate: shallow`). Shallow is a truncated version:
one fork, 2 minutes. Model: the main thread, high effort — the quality of the questions here is as
critical as in reframing; this is a dialogue with the user, not a background task.

## Mechanics

Input: `memo.md` (Phase 6), `plan.md` §0 (Decision Spec), `claims.csv`, the final report.

1. **Open the memo.** Show the user the recommendation and the forks in one message — they
   answer the grilling while looking at the summary, not flipping through 40 pages.
2. **Walk the forks one at a time** (one branch at a time, until resolved):
   > Fork 1: «if the research shows X → I do A». The research showed: <conclusion in one
   > line> [s03][s11], confidence high. Does the fork fire? Your decision?
   Wait for an answer before the next fork. Not in a batch.
3. **Three outcomes per fork:**
   - **Decision made** → record the choice + a concrete next action with a date.
   - **Blocked by data** («I can't decide because I don't know Z») → this is a
     concrete gap: one targeted gap wave (Phase 5 mechanics, the subagent on the hole,
     **max 1 round**) → another pass at the fork. The report gets fixed, not mourned.
     Not closed — an honest `blocked: <what is missing>` in application.md.
   - **«I don't know / later»** → `deferred`, no pressing. This is diagnostics, not a failure
     of the phase: if the user does not know what they took it for, that is a signal that the Phase 1 Decision Spec
     was formal. Offer once: narrow the question and prove it again, or
     explicitly admit the run was «curiosity». Record the answer, then do not press.
4. **Interrogation of relevance** (1–2 questions after the forks, no more):
   - «If the report did not exist — what would you be doing instead?» (the «was there any point» test)
   - (if there are open questions / a risk register) «Which of the unresolved items blocks
     application right now?»
5. **Write `application.md`** (template below) and add a line to the global ledger.

## The artifact `<slug>/application.md`

```markdown
---
status: applied | partial | deferred | unused
date: 2026-XX-XX
applicability_ratio: 0.72        # claims mapped to forks / all key claims (from Z12)
---

# Application — <slug>

## Decision Spec (snapshot from plan.md §0)
Decision: <...>  Consumer → step: <...>
Forks: if <X> → <A>; if <Y> → <B>

## Verdict per fork
| Fork | Research showed | User's decision | Next action + date |
|---|---|---|---|
| X→A | X confirmed [s03][s11] | accepted: A | <action, deadline> |
| Y→B | data is thin (the gap wave did not close it) | blocked: <what is missing> | — |

## If the report had not existed
<the user's answer verbatim — this is value calibration, not rhetoric>

## Unused claims
<claims from Z12 not mapped to any fork — candidates for removal from the scope
of the next research on this topic>
```

`status`: `applied` — ≥1 fork resolved into a decision; `partial` — some resolved, some
blocked; `deferred` — the user postponed; `unused` — it is honestly recorded that
there is no application. **The gate (validate_phases.py) requires the file to exist with any
status** — not an accepted decision: autonomous runs are not blocked on a human,
and a walkthrough without a user writes `deferred` with pre-drafted forks.

## The global ledger — `~/.knowing/research/applications_ledger.csv`

```csv
slug, date, decision_spec, status, applicability_ratio
payments-provider-iskra, 2026-07-26, Y, applied, 0.83
edge-computing-map, 2026-07-20, N, unused, 0.20
```

One line per run, appended after application.md is written. Read by Phase 1
of the next research: ≥2 `unused`/`deferred` in a row → show the user the pattern
(«the last N researches led to no decision — how does this one differ?»). Chronic
failure of applicability is cured only compoundingly, between runs.

## Anti-patterns

- ❌ Dumping all the questions in a batch. One fork at a time, wait for the answer.
- ❌ Pressing a user who honestly said «I don't know». One pass offering to
  narrow it — after that `deferred` and full stop.
- ❌ Answering the forks FOR the user («I think you would choose A»). The point of the phase is
  that a human speaks the application out loud; an application thought up by the agent is the same
  dead report, only with an extra section.
- ❌ Skipping the phase «because it's obvious anyway». Obvious means the walkthrough will take two
  minutes and confirm it in writing in application.md.
- ❌ More than one gap wave per fork. One not closed after the round — `blocked`, honestly.
- ❌ Forgetting the ledger. Without a line in the ledger the next run will not see the pattern.

## Phase 8 checklist

- [ ] memo.md shown to the user before the questions
- [ ] Every Decision Spec fork resolved: accepted / blocked (after ≤1 gap wave) / deferred
- [ ] The «if the report had not existed» question asked (except in truncated shallow — optional there)
- [ ] `application.md` written with status and applicability_ratio
- [ ] A line added to `~/.knowing/research/applications_ledger.csv`
