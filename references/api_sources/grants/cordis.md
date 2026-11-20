<!-- translated from upstream/references/api_sources/grants/cordis.md @ e233797 — see docs/TRANSLATION.md -->
# CORDIS (EU-funded research projects)

## Overview

- **Endpoint base:** CORDIS has no official REST/JSON search API. The real access options:
  - Bulk datasets: `https://cordis.europa.eu/data/cordis-{programme}projects-{format}.zip`
  - SPARQL: `https://cordis.europa.eu/datalab/sparql-endpoint`
  - Search UI with export: `https://cordis.europa.eu/search/en?q={query}&format={json|csv|xml}` — **not officially documented**, but public and working (used by the cordis.europa.eu site itself)
- **Auth:** None for any of the options
- **Free tier:** Unlimited
- **Rate limit:** Not documented for any method (not confirmed as of 2026-08-17)
- **Docs:** https://cordis.europa.eu/about/services (the official overview of access methods). The search-JSON endpoint is not described anywhere as a public API — discovered and verified manually, use with caution
- **Status page:** No dedicated status page
- **Coverage:** Projects FP1–FP7, H2020, Euratom, Horizon Europe (2021–2027). The HORIZON bulk file was updated 2026-08-06 (current), the FP7 file is static since 2025-01-02 (the programme is closed)
- **Verified:** 2026-08-17

## What it returns

- **Bulk (CSV/XML/JSON zip):** complete datasets per programme — projects, organizations, deliverables, publications, topics, legal basis, EuroSciVoc classification
- **SPARQL:** linked-data triples, flexible arbitrary query over the CORDIS RDF graph
- **Search-JSON (undocumented):** a structure of the form

```json
{
  "result": {"header": {"search": {"properties": {"query": {...}}}, "numHits": "2", "totalHits": "25598"}},
  "hits": {"hit": [{
    "@attributes": {"score": "8.31"},
    "project": {
      "contenttype": "project",
      "rcn": "253870",
      "id": "101108476",
      "acronym": "HyNNet NISQ",
      "teaser": "...",
      "objective": "..."
    }
  }]}
}
```

## When to use

- Find EU-funded projects by topic (Horizon Europe, H2020, FP7 and earlier)
- Get the participating organizations and their roles (coordinator/participant) for a grant
- Mass analysis of the EU R&I funding landscape per framework programme (via bulk CSV)
- Cross-check the funding acknowledgment of a European article against the real grant (Grant Agreement Number)

## When not to use

- You need live programmatic search with a guaranteed stable contract — use the bulk datasets, not the search-JSON endpoint (it is not a public API and may change without announcement)
- US federal grants — not covered (see `grants/nsf_awards.md`, `grants/nih_reporter.md`)
- You need real-time data on freshly submitted applications — CORDIS publishes already approved/signed projects, not applications under review

## Auth setup

Not needed for any of the access methods.

## Query patterns

### Bulk download by programme (current zip)

```
GET https://cordis.europa.eu/data/cordis-HORIZONprojects-csv.zip
GET https://cordis.europa.eu/data/cordis-HORIZONprojects-json.zip
GET https://cordis.europa.eu/data/cordis-h2020projects-csv.zip
GET https://cordis.europa.eu/data/cordis-fp7projects-csv.zip
```

### Search-JSON (undocumented, but working)

```
GET https://cordis.europa.eu/search/en?q={query}&format=json&num=10
```

### Filter by content type (projects only)

```
GET https://cordis.europa.eu/search/en?q=contenttype='project' AND {query}&format=json&num=10
```

### CSV export of search results

```
GET https://cordis.europa.eu/search?q=contenttype='project'&format=csv
```

### SPARQL (for complex linked-data queries)

```
POST https://cordis.europa.eu/datalab/sparql-endpoint
Content-Type: application/sparql-query
```

## Example queries

**Verified 2026-08-17, response 200, totalHits 25598:**

```
GET https://cordis.europa.eu/search/en?q=quantum&format=json&num=2
```

**Verified 2026-08-17, response 200, totalHits 3324 (projects only):**

```
GET https://cordis.europa.eu/search/en?q=contenttype='project' AND quantum&format=json&num=1
```

**Verified 2026-08-17, HEAD 200, content-length 36 672 015 bytes:**

```
HEAD https://cordis.europa.eu/data/cordis-HORIZONprojects-csv.zip
```

## Limitations

- No official REST API with a guaranteed contract — the search-JSON endpoint is not documented by CORDIS, use it knowing that it may change
- Bulk datasets are updated once a month, not real-time
- The data covers only already approved/signed projects, not calls under review
- The CSV structure uses a semicolon delimiter and requires parsing (not a comma)
- SPARQL requires knowledge of RDF/SPARQL syntax — a high entry barrier

## Combine with

- **CrossRef** (`academic/crossref.md`) — funder-lookup `filter=funder:10.13039/501100000780` (EU Commission funder ID) for papers funded by Horizon Europe/H2020
- **OpenAlex** (`academic/openalex.md`) — the reverse link EU grant → publications
- **NSF Awards API** (`grants/nsf_awards.md`) / **NIH RePORTER** (`grants/nih_reporter.md`) — the analogues for US federal funding

## Fallback if API down or rate-limited

1. The bulk zip dataset instead of search-JSON — more stable, does not depend on an undocumented endpoint
2. CORDIS Data Extraction Tool (requires registration): https://cordis.europa.eu/user/dataextractions
3. WebFetch the page `https://cordis.europa.eu/search?q={query}` (the HTML version of the same search)
