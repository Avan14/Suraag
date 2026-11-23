"""Tests for rawmode."""
from suraag import rawmode
from suraag.parse import HEADER
from tests.helpers import load_case


def test_raw_chat_prepends_header_and_strips_fences(monkeypatch):
    seen = {}

    def fake(prompt, **kw):
        seen["prompt"] = prompt
        return "```\n04/03/26, 9:14 pm - Raju bhai: hi\n\n04/03/26, 9:15 pm - Vicky: ok\n```"

    monkeypatch.setattr(rawmode, "complete", fake)
    out = rawmode.raw_chat(load_case(), errors=["chat.txt:3 problem"], nonce=7)
    assert out == HEADER + "\n04/03/26, 9:14 pm - Raju bhai: hi\n04/03/26, 9:15 pm - Vicky: ok\n"
    p = seen["prompt"]
    assert "Vicky, wo transfer ka record delete kar dena abhi" in p   # anchor verbatim
    assert "chat.txt:3 problem" in p and "nonce: 7" in p and "23" in p  # errors, nonce, message-line count
