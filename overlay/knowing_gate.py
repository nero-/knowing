#!/usr/bin/env python3
"""knowing overlay checks.

Every check here exists because "knowing" made a promise the base did not keep:

  anchor        a quote can be re-found (source id + line + hash), not just cited
  depth         the depth mode is a declared, derived, validated fact — not a word the
                model types into a key the validator never reads
  read_scope    a claim may not rest on an abstract when it claims triangulation
  adjudication  the adversarial pass ends in a verdict, and a BLOCK cannot ship

Each check returns a list of Problem(kind, where, message). Errors fail the run; warnings
do not. Nothing here trusts a self-report: every check re-reads the artefact.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# Kept byte-identical in behaviour to eval/check_quotes.py::normalize, which is the
# normaliser the base already uses for quote comparison. tests/test_normalize_parity.py
# fails if the two drift apart.
QUOTE_CHARS = "«»“”„\"'‘’`*_>"


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[«»“”„\"'‘’`*_>]", "", text)
    text = text.replace("ё", "е")
    return re.sub(r"\s+", " ", text).strip(" .,;:")


def quote_hash(text: str) -> str:
    return hashlib.sha256(normalize(text).encode("utf-8")).hexdigest()[:16]


@dataclass
class Problem:
    kind: str
    where: str
    message: str

    def __str__(self) -> str:
        return f"{self.kind:12} {self.where}: {self.message}"


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return [dict(r) for r in csv.DictReader(fh)]


# --------------------------------------------------------------------------- anchor
# Source ids are upstream's (`01_x`, `10_b`) or the plain `s01` style; the id is validated
# against the row's own sources, so the pattern stays format-agnostic.
ANCHOR_RE = re.compile(r"^(?P<sid>[^\s:]+):(?P<line>\d+)$")
HASH_RE = re.compile(r"^[0-9a-f]{16}$")


def check_anchor(run: Path) -> list[Problem]:
    """Every claim row must point at the line it quotes, and the hash must match it."""
    out: list[Problem] = []
    claims_p = run / "claims.csv"
    if not claims_p.is_file():
        return [Problem("error", "claims.csv", "missing — nothing to anchor")]
    rows = _rows(claims_p)
    if not rows:
        return [Problem("error", "claims.csv", "no rows")]
    if "anchor" not in rows[0] or "quote_sha256" not in rows[0]:
        return [Problem("error", "claims.csv",
                        "missing anchor/quote_sha256 columns — run overlay/apply_patches.py")]
    for row in rows:
        cid = (row.get("claim_id") or "?").strip()
        anchor = (row.get("anchor") or "").strip()
        want = (row.get("quote_sha256") or "").strip()
        if not anchor:
            out.append(Problem("error", f"claims.csv {cid}",
                               "no anchor — a claim without a quote locator cannot be re-checked"))
            continue
        m = ANCHOR_RE.match(anchor)
        if not m:
            out.append(Problem("error", f"claims.csv {cid}",
                               f"anchor {anchor!r} is not '<source id>:<line>'"))
            continue
        sid, line_s = m.group("sid"), int(m.group("line"))
        if sid not in {s.strip() for s in (row.get("sources") or "").split(",")}:
            out.append(Problem("error", f"claims.csv {cid}",
                               f"anchor points at {sid}, which is not in the row's sources"))
        card = run / "sources" / f"{sid}.md"
        if not card.is_file():
            out.append(Problem("error", f"claims.csv {cid}", f"no source card {card.name}"))
            continue
        lines = card.read_text(encoding="utf-8", errors="replace").splitlines()
        if not 1 <= line_s <= len(lines):
            out.append(Problem("error", f"claims.csv {cid}",
                               f"anchor line {line_s} outside {card.name} ({len(lines)} lines)"))
            continue
        got = quote_hash(lines[line_s - 1])
        if not HASH_RE.match(want):
            out.append(Problem("error", f"claims.csv {cid}",
                               f"quote_sha256 {want!r} is not 16 lowercase hex chars"))
        elif got != want:
            out.append(Problem("error", f"claims.csv {cid}",
                               f"hash mismatch at {anchor}: card line {quote_hash(want and lines[line_s-1])} "
                               f"!= recorded {want} (card edited or anchor drifted)"))
    return out


# ---------------------------------------------------------------------------- depth
DEPTHS = ("shallow", "medium", "deep")
FACTS = {
    "reversibility": {"reversible", "irreversible"},
    "cost_of_error": {"low", "high"},
    "answer_exists": {"yes", "no"},
}
FACT_RE = {k: re.compile(rf"^{k}:\s*(\w+)\s*$", re.MULTILINE) for k in FACTS}


def derive_depth(plan_text: str) -> tuple[str | None, list[Problem]]:
    """Minimum depth implied by the three facts. Missing fact = error, not a guess."""
    out: list[Problem] = []
    facts: dict[str, str] = {}
    for key, pattern in FACT_RE.items():
        m = pattern.search(plan_text)
        if not m:
            out.append(Problem("error", "plan.md", f"missing `{key}:` (one of {sorted(FACTS[key])})"))
            continue
        val = m.group(1).lower()
        if val not in FACTS[key]:
            out.append(Problem("error", "plan.md", f"`{key}: {val}` not in {sorted(FACTS[key])}"))
            continue
        facts[key] = val
    if out:
        return None, out
    if facts["reversibility"] == "irreversible" or facts["cost_of_error"] == "high":
        return "medium", out
    if facts["answer_exists"] == "yes":
        return "shallow", out
    return "medium", out


def check_depth(run: Path) -> list[Problem]:
    out: list[Problem] = []
    plan = run / "plan.md"
    if not plan.is_file():
        return [Problem("error", "plan.md", "missing")]
    text = plan.read_text(encoding="utf-8", errors="replace")
    if re.search(r"^mode:\s*\w+", text, re.MULTILINE):
        out.append(Problem("warning", "plan.md",
                           "`mode:` is the legacy key; `depth:` is canonical in knowing"))
    declared_hits = re.findall(r"^depth:\s*(\w+)", text, re.MULTILINE | re.IGNORECASE)
    if not declared_hits:
        out.append(Problem("error", "plan.md",
                           "no `depth:` — refusing to infer a mode (upstream inferred 'shallow' "
                           "and skipped the breadth floors; this check fails closed instead)"))
        return out
    declared = declared_hits[0].lower()
    if declared not in DEPTHS:
        out.append(Problem("error", "plan.md", f"depth {declared!r} not in {list(DEPTHS)}"))
        return out
    derived, problems = derive_depth(text)
    out.extend(problems)
    if derived and DEPTHS.index(declared) < DEPTHS.index(derived):
        out.append(Problem("error", "plan.md",
                           f"depth {declared!r} is below the depth its own facts imply ({derived})"))
    return out


# ------------------------------------------------------------------------ read scope
SCOPES = ("full_text", "sections", "abstract_only")
DEEP_SCOPES = ("full_text", "sections")
TRIANGULATED = ("triangulated",)


def check_read_scope(run: Path) -> list[Problem]:
    out: list[Problem] = []
    src_p, claims_p = run / "sources.csv", run / "claims.csv"
    if not src_p.is_file():
        return [Problem("error", "sources.csv", "missing")]
    sources = _rows(src_p)
    if sources and "read_scope" not in sources[0]:
        out.append(Problem("error", "sources.csv",
                           "missing read_scope column — run overlay/apply_patches.py"))
        return out
    scope_of: dict[str, str] = {}
    unknown: list[str] = []
    for row in sources:
        sid, scope = (row.get("id") or "").strip(), (row.get("read_scope") or "").strip()
        if not sid:
            continue
        if scope not in SCOPES:
            # Scope is only load-bearing when a claim leans on it. An unused candidate with no
            # scope is noise; a cited one is the failure this check exists for.
            scope_of[sid] = "unknown"
            unknown.append(sid)
            continue
        scope_of[sid] = scope
    if unknown:
        out.append(Problem("warning", "sources.csv",
                           f"{len(unknown)} source(s) have no valid read_scope "
                           f"({', '.join(unknown[:5])}{'…' if len(unknown) > 5 else ''})"))
    if not claims_p.is_file():
        return out
    for row in _rows(claims_p):
        cid = (row.get("claim_id") or "?").strip()
        status = (row.get("status") or "").strip().lower()
        cited = [s.strip() for s in (row.get("sources") or "").split(",") if s.strip()]
        unscoped = [s for s in cited if scope_of.get(s) == "unknown"]
        if unscoped:
            out.append(Problem("error", f"claims.csv {cid}",
                               f"cites {', '.join(unscoped)} with no recorded read_scope "
                               f"— record what was read before leaning on it"))
        if status not in TRIANGULATED:
            continue
        thin = [s for s in cited if scope_of.get(s) == "abstract_only"]
        if thin and not any(scope_of.get(s) in DEEP_SCOPES for s in cited):
            out.append(Problem("error", f"claims.csv {cid}",
                               f"triangulated but every source is abstract-only ({', '.join(thin)})"))
    return out


# --------------------------------------------------------------------- adjudication
VERDICT_RE = re.compile(r"^VERDICT:\s*(PASS|REVISE|BLOCK)\s*$", re.MULTILINE)
DECLINED_RE = re.compile(r"^#+\s*DECLINED TO JUDGE", re.MULTILINE | re.IGNORECASE)


def check_adjudication(run: Path) -> list[Problem]:
    out: list[Problem] = []
    depth = "medium"
    plan = run / "plan.md"
    if plan.is_file():
        m = re.search(r"^depth:\s*(\w+)", plan.read_text(encoding="utf-8", errors="replace"),
                      re.MULTILINE | re.IGNORECASE)
        if m:
            depth = m.group(1).lower()
    if depth == "shallow":
        return out
    adj = run / "adversarial.md"
    if not adj.is_file():
        return [Problem("error", "adversarial.md", f"missing — required at depth {depth}")]
    text = adj.read_text(encoding="utf-8", errors="replace")
    m = VERDICT_RE.search(text)
    if not m:
        out.append(Problem("error", "adversarial.md", "no `VERDICT: PASS|REVISE|BLOCK` line"))
    elif m.group(1) == "BLOCK":
        out.append(Problem("error", "adversarial.md", "VERDICT: BLOCK — a blocked run may not ship"))
    if not DECLINED_RE.search(text):
        out.append(Problem("error", "adversarial.md",
                           "no `## DECLINED TO JUDGE` section — name what you could not check"))
    return out


# ----------------------------------------------------------------------------- gate
CHECKS = {
    "anchor": check_anchor,
    "depth": check_depth,
    "read_scope": check_read_scope,
    "adjudication": check_adjudication,
}


def run_all(run: Path, only: list[str] | None = None) -> list[Problem]:
    out: list[Problem] = []
    for name, fn in CHECKS.items():
        if only and name not in only:
            continue
        out.extend(fn(run))
    return out


def main(argv: list[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description="knowing overlay gate")
    ap.add_argument("--research-dir", required=True, type=Path)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="warnings count as failures")
    ap.add_argument("--only", nargs="*", choices=sorted(CHECKS))
    args = ap.parse_args(argv)

    problems = run_all(args.research_dir, args.only)
    errors = [p for p in problems if p.kind == "error"]
    warns = [p for p in problems if p.kind == "warning"]
    if args.json:
        print(json.dumps([p.__dict__ for p in problems], ensure_ascii=False, indent=2))
    else:
        for p in problems[:40]:
            print(p)
        print(f"knowing: {len(errors)} error(s), {len(warns)} warning(s)")
    return 1 if errors or (args.strict and warns) else 0


if __name__ == "__main__":
    sys.exit(main())
