<!-- translated from upstream/references/api_sources/grants/nih_reporter.md @ e233797 — see docs/TRANSLATION.md -->
# NIH RePORTER API (v2)

## Overview

- **Endpoint base:** `https://api.reporter.nih.gov/v2/`
- **Auth:** None
- **Free tier:** Unlimited, no registration
- **Rate limit:** No official numeric limit. NIH asks for no more than ~1 req/sec and for large batch jobs to be moved to weekends or weekdays 21:00–05:00 ET; on violation — an IP block.
- **Docs:** https://api.reporter.nih.gov/ (Swagger UI, "V2.0")
- **Status page:** No dedicated status page. Questions — RePORT@mail.nih.gov
- **Coverage:** Grants from NIH and other HHS agencies. Data is confirmed at least from fiscal year 1985 (0 results for FY1975/1980, 49 745 for FY1985)
- **Verified:** 2026-08-17

## What it returns

JSON with structured project records: amounts, PI, organization, agency/institute, fiscal year, linked publications/patents/clinical studies (through separate endpoints).

```json
{
  "meta": {"search_id": "...", "total": 76, "offset": 0, "limit": 2},
  "results": [{
    "appl_id": 10548235,
    "project_num": "5U01DK132737-02",
    "fiscal_year": 2023,
    "organization": {"org_name": "EMORY UNIVERSITY", "org_state": "GA"},
    "award_amount": 990010,
    "principal_investigators": [{"full_name": "Mary Beth  Weber", "is_contact_pi": true}],
    "agency_ic_admin": {"code": "DK", "abbreviation": "NIDDK", "name": "National Institute of Diabetes and Digestive and Kidney Diseases"},
    "agency_ic_fundings": [{"fy": 2023, "total_cost": 990010.0}]
  }]
}
```

## When to use

- Find who received how much NIH funding by topic/institution/PI
- Check the funding acknowledgment of a biomedical paper
- Landscape analysis for a specific NIH Institute/Center (NIDDK, NCI, NIAID, etc.)
- Link a grant to publications/patents/clinical studies (via `publications/search`, `patents/search`, `clinicalstudies/search` of the same v2 API)

## When not to use

- Grants from non-HHS agencies (NSF, DOE) — not covered
- Data before FY1985 — not in the database
- Future/open NIH competitions (funding opportunities) — RePORTER is awarded grants, not opportunities; for forecasts and open FOAs you need Grants.gov or grants.nih.gov/funding

## Auth setup

Not needed. Requests are POST with a JSON body, without keys or authorization headers.

## Query patterns

### Search projects (POST)

```
POST /v2/projects/search
Content-Type: application/json

{"criteria": {"fiscal_years": [2023], "pi_names": [{"any_name": "Smith"}]}, "limit": 50, "offset": 0}
```

### By organization

```json
{"criteria": {"org_names": ["STANFORD UNIVERSITY"], "fiscal_years": [2024]}, "limit": 50}
```

### By text search (title/abstract/terms)

```json
{"criteria": {"advanced_text_search": {"operator": "and", "search_field": "projecttitle,abstracttext", "search_text": "intermittent fasting"}}, "limit": 50}
```

### By agency/IC and activity code

```json
{"criteria": {"agencies": ["NIDDK"], "activity_codes": ["R01"], "fiscal_years": [2024]}, "limit": 50}
```

### Linked publications

```
POST /v2/publications/search
{"criteria": {"appl_ids": [10548235]}, "limit": 50}
```

## Example queries

**Verified 2026-08-17, response 200 (76 hits):**

```
POST https://api.reporter.nih.gov/v2/projects/search
{"criteria":{"fiscal_years":[2023],"pi_names":[{"any_name":"Collins"}]},"limit":2,"offset":0}
```

**Landscape by topic and year:**

```
POST https://api.reporter.nih.gov/v2/projects/search
{"criteria":{"advanced_text_search":{"operator":"and","search_field":"projecttitle","search_text":"vertical farming"},"fiscal_years":[2024]},"limit":50}
```

## Limitations

- Pagination is bounded: a maximum offset of 14 999 for projects, 9 999 for publications; a maximum of 500 records per request (default 50)
- HHS agencies only (NIH and adjacent), no non-HHS federal grants
- Data before FY1985 is unavailable
- Strict community rate-limit guidance (not a formal limit, but a risk of an IP ban under aggressive polling)
- POST-only API — GET requests do not work for search, a JSON body is required

## Combine with

- **PubMed E-utilities** (`domain_specific/pubmed.md`) — publications by the same PI/topic, cross-check with `agency_ic_fundings`
- **ClinicalTrials.gov** (`domain_specific/clinicaltrials.md`) — clinical trials tied to an NIH grant
- **NSF Awards API** (`grants/nsf_awards.md`) — the same for non-medical US federal funding
- **Grants.gov** (`grants/grants_gov.md`) — if you need future/open NIH funding opportunities rather than awarded grants

## Fallback if API down or rate-limited

1. A pause of ~1 req/sec and retry — on a systemic IP block you have to wait for the NIH admin to lift the block
2. HTML search via https://reporter.nih.gov/search (the same dataset, UI)
3. Bulk export via NIH ExPORTER (https://reporter.nih.gov/exporter) — annual CSV/XML dumps of the same dataset
