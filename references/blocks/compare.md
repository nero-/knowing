<!-- translated from upstream/references/blocks/compare.md @ e233797 — see docs/TRANSLATION.md -->
# COMPARE blocks — comparison and choice

Blocks for the decision genre and any research where options must be compared.

---

## C1 — `options-matrix`

**When:** Decision. Comparing options by criteria with no weights.

**What's inside:** A table of options × criteria. A numeric score 1-5 or a qualitative one.

**Anti-pattern:** Treating all criteria as equal — in reality one or two decide. If the criteria are not equal in weight — take `weighted-score`.

**Composition:** After `decision-context`. Before `weighted-score` if you want both (matrix + scoring).

**Template:**

```markdown
## Options matrix

| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| Latency | 5 | 3 | 4 |
| Cost | 3 | 5 | 4 |
| Dev velocity | 4 | 5 | 3 |
| Reliability | 5 | 4 | 4 |
| Vendor lock-in (less is better) | 4 | 2 | 5 |
| **Sum** | **21** | **19** | **20** |

**Score legend:** 5=Best-in-class, 4=Strong, 3=Average, 2=Below average, 1=Weak/Missing.

**What did not go into the matrix (because it is the same everywhere):** ...
```

---

## C2 — `weighted-score`

**When:** Decision when the criteria carry different weights.

**What's inside:** Options × criteria × weights → weighted total.

**Anti-pattern:** Hiding the weights in footnotes. The weights must be transparent and debatable.

**Composition:** After `decision-context`. An alternative to or a supplement to `options-matrix`.

**Template:**

```markdown
## Weighted score

Weights by the priorities from the decision-context:

| Criterion | Weight | A score | A weighted | B score | B weighted | C score | C weighted |
|---|---|---|---|---|---|---|---|
| Latency | 3 | 5 | 15 | 3 | 9 | 4 | 12 |
| Cost | 2 | 3 | 6 | 5 | 10 | 4 | 8 |
| Dev velocity | 2 | 4 | 8 | 5 | 10 | 3 | 6 |
| Reliability | 3 | 5 | 15 | 4 | 12 | 4 | 12 |
| **Weighted total** | | | **44** | | **41** | | **38** |

**Justification of the weights:**
- Latency × 3 — the critical path of the product (see [s05])
- Cost × 2 — important, but not blocking
- ...

**Sensitivity:** if Latency is changed to ×2, the ranking does not change (A=37, B=38, C=34) — the choice of A is robust.
```

---

## C3 — `best-fit-when`

**When:** Decision always. For each option — the conditions under which it is the right one.

**What's inside:** For each option, a set of conditions «take it if...».

**Anti-pattern:** «X is always better» — almost never true. Every option is optimal under some conditions.

**Composition:** After `options-matrix` or `weighted-score`. Before `trade-offs`.

**Template:**

```markdown
## Best fit when

### Option A — take it if:
- Critical path = latency
- The team already knows stack A
- You are ready to accept <trade-off>
- Budget ≥ X

### Option B — take it if:
- Critical path = cost
- This is an MVP or an early stage
- The team is mixed, a low entry barrier is needed
- You can live with <trade-off>

### Option C — take it if:
- You need to avoid vendor lock-in
- The regulator requires <constraint>
- ...
```

---

## C4 — `reversibility-stakes`

**When:** Decision. Especially high-stakes and hard-to-reverse ones.

**What's inside:** Reversibility (one-way vs two-way door, Bezos-style) + the stakes level + what a rollback takes.

**Anti-pattern:** Not assessing reversibility — the main cause of regret. A two-way door can be decided fast, a one-way one never.

**Composition:** After `options-matrix`. Before `recommendation-conditional`.

**Template:**

```markdown
## Reversibility & stakes

### Option A
- **Reversibility:** two-way door (you can roll back in <time>)
- **Stakes:** medium
- **What a rollback takes:** <concrete actions + cost>
- **Point of no return:** <when it becomes one-way>

### Option B
- **Reversibility:** one-way door
- **Stakes:** high
- **What a rollback takes:** only a rebuild from scratch, ~<time> ~$<cost>
- **Mitigation:** run a pilot on 10% before full commit

### Option C
- **Reversibility:** two-way door
- **Stakes:** low
- **What a rollback takes:** trivial
```

---

## C5 — `trade-offs`

**When:** Decision always. An honest conversation about what you lose by choosing each option.

**What's inside:** For each option — what you do NOT get, what you give up.

**Anti-pattern:** Weak trade-offs («there are some difficulties»). Every trade-off must be concrete, with a number if possible.

**Composition:** After `best-fit-when`. Before `recommendation-conditional`.

**Template:**

```markdown
## Trade-offs (honest)

### Choosing A — you lose:
- The B ecosystem of integrations (~50 ready connectors)
- The team's experience in Y (there is a learning curve of ~3 months)
- <a concrete number / fact>

### Choosing B — you lose:
- The latency advantage (B is 80ms slower at P95) [s07]
- Flexibility of customization
- Long-term cost optimization (B is vendor-locked, prices grow 15% YoY)

### Choosing C — you lose:
- Community and docs (C is a small project, little documentation)
- Hiring pool (few people know it)
```

---

## C6 — `recommendation-conditional`

**When:** Decision, the final block. A clear recommendation with conditions.

**What's inside:** «Take X if Y, otherwise Z» — a format for different conditions.

**Anti-pattern:** «It depends on the circumstances» without enumerating the circumstances. If it depends — enumerate explicitly on what.

**Composition:** After all the comparative blocks. Before `actionable-next-steps`.

**Template:**

```markdown
## Recommendation

**Take A**, if at least 2 of 3 hold:
- Latency = critical path
- A team of ≥ 5 people with experience in Y
- Budget ≥ $X per month

**Otherwise take B**, if:
- MVP / early stage
- Budget < $X
- You are ready to accept <trade-off>

**Otherwise take C** (default fallback):
- Neither A nor B fits
- You need maximum independent control

**When the recommendation changes:**
- If latency stops being critical → A loses the lead
- If a regulator Z appears in our jurisdiction → C moves up
- If there is $X+ funding → A becomes the default
```

---

## C7 — `pre-mortem`

**When:** Decision high-stakes. Before committing to the decision.

**What's inside:** «Imagine that a year from now the decision has failed — why?» A list of failure causes.

**Anti-pattern:** A superficial list («bugs happen»). Every cause must be a concrete failure mechanism.

**Composition:** Before `recommendation-conditional` — it may change the recommendation.

**Template:**

```markdown
## Pre-mortem

**Scenario:** 12 months from now the decision is judged to have failed. Possible causes:

### Scenario A: <technical failure>
**What happened:** <a concrete mechanism>
**Probability:** low | medium | high
**Mitigation:** <what can be done in advance>
**Indicators (what will warn us in advance):** ...

### Scenario B: <team failure>
**What happened:** ...
**Probability:** ...

### Scenario C: <market shift>
...

### Scenario D: <vendor / partner>
...

**The scariest scenario:** <the concrete one>. Mitigation: <what must be done BEFORE the start>.
```

---

## C8 — `cost-benefit`

**When:** Custom for financial decisions or time investment. Any where there are explicit costs and benefits in comparable units.

**What's inside:** A structured cost vs benefit with allowed ranges.

**Anti-pattern:** Counting only tangible costs without opportunity cost. Time is a cost too.

**Composition:** For financial decisions, instead of `options-matrix` or as a supplement to it.

**Template:**

```markdown
## Cost-benefit

### Costs (per <period>)

| Category | Low estimate | High estimate | Source |
|---|---|---|---|
| Time | 80 hours | 160 hours | <justification> |
| Money direct | $5000 | $12000 | [s03] |
| Opportunity cost | <what you won't do> | <what you won't do> | — |
| **Total** | **$X** | **$Y** | |

### Benefits (per <period>)

| Category | Low | High | Confidence | Source |
|---|---|---|---|---|
| Revenue uplift | $10k | $50k | medium | [s07] |
| Time saved | 100h | 300h | high | [s11] |
| Strategic value | — | — | low (qualitative) | — |

### Net
- **Pessimistic (low benefits, high costs):** -$2k = net negative
- **Realistic (mid):** +$15k
- **Optimistic (high benefits, low costs):** +$50k

### Break-even
- Break-even point: <condition>
- Time to break-even: <months>
```

---

## C9 — `pros-cons-each`

**When:** Quick decision, light-weight reports. When a matrix is overkill.

**What's inside:** Pro/Con lists for each option.

**Anti-pattern:** Not to be used in high-stakes research — too superficial. For quick takes.

**Composition:** An alternative to `options-matrix` for shallow decision research.

**Template:**

```markdown
## Pros & Cons

### Option A
**Pros:**
- ✅ ... [s03]
- ✅ ...
- ✅ ...

**Cons:**
- ❌ ... [s07]
- ❌ ...

### Option B
**Pros:**
- ✅ ...
- ✅ ...

**Cons:**
- ❌ ...
- ❌ ...
```

---

## C10 — `feature-matrix`

**When:** Product comparison. When comparing products by the presence of features.

**What's inside:** A features × products table (✅ present / ❌ absent / 🟡 partial / 💰 paid).

**Anti-pattern:** A long list of features without prioritisation. Features split into core (must-have) and nice-to-have.

**Composition:** A supplement to `options-matrix` for a product decision. After it.

**Template:**

```markdown
## Feature matrix

### Core features (must-have)

| Feature | Product A | Product B | Product C |
|---|---|---|---|
| <feature 1> | ✅ | ✅ | 🟡 partial |
| <feature 2> | ✅ | ❌ | ✅ |
| <feature 3> | 💰 paid only | ✅ | ✅ |
| <feature 4> | ✅ | ✅ | ❌ |

### Nice-to-have

| Feature | A | B | C |
|---|---|---|---|
| <feature 5> | ✅ | ❌ | ❌ |
| <feature 6> | 🟡 | ✅ | ✅ |

**Coverage:**
- A: 4/4 core (75% all)
- B: 3/4 core (62% all)
- C: 3/4 core (62% all)
```

---

## C11 — `migration-path`

**When:** Decision where reversibility is possible but takes effort. «If A does not land, how do we migrate to B?»

**What's inside:** The steps of the migration A→B with time and risk.

**Anti-pattern:** Hiding the migration costs. They are part of the decision.

**Composition:** After `reversibility-stakes`. Makes the reversibility concrete.

**Template:**

```markdown
## Migration paths

### A → B (if decision A does not land)
1. **Preparation** (~<time>): <what needs to be done>
2. **Pilot migration** (~<time>): <a part of the data/functionality>
3. **Full cutover** (~<time>): <…>
4. **Rollback option until the end**: yes/no

**Risks:**
- ⚠️ Data loss risk: low | medium | high
- ⚠️ Downtime: <time>
- ⚠️ Customer impact: ...

**Total cost:** <time> + $<cost>

### A → C (alternative path)
...
```

---

## C12 — `decision-tree`

**When:** Complex multi-condition decisions. When «if X — A, if Y — B» is more than 2 branches.

**What's inside:** An ASCII decision tree or a text structure.

**Anti-pattern:** A tree with >7 leaves — it becomes unreadable. If so — simplify the question or split it into 2 trees.

**Composition:** Can replace `recommendation-conditional` for complex cases. Or supplement it.

**Template:**

```markdown
## Decision tree

```
Q1: Is this a high-stakes decision (revert >$50k)?
├─ Yes: Q2: A regulated domain?
│       ├─ Yes → Option C (compliance-first)
│       └─ No:  Q3: A team of ≥ 5 senior?
│               ├─ Yes → Option A
│               └─ No  → Option B (managed service)
└─ No:  Q4: Latency critical?
        ├─ Yes → Option A (regardless of size)
        └─ No  → Option B (cheaper, simpler)
```

**Justification of the nodes:**
- Q1 stakes threshold $50k is justified: [s05]
- Q3 «5 senior» — a practical observation: [s11]
```

---

## C13 — `kill-criteria`

**When:** Decision for risky decisions. «When to abandon each option».

**What's inside:** For each option — the indicators at which it must be killed and switched away from.

**Anti-pattern:** Sunk cost — continuing with an option after clear kill signals. Kill criteria must be pre-stated.

**Composition:** After `recommendation-conditional`. Before `actionable-next-steps`.

**Template:**

```markdown
## Kill criteria

### Option A — kill if:
- Latency did not improve after <effort> work
- Cost overruns >50% of the estimate
- 2+ months to production with no visible progress
- **Then:** migrate to B per the migration-path above

### Option B — kill if:
- The vendor raised prices >30%
- The API became unstable (>5 breaking changes per year)
- **Then:** migrate to A with budget allocation

### Option C — kill if:
- Compliance stopped being a constraint
- **Then:** freedom of choice between A and B
```
