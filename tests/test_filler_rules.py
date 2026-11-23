"""Rule L-09: filler adds no facts."""
import pytest

from suraag.fillerrules import filler_violation
from suraag.i18n import render_failure
from suraag.lang import get_pack
from suraag.parse import Artifacts
from suraag.render import render_calls, render_chat, stub_filler
from suraag.verify import check_chat_consistency
from tests.helpers import good_chat, load_case

CASE = load_case()


@pytest.mark.parametrize("text,reason", [
    ("kal 5 baje milte hain", "digit"), ("meeting सुबह ९ बजे", "digit"),
    ("Rs bhej diya", "currency"), ("paanch lakh ka scene hai", "currency"), ("₹ aa gaya", "currency"),
    ("Monday ko baat karte hain", "date"), ("see you in March", "date"),
    ("dekh lo www dot site", None), ("check example.com now", "url"), ("visit https://x", "url"),
    ("Paytm pe dekh lena", "brand"), ("HDFC ka message aaya", "brand"),
    ("wo entry delete kar do", "instruction"), ("tum pay kar dena", "instruction"), ("bhej do abhi", "instruction"),
])
def test_each_rule_catches_its_case(text, reason):
    assert filler_violation(text) == reason


@pytest.mark.parametrize("lang", ["en", "hinglish"])
def test_every_stub_line_is_clean(lang):
    assert [s for s in get_pack(lang).stub_lines if filler_violation(s)] == []


def arts_with(lines):
    return Artifacts("\n".join(lines) + "\n", render_calls(CASE))


def test_a_bad_filler_line_fails_the_hybrid_check_with_a_clear_message():
    lines = good_chat(CASE).split("\n")[:-1]
    lines[4] = lines[4].split(": ")[0] + ": kal 7 baje milte hain"
    fails = [f for f in check_chat_consistency(CASE, arts_with(lines)) if f.code == "filler_content"]
    assert [f.params["line"] for f in fails] == [5] and fails[0].message == "chat.txt:5 filler contains a digit"
    assert "अंक" in render_failure(fails[0], "hi") and "chat.txt:5" in render_failure(fails[0], "hi")


def test_the_anchor_line_is_not_held_to_the_filler_rule():
    # the anchor holds a time and a name by design; only filler lines are checked
    assert [f for f in check_chat_consistency(CASE, Artifacts(good_chat(CASE), render_calls(CASE)))
            if f.code == "filler_content"] == []


def test_raw_mode_is_not_held_to_the_filler_rule():
    lines = good_chat(CASE).split("\n")[:-1]
    lines[4] = lines[4].split(": ")[0] + ": kal 7 baje milte hain"
    assert [f for f in check_chat_consistency(CASE, arts_with(lines), mode="raw") if f.code == "filler_content"] == []


def test_stub_filler_always_passes():
    chat = render_chat(CASE, stub_filler(CASE))
    assert [f for f in check_chat_consistency(CASE, Artifacts(chat, render_calls(CASE))) if f.code == "filler_content"] == []
