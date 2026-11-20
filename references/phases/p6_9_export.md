<!-- translated from upstream/references/phases/p6_9_export.md @ e233797 — see docs/TRANSLATION.md -->
## Phase 6.9. Report export

**Executor:** `main`, without a sub-agent. Mechanical assembly, no substantive decisions.

```bash
uv run scripts/build_report.py <run>
```

Assembles `<date>_<genre>.md` into HTML, PDF and DOCX from a single source. In full —
`references/report_export.md`. Here — what the phase must leave behind and what it fails on.

**Leaves:** `<date>_<genre>.html`, `.pdf`, `.docx` in the run folder; SVGs of figures in `.build/`.

**Fails on:**
- a `[sNN]` link that is not in `sources.csv` — a broken link on 20 pages is not found by eye;
- a figure referring to a `num_id` outside `numbers.csv` — a chart has no right to assert more than the ledger;
- a mismatch «N footnotes, M carried over» — a silently lost footnote is indistinguishable from its absence.

`--no-strict` lifts the first two refusals, but not the third.

**Register — 15–20 pages for one decision.** `memo.md` stays a separate page:
one page that will definitely be read does not dissolve into twenty.
