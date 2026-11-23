"""Tests for the hint ladder."""
import pytest

from suraag.hints import PERSONAS, SPEECH, TIERS, base_hint, hint
from suraag.parse import load_chat
from suraag.render import render_chat, stub_filler
from suraag.skeleton import build_case
from tests.helpers import load_case

CASE = load_case()


def test_the_three_tiers_get_more_specific_for_the_who_question():
    assert base_hint(CASE, "Q1", 1) == "The evidence for this question is in chat.txt, calls.csv."
    assert base_hint(CASE, "Q1", 2) == "Look at chat.txt lines 9 to 15; calls.csv rows 2 to 4."
    assert base_hint(CASE, "Q1", 3) == "Check chat.txt:12, calls.csv:3."


def test_the_where_question_points_at_photo_tags_not_values():
    assert base_hint(CASE, "Q3", 1) == "The evidence for this question is in photo.jpg."
    assert base_hint(CASE, "Q3", 2) == "Look at photo.jpg tags GPSLatitude, GPSLongitude."
    assert base_hint(CASE, "Q3", 3) == "Check photo.jpg:GPSLatitude, photo.jpg:GPSLongitude."


def test_hints_work_in_hindi_and_keep_file_references_untranslated():
    hi = base_hint(CASE, "Q1", 3, "hi")
    assert "chat.txt:12" in hi and "calls.csv:3" in hi and "जाँचें" in hi


def all_hints(case, ui):
    for q in case.questions:
        for tier in range(1, TIERS + 1):
            for persona in PERSONAS:
                yield q.id, hint(case, q.id, tier, ui, persona)


def leak_strings(case):
    """Everything a hint must never say: the culprit, the evidence strings, a line's text."""
    key = {q.id: q for q in case.questions}["Q1"].answer
    culprit = case.person(key)
    out = {culprit.name, *culprit.aliases}
    for f in case.facts:
        for a in f.anchors:
            out |= set(a.must_contain)
    out |= {a.message.text for a in case.chat_anchors}
    out |= {p.name for p in case.places}
    return {s for s in out if s}


@pytest.mark.parametrize("ui", ["en", "hi"])
def test_no_hint_leaks_the_culprit_the_evidence_or_a_line_verbatim(ui):
    cases = [CASE] + [build_case(s, lang) for s in range(1, 26) for lang in ("en", "hinglish")]
    for case in cases:
        leaks = leak_strings(case)
        for qid, text in all_hints(case, ui):
            for bad in leaks:
                assert bad.casefold() not in text.casefold(), (case.case_id, qid, bad, text)


def test_a_hint_never_contains_the_text_of_any_chat_line():
    case = build_case(4, "hinglish")
    chat = load_chat(render_chat(case, stub_filler(case)))
    for qid, text in all_hints(case, "en"):
        assert not any(ln.text and ln.text in text for ln in chat), (qid, text)


def test_plain_is_the_bare_hint_and_other_personas_only_wrap_it():
    for tier in range(1, TIERS + 1):
        base = base_hint(CASE, "Q1", tier)
        assert hint(CASE, "Q1", tier, "en", "plain") == base
        for persona in ("vetaal", "birbal"):
            wrapped = hint(CASE, "Q1", tier, "en", persona)
            assert base in wrapped and wrapped != base and len(wrapped) < len(base) + 160


def test_bad_tier_or_persona_is_refused():
    for bad in (0, 4):
        with pytest.raises(ValueError):
            base_hint(CASE, "Q1", bad)
    with pytest.raises(ValueError):
        hint(CASE, "Q1", 1, "en", "someone-famous")


def test_speech_settings_are_rate_and_pitch_only():
    assert set(SPEECH) == set(PERSONAS)
    for cfg in SPEECH.values():
        assert set(cfg) == {"rate", "pitch"} and 0.5 <= cfg["rate"] <= 1.5 and 0.5 <= cfg["pitch"] <= 1.5
    assert SPEECH["plain"] == {"rate": 1.0, "pitch": 1.0}
