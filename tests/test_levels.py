"""Practice levels: every level verifies, each trap really misleads, multi-step answers need every step cited,
and the worked solution names real lines."""
import json
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from suraag.defects import EXPECTED, inject
from suraag.explain import solution_markdown, walkthrough
from suraag.grade import Citation, Claim, grade_claim
from suraag.i18n import render_expl
from suraag.levels import LEVELS, build_level_case
from suraag.model import Case
from suraag.parse import Artifacts, load_calls
from suraag.render import render_calls, render_chat, render_photo, stub_filler
from suraag.skeleton import build_case
from suraag.solver import UNSOLVABLE, shortcut_answers, solve
from suraag.verify import check_depth, verify

ROOT = Path(__file__).parent.parent


def make(case: Case) -> Artifacts:
    return Artifacts(render_chat(case, stub_filler(case)), render_calls(case), render_photo(case))


def role(case: Case, r: str):
    return next(p for p in case.people if p.role == r)


def test_level_1_is_the_unchanged_level_1_case():
    assert build_level_case(5, "en", 1) == build_case(5, "en")


@pytest.mark.parametrize("lang", ["en", "hinglish"])
@pytest.mark.parametrize("level", [2, 3, 4])
def test_every_level_verifies_and_the_solver_reproduces_the_key(level, lang):
    for seed in range(1, 16):
        case = build_level_case(seed, lang, level)
        arts = make(case)
        assert case.twists == list(LEVELS[level])
        assert verify(case, arts) == [], (seed, [f.message for f in verify(case, arts)])
        assert solve(arts, case.brief, lang) == {q.id: q.answer for q in case.questions}


@pytest.mark.parametrize("lang", ["en", "hinglish"])
def test_each_shortcut_lands_on_the_wrong_answer_it_was_built_for(lang):
    case = build_level_case(9, lang, 4)
    arts = make(case)
    short = shortcut_answers(arts, case.brief, lang)
    boss, distr, assoc = role(case, "boss"), role(case, "distractor"), role(case, "associate")
    order_t = next(e.t for e in case.timeline if e.kind == "instruction")
    code_t = next(e.t for e in case.timeline if e.kind == "code_definition")
    claimed = case.fact("F11").anchors[0].must_contain[1]
    assert short["unsaved_caller"] == ("Q1", distr.id) != ("Q1", boss.id)
    assert short["decoy"] == ("Q1", distr.id)
    assert short["code_word"] == ("Q2", code_t.isoformat()) and code_t != order_t
    assert short["alibi"] == ("Q3", next(p.id for p in case.places if p.name == claimed))
    qid, got = short["camera_clock"]
    assert qid == "Q4" and datetime.fromisoformat(got).replace(tzinfo=None) == \
        case.photo.t.replace(tzinfo=None) - timedelta(hours=5, minutes=30)
    assert assoc.id != boss.id


def test_names_never_decide_on_their_own():
    for level in (2, 3, 4):
        case = build_level_case(11, "hinglish", level)
        first = role(case, "boss").name.split()[0]
        assert sum(s.name.split()[0] == first for s in case.brief.suspects) == 2  # boss and namesake decoy
        if "unsaved_caller" in case.twists:  # "the unsaved number that is a suspect" is not unique either
            phones = {s.phone for s in case.brief.suspects}
            assert len({r.number for r in case.calls if not r.contact_name and r.number in phones}) >= 2


def test_a_trap_that_does_not_mislead_fails_the_depth_check():
    case = build_level_case(3, "en", 3)
    honest = case.model_copy(update={"photo": case.photo.model_copy(update={"offset": "+05:30"})})
    fails = check_depth(case, make(honest))
    assert [(f.code, f.params["twist"]) for f in fails] == [("trap_not_set", "camera_clock")]


def test_photo_time_without_the_cameras_zone_is_unsolvable():
    from suraag.solver import photo_time
    assert photo_time({"DateTimeOriginal": "2026:03:24 15:11:00", "OffsetTimeOriginal": "+00:00"}) == \
        "2026-03-24T20:41:00+05:30"
    assert photo_time({"DateTimeOriginal": "2026:03:24 15:11:00"}) == UNSOLVABLE


def test_a_multi_step_answer_needs_every_step_cited():
    case = build_level_case(4, "en", 3)  # Q1 rests on the code rule, the order and call, and the reply
    arts = make(case)
    line = lambda fid: next(a.line for a in case.fact(fid).anchors if a.artifact == "chat")  # noqa: E731
    row = next(a.row for a in case.fact("F1").anchors if a.artifact == "calls")
    boss = role(case, "boss").id
    some = (Citation("chat", line=line("F1")), Citation("calls", row=row))
    r = grade_claim(case, arts, Claim("Q1", boss, some))
    assert r.answer_correct and not r.citation_valid
    missing = [e for e in r.explanations if e.code == "cite_missing_step"]
    assert [e.params["support"] for e in missing] == [f"chat.txt:{line('F2')}", f"chat.txt:{line('F5')}"]
    assert all(render_expl(e, "hi") for e in missing)
    full = some + (Citation("chat", line=line("F2")), Citation("chat", line=line("F5")))
    assert grade_claim(case, arts, Claim("Q1", boss, full)).points == 2


def test_the_decoy_line_is_wrong_evidence():
    case = build_level_case(4, "en", 3)
    arts = make(case)
    decoy = next(a.line for a in case.fact("F10").anchors)
    r = grade_claim(case, arts, Claim("Q1", role(case, "boss").id, (Citation("chat", line=decoy),)))
    assert not r.citation_valid and any(m.label == "wrong" for m in r.marks)


@pytest.mark.parametrize("lang", ["en", "hi"])
def test_the_worked_solution_cites_real_lines_and_names_every_trap(lang):
    case = build_level_case(6, "en", 4)
    arts = make(case)
    walks = walkthrough(case, arts, lang)
    assert [w.question_id for w in walks] == ["Q1", "Q2", "Q3", "Q4"]
    assert sum(len(w.traps) for w in walks) == len(case.twists)
    text = " ".join(s for w in walks for s in w.steps)
    for f in case.facts:
        if f.id in {fid for q in case.questions for fid in q.answer_facts}:
            for a in f.anchors:
                loc = {"chat": f"chat.txt:{a.line}", "calls": f"calls.csv:{a.row}", "photo": f"photo.jpg:{a.exif_tag}"}
                assert loc[a.artifact] in text, (f.id, a)
    assert walks[0].answer == role(case, "boss").name


def test_level_1_solution_has_no_traps():
    case = build_level_case(2, "hinglish", 1)
    md = solution_markdown(case, make(case))
    assert "Trap" not in md and "## Q3." in md


@pytest.mark.parametrize("level", [2, 3, 4])
@pytest.mark.parametrize("kind,target", [("timestamp_clash", "chat"), ("timestamp_clash", "calls"),
                                         ("alias_conflict", "chat"), ("missing_anchor", "chat"),
                                         ("unsolvable_question", "calls")])
def test_planted_defects_are_caught_on_every_level(level, kind, target):
    case = build_level_case(8, "hinglish", level)
    codes = {f.code for f in verify(case, inject(case, make(case), kind, target=target))}
    assert EXPECTED[kind] in codes


def test_every_shipped_case_verifies_and_matches_its_hashes():
    dirs = sorted(p.parent for p in (ROOT / "cases").glob("*/manifest.json"))
    assert dirs
    for d in dirs:
        case = Case.model_validate_json((d / "case.json").read_text("utf-8"))
        arts = Artifacts.from_dir(d)
        assert verify(case, arts) == [], d.name
        assert arts.sha256() == json.loads((d / "manifest.json").read_text("utf-8"))["files"], d.name
        assert len(load_calls(arts.calls)) == len(case.calls)


def test_hints_never_leak_the_culprit_or_the_evidence_on_any_level():
    from suraag.hints import TIERS, base_hint
    from suraag.norm import norm
    for level in (2, 3, 4):
        case = build_level_case(10, "en", level)
        boss = role(case, "boss")
        secrets = [boss.name, *boss.aliases] + [m for f in case.facts for a in f.anchors for m in a.must_contain]
        for q in case.questions:
            for tier in range(1, TIERS + 1):
                h = norm(base_hint(case, q.id, tier))
                assert not [s for s in secrets if norm(s) in h], (level, q.id, tier)
