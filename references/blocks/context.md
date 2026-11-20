<!-- translated from upstream/references/blocks/context.md @ e233797 — see docs/TRANSLATION.md -->
# CONTEXT blocks — external context

Blocks about the context around the topic: regulation, geography, culture, history, politics, tech stack, ecosystem.

---

## X1 — `regulatory`

**When:** Fintech, medtech, AI, crypto, any regulated domain.

**What's inside:** Regulatory context: laws, compliance requirements, restrictions by jurisdiction.

**Anti-pattern:** Regulation as a list with no impact — you need to show how it affects the topic.

**Composition:** Before `decision` or `landscape` if regulation is critical.

**Template:**

```markdown
## Regulatory context

### Jurisdictions and applicable regulations

| Jurisdiction | Regulator | Key requirements | Status | Source |
|---|---|---|---|---|
| US | <SEC / FDA / etc> | <requirements> | active | [s03] |
| EU | <ESMA / EBA / DPC> | GDPR, MiCA, ... | active | [s07] |
| UK | FCA | <requirements> | active | [s11] |
| Asia | varies by country | — | varies | [s14] |

### Recent / upcoming changes
- **<Regulation A>** (effective <date>): <what changes> [s05]
- **<Regulation B>** (proposed): <if passes, impact ...>
- **Sunset clauses:** <if any regulations expire>

### Compliance burden
- **Light touch:** <jurisdictions>
- **Medium:** <jurisdictions>
- **Heavy:** <jurisdictions, e.g. EU MiCA>

### Banned / restricted
- In <country>, <activity> is prohibited
- In <country>, <constraint> is restricted

### Regulatory risk for the topic
- **High risk:** if <event>, whole industry affected
- **Watch list:** <pending regulations to monitor>
- **Wins from regulation:** moats for compliance-ready players

### Source disclaimer
- Not legal advice. Regulation changes fast.
- Last update: <date>
- For actual compliance — consult counsel.
```

---

## X2 — `geo-context`

**When:** Global markets, migration, jurisdictions, cross-cultural topics.

**What's inside:** Differences by country / region.

**Anti-pattern:** Generalising «in Asia X happens» — Asia is not uniform. Be concrete.

**Composition:** A supplement to `landscape` or `regulatory`. Before `cultural-context` if they go together.

**Template:**

```markdown
## Geographic context

### Regional differences

| Region / Country | What differs | Why |
|---|---|---|
| US | <unique pattern> | <historical/economic reason> |
| EU | <pattern> | <reason> |
| China | <pattern> | <reason> |
| Japan | <pattern> | <reason> |
| Brazil | <pattern> | <reason> |
| India | <pattern> | <reason> |

### Hot markets
- **Fastest growing:** <country/region> — why [s07]
- **Mature / saturating:** <country/region>
- **Emerging / unexplored:** <country/region>

### Cross-border considerations
- Data sovereignty: <where data must stay>
- Currency / payment friction: <issues>
- Localization needs: <language, formats, cultural>

### Source
- Multi-country comparison from [s05]
- Local context from [s11], [s14]
```

---

## X3 — `cultural-context`

**When:** Cross-cultural topics. Where culture matters substantially.

**What's inside:** Cultural specifics with concrete impact on the topic.

**Anti-pattern:** Stereotypes instead of observable patterns. Take data-backed observations.

**Composition:** After `geo-context`. Complements the geography.

**Template:**

```markdown
## Cultural context

### Culturally relevant patterns

#### Pattern 1: <observable cultural trait>
**Where:** <region / culture>
**What:** <observable behavior>
**Source:** [s05] (ethnographic study / survey)
**Impact on topic:** <how this changes the topic>

#### Pattern 2: ...

### Cross-cultural differences in this topic

| Dimension | Culture A | Culture B | Culture C |
|---|---|---|---|
| <relevant dim 1> | <how A approaches> | <how B> | <how C> |
| <relevant dim 2> | ... | ... | ... |

### Common mistakes (cultural blind spots)
- Westerners assuming X about Eastern markets — actually Y
- Tech assumptions universal — actually vary by culture

### Source-rigorous notes
- Avoid generalizations without backing data
- Cited cultural patterns from [s07] (peer-reviewed) and [s14] (industry survey N=2000)
```

---

## X4 — `historical-context`

**When:** Historical analysis. Deep explainer. Where «how we got here» is critical.

**What's inside:** What came before and why it matters for understanding now.

**Anti-pattern:** History for history's sake. Every historical fact must relate to current understanding.

**Composition:** At the start of the explanation. Before `mental-model` or `stepwise`.

**Template:**

```markdown
## Historical context

### Origins (<period>)
**What existed before:** <the preceding state>
**Key actors / movements:** <who/what mattered>
**Source:** [s05]

### Inflection points

#### <Year/event 1>
**What happened:** ...
**Why it mattered:** <changed trajectory>
**Source:** [s07]

#### <Year/event 2>
...

#### <Year/event 3>
...

### Path dependency
What we have now exists the way it does precisely because:
- Decision X in <year> locked in <pattern>
- Failed attempts at Y in <year> made people skeptical of <approach>
- Standard Z became default by historical accident

### If history had gone differently
- Counterfactual 1: if <event A> had not happened → <different world>
- Counterfactual 2: if <person B> had not done <X> → <different now>

### Why historical context matters for current decisions
- Path dependency means <current option> is easier than <theoretical better option>
- Cultural memory of <past failure> makes <X> politically hard
- Existing infrastructure investments lock in <pattern>
```

---

## X5 — `political-context`

**When:** Geopolitics, sanctions, market access, government-related topics.

**What's inside:** Political factors affecting the topic.

**Anti-pattern:** Partisan framing. Strive to be neutral in form, fact-based.

**Composition:** A supplement to `regulatory` or `geo-context`. When politics matters substantially.

**Template:**

```markdown
## Political context

### Government stance (by jurisdiction)
- **US:** <current admin position> — may change after the next election
- **EU:** <position> — driven by <commission body>
- **China:** <position> — strategic priority for <reason>
- **Russia:** <if relevant>
- **Other:** <country-specific positions>

### Geopolitical tensions affecting topic
- **Tension 1:** <description>, affects via <mechanism>
- **Tension 2:** <description>

### Sanctions / trade restrictions
- <country X> blocked from <activity Y>
- <country Z> faces tariffs on <category>
- Source: [s07]

### Political risk
- **High risk:** <if scenario X happens>
- **Watch list:** <upcoming elections, policy changes>
- **Stable factors:** <bipartisan consensus areas>

### Influence groups / lobbies
- <Group A> lobbying for <position>
- <Group B> opposing
- Outcome leans toward <if known>

### What could change
- Election in <country/year>
- <new admin position>
- International agreement <pending>

### Sources & neutrality
- Multiple sources from different perspectives: [s03] (left-leaning), [s07] (right-leaning), [s11] (centrist)
- Aim for triangulation, not a single point of view
```

---

## X6 — `tech-stack-context`

**When:** Tech research. When you need to understand which technologies are underneath.

**What's inside:** The technologies underneath the topic + dependencies + alternatives.

**Anti-pattern:** Tech listing without understanding "what for". Every tech must explain its role.

**Composition:** In technical explainers. Before `mental-model` for tech-heavy topics.

**Template:**

```markdown
## Tech stack context

### Foundational technologies
- **<Tech A>** — what: <role in topic>, why it is used
- **<Tech B>** — what: <role>, alternatives: <list>
- **<Tech C>** — what: <role>, history: was once <alternative> until <event>

### Architecture pattern (high-level)
```
[Layer 1: ...] — implemented with <Tech A>
[Layer 2: ...] — implemented with <Tech B>
[Layer 3: ...] — implemented with <Tech C>
```

### Dependencies
- Topic depends on <external tech/service X>
- If X breaks / changes, topic affected
- Backup / alternatives: <if any>

### Common variants of the stack
- **Variant 1:** Tech A + Tech B + alternative for C
- **Variant 2:** Different combination — when preferred
- **Variant 3:** Minimal — for prototyping

### Tech maturity
- **Mature / stable:** <techs that won't change>
- **Active development:** <techs in flux>
- **Experimental:** <bleeding edge>

### Lock-in risks
- <Tech X> creates vendor lock-in via <mechanism>
- Migration complexity: <high / medium / low>

### Source
- [s03] (technical deep-dive)
- [s07] (architectural blog from practitioners)
```

---

## X7 — `ecosystem`

**When:** Platform analysis. When the topic is part of a larger ecosystem.

**What's inside:** Neighbours, complementing and competing platforms around the topic.

**Anti-pattern:** Listing every related thing. Only the relevant ecosystem players.

**Composition:** After `landscape` or as a supplement to it. Extends the boundaries beyond direct competitors.

**Template:**

```markdown
## Ecosystem

### The subject at the centre of the ecosystem

```
              ┌─── Customers / Users ───┐
              ▼                         ▼
       ┌──── SUBJECT ────┐
       │                 │
       │                 │
       ▼                 ▼
[Suppliers/Inputs]   [Complementors]
       │                 │
       └─── Competitors ─┘
       └─── Substitutes ─┘
```

### Stakeholder groups

#### Customers / Users
- <segment 1> — needs: ..., budget: ...
- <segment 2> — needs: ...

#### Suppliers / Inputs
- <supplier A> — provides: <what>
- <supplier B> — provides: <what>

#### Complementors (make subject more valuable)
- <complementor X> — increases value of subject by <mechanism>
- <complementor Y> — without them the subject is less useful

#### Substitutes (alternative ways to achieve same goal)
- <substitute A> — when chosen over subject
- <substitute B> — emerging substitute

#### Direct competitors
- See `landscape` / `profile-card`

### Strategic implications
- **Strong complementors:** <which strengthen our subject>
- **Weak suppliers:** <bottleneck on which subject depends>
- **Emerging substitutes:** <potential disruption>

### Ecosystem health
- Net new entrants per year: <N>
- M&A activity: <high/low>
- Investor interest: <signals>
- Maturity: emerging / growing / mature / declining

### Source
- Industry overview from [s05]
- Ecosystem mapping from [s11]
```
