<!-- translated from upstream/references/phases/p3_plan.md @ e233797 — see docs/TRANSLATION.md -->
## Phase 3. Plan

**Model:** `opus` / `medium`. An architectural decision, it documents all future choices.

Write to the file `<root>/<slug>/plan.md`. The plan is a document, not a conversation. If it is in the chat — it will be lost later.

**Structure of plan.md** — 5 sections: HEADER → SCOPE → STRUCTURE → EXECUTION → TRACKING.

**plan.md template** (frontmatter + all sections 0–16, verbatim) — `references/plan_template.md`. Read it on entering Phase 3, not earlier.

**Notes on using the template:**

1. **Frontmatter critical** — machine-readable. Do not abbreviate the fields.
2. **User context (section 0)** — fill it in BEFORE the reframing or right after. Without it the rest hangs in the air.
3. **Acceptance criteria (section 4)** — the most important. If you cannot formulate what counts as done — do not start the research.
4. **Subtopics ↔ blocks mapping (section 11)** — without it the agents assemble blind.
5. **Notes during research (section 15)** — update it as you go, not at the end. This is the documentation of decisions.
6. **Update changelog (section 16)** — fill in ONLY for update.

**Minimal plan.md** (if shallow and the topic is small) — sections may be omitted:
- 0 (if obvious)
- 5 (if there is no existing)
- 10 (if there are no obvious risks)
- 11 (if one subtopic)
- 16 (if initial)

But **mandatory:** 2, 3, 4, 7, 8, 9, 12, 13, 14.
