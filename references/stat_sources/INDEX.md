<!-- translated from upstream/references/stat_sources/INDEX.md @ e233797 — see docs/TRANSLATION.md -->
# Stat sources catalog — INDEX

A knowledge base of statistical and informational sources for deepdive. Progressive loading — load only the files you need.

## How to use

1. Read this INDEX (always first).
2. Identify the categories you need — `core/*` or `industries/*`.
3. Load only the files you need — not the whole catalog.
4. In `plan.md` Information sourcing strategy, name the concrete sources.

## Structure

```
stat_sources/
├── INDEX.md                  ← you are here
├── README.md                 ← how to add/update sources
├── core/                     ← cross-industry sources
│   ├── gov_macro.md          government statistics, macro, sentiment, trade, tax
│   ├── companies_public.md   SEC filings, public company data
│   ├── companies_private.md  Crunchbase, startups, local registries
│   ├── consulting_industry.md McKinsey, BCG, Gartner, trade associations
│   ├── consumer_digital.md   apps, web/SaaS, social/creator
│   ├── crypto.md             on-chain, DeFi, crypto markets
│   ├── data_aggregators.md   open data portals
│   ├── media_entertainment.md gaming, film, music
│   ├── health.md             medical, pharma data, public health
│   ├── education.md          schools, rankings, edutech
│   ├── climate_env.md        climate, emissions, env data
│   ├── science.md            citation databases, retractions
│   ├── transport_travel.md   flights, ships, tourism
│   └── sports_fitness.md     sports stats, fitness, esports
└── industries/               ← industry-specific deep dives
    ├── energy.md             EIA, IEA, OPEC, BP
    ├── auto.md               OICA, ACEA, EV sales
    ├── pharma.md             FDA, EMA, clinical trials
    ├── retail.md             NRF, Marketplace Pulse, e-commerce
    ├── manufacturing.md      ISM, NAM, UNIDO
    ├── real_estate.md        CBRE, Zillow, MSCI
    ├── insurance.md          NAIC, EIOPA, Swiss Re Sigma
    ├── banking.md            FDIC, ECB, BIS
    ├── telecom.md            ITU, GSMA, Cloudflare Radar
    ├── logistics.md          WTO Trade, Drewry, FreightWaves
    ├── agriculture.md        FAOSTAT, USDA
    ├── defense.md            SIPRI, Janes
    ├── it_services.md        NASSCOM, ISG, outsourcing
    ├── cybersecurity.md      Verizon DBIR, ENISA, CISA
    ├── advertising.md        IAB, eMarketer, ad spend
    ├── hr_workforce.md       LinkedIn Workforce, BLS, Indeed Hiring Lab
    ├── gig_economy.md        platform work, Online Labour Index
    ├── esg_sustainability.md CDP, SBTi, Climate TRACE
    └── infrastructure.md     public infra, OECD
```

## Which file to read when

### If the research is about macro / country / GDP / inflation
→ `core/gov_macro.md`

### If the research is about a specific public company
→ `core/companies_public.md` (SEC filings, financials)

### If the research is about a startup / privately held company
→ `core/companies_private.md` (Crunchbase, registries)

### If the research is about industry-wide trends, market size
→ `core/consulting_industry.md` + the corresponding `industries/<industry>.md`

### If the research is about apps / SaaS / digital products
→ `core/consumer_digital.md`

### If the research is about a specific industry
→ `industries/<industry>.md` (targeted)

### If the research is about crypto/web3
→ `core/crypto.md`

### If the research is about health/medicine
→ `core/health.md` + (if pharma) `industries/pharma.md`

### If the research is about education
→ `core/education.md`

### If the research is about climate/the environment
→ `core/climate_env.md` + (if sustainability) `industries/esg_sustainability.md`

### If the research is about science / citations / replication
→ `core/science.md`

### If the research is about transport / travel
→ `core/transport_travel.md` + (if logistics) `industries/logistics.md`

### If the research is about sport / fitness
→ `core/sports_fitness.md`

### If the research is about media (film, music, gaming)
→ `core/media_entertainment.md`

### If we are looking for raw datasets for analysis
→ `core/data_aggregators.md`

## Source entry template

Every entry follows this structure:

```markdown
### <Source Name>

**URL:** <main URL>
**Type:** Government | Intergovernmental | Industry Body | Consulting | Vendor | Community | Academic | Self-reported
**Access:** OPEN | PARTIAL (preview free) | PAYWALL with summary | PAYWALL closed

**What's inside:**
- <bullet>

**When to use:**
- Use case 1
- Use case 2

**How to use:**
- Direct: <how to navigate>
- Search pattern: `<query template>`
- Download: <if bulk available>
- API: <if has API>

**Data quality:**
- Credibility: A | B | C
- Freshness: real-time | weekly | monthly | quarterly | annual | irregular
- Lag: <typical delay>
- Methodology: <link or note>

**Limitations:**
- <weakness>
- <bias>

**Combine with:**
- <related complementary sources>

**Fallback if blocked:**
- <alternative>
```

## Statistics

- Categories in core: 14
- Industries: 19
- Total source entries: <!--gen:count:stat_sources-->460<!--/gen-->+
- Sources distribution by access:
  - OPEN: ~190 (68%)
  - PARTIAL: ~70 (25%)
  - PAYWALL with summary: ~20 (7%)

## When to add a new source to the catalog

Not every use requires an addition. Add only if:
- The source will be genuinely useful in ≥2 future research runs
- It covers a gap in the current catalog
- It has a known URL and a data quality assessment

If you use a one-off source for the current research — record it in the research's `sources/NN.md`, not in the catalog.
