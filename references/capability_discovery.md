<!-- translated from upstream/references/capability_discovery.md @ e233797 — see docs/TRANSLATION.md -->
# Capability Discovery — Phase 3.5

## Contents

- Why the phase exists
- The phase's workflow
- When the phase is optional / mandatory
- The phase's output
- Anti-patterns
- Relation to other phases
- Phase 3.5 checklist

A phase between Plan (3) and Search (4). Optional for shallow, **recommended** for medium, **mandatory** for deep.

## Why the phase exists

After plan.md has been written with the Information sourcing strategy (section 12), the skill knows:
- Which channels will be used
- Which stat sources and API endpoints are planned

**But it does not know:**
- Which API keys are actually available in the environment (env vars)
- Which APIs are alive / deprecated / rate-limited right now
- Whether the planned sources cover all the needed subtopics

Capability Discovery closes this gap. **Transparency for the user:** what is used, what is skipped, what would be worth configuring.

**The second search engine.** One engine = one search trajectory — the conformism that the triangulation rule forbids for sources and must forbid for the search channel itself. If the env has `BRAVE_SEARCH_API_KEY`, `TAVILY_API_KEY`, `EXA_API_KEY` or `FIRECRAWL_API_KEY` — at medium/deep Phase 4 is obliged to allocate one search axis to it via `scripts/search_query.py --engine auto --qclass <qclass> --query "..."`, in parallel with the harness's regular WebSearch. The overlap of results between engines is recorded as `overlap_rate` in `plan.md` §15 (low overlap is a signal that the second engine really extends coverage, not duplicates the first).

## The phase's workflow

### Step 1: Audit env vars

The skill checks the existence of env vars for the API keys of the planned APIs:

```bash
# Check known env vars
if env $FRED_API_KEY exists → mark FRED as 'authenticated'
if env $GITHUB_TOKEN exists → mark GitHub as 'authenticated'
# ...
```

Supported env vars (see the full list in `api_sources/README.md`):

| Env var | API | Required? |
|---|---|---|
| `FRED_API_KEY` | FRED economic data | optional (an HTML fallback exists) |
| `GITHUB_TOKEN` | GitHub Search | optional (60/h without, 5000/h with) |
| `BRAVE_SEARCH_API_KEY` | Brave Search | the second search engine, mandatory for one Phase 4 axis if the key exists |
| `TAVILY_API_KEY` | Tavily | the second search engine, mandatory for one Phase 4 axis if the key exists |
| `EXA_API_KEY` | Exa.ai | the second search engine, mandatory for one Phase 4 axis if the key exists |
| `FIRECRAWL_API_KEY` | Firecrawl | the second search engine, mandatory for one Phase 4 axis if the key exists |
| `SERPAPI_KEY` | SerpAPI | **not used** — paid, no free tier |
| `NEWSAPI_KEY` | NewsAPI | for news |
| `ALPHA_VANTAGE_KEY` | Alpha Vantage | for stock prices |
| `CRUNCHBASE_API_KEY` | Crunchbase | for company data |
| `OPENWEATHER_KEY` | OpenWeather | for weather |
| `ETHERSCAN_KEY` | Etherscan | for on-chain |
| `STACKEXCHANGE_KEY` | Stack Exchange | for programming Q&A |
| `CENSUS_API_KEY` | US Census | for US demographics |
| `COMPANIES_HOUSE_API_KEY` | Companies House UK | for UK registry |
| `NCBI_API_KEY` | PubMed | optional (raises the rate limit) |
| `SEMANTIC_SCHOLAR_API_KEY` | Semantic Scholar | optional |
| `DUNE_API_KEY` | Dune Analytics | for custom on-chain SQL |
| `NASA_API_KEY` | NASA APIs | (DEMO_KEY works) |

### Step 2: Map subtopics to capabilities

For each subtopic from plan.md → a capabilities table:

```markdown
### ST1: <subtopic name>

| Planned source | Status | Notes |
|---|---|---|
| FRED API (macro context) | ✅ authenticated | $FRED_API_KEY is present |
| Semantic Scholar (academic) | ✅ open-no-auth | works without a key |
| Brave Search (search) | ⚠ fallback | $BRAVE_API_KEY absent → standard WebSearch |
| Crunchbase (companies) | ❌ unavailable | paid, no key → competitive-signals HTML |
| Industry-specific (X) | ❓ to discover | look in the upstream awesome-lists |
```

### Step 3: Discovery for unknown gaps

If the planned subtopic is not covered by the known sources — the skill goes into **awesome_lists_registry.md** and looks for a purpose-fit upstream.

Algorithm:
1. Extract keywords from the subtopic (e.g., "fashion industry market data")
2. List the relevant awesome-lists from the registry (for example, `public-apis`, `awesome-public-datasets`)
3. WebFetch their README.md or a specific category
4. Find 1-3 candidate APIs/datasets
5. Extract the base URL and the docs URL
6. Add to plan.md as `ad-hoc:` sources (they are not saved into the catalog automatically)

Example:

```markdown
ST3: fashion industry market sizing

Found no fit in my catalog → searched upstream:
- public-apis/Books → no
- public-apis/Business → Lyst API (limited docs), ShopStyle Collective
- awesome-public-datasets/Economics → no fashion specifics

Choose: Lyst API (for market activity), Vogue Business RSS (for trend signals)
Mark as ad-hoc, not in catalog — a contributor can add it to `api_sources/fashion/` via a PR.
```

### Step 4: Report to user

The final output of phase 3.5 — a compact summary report to the user:

```
Capability Discovery complete:

✅ Available (with auth):
  FRED, GitHub, Semantic Scholar, OpenAlex, DefiLlama, Reddit JSON, PubMed, ClinicalTrials.gov

⚠ Fallback to HTML (no key):
  Brave Search → standard WebSearch
  Crunchbase → competitive-signals (LinkedIn/Glassdoor scraping)

❌ Not available:
  Tavily, Exa, Alpha Vantage — paid only

❓ Ad-hoc (from upstream awesome-lists):
  Lyst API, Vogue Business RSS — for the fashion industry subtopic

To improve coverage next time, configure these env vars:
  export ALPHA_VANTAGE_KEY=... (25 free/day)

Continue with current capabilities? [Y/n]
```

The user can:
- Agree → move on to Search (Phase 4)
- Decline → a pause to configure the keys → re-run discovery
- Specify additional sources by hand

## When the phase is optional / mandatory

| Depth | Phase 3.5 | Notes |
|---|---|---|
| shallow | optional | if the topic is simple, the agent falls back itself |
| medium | recommended | a meaningful increase in transparency |
| deep | mandatory | without discovery there is a risk of missing key sources |

## The phase's output

Capability Discovery supplements `plan.md` section 12 (Information sourcing strategy) with a new sub-block per subtopic:

```markdown
## 12. Information sourcing strategy

### ST1: <subtopic>

**Channels:** web-general, academic, api-direct
**Stat sources:** core/gov_macro.md, core/science.md

**Capabilities check (Phase 3.5):**
- ✅ FRED API: authenticated, will use directly
- ✅ Semantic Scholar API: open access, will use directly
- ⚠ Brave Search: no key → fallback to standard WebSearch
- ❓ Niche topic — searching upstream...

**Decision:** proceed with available; ad-hoc add Lyst API for ST3.
```

## Anti-patterns

- ❌ Asking the user for API keys inline — ask them to add it to the env and restart
- ❌ Saving someone else's keys into the catalog's files
- ❌ Using a paid API without checking that the key is available
- ❌ Using ad-hoc upstream APIs as a single source (triangulation is needed as usual)
- ❌ Doing phase 3.5 in shallow mode when the topic is simple — overkill

## Relation to other phases

- **Phase 3 (Plan):** sets plan.md → section 12 sourcing strategy
- **Phase 3.5 (Capability Discovery):** supplements section 12 with the capabilities check
- **Phase 4 (Search):** uses only confirmed capabilities + ad-hoc upstream finds
- **Phase 5 (Score):** `sources/NN.md` records the `access:` field with the real method (api-direct / html-fallback / ad-hoc-upstream)

## Phase 3.5 checklist

- [ ] Env vars checked for all planned APIs
- [ ] The status of each API recorded (authenticated / fallback / unavailable)
- [ ] Gaps in the catalog identified — discovery via upstream awesome-lists carried out
- [ ] The summary report shown to the user
- [ ] Plan.md section 12 supplemented with the Capabilities check block
- [ ] User confirmation received (or an explicit agreement "continue")
