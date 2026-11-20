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

### Known gaps (v0.1)
- English translation covers the floor only; backlog in `docs/TRANSLATION.md`.
- "No method critique below `full_text`" not implemented (needs reliable prose detection).
- `references/model_routing.md` still names Claude Code agent types; see D6.
