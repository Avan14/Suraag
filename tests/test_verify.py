"""Tests for the full verifier: each check passes on a good case and fails on a bad one."""
import json
from datetime import timedelta

import pytest

from suraag.model import Case
from suraag.parse import Artifacts
from suraag.render import render_calls, render_chat, render_photo, stub_filler
from suraag.skeleton import build_case
from suraag.verify import (check_causality, check_cross_time, check_distractor, check_solvability,
                           check_traceability, verify)
from tests.helpers import FIXTURE, load_case

CASE = load_case()


def arts_from(case: Case) -> Artifacts:
    return Artifacts(chat=render_chat(case, stub_filler(case)), calls=render_calls(case), photo=render_photo(case))


def case_with(mutate) -> Case:
    d = json.loads(FIXTURE.read_text("utf-8"))
    mutate(d)
    return Case.model_validate(d)


def codes(failures):
    return [f.code for f in failures]


def test_good_case_verifies_clean():
    assert verify(CASE, arts_from(CASE)) == []
    assert check_traceability(CASE) == [] and check_causality(CASE) == []


def test_traceability_fails_for_unanchored_fact_and_unmapped_question():
    bad = case_with(lambda d: (d["facts"][0].update(anchors=[]), d["questions"][0].update(answer_facts=[])))
    assert set(codes(check_traceability(bad))) == {"fact_no_anchor", "question_no_fact"}


def test_cross_time_fails_when_chat_and_calls_disagree():
    arts = arts_from(CASE)
    arts.calls = arts.calls.replace("21:13:00", "21:17:00")
    fails = check_cross_time(CASE, arts)
    assert codes(fails) == ["cross_time"] and "differs by 3 min (tolerance 2)" in fails[0].message
    assert check_cross_time(CASE, arts_from(CASE)) == []


def test_cross_time_works_across_midnight():
    def mutate(d):
        d["chat_anchors"][0]["message"]["t"] = "2026-03-04T23:59:00+05:30"
        d["calls"][2]["t"] = "2026-03-05T00:01:00+05:30"

    case = case_with(mutate)
    arts = arts_from(case)
    assert "11:59 pm" in arts.chat and "2026-03-05T00:01:00+05:30" in arts.calls
    assert check_cross_time(case, arts) == []  # 2 minutes apart, not 1,438


def test_causality_fails_when_a_cause_comes_after_its_effect():
    bad = case_with(lambda d: d["timeline"][0].update(t="2026-03-04T22:00:00+05:30"))  # transfer after instruction
    assert "cause_after_effect" in codes(check_causality(bad))


def test_solvability_fails_when_the_solver_cannot_reproduce_the_key():
    arts = arts_from(CASE)
    arts.calls = arts.calls.replace(',"Raju bhai",', ',"",')
    fails = check_solvability(CASE, arts)
    assert codes(fails) == ["solver_mismatch"] and "Q1: solver answered UNSOLVABLE, key is P1" == fails[0].message


def test_distractor_checks():
    assert check_distractor(CASE, arts_from(CASE)) == []
    assert codes(check_distractor(case_with(lambda d: d.update(distractors=[])), arts_from(CASE))) == ["no_distractor"]

    def far_and_dissimilar(d):
        d["timeline"][4]["t"] = "2026-03-05T02:00:00+05:30"
        d["people"][2]["aliases"] = ["Zed"]

    bad = case_with(far_and_dissimilar)
    assert "distractor_implausible" in codes(check_distractor(bad, arts_from(bad)))

    arts = arts_from(CASE)
    arts.calls = arts.calls.replace('"+91-50000-00001","Raju bhai"', '"+91-50000-00003","Raju bhai"')
    assert "solver_picked_distractor" in codes(check_distractor(CASE, arts))


@pytest.mark.parametrize("lang", ["en", "hinglish"])
def test_invariant_stub_filler_cases_always_verify(lang):
    """Across 50 seeds, a freshly built case with stub filler passes every check."""
    for seed in range(1, 51):
        case = build_case(seed, lang)
        assert verify(case, arts_from(case)) == [], f"seed {seed}"
