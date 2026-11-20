<!-- translated from upstream/references/api_sources/search/exa.md @ e233797 — see docs/TRANSLATION.md -->
# Exa.ai API (formerly Metaphor)

## Overview

- **Endpoint base:** `https://api.exa.ai`
- **Auth:** API key (header `x-api-key`)
- **Free tier:** $10 credit on registration, ~1000 searches
- **Paid:** $5/1000 searches typically
- **Docs:** https://docs.exa.ai
- **Unique:** **semantic search** (neural), not keyword matching

## What it returns

JSON with results ranked by semantic similarity to the query.

```json
{
  "results": [
    {
      "title": "...",
      "url": "...",
      "publishedDate": "2024-03-15",
      "author": "...",
      "score": 0.89,
      "id": "exa-id-...",
      "text": "Optional full content if requested"
    }
  ]
}
```

## When to use

- Semantic search — "similar to this article"
- Concept-based queries instead of keywords
- When you do not know the exact terms but know the idea
- Searching for "like this URL but newer" / "a better version of X"

## When not to use

- Exact lookup queries — keyword search is faster
- Real-time news (Exa has a lag)
- You need structured data such as a Wikipedia infobox

## Auth setup

1. https://exa.ai → sign up
2. API key from the dashboard
3. In env: `export EXA_API_KEY="..."`

## Query patterns

Direct call from the skill: `python3 scripts/search_query.py --engine exa --query "..." [--n 10] [--json]`
(reads `EXA_API_KEY` from env, exit 2 if there is no key). Below is the raw HTTP contract
the script implements.

### Neural search

```
POST https://api.exa.ai/search
Headers: x-api-key: {EXA_API_KEY}
Content-Type: application/json

{
  "query": "research methodology for market microstructure",
  "type": "neural",
  "useAutoprompt": true,
  "numResults": 10
}
```

`useAutoprompt: true` — Exa reformulates the query under the hood for better results.

### Find similar

```
POST https://api.exa.ai/findSimilar
{
  "url": "https://example.com/research/paper",
  "numResults": 10
}
```

### Get content of result

```
POST https://api.exa.ai/contents
{
  "ids": ["exa-id-1", "exa-id-2"],
  "text": true,
  "highlights": true
}
```

## Example queries for the deep run

**Phase 4 — find similar to a paper:**

```
POST /findSimilar
{
  "url": "https://arxiv.org/abs/2401.12345",
  "numResults": 15
}
```

**Phase 4 — concept search:**

```
POST /search
{
  "query": "papers explaining how market makers profit from spread in prediction markets",
  "type": "neural",
  "useAutoprompt": true,
  "category": "research paper",
  "numResults": 10
}
```

## Categories filter

Exa can filter by content type:
- `research paper`
- `news`
- `tweet`
- `pdf`
- `github`
- `personal site`
- `linkedin profile`

## Limitations

- Not a replacement for keyword search — for exact queries (specific names, IDs) it hurts
- The index is smaller than Google's
- Cost grows quickly under heavy use

## Combine with

- **Tavily** — for answers with sources
- **Brave Search** — for broader coverage
- **Semantic Scholar** — for academic work but without semantic ranking

## Fallback if API down or rate-limited

1. Tavily with `search_depth: advanced`
2. Brave Search with an include_domains filter
3. Standard WebSearch through the agent harness
