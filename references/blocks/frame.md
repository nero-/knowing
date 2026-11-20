<!-- translated from upstream/references/blocks/frame.md @ e233797 — see docs/TRANSLATION.md -->
# FRAME blocks — the frame of the report

Frame blocks: TL;DR, scope, claim, metadata. This is the structural skeleton of any report.

---

## F1 — `tldr`

**When:** Always. The first block of the report.

**What's inside:** 2-4 lines of the main thing. Each with a confidence marker.

**Anti-pattern:** «water», abstract formulations. The TL;DR must be actionable — what was learned, what changes.

**Composition:** Written LAST, after all the other blocks. First you think it through, then you compress.

**Template:**

```markdown
## TL;DR

- **<Main answer 1 in one phrase>** [confidence: high]
- **<Main answer 2>** [confidence: medium] — <why it was lowered>
- **<Main answer 3>** [confidence: low] — <caveat>
```

---

## F2 — `decision-context`

**When:** Decision, custom-decision. Explains the frame of the decision.

**What's inside:** What we are deciding, the options, the constraints, the stakes level.

**Anti-pattern:** A vague «we need to choose a system» with no criteria. It must be precise: what we optimise and within which frame.

**Composition:** Goes right after `tldr` in the decision genre. Before `options-matrix`.

**Template:**

```markdown
## Decision context

- **What we are deciding:** <the decision in one line>
- **Options:** A, B, C (or "map mode: research with no choice")
- **We optimise by priority:** 1. <criterion>, 2. <criterion>, 3. <criterion>
- **Constraints:** <budget / time / team skills / legacy>
- **Stakes:** low | medium | high
- **When the decision is needed:** <deadline or "when ready">
```

---

## F3 — `scope`

**When:** Landscape, validation, any research with explicit boundaries.

**What's inside:** What is in scope, what is NOT in scope, the cut as of a date (important for landscape — it goes stale).

**Anti-pattern:** Skipping scope in a landscape — you get complaints «and why didn't you mention X».

**Composition:** After `tldr` or right under the title. Before the main content.

**Template:**

```markdown
## Scope

- **What is in scope:** <inclusion criteria>
- **What is NOT in scope:** <explicit exclusions and why>
- **Cut as of date:** <YYYY-MM-DD>
- **Geography:** <countries/regions or "globally">
- **Period (for historical):** <from/to>
```

---

## F4 — `claim-precise`

**When:** Validation. A precise formulation of the claim under test.

**What's inside:** The full claim, the scope of applicability, explicit exclusions.

**Anti-pattern:** A vague claim («X is useful») — there is nothing to check. It must be falsifiable.

**Composition:** Right after `tldr` in validation. Before `falsification-criteria`.

**Template:**

```markdown
## The claim

- **Precise formulation:** <the claim as a statement, not a question>
- **Scope of applicability:** <where, when, in which context>
- **What is NOT claimed:** <explicit exclusions, so that it is not substituted>
- **Source of the claim:** <where we heard it> (if any)
```

---

## F5 — `metadata`

**When:** Always. The footer of the report.

**What's inside:** Author, date, depth, blocks, version, status.

**Anti-pattern:** Duplicating the frontmatter in the metadata. The footer is for the reader, the frontmatter is for machine processing.

**Composition:** The very last block of the report.

**Template:**

```markdown
---

## Metadata

- **Date:** <YYYY-MM-DD>
- **Depth:** <shallow | medium | deep>
- **Genre:** <qa | explainer | decision | landscape | validation | custom>
- **Blocks used:** <N>
- **Sources:** <N> (used in the conclusions: <K>)
- **Time:** ~<X hours>
- **Version:** initial | update-1 | update-2
- **Status:** active | superseded by `<YYYY-MM-DD>_<genre>.md`
- **Plan:** [plan.md](plan.md)
- **Sources:** [sources.csv](sources.csv)
```

---

## F6 — `key-finding-callout`

**When:** Long reports (medium/deep), when there is ONE insight significantly more important than the rest.

**What's inside:** A highlighted quote-conclusion with sources and confidence.

**Anti-pattern:** Using it as a replacement for the TL;DR. It is an addition, not a substitute.

**Composition:** After `tldr`, as an accent on the main insight.

**Template:**

```markdown
## 🎯 Key finding

> **<The main insight in one or two phrases>**
>
> Sources: [s03], [s07], [s12]
> Confidence: high
> What it means: <a short consequence>
```

---

## F7 — `executive-summary`

**When:** Decision/landscape for stakeholders, non-technical readers. A 1-page report-inside-the-report.

**What's inside:** A plain-English version of the report on 1 page.

**Anti-pattern:** Duplicating the TL;DR. The executive summary has a separate reader, its own depth.

**Composition:** After `tldr`, before the main content. Optional, not for every report.

**Template:**

```markdown
## Executive Summary

**Context:** <2-3 sentences on what we researched and why>

**Main conclusions:**
1. ...
2. ...
3. ...

**Recommendation:** <if applicable, one phrase>

**Risks:** <the 2-3 main ones>

**What next:** <the first action>
```

---

## F8 — `glossary-link`

**When:** The project has a shared glossary (for example, `docs/glossary.md` or `UBIQUITOUS_LANGUAGE.md`).

**What's inside:** A link to the external glossary instead of an inline one.

**Anti-pattern:** Duplicating the glossary in the report when it already exists in the project — it drifts over time.

**Composition:** A replacement for `glossary-mini` or `glossary-full` if an external glossary exists.

**Template:**

```markdown
## Glossary

The terminology of this report matches the project glossary: [<filename>.md](../<path>).

Additional terms introduced ONLY in this research:
- **<Term 1>** — <definition>
- **<Term 2>** — <definition>
```

---

## F9 — `background`

**When:** The default for medium/deep in all genres. Answers «why the question is posed the way it is» — before we start dissecting the content.

**What's inside:** Prehistory and causes — what came before this question, where it came from, which events/decisions made it relevant right now. 5-10 lines, no more — this is context, not a research within a research.

**Anti-pattern:** Retelling Wikipedia about the topic in full. Background must explain exactly WHY the question is posed this way, not give the general history of the subject.

**Composition:** After `scope` [F3] (if there is a scope) or right after `tldr` [F1]. Before the main content of the report.

**Template:**

```markdown
## Background

<5-10 lines: what preceded this question — an event, a trend, a decision, a change
in conditions — because of which the question became relevant right now. Name the
sources of the premise explicitly, if there are any: [s03].>

**Why this matters for the answer:** <a short link — how this prehistory affects
the way the rest of the report must be read>
```

## F10 — `verification-header`

**When:** medium/deep — mandatory, set by Phase 6.5. In shallow — only the liveness line (Layers 2–4 were not run). Without it the report is not «ready»: the header is itself the statement of how far it can be trusted.

**What's inside:** A blockquote at the very top of the report, before `tldr` [F1]. Four axes on one line — liveness × faithfulness × qualifiers × constructs — plus a second line on source independence for medium/deep. The chain «source → claim → report» breaks at any link, so the axes do not substitute for one another and are shown together.

All numbers are taken from `.verify/*.json` and `claims.csv` and are **never recounted by hand**. How they are produced and what a bad value on each means — `references/runtime_verification.md`.

**Anti-pattern:** Showing the header as a score («9/10, good»). Every number is a failure signal, not a grade. Separately: zero `contested` on a contested topic is not an achievement but a sign that dissenters were not looked for. A metric that is improved by stopping doing the work is not a metric.

**Composition:** The very first element of the report, before [F1]. In the export (Phase 6.9) it is laid out as a trust panel on the first page.

**Template:**

```markdown
> **Citation integrity: 21/23 live · faithfulness 20/22 supported · qualifiers 22/22 preserved · constructs 7/7 sourced · 0 red flags · 2 paywalled**
> Verified <YYYY-MM-DD>: liveness via eval/check_citations.py (every OPEN source resolved live);
> faithfulness via Layer 2 judge over evidence/ (2 PARTIAL softened); qualifiers via Layer 3
> over F1/memo.md/Z12 (no scope drift); constructs via Layer 4 (1 marked as ours).
> [liveness detail](.verify/citations.md) · [faithfulness detail](.verify/faithfulness.md) · [qualifier detail](.verify/qualifiers.md) · [construct detail](.verify/constructs.md)
>
> **Source independence: authority 12/14 qualified (2 quarantined) · numbers 9/9 dated ·
> overlap 0.12 · 0 circulation flags · 1 contested claim**
> s11, s23 quarantined (no author, origin unknown) — neither is a sole support.
> CL6 contested: minority s60 (regulator filing) vs 3 secondary — both positions in §4.
```

When flags were found and paid down:

```markdown
> **Citation integrity: 23/23 live · faithfulness 23/23 supported · qualifiers 21/23 preserved · 1 red flag + 1 overclaim + 2 qualifiers restored**
> s14 (dead URL → replaced <date>); C4 (PARTIAL → claim softened to match source);
> CL7 (BROADENED → "on fixtures with embedded state" restored in TL;DR).
```

When an axis is below the floor and the user decided to ship anyway (medium only):

```markdown
> ⚠ **Citation integrity: liveness 0.64 · faithfulness 0.71 · qualifiers 0.88 — liveness below floor (0.70).**
> s07, s11 (transport UNKNOWN), s19 (OPEN dead → claim demoted); C9 (UNSUPPORTED → Open Questions).
```

shallow: the faithfulness/qualifier/construct lines are dropped if the layers were not run.
