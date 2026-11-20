<!-- translated from upstream/references/refresh_protocol.md @ e233797 — see docs/TRANSLATION.md -->
# Refresh Protocol — how to do delta research

## Contents

- Principles
- When to run an update
- Pre-flight check
- The 4 categories of delta (what to look for)
- Verified-no-change (what has NOT changed)
- Output: the structure of the delta file
- What **NOT** to do
- Model routing for an update
- What must be in `refresh_targets.md` (a separate file next to plan.md)

**When it is used:** the user calls `update <slug>` or «update the research on X». The skill **does not repeat the whole research** — it finds **only what has changed** since last time and writes a diff file.

**Why:** a full re-research is expensive, slow and loses history. The delta approach:
- New players in the industry → add to the landscape (M2)
- Fresh data on facts/numbers → re-check the N blocks
- New publications → check whether they refute H1-H3
- Old theses that **have not changed** → keep as `verified: still valid`

---

## Principles

1. **Delta, not replay.** Do not run Phase 4 from scratch. Only targeted search with date filters from `last_research_date`.
2. **The source of truth is `refresh_targets.md`.** This file is generated in Phase 7 of the previous research. It says «here is what is worth tracking in this domain».
3. **Output — a diff file, not a new report.** The old report stays. `diffs/<YYYY-MM-DD>_delta.md` — a compact list of changes.
4. **Verified as a finding.** If a fact was re-checked and did not change — that is **a result**, not emptiness. Record «still valid».
5. **Adversarial trigger.** A new publication that refutes a hypothesis is a signal «Phase 6 must be re-run on the updated context», not something to silently ignore.

---

## When to run an update

**Triggers:**
- The user explicitly said «update the research on X»
- More than 3 months have passed since `last_research_date` and the user is interested in the topic again → offer it
- An event from the research domain is mentioned in the chat («Polymarket raised a round» — while the research is about prediction markets) → offer it

**Do NOT run an update:**
- Without an explicit user request or confirmation of an offer
- If `last_research_date` < 30 days (little substantive is likely to have changed)
- On a shallow research (there is nothing to update there — restarting the old one in full is cheaper)

---

## Pre-flight check

Before starting an update:

```
1. Read research/<slug>/plan.md
   ├── last_research_date (from section 0 HEADER)
   ├── hypotheses H1-H4 (section 9)
   └── subquestions/subtopics (section 11)

2. Read research/<slug>/refresh_targets.md
   ├── companies/entities to re-check
   ├── numbers/series to re-verify
   ├── new-publication watch terms
   └── new-entrant search patterns

3. Read research/<slug>/<last>_<genre>.md final report
   └── Understand what was said — so as to see what has changed
```

If there is no `refresh_targets.md` (an old research predating this protocol) — **generate it in the process** on the basis of reading the final report + plan.md. That is the first step of the update.

---

## The 4 categories of delta (what to look for)

### 1. New entrants

**Trigger:** the research has a landscape block (M2 profiles, M5 market map) or at least one subquestion of the form «who are the players in X».

**What to look for:**
- **Crunchbase** (if `CRUNCHBASE_API_KEY` is present): queries by the category-tags from refresh_targets with `founded_after: <last_research_date>` and `total_funding > $1M` (a filter against noise)
- **GitHub topics** (from `topic:<keyword>` in refresh_targets): repositories `created:>YYYY-MM-DD` with `stars>50`
- **HuggingFace datasets/models** (if the topic is ML): `sort=Recent` with a date filter
- **News** via GDELT or NewsAPI: queries «launched», «out of stealth», «raised seed», in a combo with an industry keyword
- **Industry-specific** registries from refresh_targets (e.g. BloombergNEF for energy)

**Output format:**
```markdown
## New entrants since 2026-05-22

### Company X — Seed $5M (2026-07-15)
- Source: Crunchbase + TC article
- Category: <same category as existing players in M2>
- Why it matters: <fills gap of existing players / direct competitor>
- Update target: add to landscape M2 profile

### Company Y — out of stealth (2026-08-01)
- Source: company blog + HN thread (s12)
- Why it matters: alternative approach to <H2 thesis>
- Update target: profile + reconsider H2 in adversarial
```

### 2. Changes at specific companies (entity diff)

**Trigger:** refresh_targets lists specific companies that have to be tracked.

**What to track:**
- **Pricing page** — compare with what it was (if there is an archive in `sources/`)
- **Job postings** — the `/careers` page, headcount growth = a signal of direction
- **Leadership** — Crunchbase or LinkedIn (if access is available) for a change of CEO/CTO
- **Product pages** — have new features appeared?
- **Funding** — Crunchbase api: a new round?
- **Press releases** — the company blog + Google News with `site:<company>.com`

**Fingerprinting tactic:**
1. **WebFetch** on the page → hash the content (markdown-only, no CSS/JS)
2. Compare the hash with what was in `sources/SN_<company>_<page>.md` (if present)
3. If it changed → save the new version alongside, write a diff into the delta file
4. If it did not change → mark `verified-no-change: <today>` in the old source

**Output format:**
```markdown
## Entity diff: Company X

### Pricing page (changed 2026-07-15)
- Was: Starter $29/mo, Pro $99/mo (snapshot in s05)
- Now: Starter $39/mo (+34%), Pro $129/mo (+30%), new "Enterprise" tier
- Implication: shift upmarket — supports adversarial counter-arg CA2

### Careers page (no change since 2026-04)
- 12 open roles, mostly Eng (was 11)
- Verified-no-change confirms hiring pace stable
```

### 3. Freshness of facts and numbers (numbers refresh)

**Trigger:** the research contains numerical claims from N blocks (N1 metrics, N3 market sizing, N5 forecasts).

**What to re-check:**
- **FRED series IDs** from refresh_targets — recompute `latest_value`, `YoY change`, note if the trend has changed
- **World Bank indicators** by country codes — the same thing
- **Industry estimates** (if a range with named sources was recorded) — Statista alt, IBISWorld:
  - Search for the same phrase as in the original source
  - Compare the number; if it diverged by >20% — a high-interest delta
- **Pricing / unit economics** of companies — see category 2

**Output format:**
```markdown
## Numbers refresh

### FRED CPIAUCSL
- Was: 312.5 (2026-04, anchor in original)
- Now: 314.2 (2026-08)
- Change: +0.5% over 4mo (~1.5% annualized — slowing)
- Implication: macro assumption «inflation moderating» still valid

### Industry market size estimate
- Was: $5.0B (Statista 2026 estimate, anchor for N3 block)
- Now: $6.2B (Statista 2026-Q3 update)
- Change: +24% — exceeds expected growth from N5 forecast
- Implication: revise N5 forecast in Phase 7 synthesis update
```

### 4. New publications / opposition (adversarial trigger)

**Trigger:** there is a hypothesis H1-H4 and new articles/posts on the topic keep appearing.

**What to look for:**
- **OpenAlex / Semantic Scholar** — search by `concepts.id:<concept>` with `publication_year:<YYYY>` (after last_research_date)
- **arXiv / bioRxiv / SSRN** — a date filter, keywords from refresh_targets
- **Retraction Watch** — check whether the cited sources have been retracted
- **News-current** — events that could have refuted the facts in the research
- **Forum-discussion** — post-mortems, failures, bugs in the approaches the research described

**If a refutation is found → adversarial trigger:**
```markdown
## Adversarial trigger

### New paper contradicts H2
- Title: "<paper title>"
- Authors / venue / date
- Source: arXiv 2026.12345 (2026-07-23)
- Key claim: «<verbatim quote of contradicting claim>»
- Original H2 in our report: «<our H2 verbatim>»
- Severity: HIGH — directly opposes H2 with new dataset
- Recommendation: **re-run Phase 6 adversarial pass** with this paper as input;
  may require updating verdict in original report

### Retraction alert
- Source: s07 (Smith et al. 2024) — retracted on 2026-06-15
- Reason: data fabrication (per RetractionWatch)
- Severity: MEDIUM — was supporting H1 along with 2 others
- Recommendation: H1 still supported by 2 sources; mark s07 as `retracted`,
  re-evaluate confidence label (was: high → propose: medium)
```

---

## Verified-no-change (what has NOT changed)

This is **a result too**. After running all 4 categories — a final section:

```markdown
## Verified (still valid, no change)

### H1: «X scales linearly with Y»
- Re-checked 3 original supporting sources: all still accessible, no contradicting recent publications
- Verdict: H1 confidence remains «high»

### Regulatory landscape (X4 block)
- EUR-Lex Regulation 2015/2283: no amendments since last research
- Per-country status: re-checked Germany, Italy — no changes

### Market structure (M5 block)
- Top 5 players still same; market shares roughly stable per Statista 2026-Q3
```

Without this section the user thinks «maybe they skipped something?» — and here there is an explicit «no, checked, all the same».

---

## Output: the structure of the delta file

`research/<slug>/diffs/<YYYY-MM-DD>_delta.md`:

```markdown
---
slug: <slug>
update_date: <YYYY-MM-DD>
previous_research_date: <YYYY-MM-DD>
parent_report: <YYYY-MM-DD_genre.md>
refresh_targets_version: <YYYY-MM-DD>
trigger: <"manual" | "scheduled" | "<user-request-text>">
severity: <HIGH | MEDIUM | LOW>  # max severity among findings
---

# Delta: <topic> · <YYYY-MM-DD> vs <previous date>

## Summary (3-5 bullets)
- <main finding 1>
- <main finding 2>
- ...

## 1. New entrants since <date>
<either the list of what was found, or «None found in <X> sources checked»>

## 2. Entity diff
<per-company changes, or «No changes detected in <N> tracked entities»>

## 3. Numbers refresh
<per-metric changes>

## 4. Adversarial trigger
<new opposition, retractions, or «No opposing publications found»>

## 5. Verified (still valid)
<what was re-checked and stayed the same>

## Recommended actions
- [ ] Update M2 profile to include <new company>
- [ ] Re-run Phase 6 adversarial with <new paper> as input
- [ ] Revise N5 forecast given +24% revision in market size estimate
- [ ] (etc.)

## Sources added in this delta
- <list of new sources/SN_*.md files added with this update>

## Cost
- Model routing: the configured model for fetch, the strongest one only if a Phase 6 re-run is triggered
- Estimated: ~$0.40 (vs full re-research ~$2.00)
```

---

## What **NOT** to do

**❌ Do not do a full Phase 4 again.** This is an update, not a replay.

**❌ Do not ignore an adversarial trigger.** If you found a refutation — fix it in the Phase 6 update, do not leave it in the delta file as a notice.

**❌ Do not skip the «verified» section.** What has not changed is a signal too, it has to be recorded explicitly.

**❌ Do not overwrite the old report.** The old `<YYYY-MM-DD>_<genre>.md` stays. The delta is a separate file. If the changes are substantive → a **new** `<YYYY-MM-DD>_<genre>.md` may appear alongside (the update mode from SKILL.md) — but that is the user's decision after reading the delta.

**❌ Do not run an update without refresh_targets.md.** If the file is missing (an old research predating the protocol) — generate it first, then act.

**❌ Do not do an update on shallow.** A shallow research is <8 sources; repeating it in full is cheaper. An update makes sense from medium and up.

---

## Model routing for an update

| Update step | Model | Effort |
|---|---|---|
| Pre-flight (reading plan.md + refresh_targets.md + last report) | the configured model | low |
| Generate refresh_targets.md (if missing) | the configured model | medium |
| 1. New entrants search (sub-agents) | the fetch subagent | medium from the frontmatter (web/news/Crunchbase; on low effort it skips searches) |
| 2. Entity diff (fetch + compare) | the fetch subagent | medium from the frontmatter (fingerprinting is mechanical) |
| 3. Numbers refresh (api-direct) | the fetch subagent | medium from the frontmatter (FRED/WB/etc) |
| 4. Adversarial trigger search | the configured model | low (academic) |
| Synthesis delta file | the configured model | medium |
| **If adversarial trigger HIGH → re-run Phase 6 partial** | the strongest configured model | high (only this part) |

**Total estimated cost for a typical update without an adversarial re-run: ~$0.40** (vs ~$2 for a full medium research).

---

## What must be in `refresh_targets.md` (a separate file next to plan.md)

This file is generated automatically in Phase 7 of the initial research. The template is in `blocks/close.md` (block Z11). It contains:

1. **Entities to track** — specific companies/products/projects (with `/pricing`, `/careers`, `/blog` URLs)
2. **Numbers to refresh** — specific FRED series IDs, WB indicators, industry estimate references
3. **Topic markers** — `topic:<keyword>` for GitHub, academic concepts for OpenAlex, news keywords
4. **Hypotheses to re-test** — H1-H4 from the original research, as formulations for searching refutations
5. **Update cadence suggestion** — «monthly / quarterly / event-driven»

Without this file an update does not work optimally — the targets have to be re-discovered every time.
