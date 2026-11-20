<!-- translated from upstream/references/api_sources/academic/openalex.md @ e233797 — see docs/TRANSLATION.md -->
# OpenAlex API

## Overview

- **Endpoint base:** `https://api.openalex.org`
- **Auth:** A key is not required for basic queries — live-verified 2026-08-17: `GET /works?per-page=1` without a key → HTTP 200. Since the start of 2026 an optional free API key officially exists (gives a 10× budget + priority), without a key you get a narrower "keyless" budget
- **Free tier:** NOT unlimited — a credit-based system was introduced in 2026. Without a key: live headers on 2026-08-17 showed `x-ratelimit-limit: 1000` credits with a daily reset (~midnight UTC), a list query costs 1 credit by observation (the exact figure is not officially documented anywhere — this is direct observation, not a declared limit). With a free key: officially "$1 API budget per day" per account, no card needed (help.openalex.org/hc/en-us/articles/24397762024087-Pricing, page updated 2026-08-11)
- **Rate limit:** 100 req/sec — a hard ceiling for all tiers, officially documented (help.openalex.org/api/authentication). The old figure "10 req/sec, 100k/day" was not confirmed either in the docs or in live headers
- **Docs:** https://docs.openalex.org (redirects to https://help.openalex.org)
- **Coverage:** 250M+ scholarly works (replaced Microsoft Academic) — a live query on 2026-08-17 returned `"count": 324389590` in `meta`
- **Verified:** 2026-08-17

## What it returns

JSON with metadata + citations graph + author networks + institutional affiliations.

```json
{
  "id": "https://openalex.org/W...",
  "doi": "https://doi.org/10.1234/...",
  "title": "...",
  "authorships": [{"author": {...}, "institutions": [...]}],
  "publication_year": 2024,
  "cited_by_count": 142,
  "referenced_works": ["W...", "W..."],
  "concepts": [{"display_name": "...", "level": 2, "score": 0.85}],
  "open_access": {"is_oa": true, "oa_url": "..."}
}
```

## When to use

- Citation graph analysis at massive scale (10k+ papers)
- Find institutional collaborations (universities, countries)
- Concept-based discovery (OpenAlex adds ML-derived concept tags)
- Research metrics — find most-cited in a field

## When not to use

- A simple paper lookup — Semantic Scholar has a cleaner API
- You need abstracts — OpenAlex has inverted_index abstracts (reconstruction needed)

## Auth setup

A key is not required for basic/non-commercial queries (live-confirmed 2026-08-17), but since 2026 it is officially recommended — a 10× daily budget instead of the narrow keyless limit:

1. https://openalex.org/settings/api → create an account (~30 sec), copy the key
2. `export OPENALEX_API_KEY="..."`
3. The exact format for passing the key (query parameter vs header) was not re-verified live in this session — there is no test key, see the current docs at help.openalex.org

Without a key the politeness pool works:

```
GET /works?search={query}&mailto=your@email.com
```

This still gives priority access within the keyless budget, but does not replace a key in terms of volume.

## Query patterns

### Search works

```
GET /works?search={query}&per-page=50
```

### Filter by year, OA, type

```
GET /works?search={query}&filter=publication_year:2020-2026,is_oa:true,type:journal-article&per-page=50
```

### Get work by DOI

```
GET /works/doi:10.1234/example
```

### Citation network

```
GET /works/{work-id}?select=referenced_works,cited_by_count
```

### Author papers + h-index

```
GET /authors/{author-id}?select=works_count,cited_by_count,summary_stats
GET /works?filter=author.id:{author-id}&per-page=200
```

### Institution analysis

```
GET /works?filter=institutions.id:{institution-id}&group_by=publication_year
```

### Concept hierarchy

```
GET /concepts/{concept-id}
GET /works?filter=concepts.id:{concept-id}&per-page=200
```

## Example queries for the deep run

**Phase 4 — get all recent papers in a niche concept:**

```
GET /works?filter=concepts.display_name.search:vertical+farming,publication_year:2022-2026,is_oa:true&per-page=100&mailto=research@example.com
```

**Phase 4 — citation graph of seminal work:**

```
GET /works/W{id}?select=referenced_works
# Then for each referenced work:
GET /works/W{ref_id}?select=title,authors,publication_year
```

## Cursor pagination

For large result sets:

```
GET /works?search={query}&per-page=200&cursor=*
# Response includes next_cursor
GET /works?search={query}&per-page=200&cursor={next_cursor}
```

## Abstracts (inverted_index format)

OpenAlex stores abstracts as an inverted index (token positions). Reconstruct:

```python
# pseudo-code
abstract_words = {}
for word, positions in inverted_index.items():
    for pos in positions:
        abstract_words[pos] = word
abstract = " ".join(abstract_words[i] for i in sorted(abstract_words))
```

Or use the `mailto=` parameter — some responses include a reconstructed abstract.

## Limitations

- The abstract inverted_index format is awkward for an agent
- ML-derived concepts are sometimes noisy
- Smaller community than Semantic Scholar (less maintenance attention)
- The free tier is no longer unlimited (since 2026) — under intensive use without a key you can hit the daily keyless limit (the exact figure is not officially documented, live observation 2026-08-17 — see Overview); for serious volume you need a free key

## Combine with

- **Semantic Scholar** — cleaner API, similar coverage
- **CrossRef** — for DOI lookup
- **OurResearch Unpaywall** — for extra OA URLs

## Fallback if API down or rate-limited

1. Semantic Scholar API (similar coverage)
2. CrossRef for DOI metadata
3. Direct DOI lookup via doi.org redirects

## Notes

- OpenAlex has the most complete citation graph in open data
- Excellent for research network analysis
- Without a key a basic volume is available (live observation 2026-08-17: on the order of 1000 credits/day); for substantial volume — a free key with a $1/day budget, no card needed
- Unique in its ability to filter by institutions / countries / concepts at massive scale
