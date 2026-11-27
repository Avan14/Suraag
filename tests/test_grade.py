"""Tests for the deterministic grader."""
from suraag.grade import Citation, Claim, grade_all, grade_claim, rationale_flag
from suraag.parse import Artifacts
from suraag.render import render_calls, render_chat, render_photo, stub_filler
from tests.helpers import load_case

CASE = load_case()


def arts(chat=None) -> Artifacts:
    return Artifacts(chat=chat or render_chat(CASE, stub_filler(CASE)), calls=render_calls(CASE),
                     photo=render_photo(CASE))


CHAT12, CALLS3 = Citation("chat", line=12), Citation("calls", row=3)
GOOD = Claim("Q1", "P1", (CHAT12, CALLS3))


def codes(r):
    return [e.code for e in r.explanations]


def test_right_answer_with_right_lines_scores_two():
    r = grade_claim(CASE, arts(), GOOD)
    assert (r.answer_correct, r.citation_valid, r.points) == (True, True, 2)
    assert [m.label for m in r.marks] == ["valid", "valid"]


def test_right_answer_wrong_line_loses_only_the_citation_point_and_names_the_support():
    lines = render_chat(CASE, stub_filler(CASE)).split("\n")
    lines[2] = "04/03/26, 8:35 pm - Vicky: kal milte hain"  # line 3 holds neither the time nor the name
    r = grade_claim(CASE, arts("\n".join(lines)), Claim("Q1", "P1", (Citation("chat", line=3), CALLS3)))
    assert (r.answer_correct, r.citation_valid, r.points) == (True, False, 1)
    wrong = next(e for e in r.explanations if e.code == "cite_wrong")
    assert wrong.params["loc"] == "chat.txt:3" and wrong.params["support"] == "chat.txt:12"
    assert "9:14 pm" in wrong.params["needles"] and "Raju bhai" in wrong.params["needles"]


def test_wrong_answer_right_lines_loses_only_the_answer_point():
    r = grade_claim(CASE, arts(), Claim("Q1", "P3", (CHAT12, CALLS3)))
    assert (r.answer_correct, r.citation_valid, r.points) == (False, True, 1)
    assert "answer_wrong" in codes(r)


def test_an_extra_supporting_line_is_allowed_even_if_it_is_not_the_anchor():
    lines = render_chat(CASE, stub_filler(CASE)).split("\n")
    lines[14] = "04/03/26, 9:14 pm - Raju bhai: haan wahi baat"  # line 15 also holds both values
    r = grade_claim(CASE, arts("\n".join(lines)), Claim("Q1", "P1", (CHAT12, Citation("chat", line=15), CALLS3)))
    assert r.citation_valid and [m.label for m in r.marks] == ["valid", "valid", "valid"]


def test_a_partial_line_neither_earns_nor_costs_and_says_what_is_missing():
    lines = render_chat(CASE, stub_filler(CASE)).split("\n")
    lines[14] = "04/03/26, 9:14 pm - Vicky: ok"  # has the time but not the name
    r = grade_claim(CASE, arts("\n".join(lines)), Claim("Q1", "P1", (CHAT12, Citation("chat", line=15), CALLS3)))
    assert r.citation_valid and r.marks[1].label == "partial"
    part = next(e for e in r.explanations if e.code == "cite_partial")
    assert part.params["missing"] == ["Raju bhai"]


def test_a_required_artifact_with_no_citation_fails_the_citation_point():
    r = grade_claim(CASE, arts(), Claim("Q1", "P1", (CHAT12,)))  # the call-log row is missing
    assert not r.citation_valid
    miss = next(e for e in r.explanations if e.code == "cite_missing_artifact")
    assert miss.params["artifact"] == "calls.csv" and miss.params["support"] == "calls.csv:3"


def test_no_citations_at_all_fails_the_citation_point():
    assert not grade_claim(CASE, arts(), Claim("Q1", "P1", ())).citation_valid


def test_citing_a_line_that_does_not_exist_is_wrong():
    r = grade_claim(CASE, arts(), Claim("Q1", "P1", (CHAT12, CALLS3, Citation("chat", line=999))))
    assert not r.citation_valid and "cite_nonexistent" in codes(r)


def test_citing_an_artifact_the_question_does_not_use_is_wrong():
    r = grade_claim(CASE, arts(), Claim("Q1", "P1", (CHAT12, CALLS3, Citation("photo", exif_tag="Make"))))
    assert not r.citation_valid and "cite_irrelevant" in codes(r)


def test_when_answers_accept_several_formats_within_the_tolerance():
    for ans in ("9:14 pm", "21:14", "9:15 pm", "21:13", "2026-03-04T21:14:00+05:30", "9:14 PM",
                "9:14 p.m.", "9.14 pm", "9:14pm", "9:14 P.M.", "21.14", " 9.14 p.m "):
        assert grade_claim(CASE, arts(), Claim("Q2", ans, (CHAT12, CALLS3))).answer_correct, ans
    for ans in ("9:20 pm", "21:10", "garbage", "", "9:14 a.m.", "9.14", "21.74"):
        assert not grade_claim(CASE, arts(), Claim("Q2", ans, (CHAT12, CALLS3))).answer_correct, ans


def test_where_uses_the_photo_exif_citation():
    good = Claim("Q3", "PL2", (Citation("photo", exif_tag="GPSLatitude"),))
    r = grade_claim(CASE, arts(), good)
    assert r.answer_correct and r.citation_valid
    assert not grade_claim(CASE, arts(), Claim("Q3", "PL2", (Citation("photo", exif_tag="Make"),))).citation_valid


def test_same_input_always_gives_the_same_score():
    first = grade_claim(CASE, arts(), GOOD)
    assert all(grade_claim(CASE, arts(), GOOD) == first for _ in range(5))


def test_unanswered_questions_score_zero_in_grade_all():
    results = grade_all(CASE, arts(), [GOOD])
    assert [r.question_id for r in results] == ["Q1", "Q2", "Q3"]
    assert [r.points for r in results] == [2, 0, 0]


def test_rationale_is_advisory_and_never_changes_the_score():
    base = grade_claim(CASE, arts(), GOOD)
    with_text = grade_claim(CASE, arts(), Claim("Q1", "P1", (CHAT12, CALLS3), rationale="He did it, definitely."))
    assert with_text.points == base.points
    assert base.rationale_flag is None and with_text.rationale_flag == "could_not_verify"


def test_overclaim_classifier_is_optional_and_failures_fall_back_safely():
    assert rationale_flag("") is None and rationale_flag("text") == "could_not_verify"
    assert rationale_flag("text", classify=lambda r: "overclaim") == "overclaim"
    assert rationale_flag("text", classify=lambda r: "ok") == "ok"

    def boom(_):
        raise RuntimeError("llm down")

    assert rationale_flag("text", classify=boom) == "could_not_verify"
    assert rationale_flag("text", classify=lambda r: "nonsense") == "could_not_verify"
