#!/usr/bin/env python3
"""Apply knowing's patches to the vendored upstream tree, idempotently.

Why patches and not a sidecar script: the four reviews of the migration plan converged on the
same objection — a second gate that runs beside the validator re-creates the seam the whole
design exists to close ("the lint ran separately and the orchestrator reinterpreted its failures
as false positives"). So our checks either run *inside* the finish chain or they do not run.

Every patch asserts its anchor string is present. If upstream moves a line, this fails loudly
instead of silently applying nothing — the failure mode both reviewers flagged.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARK = "knowing-patch"


class PatchError(RuntimeError):
    pass


def _edit(rel: str, old: str, new: str, *, count: int = 1, marker: str = "") -> bool:
    """Replace `old` with `new` once. Returns True if applied, False if already applied."""
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    if marker and marker in text:
        return False
    if new in text:
        return False
    if old not in text:
        raise PatchError(f"{rel}: anchor not found — upstream changed, review the patch:\n{old[:160]}")
    p.write_text(text.replace(old, new, count), encoding="utf-8")
    return True


PATCHES = [
    # 1. The ledger gains a locator and a quote hash. Header is an allowlist, so a new column is
    #    rejected outright until it is declared here (verified: score_claims.load exits rc=1).
    (
        "scripts/validate_phases.py",
        'CLAIMS_OPTIONAL = ("claim_class", "evidence_kind", "plain", "detail")',
        'CLAIMS_OPTIONAL = ("claim_class", "evidence_kind", "plain", "detail",  # knowing-patch\n'
        '                   "anchor", "quote_sha256")  # knowing: locator + quote hash, see overlay/',
        "knowing-patch",
    ),
    # 2. Depth is read from `depth:` (the key the plan template actually writes) and `mode:` is
    #    still honoured as a legacy alias. Upstream read only `mode:`, so a plan declaring
    #    `depth: deep` validated as shallow and skipped every breadth floor.
    (
        "scripts/validate_phases.py",
        'MODE_RE = re.compile(r"^mode:\\s*(\\w+)", re.MULTILINE)',
        'MODE_RE = re.compile(r"^(?:depth|mode):\\s*(\\w+)", re.MULTILINE)  # knowing: depth is canonical',
        None,
    ),
    # 3. A missing declaration fails closed. Upstream warned and inferred 'shallow', which is the
    #    one inference that turns the non-waivable breadth floors off.
    (
        "scripts/validate_phases.py",
        """    mode, why = infer_mode(d)
    r.warn(
        f"no 'mode:' frontmatter in report or plan.md — inferred '{mode}' ({why}); "
        f"add `mode: {mode}` to plan.md or pass --mode"
    )
    return mode""",
        """    mode, why = infer_mode(d)
    # knowing: refusing the inference. Inferring 'shallow' silently disabled MIN_READ,
    # MIN_CANDIDATES, all TYPE_QUOTAS and MIN_CONTRADICTING (validate_phases:562-563).
    r.err(
        f"no `depth:` in report frontmatter or plan.md (would have inferred '{mode}' — {why}); "
        f"declare `depth: shallow|medium|deep` in plan.md, or pass --mode"
    )
    return mode""",
        None,
    ),
    # 4. sources.csv carries read scope, so a claim cannot rest on an abstract unnoticed.
    (
        "scripts/build_sources_csv.py",
        '    "discovery_path",\n]',
        '    "discovery_path",\n    "read_scope",  # knowing: full_text | sections | abstract_only\n]',
        None,
    ),
    # 5. Citation liveness becomes capable of failing. Upstream ran it at every depth without
    #    --strict, so a dead link never turned the run red in any mode.
    (
        "scripts/finish.py",
        'lambda d, m, w: ["--json", "--out", str(d / ".verify" / "citations")],',
        'lambda d, m, w: ["--json", "--out", str(d / ".verify" / "citations"), "--strict"],  # knowing',
        None,
    ),
    # 6. knowing's own checks join the finish chain, last, in the same process.
    (
        "scripts/finish.py",
        '    Step("phase_gate", REPO / "scripts/validate_phases.py", lambda d, m, w: ["--strict", *_mode(m)]),\n]',
        '    Step("phase_gate", REPO / "scripts/validate_phases.py", lambda d, m, w: ["--strict", *_mode(m)]),\n'
        '    Step("knowing", REPO / "overlay" / "knowing_gate.py", lambda d, m, w: ["--strict"]),  # knowing\n]',
        'Step("knowing"',
    ),
    # 8. The gate-matched literals accept English. Translated prose says `## Source dissection`
    #    and `| Hypothesis | Verdict |`; the Russian forms stay accepted so runs carried over from
    #    upstream still validate. Bilingual beats migration.
    (
        "scripts/validate_phases.py",
        '    no_card = [p.name for p in files if "\\n## Разбор" not in p.read_text(encoding="utf-8")]',
        '    # knowing: English and Russian headings both count\n'
        '    CARD_RE = re.compile(r"\\n##\\s+(?:Разбор|Source dissection)\\b")\n'
        '    no_card = [p.name for p in files if not CARD_RE.search(p.read_text(encoding="utf-8"))]',
        "CARD_RE = re.compile",
    ),
    (
        "scripts/validate_phases.py",
        'VERDICT_TABLE_RE = re.compile(r"^\\|[^\\n]*гипотез[^\\n]*\\|[^\\n]*вердикт", re.IGNORECASE | re.MULTILINE)',
        'VERDICT_TABLE_RE = re.compile(  # knowing: bilingual\n'
        '    r"^\\|[^\\n]*(?:гипотез|hypothes)[^\\n]*\\|[^\\n]*(?:вердикт|verdict)",\n'
        '    re.IGNORECASE | re.MULTILINE)',
        "knowing: bilingual",
    ),
    (
        "scripts/validate_phases.py",
        'DEFAULT_RE = re.compile(r"(?<![«\\w])(по умолчанию|берите|выбирайте|начинать стоит|начните с|рекомендуем)(?![»\\w])",',
        'DEFAULT_RE = re.compile(  # knowing: bilingual defaults\n'
        '    r"(?<![«\\w])(по умолчанию|берите|выбирайте|начинать стоит|начните с|рекомендуем"\n'
        '    r"|by default|take|choose|start with|begin with|we recommend)(?![»\\w])",',
        "knowing: bilingual defaults",
    ),
    (
        "scripts/validate_phases.py",
        'APPENDIX_RE = re.compile(r"приоритет над текстом|заменяется на|поправки ниже|см\\. ремедиац", re.IGNORECASE)',
        'APPENDIX_RE = re.compile(  # knowing: bilingual appendix\n'
        '    r"приоритет над текстом|заменяется на|поправки ниже|см\\. ремедиац"\n'
        '    r"|takes priority over the text|is replaced by|amendments below|see remediation",\n'
        '    re.IGNORECASE)',
        "knowing: bilingual appendix",
    ),
    # 9. The readout exporter accepts English section names while still emitting Russian for
    #    existing runs. Its output is an artefact, not a gate, so this is a soft landing.
    (
        "scripts/build_readout.py",
        '    for need in FRAME + GENRES[genre]:\n        if not any(n.startswith(need.lower()) for n in names):\n            problems.append(f"{genre}: нет раздела «{need}»")',
        '    EN = {  # knowing: English headings a translated run produces\n'
        '        "ответ": "answer", "делать": "do", "не делать": "don\'t",\n'
        '        "что поменяет решение": "what would change the decision",\n'
        '        "чего не знаем": "what we don\'t know", "варианты": "options",\n'
        '        "что говорит против": "what argues against", "карта": "map",\n'
        '        "где пусто": "where it is empty", "доводы за": "arguments for",\n'
        '        "доводы против": "arguments against", "как устроено": "how it works",\n'
        '        "вопросы": "questions", "находки": "findings",\n'
        '        "что изменило бы вердикт": "what would change the verdict",\n'
        '    }\n'
        '    for need in FRAME + GENRES[genre]:\n'
        '        alt = EN.get(need.lower(), "")\n'
        '        if not any(n.startswith(need.lower()) or (alt and n.startswith(alt)) for n in names):\n'
        '            problems.append(f"{genre}: нет раздела «{need}»")',
        "knowing: English headings",
    ),
    (
        "scripts/build_readout.py",
        '    if answer and not re.search(r"уверенность", answer, re.I):',
        '    if answer and not re.search(r"уверенность|confidence", answer, re.I):  # knowing: bilingual',
        "knowing: bilingual",
    ),
    # 7b. build_provider learns the tier-mapped backend, so per-tier endpoints are a config
    #     choice rather than a fork of runner/providers.py.
    (
        "runner/providers.py",
        '    if name == "dryrun":\n        return DryRunProvider()',
        '    if name in ("models", "tiers"):  # knowing: name -> endpoint pool, see overlay/model_map.py\n'
        '        import sys as _sys\n'
        '        from pathlib import Path as _Path\n'
        '        _sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "overlay"))\n'
        '        import config as _cfg, model_map as _mm\n'
        '        return _mm.ModelMap(_cfg.load())\n'
        '    if name == "dryrun":\n        return DryRunProvider()',
        None,
    ),
    # 10/11. State lives in ~/.knowing, not in another harness's directory.
    (
        "runner/wiki.py",
        'DEFAULT_ROOT = Path.home() / ".claude"',
        'DEFAULT_ROOT = Path.home() / ".knowing"  # knowing: own state directory',
        None,
    ),
    (
        "runner/state.py",
        'DEFAULT_ROOT = Path.home() / ".claude"',
        'DEFAULT_ROOT = Path.home() / ".knowing"  # knowing: own state directory',
        None,
    ),
    (
        "runner/wiki.py",
        "Storage lives under ~/.claude/research/wiki/ — global on purpose. Research folders land",
        "Storage lives under ~/.knowing/research/wiki/ — global on purpose. Research folders land",
        "~/.knowing/research/wiki/",
    ),
    # 12. help strings that named the old directory
    (
        "scripts/finish.py",
        'help="override ~/.claude (tests)"',
        'help="override ~/.knowing (tests)"',
        'override ~/.knowing',
    ),
    # 7. check_quotes.py returns 0 unconditionally — it reports, it cannot fail a run.
    (
        "eval/check_quotes.py",
        """    for r in res["quotes"]:
        if r["status"] != "ok":
            print(f"  {r['status']:12} {'/'.join(r['cites'])}  «{r['quote'][:90]}»")
    return 0""",
        """    for r in res["quotes"]:
        if r["status"] != "ok":
            print(f"  {r['status']:12} {'/'.join(r['cites'])}  «{r['quote'][:90]}»")
    # knowing: this used to return 0 always, so a quote that appears in no source was a report
    # nobody read. A missing or mis-attributed quote now fails the checker.
    bad = (res.get("missing") or 0) + (res.get("wrong_source") or 0)
    return 1 if bad else 0""",
        None,
    ),
]


def main() -> int:
    applied = changed = 0
    for rel, old, new, marker in PATCHES:
        try:
            if _edit(rel, old, new, marker=marker or ""):
                applied += 1
                print(f"applied   {rel}: {old.strip().splitlines()[0][:70]}")
            else:
                print(f"present   {rel}: {new.strip().splitlines()[0][:70]}")
            changed += 1
        except PatchError as exc:
            print(f"FAILED    {exc}")
            return 1
    print(f"knowing: {applied} patch(es) applied, {changed - applied} already present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
