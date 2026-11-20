<!-- translated from upstream/references/synthesis_outline.md @ e233797 — see docs/TRANSLATION.md -->
# Synthesis outline — Phase 6, steps 4.5–5

Read at Phase 6 (medium/deep). Answers two questions: what to write section by section and
how not to lose what was gathered on the way into the report.

## Why a separate artifact if there is a plan

`plan.md` §8/§11 fixes the blocks and the subtopic mapping **before** the search. By Phase 6
something else is known: what was actually found, what got triangulated, what stayed `contested`.
A synthesis going straight from the plan writes a report about what was intended; a synthesis going from
`claims.csv` — about what was found. `outline.md` is the plan brought into correspondence with the
ledger, and at the same time a machine-readable map by which each section is written.

Revising the structure along the way of the search is a legitimate operation (`phases/p4_search.md`, «Dynamic
outline revision», Phase 4, expensive-class budget). Here the result of this
revision is **fixed** in a checkable form.

## Format

```markdown
# Outline — <slug>
mode: medium

| section | block | claims |
|---|---|---|
| TL;DR | F1 | CL1; CL4; CL7 |
| Как это устроено | E3 | CL2; CL3 |
| Сравнение подходов | C1 | CL5; CL6 |
| Контраргументы | Z1 | CL8 |
| Открытые вопросы | Z2 | — |
```

- One row = one section of the report. The order of rows = the order of sections.
- `block` — the block id from `blocks/` (F1, E3, C1, Z1…), so that the template is taken from the
  category file and not invented.
- `claims` — `claim_id` separated by `;`. An empty cell (`—`) is allowed only for sections
  that by definition carry no claim: Z2 Open Questions, Z3 next research.
  Any substantive section without a `claim_id` is prose with no ledger behind it.

## Three machine checks (`validate_phases.py`)

| Check | What it catches |
|---|---|
| a section has ≥1 `claim_id` | a paragraph written «from oneself», without a row in the ledger |
| the `claim_id` exists in `claims.csv` | a reference to a claim that was renamed or never created |
| every `triangulated`/`contested` claim is mapped | **synthesis gap** — found, confirmed, not brought into the report |

The third is the only one that catches the loss of *work* rather than a recording error: the
class «retrieval worked, organisation failed». On deep it is a blocker, on medium —
a loud warning (a medium run may legally carry part of what was found into Open
Questions, but is obliged to do it explicitly, not silently).

A claim deliberately left out of the report is closed in one of two ways:
by a row in Z2 Open Questions (and then it is mapped to the section Z2) or by lowering the
status in the ledger, if it actually did not survive the check. Silent disappearance
is not an option.

## Writing by sections, not by the pool

Step 1 of Phase 6 re-reads all `used: Y` sources — that stays: without the overall picture
one cannot choose the structure. But to **write** a section holding the whole pool in
context means writing it on the weakest attention: the more text in the window, the lower
the citation precision, and quotes are what the whole skill is answerable for.

The order per section:

1. Take its `claim_id` from `outline.md`.
2. Pull in ONLY those `claims.csv` rows and the corresponding `evidence/CN.md`
   (relevant-only quotes, already filtered by Phase 5.5).
3. Write the section per the template of its block.
4. Move on to the next one. Not «collect everything and then lay it out».

This is the same principle as in 5.5 (not handing the irrelevant to the synthesis), applied at
the level of a section. `sources/NN.md` is opened pointwise — at a contested place, not as the
main input: that is what `evidence/` exists for.

## Anti-patterns

- ❌ An outline rewritten from `plan.md` §8 without checking against `claims.csv` — then it is not an
  index but a copy of the plan, and the synthesis gap is not visible.
- ❌ A «Misc»/«Other» section with a list of orphan claims: that is not placement, that is
  a dump. Either a claim carries a section, or it goes to Z2 with a reason.
- ❌ One `claim_id` in all sections in a row: a sign that the claim is too general —
  split it in the ledger, do not smear it across the report.
- ❌ Writing by sections but pulling the whole `evidence/` under each one — then the attention
  saving does not arrive, yet the check passes.
- ❌ Appending a claim to the outline after the section is written, so that the gate becomes
  green. The gate checks the correspondence of the map and the ledger; fitting the map to already
  written text is exactly what it protects against.
