<!-- translated from upstream/references/api_sources/search/tavily.md @ e233797 — see docs/TRANSLATION.md -->
# Tavily API

## Overview

- **Endpoint base:** `https://api.tavily.com`
- **Auth:** API key (header `api_key` or body field)
- **Free tier:** 1000 requests / month
- **Rate limit:** flexible on the free plan
- **Docs:** https://docs.tavily.com
- **Status page:** https://status.tavily.com

## What it returns

JSON with ready-made **answers + sources**. Tavily is a search API built specifically for LLM agents.

```json
{
  "query": "what is meta research methodology",
  "answer": "Meta-research is the study of research itself...",
  "results": [
    {
      "title": "Meta-research - Wikipedia",
      "url": "https://en.wikipedia.org/wiki/Meta-research",
      "content": "Truncated content of the page...",
      "score": 0.95,
      "raw_content": "Full content if include_raw_content=true"
    }
  ]
}
```

## When to use

- You need a **ready-made answer**, not just a list of links
- Search for LLM/agent context (Tavily filters out spam and ads)
- When WebSearch + manual WebFetch is too many steps

## When not to use

- You need maximum coverage — Brave/SerpAPI are better
- You need URLs only, without summaries — the response is too heavy

## Auth setup

1. Registration: https://tavily.com
2. API key from the dashboard
3. In env: `export TAVILY_API_KEY="tvly-..."`

## Query patterns

Direct call from the skill: `python3 scripts/search_query.py --engine tavily --query "..." [--n 10] [--json]`
(reads `TAVILY_API_KEY` from env, exit 2 if there is no key). Below is the raw HTTP contract
the script implements (basic search, without `include_answer`/`include_domains`).

### Basic search

```
POST https://api.tavily.com/search
Content-Type: application/json

{
  "api_key": "{TAVILY_API_KEY}",
  "query": "{your query}",
  "search_depth": "basic",
  "max_results": 5
}
```

### Advanced search (deeper, slower)

```
POST https://api.tavily.com/search
{
  "api_key": "{TAVILY_API_KEY}",
  "query": "{your query}",
  "search_depth": "advanced",
  "include_answer": true,
  "include_raw_content": true,
  "max_results": 10,
  "include_domains": ["arxiv.org", "scholar.google.com"],
  "exclude_domains": ["pinterest.com"]
}
```

### Get content from specific URL

```
POST https://api.tavily.com/extract
{
  "api_key": "{TAVILY_API_KEY}",
  "urls": ["https://example.com/article"]
}
```

## Example queries for the deep run

**Phase 4 — academic search:**

```
POST /search
{
  "query": "postgres logical replication performance trade-offs",
  "search_depth": "advanced",
  "include_answer": true,
  "include_domains": ["arxiv.org", "ssrn.com", "researchgate.net"],
  "max_results": 8
}
```

**Phase 4 — opposition search:**

```
POST /search
{
  "query": "kubernetes migration regrets postmortem",
  "search_depth": "advanced",
  "include_answer": false,
  "include_domains": ["reddit.com", "twitter.com", "medium.com"]
}
```

## Limitations

- Free tier 1000 req/month — for deep runs with 5 sub-agents you can exceed it in a month if you use it heavily
- `include_raw_content` takes more tokens in the response
- Answer quality depends on the topic — weaker on technical topics than on mainstream ones

## Combine with

- **Brave Search** — if you need more coverage
- **Exa.ai** — for semantic search over similar documents
- **SerpAPI** — if you specifically need Google results

## Fallback if API down or rate-limited

1. Brave Search API (paid alternative)
2. Exa.ai (semantic alternative, free tier)
3. Standard WebSearch through the agent harness WebSearch tool
4. Manual WebFetch to specific domain sources

## Notes

- Tavily is a favorite among AI agents because of the `include_answer` field, which returns a synthesized answer alongside sources
- Works well with `include_domains` filters for targeted search
- Unlike the Google Search API, Tavily requires no Custom Search Engine setup
