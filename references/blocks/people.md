<!-- translated from upstream/references/blocks/people.md @ e233797 — see docs/TRANSLATION.md -->
# PEOPLE blocks — people, teams, behaviour

Blocks about the human dimension of a topic: personas, organizations, individuals, behaviors, incentives.

---

## P1 — `persona`

**When:** UX research, product analysis, customer-centric research.

**What's inside:** User profiles with needs, behaviors, pain points.

**Anti-pattern:** Demographic profiles without needs ("33 years old female") — they do not work for design decisions. Take a jobs-to-be-done framing.

**Composition:** Before `user-journey` if present. Custom for UX research.

**Template:**

```markdown
## Personas

### Persona 1: <name/role>
**Who:** <short description — role, context>
**Goals:** what they want to achieve
**Pain points:**
- <pain 1> — [s03]
- <pain 2>
**Current behaviors:**
- What they do now to reach their goals
**Tools they use:** <existing solutions>
**Decision criteria:** <how they choose tools>
**Source basis:** <interviews / surveys / app reviews — [s05]>

### Persona 2: <name/role>
...

### Anti-persona (who it does NOT fit)
**Who this is:** ...
**Why it does not fit:** ...
```

---

## P2 — `team-org`

**When:** Competitor analysis, due diligence, organizational research.

**What's inside:** The structure of the team/organization, the key roles, the relationships.

**Anti-pattern:** Just a list of people without an understanding of their role in decision-making.

**Composition:** A supplement to `profile-card` for deep due diligence.

**Template:**

```markdown
## Team / Org structure

### <Company X>

**Total headcount:** N (as of <date>)

**Org structure:**
```
          ┌──────── CEO ────────┐
          │                     │
    ┌─────▼─────┐         ┌─────▼─────┐
    │  CTO      │         │   COO     │
    └─────┬─────┘         └───────────┘
          │
    ┌─────┴────────┬────────────┐
    ▼              ▼            ▼
  Eng (N)     ML (N)       Product (N)
```

**Key functional groups:**
- **Engineering** — N people, lead: <name>
- **ML** — N people, lead: <name>
- **Product** — N people, lead: <name>
- **GTM** — N people, lead: <name>

**Signals from structure:**
- The ML team is growing fast → ML-driven roadmap
- No dedicated security → security as a side responsibility
- Sales/CS ratio: <N/M> → product-led vs sales-led

**Hiring activity (last 6 months):**
- N new hires in <function>
- Specific roles: <list>
- What it means: <expansion in X area>

**Source:** [s07] (LinkedIn analysis), [s11] (job postings)
```

---

## P3 — `key-people`

**When:** Understanding the key people in the industry. Who stands behind what.

**What's inside:** Cards for people: bio, past projects, influence.

**Anti-pattern:** Too many people — a list without prioritisation. Take the key ones (5-10), not everyone.

**Composition:** A supplement to `profile-card` or `landscape`. Deep due diligence.

**Template:**

```markdown
## Key people

### <Person 1 Name> — <current role>

**Bio:** <short bio>
**Prior:** <prev companies/projects>
**Education:** <if relevant>
**Achievements:** <what significant was reached>
**Influence:** <how much they shape the field — 1-5>
**Public presence:** Twitter @, blog, recent talks
**Conflict of interest considerations:** <if committed to a determined view>
**Source:** [s05]

### <Person 2 Name> — <role>
...

### Networks of key people
- <Person 1> and <Person 2> often collaborate — same alma mater
- <Person 3> is perceived as an opponent to the view of <Person 1>
- <Person 4> — an emerging voice, appeared recently

### Where these people speak / publish
- <conferences>
- <publications>
- <podcasts>
```

---

## P4 — `user-journey`

**When:** UX, product design. When the user's path must be understood.

**What's inside:** Steps + what the user does + what they feel + where the friction is.

**Anti-pattern:** Only actions without emotions — the friction cannot be identified.

**Composition:** After `persona`. Often combined.

**Template:**

```markdown
## User journey: <persona> achieving <goal>

### Step 1: <Awareness / Discovery>
**Trigger:** what made them start
**Action:** <what the user does>
**Touchpoints:** <where they interact — web/app/email>
**Emotion:** 😊 / 😐 / 😟 / 😡
**Friction:** <if any — what gets in the way>
**Source:** [s03]

### Step 2: <Consideration>
...

### Step 3: <Decision>
...

### Step 4: <Purchase / Sign-up / Commit>
...

### Step 5: <Onboarding>
...

### Step 6: <Active use>
...

### Step 7: <Retention / Churn>
...

### Pain points summary
- 🔴 Step 3 — biggest friction: <description> [s07]
- 🟡 Step 5 — onboarding too long
- 🟢 Step 6 — works smoothly

### Time investment
- Time to first value: <X minutes/hours>
- Total time to commit: <X days/weeks>
```

---

## P5 — `behavioral-patterns`

**When:** Behavioral analysis. Trading behavior, user behavior, market behavior.

**What's inside:** Patterns in participant behavior + their strength + their triggers.

**Anti-pattern:** A description of behaviour without an objective signal (how we know it is a pattern).

**Composition:** Custom for behavioral/economic research. After `persona` if present.

**Template:**

```markdown
## Behavioral patterns

### Pattern 1: <name>
**What they do:** <description of the behaviour>
**When:** <trigger / conditions>
**Who:** <which participants>
**Sample:** N=<observed>
**Strength:** consistent | occasional | rare
**Direction:** rational | irrational | strategic
**Source:** [s07]

**Why this happens (hypotheses):**
- Incentive structure (see `incentive-structure`)
- Cognitive bias: <bias name>
- Information asymmetry
- Coordination dynamics

**Implications for X:** <what this means for our topic>

### Pattern 2: <name>
...

### Pattern 3: <name>
...

### Anti-patterns (what DOESN'T happen contrary to expectations)
- Nobody does <expected behavior> — why: ...
```

---

## P6 — `incentive-structure`

**When:** Game theory, market design, organizational analysis.

**What's inside:** Who gets what, what the incentives of each participant are.

**Anti-pattern:** Ignoring misaligned incentives. A conflict of interest is often the key explanation.

**Composition:** Before `behavioral-patterns`. Explains "why it is this way".

**Template:**

```markdown
## Incentive structure

### Participants

| Actor | Gets | Pays | Net incentive | Strength |
|---|---|---|---|---|
| A | <gain> | <cost> | <direction> | high |
| B | <gain> | <cost> | <direction> | medium |
| C | <gain> | <cost> | <direction> | low |

### Detailed analysis

#### Actor A
- **Primary motive:** <what matters most to A>
- **What A optimizes:** <specific metric>
- **Constraints:** <what they cannot do>
- **Conflict with whom:** <A vs B>
- **Source:** [s05]

#### Actor B
...

### Misalignments (where interests diverge)
- A vs B: A maximizes X, B maximizes ¬X
- Result: <observable conflict>

### Aligned incentives (where they converge)
- A and C both want Y
- Result: <observable cooperation>

### Equilibrium (if any)
- In the current system the stable state: <description>
- Causal model: <how some behaviours stabilize others>

### How to shift behavior
- Change the incentive: <if X changed, then A would do Y>
- Mechanism design: <leverage point>
```

---

## P7 — `expert-opinion`

**When:** Expert-driven validation. When expert opinion is critical.

**What's inside:** An expert card with the opinion and the conflict of interest.

**Anti-pattern:** Accepting an expert's opinion without assessing conflicts. Experts are biased too.

**Composition:** In validation as a specific evidence type. An alternative to `evidence-graded` for qualitative claims.

**Template:**

```markdown
## Expert opinions

### Expert 1: <Name> — <credentials>

**Stated opinion:** <what they say, direct quote or close>
**Source:** [s05] (interview / talk / paper)
**Date:** <when said>

**Credentials:**
- N years in <field>
- Published in <journals>
- Position at <institution>

**Independence:**
- **Funded by:** <source — may be a conflict>
- **Affiliations:** <relevant ones>
- **Past stances:** <consistent / changed view recently>
- **Conflict of interest:** <yes/no/possible>

**Trust score:** A (independent + credentialed) | B (credentialed but conflicted) | C (anecdotal)

### Expert 2: <Name>
...

### Aggregate of expert opinions
- Consensus: <if any>
- Disagreement: <where>
- Independent vs conflicted ratio: <N/M>

### Caveats
- All experts from one school of thought → groupthink is possible
- Experts from different schools → see `conflicting-evidence`
```
