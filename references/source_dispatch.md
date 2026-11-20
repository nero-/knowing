<!-- translated from upstream/references/source_dispatch.md @ e233797 — see docs/TRANSLATION.md -->
# Source Dispatch — how to choose channels and sources for a subquestion

## Contents

- Principles
- Matrix: typical subquestion → channels
- Registry-first: numbers are not fetched from the web
- Registry — vetted addresses per signal
- Discovery patterns — when the catalog is not enough
- Decomposition recipes — typical topic decompositions
- When to go into repositories explicitly
- Output: what to record in plan.md
- Prior when choosing a channel beyond the mandatory minimum
- Anti-patterns

**When it is used:** at the start of Phase 4 (Search). Once `plan.md` is ready and the subquestions are decomposed — for **each subquestion** you run it through this file and write the dispatch decision into plan.md section 12 «Information sourcing strategy».

**What it does:** turns a subquestion («what is X's market share in the EU») into an **ordered list of channels and concrete sources**: primary → secondary → fallback. Without this, Claude guesses anew every time «where to get the data from».

---

## Principles

1. **The source is chosen for the subquestion, not for the whole topic.** The topic «vertical farming market in EU» is decomposed into 5-8 subquestions, and each gets its own dispatch.
2. **Every subquestion → at least 2 channels of different types** (the triangulation requirement from Phase 5). One channel alone — that is already a flag for the adversarial pass.
3. **Primary = expected to be the strongest on credibility/recency.** Secondary = independent verification. Fallback = if primary is unavailable.
4. **Open APIs > HTML scraping.** If there is an API from `api_sources/` for the subquestion — it is primary. HTML only if there is no API.
5. **Awesome-lists and repositories are discovery, not a finite catalog.** Use them when your catalog does not cover the topic (see the «Discovery patterns» section below).

---

## Matrix: typical subquestion → channels

Signals in the subquestion → primary/secondary/fallback channels. Channels from `channels.md`, concrete APIs from `api_sources/`, stats from `stat_sources/`.

| Signal in the subquestion | Primary channel | Secondary | Fallback |
|---|---|---|---|
| «market size of X», «market size» | `industry-reports` (Statista alt, IBISWorld free, McKinsey/BCG/Bain public reports) | `data-statistical-gov` (FRED, World Bank, Eurostat industry codes) | `web-general` + `competitive-signals` (top players' annual reports) |
| «trend of X over time», «time series» | `api-direct` (FRED, World Bank, OECD, Eurostat) | `data-statistical-gov` (national stat sites) | `news-current` (GDELT for a qualitative chronology) |
| «is X true from a scientific standpoint» | `academic` (OpenAlex, Semantic Scholar) + `preprint-servers` (arXiv, bioRxiv, medRxiv, SSRN) | Cochrane reviews + Crossref for citations | `web-general` for pop science |
| «who the players are in X space» | `competitive-signals` (Crunchbase, OpenCorporates, Companies House) | `code-github` (for tech) + `industry-reports` | `forum-discussion` (Reddit, HN — community knowledge about the players) |
| «X in country Y» | `data-statistical-gov` of country Y (national statistics, central bank) | `api-direct` (World Bank, IMF, OECD by country code) | `news-current` + local press |
| «how X works technically» | `code-github` (reference implementations) + `academic` (foundational papers) | `forum-discussion` (Stack Exchange, technical blogs) | `web-general` (docs of official products) |
| «recent changes in X», «recent» | `news-current` (NewsAPI, GDELT, Currents) + `industry-reports` | `forum-discussion` (Reddit, HN — news discussions) | `api-direct` regulatory feeds |
| «regulation of X in jurisdiction Y» | `regulatory-legal` (country Y's regulator, EUR-Lex for the EU, CFR for the US) | `news-current` (legal press, Law360, Reuters Legal) | `academic` (legal scholarship) |
| «performance of X», «benchmark» | `code-github` (paperswithcode, lmarena, leaderboards) + `academic` | `forum-discussion` (HN threads, Reddit r/MachineLearning, ML twitter) | `news-current` |
| «sentiment / public opinion» | `forum-discussion` (Reddit, HN Algolia, Twitter API) | `news-current` + `competitive-signals` (reviews aggregators) | Survey data via `data-statistical-gov` (Pew, Eurobarometer) |
| «adoption / usage data» | `product-analytics` (SimilarWeb, App Annie, Sensor Tower public data) | `code-github` (for open-source — stars/downloads via PyPI/npm stats) | `industry-reports` |
| «price / cost of X», pricing | official sites + `web-general` | `competitive-signals` (price comparison sites) | `forum-discussion` (reddit threads about pricing) |
| «crypto/DeFi project X» | `crypto-analytics` (DefiLlama, Etherscan, Dune) + `api-direct` (CoinGecko) | `code-github` (the project's repo + audits) | `forum-discussion` (Crypto Twitter, r/cryptocurrency, governance forums) |
| «health/clinical X» | `domain-specific` (PubMed, ClinicalTrials.gov, EMA) | `academic` (Cochrane, OpenAlex) | `news-current` (medical press, STAT, Endpoints) |
| «environmental / climate X» | `data-statistical-gov` (NASA, NOAA, ESA, Copernicus, IEA) | `academic` (Nature, Science) + `api-direct` (OpenWeather) | `news-current` (climate journalism) |
| «job market / hiring X» | `data-statistical-gov` (BLS, Eurostat labor) | `competitive-signals` (LinkedIn — HTML, Glassdoor) | `industry-reports` (HR firms — Korn Ferry, Mercer) |
| «philosophical / qualitative / framework» | `academic` + `web-general` (long-form essays — substack, blogs, books online) | `forum-discussion` (LessWrong, Marginal Revolution, philosopher's stone) | own community archives |

**A second search engine as a separate axis.** If the env has `BRAVE_SEARCH_API_KEY` / `TAVILY_API_KEY` / `EXA_API_KEY` / `FIRECRAWL_API_KEY` (see `capability_discovery.md`) — regardless of the matrix row, add a `search-engine-2` axis via `scripts/search_query.py --engine auto --qclass <subquestion qclass> --query "..."`, in addition to the harness `web-general`/WebSearch. This is not a replacement for the Primary/Secondary from the matrix but an additional independent search trajectory; the overlap with WebSearch is written to `plan.md` §15 as `overlap_rate`.

**Which engine `--engine auto` takes:** the first one with a key from the order for the `qclass` (`ENGINE_ROUTES` in `search_query.py`). Scientific and conceptual classes start with exa, fresh ones (`recent-change`, `sentiment`, `crypto`) with tavily → brave, factual ones with tavily → exa. The choice is printed to stderr; write it into §12. For sources from this axis set the channel `search-engine-2/<engine>` in `discovery_path` (it is printed there too): the swarm post-processing uses it to count each engine's yield, and once there is statistics per class, `auto` picks the engine by priors rather than by the table.

**If the subquestion does not match** any row — act by default: `web-general` + `academic` + `news-current` at minimum. And **immediately write into plan.md section 12 that the dispatch was ad-hoc** — this is a signal for Phase 6 (adversarial) that the coverage may have been weak.

---

## Registry-first: numbers are not fetched from the web

**Rule.** The subquestion is quantitative (the answer is a number: size, share, price, rate, deadline)
⇒ **the primary channel must be `api-direct` or `data-statistical-gov`**, that is
a registry, a dataset, reporting. A web article with a number cannot be the root of the number — it is
a pointer to the root.

Note: two rows of the matrix above currently contradict this rule —
«market size of X» leads to `industry-reports`, «price / cost of X» to `web-general`.
For a quantitative formulation the rule overrides the matrix: the registry is searched first,
the industry report comes second.

**Why.** It is cheaper not to generate garbage at the input than to filter it at the output. Web search
returns the SEO top, and numbers there live a life of their own: market sizing from firms that sell
reports; «74% of companies...» from a 2011 presentation whose primary source is dead;
a vendor benchmark retold by four publications. Neither `recency` nor `bias` catches them —
a fresh reprint has honest ratings on both scales.

**How to execute it at step 4.0:**

1. Mark each subquestion: quantitative / qualitative.
2. For a quantitative one — check coverage in `stat_sources/INDEX.md` and
   `api_sources/INDEX.md` BEFORE assigning channels. If you found an endpoint — it is primary, the web
   goes to fallback.
3. Write the concrete endpoint into `plan.md` §12 (not «FRED», but the series), so that the sub-agent
   does not look it up again.
4. No coverage — say so: «metric M is not covered by a registry, we take it from secondary sources,
   `origin_kind: secondary`». This is an honest result, it must be visible and not
   masked by a confident number.

**It is checked by machine.** A number that got into the findings from a web source while a
covering endpoint exists is a discipline defect, not a matter of taste:
`scripts/check_number_provenance.py` will flag the source by `origin_kind`/`chain_len`, and
the fail-closed rule will not let such a number into `memo.md`.

**Anti-pattern:** take a number from an article, then «confirm» it with three other
articles. That is not triangulation but a print run of one root — the `≥2 roots` rule and the circulation
detector catch exactly this case.

---

## Registry — vetted addresses per signal

`references/registry/` — 1072 addresses with an access mark (free / key / User-Agent) by signal type: science, regulatory (parliamentary APIs), markets, technology, security, climate_health, society, registries, open_source_releases. If you need a fresh stream or a direct endpoint that is not in `api_sources/` — open ONE file by topic, not the INDEX. The reliability in the table is a reconnaissance mark, not a Phase 5.5 result; the list's shelf life is months, and a dead address is cured by the usual fallback.

## Discovery patterns — when the catalog is not enough

The catalog `stat_sources/` + `api_sources/` + `registry/` covers the basic domains, but **rare topics** (niche industries, esoteric academic fields, region-specific topics) require searching for *new sources* at runtime. The algorithm:

### 1. GitHub topic search
```
https://github.com/topics/<keyword>
https://github.com/search?q=topic:<keyword>+sort:stars
```
**Why:** To find:
- `awesome-<keyword>` repositories — curated source lists
- Open-source datasets on the topic
- Tools/libraries (which means there is an API or an ETL pipeline)

**Example:** the topic «satellite imagery» → `github.com/topics/satellite-imagery` → `awesome-satellite-imagery-datasets` → 30+ dataset links that are not in our catalog.

### 2. Awesome-lists registry
`references/awesome_lists_registry.md` already contains 25+ curated lists. **In Phase 4, first thing**, check it for the topic:
- Tier 1: `public-apis`, `awesome-public-datasets` (universal)
- Tier 2: specialized by domain (finance, science, crypto, health)
- Tier 3-4: niche and aggregators

### 3. HuggingFace + Kaggle datasets
```
https://huggingface.co/datasets?search=<topic>
https://www.kaggle.com/datasets?search=<topic>
```
**Why:** Ready-made datasets for ML/analysis. They often contain already cleaned data + source metadata.

### 4. PyPI / npm / crates search
```
https://pypi.org/search/?q=<topic>
https://www.npmjs.com/search?q=<topic>
```
**Why:** Libraries often:
- Wrap someone else's API → which means there is an API
- Include bundled datasets
- Document where to get the data

**Example:** the topic «satellite imagery» → PyPI search `satellite` → `sentinelsat` → Copernicus Open Access Hub API.

### 5. Data portals (government / EU)
- `data.gov` — US federal datasets
- `data.europa.eu` — EU open data portal
- `data.gouv.fr`, `data.gov.uk` and other national ones
- `data.worldbank.org/data-catalog` — the full WB catalog

**Why:** Authoritative sources for government statistics, regulatory data, demographics.

### 6. Academic dataset registries
- `datadryad.org` — research datasets
- `zenodo.org` — multi-domain scientific datasets
- `figshare.com` — supplementary data for articles
- `re3data.org` — registry of research data repositories

**Why:** If the topic is academic and you need the underlying data behind the articles.

### 7. Industry-specific registries
As needed — sector-specific ones:
- Healthcare: NIH BioLINCC, GHDx, IHME
- Finance: BIS, IMF datamapper, FSB
- Climate: NASA NEX, NOAA Climate Data Online, IEA datasets
- Crypto: Dune dashboards, Messari, Glassnode (paid)

If the topic is narrow — ask the USER whether they have a hint.

---

## Decomposition recipes — typical topic decompositions

Not every subquestion is visible from the wording. These recipes are **typical splits of large topics**, so as to obtain the full set of subquestions before the dispatch.

### «Market analysis of X»
1. **Size & growth** → industry-reports + gov_macro
2. **Segmentation** → industry-reports + competitive-signals
3. **Top players** → competitive-signals (Crunchbase/OpenCorporates) + code-github if tech
4. **Recent news / events** → news-current (NewsAPI/GDELT last 6mo)
5. **Academic context** → academic on underlying tech/practice
6. **Consumer sentiment** → forum-discussion (Reddit, HN) if consumer-facing
7. **Regulatory landscape** → regulatory-legal per relevant jurisdictions
8. **Forecasts** → industry-reports + especially mention which analyst houses cover it (Gartner, IDC, Forrester)

### «Is X true / does X work»
1. **Foundational claim** → academic (peer-reviewed)
2. **Systematic reviews / meta-analyses** → Cochrane, PROSPERO
3. **Counter-evidence / replication failures** → preprint-servers, retraction-watch
4. **Real-world adoption / case studies** → industry-reports, code-github if a tool
5. **Critics / sceptics** → academic critiques + forum-discussion (LessWrong, EA forum)
6. **Mechanism / how it would work** → academic + technical blogs

### «How does X work»
1. **Reference paper / original source** → academic
2. **Implementations / code** → code-github (paperswithcode, official repos)
3. **Tutorials & explanations** → web-general (long-form blogs) + forum-discussion
4. **Variations / extensions** → academic + preprint-servers (recent papers cite original)
5. **Limitations / failure modes** → forum-discussion + adversarial paper search
6. **Benchmarks / performance** → code-github (leaderboards) + academic

### «Should I do X» (decision genre)
1. **What does X actually involve** → web-general (vendor docs) + academic if there is any
2. **Cost / ROI** → industry-reports + forum-discussion (real practitioners)
3. **Risk factors** → academic on failure modes + news-current (recent failures)
4. **Alternatives** → competitive-signals + academic comparisons
5. **Who's done it (case studies)** → industry-reports + competitive-signals
6. **What experts say** → academic + people-focused (specific authorities)
7. **Counter-arguments** → critical sources, forum-discussion (skeptics)

### «Landscape: who's in X space»
1. **Top by market share / revenue** → industry-reports + competitive-signals
2. **Top by funding / valuation** → competitive-signals (Crunchbase)
3. **Top by tech / academic citations** → academic + code-github
4. **Recent entrants** → competitive-signals (Crunchbase recent) + news-current
5. **Dying / exiting** → news-current (acquisitions, shutdowns) + competitive-signals
6. **Open-source ecosystem** → code-github (topics, awesome-lists)
7. **Geographic distribution** → industry-reports + national stat sources per region

### «Validation: is it true that [claim]»
1. **Original source of claim** → find the primary source in news/academic/blogs
2. **Primary evidence** → academic + data-statistical-gov
3. **Counter-evidence** → academic critiques + retracted-papers DB
4. **Independent replication** → preprint-servers + academic
5. **Who else makes this claim** → web-general (citation chain)
6. **Who disputes it and why** → forum-discussion + academic adversarial
7. **What it would take to falsify** → reasoning + academic methodology

---

## When to go into repositories explicitly

The `code-github` source via `WebFetch` or the GitHub API (`GITHUB_TOKEN` if present) is primary in these cases:

1. **The topic mentions a technical instrument:** «open source», «library», «framework», «protocol», «standard»
2. **«How X works» where X is an algorithm/practice:** there is a high probability that a reference implementation exists
3. **Searching for datasets:** `topic:dataset`, `topic:open-data`, `topic:public-data`
4. **Searching for curated lists:** `awesome-<topic>` repo naming convention
5. **Benchmarks:** `topic:benchmark`, `topic:leaderboard`
6. **Implementations of academic papers:** add `paperswithcode` or search for a repo with the paper's title

What to look for in the repository:
- **README** — description, purpose, datasets used, methodology
- **stars + recent commits** — a proxy for quality and activity (Phase 5 scoring)
- **issues** — known problems, edge cases, what does not work (optional for adversarial)
- **discussions / wiki** — best practices, FAQ
- **CITATION.cff** or `papers/` — formal references to the papers

**Do not go into a repo just for the sake of it.** Only if you expect data or code there that is relevant to the subquestion.

---

## Output: what to record in plan.md

Once all subquestions have been run through this file — fill in section 12 of plan.md in this format:

### The `qclass` field

Each subquestion gets a `qclass` — the class by which channel
yield statistics accumulate. It is set together with the dispatch decision, written into §12 next to the channels:

`market-size` · `time-series` · `scientific-claim` · `players` · `country-stat` ·
`how-it-works` · `recent-change` · `regulation` · `benchmark` · `sentiment` ·
`adoption` · `pricing` · `crypto` · `health` · `climate` · `jobs` · `qualitative`

The class corresponds to a row of the matrix above. A subquestion that falls into no row
gets `qclass: qualitative` and is marked as ad-hoc — as it is now.

The line format in §12:

- **qclass:** `market-size`

```markdown
## 12. Information sourcing strategy

### Subquestion Q1: «What's the EU vertical farming market size and growth rate?»
- **Primary:** industry-reports → search "EU vertical farming market" agri-tech analyst houses (AgFunder, Plenty/Infarm public summaries)
- **Secondary:** data-statistical-gov → Eurostat agricultural production NACE codes A.01 for greenhouse/protected cultivation
- **Fallback:** web-general → top EU vertical farming company annual reports (Infarm, Jungle, Nordic Harvest)
- **Decomposition note:** classic «market analysis» recipe — adding Q1b «top EU players» and Q1c «forecast 2025-2030»

### Subquestion Q2: «Is vertical farming economically viable at scale?»
- **Primary:** academic → OpenAlex + Semantic Scholar with API key, "controlled environment agriculture" reviews
- **Secondary:** industry-reports → unit economics analyses from AgFunder Network, McKinsey AgTech
- **Fallback:** forum-discussion → r/verticalfarming, AgTech Twitter, conference proceedings (Indoor Ag-Con)
- **Adversarial pre-flag:** bankruptcies (Infarm 2024 restructuring, AeroFarms Chapter 11), failure-mode papers

### Subquestion Q3: «What's the regulatory status of vertical farming across EU member states?»
- **Primary:** regulatory-legal → EUR-Lex CAP (Common Agricultural Policy) on controlled environment, EFSA food safety guidance
- **Secondary:** per-country → national agriculture ministries (BMEL Germany, MASAF Italy, DEFRA UK for post-Brexit context)
- **Fallback:** news-current → Reuters Sustainability, Politico EU on AgTech policy

### Discovery executed:
- ✓ Checked awesome_lists_registry → found `awesome-agtech` and `awesome-agriculture` (Tier 2)
- ✓ GitHub topic search `topic:vertical-farming` → 8 datasets, 2 with EU focus
- ✓ HuggingFace datasets search → 1 controlled-environment-agriculture dataset

### Gaps noted:
- No EU-wide vertical-farming production tracker — accepting industry-report estimates with caveat
- No real-time regulatory feed — manual check per member state needed
```

**This is the deliverable** of the Source Dispatch step. Without it, Phase 4 is chaotic search.

---

## Prior when choosing a channel beyond the mandatory minimum

Primary and Secondary from the matrix above are the mandatory part of coverage. That part holds
triangulation (≥2 channels of different types) and is never moved by a prior: ignoring
the matrix in favor of «the channel with the best statistics» is a way to quietly break the independence
of sources.

**When the question of an additional channel arises** — and not of replacing Primary/Secondary:
depth=deep requires broader coverage of the subquestion · a deviation trigger fired
(`unexpected_finding`/`contradiction`, see Phase 4 in `SKILL.md`) and one more
round is needed · the Fallback from the matrix looks like a weak option for this particular topic.

**How to decide:**

```
python3 scripts/update_priors.py --qclass <qclass of the current subquestion>
```

Prints all known channels of this `qclass`, ranked by posterior mean
(0..1, higher — gave better evidence in past runs), without trimming to the top-20 — trimming
is appropriate for a general overview, not for a single class where the sample is small anyway.
Take the channel with the highest value among those not yet used in this subquestion.
Empty output — there is no prior for this `qclass` yet, act by the matrix as usual.

**Do not replace Primary/Secondary with this step.** It decides only about an additional channel
beyond the mandatory minimum. The matrix and the registry-first rule (above) are stronger than any
accumulated statistics — they close off a systematic error (the web as a source of
numbers), while the prior merely ranks empirical yield.

**How this statistics comes into being at all** — `SKILL.md`, the section «Post-processing
of a run — collecting Bayesian swarm observations»: after Phase 7 each run writes
observations on the channels actually used, and ad-hoc sources found here through Discovery
patterns that became a claim's `root`/`dissent` are registered as
candidates for promotion into the catalog by the same step.

---

## Anti-patterns

**❌ «Just googling»** — `web-general` is always a **fallback**, not primary. If it is primary — you did not run the topic through dispatch.

**❌ One channel per subquestion** — violates the triangulation requirement in Phase 5. Minimum 2 channels of different types.

**❌ Ignoring the awesome-lists registry** — it is there so that the catalog is not finite. Always check it if the topic is narrow.

**❌ Going into repositories without a reason** — `code-github` is primary only when the subquestion is about code/a tool/a dataset. Not for «find something on the topic».

**❌ Not recording the dispatch in plan.md** — without the record Phase 6 adversarial will not be able to check the coverage.

**❌ Using paid sources when free ones exist** — if the user has no Statista/Crunchbase/Bloomberg key, do not build the strategy around them. Free first, paid after, if free is not enough.

**❌ Substituting Primary/Secondary with a prior** — a prior ranks only the additional channel beyond the mandatory minimum (see above). The mandatory part of the matrix is never moved by a prior — otherwise the swarm will learn to go where it is already strong, and the growth points will never be re-checked.
