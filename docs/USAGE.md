# Using knowing

Two things to get right: where the skill lives, and what the run is allowed to claim. Everything else
is upstream's pipeline.

## 1. Install

```bash
git clone https://github.com/nero-/knowing ~/Agent/knowing
cd ~/Agent/knowing

python3 overlay/apply_patches.py          # applies 9 patches to the vendored upstream code
```

`apply_patches.py` is **not optional and not a one-off you can skip**: the checks live inside upstream's
finish chain, so without it the harness runs upstream's behaviour — including the bug where a plan
declaring `depth: deep` is validated as shallow and skips every breadth floor. It is idempotent and it
fails loudly if an upstream line moved.

Two Python dependencies, because upstream's fetcher and citation checker use them:

```bash
python3 -m pip install --user pyyaml requests     # or use a venv, see below
```

The Anthropic and OpenAI SDKs are only needed for the endpoints you actually configure
(`pip install anthropic`, `pip install openai`).

Link it where your agent looks for skills:

```bash
ln -s ~/Agent/knowing ~/.agents/skills/knowing
```

If the old hand-written research skill is still installed, **remove or archive it** — two skills that
both claim research will fight over the same request.

## 2. Configure models (once)

```bash
python3 overlay/config.py from-pi ~/.pi/agent/models.json > ~/.config/knowing/models.toml
```

That imports your existing providers (including `!command` keys). Then edit it into something
deliberate:

```toml
default = "small"                       # top-level keys go above the first table

[providers.sparks]                      # 1M-context box: planning, synthesis
base_url = "http://100.120.4.113:8015/v1"

[providers.sparks-tp2]                  # 262k box: fan-out
base_url = "http://100.97.112.71:8000/v1"

[providers.openrouter]                  # anything OpenAI-compatible
base_url = "https://openrouter.ai/api/v1"
api_key_cmd = "pass show openrouter/key"

[models.big]
endpoints = ["sparks/DeepSeek-V4.1-Flash", "openrouter/anthropic/claude-opus-5"]
rotate = "sticky"                       # one model per process: prompt cache survives
fallback = ["small"]

[models.small]
endpoints = ["sparks-tp2/Qwen3.8-Flash-Next", "sparks/DeepSeek-V4.1-Flash"]

[phases."6"]                            # optional: pin a phases.yaml phase
model = "big"
```

Verify before you spend a run:

```bash
python3 overlay/config.py check --probe
```

It prints each model, its endpoints, whether the credentials resolve, and `[200] serves N model(s)` for
each — warning you if a configured model id is not in the server's list. That is the typo that
otherwise costs you a full run.

You do not have to configure anything to try it: the skill works on whatever model your agent is
already running, and the config exists so the expensive phases can go somewhere with more context.

## 3. Start a run

Ask for it in the normal way — "research X, deep enough to decide Y" — and the skill drives the phases.
Two things the run writes before it searches, and both are gates:

**`plan.md`** declares depth *and* the three facts that justify it:

```yaml
depth: medium            # shallow | medium | deep
reversibility: irreversible   # reversible | irreversible
cost_of_error: high           # low | high
answer_exists: no             # yes | no
```

`irreversible` or `high` implies at least `medium`; `answer_exists: yes` with the other two clean allows
`shallow`. A declared depth **below** what the facts imply is an error, and omitting a fact is an error —
the harness will not infer a depth, because the only inference upstream made was "shallow", which
switched the breadth floors off.

**The breadth floors apply, and they are not waivable.** Medium means ≥60 candidates screened and ≥25
sources read; deep means ≥100 and ≥35. If you only want a quick answer, say so and declare `shallow`
honestly — shallow keeps citation liveness and quote hashing but skips the red team, and the run will
tell you that.

## 4. What the run leaves on disk

```
research/<slug>/
  plan.md                 depth + facts, sub-questions, hypotheses
  candidates.csv          what was considered (≥60 at medium)
  sources.csv             what was read, with read_scope and access
  sources/<id>.md         one card per source, with the quotes
  claims.csv              the ledger: claim → sources → status → anchor → quote hash
  findings/               red-team output
  adversarial.md          VERDICT: PASS | REVISE | BLOCK, and DECLINED TO JUDGE
  state.md, readout.md    run state and the human summary
  .verify/                citations, faithfulness contract, authority
  report.md               the deliverable
```

The ledger is the point. Every claim row carries `anchor` (`source_id:line`) and `quote_sha256` — the
hash of the normalised quoted line in the card — so a quote can be re-found and re-checked without
re-fetching anything:

```
claim_id,sources,status,confidence,...,anchor,quote_sha256
c7,s03; s11,triangulated,high,...,s03:118,9f2c1b3d4e5f6071
```

## 5. Finish, and what the gates will say

```bash
python3 scripts/finish.py --research-dir research/<slug>
```

One command, eight steps: builds `sources.csv`, scores the ledger, checks citation liveness
(`--strict`), ingests the wiki, checks number provenance and arithmetic, then `validate_phases.py
--strict`, then `overlay/knowing_gate.py`. Red means a phase was skipped or a claim is unsupported —
fix it, do not re-run with flags removed.

Run the overlay alone when you want to know what it thinks:

```bash
python3 overlay/knowing_gate.py --research-dir research/<slug>            # errors block
python3 overlay/knowing_gate.py --research-dir research/<slug> --strict   # warnings block too
```

| check | fails when |
|---|---|
| `anchor` | a claim has no locator, points at a source it does not cite, or the hash does not match the card line |
| `depth` | a fact is missing or out of range, `depth:` is absent, or the declared depth is below what the facts imply |
| `read_scope` | a `triangulated` claim rests only on `abstract_only` sources; a cited source has no recorded scope |
| `adjudication` | at medium or deeper: no `adversarial.md`, no `VERDICT:` line, no `DECLINED TO JUDGE`, or `VERDICT: BLOCK` |

## 6. Cheat sheet

```bash
python3 overlay/config.py check --probe                 # endpoints, keys, what each serves
python3 overlay/config.py from-pi ~/.pi/agent/models.json > ~/.config/knowing/models.toml
python3 overlay/apply_patches.py                        # after every upstream rebase
python3 overlay/knowing_gate.py --research-dir <run>    # the four overlay checks
python3 scripts/finish.py --research-dir <run>          # the full chain
python3 scripts/validate_phases.py --research-dir <run> --strict
python3 scripts/context_budget.py --window 200000       # what a run loads, in tokens
python3 -m pytest overlay/tests -q                      # 61 tests
```

## 7. What is not finished

Be clear-eyed about this list; it is the difference between "usable" and "polished".

- **It has never run on a real research question end-to-end.** Everything is tested at unit level and
  the finish chain runs on synthetic fixtures, but the first real run is still ahead. Do it on a cheap
  question at `shallow`, then `medium`, and watch `finish.py`.
- **The report-block templates are still Russian** (`references/blocks/*.md`, ~18.8k words). They are
  read one at a time by the synthesis step, and the block ids are language-neutral, so synthesis works
  — it will just be reading Russian section templates.
- **The exporter's messages are Russian** (`build_report.py`), so its error output and `readout.md`
  section names come out in Russian for now. It accepts English headings on the way in.
- **`references/model_routing.md` still names Claude Code agent types** (`deepdive-fetcher`,
  `deepdive-redteam`). On pi these map to Agent types; the mapping is written down in
  `docs/DECISIONS.md` but not applied to the prose.
- **`runner/`** (the model-agnostic scripted path, `--provider models`) is available and tested but is
  not how the skill normally runs — the phases are driven by your agent, not by the runner.
