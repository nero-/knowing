<!-- translated from upstream/references/api_sources/patents/wipo.md @ e233797 — see docs/TRANSLATION.md -->
# WIPO PATENTSCOPE

## Overview

- **Endpoint base:** no public free API. PATENTSCOPE is a web search engine (`https://patentscope.wipo.int/search/en/search.jsf`) plus a paid SOAP/WSDL web service for programmatic access
- **Auth:** none for the web interface (public, but with anti-bot protection, including CAPTCHA); for the programmatic SOAP API — a paid subscription with issued credentials
- **Free tier:** **there is no free programmatic API.** There is a free web search (for people, not for automation) and three paid products: SOAP web service (search) — 600 CHF/year, SOAP web service (full, batch download + IASR) — 2000 CHF/year, PCT-Bibliographic bulk feed (SFTP, metadata) — from 400 CHF/year, PCT-Text bulk (full-text + images) — 3900–19500 CHF/year depending on volume
- **Rate limit:** for the free web interface the ToS treats "more than 10 search-related actions per minute from one IP" as excessive use; automated queries, bulk downloading, bulk copying and web scraping are explicitly prohibited by the terms of use. For the paid SOAP API no numeric rate limit was found in public sources
- **Docs:** https://www.wipo.int/en/web/patentscope/data/index (PCT Data Products and Services), https://www.wipo.int/en/web/patentscope/data/terms_patentscope (Terms of Use)
- **Status page:** not found
- **Verified:** 2026-08-17

Live check 2026-08-17: opening `patentscope.wipo.int` in a browser immediately serves a captcha ("Please select the picture with stars") — entering and solving the captcha is prohibited (bot-detection bypass — prohibited action), so the web interface was not live-tested beyond loading the page. The Terms of Use (`.../data/terms_patentscope`) and the PCT Data Products page (`.../data/index`) load normally and are the official source for the figures above (verified live).

## What it returns

Web interface: HTML with search result pages (PCT applications + national/regional collections, if the office participates). Paid SOAP API: XML per the WSDL schema — bibliographic data, status (IASR — International Application Status Report), full text and images (for the full-access tier). Bulk SFTP: XML + TIFF images in batches.

## When to use

- You need an exploratory search over international (PCT) applications manually, occasionally, without automation — the web interface is free for that
- The organization is willing to pay 400–19500 CHF/year for structured programmatic access to PCT data and the task volume justifies it
- You need the official international status of an application (IASR) programmatically — only through the paid SOAP API

## When not to use

- **Do not try to build an agentic/automated workflow on top of free PATENTSCOPE** — the ToS explicitly prohibits automated queries, bulk acquisition, bulk downloading, bulk storing, bulk copying, web scraping and "any other abusive use". This is not a grey area: on excess WIPO explicitly reserves the right to block access by IP
- There is no budget for a paid subscription — then WIPO is not a suitable programmatic source at all; use USPTO ODP + EPO OPS/LOD, which together cover most of the same international patent landscape for free (EPO family data includes PCT applications)
- You need fast bulk volume (hundreds+ of queries) right now — the web interface serves a captcha and cuts you off at the threshold of 10 actions/min per IP

## Auth setup

For the paid SOAP API: the subscription is arranged directly through WIPO (contact/order process, details at https://www.wipo.int/en/web/patentscope/data/index), personal credentials for the WSDL endpoint are issued. There is no single API key in the "got a token in 5 minutes" style — this is a commercial contract, so there is no point setting up an env var in the `FRED_API_KEY` style for it: if the organization takes out a subscription, the credentials are issued individually and stored like any other secret (`WIPO_PATENTSCOPE_CREDENTIALS` — as a naming guideline, if you decide to add one).

For the free web interface no auth is needed, but automation is likewise prohibited by the ToS (see When not to use).

## Query patterns

There are no programmatic query patterns for free access — there is no API as such. The only legitimate pattern for an agent: a single manual WebFetch/view of a search result page by a human, without a request loop.

For the paid SOAP API (per the documentation, without access for a live check — no subscription):

```
SOAP/WSDL call for PATENTSCOPE publication documents
(IASR retrieval, batch document download — per WIPO PCT Patentscope Web-services for Offices)
```

## Example queries

There is no free programmatic query that could honestly be demonstrated as a working example. The only example verifiable without a CAPTCHA is a direct link to an application card (for a human/agent WebFetch one-off, not in a loop):

```
https://patentscope.wipo.int/search/en/detail.jsf?docId={WO_DOCUMENT_ID}
```
(the URL pattern is confirmed by public WIPO documentation; the live fetch itself was not completed because of bot detection on the search entry page — see Overview)

## Limitations

- No free programmatic access — this is the only one of the four patent sources in the catalog with no free tier for the API at all
- The web interface is actively protected against automated access (CAPTCHA already on the search entry page)
- OCR-based full text (claims/description) — WIPO itself warns in the ToS that OCR is error-prone
- The paid SOAP/WSDL is a legacy protocol, with no modern REST/JSON equivalent as of 2026-08-17; WIPO has not announced a migration date to REST

## Combine with

- **EPO OPS** (`epo_ops.md`) and **EPO Linked Open Data** (`epo_lod.md`) — EPO covers PCT applications as part of the patent family for free, this is the main free alternative to WIPO for international data
- **USPTO ODP** (`uspto_odp.md`) — for the US national phase of the same PCT application

## Fallback if API down or rate-limited

Since there is no free API, "down or rate-limited" applies only to the web interface:

1. On a captcha/block — do not try to bypass it (bypassing a CAPTCHA is prohibited); wait and retry as a single manual request later
2. EPO OPS/LOD (`epo_ops.md`, `epo_lod.md`) — cover PCT applications as the international phase inside EPO family data, without a CAPTCHA and without a paid subscription
3. Google Patents (via WebFetch) — often indexes the same PCT publications (WO numbers) without anti-bot protection at the PATENTSCOPE level
