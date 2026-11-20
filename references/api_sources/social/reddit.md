<!-- translated from upstream/references/api_sources/social/reddit.md @ e233797 — see docs/TRANSLATION.md -->
# Reddit JSON API

## Overview

- **Endpoint base:** `https://www.reddit.com/`
- **Auth:** OAuth is mandatory — anonymous `.json` no longer works
- **Free tier:** not confirmed as of 2026-08-17 (no test OAuth application to check limits; the official support.reddithelp.com page is not served even to WebFetch — 403)
- **Note:** User-Agent alone no longer helps — blocking is by IP reputation/TLS fingerprint regardless of the header (live-confirmed)
- **Docs:** https://www.reddit.com/dev/api/ (not re-verified — reddit.com blocks automated requests to its own endpoints)
- **Coverage:** All public subreddits + posts + comments (access now only through OAuth)
- **Verified:** 2026-08-17

Live check 2026-08-17: `GET https://www.reddit.com/r/programming/.json` without a token → HTTP 403 with the default curl UA, with a custom `knowing/0.4` UA and with a full browser UA (Chrome/120) — in all three cases 403 and an HTML anti-bot stub instead of JSON. The same result on `old.reddit.com` and on `oauth.reddit.com` without a Bearer token (that is the official OAuth data host — also blocked without a valid token). Several independent sources (posts/blogs, May–August 2026, not a Reddit primary source) converge on the date 28–30.05.2026: Reddit closed the unauth `.json` endpoints, citing the anti-scraping Rule 8, and at the same time sharply narrowed the issuance of new OAuth applications for personal/script use. This was not re-verified against an official Reddit source (reddit.com and support.reddithelp.com return 403 to a direct WebFetch/curl from this environment) — but it is consistent with the live result above.

## What it returns

JSON — just add `.json` to the Reddit page URL (given a valid OAuth token; without one — 403, see Overview).

## Auth setup

1. https://www.reddit.com/prefs/apps → create an application (type "script" for personal use)
2. Get the `client_id` and `client_secret`
3. `export REDDIT_CLIENT_ID="..."`
4. `export REDDIT_CLIENT_SECRET="..."`
5. Exchange for a Bearer token: `POST https://www.reddit.com/api/v1/access_token` with HTTP Basic auth (`client_id:client_secret`) and the body `grant_type=client_credentials` (or `password` for the script type with account login/password)
6. After that, requests go to `https://oauth.reddit.com/...` (not `www.reddit.com`) with the header `Authorization: Bearer {token}`

⚠️ It is not confirmed as of 2026-08-17 that a new script application will get working access for personal/research use at all — see the live check in Overview. The token exchange step itself was not tested in this session (no test account).

## Required headers

```
User-Agent: knowing/0.4 (your-contact)
Authorization: Bearer {token}
```

A User-Agent alone, without an OAuth token, no longer works (see Overview).

## Query patterns

⚠️ Below are path/parameter patterns that are structurally current, but since 2026 they require the OAuth host `oauth.reddit.com` + `Authorization: Bearer` instead of anonymous `www.reddit.com`.

### Subreddit posts

```
GET https://www.reddit.com/r/{subreddit}/hot.json?limit=25
GET https://www.reddit.com/r/{subreddit}/top.json?t=year&limit=25
# t=hour/day/week/month/year/all
```

### Search

```
GET https://www.reddit.com/r/{subreddit}/search.json?q={query}&restrict_sr=1&sort=relevance
GET https://www.reddit.com/search.json?q={query}&sort=relevance
```

### Post with comments

```
GET https://www.reddit.com/r/{subreddit}/comments/{id}.json?limit=100
```

### User profile

```
GET https://www.reddit.com/user/{username}/submitted.json
GET https://www.reddit.com/user/{username}/comments.json
```

## Use cases

- Community sentiment
- Opposition research (find critical posts)
- Anecdotal experiences ("my experience with X")
- Real-world implementation pitfalls

## Example queries for the deep run

**Phase 4 — community opposition:**

```
GET https://www.reddit.com/r/kubernetes/search.json?q=migration+regret&restrict_sr=1&sort=relevance&limit=50
```

**Phase 4 — broad search:**

```
GET https://www.reddit.com/search.json?q=postgres+logical+replication+experience&sort=top&t=year
```

## Limitations

- Blocking is aggressive — easy to get rate-limited
- Some subreddits are private/blocked
- Vote manipulation existed historically — sentiment is not ideal
- Old Reddit format is slightly different

## Combine with

- **HN Algolia** — for tech-specific discussion
- **Twitter** (if you have access)
- **Forum search** general via Brave/Tavily

## Fallback

- OAuth Reddit API — the status of access issuance is not confirmed as of 2026-08-17 (see Auth setup); it used to be the "more stable" option, now it is itself in question
- Direct WebFetch with a good User-Agent — does not help, the block is at the IP/TLS level, not the UA (live-verified 2026-08-17)
- Pushshift.io (archive, sometimes works) — not re-checked in this round

## Notes

- ⚠️ Outdated: `.json` after a Reddit URL WITHOUT auth no longer works — live-verified 2026-08-17, HTTP 403 on every variant tested. Until ~05.2026 this was true ("the simplest research API"), now OAuth is needed
- Good for the opposition voice in phase 4 (counter-arguments) — if there is any access at all
- Reddit search relevance is poor — Brave/SerpAPI with `site:reddit.com` is better (requires no Reddit auth, remains a working fallback)
