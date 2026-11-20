# Changelog

## 0.1.0 — 2026-11-19

Fork of deepdive @ e233797 (2026-11-17), MIT. Renamed to **knowing**, translated to English at the
floor, patched in seven places, and given the four checks the base documented but did not enforce.

### Added
- `overlay/knowing_gate.py` — four checks (`anchor`, `depth`, `read_scope`, `adjudication`), each
  with an exit code, each re-reading the artefact rather than trusting a self-report.
- `overlay/apply_patches.py` — seven idempotent patches with anchor assertions, so an upstream move
  fails loudly instead of applying nothing.
- `overlay/tests/test_gate.py` — 21 tests; the negative cases are the point (a gate that cannot fail
  is a comment).
- `docs/DECISIONS.md` — decision record with the audit results, corrections, and what a quote hash
  does and does not prove.
- `docs/TRANSLATION.md` — glossary-as-contract plus the coupling rule (prose, pattern and test move
  together).

### Changed (patched in place, each marked `knowing`)
1. `validate_phases.py` — `CLAIMS_OPTIONAL` gains `anchor`, `quote_sha256`.
2. `validate_phases.py` — `MODE_RE` accepts `depth:` (canonical); `mode:` stays as a legacy alias.
3. `validate_phases.py` — a missing depth declaration is an error, not an inference to shallow.
4. `build_sources_csv.py` — `read_scope` column.
5. `finish.py` — citation liveness runs with `--strict` (it could not fail before).
6. `finish.py` — the `knowing` step joins the finish chain, in-process, after `validate_phases`.
7. `eval/check_quotes.py` — returns non-zero when quotes are missing or mis-attributed.

### Fixed upstream defects found while adopting
- The plan template wrote `depth:`, the validator read `mode:` — a `depth: deep` plan validated as
  shallow and skipped `MIN_READ`, `MIN_CANDIDATES`, `TYPE_QUOTAS` and `MIN_CONTRADICTING`.
- `.verify/faithfulness.json` was described as blocking finish; only its shape is checked, and
  `runner/orchestrator.py:385` records "faithfulness not implemented".
- `check_quotes.py` returned 0 on every path.

### Notes from the test pass
- `eval/check_quotes.py` and upstream's `tests/` disagreed about source ids (`s01` vs `01_x`); the anchor
  pattern is format-agnostic and validates the id against the claim row's own `sources` column instead.
- Read-scope errors now attach to *use*: an unscoped source nobody cites is a warning, an unscoped
  source a claim leans on is an error. Discovered by running our gate over upstream's synthetic run.
- `finish.py` runs the knowing step **without** `--strict`: errors block, warnings inform. CI can
  escalate with `knowing_gate.py --strict`.
- `runner/priors.py` accepts both `### Часть X` and `### Part X`; two `tests/test_docs_swarm.py`
  assertions were updated to the translated canonical strings.

### Known gaps (v0.1)
- English translation covers the floor only; backlog in `docs/TRANSLATION.md`.
- "No method critique below `full_text`" not implemented (needs reliable prose detection).
- `references/model_routing.md` still names Claude Code agent types; see D6.

## 0.2.0 — 2026-11-20

### Added
- `overlay/tier_routing.py` + `docs/TIERS.md` — map upstream's `strong/mid/cheap` vocabulary onto
  separate endpoints (config: `KNOWING_TIERS`, `KNOWING_TIERS_FILE`, or per-tier env vars), with a
  `strong → mid → cheap` fallback that records which tier answered. `--provider tiers`.
- `overlay/tests/test_tier_routing.py` — 16 tests: config precedence, fallback, one client per
  endpoint, unknown-tier rejection, and that a missing variable is named rather than defaulted.
- Bilingual gate literals: the source-card heading (`## Разбор` / `## Source dissection`), the verdict
  table (`Гипотеза|Вердикт` / `Hypothesis|Verdict`), the unmeasured-default patterns and the
  appendix-laundering patterns now accept English. Bilingual beats a migration.
- `build_readout.py` accepts English section names while still emitting Russian; its output is an
  artefact, not a gate, so this is the soft landing.

### Translation — the load profile is complete
Every file a run loads at any depth is now English: the floor (16 files) plus the medium/deep profile
(p6_synthesis, p6_9_export, p7_refresh, subagents_v2, adversarial_pass, source_scoring, both INDEX
files, capability_discovery, awesome_lists_registry, synthesis_outline) — ~26k words translated in
this release. Backlog remaining is 40 files / ~37k words, all outside the load profiles (report
blocks, leaf data cards, export/refresh docs, code messages).
Two cross-file heading references were repaired (`«Оркестрация»`, «Эвристика подбора блоков»), and
`tests/test_docs_swarm.py` accepts the English "not used" note as well as the Russian one.

## 0.2.1 — 2026-11-20

### Changed — tiers are pools, not machines
- A tier now holds **one or more candidates**. Transient failures (connection error, timeout,
  408/409/425/429/5xx, `RateLimit`/`Timeout`/`Overloaded` classes) cool an endpoint down — 30 s
  doubling to 300 s, cleared on success — and the call fails over to the next candidate. A 400 or an
  auth error is **not** retried elsewhere: that would hide a bug behind a second failure.
- Rotation policy is per tier: `rr` (per call, for fan-out) or `sticky` (per process, for planning and
  synthesis, where switching models loses the prompt cache). `TierMapProvider.routed` records every
  attempt and every tier downgrade.

### Added — endpoints are declared once
- `overlay/config.py`: `[providers.*]` tables (`base_url`, `kind = openai|anthropic`, credentials,
  `models`) referenced from `[tiers.*]` as `provider/model`. TOML or JSON; the earlier single-object
  and bare-list shapes still load.
- Credentials resolve lazily from `api_key`, `api_key_env`, or `api_key_cmd` (the `!command` convention
  pi's `models.json` already uses). A missing variable is an error naming it.
- `python3 overlay/config.py check [--probe]` — shows tiers, whether keys resolve, and with `--probe`
  GETs `<base_url>/models` to flag a model the server does not actually serve.
- `python3 overlay/config.py from-pi ~/.pi/agent/models.json` — emits a starting config from pi's
  provider list.
- 18 config tests (dialects, credential sources, ref resolution, probe against a local HTTP server,
  CLI exit codes); 57 overlay tests total.

## 0.3.0 — 2026-11-20

### Removed — the tier vocabulary
`strong` / `mid` / `cheap` is gone from the config surface. It was upstream's internal vocabulary and
the first version of this fork exposed it as something you had to fill in. The config now defines
**model names**, which is what `phases.yaml` already uses.

### Added — three resolvers, in priority order
1. **the agent**: pass `model: "opus"` and it is honoured;
2. **the phase**: `[phases."6"] model = "opus"` pins a `phases.yaml` id;
3. **`default`**: used when neither says anything.

An unknown name is an error listing the configured names — never a silent fallback, because a typo
must not quietly reroute a synthesis step.

### Renamed
- `overlay/tier_routing.py` → `overlay/model_map.py` (`ModelMap`); `--provider models` ( `tiers` still
  accepted as a legacy alias).
- `docs/TIERS.md` → `docs/MODELS.md`.
- Config section `[models.*]` ( `[tiers.*]` still loads); top-level `default` and `[phases.*]` added.
- `~/.config/knowing/models.toml` is the default path (`tiers.toml` still discovered).

Pools, failover, cooldown and the audit trail are unchanged. 59 overlay tests.

### Fixed
- A `default = "..."` written after a `[models.*]` header (TOML files it inside that table) is now
  recovered rather than silently ignored, with a note saying where it belongs; two of them is an error.
