"""Tests for the chat-only checks in verify."""
from suraag.parse import Artifacts
from suraag.verify import check_anchors, check_chat_consistency
from tests.helpers import good_chat, load_case

CASE = load_case()
CALLS = ("# x\nrow,datetime,direction,number,contact_name,duration_s\n"
         "3,2026-03-04 21:13:00,incoming,+91-50000-00001,Raju bhai,95\n")


def arts(chat: str) -> Artifacts:
    return Artifacts(chat=chat, calls=CALLS, photo=None)


def codes(failures):
    return [f.code for f in failures]


def chat_anchor_failures(a, mode="hybrid"):
    return [f for f in check_anchors(CASE, a, mode) if f.artifact == "chat"]


def test_correct_chat_has_no_chat_failures():
    a = arts(good_chat(CASE))
    assert chat_anchor_failures(a) == [] and check_chat_consistency(CASE, a) == []


def test_swapped_filler_times_give_time_order():
    lines = good_chat(CASE).split("\n")
    lines[4], lines[5] = lines[5], lines[4]  # lines 5 and 6 swap, so line 5 is now later than line 6
    fails = check_chat_consistency(CASE, arts("\n".join(lines)))
    assert "time_order" in codes(fails)
    assert "earlier than" in [f for f in fails if f.code == "time_order"][0].message


def test_unknown_sender_gives_alias_unresolved_with_count():
    lines = good_chat(CASE).split("\n")
    lines[2] = "04/03/26, 8:38 pm - Raju: kal milte hain"
    fails = [f for f in check_chat_consistency(CASE, arts("\n".join(lines))) if f.code == "alias_unresolved"]
    assert fails and "resolves to 0 people" in fails[0].message and fails[0].message.startswith("chat.txt:3")


def test_trigger_phrase_in_filler_is_flagged():
    lines = good_chat(CASE).split("\n")
    lines[6] = lines[6].split(": ")[0] + ": entry delete krdo"
    fails = [f for f in check_chat_consistency(CASE, arts("\n".join(lines))) if f.code == "trigger_in_filler"]
    assert [f.params["line"] for f in fails] == [7]


def test_anchor_text_removed_gives_anchor_missing():
    chat = good_chat(CASE).replace("Raju bhai: Vicky", "Vicky: Vicky")
    fails = chat_anchor_failures(arts(chat))
    assert any(f.code == "anchor_missing" and "chat.txt:12" in f.message and "'Raju bhai'" in f.message for f in fails)


def test_raw_mode_finds_the_anchor_wherever_it_is():
    lines = good_chat(CASE).split("\n")
    anchor = lines.pop(11)
    lines.insert(4, anchor)  # now at line 5, so line 12 no longer holds it
    a = arts("\n".join(lines))
    assert chat_anchor_failures(a) != []
    assert chat_anchor_failures(a, "raw") == []


def test_raw_mode_flags_a_second_instruction_line():
    lines = good_chat(CASE).split("\n")
    lines[6] = lines[6].split(": ")[0] + ": record delete kar do"
    fails = check_chat_consistency(CASE, arts("\n".join(lines)), mode="raw")
    assert "trigger_in_filler" in codes(fails)
