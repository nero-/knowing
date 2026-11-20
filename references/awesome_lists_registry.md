<!-- translated from upstream/references/awesome_lists_registry.md @ e233797 — see docs/TRANSLATION.md -->
# Awesome Lists Registry — upstream discovery

## Contents

- Why this is needed
- Tier 1 — Universal APIs/Datasets
- Tier 2 — Specialized
- Tier 3 — Niche / Domain-specific
- Tier 4 — Niche aggregators
- Discovery workflow for the agent
- Limitations awesome-lists
- Future contributions
- Notes on a specific case — the Claude ecosystem

A catalog of upstream awesome-lists on GitHub that the agent turns to when my catalog has no purpose-fit source for a specific subtopic.

## Why this is needed

My catalog (`api_sources/` + `stat_sources/`) is a curated subset. Awesome-lists contain **thousands** of APIs and datasets — it is impossible to curate everything. This registry is a navigation layer:

```
Not found in my catalog → check the registry → find the upstream awesome-list →
  WebFetch their README/categories → identify 1-3 candidates → use ad-hoc
```

This turns the skill from a **closed catalog** into a **discovery hub**.

## Tier 1 — Universal APIs/Datasets

Use first when you are not sure where to look.

### public-apis/public-apis
**URL:** https://github.com/public-apis/public-apis
**What:** 1500+ free public APIs in 48 categories
**Stars:** 418k+ (the best-known API list)
**Categories:** Animals, Anime, Art & Design, Authentication, Books, Business, Calendar, Cloud Storage & File Sharing, Continuous Integration, Currency Exchange, Data Validation, Development, Dictionaries, Documents & Productivity, Email, Entertainment, Environment, Events, Finance, Food & Drink, Games & Comics, Geocoding, Government, Health, Jobs, Machine Learning, Music, News, Open Data, Open Source Projects, Patent, Personality, Phone, Photography, Programming, Science & Math, Security, Shopping, Social, Sports & Fitness, Test Data, Text Analysis, Tracking, Transportation, URL Shorteners, Vehicle, Video, Weather
**When to fetch:** any niche where you do not know the existing APIs
**How:** WebFetch README.md or the specific category section

### awesomedata/awesome-public-datasets
**URL:** https://github.com/awesomedata/awesome-public-datasets
**What:** Curated open datasets across 38 topics
**Stars:** 65k+
**Categories:** Agriculture, Architecture, Biology, Chemistry, Climate+Weather, ComplexNetworks, ComputerNetworks, CyberSecurity, DataChallenges, EarthScience, Economics, Education, Energy, Entertainment, Finance, GIS, Government, Healthcare, ImageProcessing, MachineLearning, Museums, NaturalLanguage, Neuroscience, Physics, ProstateCancer, Psychology+Cognition, PublicDomains, SearchEngines, SocialNetworks, SocialSciences, Software, Sports, TimeSeries, Transportation, eSports
**When to fetch:** you need raw datasets for your own analysis, not API queries
**How:** WebFetch README.md or the specific topic

### jnv/lists — list of lists
**URL:** https://github.com/jnv/lists
**What:** A meta-list — a list of curated lists on GitHub
**Stars:** 25k+
**When to fetch:** when you do not even know which awesome-list to look for
**How:** WebFetch README.md and a keyword search

## Tier 2 — Specialized

Narrowly specialised lists for specific domains.

### Government / Open Data

- **inveniosoftware/awesome-research-data-management** — research data infrastructure
- **r-spatial/awesome-spatial** — geospatial data
- **scienceopen/open-data** — academic open data
- **eligrey/list-of-lists** — datasets meta-list

### Finance / Economics

- **wilsonfreitas/awesome-quant** — quant finance libraries + data
- **dvgodoy/finance-economics-resources** — open finance APIs
- **economagic/data-sources** — economic data

### Science / Academia

- **shaily99/awesome-research** — academic resources
- **openMINDS-projects** — neuroscience-specific
- **inveniosoftware/awesome-research-data-management** — research data tools

### Crypto / Web3

- **bcoin-org/awesome-bitcoin** — Bitcoin specifically
- **crypti/awesome-crypto-papers** — crypto research papers
- **OffcierCia/Crypto-OpSec-SelfGuard-RoadMap** — security focus

### Health / Medical

- **kakoni/awesome-healthcare** — healthcare data and APIs
- **vinta/awesome-python** → Medical section
- **datacarpentry/biology-lesson-collections** — biology

### Tech / Developer

- **sindresorhus/awesome** — meta awesome-of-awesome
- **avelino/awesome-go** — Go ecosystem
- **vinta/awesome-python** — Python ecosystem
- **enaqx/awesome-react** — React ecosystem

### MCP / Agent infrastructure

- **appcypher/awesome-mcp-servers** — MCP servers catalog
- **wong2/awesome-mcp-servers** — alternative MCP list
- **abordage/awesome-mcp** — daily-updated MCP list
- **win4r/Awesome-Claude-MCP-Servers** — Claude-optimized MCP

### Claude ecosystem

- **travisvn/awesome-claude-skills** — Claude Skills (for distributing our skill!)
- **JSONbored/awesome-claude** — Claude registry
- **ComposioHQ/awesome-claude-plugins** — Claude Code plugins
- **rohitg00/awesome-claude-code-toolkit** — toolkit overview

## Tier 3 — Niche / Domain-specific

Narrow but high-quality.

### Geospatial / Maps

- **sacridini/Awesome-Geospatial** — GIS tools
- **rspatial/awesome-spatial** — spatial analysis

### NLP / Linguistic

- **keon/awesome-nlp** — NLP datasets and tools
- **brianspiering/awesome-dl4nlp** — deep learning NLP

### Machine Learning

- **josephmisiti/awesome-machine-learning** — ML resources
- **EthicalML/awesome-production-machine-learning** — ML in production

### Cybersecurity

- **sbilly/awesome-security** — security resources
- **paragonie/awesome-appsec** — application security

### Climate

- **protontypes/open-sustainable-technology** — climate tech
- **mwouts/awesome-jupyter** → climate science section

## Tier 4 — Niche aggregators

Lists that themselves aggregate other lists.

### sindresorhus/awesome
**URL:** https://github.com/sindresorhus/awesome
**What:** The root of all awesome-lists. Master index.
**Stars:** 350k+
**When to fetch:** when you need to find any category of awesome-list and are not sure which one exists
**How:** WebFetch README.md, a keyword search

### awesomelistsio/awesome-apis
**URL:** https://github.com/awesomelistsio/awesome-apis
**What:** Curated list of high-quality APIs, SDKs, dev tools
**When:** for a broad search across multiple domains

### whizkydee/Awesome-APIs
**URL:** https://github.com/whizkydee/Awesome-APIs
**What:** Curated APIs from around the web
**When:** an alternative view of public-apis (less broad)

## Discovery workflow for the agent

```
if my catalog (api_sources/ + stat_sources/) has no category you need:

  1. Determine the domain (finance / health / science / crypto / etc.)
  2. Find the corresponding Tier 1-3 awesome-list in this registry
  3. WebFetch its README.md
  4. Search for keywords from the subtopic
  5. Extract 2-3 candidate APIs/sources
  6. For each one: check the URL is alive (HEAD request)
  7. For the live ones: add to plan.md as ad-hoc:
     - URL
     - tier (open / partial / paywall if clear)
     - the upstream awesome-list source (for credit)
     - note: ad-hoc, not in main catalog yet

  If a candidate proves valuable after use →
     Suggest the contributor add it via PR to the right category of api_sources/ or stat_sources/
```

## Limitations awesome-lists

- **Stale data:** many entries are deprecated and do not work. Always validate the URL before use.
- **No standardization:** each list has its own format — you have to parse it individually.
- **Quality varies:** in `public-apis` there are both top-tier and hobby APIs.
- **Discovery cost:** WebFetch + parsing + validation = time. Use only when my catalog did not cover it.

## Future contributions

When a contributor finds a valuable source in an upstream awesome-list, their PR must contain:

```markdown
## Source discovered in upstream

- Original found in: [public-apis/Business](https://github.com/public-apis/public-apis#business)
- Added to my catalog as: api_sources/companies/example.md
- Reason: stable, free tier, fits gap in my coverage
```

This gives **credit** to the original awesome-list maintainer + encourages ecosystem growth.

## Notes on a specific case — the Claude ecosystem

The lists in the "Claude ecosystem" category are critical for **distributing this skill**:

- Submit deepdive to [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) after the first release
- Submit to [JSONbored/awesome-claude](https://github.com/JSONbored/awesome-claude)
- Submit to [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit)

See PUBLISH.md → Step 6: "Submit to awesome lists" for the procedure.
