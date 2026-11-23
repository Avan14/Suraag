"""Tests for parse."""
from datetime import datetime

from suraag.model import IST
from suraag.parse import HEADER, Artifacts, ChatLine, load_calls, load_chat, text_at

CSV_MIN = ("# " + HEADER + "\nrow,datetime,direction,number,contact_name,duration_s\n"
           '1,2026-03-04 21:13:00,incoming,+91-50000-00001,"Raju, Kurla",95\n'
           "2,2026-03-04 21:25:00,missed,+91-50000-00003,Raju K,0\n")


def chat(*lines):
    return HEADER + "\n" + "\n".join(lines) + "\n"


def test_chat_text_with_syntax_chars():
    arts = Artifacts(chat=chat('04/03/26, 9:14 pm - Raju bhai: time: 9 - 10, ok, "done"'), calls=CSV_MIN, photo=None)
    header, msg = load_chat(arts.chat)
    assert header.t is None and header.line == 1
    assert (msg.line, msg.sender, msg.text) == (2, "Raju bhai", 'time: 9 - 10, ok, "done"')
    assert msg.t == datetime(2026, 3, 4, 21, 14, tzinfo=IST)


def test_csv_quoted_contact_and_header_skipped():
    rows = load_calls(CSV_MIN)
    assert [r.row for r in rows] == [1, 2]
    assert rows[0].contact_name == "Raju, Kurla" and rows[0].t.hour == 21 and rows[1].direction == "missed"


def test_csv_with_bom_is_read():
    assert len(load_calls("﻿" + CSV_MIN)) == 2


def test_text_at_chat_and_calls():
    arts = Artifacts(chat=chat("04/03/26, 9:14 pm - Raju bhai: hi"), calls=CSV_MIN, photo=None)
    assert "9:14 pm" in text_at(arts, "chat", line=2) and "Raju bhai" in text_at(arts, "chat", line=2)
    got = text_at(arts, "calls", row=1)
    assert "21:13" in got and "+91-50000-00001" in got


def test_text_at_missing_returns_none():
    arts = Artifacts(chat=chat("04/03/26, 9:14 pm - A: x"), calls=CSV_MIN, photo=None)
    assert text_at(arts, "chat", line=999) is None
    assert text_at(arts, "calls", row=99) is None
    assert text_at(arts, "photo", exif_tag="GPSLatitude") is None


def test_unparseable_line_is_kept_raw():
    lines = load_chat(chat("this is not a message"))
    assert lines[1] == ChatLine(2, None, None, "this is not a message", "this is not a message")


def test_sha256_matches_bytes_and_uses_bom_for_csv():
    import hashlib
    arts = Artifacts(chat="a\n", calls="b\n", photo=b"jpg")
    h = arts.sha256()
    assert h["chat.txt"] == hashlib.sha256(b"a\n").hexdigest()
    assert h["calls.csv"] == hashlib.sha256(b"\xef\xbb\xbfb\n").hexdigest()
    assert h["photo.jpg"] == hashlib.sha256(b"jpg").hexdigest()
