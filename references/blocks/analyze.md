<!-- translated from upstream/references/blocks/analyze.md @ e233797 — see docs/TRANSLATION.md -->
# ANALYZE blocks — structured analysis

Blocks for structured analytical cuts: tables, SWOT, root cause, etc.

---

## A1 — `data-table`

**When:** Custom for «by indicators» questions. Any comparative analytics with metrics defined in advance.

**What's inside:** A parametric table of object × indicator.

**Anti-pattern:** Including indicators «because there is data». Only those that answer the user's question.

**Composition:** The base block for a custom comparison. Often combined with `profile-card`.

**Template:**

```markdown
## <Objects> by indicators

| Object | Indicator 1 | Indicator 2 | Indicator 3 | Indicator 4 | Source |
|---|---|---|---|---|---|
| Item A | <value> | <value> | <value> | <value> | [s03] |
| Item B | <value> | <value> | <value> | <value> | [s05] |
| Item C | <value> | <value> | <value> | <value> | [s07] |
| Item D | <value> | <value> | <value> | <value> | [s11] |

### Definitions of the indicators
- **Indicator 1:** <how it is measured, in which units>
- **Indicator 2:** ...
- **Indicator 3:** ...

### Quality of data
- For Item A: data as of <date>, source [s03] — Credibility 5
- For Item B: estimates only (no exact public figures) — Credibility 3
- For Items C, D: comparable, current

### Observations
- <Item X> leads on <indicator>
- <Item Y> is a clear outlier on <indicator> — why
- Spread on <indicator>: <min>-<max>, median <Z>
```

---

## A2 — `timeline`

**When:** Custom for historical / sequential topics.

**What's inside:** A chronology with dates and the significance of each event.

**Anti-pattern:** A chronology without significance — it reads as trivia. Every event must explain «so what».

**Composition:** An alternative to `stepwise` for historical topics. A supplement to `historical-context`.

**Template:**

```markdown
## Timeline

### YYYY-MM-DD — <Event 1>
**What happened:** ...
**Significance:** <why this is a turning point>
**Source:** [s03]

### YYYY-MM-DD — <Event 2>
**What happened:** ...
**Significance:** ...
**Source:** [s07]

### YYYY-MM-DD — <Event 3>
...

### Patterns in the timeline
- **Acceleration:** events come more often after <date>
- **Catalysts:** <event X> set off <chain of events Y, Z>
- **Inflection point:** <date> — after it everything became different

### Key players / authors over time
- Person A: active 2015-2020, laid the foundations
- Person B: continued 2018-current, developing in direction X
- ...
```

---

## A3 — `qa-list`

**When:** Q&A genre always. Custom as a supplement to other genres.

**What's inside:** Atomic Q→A pairs with confidence and source links.

**Anti-pattern:** Non-atomic questions («Q1: tell me everything about X»). One question = one answer.

**Composition:** The main block of Q&A. In other genres — an extra section.

**Template:**

```markdown
## Q&A

### Q1: <a concrete question in your own words>
**Answer:** <2-4 sentences>
**Confidence:** high | medium | low — <if below high, why>
**From:** [s03](sources/03_*.md), [s12](sources/12_*.md), [s17](sources/17_*.md)
**Nuances:** <caveats, context of applicability>

### Q2: <question>
**Answer:** ...
**Confidence:** ...
**From:** ...
**Nuances:** ...

### Q3: ...
### Q4: ...
### Q5: ...
```

---

## A4 — `hypotheses-outcome`

**When:** Q&A, validation, any research with explicit hypotheses in plan.md.

**What's inside:** A table: hypothesis → verdict → sources.

**Anti-pattern:** Silently dropping a hypothesis from the plan. Every one must get a verdict.

**Composition:** Before the `closing` section. Closes the loop with plan.md.

**Template:**

```markdown
## Hypotheses outcome

| Hypothesis | Verdict | Sources | Comment |
|---|---|---|---|
| H1: <thesis> | ✅ confirmed | s01, s07, s12 | Confirmed by 3 sources of different types |
| H2: <thesis> | ⚠️ partial | s03, s15 | Only under condition X |
| H3: <thesis> | ❌ contradicted | s09, s11, s14 | Refuted by 3 sources |
| H4: <thesis> | 🤷 insufficient | — | Not enough data, see Open Questions |

### What the result says
- 2 of 4 hypotheses confirmed — the expected result
- H3 contradicted — a neat finding, we record it
- H4 — a different approach is needed / next research
```

---

## A5 — `swot`

**When:** Business/product/strategic analysis. Classic SWOT.

**What's inside:** 4 quadrants: Strengths, Weaknesses (internal), Opportunities, Threats (external).

**Anti-pattern:** Mixing up the internal and the external. S and W are about the object itself, O and T are about the environment.

**Composition:** A supplement to decision or landscape. Before `recommendation`.

**Template:**

```markdown
## SWOT

### Strengths (internal, positive)
- ✅ ... [s03]
- ✅ ...

### Weaknesses (internal, negative)
- ❌ ... [s07]
- ❌ ...

### Opportunities (external, positive)
- 💡 ... [s11]
- 💡 ...

### Threats (external, negative)
- ⚠️ ... [s15]
- ⚠️ ...

### Reading the SWOT
- **S × O (best):** how strengths can capture opportunities → <strategy>
- **W × T (worst):** what weaknesses make us vulnerable to threats → <mitigation>
- **S × T:** use strengths to defend against threats
- **W × O:** address weaknesses to access opportunities
```

---

## A6 — `risk-register`

**When:** Custom for risky decisions. Project planning, business decisions.

**What's inside:** A risk register with probability × impact + mitigation.

**Anti-pattern:** No mitigation — the register becomes a list of worries.

**Composition:** In decision for risky ones. After `options-matrix`.

**Template:**

```markdown
## Risk register

| ID | Risk | Probability | Impact | Risk score | Mitigation | Owner |
|---|---|---|---|---|---|---|
| R1 | <risk description> | high | high | 9 | <action> | <who> |
| R2 | <risk> | medium | high | 6 | <action> | <who> |
| R3 | <risk> | high | low | 3 | accept | — |
| R4 | <risk> | low | high | 3 | watch + plan | <who> |
| R5 | <risk> | low | low | 1 | ignore | — |

**Scoring:** probability (1-3) × impact (1-3). Risks ≥6 — top priority.

### Top risks (>=6)
- **R1:** <expanded explanation, why it's the biggest>
- **R2:** ...

### Risk acceptance
- Which level of risk is acceptable — <threshold>
- Who accepts the risk — <person/role>
- What triggers escalation — <signal>
```

---

## A7 — `dependency-graph`

**When:** Project planning. System analysis. What depends on what.

**What's inside:** Nodes + dependencies + critical path.

**Anti-pattern:** A tree with no direction. Dependencies are directed — A depends on B.

**Composition:** Custom for project research. An alternative to `flow-diagram` for static systems.

**Template:**

```markdown
## Dependencies

```
                ┌──── E ◄─── A
                │
       D ◄────── B ◄─── C
       │
       └──► F ──► G
```

**Reading:** A depends on E. B depends on E and is required by D. C → B → D chain.

### Critical path
- A → E → B → D — longest path
- Latency of this chain: <if time matters — Z hours/days/weeks>

### Dependency types
- **Hard:** A does not work without B (strong dependency)
- **Soft:** A works worse without B (degraded)
- **Optional:** A can work without B

### Risks from dependencies
- If E falls — A, B, D fall (high blast radius)
- If F falls — only G (low blast radius)
- Single points of failure: <nodes>
```

---

## A8 — `bottleneck-analysis`

**When:** Performance analysis. Ops. Any bottleneck analysis.

**What's inside:** Where the bottleneck is + why + how to identify it.

**Anti-pattern:** «It's slow somewhere» with no specifics. A bottleneck is a concrete component with a concrete limit.

**Composition:** In technical explainers or when validating perf claims. After `flow-diagram` if there is one.

**Template:**

```markdown
## Bottleneck analysis

### Current bottleneck: <component>
**Limit:** <concrete, e.g. CPU 95%, latency 200ms, throughput 1k req/s>
**Why:** <root cause — for example, single-threaded, network-bound, etc>
**Signals:** <how we see it in the metrics>
**Impact:** <what the user feels>

### Downstream impact
- <Component A>: forced to wait
- <Component B>: drops requests

### If this bottleneck removed — next bottleneck would be
- **<Component X>** — limit: <Z>
- Then: **<Component Y>**

**Order of optimization:**
1. Fix current (<expected improvement>)
2. Then watch for next
3. Don't optimize early — current is dominant

### Why it became a bottleneck
- <historical reason>
- <design decision>
- <load growth>
```

---

## A9 — `force-field`

**When:** Change analysis. Lewin's force field — which forces are for and against the change.

**What's inside:** Forces FOR change vs forces AGAINST. Magnitudes.

**Anti-pattern:** Not assessing the magnitude — all forces then look equal. In reality they are not.

**Composition:** Custom for organizational/strategic analysis. An alternative to SWOT.

**Template:**

```markdown
## Force field analysis

**Proposed change:** <what we are changing>

### Forces FOR change (driving)
| Force | Magnitude | Description | Source |
|---|---|---|---|
| F1 | high | <description> | [s03] |
| F2 | medium | ... | [s07] |
| F3 | low | ... | — |

### Forces AGAINST change (restraining)
| Force | Magnitude | Description | Source |
|---|---|---|---|
| R1 | high | <description> | [s05] |
| R2 | medium | ... | [s11] |
| R3 | low | ... | — |

### Net force
- Forces FOR (high): N
- Forces AGAINST (high): M
- **Net direction:** <change happens / change blocked / equilibrium>

### Strategy
- **To enable change:** weaken which restraining force?
- **Strongest leverage:** R1 has high magnitude — find way to address
- **Easiest leverage:** R3 is low — pick low-hanging fruit
```

---

## A10 — `5-whys`

**When:** Root cause analysis. Any «why does X happen» question.

**What's inside:** A chain of «why» 5 levels down to the root cause.

**Anti-pattern:** Stopping at the first «because». Go down to the root.

**Composition:** Custom for debugging/diagnostic research. A supplement to `dependency-graph`.

**Template:**

```markdown
## 5 Whys

**Problem:** <observable issue>

**Why 1:** <the first cause>
**Source for this answer:** [s03]

**Why 2 (why does that happen):** <the second cause>
**Source:** [s07]

**Why 3:** ...

**Why 4:** ...

**Why 5 (root cause):** <fundamental cause>
**Source:** [s11]

### Root cause
<in sum — what the fundamental cause is>

### Fix at which level?
- Fixing at Level 1 — quick fix, problem returns
- Fixing at Level 3 — partial solution
- **Fixing at Level 5 (root) — permanent solution but expensive**

### Caveats
- 5-whys works for sequential cause chains, not for complex systems
- In complex systems there may be several root causes
- It may need to be supplemented with an Ishikawa cause diagram
```

---

## A11 — `swot-extended`

**When:** Strategic analysis. When you want not just a SWOT but something actionable.

**What's inside:** SWOT + something actionable from each quadrant (TOWS matrix).

**Anti-pattern:** Using it instead of the basic SWOT when the basic one is enough.

**Composition:** An enhanced version of `swot`. Do not use both together.

**Template:**

```markdown
## Extended SWOT (with actions)

### Strengths
- S1: ... [s03]
- S2: ...

### Weaknesses
- W1: ... [s05]
- W2: ...

### Opportunities
- O1: ... [s07]
- O2: ...

### Threats
- T1: ... [s11]
- T2: ...

### TOWS matrix — actionable strategies

|     | **Opportunities** | **Threats** |
|---|---|---|
| **Strengths** | **SO strategies (use S to capture O):**<br>1. S1 + O1 → <action><br>2. S2 + O2 → <action> | **ST strategies (use S to defend from T):**<br>1. S1 vs T1 → <action> |
| **Weaknesses** | **WO strategies (fix W to access O):**<br>1. Fix W1 → enables O1 | **WT strategies (minimize W exposure to T):**<br>1. <action> |

### Priority of actions
1. <highest priority action with rationale>
2. ...
```

---

## A12 — `pestle`

**When:** Macro analysis. Market environment analysis.

**What's inside:** Political/Economic/Social/Technological/Legal/Environmental factors.

**Anti-pattern:** Filling in every category no matter what. If there is nothing relevant under Environmental — skip it.

**Composition:** Custom for broad market/industry analysis. May precede landscape.

**Template:**

```markdown
## PESTLE analysis

### Political
- <factor> — impact: high/medium/low — direction: ↑ favorable / ↓ adverse / ↔ neutral [s03]
- ...

### Economic
- <factor> — impact, direction
- Inflation, currency, interest rates if relevant

### Social
- <demographic/cultural shift>
- Consumer behavior changes

### Technological
- <emerging tech disruption>
- Platform shifts

### Legal
- <regulatory changes>
- <new compliance requirements>

### Environmental
- <if relevant — climate, sustainability>
- If there is no relevance: write "n/a, not relevant to the topic"

### Summary
- **Net environment:** favorable / hostile / mixed
- **Dominant factors:** <top 2-3 across all categories>
- **Watch list:** factors which could shift quickly
```

---

## A13 — `before-after`

**When:** Impact analysis. Before and after a change.

**What's inside:** Metrics before and after, with the delta.

**Anti-pattern:** Only after numbers without before. No context.

**Composition:** Custom for validating the effect of changes.

**Template:**

```markdown
## Before / After

**Change:** <what happened>
**Date:** <when>
**Population:** <who/what affected>

### Metrics

| Metric | Before | After | Δ (abs) | Δ (%) | Significance |
|---|---|---|---|---|---|
| <metric 1> | 100 | 150 | +50 | +50% | high (statistically sig) |
| <metric 2> | 5 | 4.8 | -0.2 | -4% | not significant |
| <metric 3> | $1000 | $800 | -$200 | -20% | high |

### Attribution
- Confidence that the change was caused by the change: high | medium | low
- Confounders:
  - Other changes at the same time <something else changed too>
  - Seasonality
  - Selection bias

### Counterfactual
- What would have happened without the change: <baseline projection> [s07]
- Difference vs counterfactual: <numbers>

### Lessons
- <takeaway 1>
- <takeaway 2>
```
