"""Tests for the hybrid LLM filler (the LLM is faked)."""
import json

from suraag import filler
from suraag.llm import LLMUnavailable
from suraag.model import IST
from suraag.parse import Artifacts
from suraag.render import render_calls, render_chat, stub_filler
from suraag.timefmt import chat_time
from suraag.verify import check_chat_consistency
from tests.helpers import load_case

CASE = load_case()


def as_json(msgs, **over):
    return json.dumps([{"time": chat_time(m.t), "sender": over.get("sender", m.sender), "text": m.text}
                       for m in msgs])


def test_valid_json_becomes_messages_with_ist_times(monkeypatch):
    monkeypatch.setattr(filler, "complete", lambda prompt, **kw: "```json\n" + as_json(stub_filler(CASE)) + "\n```")
    out = filler.llm_filler(CASE, [])
    assert len(out) == 22 and filler.last_source == "llm"
    assert out[0].t.tzinfo is not None and out[0].t.utcoffset() == IST.utcoffset(None)
    assert out[0].t.date() == CASE.chat_window[0].date()


def test_invalid_json_twice_falls_back_to_stub(monkeypatch):
    calls = []
    monkeypatch.setattr(filler, "complete", lambda prompt, **kw: calls.append(prompt) or "not json at all")
    assert filler.llm_filler(CASE, []) == stub_filler(CASE)
    assert filler.last_source == "stub" and len(calls) == 2
    assert "previous output was not valid JSON" in calls[1]


def test_llm_unavailable_falls_back_to_stub(monkeypatch):
    def boom(prompt, **kw):
        raise LLMUnavailable("no key")

    monkeypatch.setattr(filler, "complete", boom)
    assert filler.llm_filler(CASE, []) == stub_filler(CASE) and filler.last_source == "stub"


def test_bad_sender_is_returned_unchanged_so_the_verifier_catches_it(monkeypatch):
    monkeypatch.setattr(filler, "complete", lambda prompt, **kw: as_json(stub_filler(CASE), sender="Stranger"))
    out = filler.llm_filler(CASE, [])
    arts = Artifacts(chat=render_chat(CASE, out), calls=render_calls(CASE))
    assert "alias_unresolved" in [f.code for f in check_chat_consistency(CASE, arts)]


def test_previous_errors_are_in_the_prompt_and_gaps_are_described(monkeypatch):
    seen = []
    monkeypatch.setattr(filler, "complete", lambda prompt, **kw: seen.append(prompt) or as_json(stub_filler(CASE)))
    filler.llm_filler(CASE, ["chat.txt:5 sender 'X' resolves to 0 people"])
    assert "chat.txt:5 sender 'X' resolves to 0 people" in seen[0]
    assert "10 messages" in seen[0] and "12 messages" in seen[0]  # lines 2-11 before the anchor, 13-24 after
    assert "Vicky" in seen[0]  # allowed senders are listed


def test_prompt_version_is_a_short_hash():
    assert len(filler.FILLER_PROMPT_VERSION) == 12
