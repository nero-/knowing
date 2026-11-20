<!-- translated from upstream/references/blocks/close.md @ e233797 — see docs/TRANSLATION.md -->
# CLOSE blocks — closing the report

The blocks that finish the report: counter-arguments, open questions, next steps, sources.

---

## Z1 — `counter-arguments`

**When:** Medium/deep of all genres. Mandatory.

**What's inside:** Steel-man counter-arguments with their strength and our answer.

Source of the input data: the red team log from Phase 6 (`findings/redteam_<date>.md`). HIGH defects without a closure → Open Questions.

**Anti-pattern:** Straw-man (weak counter-arguments). It must be the strongest argument against — even if it is convincing.

**Composition:** After the main content, before closing. At least 2-3 in medium/deep.

**Template:**

```markdown
## Counter-arguments (steel-man)

### CA1: <short name of the counter-argument>
**Against what:** Q1 / F2 / TL;DR-1 / recommendation
**Who says it:** [s09](sources/09_*.md) (or «hypothetical steel-man» if there is no source)
**The argument:** <as the opponent formulates it, verbatim or close>
**Strength:** low | medium | high
**Our answer:**
- <why we still claim what we claim>
- OR <we accept it, lower confidence to medium>
- OR <this is an open question, more research is needed>
**What it changes in the conclusions:** <a concrete change or "nothing, we hold"

### CA2: <name>
...

### CA3: <name>
...

### Looking for further opposing positions
- Did we deliberately look for counter-arguments (≥1 targeted query)? <yes/no>
- If we found no strong one — that is a signal that either the topic is trivial or we looked badly
```

---

## Z2 — `open-questions`

**When:** Always. What is not closed and what to dig into next.

**What's inside:** A list of open questions with their type.

Source of the input data: the red team log from Phase 6 (`findings/redteam_<date>.md`). HIGH defects without a closure → Open Questions.

**Anti-pattern:** «Much remained unclear» with no specifics. An open Q must be actionable for the next research.

**Composition:** After `counter-arguments`. Before `next-research`.

**Template:**

```markdown
## Open questions

- **OQ1.** <a concrete question>
  - Type: «no data» | «contradictory sources» | «a different expert is needed» | «methodologically hard»
  - What would help: <a type of source or approach>

- **OQ2.** <question>
  - Type: ...
  - What would help: ...

- **OQ3.** <question>
  - Type: ...

### Known unknown unknowns
- We did not cover area N at all — it may hide relevant info
- Sources only in <language>, we may have missed <another language>
```

---

## Z3 — `next-research`

**When:** Always. What to dig into after this research.

**What's inside:** 2-3 topics for the next research runs, with a slug.

**Anti-pattern:** «There is much more to research» — every next research must be a concrete topic with a slug.

**Composition:** After `open-questions`.

**Template:**

```markdown
## Next research

- **Next 1:** <Topic>
  - Slug: `<slug-name>`
  - Why this one: <logically follows from the open questions / is the priority>
  - Genre: <the assumed one — explainer/decision/etc>

- **Next 2:** <Topic>
  - Slug: `<slug-name>`
  - Why: ...
  - Genre: ...

- **Next 3:** <Topic>
  - Slug: `<slug-name>`
  - Why: ...
```

---

## Z4 — `actionable-next-steps`

**When:** Decision, validation. When the research must turn into action.

**What's inside:** The first 3 actions after the research.

**Anti-pattern:** Vague actions («think about X»). Every one must be a concrete act with an owner and a deadline.

**Composition:** After `recommendation-conditional` in decision. After `verdict-conditional` in validation.

**Template:**

```markdown
## Actionable next steps

### Action 1 — <short name>
**What to do:** <a concrete action>
**Owner:** <who> (or «I» if solo)
**When:** <a deadline, an absolute date if possible>
**Output:** <what must appear>
**Depends on:** <preconditions if any>

### Action 2 — ...
### Action 3 — ...

### If something changes (triggers)
- If <X> happens → revisit Action 1
- If <Y> → run an update of this research
- If <Z> → re-evaluate recommendation
```

---

## Z5 — `map-of-sources`

**When:** Always. Grouping the sources by type.

**What's inside:** Sources by type with the opposition voices explicitly marked out.

**Anti-pattern:** Hiding the excluded sources (low quality). Show what was excluded and why.

**Composition:** Always. Before `metadata`.

**Template:**

```markdown
## Map of sources

- **Primary (N):** [s01](sources/01_*.md), [s07](sources/07_*.md), [s12](sources/12_*.md)
- **Academic (N):** [s02](sources/02_*.md), [s05](sources/05_*.md), [s08](sources/08_*.md)
- **Industry-media (N):** [s04](sources/04_*.md), [s10](sources/10_*.md), [s13](sources/13_*.md)
- **Expert blogs (N):** [s06](sources/06_*.md), [s14](sources/14_*.md)
- **Opposition voices (N):** [s09](sources/09_*.md), [s11](sources/11_*.md), [s15](sources/15_*.md)
- **Excluded (low quality, N):** [s24], [s25] — total < 8, not used in the conclusions

### Coverage
- Source types: N (out of 7 possible)
- A-grade quality (total ≥ 12): N
- B-grade (9-11): N
- Excluded (< 9): N

### What is missing
- <the type of source that is lacking> — why

Full list: [sources.csv](sources.csv).
```

---

## Z6 — `findings-index`

**When:** If there are large findings moved out into separate `findings/FN.md` files.

**What's inside:** Links to the findings with confidence.

**Anti-pattern:** Using it when there are no findings — skip the block.

**Composition:** After Q&A or the main content. Before `closing`.

**Template of the section in the report:**

```markdown
## Findings index

Atomic theses moved out separately for reuse in other research:

- [F1: <thesis>](findings/F1.md) — confidence: high, based on s01, s07, s12
- [F2: <thesis>](findings/F2.md) — confidence: medium
- [F3: <thesis>](findings/F3.md) — confidence: high

Each finding can be cited from other research by its ID.
```

### Template of a separate `findings/FN.md` file

Use it for theses that:
- Are more complex than one block in the main report.
- Will be reused in other research.
- Deserve a separate defence with a steel-man.

```markdown
---
id: F1
thesis: <the thesis in one sentence>
confidence: high | medium | low
sources: [s01, s07, s12, s15]
created: <YYYY-MM-DD>
status: active | superseded
---

# F1: <name of the thesis>

## Thesis

<1-2 sentences, as we formulate it>

## Supporting facts

1. **<Fact A>** — from [s01](../sources/01_*.md):
   > «verbatim quote»

2. **<Fact B>** — from [s07](../sources/07_*.md):
   > «verbatim quote»

3. **<Fact C>** — from [s12](../sources/12_*.md):
   > «verbatim quote»

## The strongest counter-argument (steel-man)

<The strongest argument AGAINST this thesis that could be found>

**Where from:** [s09](../sources/09_*.md)
**What it says:** ...
**Why we still hold the thesis:** ...
**Or: why we lower confidence:** ...

## What this means for the decision

<What changes depending on whether this thesis is right or not>

## Related theses / research runs

- F2 — supports
- F4 (from the research `<slug>`) — competes
```

---

## Z7 — `confidence-summary`

**When:** Long reports (deep) with many findings. When the reader needs a summary of confidence.

**What's inside:** A table of all claims with confidence.

**Anti-pattern:** Duplicating the confidence from the main text with no new info. Do it only if there is summary value.

**Composition:** Before `map-of-sources`.

**Template:**

```markdown
## Confidence summary

| Claim | Confidence | Why | Where in report |
|---|---|---|---|
| <claim 1> | high | 3 primary sources, replicated | Q1, F1 |
| <claim 2> | medium | 2 sources of mixed quality | Q3 |
| <claim 3> | low | single source, contested | Q5, CA2 |
| <claim 4> | high | direct primary source | F2 |

### Reading
- **High-confidence claims (N):** act on them without looking back
- **Medium (N):** take them into planning, but validate further
- **Low (N):** do not make decisions on them alone

### If you want to raise confidence medium → high
- See Open Questions OQ1, OQ3
- Or the next research <slug>
```

---

## Z8 — `assumptions-log`

**When:** Any research with explicit assumptions. Especially forecast/projection.

**What's inside:** A list of assumptions with a description of the sensitivity.

**Anti-pattern:** Hiding the assumptions. If an assumption is wrong — the verdict collapses.

**Composition:** Before `closing`. May live in `metadata` for short reports.

**Template:**

```markdown
## Assumptions

The assumptions the research is built on. If they are wrong — the verdict changes.

### A1: <assumption>
**Why I assumed it:** <reasoning>
**Evidence (if any):** [s05]
**Sensitivity:** high — if wrong, <what changes in the conclusions>
**Confidence in the assumption:** medium

### A2: <assumption>
**Why:** ...
**Sensitivity:** low — even if wrong, little changes
**Confidence:** high

### A3: <assumption>
**Why:** "found no opposing data"
**Sensitivity:** medium
**Confidence:** low — this is a weak assumption, worth testing

### If several assumptions collapse at once
- The most catastrophic combinations: A1 + A3 → <what it would be>
- Robust to: failure of A2 alone, A4 alone
```

---

## Z9 — `glossary-final`

**When:** Long reports with abundant terminology. When the reader may get lost.

**What's inside:** A final alphabetical glossary of all the terms from the report.

**Anti-pattern:** Duplicating `glossary-mini` or `glossary-full`. Use ONE type of glossary, not several.

**Composition:** Before `metadata`. Only if there was no full glossary at the beginning.

**Template:**

```markdown
## Glossary (final)

In alphabetical order. If a term was defined in the text — a short reference.

- **A** — <definition>. Introduced in Q1.
- **B** — <definition>. See mental-model.
- **C** — <definition>. From [s07].
- **D** — <definition>.
- ...
```

---

## Z10 — `update-triggers`

**When:** All research. What must happen for an update to be needed.

**What's inside:** The conditions that will make the research obsolete.

**Anti-pattern:** «When something changes» with no specifics. They must be observable triggers.

**Composition:** Before `metadata`. Helps decide when to reopen the research.

**Template:**

```markdown
## Update triggers

This research goes stale if:

- **Time-based:** after <X months>, because <area changes fast>
- **Event-based:**
  - <event 1> happens (e.g., new regulation, key player exits market)
  - <event 2>
  - A contrary RCT appears (for validation)
- **Threshold-based:**
  - If <metric X> exceeds Y
  - If >N new entrants appear in the landscape

### Watch list
- Subscribe to <feed/newsletter>
- Quarterly check on <metric>
- Notify if <key person> publishes

### What an update would look like
- Run with `update <slug>` (see update mode)
- Delta research: check only what changed
- Do not repeat the scoping and methodology — only refresh the evidence
```

## Z11 — `refresh-targets` (a separate file)

**When:** all medium/deep research. Z10 says **when** to update, Z11 says **what exactly to check** on an update. Without Z11 an update wastes a lot of time on re-discovery.

**Where it lives:** not inside the final report, but as a **separate file** `research/<slug>/refresh_targets.md`. That lets `update` mode read it straight away and go and check.

**What's inside:** a list of concrete entities, metrics, topic markers, hypotheses — everything the update will re-verify.

**Composition:** generated in Phase 7 (synthesis), after the final report is written. The template below — fill it in based on what was actually used in the M-, N-, V-blocks.

**See also:** `references/refresh_protocol.md` — how exactly `update` uses this file.

**Template `refresh_targets.md`:**

```markdown
---
slug: <slug>
generated_at: <YYYY-MM-DD>
parent_research: <YYYY-MM-DD_genre.md>
update_cadence: <"monthly" | "quarterly" | "event-driven" | "yearly">
---

# Refresh targets — <topic>

## 1. Entities to track

Companies/projects/products that the original research profiled in landscape blocks (M2, M5) or analyzed in compare blocks (C1-C5). Update will re-check these.

### <Company / Project Name>
- **Type:** <company | open-source project | research group | regulator>
- **Why in scope:** <e.g. «leader in segment X», «active competitor to focus company Y»>
- **Pages to monitor:**
  - Pricing: `<url>` (last hash: `<sha256 from sources/SN.md if available>`)
  - Careers: `<url>`
  - Blog/changelog: `<url>` (RSS if available: `<rss-url>`)
  - Crunchbase: `<crunchbase-permalink>` (if funded company)
- **Specific fields to watch:**
  - Pricing tier changes (especially «X added new tier» events)
  - CEO/CTO changes
  - Total funding raised
  - <other entity-specific>

### <Company 2>
(same template)

## 2. Numbers to refresh

Specific metrics anchored in original report's N-blocks. Update will re-fetch these and compare.

### <Metric name>
- **Source:** <FRED CPIAUCSL | World Bank SP.POP.TOTL | Statista 2026 industry report «...» | etc.>
- **API access:** <FRED API / World Bank API / manual fetch>
- **Last value:** <X.Y on YYYY-MM-DD>
- **What change matters:**
  - Direction reversal (e.g., growth → decline)
  - Magnitude > <X%> change from current
  - New methodology revision (Statista often revises previous-year estimates)
- **Anchored in:** <which blocks/claims in the report depend on this number>

### <Metric 2>
(same template)

## 3. Topic markers (for discovering NEW things)

Patterns that update will use to find new entrants, new publications, new datasets.

### GitHub topics
- `topic:<keyword-1>` — for finding new repos in domain
- `topic:<keyword-2>`
- Filter: `stars:>50 created:>last_research_date` (adapt the date on update)

### Academic concepts
- **OpenAlex concept ID:** `<C-XXXXXXX>` («<concept name>»)
- **Semantic Scholar paper IDs to cite-trace:** `<S2-paper-id>` («<paper title>»)
- **arXiv categories:** `<cs.LG, q-fin.TR, etc>`

### News keywords
- Primary: `<keyword combination>`
- Opposition / failure mode keywords: `<«X doesn't work», «X bankruptcy», etc>`

### Industry-specific
- Newsletter/feed: `<URL>` (manual check or RSS)
- Conference proceedings: `<conference name>` (annual; check post-event for new papers)

## 4. Hypotheses to re-test

Original report's H1-H4 (from plan.md section 9). Update will search for new opposing evidence to each.

### H1: «<verbatim hypothesis>»
- **Status at last research:** <supported | contradicted | inconclusive> (confidence: <H/M/L>)
- **Supporting sources (count):** <N> sources of types <Academic, Industry-media, ...>
- **Watch for:**
  - Replication failures: `«<H1 phrase> failed replication»`, `«<H1 phrase> doesn't generalize»`
  - Retractions: search RetractionWatch for cited papers
  - Counter-RCTs / new datasets that test the same claim

### H2: «<verbatim hypothesis>»
(same template)

## 5. Sources requiring re-verification (high-stakes only)

If specific sources are critical to the report's conclusions, they get extra re-check on update.

### sources/SN_<critical-source>.md
- **Why critical:** <«primary source for H1», «only source on regulatory status», etc.>
- **Re-check action:**
  - Verify URL still accessible (not 404)
  - If author/venue: check if retracted
  - If gov data: check for revised version
  - If company page: refetch and diff
```

**Anti-patterns:**

- ❌ Filling in Z11 «from memory» — every field must reference a block from the final report where it was used
- ❌ Listing «all possible sources» — this is refresh_targets, not a bibliographic database. Critical path only
- ❌ No update_cadence — the user will not understand when to come back
- ❌ No saved hash/snapshot for the entity pages — fingerprinting does not work

---

## Z12 — `so-what-for-you`

**When:** Medium/deep, mandatory. A projection of the report's key conclusions onto the user's concrete case — not an abstract «here is what we learned about the world».

**Input:** `plan.md` section 0 (Decision Spec: the decision / consumer→step / if-then forks + User context) + `claims.csv` (the key theses with their confidence).

**What's inside:** For each key conclusion — what it means specifically for the user's situation, a concrete action, the trade-off of that action, and the kill-criteria (what must happen for the recommendation to stop being true).

**Mapping to the Decision Spec (mandatory):** every key claim is tied to the fork/criterion of the decision that it affects. The output of the mapping is the **applicability ratio** = mapped claims / all key claims; the number goes into the frontmatter of `application.md` (Phase 8) and into the eval rubric as a descriptive metric. Claims that affect no fork are listed on a separate line with the honest question «why is it in the report?» — they are candidates for being cut from scope in the next research run on the topic. A low ratio is exactly the measured «uselessness of the language»: the report says a lot, affects the decision little.

**Anti-pattern:** Repeating the TL;DR in other words. Z12 must add what is not in the TL;DR — personalisation to the concrete case from `plan.md` section 0, not a retelling of facts. The second anti-pattern: mapping all claims onto the forks formally («relates to the decision as a whole») — the mapping is honest only where there is a direct influence on the choice of branch.

**Composition:** After `map-of-sources` [Z5] / `confidence-summary` [Z7], **before** `actionable-next-steps` [Z4] — first «what this means for you», then «what exactly to do».

**Template:**

```markdown
## So what for you

Context of use (from plan.md §0): <who is asking, why, how they will use it>

### Conclusion 1: <the key thesis from claims.csv, confidence: high/medium/low>
**Decision Spec fork:** <«if X → A» / — affects none (flag: why is it in the report?)>
**What this means for your situation:** <a concrete projection, not an abstraction>
**Recommended action:** <what to do given this>
**Trade-off:** <what you lose by choosing this action>
**Kill-criteria:** <what must happen for this recommendation to stop being true>

### Conclusion 2: <thesis, confidence>
**What this means:** ...
**Action:** ...
**Trade-off:** ...
**Kill-criteria:** ...

### Conclusion 3: ...
```
