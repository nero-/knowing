<!-- translated from upstream/references/api_sources/patents/epo_lod.md @ e233797 — see docs/TRANSLATION.md -->
# EPO Linked Open Data

## Overview

- **Endpoint base:** `https://data.epo.org/linked-data/query` (SPARQL endpoint, Apache Jena Fuseki)
- **Auth:** None
- **Free tier:** Unlimited (no publicly declared quota/limit was found — EPO describes the service as open for occasional use via the query interface, and recommends bulk download for heavy use)
- **Rate limit:** not documented and not confirmed as of 2026-08-17 — a separate page about rate limits for data.epo.org (unlike OPS, which has a fair-use charter) could not be found
- **Docs:** https://www.epo.org/en/searching-for-patents/data/linked-open-data
- **Status page:** no separate status page for data.epo.org was found; see the general https://www.epo.org/en/service-support/status-online-services
- **Verified:** 2026-08-17

Live check 2026-08-17 — a real SPARQL query without auth, the full successful response:
```
curl -G "https://data.epo.org/linked-data/query" \
  --data-urlencode "query=SELECT DISTINCT * WHERE { <http://data.epo.org/linked-data/id/application/EP/01903571> ?p ?o . } LIMIT 5" \
  -H "Accept: application/sparql-results+json"
→ HTTP 200, returned applicationAuthority, applicationNumber, filingDate, grantDate, etc.
```

## What it returns

RDF triples. Through the SPARQL endpoint — JSON (`application/sparql-results+json`), XML or HTML (depending on `Accept`). The data is the bibliographic data of EP applications and publications: numbers, filing/grant dates, applicant/inventor, classifications, links between application and publication, etc., linked through URIs of the form `http://data.epo.org/linked-data/id/...`.

```json
{
  "head": {"vars": ["p", "o"]},
  "results": {
    "bindings": [
      {"p": {"type": "uri", "value": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"},
       "o": {"type": "uri", "value": "http://data.epo.org/linked-data/def/patent/Application"}},
      {"p": {"type": "uri", "value": "http://data.epo.org/linked-data/def/patent/filingDate"},
       "o": {"type": "literal", "datatype": "http://www.w3.org/2001/XMLSchema#date", "value": "2001-01-20"}}
    ]
  }
}
```

## When to use

- You need an arbitrary graph query over patent data relations (SPARQL) without the OAuth scaffolding of OPS
- A quick bibliographic lookup by a known application/publication number without registration
- Linking patent data with other linked-data sources (the general web of data approach via URIs)
- Prototyping/researching data without quotas and authorisation

## When not to use

- You need full text (claims/description) — LOD covers primarily bibliographic data, not full text (for that, OPS `/fulltext` or Espacenet)
- You are not familiar with SPARQL and have no time to work out the syntax — then OPS REST or the Espacenet UI is simpler
- You need SLA/rate limit guarantees — LOD, unlike OPS, has no published fair-use policy, which also means no official availability guarantees under heavy load

## Auth setup

Not required. A public SPARQL endpoint, no key/token needed.

## Query patterns

### Get all properties of a resource by URI

```
GET /linked-data/query?query=SELECT DISTINCT * WHERE { <{URI}> ?p ?o . } LIMIT 100
Accept: application/sparql-results+json
```

### Find an application by number (example of the concrete URI pattern)

```
URI: http://data.epo.org/linked-data/id/application/{authority}/{number}
# authority = ST.3 office code, e.g. EP
```

### POST request (for long SPARQL queries)

```
POST /linked-data/query
Content-Type: application/x-www-form-urlencoded
Body: query=SELECT ... (urlencoded)
```

## Example queries

A real query, verified live 2026-08-17, and the confirmed response:

```bash
curl -G "https://data.epo.org/linked-data/query" \
  --data-urlencode "query=SELECT DISTINCT * WHERE { <http://data.epo.org/linked-data/id/application/EP/01903571> ?p ?o . } LIMIT 5" \
  -H "Accept: application/sparql-results+json"
```

Response (abridged):
```json
{"p": ".../applicationNumber", "o": {"value": "01903571"}}
{"p": ".../filingDate", "o": {"value": "2001-01-20"}}
{"p": ".../grantDate", "o": {"value": "2006-08-16"}}
```

## Limitations

- The data URI scheme is somewhat muddled in the documentation: older URIs lived under `http://data.epo.org/linkeddata/...` (without a hyphen), the current endpoint is `linked-data` (with a hyphen); when building queries, check against the real URIs from responses rather than assembling them by hand from a guess
- No published SLA/rate limit — under intensive use there is no formal guarantee, unlike OPS with its explicit fair-use policy
- Coverage is primarily EP (European) applications/publications, not a replacement for OPS in data depth (legal status, family, full-text are represented more weakly)
- The response format depends on the `Accept` header — if you do not specify it, you may get HTML instead of JSON

## Combine with

- **EPO OPS** (`epo_ops.md`) — for full text, legal status, patent family — what LOD does not cover
- **USPTO ODP** (`uspto_odp.md`) — for symmetric US data
- **CrossRef / OpenAlex** (`academic/`) — if the patent cites or is cited by scientific literature, for triangulation

## Fallback if API down or rate-limited

1. Bulk download of the full dataset (mentioned on the EPO page as an option for heavy use, details at epo.org/en/searching-for-patents/data/linked-open-data)
2. EPO OPS (`epo_ops.md`) — REST/XML instead of SPARQL, for the same bibliographic data
3. WebFetch to the Espacenet UI for a one-off manual search
