<!-- translated from upstream/references/registry/INDEX.md @ e233797 — see docs/TRANSLATION.md -->
# Source registry — INDEX

Concrete verified addresses by signal type: 1072 entries, reconnaissance 2026-08-05, value threshold 5/5.

Read on demand in Phase 4, when a subquestion needs a fresh stream on the topic (channels `news-current`, `industry-specific`, `preprint-servers`, `forum-discussion`, `api-direct`). Not part of the base budget — load the file you need, not all of them.

| File | Topic | Entries |
|---|---|---|
| `open_source_releases.md` | Open source releases | 526 |
| `regulatory.md` | Regulation and law | 137 |
| `markets.md` | Markets and macro | 130 |
| `science.md` | Science | 98 |
| `technology.md` | Technology | 97 |
| `society.md` | Society | 28 |
| `climate_health.md` | Climate, ESG and health | 25 |
| `security.md` | Security and reliability | 19 |
| `registries.md` | Registries | 12 |

## What is not here

- Scoring of a source for a specific claim — that is `source_scoring.md` and Phase 5.5.
- How to access with limits and example queries — that is `api_sources/`.
- Canonical sources for a domain — that is `stat_sources/`.
- Market reconnaissance of the importing project, municipal GIS datasets and addresses already marked dead — filtered out at import (`scripts/import_source_registry.py`).

## Updating

```bash
python scripts/import_source_registry.py --source <path>/sources.csv --min-value 5
```

The `--min-value 3` threshold yields roughly three times as many entries — widen deliberately, the catalog pays for it in context.
