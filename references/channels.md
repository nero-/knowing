<!-- translated from upstream/references/channels.md @ e233797 — see docs/TRANSLATION.md -->
# Search channels — a catalog of <!--gen:count:channels-->29<!--/gen--> search channels

## Contents

- How to use
- Catalog of <!--gen:count:channels-->29<!--/gen--> channels
- Channel selection — by genre
- Channel selection — by data types in the question
- Paywall fallback protocol (universal)
- Bot-block ≠ paywall
- Open doors of closed sites
- Forbidden patterns (do not use)
- When a channel «does not work»
- Future channels (TODO when capabilities appear)

Channels are **named search strategies** for different types of sources. Each channel has known query patterns, an expected result format, and known limitations.

## How to use

1. After Phase 2 (genre & block selection) — determine which channels are relevant for each subtopic.
2. In `plan.md` the Information sourcing strategy section states the channels per subtopic.
3. The sub-agent prompt gets `channels: [list]` — the agent knows where to search.
4. In `sources/NN.md` the `channel:` field records which channel produced the source.

A channel says WHERE to search; the concrete vetted addresses per signal live in `references/registry/` (see `source_dispatch.md`, the «Registry» section). The channels `news-current`, `industry-specific`, `preprint-servers`, `forum-discussion`, `api-direct`, `regulatory-legal` are covered most densely there.

## Catalog of <!--gen:count:channels-->29<!--/gen--> channels

### Часть A — Web and discovery

#### 1. `web-general`
**What:** Broad WebSearch without specific sites.
**Query pattern:** `<topic> <keyword>` — broad.
**Returns:** mainstream media, blogs, general references.
**When:** the first round for understanding the topic, common knowledge.
**Limitations:** SEO-skewed, recent dominates, little academic.
**By genre:** baseline everywhere.

#### 2. `wikipedia-references`
**What:** Wikipedia as a **navigation hub** to primary sources.
**Query patterns:**
- `site:en.wikipedia.org <topic>` (English)
- `site:ru.wikipedia.org <topic>` (Russian)
- Find specific articles, then follow References/Bibliography
**Returns:** links to primary sources via the bibliography.
**When:** at the start of any research for quick framing.
**Quality:** Wikipedia itself is C-grade. Use only for navigation, never as citation.

#### 3. `archive-historical`
**What:** archive.org Wayback Machine, archive.today for paywalled/deleted.
**Query patterns:**
- `https://web.archive.org/web/*/<url>` — for a specific URL
- `archive.today/<url>` — newer mirror
**Returns:** older versions of pages, removed content, paywalled content via cache.
**When:** fallback when the live source is blocked; checking changes over time.
**Limitations:** not everything is in the archive; recent dynamic content is often missing.

---

### Часть B — Academic / Scholarly

#### 4. `academic`
**What:** Search in academic sources.
**Query patterns:**
- `site:scholar.google.com <topic>` — broad scholarly
- `site:semanticscholar.org <topic>` — AI-powered
- `site:ncbi.nlm.nih.gov <topic>` (PubMed)
- `<topic> "meta-analysis"`
- `<topic> "systematic review"`
- `<topic> filetype:pdf` (preprints, white papers)

**Paywall fallback sequence:**
1. Try `preprint-servers` channel
2. `"<paper title>" researchgate OR academia.edu`
3. `"<paper title>" filetype:pdf` — institutional copy
4. `site:edu "<paper title>"` — university hosting
5. Unpaywall search
6. If nothing — fetch the abstract, mark `access: paywalled-abstract-only`

**When:** validation of scientific claims, deep explainer, any scientific topic.

#### 5. `preprint-servers`
**What:** Legal open access scholarly preprints — **the first stop for recent academic**.
**Query patterns:**
- `site:arxiv.org <topic>` — CS, physics, math
- `site:biorxiv.org <topic>` — biology
- `site:medrxiv.org <topic>` — medicine
- `site:ssrn.com <topic>` — economics, social science, law
- `site:osf.io/preprints <topic>` — general
- `site:psyarxiv.com <topic>` — psychology
- `site:chemrxiv.org <topic>` — chemistry
- `site:engrxiv.org <topic>` — engineering

**Returns:** open access scholarly papers full text.
**When:** validation, any recent scientific claim.
**Advantage:** free, legal, full text. Often preprint = final version.
**Limitations:** some preprints are never peer-reviewed eventually; check «later published».

#### 6. `conference-proceedings`
**What:** Conference papers from major academic venues.
**Query patterns:**
- `site:acm.org <topic>`
- `site:ieee.org <topic>`
- `<topic> "ICML"` / `"NeurIPS"` / `"USENIX"` / `"VLDB"` / `"SIGGRAPH"` etc.
- `<topic> conference proceedings filetype:pdf`
- `<topic> "workshop"`

**Returns:** cutting-edge research, peer-reviewed conference papers.
**When:** academic-deep validation, tech research where conferences are the main venue.
**Limitations:** often paywalled — fallback to preprint-servers.

---

### Часть C — Code

#### 7. `code-github`
**What:** Public GitHub repositories.
**Query patterns:**
- `site:github.com <topic>`
- `site:github.com <topic> stars:>1000` — only popular
- `<topic> issue site:github.com`
- `<topic> "lessons learned" site:github.com`
- `<topic> ADR site:github.com` — architecture decision records
- `<topic> filetype:md site:github.com` — READMEs/docs

**Returns:** real implementations, READMEs, issue discussions, ADRs.
**When:** tech explainer, decision (how X is solved in practice), validation of tech claims.
**Limitations:** public only; code requires understanding.

#### 8. `code-other`
**What:** GitLab, Bitbucket, sourcehut, other code hosts.
**Query patterns:**
- `site:gitlab.com <topic>`
- `site:bitbucket.org <topic>`
- `site:sr.ht <topic>`

**When:** projects that deliberately are not on GitHub (some EU/government/privacy-focused).

---

### Часть D — Community / Discussion

#### 9. `forum-discussion`
**What:** Targeted search on discussion sites.
**Query patterns:**
- `site:reddit.com <topic>` (or subreddit-specific: `site:reddit.com/r/<sub>`)
- `site:news.ycombinator.com <topic>`
- `site:stackexchange.com <topic>` / `site:stackoverflow.com`
- `site:lobste.rs <topic>`
- `<topic> "my experience" reddit`
- `<topic> "regret" reddit` — for validation/decision

**Returns:** real-user experiences, anecdotes, community sentiment, contrarian voices.
**When:** validation («does X work in practice»), landscape (community signals), decision (regret stories).
**Quality:** anecdotal — C on our scale. Use for signal, not proof. Good for an opposition voice.

#### 10. `social-twitter`
**What:** Twitter/X public posts.
**Query patterns:**
- `site:twitter.com <topic>` / `site:x.com <topic>`
- `<person> twitter <topic>`
- `<topic> "viral"` recent
- `<topic> "controversial"`

**Returns:** real-time discourse, hot takes.
**When:** landscape (current discourse), validation contrarian voices.
**Limitations:** WebSearch indexes Twitter poorly from 2023+ (API closure); often only cached/embedded. Weak signal source.

---

### Часть E — News and Industry

#### 11. `news-current`
**What:** News sources + date filters.
**Query patterns:**
- `<topic>` + filter «last year/month»
- `site:reuters.com <topic>`
- `site:bloomberg.com <topic>`
- `site:techcrunch.com <topic>` (tech)
- `site:ft.com <topic>` (financial)
- `<topic> "announced"` recent

**Returns:** current events, announcements, recent changes.
**When:** landscape current state, trends, recent context.
**Limitations:** sensationalism, churn, goes stale.

#### 12. `industry-reports`
**What:** Consulting firms, analyst houses.
**Query patterns:**
- `site:mckinsey.com <topic>`
- `site:bcg.com <topic>`
- `site:bain.com <topic>`
- `site:gartner.com <topic>` (often paywalled — look for press releases)
- `site:cbinsights.com <topic>`
- `<topic> "market size" <year>`
- `<topic> "industry report" filetype:pdf`

**Returns:** market sizing, trend analyses, expert commentary.
**When:** landscape, market sizing, decision context.
**Limitations:** conflict of interest (selling services), often paywalled — look for summaries.
**See also:** stat_sources/core/consulting_industry.md

---

### Часть F — Multimedia

#### 13. `video-talks`
**What:** Conference talks and video lectures.
**Query patterns:**
- `<topic> transcript`
- `<topic> conference talk PDF` (slides are more often available than a transcript)
- `<speaker> talk <topic>`
- `<conference> <year> <topic>` (e.g., AWS re:Invent, RustConf)
- `site:youtube.com <topic>` — find the video, then look for a transcript

**Returns:** conference talks (slides+transcripts), interviews, lectures.
**When:** explainer deep, expert opinion, cutting-edge topics without formal literature.
**Limitations:** transcripts inconsistent. Find a summary blog by the speaker as a proxy.

#### 14. `podcasts`
**What:** Podcast episodes with notes/transcripts.
**Query patterns:**
- `<topic> "show notes"`
- `<topic> transcript podcast`
- `<topic> podcast site:lexfridman.com` (or other top podcasts)
- `<topic> "deep dive" podcast`

**Returns:** in-depth interviews, long discussions.
**When:** expert-opinion, deep explainer, thought leader landscape.
**Limitations:** transcripts uneven; the time investment is large.

---

### Часть G — People

#### 15. `expert-individual`
**What:** Specific experts, authors, founders.
**Query patterns:**
- `"<Person Name>" <topic>` — what they said
- `<Person> blog`
- `<Person> interview <topic>`
- `<Person> "I think"` / `<Person> "predict"`
- `site:linkedin.com/in/<person>` — bio

**Returns:** expert opinions, their blogs, interviews.
**When:** validation (expert opinion), landscape (key people), understanding specific schools of thought.
**Limitations:** one voice — triangulation needed. Conflict of interest is always possible.

#### 16. `books-literature`
**What:** Books, long texts, summaries.
**Query patterns:**
- `site:books.google.com <topic>` — preview
- `site:openlibrary.org <topic>`
- `<book title> "table of contents"`
- `<book title> "summary"`
- `<topic> "in his book"`

**Returns:** links to books, fragments via preview, summaries.
**When:** deep explainers, historical-context, expert-individual (the author's books).
**Limitations:** full text often unavailable; preview is limited.

---

### Часть H — Official / Legal

#### 17. `regulatory-legal`
**What:** Government sites, regulators, official documents.
**Query patterns:**
- `site:sec.gov <company>` — SEC filings
- `site:eur-lex.europa.eu <topic>` — EU regulations
- `site:fda.gov <topic>`
- `<topic> "regulation" site:gov`
- `<company> 10-K` — annual reports
- `<topic> "directive" site:europa.eu`

**Returns:** official documents, regulatory texts, financial filings.
**When:** regulatory context, validation of legal claims, financial due diligence.
**Limitations:** long documents; navigation to specific sections is needed.
**See also:** stat_sources/core/gov_macro.md, stat_sources/core/companies_public.md

#### 18. `patents`
**What:** Patent databases.
**Query patterns:**
- `site:patents.google.com <topic>`
- `inventor:"<Name>" site:patents.google.com`
- `assignee:"<Company>" site:patents.google.com`
- `<topic> patent USPTO`

**Returns:** patent filings, inventors, prior art.
**When:** tech history, competitive analysis (what is patented), validation of tech claims.
**Limitations:** patents use legal language, not technical clarity. Patent ≠ working tech.

---

### Часть I — Quantitative

#### 19. `data-statistical-gov`
**What:** Government and intergovernmental statistical agencies.
**Query patterns:**
- `site:data.gov <topic>`
- `site:eurostat.ec.europa.eu <topic>`
- `site:ourworldindata.org <topic>`
- `site:bls.gov <topic>` (US labor)
- `site:fred.stlouisfed.org <topic>` (US macro)
- `<country> "statistics" <topic>`

**Returns:** official statistics, time series.
**When:** numbers blocks (metric-tracker, historical-data), validation of quantitative claims.
**See also:** stat_sources/core/gov_macro.md

#### 20. `product-analytics`
**What:** Open stat sites for apps, SaaS, web products.
**Query patterns:**
- `site:sensortower.com/blog <app>` — mobile
- `site:similarweb.com/website/<domain>`
- `site:crunchbase.com/organization/<co>`
- `site:builtwith.com/<domain>` — tech stack
- `site:g2.com/products/<product>` — SaaS reviews
- `site:producthunt.com/products/<product>`
- `<company> "MAU" OR "DAU" OR "ARR"` — leaked stats

**Returns:** product analytics, traffic, tech stacks, user reviews.
**When:** competitive-signals, profile-card in a landscape, market sizing for apps/SaaS, validation of popularity.
**See also:** stat_sources/core/consumer_digital.md

#### 21. `crypto-analytics`
**What:** On-chain data, crypto market analytics.
**Query patterns:**
- `site:coingecko.com/en/coins/<coin>`
- `site:defillama.com <protocol>`
- `site:dune.com <topic>` — community dashboards
- `site:etherscan.io <address>` — on-chain Ethereum
- `<protocol> "TVL"` / `<token> "market cap"`

**Returns:** market data, TVL, on-chain analytics.
**When:** crypto/web3 research.
**Quality:** high — the data is verifiable on-chain.
**See also:** stat_sources/core/crypto.md

#### 22. `social-creator-stats`
**What:** Stats for social media creators.
**Query patterns:**
- `site:socialblade.com/<platform>/user/<name>`
- `site:twitchtracker.com <streamer>`
- `<creator> "subscribers"` / `<creator> "growth"`

**Returns:** YouTube/Twitter/Twitch/etc creator stats.
**When:** influence analysis, content creator landscape.

#### 23. `industry-benchmarks`
**What:** Industry surveys and benchmark reports.
**Query patterns:**
- `<industry> "developer survey" <year>` (Stack Overflow, JetBrains)
- `<topic> "State of <industry>" report`
- `<topic> survey <year>`
- `<topic> "industry report"`

**Returns:** quantitative opinion + benchmarks.
**When:** validation of popular claims, benchmark-numbers block, persona research.
**See also:** stat_sources/core/consulting_industry.md

#### 24. `surveys-polls`
**What:** Surveys, polls.
**Query patterns:**
- `<topic> survey <year>`
- `site:pewresearch.org <topic>`
- `site:gallup.com <topic>`
- `<topic> "n=" survey`

**Returns:** public opinion data with sample sizes.
**When:** persona research, behavioral-patterns, validation of popular sentiment.
**Limitations:** sampling bias, variable methodology.

---

### Часть J — Indirect signals

#### 25. `competitive-signals`
**What:** Indirect signals about companies.
**Query patterns:**
- `site:linkedin.com/jobs <company>` — what they are hiring for
- `<company> "raised"` / `<company> "funding"`
- `<company> crunchbase`
- `<company> linkedin company size`
- `<company> "leaked"` (deck leaks etc)
- `<company> "founders" interview`

**Returns:** indirect signals about company state.
**When:** landscape, profile-card, due diligence without direct access.
**Limitations:** indirect — outdated, sample-biased; triangulation needed.
**See also:** stat_sources/core/companies_private.md

---

### Часть K — Local context

#### 26. `local-project`
**What:** Local files in the current project. Used only when `subagent_type=general-purpose` or the main thread reads them itself.
**NOT WebSearch — this is file system access.**

**Targets:**
- `CLAUDE.md`, `CLAUDE.local.md` — project context
- `docs/`, `README.md`
- `research/<other-slug>/<date>_*.md` — previous research runs
- Source code (if relevant)
- `memory/MEMORY.md`

**When:** project-specific research; hybrid (external + internal).
**Limitations:** `subagent_type=Explore` can NOT write files and does not have full file access. Either the main thread, or a general-purpose subagent.

---

### Часть L — Trade associations / Industry-specific

#### 27. `trade-associations`
**What:** Trade associations specific to industries.
**Search pattern:**
- `"<industry> association" stats`
- `"<industry> trade association" report`
- `"<industry> federation" data`

Examples (see stat_sources/industries/<industry>.md):
- Software: BSA, SIIA
- Auto: OICA, ACEA
- Aviation: IATA
- Tourism: WTTC
- Construction: AGC, NAHB
- Hotels: AHLA, STR
- Pharma: PhRMA, EFPIA
- Steel: worldsteel.org

**Returns:** industry-specific data, associations often publish public reports.
**When:** industry landscape, market sizing, regulatory landscape.

#### 28. `industry-specific`
**What:** Catch-all for industry-specific data sources.
**Use via the catalog:** `references/stat_sources/industries/<industry>.md`

Each industry file has its own curated source list. Use the catalog as a map: which industry — which sources.

---

### Часть M — API-direct (programmatic access)

#### 29. `api-direct`

**What:** A direct request to an API endpoint (JSON/XML) instead of parsing an HTML page. Full catalog in `api_sources/INDEX.md`.

**When to use:**
- Structured data (JSON) is needed, not HTML
- Bulk queries — «give me 100 papers in one request»
- Server-side filtering (`?industry=fintech&min_funding=10M`)
- Real-time data (prices, on-chain metrics)
- Programmatic search (Brave/Tavily/Exa)

**When NOT to use:**
- WebFetch HTML works and the data is sufficient
- The API requires a key and you do not have one → fallback to HTML
- The free tier is exhausted → fallback or an alternative API
- A simple one-off lookup → WebSearch is faster

**Main free no-auth APIs (priority for agents):**

- `Semantic Scholar` — 200M papers, academic search
- `OpenAlex` — 250M scholarly works, citation graph
- `CrossRef` — 130M DOIs, metadata
- `arXiv` — preprints, free full-text
- `DefiLlama` — DeFi TVL/protocols
- `CoinGecko` — crypto markets
- `Reddit JSON` — add `.json` to any Reddit URL
- `HN Algolia` — Hacker News search
- `World Bank` — global development
- `SEC EDGAR` — US public filings (needs a User-Agent header)
- `ClinicalTrials.gov` — trial registry
- `PubMed E-utilities` — biomedical literature
- `GDELT` — global news events
- `PyPI / npm` — package metadata

**APIs with a key (one-time setup, environment variable):**

- `FRED` — US economic data (instant key)
- `GitHub` — 5000 req/h authenticated
- `Stack Exchange` — 10k req/day with a key
- `NewsAPI` — 100 req/day free
- `Etherscan` — 100k req/day

**Paid (when it is worth paying):**

- `Brave Search` — Google-quality search, $3/1k
- `Tavily` — AI-optimized search with built-in answers
- `Exa.ai` — semantic neural search
- `SerpAPI` — unified Google/Bing/DuckDuckGo
- `Crunchbase Basic` — startup funding data
- `Dune Analytics` — custom on-chain SQL queries

**Auth dispatch for the agent:**

```
if an API is needed:
  → check the env var for the key (FRED_API_KEY, GITHUB_TOKEN, ...)
  → if present → use the API
  → if not:
     → is there a free no-key tier? → use it
     → no → fallback to the HTML version via WebFetch
     → mark in sources/NN.md: access: html-fallback (api blocked)
```

**Rate limit handling:**

On 429 (rate limit):
1. Wait the time from the `Retry-After` header
2. If the wait > 30 sec → fallback to HTML or an alternative API
3. Mark in `sources/NN.md` notes: `rate-limited at <ts>, fell back to <source>`

**Marks in sources/NN.md frontmatter:**

```yaml
channel: api-direct
access: api-free-no-key   # | api-free-with-key | api-paid | api-fallback-html
```

**Caveats:**
- The skill does NOT store API keys — only via environment variables
- Never ask for a key inline — ask for it to be added to the shell config
- Free tiers run out fast on active research — plan the budget

**Where to find docs:**

See the `api_sources/` catalog. The files are organized into 10 categories:
- `search/` — Brave, Tavily, Exa, SerpAPI, You.com
- `academic/` — Semantic Scholar, OpenAlex, CrossRef, arXiv
- `financial/` — FRED, World Bank, SEC EDGAR, OECD, Alpha Vantage
- `companies/` — Crunchbase, OpenCorporates, Companies House
- `crypto/` — CoinGecko, DefiLlama, Etherscan, Dune
- `code/` — GitHub, Stack Exchange, PyPI, npm
- `social/` — Reddit, HN Algolia, Lemmy
- `news/` — NewsAPI, GDELT, Currents
- `stats/` — Eurostat, Census US, UN Data
- `domain_specific/` — PubMed, ClinicalTrials, EMA, NASA, OpenWeather

Every API file has: endpoint, auth, free tier, rate limits, query templates, example queries for deepdive, limitations, combine-with recommendations, fallback strategy.

---

## Channel selection — by genre

| Genre | Primary channels | Secondary | Use sparingly |
|---|---|---|---|
| **explainer** | web-general, academic, wikipedia-references, code-github | books-literature, video-talks, expert-individual, api-direct (Semantic Scholar/arXiv) | social-twitter |
| **decision** | web-general, forum-discussion, industry-reports, code-github (tech) | expert-individual, surveys-polls, podcasts, api-direct (CoinGecko/SEC EDGAR for data) | conference-proceedings |
| **landscape** | competitive-signals, news-current, industry-reports, product-analytics | patents, forum-discussion, trade-associations, industry-specific, api-direct (Crunchbase/OpenCorporates) | social-twitter, books-literature |
| **validation** | academic, preprint-servers, conference-proceedings | forum-discussion (opposition), expert-individual, surveys-polls, archive-historical (retractions), api-direct (PubMed/Semantic Scholar for a bulk literature scan) | patents |
| **qa** | web-general + 2-3 channels by subtopic | api-direct if there is a relevant API | varies |
| **custom** | for the chosen blocks | varies | — |

## Channel selection — by data types in the question

| What we are looking for | Channel |
|---|---|
| Scientific consensus | academic + preprint-servers + conference-proceedings |
| Real-user experiences | forum-discussion + surveys-polls |
| Current state (recent events) | news-current + social-twitter |
| Market size | industry-reports + data-statistical-gov + industry-benchmarks |
| A specific company (public) | regulatory-legal (filings) + news-current + competitive-signals |
| A specific company (private) | competitive-signals + crunchbase via product-analytics |
| Mobile app data | product-analytics + industry-reports |
| Crypto/DeFi | crypto-analytics + forum-discussion |
| Industry-specific KPI | industry-specific (via the catalog) + trade-associations |
| Legal precedents | regulatory-legal + academic (law) |
| Historical context | archive-historical + books-literature + academic |
| Expert opinions | expert-individual + podcasts + video-talks |
| Code examples | code-github + code-other |

---

## Paywall fallback protocol (universal)

When we hit a paywall — follow the sequence:

```
1. Try preprint-servers (for academic)
2. Try archive-historical (Wayback / archive.today)
3. Try author's personal site / institutional repo
4. Try an alternative source with the same content (summary, news article, blog)
5. Try ResearchGate / Academia.edu (for academic)
6. Try Google Cache
7. If nothing works:
   - `access: paywalled-abstract-only` (if an abstract exists)
   - `access: closed` (if it is entirely unavailable)
   - Write to the source's `gaps` in the sub-agent JSON
```

## Bot-block ≠ paywall

Two different refusals, and they are constantly confused. The protocol above is about a **paywall**: the content exists, but behind money or a login. A separate case is when the content is public and free, but it is the AI agent specifically that is blocked: `robots.txt` with `Disallow` for `GPTBot`/`ClaudeBot`/`CCBot`. WebFetch honors such rules and answers «unable to fetch from …», which makes a live open source look dead.

A measurement on 7 URLs (numbers and date — `NOTES_dated.md`): WebFetch did not get them all; `scripts/fetch_source.py` returned content on the first tier for sites that serve the page to an ordinary client and cut only AI tokens (nytimes, theverge, wired). The rest were not a bot block but an auth wall (reuters 401, reddit 403, stackoverflow 403 Cloudflare).

Hence the rule: **classify the refusal first, then choose the protocol.**

| Refusal | Sign | Where to go |
|---|---|---|
| AI exclusion | WebFetch «unable to fetch», robots cuts AI tokens, `*` allowed | fetch ladder, Phase 4.2 |
| Paywall / auth wall | 401/402, «sign in», «subscribers only», «developer token» | `fallback_routes.yaml` → the protocol above |
| Anti-bot challenge | 403, Cloudflare, «verify you are human» | `fallback_routes.yaml` → API/feed, not force |
| Site-wide `Disallow` | robots closes the path for all clients | `gaps`, ask the user |

## Open doors of closed sites

`references/fallback_routes.yaml` is a curated map «domain → official API / feed / archive», which `fetch_source.py` prints itself on `antibot` and `auth-wall` verdicts. The map is manual not out of laziness: `api_sources/` has no field for the web domain (the audit and numbers are in `NOTES_dated.md`: `Endpoint base:`/`Auth:`/`Docs:` exist in every file, the domain in none), and the relation is of two kinds — `self` (the API on the same domain) and `proxy` (a third-party aggregator serving someone else's content). This is not derivable by machine.

**The main finding of the measurement (date — `NOTES_dated.md`): a feed survives an HTML block.** The feed pipeline is separate and is usually not covered by the anti-bot layer.

| Site | HTML | Feed / API |
|---|---|---|
| stackoverflow.com | 403 Cloudflare | Atom 200 · 115 KB; StackExchange API 200 without a key |
| economist.com | paywall | RSS 200 · 151 KB |
| theguardian.com | — | RSS 200 · 96 KB |
| nytimes.com | robots cuts 7 AI tokens | RSS 200 · 55 KB |
| wsj.com / ft.com | paywall | RSS 200 |
| reddit.com | 403 | only OAuth — `.rss` is also 403 under three UAs |
| reuters.com | 401 | RSS dead (404), aggregators only (GDELT, NewsAPI) |

Caveats:

- **A feed ≠ an article.** Title, date, annotation, URL — yes. Full text — no. A quote from the annotation is marked as an annotation.
- **The archive answers «what was there», not «what is there now».** Take the snapshot's `as_of` into `data_as_of`.
- **`verified` without a date and a response code is not `verified`.** A stale route is worse than a missing one: it eats a search round and looks like it works.
- Known holes in the map: twitter/x (the API is paid), youtube (only via SerpAPI), wikipedia (not wired up, although the MediaWiki API is open).

## Forbidden patterns (do not use)

Do NOT apply these approaches, even as a fallback:
- Solving CAPTCHAs and Cloudflare challenges, stealth fingerprinting against the anti-bot layer — `fetch_source.py` deliberately does not have this, and it is not to be added. A 403 is a signal to go to the site's API, not to increase the camouflage.
- Credential reuse / login bypass / circumventing a paywall — NEVER. An auth wall is a terminal verdict.
- Site-wide `Disallow` in robots.txt (a ban for all clients, not for AI tokens) — do not step over it yourself. `--ignore-robots` exists, but the user sets it, and the override is written to the source's `fetch_note:`.
- An arbitrary `curl -A 'Mozilla/…'` bypassing WebFetch — not because «you must not fetch», but because bypassing `fetch_source.py` loses the robots check, the prompt-injection sanitizer and the `fetch_tier` in the provenance.

## When a channel «does not work»

If a channel should have produced results but does not — the options:
1. Query too narrow — try a broader one
2. Topic not covered by this channel — try another
3. Source blocked — fallback sequence (paywall protocol)
4. The topic is too new — no data yet, move to news-current/social-twitter

In `sources/NN.md` of the sub-agent JSON the `secrets` field `channel:` shows where material was taken from — if several channels returned zero, record it in `gaps`. <!-- translator: ambiguous -->

## Future channels (TODO when capabilities appear)

These channels are not yet available through standard WebSearch+WebFetch — noted for the future:
- Twitter Streaming API (requires an API key)
- LinkedIn data (login required)
- Specific paywalled databases (Bloomberg, Refinitiv) — requires subscriptions
- YouTube transcripts API
- Spotify API for music
