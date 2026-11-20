<!-- translated from upstream/references/model_routing.md @ e233797 — see docs/TRANSLATION.md; rewritten for knowing: no the model-specific executors, model names are config keys -->
# Model routing — which model takes which step

## Contents

- Principles
- Who decides
- Phase → model name
- Routing for sub-agents (Phase 4.1)
- Effort: what you control, and what you do not
- Cost economics
- How to override

**When this is used:** at the start of every phase you pick the model name and the effort for the work
at hand. Mechanical work (searching, reading, extracting, classifying) goes to a sub-agent on the
cheapest *configured* model that still does the job. Hard reasoning and structural decisions stay on
the main thread or on the `big` name.

**Why:** without explicit routing, a sub-agent inherits whatever the main thread runs, which is
expensive for bulk work (URL search, scoring, dedupe) and weak for the moments that matter (reframing,
the adversarial pass). Explicit naming makes the trade visible in the plan instead of hiding in a
default.

---

## Principles

1. **More expensive is not better.** A simple task on the largest model is wasted tokens. A hard task on
   a small one is a weak result, and you will pay for it twice when the phase has to be redone.
2. **Effort matters more than size.** On the same model, `high` and `low` effort give different results:
   a mid-size model at high effort often beats the largest one at low effort for a middle-difficulty
   step.
3. **Parallelism is a reason to go cheaper.** If Phase 4 launches five sub-agents, they must be on the
   cheap name, not the big one. Otherwise the price of the research multiplies by five, and most of the
   work is extraction.
4. **One name per process, where it matters.** A step that has to agree with the previous one belongs on
   the same model: switching models mid-run loses the prompt cache and can shift quality between two
   sections that must read as one report. `models.toml` expresses this with `rotate = "sticky"`.

## Who decides

Three layers, first one wins:

1. **You, per call.** Name a model from `models.toml` and it is honoured.
2. **`phases.yaml`**, which declares `model:` per phase. Those values *are* keys in `models.toml`.
3. **`default`** in `models.toml`, when neither says anything.

An unknown name is an error that lists the names you have — never a silent fallback. A typo must not
quietly reroute the synthesis phase.

## Phase → model name

The table lives in `phases.yaml` and is stamped into the phase list; this is the reasoning behind it,
not a second copy of it.

| what the phase does | name | why |
|---|---|---|
| reframing, the plan gate, synthesis, the adversarial pass | `big` | these decide the shape of the whole run; a weak reframing is expensive to discover later |
| search fan-out, per-source reading, scoring, dedupe | `small` | high volume, low reasoning; the output is checked by a script or by the ledger |
| verification, evidence filter, wiki reconcile | `mid` | needs judgement, but bounded and mechanical |

If your endpoints only give you two sizes, map `mid` to `big` or `small` and say which in `plan.md`.
Nothing breaks: the names are yours.

## Routing for sub-agents (Phase 4.1)

Every dispatched sub-agent gets an explicit name and effort. The default inherited from the main thread
is the expensive one, which is exactly wrong for search.

- Fetcher sub-agents (URL search, page reading, extraction): the cheap name, low or medium effort.
- Batches of reads (screening 60–100 candidates, dedupe, scoring): the cheap name; consider splitting
  into several calls rather than one large one.
- The synthesis sub-agent: the big name if the report is the deliverable; otherwise `mid`.
- The adversarial pass: the big name. It is the step whose job is to find what the rest missed, and it
  reads the assembled claims rather than raw pages.

## Effort: what you control, and what you do not

| lever | effect |
|---|---|
| `effort` in `phases.yaml` | sets the thinking level for that phase's main-thread work |
| an explicit name for a sub-agent | changes which endpoint the work runs on |
| splitting one large call into several small ones | usually cheaper than raising effort, and gives more salvageable output |

You cannot make a small model do a hard step well by raising its effort. If a phase keeps failing, the
answer is a different name, not more effort.

## Cost economics

Two costs, both real:

- **Tokens.** A run at medium screens 60–100 candidates and reads 25–30 sources. Sending the fan-out to
  the expensive name multiplies the bill for work whose output is a table.
- **Context.** The main thread's window is the scarcer resource. A fan-in of ten full reports is large
  whether or not it is cheap; that is what the fan-out width rule in `subagents_v2.md` is for.

The cheap lever nobody uses: **do less**. Fewer rounds, tighter queries, and a narrower question cost
less than any routing.

## How to override

- Per call: name a model. `model: big` on a step that `phases.yaml` puts on `mid`.
- For a whole run: pass a different name for the search phases, or set `default` in `models.toml`.
- For one phase, permanently: edit `model:` in `phases.yaml`, or pin it in `models.toml`:

```toml
[phases."6"]
model = "big"
```

The second is preferable: `phases.yaml` is upstream's file and will be rebased; `models.toml` is yours.

Whatever you choose, `ModelMap.routed` records which model and which endpoint actually served each
step, so a run that quietly degraded is visible afterwards rather than inferred.
