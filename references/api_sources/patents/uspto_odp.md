<!-- translated from upstream/references/api_sources/patents/uspto_odp.md @ e233797 — see docs/TRANSLATION.md -->
# USPTO Open Data Portal (ODP)

## Overview

- **Endpoint base:** `https://api.uspto.gov/api/v1/`
- **Auth:** API key (`X-API-KEY` header) — requires a registered USPTO.gov account linked to a verified ID.me account (identity verification, not just email registration)
- **Free tier:** free, but with weekly quotas (see Rate limit) and a noticeable onboarding threshold because of ID.me
- **Rate limit:** burst = 1 (no parallel requests on one key), rate 4–15 req/sec depending on the call type; separately — weekly quotas: 5,000,000 calls/week across all metadata-retrieval APIs in total, 1,200,000 calls/week for the Patent File Wrapper Documents API, 20 downloads/year per file via the Bulk Datasets Downloads API (except XML — the limit there is higher), no more than 5 files per 10 sec from one IP. The quota resets on Sunday at midnight UTC
- **Docs:** https://data.uspto.gov/apis/getting-started , https://data.uspto.gov/apis/api-rate-limits , https://data.uspto.gov/apis/api-syntax-examples
- **Status page:** no separate status page found; see https://data.uspto.gov/support (FAQ/support)
- **Verified:** 2026-08-17

⚠️ External reconnaissance before this research assumed a limit of "45 req/min" — that was not confirmed. The real limit model is different: burst=1 + per-endpoint rate 4–15 req/sec + separate weekly quotas on three API categories (see above). Do not use the figure 45 req/min.

Live check 2026-08-17: `curl https://api.uspto.gov/api/v1/patent/applications/search?q=Utility` without a key → `HTTP 401` (endpoint is live, requires auth).

## What it returns

JSON. Patent applications and Patent File Wrapper data — application metadata, continuity data, transactions, patent term adjustment, foreign priority, assignments, documents (PDF/XML/DOC), plus Bulk Datasets, PTAB Trials/Appeals/Interferences, Office Action texts and citations.

```json
{
  "patentFileWrapperDataBag": [
    {
      "applicationNumberText": "16123456",
      "applicationMetaData": {
        "inventionTitle": "Example Title",
        "filingDate": "2021-05-01",
        "applicationTypeLabelName": "Utility",
        "applicationStatusDescriptionText": "Patented Case"
      }
    }
  ]
}
```

## When to use

- Search and metadata for US patent applications (including pre-grant publications) by title, filing date, status, applicant
- Continuity data — links between parent/child applications
- Office Action texts and citations (grounds for refusal, cited prior art)
- PTAB proceedings (trials, appeals, interferences)
- Bulk download of Patent File Wrapper documents (PDF/XML/Word)

## When not to use

- A quick one-off lookup without willingness to go through USPTO.gov registration + ID.me verification (a process of at least several minutes, for non-US users a video call with ID.me)
- Full-text search over granted patents with claims/description text as the main task — Google Patents / Espacenet is a better fit for that (see Combine with), ODP focuses on the file wrapper and metadata
- When you are not prepared to partially disclose your identity through ID.me — for an organization this may be a blocker

## Auth setup

1. Create a USPTO.gov account: https://account.uspto.gov (email + code confirmation, the code expires in 48 hours)
2. Create an ID.me account and pass identity verification (self-service or live video call; for users outside the US — a video call plus documents in English is mandatory)
3. Link the USPTO.gov and ID.me accounts through "Manage API Key" in ODP, get the API key
4. In env: `export USPTO_ODP_API_KEY="..."`
5. The key does not expire if used at least once a year; after 90 days of non-use it is deleted automatically

Request: `-H 'X-API-KEY: <USPTO_ODP_API_KEY>'`

## Query patterns

### Simplified search (GET, query string)

```
GET /api/v1/patent/applications/search?q=Utility
GET /api/v1/patent/applications/search?q=applicationMetaData.inventionTitle:Apple*%20AND%20applicationMetaData.filingDate:[2021-01-01%20TO%202022-12-01]&offset=0&limit=25
```

### Advanced search (POST, JSON body, powered by OpenSearch)

```
POST /api/v1/patent/applications/search
{
  "q": "Nanobody",
  "filters": [
    {"name": "applicationMetaData.applicationTypeLabelName", "value": ["Utility"]}
  ],
  "rangeFilters": [
    {"field": "applicationMetaData.filingDate", "valueFrom": "2022-01-01", "valueTo": "2023-12-31"}
  ],
  "pagination": {"offset": 0, "limit": 25},
  "sort": [{"field": "applicationMetaData.filingDate", "order": "Desc"}]
}
```

### Documents for a given application

```
GET /api/v1/patent/applications/{applicationNumber}/documents
GET /api/v1/download/applications/{applicationNumber}/{documentId}.pdf
```

## Example queries

A real, officially documented one (not verified live with a key — an API key is needed):

```
GET https://api.uspto.gov/api/v1/patent/applications/search?q=applicationMetaData.inventionTitle:Apple*%20AND%20applicationMetaData.filingDate:[2021-01-01%20TO%202022-12-01]&offset=0&limit=25
```

Live without a key confirms that the endpoint responds (401, not 404/timeout):

```
curl "https://api.uspto.gov/api/v1/patent/applications/search?q=Utility"
→ HTTP 401
```

## Limitations

- US applications/patents only (USPTO), no international coverage (for that, EPO/WIPO)
- Heavy onboarding: ID.me verification is not just "get a key" but a full identity check
- Bulk document downloads are tightly quota'd (20/year per file) — for large volumes use the Bulk Datasets Downloads API separately, not the Documents API
- Large files (>100 MB) stream with a delay of up to 60 sec, files >250 MB sometimes time out even after 10 minutes
- The API key is bound to one account, it cannot be shared, parallel requests with one key are blocked

## Combine with

- **EPO OPS** (`epo_ops.md`) — for European equivalents and the patent family
- **EPO Linked Open Data** (`epo_lod.md`) — for SPARQL queries over European patent relations
- **Google Patents / Espacenet** (via WebFetch) — for full-text search of claims/description over granted patents, if the ODP file-wrapper focus does not fit

## Fallback if API down or rate-limited

1. Wait for `Retry-After`/until the weekly quota resets (reset — Sunday 00:00 UTC)
2. Data without a key: https://data.uspto.gov offers direct download of bulk data products without an API key (slower, no programmatic search)
3. ⚠️ **PatentsView (`search.patentsview.org`) is dead** — the domain does not resolve (DNS failure, verified 2026-08-17), not merely a 410. PatentsView officially shut down on 20 March 2026 and migrated its data into USPTO ODP bulk datasets. Do not try to use PatentsView as a fallback or alternative — it is the same ODP, just under the old URL.
4. WebFetch to https://ppubs.uspto.gov/pubwebapp/ (Patent Public Search UI) as the last option for manual search
