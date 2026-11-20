<!-- translated from upstream/references/phases/p7_refresh.md @ e233797 — see docs/TRANSLATION.md -->
## Phase 7. Refresh targets generation (medium/deep — mandatory)

**Model:** `sonnet` / `medium`. A mechanical pass over the final report with extraction of entities, numbers, hypotheses.

**Why:** this file is the **entry point for future `update <slug>`**. Without it every update wastes time re-discovering «what to track in this topic at all».

**Steps:**
1. Read the final `<date>_<genre>.md` + `plan.md`.
2. Extract **entities** from blocks M2 (profile-cards), M5 (white-spaces), C1-C5 (compare matrices): concrete companies/projects with URLs.
3. Extract **numbers** from blocks N1-N8: concrete FRED series IDs, World Bank indicators, industry estimate refs.
4. Extract **topic markers** from the plan: GitHub topics from awesome_lists_registry discovery, OpenAlex concept IDs.
5. Extract **hypotheses H1-H4** from plan.md with the final status from A4 (hypotheses-outcome).
6. Write into `<root>/<slug>/refresh_targets.md` per the **Z11** template from `blocks/close.md`.

**Refresh candidates — an additional source:**

- **Carry-forward deviations.** Read `deviations.md` for `not_pursued` records with a
  `carry_forward` field; each is a first-class refresh-target candidate (an angle the
  search loop identified but could not pursue within budget/depth).

**Output:** the file `refresh_targets.md` next to `plan.md`. Used in subsequent `update <slug>` — see `refresh_protocol.md`.

**Anti-patterns:** see block Z11 in `blocks/close.md`.
