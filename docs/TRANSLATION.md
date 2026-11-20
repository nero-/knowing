# TRANSLATION — glossary and coupling rules

Upstream prose is Russian, but **the gates read Russian too**. `scripts/validate_phases.py` and
`scripts/build_readout.py` match literal Cyrillic strings and regexes over report structure. So
translation is a *coupled* change: the prose, the pattern that reads it, and a test that proves the
pattern still fires must move together. Translating prose alone silently converts gates into no-ops
(a pattern that matches nothing is indistinguishable from a pattern that passed).

## Canonical glossary — the English side is a contract, not a preference

| Russian (upstream) | English (knowing) | where the literal is matched |
|---|---|---|
| `## Разбор` | `## Source dissection` | `validate_phases.py:602` (source card detection) |
| `гипотез` … `вердикт` (table header) | `Hypothesis` … `Verdict` | `VERDICT_TABLE_RE`, `validate_phases.py:446` |
| `Ответ` | `Answer` | `build_readout.py:148`, `ANSWER` section probe `:464` |
| `Делать` | `Do` | `build_readout.py:148` |
| `Не делать` | `Don't` | `build_readout.py:148` |
| `Что поменяет решение` | `What would change the decision` | `build_readout.py:148` |
| `Чего не знаем` | `What we don't know` | `build_readout.py:148` |
| `уверенность` | `confidence` | `build_readout.py:215` |
| `по умолчанию` / `берите` / `выбирайте` / `начинать стоит` / `начните с` / `рекомендуем` | `by default` / `take` / `choose` / `start with` / `begin with` / `we recommend` | `DEFAULT_RE`, `validate_phases.py:458` |
| `приоритет над текстом` / `заменяется на` / `поправки ниже` / `см. ремедиац` | `takes priority over the text` / `is replaced by` / `amendments below` / `see remediation` | `APPENDIX_RE`, `validate_phases.py:492` |
| `depth:` (plan_template) vs `mode:` (validator) | **`depth:` everywhere** | the mismatch is a bug we fix, see `docs/DECISIONS.md` D3 |

Rules for the translator:

1. **Never invent, never delete, never soften.** A command stays a command. If a sentence is unclear,
   translate it literally and add `<!-- translator: ambiguous -->` on the same line.
2. **Do not touch** fenced code, inline `code`, file paths, script names, flag names, YAML keys,
   table column orders, or `<!--gen:...-->` stamps.
3. **Section headings that are matched by a gate must use the glossary exactly**, including case and
   apostrophe style (`Don't`, not `Do not`).
4. **Keep the upstream file's structure**: same headings in the same order, same number of tables,
   same bullets. A translated file must diff cleanly against its source in structure even though the
   words differ.
5. **Add one header line** to every translated file:
   `<!-- translated from upstream/references/<path> @ e233797 — see docs/TRANSLATION.md -->`
6. The Russian originals stay in `upstream/` untouched, so any translation can be checked against
   its source by a reader who has both.

## What is translated in v0.1

The **floor**: the files in `context_budget.py::ALWAYS_LOAD` (what a run loads unconditionally), plus
`plan_template.md`. Everything else stays Russian in v0.1 and is listed in `docs/TRANSLATION.md`'s
backlog; the load profiles in `context_budget.py` are the authority on what a run actually pulls, so
the backlog is ordered by that list, not by file count.

## Known coupling regressions in v0.1

- Section locators inside translated files (e.g. «§ Routing for sub-agents», «§ Fourth condition»)
  now point at English headings that live in files still in Russian — `source_scoring.md`,
  `subagents_v2.md`, `adversarial_pass.md`. They will resolve once the backlog is done; until then a
  reader of those files must search by meaning, not by heading. This is the exact cost the reviews
  predicted ("56 references run out of translated files into untranslated ones"), recorded rather
  than hidden.

## How a translation is verified

- `overlay/tests/test_coupling.py` asserts that every pattern listed in the glossary above still
  matches the English fixture **and** still fails on a deliberately broken one. A translated gate
  without that test is not migrated, only reworded.
- `scripts/validate_phases.py` is run against the fixture run in `overlay/tests/fixtures/run_ok/`
  and must exit 0; against `run_bad/` and must exit non-zero with the expected gate names.
