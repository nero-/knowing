<!-- translated from upstream/references/phases/p8_walkthrough.md @ e233797 — see docs/TRANSLATION.md -->
## Phase 8. Decision walkthrough (mandatory always, including shallow)

**Model:** the main thread, `opus` / `high` — the quality of the questions is critical, as in Phase 1.

The report is not «discussed», it is executed: the agent shows `memo.md` and leads
the user through the if-then forks of the Decision Spec one at a time — «the research showed X [s03][s11]
— does fork A fire? your decision?». Outcomes per fork: **accepted** (decision + next
action with a date) / **blocked by data** (one targeted gap wave, max 1 round →
retry, if it did not close — honestly `blocked`) / **deferred** (`deferred`, no
pressure). The full mechanics, the `application.md` template, the global ledger and the anti-patterns
— `references/decision_walkthrough.md`.

**Output:** `<slug>/application.md` (any status — the gate requires the file, not an accepted
decision) + a row in `~/.claude/research/applications_ledger.csv`.

## Checklist after Phase 8

- [ ] **Acceptance criteria from plan.md (section 4) ALL met** — every check-box has evidence (a file, a script output)
- [ ] All `sources/NN.md` have correct frontmatter (scoring, channel, access filled in)
- [ ] `sources.csv` updated, total recalculated
- [ ] `claims.csv` filled in — every row has a status; rows that are not triangulated went through the gap wave (see Phase 5, max 2 rounds) and are honestly marked `data-insufficient` if they did not close
- [ ] Not a single statement with `confidence: high` violates the primary-first rule (without a primary source confidence ≤ medium)
- [ ] `plan.md` has `status: completed`
- [ ] `plan.md` section 15 (notes) finalised — all important observations documented
- [ ] `<date>_<genre>.md` assembled from all the blocks from `plan.md` → `blocks:`
- [ ] All required blocks for the genre are present (see `genres.md`)
- [ ] Every statement has a reference to a specific [sNN] or is marked `[без подтверждения]`
- [ ] Channels coverage ≥3 different types (see plan.md section 14)
- [ ] Multi-angle red team done (roles by the depth gate), Z1 counter-arguments recorded, the log `findings/redteam_<date>.md` created
- [ ] Hypotheses outcome table filled in — all H1-H4 have a status
- [ ] Risk register from plan.md (section 10) checked — the risks that materialised are marked, did the mitigation work?
- [ ] Open questions listed (Z2)
- [ ] Next research suggestions — 2–3 items (Z3)
- [ ] If update mode: changelog (plan.md section 16) finalised
- [ ] If there is `memory/` — memory candidates proposed
- [ ] **`refresh_targets.md` generated** (Phase 7, for medium/deep) — entities/numbers/hypotheses/topic markers filled in per the Z11 template
- [ ] **`memo.md` assembled** (Phase 6, always) — a recommendation without «it depends», the forks, 3 numbers with [sNN]+as_of, the risk, next actions
- [ ] **Decision walkthrough held** (Phase 8, always) — forks resolved (accepted/blocked/deferred), `application.md` written with status and applicability_ratio
- [ ] A row added to `~/.claude/research/applications_ledger.csv`
- [ ] Files saved, the path shown to the user as a markdown link
