"""Tests for generate_case and the command line."""
import json

import pytest

from suraag import pipeline
from suraag.render import stub_filler
from suraag.verify import verify
from suraag.parse import Artifacts


def stub_fn(case, errors):
    return stub_filler(case)


@pytest.mark.parametrize("lang", ["en", "hinglish"])
def test_generate_case_writes_every_file(tmp_path, lang):
    res = pipeline.generate_case(3, lang, "hybrid", tmp_path / "c", filler_fn=stub_fn)
    assert res.ok
    names = {p.name for p in (tmp_path / "c").iterdir()}
    assert names == {"chat.txt", "calls.csv", "photo.jpg", "manifest.json", "case.json", "brief.json", "brief.md",
                     "solution.md"}
    case = pipeline.Case.model_validate_json((tmp_path / "c" / "case.json").read_text("utf-8"))
    assert verify(case, Artifacts.from_dir(tmp_path / "c")) == []  # the files on disk verify, not just in memory


def test_student_brief_never_leaks_the_answer(tmp_path):
    pipeline.generate_case(3, "en", "hybrid", tmp_path, filler_fn=stub_fn)
    case = json.loads((tmp_path / "case.json").read_text("utf-8"))
    md = (tmp_path / "brief.md").read_text("utf-8")
    boss = next(p for p in case["people"] if p["role"] == "boss")
    assert "SYNTHETIC CASE" in md and "Answer: ____" in md and "Cite" in md and "not that they are authentic" in md
    assert "boss" not in md.lower() and '"answer"' not in (tmp_path / "brief.json").read_text("utf-8")
    assert boss["name"] in md  # the boss is one of the listed suspects, like everyone else


def test_planted_defect_is_repaired_through_the_pipeline(tmp_path):
    seen = []
    res = pipeline.generate_case(4, "hinglish", "hybrid", tmp_path, defect="timestamp_clash",
                                 filler_fn=stub_fn, on_attempt=seen.append)
    assert res.ok and len(seen) == 2 and seen[0].failures and not seen[1].failures


def test_cli_runs_offline_with_stub_filler(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("SURAAG_OFFLINE", "1")
    monkeypatch.setenv("SURAAG_LLM_CACHE", str(tmp_path / "cache"))
    out = tmp_path / "case"
    code = pipeline.main(["--seed", "5", "--lang", "hinglish", "--out", str(out), "--offline"])
    text = capsys.readouterr().out
    assert code == 0 and f"SEALED {out}" in text and (out / "manifest.json").exists()
    manifest = json.loads((out / "manifest.json").read_text("utf-8"))
    assert manifest["model"] == "stub"  # the LLM was unavailable, and the manifest says so honestly
