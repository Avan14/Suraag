"""App-level flow, offline: a student's answers survive a view switch, and Submit grades them.

Only the active view runs, and Streamlit drops the state of widgets that were not drawn, so these are real
regression risks (found in review), not formalities.
"""
import os

import pytest
from streamlit.testing.v1 import AppTest

CASE = "upi-ring-001-en"


@pytest.fixture(autouse=True)
def offline(monkeypatch):
    monkeypatch.setenv("SURAAG_OFFLINE", "1")


def start(view: str) -> AppTest:
    at = AppTest.from_file(os.path.join(os.path.dirname(__file__), "..", "app.py"), default_timeout=60)
    at.session_state["view"] = view
    at.session_state["lang"] = "en"  # the harness calls format_func outside a script run
    return at.run()


def go(at: AppTest, view: str) -> AppTest:
    at.button(key=f"nav_{view}").click()
    return at.run()


def test_student_answers_survive_a_trip_to_another_view():
    at = start("student")
    at.text_input(key=f"r::{CASE}::Q1").input("the delete line and the call before it")
    at.text_input(key=f"a::{CASE}::Q2").input("6:58 pm")
    at.run()
    at = go(at, "lecturer")
    at = go(at, "student")
    assert not at.exception
    assert at.text_input(key=f"r::{CASE}::Q1").value == "the delete line and the call before it"
    assert at.text_input(key=f"a::{CASE}::Q2").value == "6:58 pm"


def test_lecturer_choices_survive_a_trip_to_another_view():
    at = start("lecturer")
    at.number_input(key="gen_seed").set_value(42)
    at.run()
    at = go(at, "eval")
    at = go(at, "lecturer")
    assert not at.exception
    assert at.number_input(key="gen_seed").value == 42


def test_submit_grades_through_the_button_and_reset_clears_it():
    at = start("student")
    at.session_state[f"cites::{CASE}"] = {"Q2": ["chat:13", "calls:4"]}
    at.text_input(key=f"a::{CASE}::Q2").input("6:58 pm")
    at.run()
    at.button(key=f"submit::{CASE}").click()
    at.run()
    assert not at.exception
    graded = at.session_state[f"graded::{CASE}"]
    q2 = next(r for r in graded if r.question_id == "Q2")
    assert q2.answer_correct and q2.citation_valid
    at.button(key=f"reset::{CASE}").click()
    at.run()
    assert not at.exception and f"graded::{CASE}" not in at.session_state


LEVEL2 = "L2-upi-ring-021-en"


def test_a_student_picks_a_level_and_opens_the_worked_solution_after_submitting():
    at = start("student")
    at.button(key="stulevel_2").click()
    at.run()
    assert at.selectbox(key="stu_pick").value == LEVEL2
    at.button(key=f"submit::{LEVEL2}").click()
    at.run()
    assert not at.exception
    assert [e.label for e in at.expander].count("How to solve it") == 3  # one per question


def test_the_lecturer_sees_the_depth_check_for_a_practice_level():
    at = start("lecturer")
    at.selectbox(key="lec_pick").set_value(LEVEL2)
    at.run()
    assert not at.exception
    assert any("Depth" in m.value for m in at.markdown)
