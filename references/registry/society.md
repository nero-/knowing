<!-- translated from upstream/references/registry/society.md @ e233797 — see docs/TRANSLATION.md -->
# Source registry — Society

Conflicts, state narratives, democracy and infrastructure indices, the labour market, culture, games, sport.

**Verified:** 2026-08-05 — every address answered a live request at the time of reconnaissance. Only sources of value 5 out of 5 were selected.
**The addresses are final, after redirects** — the original check ran without `curl -L`, otherwise a dead address is painted green by a response from a redirect.
**Entries:** 28, of them 1 require a key or registration.

The registry answers "where to look for this signal", not "how reliable the source is": the credibility column is a reconnaissance estimate, not a Phase 5 result. The provenance of a number is still checked via `source_scoring.md`. The shelf life of such a list is months; a dead address is not a registry bug but a signal to re-check.

| Source | Address | Signal | Access | Credibility |
|---|---|---|---|---|
| ACLED — Armed Conflict Location & Event Data Project (API, requires registration) | <https://acleddata.com/conflict-data> | conflict-event-signal | нужен ключ | high |
| Al Jazeera English — All News RSS Feed | <https://www.aljazeera.com/xml/rss/all.xml> | conflict-event-signal | free | medium |
| Colombia Reports — RSS Feed | <https://colombiareports.com/feed> | conflict-event-signal | free | medium |
| Defense News — RSS Feed | <https://www.defensenews.com/arc/outboundfeeds/rss/> | conflict-event-signal | free | high |
| Kyiv Post — RSS Feed | <https://www.kyivpost.com/feed> | conflict-event-signal | free | high |
| Meduza — RSS Feed (English) | <https://meduza.io/rss/en/all> | conflict-event-signal | free | high |
| MercoPress — RSS Feed | <https://en.mercopress.com/rss/> | conflict-event-signal | free | medium |
| Myanmar Now (English) — RSS Feed | <https://myanmar-now.org/en/feed/> | conflict-event-signal | free | high |
| Taipei Times — Front Page RSS | <https://www.taipeitimes.com/xml/index.rss> | conflict-event-signal | free | high |
| The Korea Times — RSS Feed (All News) | <https://feed.koreatimes.co.kr/k/allnews.xml> | conflict-event-signal | free | high |
| The Moscow Times — RSS Feed (All News) | <https://www.themoscowtimes.com/rss/all> | conflict-event-signal | free | high |
| The Rio Times — RSS Feed | <https://www.riotimesonline.com/feed> | conflict-event-signal | free | medium |
| FBI IC3 Annual Report — Internet Crime Complaint Center Victim Statistics | <https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf> | crime-victimization-statistics-signal | free | high |
| The Metropolitan Museum of Art — Open Access Collection API | <https://collectionapi.metmuseum.org/public/collection/v1/objects/1> | cultural-heritage-signal | free | high |
| V-Dem (Varieties of Democracy) — vdemdata dataset (GitHub, RData) | <https://api.github.com/repos/vdeminstitute/vdemdata/contents/data> | democracy-index-signal | free | high |
| ESRB — VideoGame Rating Schema (per-title page) | <https://www.esrb.org/ratings/38265/steel-assault/> | gaming-content-rating-signal | free | high |
| Steam Store API — App Details | <https://store.steampowered.com/api/appdetails?appids=730> | gaming-industry-data-signal | free | high |
| World Bank Logistics Performance Index (LPI) API | <https://api.worldbank.org/v2/country/all/indicator/LP.LPI.OVRL.XQ?format=json&per_page=300> | infrastructure-index-signal | free | high |
| Football-Data.org — Competitions API | <https://api.football-data.org/v4/competitions> | sports-performance-data-signal | free | high |
| Kremlin.ru — President News Feed (English) | <http://en.kremlin.ru/events/president/news/feed> | state-narrative-signal | free | high |
| RT — RSS Feed (Daily News) | <https://www.rt.com/rss/> | state-narrative-signal | free | low |
| TASS — RSS Feed (English) | <https://tass.com/rss/v2.xml> | state-narrative-signal | free | low |
| Tehran Times — RSS Feed | <https://www.tehrantimes.com/rss> | state-narrative-signal | free | low |
| UN Press — Meetings Coverage and Press Releases RSS | <https://press.un.org/en/rss.xml> | state-narrative-signal | free | high |
| Canada Job Bank — Job Postings Open Data (monthly bulk CSV) | <https://open.canada.ca/data/en/dataset/ea639e28-c0fc-48bf-b5dd-b8899bd43072> | talent-flow-signal | free | high |
| Greenhouse Job Board API (per-company postings, no key) | <https://boards-api.greenhouse.io/v1/boards/airbnb/jobs> | talent-flow-signal | free | high |
| NPI Registry API (CMS National Provider Identifier) | <https://npiregistry.cms.hhs.gov/api/?number=&first_name=&last_name=&state=CA&limit=5&version=2.1> | talent-flow-signal | free | high |
| OPM FedScope — Federal Employment Summary Data File (bulk download) | <https://www.opm.gov/data/datasets/Files/756/a1acc4f3-0c10-45e3-ac1f-0ee7f5769e1d.zip> | talent-flow-signal | free | high |
