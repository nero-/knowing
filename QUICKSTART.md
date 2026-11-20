# Quickstart

One documented research run, local models only, in about ten minutes of setup and then however long
the question deserves.

## 1. Put the skill where your agent looks

```bash
git clone https://github.com/nero-/knowing ~/Agent/knowing
cd ~/Agent/knowing
python3 overlay/apply_patches.py               # required: the checks live inside upstream's finish chain
python3 -m pip install --user pyyaml requests
ln -s ~/Agent/knowing ~/.agents/skills/knowing
```

A skill is a folder of instructions and scripts your agent reads — not a binary, and not something you
run by hand. Once it is installed, you ask for research in normal language and the agent drives the
phases, running the scripts as it goes.

Remove or archive any older research skill first: two skills claiming the same job compete for the same
request.

## 2. Point it at your models

```bash
python3 overlay/config.py from-pi ~/.pi/agent/models.json > ~/.config/knowing/models.toml
```

Then edit it. Local endpoints only — anything speaking `/v1` works (vLLM, llama.cpp, Ollama, LM Studio):

```toml
default = "small"

[providers.big-box]
base_url = "http://100.120.4.113:8015/v1"

[providers.small-box]
base_url = "http://100.97.112.71:8000/v1"

[models.big]
endpoints = ["big-box/DeepSeek-V4.1-Flash"]
rotate = "sticky"
fallback = ["mid"]

[models.mid]
endpoints = ["big-box/DeepSeek-V4.1-Flash", "small-box/Qwen3.8-Flash-Next"]

[models.small]
endpoints = ["small-box/Qwen3.8-Flash-Next"]
```

Names are yours; `phases.yaml` references them, and `[phases."6"] model = "big"` can pin one.
`rotate = "sticky"` keeps one model for the whole process, which matters where the prompt cache does.

Verify before spending a run:

```bash
python3 overlay/config.py check --probe
```

## 3. Ask for research

"Research X, deep enough to decide Y" is enough. The skill writes `plan.md` first, and that file is a
gate: it declares the depth *and* the three facts that justify it.

```yaml
depth: medium
reversibility: irreversible
cost_of_error: high
answer_exists: no
```

Breadth floors are enforced and not waivable: medium means ≥60 candidates screened and ≥25 sources read,
deep means ≥100 and ≥35. If you want a fast answer, say so — a declaration of `shallow` is honest and
keeps citation liveness and quote hashing, but skips the red team.

## 4. Read the finish output, not the prose

The agent ends by running `scripts/finish.py`, whose last two steps are upstream's validator and the
overlay gate. If either is red, the run is not done, whatever the report says. The overlay rejects:

- a claim with no `anchor` (`source_id:line`) or a quote hash that does not match the card;
- a depth declaration missing a fact, or lower than its own facts imply;
- a `triangulated` claim resting only on `abstract_only` sources;
- no `adversarial.md`, no `VERDICT:` line, no `DECLINED TO JUDGE`, or `VERDICT: BLOCK`.

## 5. What you will have

```
research/<slug>/
  plan.md · candidates.csv · sources.csv · sources/<id>.md
  claims.csv          claim → sources → status → anchor → quote hash
  adversarial.md      VERDICT + declined-to-judge
  report.md           the deliverable
  .verify/            citation liveness, faithfulness contract
```

The point of the run is the ledger: every claim row carries a locator and the hash of the line it quotes,
so any sentence can be re-checked later without re-fetching anything.

Details, the model guide and the remaining gaps: `docs/USAGE.md`, `docs/MODELS.md`.
