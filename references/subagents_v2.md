<!-- translated from upstream/references/subagents_v2.md @ e233797 — see docs/TRANSLATION.md -->
# Subagents v2 — parallel search via the Agent tool

## Contents

- Architecture
- Which subagent_type
- Which model to choose (model routing)
- Parallelism
- The prompt to a sub-agent — template
- After the sub-agents return — what the main thread does
- Anti-patterns
- When NOT to launch sub-agents

Applies in **medium** (2–3 sub-agents) and **deep** (4–5) modes.

`<SKILL_DIR>` = the absolute path to this skill's own directory (the one holding `SKILL.md`); the main thread expands it at call time. Paths to skill files in agent briefs are written as `<SKILL_DIR>/…`.

## Architecture

```
Main thread (assistant):
  - builds the plan, splits the topic into subtopics
  - assigns each agent a range of source numbers (s01-s09, s10-s19, ...)
  - launches the sub-agents in ONE message (parallel)
  - receives ONLY index rows for sources.csv (URL/title/type/date/scores/
    subquestion_ids/file) — not full texts
  - merges sources.csv, dedups by URL across ranges
  - fills claims.csv from the index rows + declared claims
  - triangulates over claims.csv, synthesizes

Sub-agent (subagent_type=knowing-fetcher, its own range NN):
  - reads its prompt (including the pinned range of numbers)
  - does WebSearch + WebFetch
  - scores each source itself (no separate scoring pass — H7)
  - WRITES full sources/NN_slug.md files in its range (Write — in parallel,
    without conflicts, since the ranges do not overlap)
  - returns to the main thread ONLY index rows (compactly — full source
    texts do not pass through the main context)
```

This way the main thread is not bloated by raw source texts (only compact index rows), and the parallel writing of `sources/NN.md` does not conflict, because every agent has its own non-overlapping range of numbers.

## Which subagent_type

- **`knowing-fetcher`** — the default for fetch + save (Phase 4.1). Writes each source to
  `sources/NN.md` itself, inside its assigned id range, so full texts never travel back into the main
  thread. Default model `small`, medium effort, `maxTurns 40`. Ships in this repo at
  `agents/knowing-fetcher.md` — install it with `cp agents/*.md ~/.pi/agents/`.
- **`Explore`** (built in) — read-only reconnaissance with no files written: Phase 3.5 capability
  discovery, or a quick «is there enough material here at all» before splitting into subtopics. The
  moment an agent needs to write `sources/NN.md`, that is `knowing-fetcher`.
- **`knowing-redteam`** — the adversarial pass. Read-only, `big` model, high effort; ships at
  `agents/knowing-redteam.md`. Launch it only after synthesis, on the assembled claims.


## Which model to choose (model routing)

Before launching sub-agents, read `model_routing.md`: it holds the phase × subtask → executor matrix, and this excerpt is incomplete without it.

A short excerpt for Phase 4.1 (launch sub-agents):

| Subtask type of the sub-agent | Executor | Model / Effort |
|---|---|---|
| Web search + metadata (web-general/news/forum) | `knowing-fetcher` | `small` / medium |
| Read long source + extract quotes | `knowing-fetcher` | `small` / medium |
| Academic / preprint-servers | `knowing-fetcher` | `small` / medium |
| API-direct (curl + jq) | `knowing-fetcher` | `small` / medium |
| Code analysis (clone + grep) | `knowing-fetcher` gathers facts and paths; conclusions stay on the main thread | `small` / medium |
| Heavy reasoning subtask | `main` | — |

**Default if unsure** → `knowing-fetcher`.

The model and effort of `knowing-fetcher` are recorded in its frontmatter; the call does not pass them, so that the setting lives in one place. Escalation after a refusal or a thin result — `general-purpose` with explicit `model: "big"`, `thinking: "high"`, see `model_routing.md` «How to pass the model into the `Agent` tool».

```
Agent({
  subagent_type: "knowing-fetcher",   // fetch+save needs Write, see above
  description: "...",
  prompt: "..."
})
```

## Parallelism

In one assistant message — ALL Agent calls simultaneously.

If there are 4+ sub-agents — launch with `run_in_background: true`:
- Real parallelism, not a queue.
- Notifications when each one finishes — no polling needed.
- You can start assembling the results as they arrive.
- Caveat: background sub-agents get a trimmed tool set — before launching a fetch in the background, check that the needed Write/WebFetch are available; if it has not been checked — launch in the foreground.

If there are 2 sub-agents — you can do without background (faster per round).

## The prompt to a sub-agent — template

**Source of the prompt's content.** The sub-agent's prompt is **NOT written from scratch** — it is assembled from the ready `plan.md`:

- `SUBTOPIC` ← the planned subtopic (from `plan.md` section 11 — the «Subtopic ↔ Blocks mapping» table)
- `BLOCKS THIS SUBTOPIC FEEDS` ← from the same table (which blocks we are gathering for)
- `HYPOTHESES TO TEST` ← from `plan.md` section 9 (only those relevant to the subtopic)
- `CHANNELS TO USE` ← from `plan.md` section 12 after Phase 4.0 Source Dispatch: already laid out into **primary / secondary / fallback** via the `source_dispatch.md` matrix. The sub-agent does NOT choose channels itself — it follows the already fixed dispatch strategy.
- `STAT-SOURCES TO USE` ← from the same section 12 → stat sources (concrete files from `stat_sources/`)
- `API ENDPOINTS TO USE` ← from the same section 12 → concrete APIs from `api_sources/` (noting which auth-env-vars are needed)
- `DISCOVERY EXECUTED` ← from section 12: what was already found via the awesome-lists registry / GitHub topics / HuggingFace at step 4.0 — the sub-agent can build on that, not repeat the discovery in vain
- `CRITICAL GAPS` ← from section 12 → critical gaps to address for this subtopic
- `SOURCE ID RANGE` ← the range of source numbers pinned to this agent, assigned by the main thread BEFORE launch: agent #1 → `s01-s09`, #2 → `s10-s19`, #3 → `s20-s29`, etc. (a step of 9-10 numbers with headroom). The ranges do not overlap — this removes conflicts during the parallel writing of `sources/NN.md`.

This way the main thread does not duplicate the plan's work and provides transparency: in plan.md the user sees exactly the same brief as the agent.

Every prompt is **self-contained** — the sub-agent does not see the context of the main dialogue.

**Prompt language.** If the subtopic is English-language sources (international institutions, tech, academic) — write in English. If it is the RU segment — in Russian. The quality of the sub-agent's answers is better when the prompt language and the language of the sources match.

### EN template

```
CONTEXT: We are researching <main_question>. This is the deepdive workflow,
medium/deep depth, with structured JSON output requested.

YOUR SUBTOPIC: <narrow subtopic — what THIS agent looks for, not the whole theme>

YOUR SOURCE ID RANGE: s<NN>-s<MM> (e.g. s10-s19). Use ONLY these numbers for the
files you write. Do not reuse a number outside your range — other agents are
writing in parallel with their own ranges.

BLOCKS THIS SUBTOPIC FEEDS:
- <block-id>: <what data the block needs>
- <block-id>: <what data the block needs>
(from plan.md section 11 — subtopic↔blocks mapping)

HYPOTHESES TO TEST:
- H1: <falsifiable statement>
- H2: ...
- (only the hypotheses relevant to THIS subtopic)

SOURCING STRATEGY (already dispatched via source_dispatch.md — DO NOT re-pick):
- Primary channel: <channel-name> — <what specifically>
  Query template: `<...>`
  Specific endpoints: <api_sources/.../X.md> if api-direct
- Secondary channel: <channel-name> — <what>
  Query template: `<...>`
- Fallback channel: <channel-name> — only if primary/secondary fail

See <SKILL_DIR>/references/channels.md for query patterns, paywall fallback protocols, limitations.

DISCOVERY ALREADY EXECUTED (from plan.md section 12):
- <awesome-list or repo found at dispatch step — start there, don't rediscover>
- <huggingface/kaggle dataset already identified>
- <github topic search result>
(if none — discovery wasn't run for this subquestion; you may run it but flag it)

STAT-SOURCES TO USE (if relevant):
- `stat_sources/<path>.md` → <source name> for <metric>
- `stat_sources/<path>.md` → <source name> for <metric>

Direct these sources for quantitative claims. Use the URLs/queries from those files.

STANCE (read before you start):
A source can be unreliable, and every source has interests of its own. Popularity
is not evidence and agreement between sources is not evidence either — ten pages
can agree because they copied one press release. As you read, actively look for
CONTRADICTIONS between sources and ask of each: who produced this material, who
paid for it, and would they publish the opposite finding? Record what you find in
the fields below; do not silently pick a winner.

TASK:
1. Search using the channels above. For 5-10 sources total across all channels.
   Different source types: Primary, Academic, Industry-media, General-media,
   Expert-blog, Forum, Opposition.
2. For each source — read it (WebFetch) and extract:
   - If WebFetch comes back THIN — under ~500 chars of main text, no quotable
     passage, or a block/consent/paywall page — run the ladder RIGHT THEN, as a
     standard step, not as an exception:
     `uv run <SKILL_DIR>/scripts/fetch_source.py <URL> -o <run>/.fetch/NN.md --meta <run>/.fetch/NN.json`
     Record `fetch_tier:` from the metadata in the source frontmatter.
   - 2-4 key direct quotes (verbatim, with location/page if possible)
   - Author, publication date, source type. `type` is a STRICT enum — copy ONE
     of these seven verbatim, never invent a label or a variant spelling:
     Primary | Academic | Industry-media | General-media | Expert-blog | Forum | Other.
     Triangulation counts DISTINCT types, so a free-form label silently inflates
     type diversity and turns a one-type claim into a "triangulated" one.
   - How it relates to each hypothesis (supports / contradicts / neutral)
3. Score each source YOURSELF on three axes 1-5 (no separate scoring pass follows —
   you are the one who read it, you score it):
   - Credibility: 5=primary/peer-review, 4=industry-authority, 3=quality general media,
     2=expert blog, 1=forum/anon
   - Recency: 5=<1yr, 4=1-3yr, 3=3-5yr, 2=5-10yr, 1=>10yr (unless historical topic)
   - Bias: 5=neutral/scientific, 4=industry-neutral, 3=mainstream with known slant,
     2=lobbyist, 1=propaganda
4. Include at least 1-2 sources representing opposition or criticism of the
   dominant view in this subtopic: the stop criteria require an analysed opposition
   search, and red team has nothing to test without it. If you cannot find any,
   say so explicitly.
5. WRITE the full source file yourself: `sources/<id>_<short-slug>.md` using the
   template in `<SKILL_DIR>/references/source_scoring.md`, with complete frontmatter (channel, access,
   scores, subquestion_ids) and verbatim quotes. Never write a source with fewer
   than 2 verbatim quotes: run the ladder first. If the ladder ends in auth-wall /
   anti-bot, write it with `access: closed` and only what the snippet gave — such a
   source cannot be a triangulation leg. Use ONLY ids from your assigned
   range (see YOUR SOURCE ID RANGE above).
   Fill the `root:` field while reading (see source_scoring.md "Provenance"):
   `own` if the source produced its material itself; a short stable id of the
   underlying material it retells (e.g. `press-release-acme-2026-03`,
   `study-smith-2024`) otherwise; `unclear` if you cannot tell where the data
   comes from. Ten articles retelling one press release are ONE voice — the
   triangulation rule counts distinct roots, so this field is not optional.
   If several sources retell the SAME underlying material, they must carry the
   BYTE-IDENTICAL root string — otherwise root dedup silently fails.
   Own measurements (a lab run, benchmark, or experiment you executed) all share
   ONE root `own-lab-<slug>`, however many files the results are split across —
   three slices of one run are one voice, not three.

   Also fill `discovery_path:` — HOW you reached this source: `<channel>|<exact
   query string>|<language>` (e.g. `web-general|EU vertical farming yield 2025|en`,
   or `api-direct|FRED:CPIAUCSL|-` for a registry pull). Two sources found by the
   same query in the same channel are ONE sampling of one index, however different
   they look; triangulation counts distinct discovery paths as its fourth
   condition, so a copy-pasted value here inflates independence.

   For any source carrying a NUMBER you expect to use, also fill:
   - `origin_kind:` — one of `measurement` | `registry` | `filing` | `survey` |
     `model-estimate` | `secondary` | `unknown`. What KIND of act produced the
     number, not who republished it.
   - `origin_url:` — URL of the document that PRODUCED the number (the filing, the
     dataset, the paper with methodology). Not the page you read it on, unless
     that page is itself the producer. `-` if you could not find it.
   - `data_as_of:` — the date of the DATA (`2025-Q3`, `2024-12`), not the
     publication date of the article. A number whose data date you cannot
     establish is a number you must mark `unknown`.
   - `chain_len:` — `0` if this source produced the number itself, `1` if it
     retells the producer directly, `2+` if it retells a retelling.
   Do not guess these to look complete: `unknown` / `-` is a valid, useful answer
   and is treated as a quarantine flag downstream. A fabricated `origin_url` is
   far worse than an honest `-`.
6. For each claim/thesis this subtopic supports, note it as a candidate row for
   `claims.csv` (claim text, hypothesis id if any, which source ids back it, source
   types, whether at least one is Primary — the "primary_source" flag).

OUTPUT FORMAT — write the JSON below to `<run>/agent_reports/<subtopic-id>.json`
(strict JSON, compact index rows, NOT full source text — that already lives in the
files from step 5). Your final chat reply is ≤15 lines: the JSON file path, counts
(sources kept / claim_candidates / systems), top-3 gaps, opposition found yes/no.
Do NOT paste the JSON into the reply — measured: replies with the JSON inline ran
19–24k chars each (~10k tokens of the main thread), replies with a line limit 3–5k.

JSON file content:

{
  "subtopic": "<this subtopic>",
  "summary": "<3-5 sentence summary of what you found>",
  "source_index": [
    {
      "id": "s07",
      "url": "https://...",
      "title": "...",
      "type": "Primary|Academic|Industry-media|General-media|Expert-blog|Forum|Other",
      "channel": "<channel-name-from-channels.md>",
      "date": "YYYY-MM-DD or YYYY",
      "credibility": 5, "recency": 4, "bias": 4, "total": 13,
      "root": "own | <root-id> | unclear",
      "discovery_path": "<channel>|<exact query>|<lang>",
      "caveat": "- | vendor | self-reported | disputed:sNN",
      "origin_kind": "measurement|registry|filing|survey|model-estimate|secondary|unknown",
      "origin_url": "https://... or -",
      "data_as_of": "YYYY-QN or YYYY-MM or -",
      "chain_len": 0,
      "subquestion_ids": ["Q2"],
      "file": "sources/07_<slug>.md"
    }
  ],
  "claim_candidates": [
    {
      "claim": "<one-line thesis>",
      "hypothesis": "H1",
      "sources": ["s07", "s09"],
      "source_types": ["Primary", "Industry-media"],
      "primary_source": true,
      "as_of": "2025-Q3 or -",
      "dissent": ["s12"]
    }
  ],
  "contradictions": [
    {
      "about": "<what the sources disagree on, one line>",
      "sides": {"sNN": "<what this source claims>", "sMM": "<what that one claims>"},
      "resolvable": "yes|no|unclear",
      "note": "<if one side is primary/methodologically stronger, say which and why>"
    }
  ],
  "opposition_found": true,
  "opposition_summary": "<if true: what the opposition argues, otherwise null>",
  "gaps": ["<what you searched for but did not find>"],
  "query_performance": [
    {"query": "<exact query string>", "channel": "<channel>", "yield": "used|noise|empty"}
  ]
}

`query_performance`: one row per distinct query you actually ran. `yield`: "used" —
produced at least one source you kept; "noise" — hits, but nothing worth keeping;
"empty" — no relevant hits. The orchestrator uses this to mutate next round's
queries (language switch, operators, terminology) instead of re-running what failed.

`contradictions`: report every disagreement you found, INCLUDING ones where a single
source contradicts several others. Do NOT resolve a disagreement by majority and
report only the winner — a lone regulatory filing outranks three articles retelling
each other, and the ledger, not you, decides. If you found no contradictions at all
in a contested topic, say so explicitly in `gaps` — it usually means you only read
one side.

`dissent` (inside `claim_candidates`): ids of sources you read that CONTRADICT this
claim. Leave `[]` only if you actually looked for opposing sources under this claim.

CONSTRAINTS:
- Maximum 10 sources. Quality over quantity.
- Do not spawn subagents. Stop rule: 5 queries in a row without a new source → return the list of gaps and stop.
- Quotes must be VERBATIM. Do not paraphrase.
- If a source is paywalled / inaccessible — note it in `gaps` and try alternative.
- Do not use bash/curl to bypass WebFetch. The one sanctioned ladder is
  `uv run <SKILL_DIR>/scripts/fetch_source.py <URL> -o <run>/.fetch/NN.md --meta <run>/.fetch/NN.json`
  — it is the STANDARD second step, not an exception. Run it whenever WebFetch
  answers "unable to fetch from ..." OR returns a thin result (<500 chars of main
  text, no quotable passage, block/consent/paywall page): usually a robots.txt
  AI-agent exclusion or a JS-only page, not a dead one. Copy `access:`, `fetched:`,
  `fetch_tier:` and any `fetch_note:` from the metadata into the source frontmatter.
  A thin source (<2 verbatim quotes, or `access: PARTIAL/closed`) is not a
  triangulation leg — validate_phases.py errors on a `triangulated` claim standing
  only on such sources.
- Exit 4 (auth wall / anti-bot) is terminal for the HTML, not for the source. The
  script prints the open doors of that same site — official API, feed, archive
  snapshot — from `<SKILL_DIR>/references/fallback_routes.yaml`. Work that list top-down before
  giving up. Feeds very often survive when the HTML is blocked (stackoverflow HTML
  403, its Atom feed 200). Do not retry the HTML harder.
- A feed gives title, date, summary and URL — NOT the full article. Quote from a
  summary only as a summary, and never present it as a quote from the article.
- A PDF is saved as `.pdf`, not markdown, and the metadata says `content_kind: pdf`.
  Read it with the Read tool (it takes a `pages` range). Preprints and working
  papers arrive as PDFs, so this is the normal academic path, not an edge case.
- Exit 3 means robots.txt closes the path to every client, not just AI agents. Never
  pass `--ignore-robots` yourself — record the URL in `gaps` and move on.
- If both WebFetch and the ladder fail — try an alternative source, don't insist.
- Do NOT return full source text/quotes in your final JSON reply — they belong in
  the files you wrote. Returning them again bloats the main thread's context.
```

### RU template

```
КОНТЕКСТ: Исследуем <главный вопрос>. Workflow — deepdive, режим medium/deep,
ожидается структурированный JSON.

ТВОЯ ПОДТЕМА: <узкая подтема — что ищет ЭТОТ агент, не вся тема>

ТВОЙ ДИАПАЗОН НОМЕРОВ ИСТОЧНИКОВ: s<NN>-s<MM> (например s10-s19). Используй ТОЛЬКО
эти номера для своих файлов — другие агенты параллельно пишут в своих диапазонах.

ГИПОТЕЗЫ ДЛЯ ТЕСТИРОВАНИЯ:
- H1: <опровергаемое утверждение>
- H2: ...

ПОЗИЦИЯ (прочитай до начала):
Источник может быть недостоверным, и у каждого источника есть свой интерес.
Популярность — не доказательство, согласие источников между собой — тоже: десять
страниц могут совпадать потому, что переписали один пресс-релиз. По ходу чтения
специально ищи ПРОТИВОРЕЧИЯ между источниками и спрашивай о каждом: кто произвёл
этот материал, кто за него платил и опубликовал бы он обратный результат.
Найденное фиксируй в полях ниже; не выбирай молча «правильную» сторону.

ЗАДАЧА:
1. Найти 5-10 источников разных типов: первичные, академические, отраслевая медиа,
   общая пресса, экспертные блоги, обсуждения, противоположная позиция.
2. Каждый источник прочитать (WebFetch) и извлечь:
   - Если WebFetch вернул ТОНКО — меньше ~500 знаков основного текста, ни одной
     цитируемой фразы, страница блокировки/консента/paywall — сразу запускать
     лестницу, это штатный шаг, а не исключение:
     `uv run <SKILL_DIR>/scripts/fetch_source.py <URL> -o <run>/.fetch/NN.md --meta <run>/.fetch/NN.json`
     `fetch_tier:` из метаданных перенести во frontmatter источника.
   - 2-4 прямые цитаты (дословно, с указанием раздела/страницы если есть)
   - Автор, дата публикации, тип источника
   - Отношение к каждой гипотезе (supports / contradicts / neutral)
3. Оценить каждый источник САМОМУ по 3 осям 1-5 (отдельного scoring-прохода не
   будет — кто прочитал, тот и скорит):
   - Credibility: 5=первичный/peer-review, 4=отраслевая медиа, 3=качественная пресса,
     2=экспертный блог, 1=форум/анон
   - Recency: 5=<1г, 4=1-3г, 3=3-5л, 2=5-10л, 1=>10л
   - Bias: 5=нейтральный/научный, 4=отраслевая нейтральная, 3=мейнстрим с уклоном,
     2=лоббист, 1=пропаганда
4. КРИТИЧНО: включить ≥1-2 источника с противоположной позицией / критикой
   доминирующего взгляда. Если не нашёл — сказать прямо.
5. ЗАПИСАТЬ полные файлы `sources/<id>_<slug>.md` самому (шаблон в
   `<SKILL_DIR>/references/source_scoring.md`), используя только номера из своего диапазона.
   Обязательно заполнить: `root:` (первоисточник материала), `discovery_path:`
   (`<канал>|<точный запрос>|<язык>` — как ты дошёл до источника), `caveat:`.
   Для источников с ЧИСЛАМИ — ещё `origin_kind:` / `origin_url:` / `data_as_of:`
   (дата ДАННЫХ, не публикации) / `chain_len:`. Не выдумывай значения ради
   заполненности: `unknown` и `-` — валидные ответы, они уводят число в карантин,
   а придуманный `origin_url` отравляет весь вывод.
6. Для каждого тезиса, который подтверждает эта подтема, — кандидат-строка для
   `claims.csv` (текст тезиса, гипотеза, какие sources подтверждают, их типы,
   есть ли среди них primary source).

ФОРМАТ ВЫВОДА — JSON записать в `<run>/agent_reports/<id-подтемы>.json` (строгий
JSON, компактные index-строки, НЕ полные тексты источников — они уже в файле из
шага 5). Финальный ответ в чат ≤15 строк: путь к JSON, счётчики (источников /
claim_candidates / систем), три главных gaps, оппозиция найдена да/нет. JSON в чат
НЕ вставлять: с JSON в ответе было по 19–24 тыс. символов, с лимитом строк — 3–5 тыс.
Содержимое файла:

[см. EN шаблон выше — структура `source_index` + `claim_candidates` та же]

ОГРАНИЧЕНИЯ:
- Максимум 10 источников. Качество важнее количества.
- Субагентов не спавнить. Стоп-правило: 5 запросов подряд без нового источника → вернуть список gaps и остановиться.
- Цитаты ДОСЛОВНЫЕ. Не пересказ.
- Если источник за paywall — в `gaps`, искать альтернативу.
- НЕ использовать произвольный bash/curl в обход WebFetch. Единственная санкционированная лестница:
  `uv run <SKILL_DIR>/scripts/fetch_source.py <URL> -o <run>/.fetch/NN.md --meta <run>/.fetch/NN.json`
  — это ШТАТНЫЙ второй шаг, не исключение. Запускать и когда WebFetch ответил
  «unable to fetch from …», и когда вернул тонкий результат (<500 знаков основного
  текста, нет цитируемой фразы, страница блокировки/консента/paywall): обычно это
  robots-исключение для AI-агентов или JS-only страница, а не мёртвая. `access:`,
  `fetched:`, `fetch_tier:` и `fetch_note:` из метаданных перенести во frontmatter.
  Источник без 2 дословных цитат не пишется вовсе; если лестница упёрлась в
  auth-волл/анти-бот — писать с `access: closed` и только тем, что дал сниппет, и
  плечом триангуляции он быть не может (validate_phases.py даёт error).
- Код 4 (auth-волл / анти-бот) — терминально для HTML, не для источника. Скрипт сам
  печатает открытые двери того же сайта (API, фид, архив) из `<SKILL_DIR>/references/fallback_routes.yaml` —
  идти по списку сверху вниз. Фид часто жив, когда HTML мёртв: у stackoverflow HTML
  403, а его Atom-фид 200. HTML сильнее не долбить.
- Фид даёт заголовок, дату, аннотацию и URL — НЕ полный текст. Цитату из аннотации
  помечать как аннотацию, не выдавать за цитату из статьи.
- PDF сохраняется как `.pdf`, не как markdown, и в метаданных стоит `content_kind: pdf`.
  Читать штатным `Read` с диапазоном `pages`. Препринты и рабочие бумаги приезжают
  PDF-ами — это основной академический путь, не краевой случай.
- Код 3 — robots закрывает путь всем клиентам, не только AI. `--ignore-robots` самому
  НЕ ставить: URL в `gaps` и дальше.
- НЕ возвращать полные цитаты/тексты источников в финальном JSON — они уже в
  записанных файлах, повторный возврат раздувает контекст главного потока.
```

## After the sub-agents return — what the main thread does

1. **Parsing the JSON.** Read `agent_reports/<id>.json` with a python script (`json.load`), into the context — only the counters, not the file itself. No file or garbage — ask the agent to rewrite the file, do not interpret it yourself. Expect `source_index` (compact rows) + `claim_candidates` — NOT full source texts (the agent already wrote them itself, see above).

2. **Dedup by URL — and measuring `overlap_rate` (do not throw the duplicate away silently).** If two sub-agents found the same URL — it is ONE source: keep the file with the better scoring, mark the second record as a duplicate in `sources.csv`. But the very fact of a match is **the most valuable diagnostic of the round, and it disappears if the duplicate is simply deleted**.

   Agents are low-dispersion: only the context, the scaffold and the model distinguish them. If all three coincided — the actions will coincide too (Anthropic Frontier Red Team, 13.08.2026: 18 of 30 agents created a branch with the same name, not one of them was asked to). Your fetch agents receive one prompt template, one model and one search index — only the subtopic differs. Therefore:

   ```
   overlap_rate = (URLs found by >1 agent) / (unique URLs of the round)
   ```

   Write it into `plan.md` section 15 (notes) for every round and treat it as follows:
   - **overlap_rate > 0.3** — the agents searched alike, source diversity is fictitious. A query mutation is **mandatory** in the next round (RU↔EN, channel change, other terminology) plus separating the agents along search axes, and not only by subtopics.
   - **overlap_rate < 0.05 with high novelty** — healthy separation, continue as is.
   - **overlap_rate = 0 on all rounds** — check that the agents are searching in overlapping areas at all; zero overlap on a broad topic more often means that each agent found a random sample, not that they are well separated.

   A URL match between agents is a signal of conformism, not a «lucky validation of the finding».

3. **Merge of `sources.csv`** from all `source_index` — the files are already on disk (the agents wrote them themselves within their ranges), here the main thread only consolidates the index, it does not rewrite `sources/NN.md`.

4. **Filling `claims.csv`** from all `claim_candidates` (Phase 5 — see `source_scoring.md`, the claims-ledger section). Merge duplicate claims from different agents (if the thesis is one and the same — combine sources/source_types into one row).

5. **Write-perimeter check (machine, not on trust).** The range of numbers is held only by the prompt text — the agent has `Write` and an isolated context. After the sub-agents return, reconcile the actual contents of `sources/` with the ranges handed out:

   ```bash
   ls research/<slug>/sources/ | grep -oE '^[0-9]+' | sort -n | uniq
   ```

   A file with a number outside all the ranges handed out ⇒ the agent went outside the perimeter ⇒ its result is invalid: the file is not accepted into `sources.csv`, the row is flagged in `plan.md` §15, on a repeat — the agent is restarted with a narrowed task. This is checked at finish-up too (`validate_phases.py`). The boundary must be held by a mechanism, not by the model's politeness.

6. **Coverage check:**
   - How many source types? (≥4 needed)
   - Was opposition found? (at least one needed)
   - Did all hypotheses receive evidence? (≥3 sources per hypothesis needed)
   - How many `claims.csv` rows are NOT triangulated? → this is the entry into the gap wave (see `phases/p5_claims.md` «Gap wave»).

7. **Rebuilding the round window — `state.md`** (medium/deep; the rule is in `phases/p4_search.md`,
   «Round workspace»). The main thread has done everything above in a context where the
   results of all this round's agents already lie — and the decision about the next round is taken in that same
   window, and on top of the previous ones at that. Therefore before the next round the window
   is **rebuilt**: `state.md` is REWRITTEN (not appended to) from the results, and
   planning proceeds from it.

   ```markdown
   ---
   round: 3
   mode: medium
   ---
   ## Known
   - Q1 closed: rate 4.2% [s03][s07] (CL2, triangulated)
   - Q2 partial: the 2024 figure exists, no primary (CL5, single-root)
   - Q3 closed negatively: the registry has not been maintained since 2019 [s11]
   ## Gaps
   - Q2: primary registry not found, the `registry` channel not worked
   - Q4: empty in EN, the RU terminology not tried
   ## Next
   - round 3: 2 agents — registry for Q2 (s20-s24), RU mutation for Q4 (s25-s29)
   ```

   Rules:
   - **The known — by statuses, not by content.** A `Known` line references
     `claim_id`/`[sNN]`; the content lives in `sources/` and `evidence/`. As soon as paragraphs from sources
     appear in `state.md`, it turns into a second transcript
     — exactly what the window is rebuilt away from. Budget ≤6 KB, machine-checked at
     finish-up (`validate_phases.py`: >12 KB — an error).
   - **A negative result is also `Known`.** «The registry is not maintained» closes the
     subquestion; having dropped out of the window, it will come back as «we should look for a registry».
   - **`Gaps` is the only channel into the next round.** The agent of round N+1 receives
     its own hole, NOT someone else's `Known`: the ban on exchanging findings (see Anti-patterns below)
     is not lifted by rebuilding the window. Saving the orchestrator's context must not
     open a channel of conformism.
   - **`Next` is written with id ranges** — then the write perimeter (step 5) is checked in
     the next round too.
   - The history of the rounds is not lost: it is in `deviations.md` (triggers, novelty,
     circuit breaker) and `plan.md` §15 (overlap_rate, observations). `state.md` is a window, and
     not a journal.

## Anti-patterns

- ❌ Launching 1 sub-agent in medium — gives no parallelism, adds overhead. Do it in the main thread.
- ❌ Giving too generic a prompt «search about X» — a watery digest comes back. The subtopic must be NARROW.
- ❌ Launching sub-agents sequentially (Agent call → wait → the next one). Only in parallel in one message.
- ❌ Accepting a sub-agent's digest as final without checking. Dedup the URLs and check the scoring.
- ❌ Using `Explore` when the agent needs to write `sources/NN.md` — it is read-only and will not save the file. For fetch + save always use `knowing-fetcher`.
- ❌ Not assigning an agent a range of numbers BEFORE launch — without it the parallel writing risks an id collision.
- ❌ Asking a sub-agent to return full source texts/quotes in the JSON reply — bloats the main thread's context. The full text lives in the file, only the index row goes into the main thread.
- ❌ Leaving in the agent's prompt the «strict JSON in the reply» format without a limit on the reply size: 4 agents without a limit returned 19–24k chars each (~41k tokens of the main thread). JSON — into a file, into the chat ≤15 lines.
- ❌ Skipping the requirement «find the opposition» — by default sub-agents look for confirmation, not contradiction.
- ❌ **Separating the agents ONLY by subtopics.** The same template + one model + one language = one search trajectory, and triangulation receives correlated voices. Separate also along the search axis: agent A — English-language academia and preprints, B — the RU segment, local regulators and industry associations, C — practitioners (forums, issue trackers, discussions), D — primary registries and reporting. Then an overlap of findings is a signal of genuine independence, not an artifact of an identical prompt.
- ❌ **Passing the neighbours' findings into the second round.** The temptation is understandable, but the observability of others' actions is itself a coordination channel: in Anthropic's experiment the agents continued to collude after all communication channels were removed, synchronising through a public board. Letting agents see each other's findings is building such a board with your own hands and finishing off the remains of independence. Share only HOLES: «subquestions Q3, Q7 are not closed; on Q5 not a single opposition was found».
- ❌ Silently discarding URL duplicates between agents (see `overlap_rate` below) — this erases the only direct measurement of conformism. <!-- translator: ambiguous — upstream says "below", but overlap_rate is defined above, in step 2 -->

## When NOT to launch sub-agents

- **shallow** mode — 5-7 sources are faster to gather in the main dialogue.
- **A narrow topic** — if it does not split into 2+ subtopics, there is no point.
- **A topic in the project context that requires reading many project files** — a sub-agent does not see local files as easily; the main dialogue will cope faster.
- **Update mode with a small delta** — if 3-5 sources need to be dug up, the main thread will cope.
