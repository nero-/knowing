<!-- translated from upstream/references/source_scoring.md @ e233797 — see docs/TRANSLATION.md -->
# Source Scoring — the source rating system

## Contents

- Credibility scale (trustworthiness)
- Recency scale (currency)
- Bias scale (neutrality)
- Total and the filter
- Up-front scepticism — vendor / self-reported / disputed (before the claims ledger)
- Provenance — the `root:` field (anti-circular-reporting)
- Number provenance — `origin_kind` / `origin_url` / `data_as_of` / `chain_len`
- Number arithmetic — `numbers.csv`
- Triangulation
- Claims ledger — `claims.csv`
- The sources/NN_slug.md file — template
- Row template for sources.csv
- Anti-patterns

Every source collected is scored along three axes 1–5. The sum (max 15) determines whether the source makes it into the basis of the findings.

## Credibility scale (trustworthiness)

- **5** — Primary source: an official document of a museum/institute, a peer-reviewed article, original research with open data, a talk by a practitioner author.
- **4** — Authoritative industry media with fact-checking: ICOM, Museum-iD, specialised academic journals without peer-review, association reports.
- **3** — General quality press: Guardian, NYTimes, Kommersant, RBC — with a working editorial desk. Books from publishers with a reputation.
- **2** — A personal blog of a named expert, but without review. A case study with a marketing slant. Unauthorised press releases.
- **1** — A forum, a rumour aggregator, an anonymous post, AI-generated content, pages with an obvious proxy goal (to sell, to recover traffic).

## Recency scale (currency)

Applied by default. If the topic is historical — record that in the plan and skip this scale or adapt it.

- **5** — Published <1 year ago
- **4** — 1–3 years
- **3** — 3–5 years
- **2** — 5–10 years
- **1** — >10 years (if the topic is current)

## Bias scale (neutrality)

- **5** — Scientific/independent. Discloses the methodology, the sources, the limitations. Ready to admit the opposite.
- **4** — Industry neutral press. Has an editorial policy, but sees several sides.
- **3** — Mainstream with a known slant. Writes within its own frame, but checks the facts.
- **2** — A lobbyist position. Declares the goal «to defend X's interests», openly or not.
- **1** — Overt propaganda / a fraudulent interest. Ignores the opposing data. The goal is manipulation.

## Total and the filter

**Total = Credibility + Recency + Bias** (from 3 to 15). It is computed by `scripts/build_sources_csv.py`
over the three axes; a `total:` in the frontmatter that disagrees with the sum is overwritten in `sources.csv`.

- **12–15** — the basis of the findings. Quote directly.
- **8–11** — supporting sources. Use them as reinforcement, but not as the sole basis of a claim.
- **7 and below** — supplementary material. Do NOT derive from these. You may mention them as «an opinion also occurs …». `score_claims.py` does not count such a source as a triangulation arm.

## Up-front scepticism — vendor / self-reported / disputed (before the claims ledger)

The Bias scale above catches a general slant, but NOT the specific trap of quantitative findings:
**a source that measures its own product, publishes a self-reported benchmark, or
whose number another source directly disputes.** The red team at Phase 6 catches this late —
when the claim is already in the findings. Mark it up front, when scoring each source, BEFORE
it lands in `claims.csv`.

**`caveat:` is a strict enum, exactly one of:** `-` · `vendor` · `self-reported` ·
`disputed:sNN` (NN — the number of the disputing source). **No free text in the
field** — write the explanation («why vendor», «what exactly is disputed») into the BODY of the
file (the «Author context» or «What the source gives» section), not into the field's value. Free
text in `caveat:` breaks machine processing (you cannot grep by the enum, `eval/validate_structure.py`
will warn) and tears the CSV apart with commas. An outdated source is NOT a caveat (the Recency
scale exists for that); a caveat is only about a vendor conflict / self-report / dispute.

- **`vendor`** — the source sells what it measures (a vendor benchmark «our product vs
  the competitor», a case with a marketing slant). Not forbidden — but its **magnitude** (not
  the direction) is unreliable. Triangulate the direction with an independent source.
- **`self-reported`** — a number from the author's own measurement without independent replication
  (a claimed SOTA on one's own benchmark, «we reached X%»).
- **`disputed:sNN`** — another collected source (sNN) directly disputes this number/conclusion.
  The discrepancy is itself a finding: do not silently pick the «right» side, show the dispute.

Write the marker into the `caveat:` field of the source's frontmatter (`sources/NN.md`) and carry it into the
claims ledger (see below). The rule is symmetric to primary-first: **a claim whose key
quantitative anchor is marked `vendor`/`self-reported`/`disputed` does not get
`confidence: high`** — the ceiling is `medium`, and `disputed` without an independent arbiter →
`low` + an explicit caveat in the report. This is a cheap filter at the input, NOT a full adversarial
pass (that one stays in Phase 6) — the goal: that synthesis knows from the very start which
number not to trust as the sole basis.

## Provenance — the `root:` field (anti-circular-reporting)

Ten URLs retelling one press release are one voice, not ten. The `root:` field in the
frontmatter is filled by the fetch agent **at the moment of reading the source** (the same
H7 principle as with scoring: the one who read it marks it):

- **`own`** — the source produced the material itself: its own research, reporting with
  its own interviews, an official filing, a dataset.
- **`<root id>`** — the source retells/quotes someone else's material: a short stable
  root identifier (`press-release-acme-2026-03`, `study-smith-2024`,
  `gartner-mq-2025`). The same root across different sources — **the identical string**,
  otherwise root dedup will not fire.

Filling rule: if the source's key facts trace back to a single external
piece — that is its root. If the source compiles from many places with its own
analysis — `own`. Do not leave it empty: data of unclear origin is also a signal, write
`unclear` and lower credibility.

**`own` is a class, not an identifier.** Two independent studies both honestly
get `own`, and when counting roots that is TWO different roots, not one. Therefore when
comparing roots, `own` in different sources counts as distinct roots — unless
it is the same material (see the rule on own measurements below).
In the counting, `unclear` does not count as a root at all: unknown provenance
does not confirm independence.

**Own measurements: one experiment = one root.** The results of your own
bench, run or experiment get a shared root of the form `own-lab-<slug>` —
**the identical string for all files of one experiment**, however many files the results
are spread over (latency, injections, extraction — that is one
bench, not three sources). The rule is symmetric to the rule about retelling a press release:
three slices of one run are one voice, not three.

Consequence, to be applied deliberately: **an own measurement cannot give
`triangulated` on its own** — however many files it occupies, there is one root, and
the row gets `single-root` (confidence ceiling `medium`) until an
external confirmation appears. A measurement that entered the findings without an external root must
carry `caveat: self-reported` (see «Up-front scepticism» above).

The field goes into `sources.csv` (the `root` column) and works in the Phase 5 triangulation rule:
the status `triangulated` requires **≥2 distinct roots** among the confirming sources
(see `phases/p5_claims.md`). Otherwise — `single-root`: formally many sources, in fact
one voice.

## Number provenance — `origin_kind` / `origin_url` / `data_as_of` / `chain_len`

`root` answers the question «whose material this is». For **numbers** that is not enough: the skill
checks that the source is quoted correctly (Phase 6.5 faithfulness), but nowhere does it
check **where the source took the number from and whether it is entitled to call it that**. A junk site
with a verbatim quote passes faithfulness perfectly. Hence four fields, mandatory
for any source whose number you intend to use:

| Field | What it means | How people get it wrong |
|---|---|---|
| `origin_kind` | WHICH act produced the number | a retelling of a report is marked `measurement` |
| `origin_url` | the producing document | they put the URL of the page where they read it |
| `data_as_of` | the date of the DATA | they put the publication date of the article |
| `chain_len` | the length of the retelling chain | they put 0 «by default» |

**Fail-closed rule.** `origin_kind: unknown` **or** `chain_len ≥ 2` **or**
`data_as_of: unknown` ⇒ the number **does not enter** `memo.md`, the TL;DR (F1) and block F9, and
the claim resting on it does not get `confidence: high`. Not «the model will decide» — it is checked
by the script `scripts/check_number_provenance.py` over `claims.csv` and `sources/`.

Unknown provenance is a quarantine, not a pass. Symmetric to the
primary-first rule: the skill already refuses to give `high` without a primary source; here
it refuses to give a platform to a number without a traceable producer.

This hits the class that neither `recency` nor `bias` catches: **a zombie number** —
a number that has circulated on the web for years while the primary source is dead or never existed. A
2026 reprint has an honest `recency: 5`, an honest `bias: 4` and a substantive
quote; the only thing that gives it away is the impossibility of naming the document that produced
this number, and the date of the measurement.

**Do not go to the web for numbers when a registry exists.** If the metric is covered by the catalog
(`stat_sources/`, `api_sources/`), a web article with this number cannot be the root —
it is a pointer to the root. The rule is enforced in Phase 4.0 (`source_dispatch.md`):
for a quantitative subquestion → the primary channel must be registry/API. It is cheaper not to
filter garbage at the output than to generate it at the input.

## Number arithmetic — `numbers.csv`

Provenance answers «where the number comes from». It does not answer **«does it add up»**. A percentage,
a share, a growth, a ratio — these are the result of a computation, and a computation done in prose
nobody redoes: the report prints `34.2%`, and all subsequent layers check whether the
SOURCE was quoted correctly, not whether the division was correct. Transposed digits
(`34.2` → `43.2`), shares that do not add up to 100%, and growth computed from the wrong base
pass liveness, faithfulness and qualifier preservation straight through.

Therefore all the numbers the report stands on are declared machine-readably, and
derived ones are **recomputed by a script**: `scripts/check_number_arithmetic.py`.

**`numbers.csv` schema** (run root, next to `claims.csv`; medium/deep —
mandatory, shallow — if the memo has even one derived number):

| Field | Value |
|---|---|
| `num_id` | `N1`, `N2`, ... continuous numbering |
| `value` | the number as it is printed in the report (`34.2`) |
| `unit` | `%`, `$B`, `ms`, `x`, `-` |
| `kind` | STRICT enum: `verbatim` (the source calls this number by itself) \| `derived` (we computed it) \| `share` (a share within a group, must be `%`) |
| `formula` | arithmetic over the names from `inputs` (`a/b*100`, `(b-a)/a*100`); `-` for `verbatim`/`share`. Only `+ - * / **` and parentheses |
| `inputs` | `a=1710[s03]; b=5000[s03]` — name=value[source]; every input number carries its own `[sNN]` |
| `group` | for `kind: share` — the name of the group over which the shares are summed (`browsers`); otherwise `-` |
| `claim_id` | the row of `claims.csv` that this number carries, or `-` |
| `sources` | source ids separated by `;` |
| `as_of` | the date of the DATA (the same semantics as in `claims.csv`) |

**What the script checks:**

1. `derived` — recomputes `formula` over `inputs` and compares it with `value`. Tolerance: 1%
   relative or 0.05 absolute (rounding to a whole number is not a defect,
   transposing digits is a defect).
2. `share` — the shares of one `group` must add up to 100 ± 0.5.
3. **Fail-closed:** a number of a derived FORM (`%`, `×`, `p.p.`, «N-fold») in
   `memo.md` that has no row in `numbers.csv` is an error. An unregistered
   derived number was recomputed by nobody.
4. Hygiene: `kind` from the enum, `num_id` unique, `sources` non-empty, `claim_id`
   resolves in `claims.csv`, `derived` has both `formula` and `inputs`.

**A number taken verbatim is also registered** — as `verbatim`. Otherwise rule 3
would not distinguish «the source said exactly this» from «we computed it and did not check», and fail-closed
would have to be weakened to a warning. The requirement is symmetric to what already exists in
`memo.md`: three key numbers with `[sNN]` and `as_of`.

This is NOT a duplicate of provenance: `check_number_provenance.py` judges the **origin**
(`origin_kind`, `chain_len`, the circulation of the value across different roots),
`check_number_arithmetic.py` — the **computation**. A number can have impeccable
provenance and still not add up.

## Triangulation

Every statement in the final findings must be confirmed by **at least 3 independent sources of different type AND at least 2 distinct primary sources (`root:`)**. For example, a claim cannot be supported by three articles of one author in one outlet — that is one voice, not three. Exactly likewise it cannot be supported by three outlets retelling one press release — count roots, not URLs.

If there are ≥ 3 sources but all of one type (for example, only media) — mark it «requires confirmation by a primary source».

If there are no opponents of the position at all among the sources — that is a signal. Possibly:
- The topic is poorly researched (then be honest: «there is little literature on the topic, the conclusions are preliminary»).
- An echo chamber / we are searching badly (then a separate search with the opposite query).

## Claims ledger — `claims.csv`

From this version triangulation is tracked not only «in one's head» during synthesis, but as a separate
artifact — a ledger next to `sources.csv`. It is filled in Phase 5 (see `phases/p5_claims.md`)
from the index rows and claim candidates returned by the fetch sub-agents (see
`subagents_v2.md`) — each agent itself notices which claim its subtopic confirms,
and passes on a candidate row, instead of leaving it to «remember at the end».

**Schema:**

| Field | Value |
|---|---|
| `claim_id` | `CL1`, `CL2`, ... continuous numbering |
| `claim` | the claim in one line |
| `hypothesis` | `H1`-`H4`, or `-` if the claim is not tied to a plan hypothesis |
| `sources` | source ids separated by `;` (`s01;s07;s12`) |
| `source_types` | types separated by `;`, the same order as `sources` (`primary;academic;industry`) |
| `roots` | roots separated by `;`, the same order as `sources` (`own;study-smith-2024;own`) — taken from `root:` in each source's frontmatter; needed for the third triangulation condition |
| `paths` | discovery paths separated by `;`, the same order as `sources` — taken from `discovery_path:`; needed for the fourth condition |
| `status` | `triangulated` \| `contested` \| `weak` \| `single-type` \| `single-root` \| `single-path` \| `contradicted` \| `data-insufficient` |
| `confidence` | `high` \| `medium` \| `low` |
| `primary_source` | `Y` \| `N` — whether among the sources there is at least one Credibility=5 primary one |
| `source_caveat` | `-` \| `vendor` \| `self-reported` \| `disputed:sNN` — the up-front scepticism marker (see above); non-`-` lowers the confidence ceiling |
| `dissent` | ids of sources that CONTRADICT this claim, separated by `;` (`s12;s19`), or `-`. Filled from `dissent`/`contradictions` in the sub-agents' JSON |
| `as_of` | the date of the DATA of the claim's key number (`2025-Q3`), `unknown` if there is a number but no date, `-` if the claim is not quantitative |

**Header contract.** The columns above are in exactly this order; after them only
`claim_class`, `evidence_kind`, `plain`, `detail` are allowed. For `numbers.csv` — the columns of its schema in that
order, plus an optional `label`. Otherwise `validate_phases.py` is red at any depth: the audit found 26
variants of the `numbers.csv` header, and a rule that did not find its column silently failed to fire.

**`claim_class`** — `empirical` (by default) | `documentary`. Documentary — a claim about the content of a document
(«152-FZ requires parental consent», «the Pro plan costs $20»): high on a single primary source is legitimate,
the document itself is the proof. On a secondary retelling of a document — the ceiling is medium, as for everything.
An empirical claim about the world (growth, effect, share) is never documentary, even if taken from a report.

**The script computes it.** `status`, `confidence` (as the ceiling), `source_types`, `roots`, `paths`,
`primary_source` are filled by `scripts/score_claims.py --write` from `sources.csv`; the model does not set them.
A triangulation arm is a unique normalised URL (without `www`, the fragment and utm tags), not a thin source
and not `total < 8`. `root: own` in different sources means different roots, `unclear` is not a root. An empty
`root:`/`discovery_path:` counts as one shared «unknown»: independence that nobody recorded is not independence.
One row — one statement: `;` or two sentences in `claim` — a compound claim, finish red.

**Mechanical triangulation:** `status: triangulated` ⟺ ≥3 sources **AND** ≥2 different
types **AND** ≥2 distinct roots (`root:`) **AND** ≥2 different discovery paths
(`discovery_path:`). This is checked by counting the fields `sources`/`source_types`/`roots`/`paths`,
not by re-reading the content — which is why it is computed by `score_claims.py --write`, not by the model (`model_routing.md`, Phase 5).

**A thin source is not a triangulation arm.** A file with fewer than 2 verbatim
quotes or with `access:` PARTIAL/closed/paywalled/abstract-only does not enter the counting of the four conditions:
either refetch it with the ladder (`scripts/fetch_source.py`) or lower the
claim's status. `validate_phases.py` raises an error if `triangulated` rests only on
such sources.

The third condition (roots) is not optional: without it, ten URLs retelling one
press release pass as ten voices.

**The fourth condition (discovery paths) — against search conformism.** The first three
count how different the sources themselves are; none of them looks at how different the places
they were *searched for* are. Sub-agents get one prompt template, one model and one search
index — their trajectories are correlated by construction (Anthropic Frontier Red Team,
13.08.2026: agents are «low-dispersion», when the context/scaffold/model coincide the actions
coincide too — 18 out of 30 chose the same branch name). Three sources of different
types and roots, pulled out by one formulation from one channel, are one sample
from one distribution, not three voices. All sources with one `discovery_path` ⇒
`single-path`, confidence ceiling `medium`.

The full breakdown of statuses when the conditions are not met — `phases/p5_claims.md` «Triangulation rule»;
here and there the formulation must coincide verbatim on all four conditions.

**The dissent rule (protection of the minority).** Triangulation is by construction a majority rule:
three sources beat one. In research this is often wrong — a lone
regulatory filing is right against three retellings by the industry press. The second
epistemic failure is exactly the opposite of the first: credulity is punished
by triangulation, while a **hidden profile** (the decisive information is held by only
one participant, and the group converges on shared knowledge) is *created* by triangulation.
One scepticism regulator does not fix both — an explicit carrier of disagreement is needed:

- `dissent` ≠ `-` and among the contradicting sources there is one with `type: Primary` **or**
  `credibility ≥ 4` ⇒ the status is **`contested`**, not `triangulated`, whatever the
  majority. The confidence ceiling is `medium`.
- `contested` must enter the report with **both** positions, with an explicit basis for the
  choice («position A is accepted because s07 is a primary filing, while s03/s11/s14
  reduce to press release s02»), and not be averaged into one formulation.
- Dissent can only be extinguished substantively: show a methodological error of the
  disagreeing source or find independent confirmation of the majority
  (another root AND another path). Lowering the `credibility` of the disagreeing source so that the
  rule does not fire is fitting the ledger to the desired conclusion.
- An empty `dissent` for a claim in a contested topic is suspicious in itself: it means
  the opposition was not looked for. That is an entry into the gap wave, not a sign of solidity.

**Primary-first rule:** `confidence: high` is allowed ONLY if `primary_source: Y`.
Without a primary source — the ceiling is `medium`, even if it is formally triangulated by
count and type diversity. Reason: three secondary retellings of one and the same primary fact easily create
the illusion of independent confirmation.

**Caveat rule (symmetric to primary-first):** if `source_caveat` ≠ `-`, the confidence
ceiling is `medium` (for `vendor`/`self-reported`), and `disputed:sNN` without an independent
arbiter → `low` + a caveat in the report. The claim's key quantitative anchor on a
vendor/self-reported/disputed number is unreliable in magnitude — synthesis must know about this
before the conclusions, and not learn it from the red team.

**Example:**

```csv
claim_id,claim,hypothesis,sources,source_types,roots,paths,status,confidence,primary_source,source_caveat,dissent,as_of
CL1,"Postgres logical replication handles N nodes without external tooling",H1,s01;s07;s12,primary;industry;academic,own;study-smith-2024;own,academic|logical replication N nodes|en;web-general|postgres multi-master 2026|en;forum-discussion|pgsql-hackers replication|en,triangulated,high,Y,-,-,-
CL2,"CDC tooling adds >200ms p99 latency at scale",H2,s09;s14,industry;industry,own;own,web-general|CDC latency benchmark|en;web-general|CDC latency benchmark|en,single-type,medium,N,-,-,2025-Q2
CL3,"Vendor X claims zero-downtime migration",-,s22,industry,own,web-general|vendor X migration|en,weak,low,N,vendor,-,-
CL4,"Product Z beats competitors 3.4x on benchmark",H3,s31,industry,own,web-general|product Z benchmark|en,weak,low,N,disputed:s33,s33,2025-Q4
CL5,"Adoption of X doubled year over year",H1,s18;s19;s27,industry;general-media;industry,press-release-acme-2026-03;press-release-acme-2026-03;press-release-acme-2026-03,web-general|X adoption growth|en;news-current|X adoption|en;web-general|X adoption growth|en,single-root,medium,N,-,-,2026-Q1
CL6,"The regulator permits practice Y without restrictions",H2,s41;s44;s52,industry;general-media;industry,assoc-brief-2026;assoc-brief-2026;own,web-general|Y regulation|ru;news-current|Y is permitted|ru;web-general|Y practice|ru,contested,medium,N,-,s60,2026-Q2
```

`CL6` — the dissent rule at work: three sources, two types, formally almost
triangulated, but `s60` (the regulator's primary document) contradicts them ⇒
`contested`, both positions in the report. `CL2` — all sources were found by one query in
one channel: the `paths` coincide, the independence is illusory.

**Three columns for the human version** (appended to the end of the row; old runs without them still build, but with a warning):

| Column | What | Example |
|---|---|---|
| `evidence_kind` | the type of material: `fact` (a fact, an event) · `study` (a study) · `position` (a position, an opinion — who says it and their interest) · `product` (a product, a price, an offer) · `case` (a case, an incident) · `norm` (a norm, a rule) · `absence` (we looked — and did not find) | `product` |
| `plain` | the same claim for a human without the context: one phrase, without the skill's codes and jargon | «Continuous checking with a public badge is already on sale — at least 4 products at $9–50 a month» |
| `detail` | the row the type requires: for `study` — method, sample, weak point; for `position` — who and their interest; for `product` — who, for whom, when checked; for `absence` — where it was searched | «VibeLegit, VibeSafely et al. They check security, not business rules» |

Numbers do not get a type — they are already in `numbers.csv`; there is also the optional `label` column — what this number is, in words.

**Holes (status ≠ triangulated) → gap wave.** See `phases/p5_claims.md` «Gap wave»: a targeted
`knowing-fetcher` for a specific hole, at most 2 rounds, otherwise honestly
`status: data-insufficient`.

## The sources/NN_slug.md file — template

Each source = a separate file. This is the long-term memory of the research — a month later you come back and see quotes with metadata without re-reading the report.

The numbering is continuous (`01`, `02`, ...). The slug in the file name is short, by the topic of the source.

```markdown
---
id: s03
url: https://example.com/article
title: <Title>
author: <Author Name>
date: 2024-03-15
type: Primary                    # STRICT enum, exactly one: Primary | Academic | Industry-media | General-media | Expert-blog | Forum | Other. Free form breaks the «≥2 different types» count in triangulation
channel: <channel-name>          # from channels.md (web-general | academic | preprint-servers | code-github | forum-discussion | etc)
credibility: 5
recency: 4
bias: 4                          # the Bias scale = NEUTRALITY: 5 = independent/scientific, 1 = propaganda. More = better, as with the two axes above
total: 13
caveat: -                        # STRICT enum, exactly one: - | vendor | self-reported | disputed:sNN. The explanation — into the body of the file, NOT here
root: own                        # the primary source the material is based on: own | <short root id, e.g. "press-release-acme-2026-03" | "study-smith-2024" | "gartner-mq-2025">
discovery_path: web-general|EU vertical farming yield 2025|en   # HOW it was found: <channel>|<exact query>|<language>. The fourth triangulation condition — copy-pasting this field inflates independence
origin_kind: -                   # only for sources with numbers. STRICT enum: measurement | registry | filing | survey | model-estimate | secondary | unknown | -
origin_url: -                    # the URL of the document that PRODUCED the number (filing / dataset / article with a methodology), not of the page where you read it. `-` if you did not find it — an invented URL is worse than an honest dash
data_as_of: -                    # the date of the DATA (2025-Q3), NOT of publication. `unknown` if there is a number but no measurement date; `-` for non-numeric sources
chain_len: 0                     # 0 — the source produced the number itself, 1 — a retelling of the primary, 2+ — a retelling of a retelling
used: Y                          # Y — made it into the basis of the findings, N — only for context
hypothesis_evidence:
  H1: supports                   # supports | contradicts | partial | neutral
  H2: contradicts
  H3: neutral
language: en | ru | de | ...
access: OPEN | PARTIAL | PAYWALLED | paywalled-abstract-only | closed | archive-restored | GRAY-AREA-SOURCE
fetched: 2026-05-21              # extraction date
fetch_tier: webfetch              # webfetch | http | browser — what the content was taken with
fetch_note: -                     # - | AI exclusion in robots | robots-disallowed, operator-overridden
content_kind: -                   # - (html) | pdf | feed — a feed gives an annotation, not the full text
---

# <Title>

## Summary
2-4 sentences in your own words: what the source says on the topic.

## Key quotes

> …the sentence before. «Direct quote 1 — verbatim.» The sentence after…
> *— Section 2, page 34*

> «Direct quote 2.»
> *— Section "Methodology"*

## Supports hypotheses

- **H1: supports** — quote 1 directly asserts X
- **H3: partial** — quote 2 supports only under condition Y

## Contradicts / refutes

- **H2: contradicts** — the author asserts the opposite, see quote 2. This is a serious counter — account for it in the adversarial pass.

## Source dissection

- **Claim type:** measurement | opinion | marketing — by the main claim; for a mixed source — by the claim we rely on.
- **Method and data:** how it was obtained (a measurement, a sample of N, a survey, a single-company case, «in our experience»); no method — say so.
- **Where it applies:** version, scale, industry, year; where the conclusion no longer holds.
- **Modality verbatim:** «may», «typically», «in our tests» — as in the original, without strengthening.
- **Limitations and the author's interest:** who the author is, what they sell, what the source did not check.

The card is written by `mid` in batches of 5–8 files after fetch (`phases/p4_search.md` 4.1); the fetcher on `small` does not fill it in. A quote in Key quotes comes with ±1 sentence of context, otherwise modality and conditions are lost.

## Related sources

- s07 — the same author, another publication (risk of double counting in triangulation)
- s12 — the opposite position
- s15 — supports the same claim from a different source type
```

## Row template for sources.csv

An index of all sources, updated as they are added.

```csv
№,URL,Title,Type,Channel,Access,Author,Date,Credibility,Recency,Bias,Total,Used,File,Note
1,https://vam.ac.uk/...,V&A Open Storage,Primary,web-general,OPEN,V&A Curator,2023-11,5,4,4,13,Y,sources/01_vam-open-storage.md,Direct source
2,https://museum-id.com/...,Museum-iD article,Industry-media,industry-reports,OPEN,J. Smith,2024-02,4,5,4,13,Y,sources/02_museum-id.md,Support for H1
3,https://reddit.com/...,Reddit thread,Forum,forum-discussion,OPEN,anon,2024-09,1,5,3,9,N,sources/03_reddit.md,Public reaction only
```

`Type`: Primary / Academic / Industry-media / General-media / Expert-blog / Forum / Other.
`Channel`: a value from channels.md (web-general / academic / preprint-servers / code-github / etc).
`Access`: OPEN / PARTIAL / paywalled-abstract-only / closed / archive-restored.

## Anti-patterns

- ❌ Accepting the first source found without scoring it.
- ❌ Using forum quotes as proof of a claim.
- ❌ Taking a piece of news 5-10 years old about a rapidly changing topic.
- ❌ Citing one author as «independent confirmation» in several different publications — that is one voice.
- ❌ Marking a source «total 12+» without recomputing — recompute explicitly.
- ❌ Paraphrasing quotes in `sources/NN.md` — verbatim only.
- ❌ Compressing all sources into one file — searchability, reuse and the reference from the report are lost.
- ❌ Setting `confidence: high` in `claims.csv` without a primary source — violates the primary-first rule, even if formally there are 3+ sources of different types.
- ❌ Leaving a `claims.csv` row without a status after the first pass — run the gap wave (Phase 4.5), at most 2 rounds, then honestly `data-insufficient`.
