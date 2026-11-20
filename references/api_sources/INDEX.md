<!-- translated from upstream/references/api_sources/INDEX.md @ e233797 — see docs/TRANSLATION.md -->
# API sources catalog — INDEX

A catalog of API endpoints for direct programmatic access to data. Complements `stat_sources/` (HTML/web) and `channels.md` (search strategies).

## Why an API when WebFetch exists?

WebFetch fetches an HTML page, the agent parses it. An API returns structured JSON — that is:

- **Structured output** — JSON instead of parsing HTML
- **Bulk queries** — «give me 100 results» in one request, not 100 pages
- **Server-side filtering** — `?industry=fintech&country=US&min_funding=10M`
- **Real-time data** — quotes, on-chain metrics, live feeds
- **Fewer tokens** — JSON is more compact than an HTML page

## When **not** to use an API

- WebFetch HTML already works and the data is sufficient
- A key is needed + you do not have one → use the HTML version of the source
- The free tier is exhausted → fall back to HTML or an alternative source
- A simple one-off lookup → WebSearch is simpler

## Catalog structure

```
api_sources/
├── INDEX.md                    ← navigation (this file)
├── README.md                   ← auth, free tiers, fallback protocol
├── search/                     ← AI/web search APIs
│   ├── brave_search.md         Brave Search API
│   ├── tavily.md               Tavily (AI-first)
│   ├── exa.md                  Exa.ai (semantic)
│   ├── serpapi.md              SerpAPI (Google/Bing/etc)
│   └── you_com.md              You.com Search API
├── academic/                   ← scholarly research
│   ├── semantic_scholar.md     200M papers, no auth
│   ├── openalex.md             250M works, no auth
│   ├── crossref.md             130M DOIs, no auth
│   └── arxiv.md                preprints, no auth
├── financial/                  ← economic / macro
│   ├── fred.md                 FRED (Fed economic data)
│   ├── world_bank.md           World Bank Indicators
│   ├── sec_edgar.md            SEC EDGAR filings
│   ├── oecd.md                 OECD SDMX
│   └── alpha_vantage.md        Stocks/forex/crypto prices
├── companies/                  ← company data
│   ├── crunchbase.md           Crunchbase Data API (⚠️ paid, price not published)
│   ├── opencorporates.md       OpenCorporates (⚠️ paid from £2250/year)
│   └── companies_house.md      UK Companies House
├── crypto/                     ← on-chain & markets
│   ├── coingecko.md            CoinGecko Public API
│   ├── defillama.md            DefiLlama (no auth)
│   ├── etherscan.md            Etherscan API
│   └── dune.md                 Dune Analytics
├── code/                       ← code / packages
│   ├── github.md               GitHub Search API
│   ├── stackexchange.md        Stack Exchange API
│   ├── pypi.md                 PyPI JSON API
│   └── npm.md                  npm Registry API
├── social/                     ← community signals
│   ├── reddit.md               Reddit JSON (⚠️ OAuth mandatory since 2026, not free — see the file)
│   ├── hn_algolia.md           HN Algolia (no auth)
│   └── lemmy.md                Lemmy ActivityPub
├── news/                       ← current events
│   ├── newsapi.md              NewsAPI.org
│   ├── gdelt.md                GDELT 2.0 (no auth)
│   └── currents.md             Currents API
├── stats/                      ← statistics
│   ├── eurostat.md             Eurostat REST API
│   ├── census_us.md            US Census API
│   └── un_data.md              UN Data API
├── patents/                    ← patent offices
│   ├── uspto_odp.md            USPTO Open Data Portal (key + ID.me)
│   ├── epo_ops.md              EPO OPS (OAuth2, 4 GB/week free)
│   ├── epo_lod.md              EPO Linked Open Data (SPARQL, no auth)
│   └── wipo.md                 WIPO — paid, there is no free programmatic API
├── grants/                     ← research funding
│   ├── nsf_awards.md           NSF Awards (no auth)
│   ├── nih_reporter.md         NIH RePORTER v2 (no auth, POST-only)
│   ├── cordis.md               CORDIS EU projects (bulk + SPARQL)
│   └── grants_gov.md           Grants.gov search2 (no auth)
└── domain_specific/            ← specialized
    ├── pubmed.md               PubMed E-utilities
    ├── clinicaltrials.md       ClinicalTrials.gov
    ├── ema.md                  European Medicines Agency
    ├── nasa.md                 NASA APIs
    └── openweather.md          OpenWeather
```

## Quick reference

### Free, no key required (priority sources for agents)

These APIs need no keys — the agent can use them right away:

| API | What | When |
|---|---|---|
| **Semantic Scholar** | 200M papers, citations | academic search |
| **OpenAlex** | 250M scholarly works (the key is optional but recommended — 10× budget; see `academic/openalex.md`) | citation graph |
| **CrossRef** | 130M DOIs | DOI metadata |
| **arXiv** | preprints | physics/CS/math papers |
| **DefiLlama** | DeFi TVL/protocols | crypto research |
| **CoinGecko** | crypto prices/markets | crypto data (rate-limited) |
| **HN Algolia** | Hacker News search | tech discussions |
| **World Bank** | global development | macro stats |
| **SEC EDGAR** | US public filings | company financials |
| **ClinicalTrials.gov** | trial registry | medical research |
| **PubMed E-utilities** | biomedical literature | medical search |
| **GDELT** | global events | news/sentiment |
| **PyPI / npm** | package metadata | tech stack research |
| **NSF Awards** | US research grants since 1969 | who funds the topic, the amounts |
| **NIH RePORTER** | NIH biomedical grants since FY1985 | funding for medical topics |
| **Grants.gov** | open US federal competitions | future opportunities, not yet awarded |
| **EPO Linked Open Data** | patent publications, SPARQL | patent activity without a key |

### Free with key (one-time setup, then automatic)

| API | Free tier | Setup |
|---|---|---|
| **FRED** | unlimited | https://fred.stlouisfed.org/docs/api/api_key.html |
| **USPTO ODP** | 5M calls/week metadata, 1.2M documents | https://developer.uspto.gov (an ID.me-verified account is required) |
| **EPO OPS** | 4 GB/week, ~1 Mbit/sec | https://developers.epo.org (OAuth2 client_credentials) |
| **GitHub** | 5000 req/h authenticated | https://github.com/settings/tokens |
| **Stack Exchange** | 10000 req/day | https://stackapps.com/apps/oauth/register |
| **NewsAPI** | 100 req/day | https://newsapi.org/register |
| **Alpha Vantage** | 25 req/day | https://www.alphavantage.co/support/#api-key |
| **Etherscan** | 5 req/sec | https://etherscan.io/myapikey |
| **Reddit JSON (OAuth)** | not confirmed as of 2026-08-17 — anonymous `.json` is closed (403, live-verified ~05.2026); the issuance of new OAuth script apps has narrowed, the real limit for personal use is not confirmed | https://www.reddit.com/prefs/apps → `REDDIT_CLIENT_ID`/`REDDIT_CLIENT_SECRET`, see `social/reddit.md` |

### Paid (powerful but cost money)

| API | Cost | Why pay |
|---|---|---|
| **Brave Search** | $3/1k queries | Google-quality, no bias toward Google products |
| **Tavily** | $0/1k free, then paid | Built for AI agents, returns answers |
| **Exa.ai** | $5/1k searches | Semantic search, neural |
| **SerpAPI** | $50/mo | Google/Bing/DuckDuckGo unified |
| **Crunchbase** | price not published, custom/contact-sales (the old figure "$99/mo" was not confirmed as of 2026-08-17, see `companies/crunchbase.md`) | Company data, funding rounds |
| **OpenCorporates** | from £2250/year (Essentials); free access on application for journalists/NGO/anti-corruption groups | Company registry data, 130+ countries |
| **WIPO** | 600–2000 CHF/year SOAP, 400–19500 CHF/year bulk | there is no free programmatic access at all; the web UI serves a CAPTCHA |

**Dead, do not waste time:** `search.patentsview.org` — the service shut down on 20.03.2026, the domain does not resolve; the data moved to USPTO ODP bulk. Details — `patents/uspto_odp.md`, the Fallback section.

## How to navigate this catalog

1. **Identify your need:** what kind of data — papers, prices, filings, social signals?
2. **Pick category folder** (search/academic/financial/...)
3. **Read the relevant API file** — each has full reference: endpoint, auth, free tier, query examples
4. **Use the example queries** as templates in your research
5. **Document API call** in your `sources/NN.md` frontmatter (`channel: api-direct`, `access: api-free-no-key`)

## See also

- `channels.md` → channel **`api-direct`** — the strategy for using APIs in the workflow
- `stat_sources/` → the HTML/web version of the same sources (for fallback when the API does not work)
- `subagents_v2.md` → how to give sub-agents instructions on API queries
