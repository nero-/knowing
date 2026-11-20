<!-- translated from upstream/references/api_sources/grants/nsf_awards.md @ e233797 — see docs/TRANSLATION.md -->
# NSF Awards API

## Overview

- **Endpoint base:** `https://api.nsf.gov/services/v1/`
- **Auth:** None
- **Free tier:** Unlimited, no registration
- **Rate limit:** Not officially documented. Community courtesy guideline — ~1 req/sec (not confirmed by NSF documentation). 8 requests in a row without a pause passed without a 429 during verification.
- **Docs:** https://resources.research.gov/common/webapi/awardapisearch-v1.htm (general dev resources — https://www.nsf.gov/digital/developer)
- **Status page:** No dedicated status page. Scheduled/unscheduled outages are announced at https://www.research.gov
- **Coverage:** All awarded NSF grants, data at least from 1959–1969 (verified by query — 0 results for 1959, 414 for 1969)
- **Verified:** 2026-08-17

## What it returns

JSON (or XML/JSONP) with structured award data: awardee, PI, amount, programme, dates, abstract.

```json
{
  "response": {
    "award": [{
      "id": "7001483",
      "title": "...",
      "awardeeName": "Entomological Society of America",
      "pdPIName": "DATA NOT AVAILABLE",
      "startDate": "01/01/1970",
      "expDate": "12/31/1972",
      "estimatedTotalAmt": "11000",
      "fundsObligatedAmt": "11000",
      "orgLongName": "Directorate for Computer and Information Science and Engineering",
      "fundProgramName": "",
      "abstractText": "..."
    }],
    "metadata": {"offset": 0, "rpp": 1, "totalCount": 414}
  }
}
```

## When to use

- Find who received how much NSF funding by topic/organization/state
- Check the funding acknowledgment from a paper (NSF award number → grant details)
- Landscape analysis: how much money NSF invested in a field over a period
- Find PIs working in a specific area (for outreach/collaboration research)

## When not to use

- Grants from other agencies (NIH, DOE, DOD) — the NSF Awards API covers NSF only
- Future/open competitions — this is a database of ALREADY AWARDED grants, not opportunities (for that you need Grants.gov)
- Mass bulk export of the whole database in one request — `rpp` is capped at 25 records per page, a full dump needs pagination via `offset`

## Auth setup

Not needed. There is no key/registration, and the 25-records-per-page limit is easily worked around via `offset`.

## Query patterns

### Keyword search

```
GET /awards.json?keyword={query}&rpp=25
```

### By awardee / PI

```
GET /awards.json?awardeeName={org}&rpp=25
GET /awards.json?pdPIName={name}&rpp=25
```

### Date range

```
GET /awards.json?dateStart={mm/dd/yyyy}&dateEnd={mm/dd/yyyy}&rpp=25
```

### Amount range

```
GET /awards.json?estimatedTotalAmtFrom={n}&estimatedTotalAmtTo={n}&rpp=25
```

### Select specific fields

```
GET /awards.json?keyword={query}&printFields=id,title,awardeeName,pdPIName,startDate,estimatedTotalAmt&rpp=25
```

### Pagination

```
GET /awards.json?keyword={query}&rpp=25&offset=26
```

## Example queries

**Verified 2026-08-17, response 200:**

```
GET https://api.nsf.gov/services/v1/awards.json?keyword=quantum&rpp=2
```

Returned 2 award records with the full abstract, awardee, PI, amounts.

**Funding landscape by topic for a year:**

```
GET https://api.nsf.gov/services/v1/awards.json?keyword=vertical+farming&dateStart=01/01/2024&dateEnd=12/31/2024&printFields=id,title,awardeeName,estimatedTotalAmt&rpp=25
```

## Limitations

- `rpp` (results per page) maxes out at 25 — large exports need pagination via `offset`
- US federal awards from NSF only — no data on other agencies
- Old records (1960s–70s) often contain `"DATA NOT AVAILABLE"` in the PI/performance location fields
- No explicit rate limit in the documentation — risk of unexpected throttling under aggressive polling
- The `http://` endpoint issues a 301 redirect to `https://` — use https directly

## Combine with

- **NIH RePORTER** (`grants/nih_reporter.md`) — the same logic for medical grants
- **CrossRef** (`academic/crossref.md`) — funder-lookup `filter=funder:10.13039/100000001` (NSF funder ID) for papers funded by NSF
- **OpenAlex** (`academic/openalex.md`) — the reverse link grant → publications via funder ID
- **Grants.gov** (`grants/grants_gov.md`) — if you need future/open NSF competitions rather than awarded grants

## Fallback if API down or rate-limited

1. Pause and retry — there is no public Retry-After, wait manually ~5-10 sec
2. HTML search via https://www.nsf.gov/awardsearch/ (the same dataset, manual parsing)
3. CrossRef funder-lookup (`academic/crossref.md`) for papers where the funder is NSF, as an indirect source
