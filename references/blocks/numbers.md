<!-- translated from upstream/references/blocks/numbers.md @ e233797 — see docs/TRANSLATION.md -->
# NUMBERS blocks — quantitative data

Blocks for quantitative claims: metrics, market sizing, forecasts, benchmarks.

---

## N1 — `metric-tracker`

**When:** "By metrics", "by KPI", any research with concrete numeric indicators.

**What's inside:** Metrics with numbers, units, time, sources.

**Anti-pattern:** Numbers without units or time — useless. Every number needs context.

**Composition:** Custom for quantitative research. Often combined with `data-table` or `profile-card`.

**Template:**

```markdown
## Metrics

| Metric | Value | Unit | As of | Confidence | Source |
|---|---|---|---|---|---|
| <metric 1> | 1,200 | active users | 2025-Q4 | high | [s03] |
| <metric 2> | $4.5M | ARR | 2025-12 | medium (estimate) | [s07] |
| <metric 3> | 18% | YoY growth | 2024→2025 | high | [s05] |
| <metric 4> | 95ms | P95 latency | benchmark | high | [s11] |
| <metric 5> | 0.4% | conversion rate | 30-day avg | medium | [s14] |

### Metric definitions
- **<metric 1>:** how it's measured, what counts as "active"
- **<metric 2>:** ARR formula used
- **<metric 3>:** methodology of YoY calculation

### Metric quality notes
- <metric 2> is an estimate from public signals, not official
- <metric 5> varies seasonally — the value is an average

### Movement / trends
- <metric 1> grew from N to M over the period
- <metric 5> declining: <hypothesis why>
```

---

## N2 — `market-sizing`

**When:** Market research. When the size of a market must be established.

**What's inside:** TAM/SAM/SOM or another sizing methodology.

**Anti-pattern:** An overly optimistic TAM without justification. Every layer must have top-down and bottom-up validation.

**Composition:** Custom for market analysis. Before `landscape`, for context.

**Template:**

```markdown
## Market sizing

### TAM (Total Addressable Market)
**Value:** ~$<X>B
**Definition:** all potential buyers regardless of reach
**Methodology:** top-down (industry reports) OR bottom-up (users × ARPU)
**Top-down estimate:** [s03] — $X.YB
**Bottom-up estimate:** <calc> — $X.YB
**Convergence:** <if both approaches converge, confidence is higher>
**Confidence:** medium

### SAM (Serviceable Addressable Market)
**Value:** ~$<X>B (X% of TAM)
**Definition:** TAM minus the segments we cannot reach (geography, regulations, etc)
**Excluded:** <segment 1>, <segment 2>
**Confidence:** medium

### SOM (Serviceable Obtainable Market)
**Value:** ~$<X>M (X% of SAM)
**Definition:** the realistically attainable market within <timeframe>
**Reasoning:** <obstacles, competitive constraints>
**Confidence:** low (depends on execution)

### Growth projections
- TAM growing at <X>% YoY [s05]
- SAM expanding via <regulatory change / new tech>
- SOM reachable in <X years>

### Caveats
- "Markets" overlap with adjacent ones — clean delineation is hard
- Top-down reports are often inflated by N% (industry interest)
- Bottom-up relies on multiple assumptions
```

---

## N3 — `growth-rates`

**When:** Growth analysis. YoY / CAGR / MoM.

**What's inside:** Growth rates with ranges and sources.

**Anti-pattern:** A single rate without context (short period? cherry-picked?). Show the time window.

**Composition:** A supplement to `metric-tracker` or `trends`.

**Template:**

```markdown
## Growth rates

### YoY (year-over-year)
| Metric | 2022 | 2023 | 2024 | 2025 | YoY 2024→2025 | Source |
|---|---|---|---|---|---|---|
| Users | 100k | 200k | 350k | 500k | +43% | [s03] |
| Revenue | $1M | $2M | $4M | $7M | +75% | [s07] |
| Margin | 30% | 32% | 35% | 36% | +3pp | [s11] |

### CAGR (compound annual growth rate)
- Users 2022→2025: CAGR = <X%>
- Revenue 2022→2025: CAGR = <Y%>

### Comparison to peers
- Industry avg CAGR (users): <X%>
- Industry avg CAGR (revenue): <Y%>
- This company vs industry: <faster / slower / on par>

### Sustainability
- Is this growth sustainable? <factors>
- Decay signals: <if seen>
- Growth quality: revenue per user growing or flat?
```

---

## N4 — `unit-economics`

**When:** SaaS / business analysis. CAC, LTV, payback period.

**What's inside:** The unit economics formula with numbers.

**Anti-pattern:** Only the LTV/CAC ratio without the time dimension. LTV grows over time, CAC falls — a snapshot misleads.

**Composition:** Custom for product/business analysis. A supplement to `metric-tracker`.

**Template:**

```markdown
## Unit economics

### Customer Acquisition
- **CAC:** $<X>
- **CAC components:**
  - Marketing spend / new customer: $<X>
  - Sales cost / new customer: $<Y>
  - Total CAC: $<Z>
- **CAC payback period:** <N months>
- **Source:** [s07]

### Customer Value
- **Average revenue per user (ARPU):** $<X>/month
- **Average customer lifespan:** <X months>
- **Gross LTV:** $<X> (ARPU × lifespan)
- **Net LTV (with churn-adjusted):** $<X>
- **LTV / CAC ratio:** <X> (healthy: >3, unhealthy: <1)

### Margin
- **Gross margin:** <X>%
- **Net margin:** <Y>%
- **Contribution margin per unit:** $<Z>

### Cohort behavior
- 30-day retention: <X>%
- 90-day retention: <X>%
- 12-month retention: <X>%
- Annual revenue retention: <X>% (negative if expansion > churn)

### Health indicators
- ✅/❌ LTV/CAC > 3
- ✅/❌ CAC payback < 12 months
- ✅/❌ Gross margin > 70% (for SaaS)
- ✅/❌ Net revenue retention > 100%
```

---

## N5 — `cost-breakdown`

**When:** Financial analysis. Due diligence. Understanding structures of costs.

**What's inside:** The cost structure with shares.

**Anti-pattern:** Generic categories without drill-down. If "infrastructure" — what exactly?

**Composition:** Custom for financial. A supplement to `unit-economics`.

**Template:**

```markdown
## Cost breakdown

### Total monthly costs: $<X>

| Category | $/month | % | Notes |
|---|---|---|---|
| Infrastructure | $X | Y% | Cloud + 3rd party APIs |
| Salaries (Eng) | $X | Y% | N FTE × avg $Z |
| Salaries (other) | $X | Y% | Sales, ops, finance |
| Marketing | $X | Y% | Mostly paid acq |
| Office / overhead | $X | Y% | — |
| Software / tools | $X | Y% | — |
| **Total** | **$X** | **100%** | |

### Variable vs fixed
- **Variable** (scales with usage): <X>% — infrastructure, API costs
- **Fixed** (constant): <Y>% — salaries, office, software

### Per-unit cost
- Cost / active user: $<X>
- Cost / transaction: $<Y>
- Cost / new customer (CAC component): $<Z>

### Cost trends
- Last 12 months trend: <category X grew Y%>
- Outlier: <category that's surprising>

### Optimization opportunities
- <category 1>: could reduce <X%> by <action>
- <category 2>: locked in for <reason>

### Source
- [s05] — public filings / leaked deck / estimates
```

---

## N6 — `benchmark-numbers`

**When:** Performance analysis. When industry benchmarks are needed for comparison.

**What's inside:** Industry-wide benchmarks for metrics.

**Anti-pattern:** Stale benchmarks (>2 years). Cherry-picked benchmarks without a range.

**Composition:** A supplement to `metric-tracker` for context.

**Template:**

```markdown
## Industry benchmarks

| Metric | Industry P25 | P50 | P75 | P90 | Best-in-class | Source |
|---|---|---|---|---|---|---|
| Gross margin | 50% | 65% | 75% | 80% | 85%+ | [s07] |
| LTV/CAC | 1.5 | 3.0 | 4.5 | 6.0 | 8.0+ | [s11] |
| Annual churn | 15% | 8% | 4% | 2% | <1% | [s03] |
| Time to PMF | 24mo | 18mo | 12mo | 9mo | <6mo | [s14] |

### Methodology behind benchmarks
- Sample: <type of companies — SaaS B2B, ARR $1-10M, etc>
- N: <how many companies in benchmark>
- Year: <when collected>
- Caveat: <bias of survey responders>

### Where THIS subject sits
- Metric 1: P40 (below median)
- Metric 2: P70 (above median)
- Metric 3: P85 (top quartile)

### Implications
- Metric 1 below median → top priority for improvement
- Metric 3 already best-in-class → don't over-invest, maintain
```

---

## N7 — `forecast`

**When:** Forecasting. Any statement about future values.

**What's inside:** Forecasts with ranges and assumptions.

**Anti-pattern:** A point forecast without an interval ("will be $5M next year"). A forecast is always a range.

**Composition:** Custom for prediction-heavy research. After `growth-rates` or `historical-data`.

**Template:**

```markdown
## Forecast

**Metric:** <what we forecast>
**Horizon:** <e.g. 12 months / 3 years>
**Forecast date:** <YYYY-MM-DD>

### Scenarios

| Scenario | Probability | Value at horizon | Assumptions |
|---|---|---|---|
| Pessimistic | 25% | <X> | <key downside assumptions> |
| Realistic | 50% | <Y> | <baseline assumptions> |
| Optimistic | 25% | <Z> | <key upside assumptions> |

### Methodology
- **Base:** historical CAGR of X% [s07]
- **Adjustments:**
  - Market saturation effect: -Y%
  - New product launches: +Z%
  - Competitive pressure: -W%
- **Final base rate:** <result>

### Key assumptions
- A1: <market continues at current pace>
- A2: <no major regulatory change>
- A3: <key personnel stays>

### Sensitivity analysis
- If A1 fails: <new forecast range>
- If A2 fails (regulation): <new forecast>
- Most fragile assumption: <which>

### Validity / track record
- Past forecasts by same method: hit rate <X%>
- Confidence interval: <how wide>

### When to update forecast
- After Q1 results (recalibrate baseline)
- If <major event> happens
- See `update-triggers`
```

---

## N8 — `historical-data`

**When:** Data analysis, trend research. When a time series is needed.

**What's inside:** A historical time series with the data and the anomalies.

**Anti-pattern:** Only final values without the full series. Specific points in time can show the story.

**Composition:** Before `forecast` or `trends`. A supplement to `metric-tracker`.

**Template:**

```markdown
## Historical data

**Metric:** <what we track>
**Period:** <YYYY-MM to YYYY-MM>
**Frequency:** annual / quarterly / monthly / daily

### Time series

| Period | Value | Notable events | Source |
|---|---|---|---|
| 2020-Q1 | <X> | COVID start | [s03] |
| 2020-Q2 | <Y> | lockdowns | [s03] |
| 2020-Q3 | <X> | reopening | [s05] |
| 2020-Q4 | <X> | — | [s05] |
| 2021-Q1 | <X> | new product launch | [s07] |
| ... | ... | ... | ... |
| 2025-Q4 | <X> | current | [s11] |

### Visualization (ASCII sparkline if simple)

```
Value
  ▲
8 │                              ●
6 │                          ● ● 
4 │                ● ● ● ●
2 │      ● ●  ●  ●
  └─────────────────────────────► time
   '20  '21  '22  '23  '24  '25
```

### Notable events / inflections
- 2020-Q2: drop -X% (COVID effect)
- 2021-Q3: jump +Y% (new product launch)
- 2023-Q1: the plateau began — why: [s07]
- 2024-Q4: recovery — [s11]

### Patterns
- Seasonality: <yes/no, which>
- Cyclicality: <yes/no>
- Trend: <linear / exponential / decay / cyclic>

### Outliers
- 2022-Q3: anomaly — <explanation>
- 2024-Q1: anomaly — <explanation>

### Quality of historical data
- Pre-2020: estimates from secondary sources
- 2020-2022: company-reported, audited
- 2023+: primary public filings
```
