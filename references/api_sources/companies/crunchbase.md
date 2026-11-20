<!-- translated from upstream/references/api_sources/companies/crunchbase.md @ e233797 — see docs/TRANSLATION.md -->
# Crunchbase Basic API

## Overview

- **Endpoint base:** `https://api.crunchbase.com/api/v4/`
- **Auth:** API key (`user_key` query parameter or `X-cb-user-key` header — both confirmed by the official docs at data.crunchbase.com/docs/using-the-api)
- **Free tier:** no self-serve free purchase/trial found as of 2026-08-17. The official docs send you straight to "Contact us to explore API pricing" — the full API is only available under an Enterprise/Applications licence, custom price. A "Crunchbase Basic" plan is mentioned, limited to a subset of "Basic APIs" — its price is not published anywhere
- **Paid:** not confirmed as of 2026-08-17. Neither "$99/mo Basic" (our old figure) nor "$49/mo" (from external reconnaissance) appeared on the official pages about.crunchbase.com/products/data-licensing and data.crunchbase.com/docs/using-the-api — both send you to a sales conversation without numbers. It looks like both numbers are actually about a **Crunchbase Pro** subscription (the web search/export platform) — a different product, not the Data API
- **Docs:** https://data.crunchbase.com/docs/getting-started
- **Coverage:** Startup data — funding rounds, founders, acquisitions, valuations
- **Verified:** 2026-08-17

## What it returns

JSON with organization data, funding events, people, news.

## Auth setup

1. https://about.crunchbase.com/products/data-licensing → "Contact us" (no self-serve found as of 2026-08-17; `www.crunchbase.com/api` from an older version of this file now blocks a direct curl request — 403)
2. `export CRUNCHBASE_API_KEY="..."`

## Query patterns

### Organization details

```
GET /entities/organizations/{uuid}?field_ids=name,short_description,founded_on,total_funding_amount&user_key={key}
```

### Search organizations

```
POST /searches/organizations
Body: {
  "query": [{"type": "predicate", "field_id": "industries", "operator_id": "includes", "values": ["fintech"]}],
  "field_ids": ["name", "short_description", "total_funding_amount"],
  "limit": 50
}
```

### Funding rounds

```
GET /entities/funding_rounds/{uuid}
```

## Example queries for the deep run

**Phase 4 — competitive landscape:**

```
POST /searches/organizations
{
  "query": [
    {"type": "predicate", "field_id": "industries", "operator_id": "includes", "values": ["prediction markets"]},
    {"type": "predicate", "field_id": "founded_on", "operator_id": "gte", "values": ["2018-01-01"]}
  ],
  "field_ids": ["name", "total_funding_amount", "investor_identifiers", "founded_on"],
  "limit": 50
}
```

## Limitations

- **Paid** for serious use, the price is on request from sales (custom, not published)
- A free trial is not mentioned in the current public docs (not confirmed as of 2026-08-17, it was in an older version of this file)
- Data quality is better for US/EU startups, weaker for Asia

## Combine with

- **OpenCorporates** — for company registry data (⚠️ no longer free — paid since 2026, from £2250/year, or a grant application for journalists/NGOs; see `opencorporates.md`)
- **PitchBook** — alternative (paid, comprehensive)
- **AngelList/Wellfound** — for startup jobs

## Fallback

- HTML scrape of Crunchbase profiles
- Latka SaaS revenue database
- The company's own about page + LinkedIn
