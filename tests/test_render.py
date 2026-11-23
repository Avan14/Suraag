"""Tests for the chat and calls renderers and stub filler."""
import pytest

from suraag.model import ChatMessage
from suraag.parse import HEADER, Artifacts, load_calls, load_chat, text_at
from suraag.render import FillerShortError, render_calls, render_chat, stub_filler, write_artifacts
from suraag.verify import check_anchors, check_chat_consistency
from tests.helpers import load_case

CASE = load_case()


def test_stub_filler_is_deterministic_and_the_right_size():
    a, b = stub_filler(CASE), stub_filler(CASE)
    assert a == b and len(a) == CASE.filler_needed() == 22


def test_render_is_byte_for_byte_repeatable():
    assert render_chat(CASE, stub_filler(CASE)) == render_chat(CASE, stub_filler(CASE))
    assert render_calls(CASE) == render_calls(CASE)


def test_chat_layout_and_anchor_line():
    chat = render_chat(CASE, stub_filler(CASE))
    lines = chat.split("\n")
    assert lines[0] == HEADER and len(lines) == 25 and lines[-1] == ""  # 24 lines + trailing newline
    arts = Artifacts(chat=chat, calls=render_calls(CASE))
    at12 = text_at(arts, "chat", line=12)
    assert "9:14 pm" in at12 and "Raju bhai" in at12


def test_rendered_chat_passes_the_chat_checks():
    arts = Artifacts(chat=render_chat(CASE, stub_filler(CASE)), calls=render_calls(CASE))
    assert [f for f in check_anchors(CASE, arts) if f.artifact in ("chat", "calls")] == []
    assert check_chat_consistency(CASE, arts) == []


def test_short_filler_raises_with_counts():
    with pytest.raises(FillerShortError) as e:
        render_chat(CASE, stub_filler(CASE)[:-1])
    assert (e.value.needed, e.value.got) == (22, 21)


def test_extra_filler_is_dropped_and_newlines_flattened():
    filler = stub_filler(CASE)
    filler[0] = ChatMessage(t=filler[0].t, sender=filler[0].sender, text="two\nlines")
    chat = render_chat(CASE, filler + filler[:3])
    assert len(chat.split("\n")) == 25 and "two lines" in chat


def test_calls_roundtrip_and_header():
    csv_text = render_calls(CASE)
    assert csv_text.startswith("# " + HEADER + "\nrow,datetime,direction,number,contact_name,duration_s\n")
    rows = load_calls(csv_text)
    assert [r.row for r in rows] == [1, 2, 3, 4] and rows[2].number == "+91-50000-00001"


def test_written_files_roundtrip_and_csv_has_a_bom(tmp_path):
    arts = Artifacts(chat=render_chat(CASE, stub_filler(CASE)), calls=render_calls(CASE), photo=b"jpg")
    write_artifacts(arts, tmp_path)
    assert (tmp_path / "calls.csv").read_bytes().startswith(b"\xef\xbb\xbf")
    back = Artifacts.from_dir(tmp_path)
    assert back.chat == arts.chat and back.calls == arts.calls and back.sha256() == arts.sha256()
    assert len(load_chat(back.chat)) == 24
