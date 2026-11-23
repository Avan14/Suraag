"""Tests for the verify/repair loop, sealing and the failure log."""
import hashlib
import json

from suraag.model import Case
from suraag.render import stub_filler
from suraag.repair import GenMeta, run
from tests.helpers import FIXTURE, load_case

CASE = load_case()
META = GenMeta(seed=1, model="stub", prompt_hashes={"filler": "abc"}, mode="hybrid", lang="hinglish")


def stub_fn(case, errors):
    return stub_filler(case)


def go(tmp_path, **kw):
    kw.setdefault("filler_fn", stub_fn)
    return run(CASE, meta=META, out_dir=tmp_path / "out", log_path=tmp_path / "failures.jsonl", **kw)


def test_clean_case_seals_with_matching_hashes(tmp_path):
    res = go(tmp_path)
    assert res.ok and len(res.attempts) == 1 and res.attempts[0].action == "initial"
    manifest = json.loads((tmp_path / "out" / "manifest.json").read_text("utf-8"))
    for name, digest in manifest["files"].items():
        assert hashlib.sha256((tmp_path / "out" / name).read_bytes()).hexdigest() == digest
    assert set(manifest["files"]) == {"chat.txt", "calls.csv", "photo.jpg"}
    assert manifest["seed"] == 1 and manifest["model"] == "stub" and manifest["prompt_hashes"] == {"filler": "abc"}


def test_chat_clash_is_flagged_then_repaired_by_regenerating_the_chat(tmp_path):
    res = go(tmp_path, defect="timestamp_clash", defect_target="chat")
    assert res.ok and len(res.attempts) == 2
    assert "cross_time" in [f.code for f in res.attempts[0].failures]
    assert res.attempts[1].failures == [] and "regenerate chat (LLM)" in res.attempts[1].action


def test_calls_clash_is_repaired_by_rerendering_calls_only(tmp_path):
    res = go(tmp_path, defect="timestamp_clash", defect_target="calls")
    assert res.ok and res.attempts[1].action == "re-render calls"


def test_unsolvable_question_is_repaired(tmp_path):
    res = go(tmp_path, defect="unsolvable_question")
    assert res.ok and "solver_mismatch" in [f.code for f in res.attempts[0].failures]


def test_unrepairable_filler_is_discarded_logged_and_writes_no_files(tmp_path):
    res = go(tmp_path, filler_fn=lambda c, e: [])
    assert not res.ok and len(res.attempts) == 4  # the first try plus 3 repairs
    lines = (tmp_path / "failures.jsonl").read_text("utf-8").splitlines()
    assert len(lines) == 1
    entry = json.loads(lines[0])
    assert entry["checks"] == ["filler_count"] and entry["codes"] == ["filler_short"]
    assert entry["tries"] == 4 and entry["case_id"] == "upi-ring-001"
    assert not (tmp_path / "out").exists()


def test_a_model_level_failure_cannot_be_repaired(tmp_path):
    d = json.loads(FIXTURE.read_text("utf-8"))
    d["facts"][0]["anchors"] = []
    res = run(Case.model_validate(d), filler_fn=stub_fn, meta=META, out_dir=tmp_path / "out",
              log_path=tmp_path / "failures.jsonl")
    assert not res.ok and len(res.attempts) == 1
    assert "fact_no_anchor" in json.loads((tmp_path / "failures.jsonl").read_text("utf-8"))["codes"]


def test_on_attempt_is_called_once_per_attempt(tmp_path):
    seen = []
    res = go(tmp_path, defect="timestamp_clash", on_attempt=seen.append)
    assert [a.n for a in seen] == [1, 2] == [a.n for a in res.attempts]
