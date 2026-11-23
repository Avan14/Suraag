"""Tests for the rule-based solver."""
from suraag.model import Brief
from suraag.parse import Artifacts
from suraag.render import render_calls, render_chat, render_photo, stub_filler
from suraag.solver import UNSOLVABLE, haversine_m, solve
from tests.helpers import load_case

CASE = load_case()
BRIEF: Brief = CASE.brief


def make(case=CASE, chat=None, calls=None) -> Artifacts:
    return Artifacts(chat=chat or render_chat(case, stub_filler(case)), calls=calls or render_calls(case),
                     photo=render_photo(case))


def test_fixture_is_solved_from_the_artifacts_alone():
    assert solve(make(), BRIEF, "hinglish") == {
        "Q1": "P1", "Q2": "2026-03-04T21:14:00+05:30", "Q3": "PL2"}


def test_contact_name_matching_survives_case_spaces_and_zero_width():
    calls = render_calls(CASE).replace("Raju bhai", "Raju  BHAI​")
    assert solve(make(calls=calls), BRIEF, "hinglish")["Q1"] == "P1"


def test_blank_contact_name_makes_who_unsolvable():
    calls = render_calls(CASE).replace(",Raju bhai,", ",,")
    out = solve(make(calls=calls), BRIEF, "hinglish")
    assert out["Q1"] == UNSOLVABLE and out["Q2"] == "2026-03-04T21:14:00+05:30"


def test_two_instruction_lines_make_who_and_when_unsolvable():
    lines = render_chat(CASE, stub_filler(CASE)).split("\n")
    lines[4] = lines[4].split(": ")[0] + ": entry delete krdo"  # a second instruction at line 5
    out = solve(make(chat="\n".join(lines)), BRIEF, "hinglish")
    assert out["Q1"] == UNSOLVABLE and out["Q2"] == UNSOLVABLE


def test_photo_far_from_every_place_is_unsolvable():
    far = CASE.model_copy(update={"photo": CASE.photo.model_copy(update={"lat": CASE.photo.lat + 0.02})})
    assert solve(make(far), BRIEF, "hinglish")["Q3"] == UNSOLVABLE


def test_no_photo_is_unsolvable():
    arts = Artifacts(chat=render_chat(CASE, stub_filler(CASE)), calls=render_calls(CASE), photo=None)
    assert solve(arts, BRIEF, "hinglish")["Q3"] == UNSOLVABLE


def test_haversine_is_re_exported():
    assert 6000 < haversine_m(19.0726, 72.8845, 19.0178, 72.8478) < 7500
