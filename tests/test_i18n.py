"""Tests for the English/Hindi strings and the message renderers."""
import re
import string

import pytest

from suraag.defects import EXPECTED, inject
from suraag.grade import Citation, Claim, grade_claim
from suraag.i18n import EN, HI, STRINGS, render_expl, render_failure, t
from suraag.parse import Artifacts
from suraag.render import render_calls, render_chat, render_photo, stub_filler
from suraag.repair import GenMeta, run
from suraag.verify import verify
from tests.helpers import load_case

CASE = load_case()
DEVANAGARI = re.compile(r"[ऀ-ॿ]")


def arts() -> Artifacts:
    return Artifacts(render_chat(CASE, stub_filler(CASE)), render_calls(CASE), render_photo(CASE))


def fields(template: str) -> set[str]:
    # list-format variants (needles_nor / needles_slash, has_and ...) count as one placeholder
    return {re.sub(r"_(and|nor|slash)$", "", f) for _, f, _, _ in string.Formatter().parse(template) if f}


def test_both_languages_have_exactly_the_same_keys():
    assert set(EN) == set(HI)


def test_placeholders_match_between_languages():
    for key in EN:
        assert fields(EN[key]) == fields(HI[key]), key


def test_hindi_strings_are_really_hindi_and_english_ones_are_not():
    for key, text in HI.items():
        if text == EN[key]:  # language-neutral ("n = {n}") or the deliberately empty plain-persona affixes
            assert not text or key == "eval.n", key
            continue
        assert DEVANAGARI.search(text), key
    assert not any(DEVANAGARI.search(v) for v in EN.values())


def test_no_emoji_and_only_the_allowed_glyphs():
    allowed = set("✓✕→↑")
    for lang in STRINGS.values():
        for key, text in lang.items():
            odd = [c for c in text if ord(c) > 0x2000 and not DEVANAGARI.match(c) and c not in allowed
                   and c not in "—’“”"]
            assert not odd, (key, odd)


def test_t_formats_and_falls_back_to_english():
    assert t("lec.attempt", "en", n=2, action="re-render calls") == "Attempt 2: re-render calls"
    assert t("ui.tab_student", "hi") == "छात्र"
    assert t("ui.tab_student", "xx") == "Student"
    with pytest.raises(KeyError):
        t("no.such.key")


def failures_from_every_defect():
    out = []
    for kind, target in (("timestamp_clash", "chat"), ("timestamp_clash", "calls"), ("alias_conflict", "chat"),
                         ("missing_anchor", "chat"), ("unsolvable_question", "calls")):
        out += verify(CASE, inject(CASE, arts(), kind, target=target))
    raw = Artifacts(render_chat(CASE, stub_filler(CASE)), render_calls(CASE), None)
    out += verify(CASE, raw, mode="raw")
    return out


def test_english_rendering_is_identical_to_the_verifiers_own_message():
    fails = failures_from_every_defect()
    assert {f.code for f in fails} >= set(EXPECTED.values())
    for f in fails:
        assert render_failure(f, "en") == f.message, f.code


def test_every_failure_renders_in_hindi_without_losing_the_evidence_strings():
    for f in failures_from_every_defect():
        hi = render_failure(f, "hi")
        assert DEVANAGARI.search(hi), f.code
        for token in re.findall(r"chat\.txt:\d+|calls\.csv:\d+|photo\.jpg:\w+", f.message):
            assert token in hi, (f.code, token)  # file references are never translated


def test_unrepairable_failures_render_too():
    res = run(CASE, filler_fn=lambda c, e: [], meta=GenMeta(1, "stub", {}, "hybrid", "hinglish"),
              out_dir="unused", log_path=__import__("pathlib").Path("unused.jsonl"))
    f = res.attempts[0].failures[0]
    assert render_failure(f, "en") == f.message and DEVANAGARI.search(render_failure(f, "hi"))


def test_grader_explanations_match_the_design_kit_copy():
    lines = render_chat(CASE, stub_filler(CASE)).split("\n")
    lines[2] = "04/03/26, 8:35 pm - Vicky: kal milte hain"
    a = Artifacts("\n".join(lines), render_calls(CASE), render_photo(CASE))
    r = grade_claim(CASE, a, Claim("Q1", "P1", (Citation("chat", line=3), Citation("calls", row=3))))
    wrong = next(e for e in r.explanations if e.code == "cite_wrong")
    assert render_expl(wrong, "en") == 'chat.txt:3 contains neither "9:14 pm" nor "Raju bhai". A supporting line is chat.txt:12.'
    hi = render_expl(wrong, "hi")
    assert "chat.txt:3" in hi and "chat.txt:12" in hi and '"9:14 pm"' in hi and DEVANAGARI.search(hi)


def test_every_grader_explanation_code_renders_in_both_languages():
    from suraag.grade import Expl
    samples = [Expl("answer_ok", {"question": "Q1"}), Expl("answer_wrong", {"question": "Q1"}),
               Expl("cite_valid", {"loc": "chat.txt:12"}),
               Expl("cite_partial", {"loc": "chat.txt:3", "has": ["9:14 pm"], "missing": ["Raju bhai"], "support": "chat.txt:12"}),
               Expl("cite_wrong", {"loc": "chat.txt:3", "needles": ["a", "b"], "support": "chat.txt:12"}),
               Expl("cite_nonexistent", {"loc": "chat.txt:999"}),
               Expl("cite_irrelevant", {"loc": "photo.jpg:Make", "artifact": "photo.jpg"}),
               Expl("cite_missing_artifact", {"artifact": "calls.csv", "support": "calls.csv:3"})]
    for e in samples:
        assert render_expl(e, "en") and DEVANAGARI.search(render_expl(e, "hi")), e.code
