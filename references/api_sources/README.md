<!-- translated from upstream/references/api_sources/README.md @ e233797 — see docs/TRANSLATION.md -->
# API sources — README

How to use the API catalog.

## API file template (for each entry)

```markdown
# <API Name>

## Overview

- **Endpoint base:** `https://api.example.com/v2/`
- **Auth:** none / API key / OAuth / Bearer token
- **Free tier:** 100 req/day / unlimited / N/A
- **Rate limit:** 10 req/sec
- **Docs:** `https://docs.example.com`
- **Status page:** `https://status.example.com`

## What it returns

Structured JSON. An example response for a typical request.

## When to use

- Use case 1
- Use case 2

## When not to use

- Edge case where this is wrong choice

## Auth setup

If a key is needed — where to get it, which permissions.

## Query patterns

### Search/lookup
\`\`\`
GET /v2/search?q={query}&limit=20
\`\`\`

### Bulk
\`\`\`
POST /v2/bulk
Body: { "ids": [...] }
\`\`\`

## Example queries

Concrete queries with example JSON responses (truncated).

## Limitations

- Geographic coverage
- Data lag (real-time / 1 day / 1 week)
- Missing fields
- Known issues

## Combine with

- Related APIs to triangulate
- Related HTML sources in `stat_sources/` for fallback

## Fallback if API down or rate-limited

1. Cached responses (if any)
2. Alternative API
3. HTML source from `stat_sources/`
```

## Auth strategy for an agent

The skill **does not store keys**. When an agent needs an API with a key:

1. **First** check the environment variables:
   - `FRED_API_KEY`, `GITHUB_TOKEN`, `NEWSAPI_KEY`, `BRAVE_API_KEY`, etc.
2. If there is no key → fall back to the free version (no auth) or to an HTML source
3. **Never** ask the user for a key inline — ask them to add it to env and restart

Example agent prompt:

```
I will try to use the FRED API. Checking $FRED_API_KEY...
Not found → fall back to HTML parsing of fred.stlouisfed.org via WebFetch.

To speed up future research with FRED:
1. Get a free key: https://fred.stlouisfed.org/docs/api/api_key.html
2. Add to ~/.zshrc or ~/.bashrc:
   export FRED_API_KEY="your-key-here"
3. Restart the shell and the agent harness
```

## Free tier dispatch logic

```
if API X is needed:
  if there is an API key in env:
    → use the API
  else if there is a free tier without a key:
    → use the free tier
  else:
    → fall back to the HTML version from stat_sources/<category>.md
    → mark in sources/NN.md: access: html-fallback (api blocked)
```

## Rate limit handling

On hitting a 429 (rate limit):

1. Wait the time specified in the `Retry-After` header
2. If the wait is > 30 sec → fall back to HTML or an alternative API
3. Mark in `sources/NN.md` notes: `rate-limited at <timestamp>, fell back to <source>`

## API quality grading

In `sources/NN.md` for API-obtained sources:

- `channel: api-direct`
- `access:` one of:
  - `api-free-no-key` — the best option
  - `api-free-with-key` — requires setup but free
  - `api-paid` — paid, used because free did not cover it
  - `api-fallback-html` — the API did not work, fell back to HTML

## When to add a new API to the catalog

Criteria for a PR:

- The API has been working stably for >1 year
- It has official documentation
- It has a free tier OR fills a unique gap (no free alternative)
- It returns structured JSON/XML
- It is not deprecated and not "beta" with aggressive breaking changes

## Antipatterns

- ❌ Documenting an API without checking that it works
- ❌ Ignoring rate limits — you need to know the limits
- ❌ Hardcoding keys in query templates — always through env
- ❌ Duplicating stat_sources/ — an API entry must offer something qualitatively different (programmatic access), not just another URL
- ❌ Adding an API without a fallback strategy
