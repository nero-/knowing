<!-- translated from upstream/references/registry/registries.md @ e233797 — see docs/TRANSLATION.md -->
# Source registry — Registries

Corporate, network, procurement and non-profit registries — the entry point for the question "who is this and what do they own". Patent offices are not here: reconnaissance turned up none, the hole is filled manually via api_sources/.

**Verified:** 2026-08-05 — every address answered a live request at the time of reconnaissance. Only sources of value 5 out of 5 were selected.
**The addresses are final, after redirects** — the original check ran without `curl -L`, otherwise a dead address is painted green by a response from a redirect.
**Entries:** 12, of them 1 require a key or registration.

The registry answers "where to look for this signal", not "how reliable the source is": the credibility column is a reconnaissance estimate, not a Phase 5 result. The provenance of a number is still checked via `source_scoring.md`. The shelf life of such a list is months; a dead address is not a registry bug but a signal to re-check.

| Source | Address | Signal | Access | Credibility |
|---|---|---|---|---|
| OECD SDMX Data API — Patents Indicators | <https://sdmx.oecd.org/public/rest/data/OECD.ENV.EPI,DSD_PAT_IND@DF_PAT_IND,1.0/all?format=jsondata> | ip-activity-signal | free | high |
| AFRINIC RDAP — Regional Internet Registry (Africa) | <https://rdap.afrinic.net/rdap/ip/196.216.2.0/24> | market-registry-signal | free | high |
| Artemis.bm Catastrophe Bond & ILS News RSS | <https://www.artemis.bm/feed/> | market-registry-signal | free | high |
| Candid (GuideStar) — Essentials API v4 (nonprofit profile/financial/taxonomy data) | <https://developer.candid.org/reference/essentials_v4> | market-registry-signal | нужен ключ | high |
| EU VIES — VAT Information Exchange System (REST/SOAP validation API) | <https://ec.europa.eu/taxation_customs/vies/rest-api/ms/DE/vat/811569869> | market-registry-signal | free | high |
| IRS Exempt Organizations Business Master File (EO BMF) — bulk CSV per state | <https://www.irs.gov/pub/irs-soi/eo_dc.csv> | market-registry-signal | free | high |
| International Franchise Association — Franchise Directory (WP REST API) | <https://www.franchise.org/wp-json/wp/v2/franchise?per_page=3> | market-registry-signal | free | high |
| Open Banking Tracker — API Aggregators Registry (PSD2/Open Banking TPP Directory) | <https://api.github.com/repos/not-a-bank/open-banking-tracker-data/contents/data/api-aggregators> | market-registry-signal | free | high |
| PeeringDB API — Network Operator / Internet Exchange Registry | <https://www.peeringdb.com/api/net?limit=2> | market-registry-signal | free | high |
| Prozorro / OpenProcurement — Live Public Tenders API | <https://public.api.openprocurement.org/api/2.5/tenders?descending=1&limit=3> | market-registry-signal | free | high |
| RIPE NCC Stat API — Regional Internet Registry (Europe/Middle East/Central Asia) | <https://stat.ripe.net/data/network-info/data.json?resource=8.8.8.8> | market-registry-signal | free | high |
| UNESCO Institute for Statistics (UIS) Data API — Education Indicators | <https://api.uis.unesco.org/api/public/data/indicators?indicator=CR.1&geoUnit=USA> | market-registry-signal | free | high |
