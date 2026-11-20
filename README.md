# knowing

Evidence-disciplined research for coding agents, forked from [deepdive](https://github.com/Socialpranker/deepdive).

`knowing` runs a 13-phase research pipeline (reframe → genre → plan → search → claims → synthesis →
verify → refresh → walkthrough) with machine-checked gates. It is a fork: the pipeline, the validator,
the breadth floors and the report blocks come from upstream. What this fork adds is the small set of
checks upstream *documented* but did not implement, plus the fixes that make the existing gates
actually fire.

## What this fork adds

| addition | why it exists | where |
|---|---|---|
| **Quote anchors** — every claim row names `source_id:line` plus a hash of the quoted span | the base checked that a quote exists in *some* card; nothing let you re-find it | `overlay/knowing_gate.py::check_anchor` |
| **Depth derivation** — `depth:` is read (it wasn't), and a run's depth must match the facts it declares | upstream's plan template wrote `depth:` while the validator read `mode:`, so a `depth: deep` plan validated as *shallow* and skipped every breadth floor | `check_depth`, `overlay/apply_patches.py` |
| **Read-scope enforcement** — `abstract_only` cannot carry a triangulated claim | the base had paywall states, not read depth | `check_read_scope` |
| **Adjudication verdict** — `VERDICT: PASS / REVISE / BLOCK` + `DECLINED TO JUDGE`, and a BLOCK cannot ship | the base had severity tiers, no run-level verdict | `check_adjudication` |
| **Teeth** — citation liveness runs with `--strict`, `check_quotes.py` exits non-zero on a synthetic quote, and all of the above join `finish.py` in-process | upstream's checks were runnable but could not fail a run | `overlay/apply_patches.py`, 7 patches |

Not added, deliberately: dependency-injection, a query language, a plugin system. This is a research
harness, not a framework.

## Install

```bash
git clone https://github.com/<you>/knowing
ln -s "$PWD/knowing" ~/.agents/skills/knowing      # pi
# or copy the tree into your skills directory
python3 overlay/apply_patches.py                   # idempotent; fails loudly if upstream moved
```

`overlay/apply_patches.py` must be run once after a clone or a rebase. It **refuses to apply
blindly**: every patch asserts its anchor line is present, so an upstream change surfaces as a
failure rather than a silent no-op.

Run the local checks:

```bash
python3 -m venv .venv && .venv/bin/pip install pytest pyyaml requests
.venv/bin/python -m pytest overlay/tests -q      # 37 tests, ours
.venv/bin/python -m pytest tests -q             # upstream's suite
```

**Test status (honest):** upstream's suite is 40 failed / 670 passed at the pinned commit, before any
of our edits. After them it is 40 failed / 670 passed — the same failures, none new, and 37 of our own
tests pass. The 40 are upstream's: `tests/test_providers.py` needs the `anthropic` SDK, and
`tests/test_report_export.py` asserts Russian error strings from `build_report.py`, which v0.1 does not
translate. Two upstream tests were updated by us because the behaviour they asserted is the behaviour we
deliberately changed (`resolve_mode` no longer infers a depth; `finish` now ends with the knowing step).

## Different models on different boxes

`--provider tiers` maps upstream's tier vocabulary onto your own endpoints, so the expensive phases
(planning, synthesis, adjudication) can run on a large-context box while the fan-out runs somewhere
cheaper. Configure with `KNOWING_TIERS` (JSON), `KNOWING_TIERS_FILE`, or per-tier env vars; a
half-configured setup falls back down `strong → mid → cheap` and reports which tier answered.
Full guide, worked example and the two things that should drive the mapping: `docs/TIERS.md`.

## Status

- v0.1: English translation covers the **floor** — the files a run loads unconditionally
  (`context_budget.py::ALWAYS_LOAD`) plus `plan_template.md`. `docs/TRANSLATION.md` lists the
  backlog in load order. Russian originals live in `vendor/deepdive/` so any translation can be
  diffed against its source.
- The base's own `docs/`, `eval/`, `tests/` are kept upstream-faithful. `eval/` and `tests/` are not
  installed into the skill directory; they are for development only.
- Known open item: `references/model_routing.md` names Claude Code agent types
  (`deepdive-fetcher`, `deepdive-redteam`, `deepdive-synthesizer`). On pi these map to Agent types;
  the mapping is recorded in `docs/DECISIONS.md` (D6) and not yet rewritten in prose.

## Provenance and licence

MIT. Derived from deepdive, Copyright (c) 2026 ivanterescheenko-ai, at commit `e233797`
(2026-11-17); see `NOTICE` and `LICENSE`. Upstream's prose was translated; upstream's code was
patched at seven points, each marked `knowing`/`knowing-patch` in the source so a rebase conflict is
readable rather than mysterious.

The audit that produced these changes — what the base claims, what it actually enforces, and which
of its documented guarantees were prose — is in `docs/DECISIONS.md`.
