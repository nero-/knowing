<!-- translated from upstream/references/swarm_postprocess.md @ e233797 — see docs/TRANSLATION.md -->
# Run post-processing — collecting Bayesian swarm observations

Read at the end of a medium/deep run (after Phase 7, before Phase 8 or right after it).

It works on the run's ready-made artifacts, nothing needs to be written by hand. `run_id` = the run's `<slug>`, the same in all four calls. The mechanics are in `docs/specs/2026-08-18-bayesian-swarm-design.md`.

**1. Observations — a separate call for EACH subquestion** from `plan.md` §12, with its `qclass` and the channels actually requested (primary + secondary + fallback, if a fallback was needed):

```
python3 scripts/collect_observations.py --research-dir <root>/<slug> --run-id <slug> \
  --requested academic=scientific-claim,data-statistical-gov=scientific-claim
```

A single shared list for the whole run is not allowed: `--requested` is parsed into a dictionary keyed by channel, and one channel with a different `qclass` in one line would silently overwrite the first pair. Separate calls append independently.

If a subquestion was also searched through a second engine, add its channel to the same call: `--requested academic=scientific-claim,search-engine-2/exa=scientific-claim`. The channel name comes from the stderr of `search_query.py` and matches the first field of the `discovery_path` of the sources found that way. Without this pair the engine will not get an observation, and `--engine auto` will keep choosing from the static table.

**2. Priors:** `python3 scripts/update_priors.py`. A fraction of a second, call it after every run: without it the observations will not land in `priors.json` and the next run will not see the statistics.

**3. Ad-hoc sources** — found via Discovery patterns (`source_dispatch.md`), not from the catalog (`api_sources/`, `stat_sources/`, `registry/`), and that became the `root` or an unresolved `dissent` of at least one claim. `url` and the first segment of `discovery_path` (that is the channel) — from `sources/NN.md`, `qclass` — from §12. Dead at the time of the run — the same call with `--dead`.

```
python3 scripts/promote_candidates.py --track https://api.example.org/v1 \
  --channel api-direct --qclass market-size --run-id <slug>
```

**4. Once every few runs:** `python3 scripts/promote_candidates.py --write` — prints the promotion (≥3 pieces of evidence in ≥3 different runs, a live endpoint, the channel prior did not degrade) and the demotion (≥3 runs in a row dead). Without `--write` it only prints; with `--write` it writes to `references/api_sources/promoted/` — **look at the `git diff`, commit by hand**, the script never commits.

The free-budget allocator beyond the mandatory minimum — `update_priors.py --qclass <qclass of the subquestion>` when choosing a channel beyond Primary/Secondary; the caveats are in `source_dispatch.md` §«Prior when choosing a channel beyond the mandatory minimum».
