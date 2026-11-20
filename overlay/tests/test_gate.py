"""Tests for the knowing overlay gate.

Each test builds a throwaway run directory and asserts one specific promise. The negative
tests are the point: a gate that cannot fail is a comment.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import re
import sys
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "overlay"))

import knowing_gate as kg  # noqa: E402

PLAN_OK = textwrap.dedent(
    """\
    # Plan — test run

    depth: medium
    reversibility: irreversible
    cost_of_error: high
    answer_exists: no
    """
)
CLAIM_HEADER = [
    "claim_id", "claim", "hypothesis", "sources", "source_types", "roots", "paths",
    "status", "confidence", "primary_source", "source_caveat", "dissent", "as_of",
    "anchor", "quote_sha256",
]
CARD = """# s01 — Test source

Intro line.

> The measured effect was 12% with a confidence interval that excluded zero.

Footer.
"""
QUOTE_LINE = 5  # 1-based line of the blockquote above


def make_run(tmp_path: Path, *, depth="medium", status="triangulated", scope="full_text",
             verdict="REVISE", declined=True, claim_line=QUOTE_LINE,
             hash_override=None) -> Path:
    run = tmp_path / "run"
    (run / "sources").mkdir(parents=True)
    plan = PLAN_OK.replace("depth: medium", f"depth: {depth}")
    (run / "plan.md").write_text(plan, encoding="utf-8")
    (run / "sources" / "s01.md").write_text(CARD, encoding="utf-8")
    card_lines = CARD.splitlines()
    quoted = card_lines[claim_line - 1] if claim_line <= len(card_lines) else card_lines[QUOTE_LINE - 1]
    qh = hash_override if hash_override is not None else kg.quote_hash(quoted)
    with (run / "claims.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(CLAIM_HEADER)
        w.writerow(["c1", "the effect is 12%", "h1", "s01", "academic", "study-x", "academic",
                    status, "high", "s01", "", "", "2026-11-19",
                    f"s01:{claim_line}", qh])
    fields = ["id", "url", "title", "type", "channel", "access", "root", "used", "read_scope"]
    with (run / "sources.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(fields)
        w.writerow(["s01", "https://example.org", "Test", "paper", "academic", "OPEN",
                    "study-x", "yes", scope])
    if verdict is not None:
        body = f"# Adversarial review\n\nVERDICT: {verdict}\n"
        if declined:
            body += "\n## DECLINED TO JUDGE\n\n- nothing\n"
        (run / "adversarial.md").write_text(body, encoding="utf-8")
    return run


def kinds(problems, kind="error"):
    return [p for p in problems if p.kind == kind]


# ------------------------------------------------------------------------ anchor
def test_anchor_ok(tmp_path):
    run = make_run(tmp_path)
    assert kinds(kg.check_anchor(run)) == []


def test_anchor_hash_mismatch_fails(tmp_path):
    run = make_run(tmp_path, hash_override="0" * 16)
    errs = kinds(kg.check_anchor(run))
    assert errs and "hash mismatch" in errs[0].message


def test_anchor_points_at_other_source_fails(tmp_path):
    run = make_run(tmp_path)
    text = (run / "claims.csv").read_text().replace("s01:5", "s02:5")
    (run / "claims.csv").write_text(text)
    errs = kinds(kg.check_anchor(run))
    assert any("not in the row's sources" in e.message for e in errs)


def test_anchor_missing_column_fails(tmp_path):
    run = make_run(tmp_path)
    text = (run / "claims.csv").read_text().replace(",anchor,quote_sha256", "")
    (run / "claims.csv").write_text(text)
    errs = kinds(kg.check_anchor(run))
    assert any("apply_patches" in e.message for e in errs)


def test_anchor_line_out_of_range_fails(tmp_path):
    run = make_run(tmp_path, claim_line=999)
    errs = kinds(kg.check_anchor(run))
    assert any("outside" in e.message for e in errs)


# ------------------------------------------------------------------------- depth
def test_depth_ok(tmp_path):
    run = make_run(tmp_path)
    assert kinds(kg.check_depth(run)) == []


def test_depth_missing_fails_closed(tmp_path):
    """Regression: upstream warned and inferred 'shallow', which disabled the breadth floors."""
    run = make_run(tmp_path)
    plan = (run / "plan.md").read_text().replace("depth: medium\n", "")
    (run / "plan.md").write_text(plan)
    errs = kinds(kg.check_depth(run))
    assert errs and "refusing to infer" in errs[0].message


def test_depth_below_derived_fails(tmp_path):
    run = make_run(tmp_path, depth="shallow")  # irreversible + high cost imply >= medium
    errs = kinds(kg.check_depth(run))
    assert any("below the depth its own facts imply" in e.message for e in errs)


def test_depth_missing_fact_fails(tmp_path):
    run = make_run(tmp_path)
    plan = (run / "plan.md").read_text().replace("cost_of_error: high\n", "")
    (run / "plan.md").write_text(plan)
    errs = kinds(kg.check_depth(run))
    assert any("cost_of_error" in e.message for e in errs)


def test_depth_legacy_mode_key_warns(tmp_path):
    run = make_run(tmp_path)
    plan = (run / "plan.md").read_text() + "mode: medium\n"
    (run / "plan.md").write_text(plan)
    assert kinds(kg.check_depth(run), "warning")


# -------------------------------------------------------------------- read scope
def test_read_scope_ok(tmp_path):
    run = make_run(tmp_path)
    assert kinds(kg.check_read_scope(run)) == []


def test_triangulated_on_abstract_only_fails(tmp_path):
    run = make_run(tmp_path, scope="abstract_only")
    errs = kinds(kg.check_read_scope(run))
    assert errs and "abstract-only" in errs[0].message


def test_sections_is_deep_enough(tmp_path):
    run = make_run(tmp_path, scope="sections")
    assert kinds(kg.check_read_scope(run)) == []


def test_read_scope_missing_column_fails(tmp_path):
    run = make_run(tmp_path)
    text = (run / "sources.csv").read_text().replace(",read_scope", "")
    (run / "sources.csv").write_text(text)
    errs = kinds(kg.check_read_scope(run))
    assert any("apply_patches" in e.message for e in errs)


# ------------------------------------------------------------------ adjudication
def test_adjudication_ok(tmp_path):
    run = make_run(tmp_path)
    assert kinds(kg.check_adjudication(run)) == []


def test_adjudication_block_fails(tmp_path):
    run = make_run(tmp_path, verdict="BLOCK")
    errs = kinds(kg.check_adjudication(run))
    assert any("may not ship" in e.message for e in errs)


def test_adjudication_missing_declined_list_fails(tmp_path):
    run = make_run(tmp_path, declined=False)
    errs = kinds(kg.check_adjudication(run))
    assert any("DECLINED" in e.message for e in errs)


def test_adjudication_not_required_at_shallow(tmp_path):
    run = make_run(tmp_path, depth="shallow", verdict=None)
    plan = (run / "plan.md").read_text().replace("reversibility: irreversible",
                                                 "reversibility: reversible")
    plan = plan.replace("cost_of_error: high", "cost_of_error: low")
    (run / "plan.md").write_text(plan)
    assert kinds(kg.check_adjudication(run)) == []


# ----------------------------------------------------------------------- the gate
def test_gate_exit_codes(tmp_path):
    ok = make_run(tmp_path / "a")
    assert kg.main(["--research-dir", str(ok)]) == 0
    bad = make_run(tmp_path / "b", verdict="BLOCK")
    assert kg.main(["--research-dir", str(bad)]) == 1


# --------------------------------------------------------------------- coupling
def test_normalize_parity_with_upstream():
    """Our normaliser must stay identical to the one the base uses for quote comparison."""
    spec = importlib.util.spec_from_file_location("cq", ROOT / "eval" / "check_quotes.py")
    cq = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cq)
    for s in ["«The Effect» was 12%.", "  spaced   text ", "Ёжик, 12,3%", "> quoted _emph_ line"]:
        assert cq.normalize(s) == kg.normalize(s), s


def test_mode_regex_reads_depth_after_patch():
    """Regression: the plan template writes `depth:`, the validator read `mode:`."""
    spec = importlib.util.spec_from_file_location("vp", ROOT / "scripts" / "validate_phases.py")
    vp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vp)
    assert vp.MODE_RE.search("depth: deep").group(1) == "deep"
    assert vp.MODE_RE.search("mode: shallow").group(1) == "shallow"
