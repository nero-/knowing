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

## Start here

`docs/USAGE.md` — install, configure models, run a first research question, and read the gates. The
short version: `apply_patches.py` once, `overlay/config.py check --probe` to verify endpoints, then ask
your agent for the research and let `scripts/finish.py` tell you whether it holds up.

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
.venv/bin/python -m pytest overlay/tests -q      # 59 tests, ours
.venv/bin/python -m pytest tests -q             # upstream's suite
```

**Test status (honest):** upstream's suite is 40 failed / 670 passed at the pinned commit, before any
of our edits. After them it is 40 failed / 670 passed — the same failures, none new, and 59 of our own
tests pass. The 40 are upstream's: `tests/test_providers.py` needs the `anthropic` SDK, and
`tests/test_report_export.py` asserts Russian error strings from `build_report.py`, which v0.1 does not
translate. Two upstream tests were updated by us because the behaviour they asserted is the behaviour we
deliberately changed (`resolve_mode` no longer infers a depth; `finish` now ends with the knowing step).

## Any model, any endpoint — and the agent can choose

No tiers, no policy list. A **model name** is whatever you want to call it, pointing at one or more
interchangeable endpoints. `phases.yaml` already names a model per phase; that is the routing table.
This answers "where does that name live", with failover behind it.

```toml
# ~/.config/knowing/models.toml
[providers.sparks]
base_url = "http://100.120.4.113:8015/v1"

[providers.tp2]                        # second local box
base_url = "http://100.97.112.71:8000/v1"

[models.big]
endpoints = ["sparks/DeepSeek-V4.1-Flash"]
rotate = "sticky"                      # one model per process: prompt cache survives
fallback = ["small"]

[models.small]
endpoints = ["tp2/Qwen3.8-Flash-Next", "sparks/DeepSeek-V4.1-Flash"]

default = "small"                      # when neither the agent nor the phase names one

[phases."6"]                           # optional: pin a phases.yaml id
model = "big"
```

Resolution order: **the agent's explicit name → the phase pin → `default` → an error listing the names
you do have.** A typo cannot quietly reroute a synthesis step. Endpoints behind a name are pooled:
a transient failure (connection error, timeout, 429/5xx) cools that endpoint down and fails over; a 400
is *not* retried elsewhere. Every routing decision lands in `ModelMap.routed`.

```bash
python3 overlay/config.py check --probe       # models, keys, and what each server really serves
python3 overlay/config.py from-pi ~/.pi/agent/models.json > ~/.config/knowing/models.toml
```

Local endpoints only: anything speaking OpenAI's `/v1` — vLLM, llama.cpp, Ollama, LM Studio, TGI.
Guide, pools, failover and the reasoning: `docs/MODELS.md`.

## Status

- **Translation complete**: every prose file under `references/`, plus `SKILL.md` and `QUICKSTART.md`,
  is English. Russian originals stay in `vendor/deepdive/` for diffing. The one deliberate exception is
  documented in `docs/TRANSLATION.md` (an enum token the registry generator emits).
- The base's own `docs/`, `eval/`, `tests/` are kept upstream-faithful. `eval/` and `tests/` are not
  installed into the skill directory; they are for development only.
- Local-only: no cloud endpoints, no vendor SDK requirement, no other harness's directories. State lives
  in `~/.knowing/`, config in `~/.config/knowing/models.toml`, and two agent definitions ship in
  `agents/` (`knowing-fetcher`, `knowing-redteam`).

## Provenance and licence

MIT. Derived from deepdive, Copyright (c) 2026 ivanterescheenko-ai, at commit `e233797`
(2026-11-17); see `NOTICE` and `LICENSE`. Upstream's prose was translated; upstream's code was
patched at seven points, each marked `knowing`/`knowing-patch` in the source so a rebase conflict is
readable rather than mysterious.

The audit that produced these changes — what the base claims, what it actually enforces, and which
of its documented guarantees were prose — is in `docs/DECISIONS.md`.
