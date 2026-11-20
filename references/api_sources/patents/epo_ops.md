<!-- translated from upstream/references/api_sources/patents/epo_ops.md @ e233797 — see docs/TRANSLATION.md -->
# EPO Open Patent Services (OPS)

## Overview

- **Endpoint base:** `https://ops.epo.org/3.2/rest-services/`
- **Auth:** OAuth 2.0 (`client_credentials` grant) — you need a Consumer Key + Consumer Secret from free registration at developers.epo.org
- **Free tier:** up to 4 GB of traffic per week free ("free threshold"); a week is calendar, Mon 00:00 – Sun 24:00 GMT. Beyond that — a paid annual subscription (exact prices are in the brochure "EPO Patent Information - Price list", the fair-use page itself does not state a price)
- **Rate limit:** maximum traffic speed ≈ 1 Mbit/sec for both OPS and the European Publication Server REST API. Only this speed throttling and the weekly volume quota (4 GB) are officially documented; more granular figures of the "N req/min" kind were not found in EPO's official documentation — third-party client libraries (python-epo-ops-client, Go epo-ops) mention separate per-hour throttling with a 1-minute sliding window, but the exact req/hour number is **not confirmed as of 2026-08-17**
- **Docs:** https://www.epo.org/en/searching-for-patents/data/web-services/ops , https://developers.epo.org/
- **Status page:** https://www.epo.org/en/service-support/status-online-services (Availability of online services, mentioned in the fair-use charter as the source of info about scheduled OPS maintenance)
- **Verified:** 2026-08-17

Live check 2026-08-17:
```
curl -X POST https://ops.epo.org/3.2/auth/accesstoken -d "grant_type=client_credentials"
→ HTTP 401 {"message":"Client identifier is required"}

curl https://ops.epo.org/3.2/rest-services/published-data/search?q=ti=plastic
→ HTTP 403 {"code":403,"message":"This request has been rejected due to the violation of Fair Use policy","moreInfo":"https://www.epo.org/service-support/ordering/fair-use.html"}
```
Both endpoints are live and respond as expected (auth and rest-services do not pass without a token).

Official text of the fair-use policy (epo.org/service-support/ordering/fair-use.html, verified live 2026-08-17): *«Downloading data via OPS is free of charge up to a maximum data volume of 4 GB per week ("free threshold")»*, and also *«the maximum traffic volume allowed is approximately 1 Mbit per second»*.

## What it returns

A standardized XML interface (RESTful) over the same databases as Espacenet and the European Patent Register: bibliographic data, worldwide legal status, full text, images. JSON is available via `Accept: application/json` (confirmed by third-party OPS v3.2 client libraries; the official page with the Accept header specification could not be retrieved — EPO pages with that level of detail do not serve static HTML for WebFetch).

## When to use

- Patent data on 100M+ documents from the EPO databases, including worldwide legal status
- Patent family — links between patents from different jurisdictions for one invention
- Bibliographic + full text + images from one API, without having to combine several sources
- Integrating EPO data into your own application/database

## When not to use

- A one-off manual search for a single patent — a WebFetch to the Espacenet UI (`worldwide.espacenet.com`) is simpler and needs no OAuth setup
- Applications with unpredictable high traffic volume without willingness to pay for a subscription beyond 4 GB/week
- You need ready-made JSON without parsing XML as the main scenario — OPS is historically XML-first, JSON is supported but less documented

## Auth setup

1. Register at https://developers.epo.org/user/register (free, ~5 minutes)
2. Log in, create a test app in the Developer's Console → get a Consumer Key and Consumer Secret
3. In env:
   ```
   export EPO_OPS_CONSUMER_KEY="..."
   export EPO_OPS_CONSUMER_SECRET="..."
   ```
4. Get an access token (OAuth2 client_credentials, Basic Auth header with key:secret in base64):
   ```
   POST https://ops.epo.org/3.2/auth/accesstoken
   Authorization: Basic base64(EPO_OPS_CONSUMER_KEY:EPO_OPS_CONSUMER_SECRET)
   Content-Type: application/x-www-form-urlencoded
   Body: grant_type=client_credentials
   ```
   Returns `access_token`, use it as `Authorization: Bearer <token>` in subsequent requests.

## Query patterns

### Published data search

```
GET /3.2/rest-services/published-data/search?q={CQL query}
```

### Bibliographic data by publication number

```
GET /3.2/rest-services/published-data/publication/epodoc/{number}/biblio
```

### Full-text (description/claims)

```
GET /3.2/rest-services/published-data/publication/epodoc/{number}/fulltext
```

### Patent family

```
GET /3.2/rest-services/family/publication/epodoc/{number}
```

### Legal status

```
GET /3.2/rest-services/legal/publication/epodoc/{number}
```

## Example queries

CQL search by title (the request structure is confirmed by the OPS documentation; an OAuth token is needed to get a response — unavailable without registration, so the resulting response was not reproduced live):

```
GET https://ops.epo.org/3.2/rest-services/published-data/search?q=ti=plastic
Authorization: Bearer {access_token}
```

Live check without a token (confirms that the endpoint exists and requires auth, see Overview):
```
curl https://ops.epo.org/3.2/rest-services/published-data/search?q=ti=plastic
→ HTTP 403 (Fair Use policy — in practice this is the standard response to a request without a valid token)
```

## Limitations

- XML-first design, JSON is a secondary format
- The OAuth token must be refreshed (standard client_credentials, the token lifetime was not checked separately — usually time-limited, as in all OAuth2 client_credentials implementations)
- 4 GB/week can be tight for bulk scenarios — then you need a paid tier or direct contact with patentdata@epo.org for large volumes
- EPO's official documentation is poorly served to static HTML parsers (much of the content loads dynamically) — the exact numeric throttling thresholds in req/min could not be re-verified directly, only via the fair-use charter (GB/week + Mbit/sec) and via independent client libraries

## Combine with

- **EPO Linked Open Data** (`epo_lod.md`) — SPARQL over the same data, without OAuth, for lighter/structural queries
- **USPTO ODP** (`uspto_odp.md`) — for US applications and the file wrapper
- **Google Patents** (via WebFetch) — a quick manual cross-check without quotas

## Fallback if API down or rate-limited

1. On a 403 Fair Use policy — wait for the weekly window to reset (Monday 00:00 GMT) or reduce traffic volume
2. EPO Linked Open Data (`epo_lod.md`) — a SPARQL endpoint without OAuth and without a declared weekly quota, covers a subset of the same bibliographic data
3. WebFetch to Espacenet (`worldwide.espacenet.com`) for manual searching of individual patents with no quotas at all
