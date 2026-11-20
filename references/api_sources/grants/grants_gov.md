<!-- translated from upstream/references/api_sources/grants/grants_gov.md @ e233797 — see docs/TRANSLATION.md -->
# Grants.gov Search2 API

## Overview

- **Endpoint base:** `https://api.grants.gov/v1/api/`
- **Auth:** None for `search2` and `fetchOpportunity`. Separate endpoints (submission, applicant-only) require an API key via a Help Desk ticket — not relevant to search
- **Free tier:** Unlimited, without registration
- **Rate limit:** Not documented for `search2`/`fetchOpportunity` (10 requests in a row without a pause passed without a 429 during verification). **Do not confuse** with the separate, newer beta API `api.simpler.grants.gov` — that one officially declares 60 req/min / 10 000 req/day per key, but it is a different service with different auth (`X-API-Key`), not search2
- **Docs:** https://grants.gov/api/api-guide, https://grants.gov/api/common/search2
- **Status page:** No dedicated status page. Scheduled maintenance announcements — https://grants-gov.blogspot.com
- **Coverage:** Current/future federal US funding opportunities (posted, forecasted) + closed/archived. The archived status is confirmed at least as far back as 2004 (72 887 hits on an empty query with the archived filter, the oldest found — 2004)
- **Verified:** 2026-08-17

## What it returns

JSON with a list of funding opportunities (not awarded grants — these are competitions/announcements).

```json
{
  "errorcode": 0,
  "msg": "Webservice Succeeds",
  "data": {
    "hitCount": 67,
    "oppHits": [{
      "id": "103313",
      "number": "NOAA-OAR-CPO-2012-2003041",
      "title": "Climate Program Office for FY 2012",
      "agencyCode": "DOC",
      "agency": "Department of Commerce",
      "openDate": "07/06/2011",
      "closeDate": "",
      "oppStatus": "posted",
      "docType": "synopsis",
      "cfdaList": ["11.431"]
    }]
  }
}
```

## When to use

- Find open/upcoming federal US grant competitions by topic, agency, eligibility
- Monitor new funding opportunities for a specific organization/field
- Check the status of a specific opportunity number
- Unlike NSF Awards / NIH RePORTER — these are **future opportunities**, not the history of money awarded

## When not to use

- You need grants already awarded (who got how much) — Grants.gov does NOT provide that, use `grants/nsf_awards.md` or `grants/nih_reporter.md`
- You need high throughput with a guaranteed SLA/limits — consider the beta `api.simpler.grants.gov` with a key (in development as of 2026-08-17, the schema may change)
- EU/non-US grants — not covered, see `grants/cordis.md`

## Auth setup

Not needed for `search2`. No key required, no env var needed.

## Query patterns

### Keyword search (POST)

```
POST /v1/api/search2
Content-Type: application/json

{"keyword": "climate", "rows": 25}
```

### Filter by competition status

```json
{"keyword": "", "oppStatuses": "forecasted|posted", "rows": 25}
```

### Filter by agency and funding category

```json
{"keyword": "research", "agencies": "NSF", "fundingCategories": "ST", "rows": 25}
```

### Pagination

```json
{"keyword": "climate", "rows": 25, "startRecordNum": 25}
```

### Get a specific opportunity (fetchOpportunity)

```
POST /v1/api/fetchOpportunity
{"opportunityId": "103313"}
```

## Example queries

**Verified 2026-08-17, response 200, hitCount 67:**

```
POST https://api.grants.gov/v1/api/search2
{"keyword": "climate", "rows": 2}
```

**Verified 2026-08-17, response 200, hitCount 72887 (archived filter without a keyword):**

```
POST https://api.grants.gov/v1/api/search2
{"keyword": "", "oppStatuses": "archived", "rows": 3, "sortBy": "openDate|asc"}
```

## Limitations

- US federal opportunities only — does not cover state/local/private grants
- Returns competition announcements, NOT data about awarded grants — for that you need the NSF/NIH-specific APIs
- No official rate limit — risk of unexpected throttling under aggressive use; for serious production integration Grants.gov recommends a separate keyed gateway
- The response schema in places resembles a legacy SOAP wrapper in JSON (`errorcode`/`msg`/`token`) — not a clean REST design

## Combine with

- **NSF Awards API** (`grants/nsf_awards.md`) — once a competition has closed and the grants have been awarded, look for them here
- **NIH RePORTER** (`grants/nih_reporter.md`) — the same for NIH funding opportunities → awarded grants
- **CORDIS** (`grants/cordis.md`) — the EU equivalent for tracing already-funded projects after a call
- **SEC EDGAR** (`financial/sec_edgar.md`) — if the grant recipient is a public company, for financial context

## Fallback if API down or rate-limited

1. Retry with a pause — no public Retry-After was discovered, wait manually
2. HTML search via https://grants.gov/search-grants (the same dataset, UI)
3. RSS/email alerts via https://grants.gov (subscription to specific categories — not for an agent, but useful for the user)
