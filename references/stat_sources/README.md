<!-- translated from upstream/references/stat_sources/README.md @ e233797 — see docs/TRANSLATION.md -->
# Stat sources catalog — README

How to use and extend the stat_sources catalog.

## Reading

1. The main thread or an agent first reads `INDEX.md` for navigation.
2. Decides which core/* and industries/* files are relevant.
3. Loads only those files (progressive loading — not the whole catalog).
4. Uses the entries in `plan.md` Information sourcing strategy.

## Each entry's record

Every entry has the same structure — this is a template. Do not deviate, otherwise compose-ability is lost:

- `URL` — the exact landing page (not the site home page, if possible)
- `Type` — what type of organization it is (needed for bias assessment)
- `Access` — whether there is a paywall, whether there is a preview
- `What's inside` — specifically which data
- `When to use` — use cases (at least 2)
- `How to use` — how to navigate; a search pattern is mandatory
- `Data quality` — credibility / freshness / lag / methodology
- `Limitations` — what is NOT there; known biases
- `Combine with` — which sources are complementary
- `Fallback if blocked` — an alternative if the URL does not work

## When to update

- The source changed its URL → update immediately
- The access changed (was open, became paywalled, or the reverse) → update
- A significantly better alternative appeared → add it + mark the old one as "see also"
- A revealed bias was recorded → add a note in Limitations

## When to add a new entry

Only if:
- The source will be used in ≥2 future research runs
- It fills a gap (nothing similar)
- It has a stable URL

Do not add one-off sources from a specific run. They live in that run's `sources/NN.md`.

## Category structure

**core/** — cross-industry sources.

**industries/** — industry-specific. One file per industry.

If a source serves several industries (like BLS — US labor across industries) — it goes in `core/gov_macro.md`, not in industries/. Industries/ is only for **industry-specific** sources.

## Quality grades

- **A (Credibility 5):** primary, peer-validated, official agency
- **B (Credibility 3-4):** industry-recognized, has methodology, transparent
- **C (Credibility 1-2):** self-reported, no methodology, marketing

## Licences and legal

When adding a new source, record:
- Licence / terms of use (especially for bulk downloads)
- If scraping — what robots.txt says
- If the data is commercial — what the licence says
- If the data is personal — privacy considerations

## Forbidden sources

Do NOT add to the catalog:
- Pirate sites (Sci-Hub, LibGen, Z-Library) — do not use, including as a fallback
- Sources with stolen data / leaked credentials
- Sources requiring obfuscation / impersonation

## Maintenance

Quarterly review:
- Check all URLs (link rot)
- Update freshness/lag for each source
- Add new sources for discovered gaps
- Archive outdated ones
