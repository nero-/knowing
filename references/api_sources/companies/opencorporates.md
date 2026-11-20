<!-- translated from upstream/references/api_sources/companies/opencorporates.md @ e233797 — see docs/TRANSLATION.md -->
# OpenCorporates API

## Overview

- **Endpoint base:** `https://api.opencorporates.com/v0.4/`
- **Auth:** ⚠️ A token is mandatory — anonymous access no longer exists. Live-verified 2026-08-17: `GET /companies/search?...` and `GET /companies/{jurisdiction}/{number}` without a token → HTTP 401, body `{"error":{"message":"Invalid Api Token. Please check your OpenCorporates account"}}`
- **Free tier:** There is no self-serve free tier. The official pricing page (opencorporates.com/pricing/, checked 2026-08-17) starts with a paid plan. Separately there is a no-charge programme for investigative journalists, NGOs, universities and anti-corruption research groups — but by manual application, not self-serve and not automatic
- **Paid:** Essentials £2 250/year (£225/mo, up to 500 calls/mo, 200/day), Starter £6 600/year (2 500/mo, 500/day), Basic £12 000/year (5 000/mo, 1 000/day), Enterprise — custom price
- **Docs:** https://api.opencorporates.com
- **Coverage:** 200M+ companies from company registries in 130+ countries
- **Verified:** 2026-08-17

## What it returns

JSON with data from official company registries — incorporation date, officers, addresses, filings.

```json
{
  "results": {
    "company": {
      "name": "Apple Inc.",
      "company_number": "C0806592",
      "jurisdiction_code": "us_ca",
      "incorporation_date": "1977-01-03",
      "officers": [...],
      "registered_address": {...}
    }
  }
}
```

## Auth setup

1. https://opencorporates.com/pricing/ → a paid plan (Essentials — from £2250/year) OR an application for free access for journalists/NGOs/researchers/anti-corruption groups through OpenCorporates contacts (reviewed manually, not instantly)
2. `export OPENCORPORATES_API_KEY="..."`
3. Pass it as the `api_token={key}` query parameter (the current format was not re-verified live — there is no test token; check against the current docs at api.opencorporates.com)

## Query patterns

### Search companies

```
GET /companies/search?q={query}&country_code=US&per_page=20
```

### Company details

```
GET /companies/{jurisdiction}/{company_number}
# Example: /companies/us_ca/C0806592 (Apple)
```

### Officer search

```
GET /officers/search?q={name}&per_page=20
```

## Use cases

- Find official company existence (vs marketing claims)
- Track officer/director relationships
- Verify incorporation dates
- Find parent companies, subsidiaries

## Limitations

- ⚠️ No longer a free API (live-confirmed 2026-08-17) — a paid tier from £2250/year, or a grant application for journalists/NGOs/anti-corruption groups. Do not use it as the default "free fallback"
- Not financial data — registry facts only
- Coverage uneven — UK/EU strong, US weaker (state-level)
- Some jurisdictions lag

## Combine with

- **Crunchbase** — for funding history
- **Companies House** (UK) — more detail for the UK
- **SEC EDGAR** — for US public companies

## Fallback

- Direct national registries (Companies House, Bundesanzeiger, etc.)
- HTML scraping of company official pages
