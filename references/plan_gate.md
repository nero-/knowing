<!-- translated from upstream/references/plan_gate.md @ e233797 — see docs/TRANSLATION.md -->
# Plan-review Gate — Phase 3.7

## Contents

- When it fires — hardness by mode
- Step 1 — Clarification triage (inherited from Phase 1)
- Step 1.5 — Scout pass (medium — optional, deep — recommended)
- Step 2 — Plan-review block (what to show)
- Step 3 — Handling the answer
- Anti-patterns
- Phase 3.7 checklist

The only human-in-the-loop checkpoint before the expensive Phase 4 (Search). Show the user a condensed plan and let them approve or correct it — BEFORE tokens are spent on sub-agents.

**Why.** Correcting the plan before execution is the cheapest quality lever. At Gemini Deep Research the review/edit of the plan is called «biggest lever over output quality»; open_deep_research (`allow_clarification`), OpenAI (two-step clarifier→research) and dzhng/deepdive do the same thing before the start. Bad research is almost always a correctly executed wrong plan. The gate catches a «the model understood it wrong» divergence in seconds, not in 30 minutes and the whole budget.

**Also — enforcement.** The gate naturally checks that Phases 1–3 were actually gone through: if there is nothing to show (no hypotheses, no genre, no channels) — then the phase was skipped. Do not assemble the block out of empty fields — go back and finish the phase.

## When it fires — hardness by mode

| Mode | Gate behaviour |
|---|---|
| **shallow** | **Skip.** Low-stakes, the topic is familiar — do not slow down. At most one line «doing shallow on X, hypothesis Y» and straight into the search. |
| **medium** | **Soft.** Show the plan block, ask for a one-line confirmation, but do not block hard: if the user does not object — continue. Do not wait indefinitely. |
| **deep** | **Hard. Show the plan block and WAIT for an explicit «Ok» (or corrections).** Do not launch Phase 4 sub-agents until the user has answered. High-stakes/expensive — the price of a wrong plan is maximal, the price of a pause is negligible. |

The mode is set in Phase 1 (shallow/medium/deep). The gate inherits it and does not ask separately.

## Step 1 — Clarification triage (inherited from Phase 1)

Clarification is NOT «always ask questions». It is a decision *whether they are needed*, by explicit criteria. The triage is done in Phase 1 (see `question_reframing.md`), the gate only checks that it took place.

**Ask 1–3 clarifying questions ONLY if at least one of these holds:**
- The decision the research supports cannot be derived (what changes depending on the answer is unclear).
- A key term is ambiguous and changes the whole scope («agent» = AI agent or legal agent? «rust» = the language or corrosion?).
- The frame is unclear: time horizon, geography, audience, industry — and this radically changes the search.
- The user asks to «compare/choose» but gave no selection criterion.
- **Not a single if-then fork of the Decision Spec can be derived** («it shows X → I do A») — this criterion is mandatory and independent of the others: ask «what would you do differently depending on the answer?» (see `question_reframing.md` item 2, item 5).

**Do NOT ask questions (say «scope is clear, I am starting») if:**
- The decision and the frame are derivable from the request or the project context (AGENTS.md, memory).
- The question is concrete and unambiguous.
- You have already asked 3 questions — from here move on with an explicit assumption.

Wording when questions are not needed (following open_deep_research's verification message):
> Scope is clear: [one line on what I understood]. No clarifications needed — moving on to the plan.

Wording when they are needed (≤3, from `question_reframing.md` push-back):
> Before I dig in — [1–3 questions]. If you do not answer — I will move on with the assumption «…».

## Step 1.5 — Scout pass (medium — optional, deep — recommended)

**Why.** Phase 4 is partitioning: the agents search exactly where the plan pointed them. Everything that is not in the plan will not be found at all. The Anthropic Frontier Red Team measurement on vulnerability discovery (13.08.2026) showed the price of this: a swarm with a shared forum found 266 findings against 21 for partitioned agents with an overlap of only 12 — **about half of the swarm's findings fell outside the directories the independent agents were pointed at**. This is not «the swarm is better», these are different coverages: partitioning searches by instruction, the swarm decides for itself where to dig.

The scout pass buys the second coverage cheaply — before the plan is fixed.

**How.** 3–4 `deepdive-scout` sub-agents (the small model, web search: WebSearch/WebFetch, writes no source files), launched in ONE message, a short budget.

The scout's task is **not sources but questions**:

```
Research topic: <main question>.
Our plan currently covers the subtopics: <list from plan.md §11>.

TASK: in 5-7 quick searches find what this list is MISSING.
Return ONLY JSON:
{
  "missing_subquestions": [{"question": "<subquestion>", "why": "<why it changes the conclusion>", "signal": "<what prompted it: source/term/dispute>"}],
  "wrong_framing": "<if the question is worded so that it leads away from the point — say so; otherwise null>",
  "unexpected_channels": ["<channel/community/registry that is not in the plan>"]
}
Do NOT save files. Do NOT gather sources. We are looking for holes in the plan, not material.
```

**Output** — edits in `plan.md` (sections 11 and 12) and a line in the plan block below: «the scout found N uncovered subquestions, added K». Zero records in `sources/`.

**Anti-patterns:**
- ❌ Giving the scout `general-purpose` and allowing it to write `sources/NN.md` — that is already Phase 4 out of turn, the id numbers have not been handed out yet.
- ❌ Dragging the scout's findings into claims — the scout confirms nothing, it raises questions.
- ❌ Running the scout on shallow — 5-7 sources do not pay for a separate phase.

## Step 2 — Plan-review block (what to show)

One compact block. Do not retell the whole `plan.md` — only what the user can really correct and what determines the outcome. Format:

```
📋 Research plan — <slug>  [<mode>]

Question (as understood): <one reframing line>

Decision Spec:
  Decision: <verb + object + deadline>
  Consumer → next step: <who reads it and what they do afterwards>
  Forks: if <X> → <A>; if <Y> → <B>

Genre: <qa/explainer/decision/landscape/validation/custom — the shape for the consumer's process>, blocks: <2–4 key ones>

Hypotheses:
  H1: <falsifiable>
  H2: <falsifiable>
  H3: <falsifiable>   (2–4 of them)

Persona perspectives (medium/deep): <practitioner / sceptic / economist …>

Search channels: <3–6 primary channels from source_dispatch: web / arXiv / GitHub / FRED …>
Stop criterion: <when I consider the answer sufficient>

Routing: <phases×models, estimated cost> — see model_routing
```

Then — an explicit fork question (text by mode):
- **deep:** `Ok like this? Or correct something — hypotheses / scope / channels / depth? (waiting for an answer before searching)`
- **medium:** `If it is ok — I go searching. Something to correct — say it now.`

Plus always offer the routing override labels: `«everything on `big`» / «cheap mode» / «default»`.

## Step 3 — Handling the answer

- **«Ok» / silence (medium)** → Phase 4.
- **Correction of scope/question** → go back to Phase 1, rewrite the reframing + hypotheses, rewrite `plan.md`, show the block again (for deep — wait again).
- **Correction of hypotheses** → update the hypotheses section in `plan.md` without running all of Phase 1.
- **Correction of channels/depth** → update section 12 (sourcing strategy) and/or the mode; if the mode changed — recompute whether the gate is skipped.
- **Override routing** («everything on `big`» / «cheap») → apply to model_routing, reflect in plan.md, continue.

After approval — record in `plan.md` section 16 (changelog): `plan approved by the user <date>` (or `corrections: <what>`). This records that the gate actually fired.

## Anti-patterns

- ❌ Showing the gate and immediately, without waiting for an answer, launching Phase 4 sub-agents (for deep). A gate without waiting = not a gate.
- ❌ Dumping the whole `plan.md` (5 sections, risk register, glossary). The user will not read it — show only the fork points.
- ❌ Asking clarification questions when the scope is obvious. An extra question on an unambiguous request is friction, not value.
- ❌ Blocking on shallow. Low-stakes research must not wait for confirmation.
- ❌ Assembling the plan block out of empty fields (no hypotheses / no channels) and showing it as is. An empty field = an unfinished phase, go back and finish it.

## Phase 3.7 checklist

- [ ] Mode determined (inherited from Phase 1) → shallow skips the gate
- [ ] Clarification triage took place (questions asked OR «scope is clear» explicitly stated)
- [ ] Decision Spec filled (decision+deadline / consumer→step / ≥1 fork) OR a downgrade to shallow «curiosity» recorded
- [ ] Compact plan-review block assembled (question / Decision Spec / genre / hypotheses / channels / stop / routing)
- [ ] Fork shown by mode (deep — wait; medium — soft)
- [ ] (deep) Waited for an explicit answer before launching Phase 4
- [ ] Approval/corrections reflected in plan.md section 16
