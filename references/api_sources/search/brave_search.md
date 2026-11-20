<!-- translated from upstream/references/api_sources/search/brave_search.md @ e233797 — see docs/TRANSLATION.md -->
# Brave Search API

## Overview

- **Endpoint base:** `https://api.search.brave.com/res/v1/`
- **Auth:** API key (header `X-Subscription-Token`)
- **Free tier:** 2000 queries/month, 1 query/sec
- **Paid:** $3-$5 per 1000 queries
- **Docs:** https://api.search.brave.com/app/documentation
- **Independent index** (not a Google rebrand)

## What it returns

JSON with organic results, news, videos, infobox.

```json
{
  "web": {
    "results": [
      {
        "title": "...",
        "url": "...",
        "description": "...",
        "age": "2 days ago",
        "language": "en",
        "family_friendly": true
      }
    ]
  },
  "news": {...},
  "infobox": {...}
}
```

## When to use

- You need Google-quality search without Google bias
- A privacy-respecting alternative
- Bulk programmatic search

## When not to use

- You need more than 2000 free queries/month
- You need Google specifically (SerpAPI is for that)

## Auth setup

1. https://api.search.brave.com → sign up
2. Get an API key
3. In env: `export BRAVE_SEARCH_API_KEY="BSA..."`

## Query patterns

Direct call from the skill: `python3 scripts/search_query.py --engine brave --query "..." [--n 10] [--json]`
(reads `BRAVE_SEARCH_API_KEY` from env, exit 2 if there is no key). Below is the raw HTTP contract
the script implements.

### Web search

```
GET https://api.search.brave.com/res/v1/web/search?q={query}&count=20
Headers: X-Subscription-Token: {BRAVE_SEARCH_API_KEY}
```

### News search

```
GET https://api.search.brave.com/res/v1/news/search?q={query}&count=20&freshness=pw
```

`freshness`: `pd` (past day), `pw` (past week), `pm` (past month), `py` (past year)

### Goggle (custom rankings)

Brave Goggles let you create a custom ranker:

```
GET https://api.search.brave.com/res/v1/web/search?q={query}&goggles_id={GOGGLE_ID}
```

## Example queries for the deep run

**Phase 4 — landscape research:**

```
GET /web/search?q=eu%20ai%20act%20compliance%20timeline%202026&count=20&freshness=py
```

**Phase 4 — recent news:**

```
GET /news/search?q=duckdb%20release&count=10&freshness=pm
```

## Limitations

- 2000 free queries/month — for deep runs with active sub-agents that is not much
- Fewer "rich features" than Google (no instant answers for everything)
- The index is not as broad as Google's for niche topics

## Combine with

- **Tavily** — for ready-made answers with sources
- **SerpAPI** — if you need Google specifically
- **Exa** — for semantic search

## Fallback if API down or rate-limited

1. Tavily API (its own free tier)
2. Standard WebSearch tool in the agent harness
3. DuckDuckGo through a Brave alternative (but lower quality)
