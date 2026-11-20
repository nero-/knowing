<!-- translated from upstream/references/blocks/validate.md @ e233797 — see docs/TRANSLATION.md -->
# VALIDATE blocks — truth verification

Blocks for the validation genre. "Is X true?"

---

## V1 — `falsification-criteria`

**When:** Validation always. BEFORE looking at the evidence.

**What's inside:** What would force us to call the claim false. Formulated in advance — a defence against confirmation bias.

**Anti-pattern:** Formulating falsification after the evidence — that is already rationalization. Pre-stated only.

**Composition:** Immediately after `claim-precise`. Before `evidence-graded`.

**Template:**

```markdown
## Falsification criteria

BEFORE looking at the evidence we fix: which data would refute the claim?

**If we find:** <specific observation X> → the claim is FALSE.
**If we find:** <observation Y> → the claim is TRUE.
**If we find:** <observation Z> → the claim is conditionally true (only under <condition>).

**Which evidence would be INSUFFICIENT for us:**
- <source type / data type> — even if we find it, we do not count it
- <e.g.: a single study, not replicated — insufficient>

**Recorded before the evidence search began:** yes | no (if no — flag it, admit the bias risk)
```

---

## V2 — `evidence-graded`

**When:** Validation always. After falsification, before the verdict.

**What's inside:** Evidence FOR and AGAINST separately, each with a quality grade A/B/C.

**Anti-pattern:** Mixing the evidence into one list. FOR/AGAINST must be parallel and comparable.

**Composition:** After `falsification-criteria`. Before `verdict-conditional`.

**Template:**

```markdown
## Evidence

### Quality grading
- **A** — peer-reviewed study, RCT, large N, replicated
- **B** — observational study, expert consensus, single-source primary
- **C** — anecdote, single expert opinion, blog post

### Evidence FOR

#### F1: <the thesis in one sentence>
**Source:** [s03] — peer-reviewed, N=2000, 3-year follow-up
**What it says:** ...
**Quality:** A
**Scope:** where, when, on whom the study was done
**Limitations:** ...

#### F2: <thesis>
**Source:** [s07]
**Quality:** B (observational)
...

#### F3: ...

### Evidence AGAINST

#### A1: <the thesis in one sentence>
**Source:** [s11] — meta-analysis of 14 studies
**What it says:** ...
**Quality:** A
**Scope:** ...

#### A2: ...

### Weight summary
- FOR: 3 A-grade + 4 B-grade + 1 C-grade
- AGAINST: 1 A-grade + 2 B-grade
- **Balance:** the evidence is weighted toward FOR, but the A-grade against is serious
```

---

## V3 — `conflicting-evidence`

**When:** Validation when there are directly contradictory sources.

**What's inside:** Cases where the data says X, and where ¬X. An analysis of why they diverge.

**Anti-pattern:** Hiding conflicts. A conflict is itself important information.

**Composition:** After `evidence-graded`. Before `verdict-conditional`.

**Template:**

```markdown
## Conflicting evidence

### Conflict 1: <topic>
**Side A says:** ... [s05]
**Side B says:** ... [s11]
**Why they diverge:**
- Different populations (A in group X, B in group Y)
- Different methodology (RCT vs observational)
- Conflict of interest (B funded by Z)
- Time period (A 2018, B 2024 — things may have changed)

**What is more likely true:** <justification>
**Confidence in this resolution:** medium

### Conflict 2: ...
```

---

## V4 — `base-rates`

**When:** Validation of medical/scientific/probabilistic claims. Where there is a baseline probability.

**What's inside:** The apriori probability + why it is what it is.

**Anti-pattern:** Ignoring the base rate. Bayesian reasoning requires a prior.

**Composition:** Before `evidence-graded`. Context for assessing the strength of the evidence.

**Template:**

```markdown
## Base rates (prior probability)

**Claim:** "X causes Y".

**Base frequency of Y in the general population:** ~Z% [s05]
**Base frequency of Y among people with X:** ~W% [s07]
**Difference (effect size):** W - Z = <X percentage points>

**What this means for the prior:**
- If W ≈ Z → no visible effect in the observational data
- If W >> Z → strong correlation, but causality is still needed

**Confounders that could explain the difference:**
- Age (people with X are older on average)
- Lifestyle
- Selection bias (only certain types report X)

**Prior probability the claim is true (our estimate before the evidence):** ~30%.
```

---

## V5 — `verdict-conditional`

**When:** Validation always. The final verdict.

**What's inside:** The verdict with conditional modifications — "true under X, false under Y, not enough under Z".

**Anti-pattern:** A binary verdict (true/false) when things are really conditional. Most claims are conditional.

**Composition:** After all the evidence blocks. Before `closing` section.

**Template:**

```markdown
## Verdict

**Overall:** confirmed | partially confirmed | contradicted | inconclusive
**Confidence:** high | medium | low

### Unconditional verdict

<if applicable: "The claim is true" or "The claim is false" with a one-sentence justification>

### Conditional verdict (if applicable)

- **True UNDER the condition:** <X>
- **False under:** <Y>
- **Not enough data for:** <Z scenario>

### Scope verdict
- **In context X:** confirmed
- **In context Y:** unclear (more data needed)
- **In context Z:** contradicted

### What went into the verdict
- Evidence FOR — A-grade: <count>, B-grade: <count>
- Evidence AGAINST — A-grade: <count>, B-grade: <count>
- Falsification criteria: <met? violated?>
- Base rate consideration: <taken into account>

### What did NOT go in (deliberately excluded)
- C-grade anecdotes (per the quality cutoff discipline)
- Sources with a known conflict of interest and no disclosure
```

---

## V6 — `what-would-change-verdict`

**When:** Validation after the verdict. What would force a re-examination.

**What's inside:** Concrete data types that would shift the verdict in either direction.

**Anti-pattern:** "More research" without specifics. Be precise — which research exactly, of what design.

**Composition:** After `verdict-conditional`. Before `closing`.

**Template:**

```markdown
## What would change the verdict

**The verdict would rise (from medium to high confidence)** if the following appeared:
- <study type X with N >= ...>
- A replication in <country/population>
- Mechanism elucidation (mechanistic study)

**The verdict would fall (from confirmed to contradicted)** if:
- <evidence type>
- Retraction of <s03>
- A counter-RCT with the opposite effect

**The verdict will not change** from:
- More anecdotal evidence (qualitative ceiling reached)
- More observational data without causation
- Marketing materials
```

---

## V7 — `replication-status`

**When:** Scientific validation. Checking reproducibility.

**What's inside:** Whether the result has been replicated, by whom, how many times.

**Anti-pattern:** Relying on a single study. The replication crisis shows you need ≥2-3.

**Composition:** A supplement to `evidence-graded`. One of the quality factors.

**Template:**

```markdown
## Replication status

### Original study
- **Citation:** [s03]
- **Year:** 2018
- **N:** 250
- **Method:** RCT, double-blind, placebo-controlled

### Replications

| Year | Citation | N | Independent? | Result |
|---|---|---|---|---|
| 2019 | [s05] | 180 | yes (diff lab) | ✅ replicated |
| 2020 | [s07] | 500 | yes (diff country) | 🟡 partial replication (effect smaller) |
| 2022 | [s11] | 300 | no (same lab) | ✅ replicated (but same authors) |
| 2023 | [s14] | 800 | yes | ❌ failed to replicate |

### Status
- **Independent replications:** 2 successful, 1 failed
- **Confidence in original:** medium (mixed replication)
- **Meta-analysis available:** [s17] pooling N=2030, effect size <X>

### Replication signals
- Pre-registration: <yes/no/some>
- Open data: <yes/no/some>
- Conflict of interest declared: <yes/no/some>
```

---

## V8 — `sample-size-analysis`

**When:** Quantitative validation. When the sample size is critical.

**What's inside:** N in each source, statistical power, what it means for confidence.

**Anti-pattern:** Ignoring small N. A study with N=20 is no basis for a confident verdict.

**Composition:** A supplement to `evidence-graded`. Quality detail.

**Template:**

```markdown
## Sample size analysis

| Source | N | Power (if known) | Notes |
|---|---|---|---|
| [s03] | 250 | 0.8 (calculated for d=0.3) | adequate for moderate effect |
| [s05] | 50 | underpowered for small effects | could miss real but small effect |
| [s07] | 2000 | very high power | overall trustworthy |
| [s11] | 18 | severely underpowered | results suggestive only |

### Aggregate N
- Total participants across A-grade studies: ~2300
- Total across B-grade: ~400

### Power considerations
- Small effect (d=0.2) detectable: needs N≥350
- Medium effect (d=0.5) detectable: needs N≥65
- The studies are adequate for a medium effect, marginal for a small one

### Significance vs significance
- Statistical significance ≠ practical significance
- Effect size in real units: <X% change in the outcome>
- Is it clinically/practically significant? <yes/no/depends>
```

---

## V9 — `methodology-critique`

**When:** Validation of scientific claims with serious methodological depth.

**What's inside:** A critique of the methodology of the key sources.

**Anti-pattern:** Treating peer review as finality. Peer review does not catch every problem.

**Composition:** A supplement to `evidence-graded`. Deep critique.

**Template:**

```markdown
## Methodology critique

### [s03] — the main FOR source
**Design:** RCT, N=250
**Strengths:**
- Pre-registered
- Blinded both ways
- Adequate power for stated effect

**Weaknesses:**
- Selection bias risk: only <demographics>, does not generalize
- Outcome measure subjective (self-report)
- 18-month follow-up — may have changed long-term
- Funding: <source> — potential conflict

**Verdict on study:** strong but limited generalizability

### [s11] — the main AGAINST source
**Design:** Observational, N=800
**Strengths:**
...
**Weaknesses:**
- No controls for confounders (age, lifestyle)
- Voluntary participation → selection bias
- ...

**Verdict:** suggestive but not definitive

### Common methodological issues in the field
- <pattern 1>
- <pattern 2>
```

---

## V10 — `bayesian-update`

**When:** Probabilistic validation. When there is a prior and evidence to update on.

**What's inside:** Prior → posterior calculation with likelihood ratios.

**Anti-pattern:** Hardcore Bayesian math without justification. This is for a read-friendly verdict.

**Composition:** After `evidence-graded`. A supplement to `verdict-conditional`.

**Template:**

```markdown
## Bayesian update

### Prior
- P(claim is true) before the evidence: ~30% (see `base-rates`)

### Evidence likelihoods

| Evidence | P(E | claim) | P(E | ¬claim) | LR |
|---|---|---|---|---|---|
| F1 (RCT positive) | 0.7 | 0.2 | 3.5 |
| F2 (replication) | 0.6 | 0.3 | 2.0 |
| A1 (failed replication) | 0.3 | 0.7 | 0.43 |

### Calculation

```
Prior odds = 0.30 / 0.70 = 0.43
× LR(F1) × LR(F2) × LR(A1) = 0.43 × 3.5 × 2.0 × 0.43
≈ 1.29 (posterior odds)

Posterior probability = 1.29 / (1 + 1.29) ≈ 56%
```

### Posterior
- **P(claim is true) after the evidence:** ~56%
- **Movement from prior:** +26 percentage points
- **Confidence:** medium (close to 50/50, sensitive to LR estimates)

### Sensitivity
- If LR(F1) is revised down to 2.0 → posterior 38%
- If one more failed replication is added → posterior 35%
- This analysis is sensitive — the verdict is robust in the 40-65% range, no wider
```
