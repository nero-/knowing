<!-- translated from upstream/references/phases/p5_claims.md @ e233797 — see docs/TRANSLATION.md -->
## Phase 5. Claims ledger and triangulation

**Executor:** assembly of `claims.csv` from index rows — `sub: explore-`small`` (`small` / medium from the frontmatter; on low, the small model 5.5 skips the checks). Triangulation check — the script `score_claims.py --write`, no model needed (the rule is mechanical, see below — only a count of sources/types/roots per row).

**Source scoring is no longer a separate step.** Every source in `sources/NN.md` already has a filled frontmatter with its scoring — the fetch sub-agent set it at step 4.1, at the moment it read the source (H7 rule: whoever read it, scores it). Here, in Phase 5, the scale is described in detail in `source_scoring.md` for reference, but a second pass over all sources is not required.

**Claims ledger (`claims.csv`)** — a new ledger artifact next to `sources.csv`. Schema:

```
claim_id, claim, hypothesis, sources, source_types, roots, paths, status, confidence, primary_source, source_caveat, dissent, as_of
```

- `claim` — the thesis in one line.
- `hypothesis` — H1-H4 or `-` if not tied to a hypothesis.
- `sources` — list of ids (`s01;s07;s12`).
- `source_types` — source types separated by `;` (`primary;academic;industry`).
- `roots` — roots separated by `;`, same order as `sources` (`own;study-smith-2024;own`); from `root:` in each source's frontmatter. Without this column the third triangulation condition cannot be checked.
- `paths` — discovery paths separated by `;`, same order; from `discovery_path:`. Without it the fourth condition cannot be checked (independence of the search, not only of the sources).
- `status` — `triangulated | contested | weak | single-type | single-root | single-path | contradicted | data-insufficient`.
- `confidence` — `high | medium | low`.
- `primary_source` — `Y | N`.
- `source_caveat` — `- | vendor | self-reported | disputed:sNN`.
- `dissent` — ids of sources CONTRADICTING the thesis (`s12;s19`), or `-`. Taken from the `dissent`/`contradictions` fields in the sub-agents' JSON. An empty field on a contested topic is a signal that the opposition was not sought, not that it does not exist.
- `claim_class` (optional, after `as_of`) — `empirical` (by default: a statement about the world) | `documentary` ("document X says Y" — a law, a standard, product terms; high on a single primary source is legitimate, the document itself is the proof).
- `as_of` — for volatile numbers (price, market share, version, exchange rate): the MEASUREMENT date `YYYY-MM`/`YYYY-QN` from the source's `data_as_of` field; `unknown` — the number exists, the date does not; `-` for non-numeric ones. **The source of the value is `data_as_of` in the frontmatter, not the article's publication date and not the main thread's guess** (it has not read the sources). A number without a measurement date is not a fact but a mine for a future `update`, and by the fail-closed rule it does not get into `memo.md`.

**One row — one statement.** "X grew 20%; Y fell 5%" — two rows: each has its own sources and its own status. The script counts a `;` or two sentences in `claim` as a composite thesis and fails the finish.

**Filling:** the main thread assembles `claims.csv` from the `claim_candidates` each fetch sub-agent returned (see `subagents_v2.md`), plus from an explicit reading of the claims in the already written `sources/NN.md`. Duplicate claims from different agents — merge into one row (union `sources`/`source_types`).

**The script computes status and the confidence ceiling, not the model.** The model writes `claim_id`, `claim`, `hypothesis`, `sources`, `source_caveat`, `dissent`, `as_of`, `claim_class`; then
`python scripts/build_sources_csv.py --research-dir <run> && python scripts/score_claims.py --research-dir <run> --write` — the script fills `source_types`/`roots`/`paths`/`primary_source` from `sources.csv`, computes `status` and cuts `confidence` to the ceiling. One URL in two files — one leg: the lowest id of the group stays in all the cells, merge the group's remaining files into it: `--strict` goes red on any pair of files with the same URL; a thin source is not a leg. The model can only lower it: `contradicted`/`data-insufficient` the script preserves. Audit of 70 runs: 18 `triangulated` on <3 sources and 282 `high` on a single source — the rules below were correct, the model's application of them was not. `finish.py` runs the same script with `--strict`: a ledger that disagrees with the count = red finish.

**Triangulation rule (mechanical):** a row gets `status: triangulated` if ≥3 sources **AND** ≥2 different types **AND** ≥2 distinct roots (`root:`) **AND** ≥2 different discovery paths (`discovery_path:`) — see `source_scoring.md` «Provenance» and «Fourth condition». Otherwise:
- < 3 sources → `status: weak`, confidence: low (exception — `claim_class: documentary` with a primary source: high)
- ≥3 sources but one type → `status: single-type`, confidence: medium (max)
- ≥3 sources and ≥2 types, but all reduce to one `root:` → `status: single-root`, confidence: medium (max) — ten retellings of one press release are one voice; the rule counts roots, not URLs
- ≥3 sources, ≥2 types, ≥2 roots, but all found by one `discovery_path` → `status: single-path`, confidence: medium (max) — one wording in one channel gives one sample from one index, not three independent voices
- There is unresolved `dissent` from a source with `type: Primary` or `credibility ≥ 4` → `status: contested`, confidence: medium (max) — **the majority rule does not apply here**; both positions go into the report with an explicit basis for the choice (see «Dissent rule» in `source_scoring.md`)
- An explicit contradiction between sources with no clear minority → `status: contradicted` — a separate counter-argument (Z1)
- After the gap wave (see above) still not closed → `status: data-insufficient` (an honest result, do not hide it)

**Primary-first rule:** a key number/fact without at least one primary source (`primary_source: N`) cannot get a `confidence` above `medium`, even if formally triangulated by count/type diversity. Primary here means a filing, official docs, a dataset, original research (see Credibility=5 in `source_scoring.md`).

**After assembly** — update `sources.csv` (the source index, as before) and the new `claims.csv`:

```csv
№,URL,Title,Type,Author,Date,Credibility,Recency,Bias,Total,Used,File,Note
1,https://...,Postgres logical replication docs,Primary,Postgres team,2024-09,5,4,4,13,Y,sources/01_pg-docs-logical.md,Primary source
2,https://...,Industry benchmark,Industry-media,J. Smith,2026-02,4,5,4,13,Y,sources/02_industry.md,Supports H1
```

```csv
claim_id,claim,hypothesis,sources,source_types,roots,paths,status,confidence,primary_source,source_caveat,dissent,as_of
CL1,"Logical replication scales to N nodes without external tooling",H1,s01;s07;s12,primary;industry;academic,own;study-smith-2024;own,academic|logical replication N nodes|en;web-general|postgres multi-master 2026|en;forum-discussion|pgsql-hackers|en,triangulated,high,Y,-,-,-
CL2,"CDC adds >200ms p99 latency at scale",H2,s09;s14,industry;industry,own;own,web-general|CDC latency benchmark|en;web-general|CDC latency benchmark|en,single-type,medium,N,-,-,2026-02
```

### Gap wave (Phase 5 continues — not a new phase, same as the Phase 4 loop convention)

**Executor:** `subagent_type: knowing-fetcher` (`small` / medium, from its frontmatter). A narrow, pointed task on one specific hole — an expensive model is not needed, but this is searching, and on low effort a small model skips searches.

After the first filling of `claims.csv`, compile the list of holes — rows with `status ≠ triangulated`.

**Pointed second wave:** one agent per hole (or in batches, in parallel), the prompt = the specific claim + what exactly is missing:
- "a primary source is needed for CL2"
- "a 3rd source type is needed, right now only industry×2"
- "contradiction between s09 and s14 — find the cause or an additional arbiter"

**Maximum 2 rounds.** If the hole is not closed after the second round — the row is marked `status: data-insufficient`. This is an honest result of the report, not a failure: it goes into Open Questions (Z2), not masked.

**Output:** an updated `claims.csv`, updated `sources/NN.md` (new sources in a fresh number range — the next free block after the ones already taken).
