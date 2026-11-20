<!-- translated from upstream/references/model_routing.md @ e233797 — see docs/TRANSLATION.md -->
<!-- translator: executor names are Claude Code agent types; on pi they map to Agent types — see docs/DECISIONS.md D6 -->
# Model Routing — which Claude model to take for each step

## Contents

- Principles
- Matrix: phase × subtask → executor + effort
- Routing for sub-agents (Phase 4.1)
- Cost economics
- Effort: what we control and what we do not
- How to pass the model into the `Agent` tool
- How to tell the user
- Override mechanics
- Anti-patterns

**When it is used:** at the start of each phase you choose the executor and the effort for the character of the task. Simple work (search, reading, extraction, classification) — to sub-agents on Haiku 5.5 (cheap, fast). Complex reasoning and architectural decisions — `main` (Opus) or `sub: deepdive-redteam`.

**Why:** without explicit routing a sub-agent inherits the main model (currently Opus 5.5); a forgotten `model` parameter = an expensive call. That is **expensive for bulk simple work** (URL search, scoring, dedupe) and **a bit weak for critical moments** (reframing, adversarial pass).

---

## Principles

1. **More expensive does not mean better.** A simple task on Opus = a waste of tokens. A complex one on Haiku = a weak result.
2. **Effort matters more than the model.** On the same model different `effort` values give a different result: Sonnet/high can be better than Opus/low for a middle-complexity task.
3. **Parallelism is a reason for a cheap model.** If we launch 5 sub-agents in Phase 4, they must be `sub: deepdive-fetcher` (Haiku), not Opus. Otherwise the cost of the research is multiplied by 5.
4. **Final deliverables are a reason for an expensive model.** Phase 1 reframing, Phase 6 red team and synthesis — that is where quality multiplies across the whole research. Do not skimp.
5. **Main thread vs sub-agent.** The main thread (`main`, where the user lives) — Opus. Sub-agents can be much cheaper — they have a narrow task with a fixed output.
6. **Economics: Opus is many times more expensive than Haiku 5.5** (the multipliers are in Cost economics below and in NOTES.md). Do not save on critical single calls (reframing, adversarial) — save on fan-out (N parallel sub-agents in Phase 4 and in the gap wave).

---

## Matrix: phase × subtask → executor + effort

> **The main session is Opus 5.5 (effort `medium`; the switch date is in `NOTES_dated.md`).** The `main` executor is the model of the main session (Opus 5.5); no separate model is chosen for it. If the session was explicitly raised to Fable 5.1 — **do not switch down**, Fable covers the `main` cells. The `sub: …` executors are sub-agents via `Agent` and do not depend on the session model. For agents from `~/.claude/agents/` (`deepdive-*`, `explore-haiku`) the model and effort are recorded in the frontmatter, and the call does not pass them: a per-call value overrides the frontmatter, and then the agent's setting is changed in two places, and they diverge silently. Only the built-in types (`general-purpose`) get `model` and `effort` per-call. Never use Fable in sub-agents (for the price see NOTES.md, and the slicing has already been done by the main session).
>
> **Cyber and bio topics.** Only the main model is remapped: if needed it is moved to `claude-opus-5` (by explicit ID); Opus 5.5 and Fable have `bio`/`cyber` filters of the same level, and both can return `stop_reason: refusal`. This does not extend to sub-agents: Haiku 5.5 has its own cyber classifier and there is no fallback (NOTES.md, «Orchestration», the Security block). A fetch on such topics goes through `sub: deepdive-fetcher` (Haiku from the frontmatter), and Haiku may refuse (`stop_reason: refusal`). Repeating the same request will be refused again, so on a refusal the subtask is taken over by `sub: general-purpose` with `model: "sonnet"`, `effort: "high"`: the same brief plus the line «format and rules — read `~/.claude/agents/deepdive-fetcher.md`».

Executor dictionary: `main` (the main model, Opus); `sub: deepdive-scout` (Haiku); `sub: deepdive-fetcher` (Haiku); `sub: deepdive-redteam` (Opus, high); `sub: deepdive-synthesizer` (Opus, high, writes the report); `sub: explore-haiku` (Haiku, read-only); `sub: general-purpose` (only writing tasks outside those listed).

| Phase | Subtask | Executor | Effort | Rationale |
|---|---|---|---|---|
| **Pre-discover** | Reading CLAUDE.md, checking existing research | `main` | inherit | Main thread, no need to switch |
| **Phase 1** | Reframing — restating the question, formulating hypotheses | `main` | inherit (medium) | Opus 5.5 on medium is not worse than Opus 5 on high. xhigh — only if a measurement showed a gain |
| **Phase 2** | Genre selection, choosing blocks | `main` | medium | A decision based on the preset table from genres.md |
| **Phase 3** | Plan composition (17 sections) | `main` | medium | An architectural decision, documents all future choices |
| **Phase 3.5** | Capability discovery — env vars audit, mapping | `sub: explore-haiku` | medium | Haiku 5.5 on low skips searches and checks |
| **Phase 4.0** | Source Dispatch — running subquestions through the matrix | `main` | medium | A lookup in `source_dispatch.md` + a record in plan.md |
| **Phase 4.1** | Launch sub-agents (web search, simple lookups) | `sub: deepdive-fetcher` | medium | A narrow task and JSON output. Cheap × N agents. Scores itself, see Phase 5 |
| **Phase 4.1** | Launch sub-agents (reading long sources, extracting quotes) | `sub: deepdive-fetcher` | medium | Haiku 5.5's window is 1M (NOTES.md), long sources fit |
| **Phase 4.1** | Launch sub-agents (api-direct: curl + jq + parse) | `sub: deepdive-fetcher` | medium | Bash work + mechanical JSON parsing |
| **Phase 4.1** | Launch sub-agents (code analysis in a repository) | `sub: deepdive-fetcher` | medium | The fetcher gathers facts and paths; conclusions about causes are made by `main` |
| **Phase 4.2** | Fetch + dedup (main thread) | `main` | medium | Manages the sub-agents, aggregates the results |
| **Phase 4** | Goal-check between rounds — per-subquestion `goal_status` met/partial/unmet + gap | `main` | low | Names the hole so that evaluation works from the diagnosis instead of deriving it from scratch. Labels only, takes no decisions |
| **Phase 4.3** | Save sources to files | `sub: deepdive-fetcher` | medium | The fetch agent writes itself into its own number range, see `subagents_v2.md` |
| **Phase 4.5** | Gap wave — targeted agents for the holes in `claims.csv` (status ≠ triangulated), maximum 2 rounds | `sub: deepdive-fetcher` | medium | A narrow task «find one more source of type X for claim Y» — an expensive model is not needed |
| **Phase 5** | Scoring (credibility/recency/bias by rubric) | *(built into Phase 4.1, see above)* | — | No separate pass is launched — the agent that read the source does the scoring |
| **Phase 4** | Candidate pool `candidates.csv` (title+snippet, academic APIs, snowball) — without reading (medium/deep) | `sub: explore-haiku` | medium (frontmatter) | Selecting by snippets requires no reasoning, but the pool is assembled by searching the APIs, and on low Haiku 5.5 skips searches; the expensive part is reading, which belongs to the fetchers |
| **Phase 5** | Triangulation check over `claims.csv` (mechanical: ≥3 sources AND ≥2 types AND ≥2 `root:` roots → triangulated) | `main`: `score_claims.py --write` | — | The rule is mechanical, a script computes it; no agent needed |
| **Phase 3.7** | Scout pass inside the plan gate — «which subquestions did we not ask» | `sub: deepdive-scout` | medium (frontmatter) | A short reconnaissance without recording sources, it does not create a separate phase. Cheap ×3-4 agents, see `plan_gate.md` step 1.5 |
| **Phase 5.5** | Evidence filter: relevance × authority over load-bearing pairs | `sub: explore-haiku` | medium | Two pairwise classifications over verbatim quotes; on low Haiku skips checks |
| **Phase 6** | Multi-angle red team — N hostile roles as sub-agents (deep: R1–R5; medium: R1+R2+R4, +R5 on dissent) | `sub: deepdive-redteam` | high | **A strong model is mandatory here.** An attack on the hypotheses (Skeptic/Contrarian/Gap-hunter/Implementer/Minority advocate) requires real reasoning, not pattern matching. The value comes from the DIFFERENCE OF ROLES and the isolation of contexts, not from the model class — not «raise everyone to opus» but spread the roles apart |
| **Phase 6.5** | Verify — liveness + faithfulness of quotes | `sub: explore-haiku` | medium | Entailment claim⊨quote is a judgment; on low Haiku skips checks |
| **Phase 6** | Synthesis — assembling the report from blocks | `sub: deepdive-synthesizer` | high | The long context of all sources + blocks + plan is held by the sub-agent, it does not get into the main thread |
| **Phase 6** | Final report write-up (language, style, cleanup) | `main` | medium | Quality writing |
| **Phase 8** | Decision walkthrough — executing the report along the Decision Spec forks with the user | `main` | high | Main thread, not a sub-agent. The quality of the questions multiplies into the applicability of the whole research — as in Phase 1, do not skimp |

Phase 6 red-team: deep → `sub: deepdive-redteam` (all five roles R1–R5); medium → `sub: deepdive-redteam` (R1+R2+R4, +R5 on dissent); shallow → R1 inline, executed on `main` (no sub-agent). Synthesis/chairman → `sub: deepdive-synthesizer` (medium/deep), `main` on shallow. Cost: +4–5 sub-agents per deep report (≈ cheap relative to the search).

---

## Routing for sub-agents (Phase 4.1)

In Phase 4.1 N (2-5) sub-agents are launched in parallel. Each gets a narrow subtask. All fetch and gap agents are `sub: deepdive-fetcher` (model `haiku`, effort `medium`, both from the agent's frontmatter; do not pass them in the `Agent` call). Deviation from the default — by subtask type:

| Sub-agent subtask type | Signals | Executor | Model / Effort |
|---|---|---|---|
| Web search + extract metadata (URL/title/date/snippet) | primary channel = `web-general`, `news-current`, `forum-discussion` | `sub: deepdive-fetcher` | haiku / medium |
| Read long source + extract pinned quotes | the subtask requires reading 5-10 long pages | `sub: deepdive-fetcher` | haiku / medium (window 1M) |
| Academic paper search + abstracts | primary channel = `academic`, `preprint-servers` | `sub: deepdive-fetcher` | haiku / medium |
| API-direct request + parse JSON | primary channel = `api-direct` (FRED, World Bank, etc.) | `sub: deepdive-fetcher` | haiku / medium |
| Gap wave (targeted search for a claim) | status ≠ triangulated in `claims.csv` | `sub: deepdive-fetcher` | haiku / medium |
| Code analysis (clone + grep + understand) | primary channel = `code-github` + impl-question | `sub: deepdive-fetcher` gathers facts and paths; conclusions about causes — `main` | haiku / medium |
| Scraping a site with pagination/state | primary channel = `competitive-signals` + scraping | `sub: deepdive-fetcher`; on failure — `sub: general-purpose` with `model: "sonnet"`, `effort: "high"` and the fetcher's instructions in the brief (Haiku is weaker at agentic tasks, see NOTES.md) | haiku / medium |
| Heavy reasoning sub-task (rare) | a subquestion «assess the trade-offs between X and Y», not just fact gathering | `main` | — |

**Default for a sub-agent** if unsure → `sub: deepdive-fetcher` (haiku / medium).

> **Haiku 5.5's quality on fetch has not been measured.** The choice of Haiku rests on prices and NOTES.md, not on a measurement for this skill. The check is on the first real run: the share of verbatim quotes that passed `check_number_provenance` and the verify faithfulness axis. If the share is noticeably lower than Sonnet's on the same subtopic, change `model` in the `deepdive-fetcher` frontmatter rather than passing `sonnet` in every call.

**Scoring is built in.** Each fetch sub-agent scores the source itself in the same call (reads → sets credibility/recency/bias → writes `sources/NN.md` into its own number range; the fetch agent needs `Write`, hence `sub: deepdive-fetcher` and not `explore-haiku` — see `subagents_v2.md`). There is no separate scoring pass.

---

## Cost economics

Model prices change faster than this file is rewritten — check the current ones via the
`claude-api` skill (it auto-syncs), not from memory. The price snapshot is dated in `NOTES_dated.md`:

| Model | Model ID | Alias in `Agent` | Input $/1M | Output $/1M | Context | Ratio vs Haiku |
|---|---|---|---|---|---|---|
| Haiku 5.5 | `claude-haiku-5-5` | `haiku` | $0.10 (≤100k prompt; above $0.50) | $0.50 (≤100k; above $2.50) | 1M | 1× |
| Sonnet 5.5 | `claude-sonnet-5-5` | `sonnet` | $2.00 | $10.00 | 1M | 20× |
| Opus 5.5 | `claude-opus-5-5` | `opus` | $4.00 | $20.00 | 1M | 40× |
| Opus 5 | `claude-opus-5` | — (explicit ID only) | $5.00 | $25.00 | 1M | 50× |
| Fable 5.1 | `claude-fable-5-1` | `fable` | $10.00 | $50.00 | 1M | 100× nominally, **effectively less** |

The ratio is computed from Haiku 5.5 at the ≤100k prompt rate (prices — NOTES.md). Haiku 5.5: accepts effort (default `medium`), 128K output, the tokenizer gives ~+30% tokens versus 4.5; exact characteristics — NOTES.md.

**The main shift: Haiku 5.5 is tens of times cheaper than Opus.** Keeping Opus on Phase 1/Phase 6 is still pennies against the background of the search; you need to save on fan-out (N sub-agents in Phase 4), not on these phases.

**Fable 5.1: the nominal rate overstates the price.** Cache reads at $0.25/MTok (−75% against Fable 5) give ~25% savings on typical loads and up to 45% on agentic ones — where the cache is reused. The multiplier in the table cannot be taken at nominal. This does not affect sub-agents anyway: we do not let Fable into them regardless, and `subagentPromptCacheTtl: 1h` in settings.json works for everyone.

**Read the Effort in the matrix below as the desired depth, not as the session policy.** The policy (`CLAUDE.md` § Models; date — `NOTES_dated.md`): default `medium`, `xhigh` only on the irreversible. The `high`/`xhigh` cells in the matrix are justified where a phase's mistake carries over into the whole research (Phase 1 reframing, Phase 6 red-team) — that is exactly the class «irreversible within the task». Lower the other cells when in doubt, do not raise them.

**The window is no longer a reason for Sonnet.** Haiku 5.5 has a 1M context, like the others (NOTES.md), so the subtask «read 5-10 long pages» stays with `sub: deepdive-fetcher`. Sonnet — only where Haiku does not hold up on quality (agentic code, multi-criteria gates).

**Do not put Fable 5.1 as the main orchestrator.** Only on an explicit user request and only for multi-day runs; in deepdive its price does not pay off on any phase.

## Effort: what we control and what we do not

Since Claude Code v2.1.292 the `Agent` tool accepts **`model` and `effort`**. The controllable levers:

- **the main thread** — `/effort` in the session (`low`/`medium`/`high`/`xhigh`/`max`);
- **the `deepdive-*` and `explore-haiku` sub-agents** — model and effort in the agent file's frontmatter; the Effort column of the matrix repeats the frontmatter for them and is not passed by the call. If they diverge — fix the frontmatter, not the call;
- **built-in sub-agents** (`general-purpose`) — `model` + `effort` per-call; without them they inherit the session's model and effort;
- **`Workflow` scripts** — `agent()` with `opts.effort`, as before.

The `xhigh` and `max` levels appeared after the first edition of this file. `xhigh` is the working maximum for coding and agentic tasks; `max` is greedy and prone to overthinking. For deepdive: `xhigh` — only on a phase where a measurement showed a gain (Opus 5.5 on xhigh thinks noticeably longer than Opus 5), `max` — is not appropriate anywhere (research runs into the quality of sources, not into the depth of one model's reasoning).

**Illustration (deep, ~5 sub-agents):** the numbers of the previous edition (Haiku 4.5 $1/$5) are outdated and not recalculated; Phase 4 on 5×`deepdive-fetcher` (Haiku 5.5) costs pennies against Opus (prices — NOTES.md). The rule is architectural (narrow task = cheap model, do not skimp on Phase 1/6), not about price.

(Check the current prices.)

---

## How to pass the model into the `Agent` tool

The deepdive agents take the model and effort from their frontmatter, the call names only the type:

```
Agent({
  subagent_type: "deepdive-fetcher",   // haiku / medium from the frontmatter; fetch+save needs Write
  description: "...",
  prompt: "..."
})
```

For a built-in type the model and effort are passed explicitly (an example — fetch escalation after a Haiku refusal or failure):

```
Agent({
  subagent_type: "general-purpose",
  model: "sonnet",
  effort: "high",
  description: "...",
  prompt: "... format and rules — read ~/.claude/agents/deepdive-fetcher.md ..."
})
```

A built-in type without `model` inherits the main model (currently Opus 5.5); a forgotten `model` parameter = an expensive call.

---

## How to tell the user

At the start of a medium/deep research, after Phase 3 (the plan is ready), once:

```
Starting a medium research. Routing:
- Phase 1, 3, 6 (synthesis): main (Opus)
- Phase 6 red team: deepdive-redteam (Opus/high)
- Phase 4: 4 deepdive-fetcher (Haiku/medium)
- Phase 3.5, 5, 5.5, 6.5: explore-haiku

Estimated cost: ~$2 (vs ~$8 if everything were on Opus)
```

This is not marketing — it is **transparency**, the user must be able to say «no, I need quality, run everything on Opus».

---

## Override mechanics

The user can explicitly override:

```
> deepdive X with all on opus
```

Then the router is ignored and **all** phases and sub-agents run on Opus. The price is higher; for high-stakes decisions it is OK.

Likewise:
- `... with cheap mode` → everything on Haiku where possible, Sonnet only on Phase 1/6
- `... with default routing` (or nothing) → the matrix above

---

## Anti-patterns

**❌ Running Phase 6 adversarial on Haiku.** Adversarial is critical thinking. Haiku here will be a soft pushback without a real attack on the hypotheses. Only `sub: deepdive-redteam` (Opus/high).

**❌ Running 5 parallel sub-agents all on Opus.** That is multiplying the price by 5 with no justification. Sub-agents with a narrow task — `deepdive-fetcher` (Haiku).

**❌ Raising the Phase 4.1 fetch agents to Opus «for quality».** It is not only about the price. A model's capability is orthogonal to its «prosociality» in a multi-agent configuration (Anthropic Frontier Red Team, 13.08.2026): a stronger model does not coordinate better — it does its own thing more confidently and faster. A fetch agent has `Write` and an isolated context, that is, the right to act without supervision; on a strong model what grows is not the quality of the search but the price of an error — a wrong interpretation of the subtopic chosen more confidently, a `root` set more confidently, a source discarded more confidently. The boundaries (the id range, the fixed dispatch, the mandatory fields) hold quality better than the model class.

**❌ Treating `xhigh`/`max` as a free improvement.** Higher effort — a longer trajectory and a greater tendency to overthink. On Phase 4 that is directly harmful: the agent needs to collect sources by the fixed strategy, not to reinvent it.

**❌ Not telling the user about the routing.** Transparency about the savings is a **feature**, not an easter egg. Say once at the start what the routing and the estimated cost are.

**❌ Ignoring the override.** If the user said «everything on Opus» — obey, do not «optimize behind their back».

**❌ Hardcoded routing «always one model everywhere».** That is losing Haiku's advantages on simple work and Opus's on the critical parts.
