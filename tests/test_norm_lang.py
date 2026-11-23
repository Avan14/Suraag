"""Tests for norm and the language packs."""
import pytest

from suraag.lang import get_pack
from suraag.norm import norm


def test_norm_equates_case_spacing_zero_width_and_nukta():
    assert norm("Raju  Bhai​") == norm("raju bhai")
    assert norm("क़") == norm("क")
    assert norm("a b c") == "a b c"


HINGLISH_POS = ["record delete kar dena", "entry delete krdo", "wo transaction hata do",
                "record del karo jaldi", "RECORD DELETE KAR DO"]
HINGLISH_NEG = ["kal milte hain", "record dekh liya", "delete wala joke sun", "paise aa gaye"]
ENGLISH_POS = ["delete the transfer record now", "please remove that entry", "erase the transaction record"]
ENGLISH_NEG = ["record the match tonight", "remove the tea cups from the table", "transfer the files tomorrow"]


@pytest.mark.parametrize("s", HINGLISH_POS)
def test_hinglish_trigger_pos(s):
    assert get_pack("hinglish").triggers["instruction"].search(norm(s))


@pytest.mark.parametrize("s", HINGLISH_NEG)
def test_hinglish_trigger_neg(s):
    assert not get_pack("hinglish").triggers["instruction"].search(norm(s))


@pytest.mark.parametrize("s", ENGLISH_POS)
def test_english_trigger_pos(s):
    assert get_pack("en").triggers["instruction"].search(norm(s))


@pytest.mark.parametrize("s", ENGLISH_NEG)
def test_english_trigger_neg(s):
    assert not get_pack("en").triggers["instruction"].search(norm(s))


@pytest.mark.parametrize("lang", ["en", "hinglish"])
def test_pack_consistency(lang):
    p = get_pack(lang)
    trig = p.triggers["instruction"]
    assert len(p.stub_lines) >= 12 and len(p.places) >= 6 and len(p.instruction_templates) >= 2
    assert not any(trig.search(norm(s)) for s in p.stub_lines)
    assert all(trig.search(norm(t.format(owner="Vicky"))) for t in p.instruction_templates)
    assert {"who", "when", "where"} <= set(p.question_texts)
    for tpl in (p.filler_prompt, p.raw_prompt, p.brief_summary):
        assert tpl.strip()


def test_devanagari_pack_is_a_stretch_goal():
    with pytest.raises(NotImplementedError):
        get_pack("hi")
