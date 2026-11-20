<!-- translated from upstream/references/workflow.md @ e233797 — see docs/TRANSLATION.md -->
# Workflow — details of the <!--gen:count:phases-->13<!--/gen--> phases

A supplement to SKILL.md. The details of each phase live in a separate file under `phases/`: on entering a phase read only its file. Do not read the whole set at once: in a single window it costs ~60 KB and by Phase 6 it pushes the current round out of the context.

| Phase | File | Who reads |
|---|---|---|
| 1. Reframing | `phases/p1_reframing.md` | main thread |
| 2. Genre & block selection | `phases/p2_genre.md` | main thread |
| 3. Plan | `phases/p3_plan.md` | main thread |
| 3.5. Capability Discovery | `phases/p3_5_capability.md` | sub-agent (deep) |
| 3.7. Plan-review gate | `plan_gate.md` | main thread |
| 4. Search: dispatch, rounds, candidates and quotas, `state.md`, circuit breaker | `phases/p4_search.md` | main thread |
| 5. Claims-ledger, triangulation, gap wave | `phases/p5_claims.md` | main thread + sub-agent |
| 6. Synthesis + multi-angle red team | `phases/p6_synthesis.md` | `deepdive-synthesizer`; main thread — only the `### Orchestration` section |
| 6.9. Report export | `phases/p6_9_export.md` | main thread |
| 7. Refresh targets | `phases/p7_refresh.md` | main thread |
| 8. Decision walkthrough + checklist after Phase 8 | `phases/p8_walkthrough.md` | main thread |
| Run exit and the full statements of the rules | `phases/rules.md` | on entering Phases 4, 5 and 6 |

A reference of the form «see Phase 5» inside a phase file points to the file from this table.
