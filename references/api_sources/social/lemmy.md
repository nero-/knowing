<!-- translated from upstream/references/api_sources/social/lemmy.md @ e233797 — see docs/TRANSLATION.md -->
# Lemmy API (Fediverse alternative to Reddit)

## Overview

- **Endpoint base:** Depends on the instance — `https://lemmy.ml/api/v3/` (one of the large ones)
- **Auth:** None for public read
- **Free tier:** Unlimited (politely)
- **Docs:** https://join-lemmy.org/api/
- **Coverage:** Every Lemmy instance is its own; popular ones: lemmy.ml, lemmy.world, beehaw.org

## Query patterns

### Search posts

```
GET /api/v3/search?q={query}&type_=Posts&sort=TopAll&limit=20
```

### Community posts

```
GET /api/v3/post/list?community_name={community}&sort=Hot&limit=20
```

### Federated search (across instances)

Each instance sees federated content — a search in lemmy.ml will return posts from other instances it subscribes to.

## Use cases

- An alternative view on technical topics (when Reddit is cancelled or skews)
- Tech-savvy audience opinions (Lemmy users tend to be technical)
- Decentralized discourse

## Limitations

- Much smaller than Reddit
- Coverage uneven — popular topics are there, niche ones weaker
- Each instance is a separate API endpoint

## Combine with

- **Reddit** — primary social
- **HN** — for tech-specific
- **Mastodon API** — for a microblogging alternative

## Notes

- Lemmy is still growing — useful for topics where Reddit has become toxic or ban-happy
- Useful for a balanced opposition voice
