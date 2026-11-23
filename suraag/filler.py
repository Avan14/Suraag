"""Hybrid mode: the LLM writes only the filler between the anchored lines.

It never raises: bad JSON or an unavailable LLM falls back to the offline stub filler, and
`last_source` says which one was used so the UI can show "offline: stub filler". It does NOT
repair bad senders, times or counts; the verifier and FillerShortError surface those.
"""
import json
from datetime import timedelta

from suraag.lang import get_pack
from suraag.llm import LLMUnavailable, complete, prompt_hash
from suraag.model import Case, ChatMessage
from suraag.render import filler_gaps, stub_filler
from suraag.timefmt import chat_time, parse_chat_ts

last_source: str = "stub"  # "llm" or "stub": what the most recent llm_filler call returned
FILLER_PROMPT_VERSION = prompt_hash(get_pack("hinglish").filler_prompt + get_pack("en").filler_prompt)


def _parse(raw: str, case: Case) -> list[ChatMessage] | None:
    lo, hi = raw.find("["), raw.rfind("]")
    if lo < 0 or hi < lo:
        return None
    try:
        items = json.loads(raw[lo:hi + 1])
        day = case.chat_window[0]
        out = []
        for it in items:
            t = parse_chat_ts(f"{day:%d/%m/%y}, {it['time']}")
            if t < day:  # a chat that runs past midnight
                t += timedelta(days=1)
            out.append(ChatMessage(t=t, sender=str(it["sender"]), text=str(it["text"])))
        return out
    except (ValueError, KeyError, TypeError):
        return None


def llm_filler(case: Case, errors: list[str] | None = None) -> list[ChatMessage]:
    global last_source
    pack = get_pack(case.lang)
    senders = ", ".join(case.person(p).saved_as for p in case.chat_members)
    gaps = "\n".join(f"- between {chat_time(t0)} and {chat_time(t1)}: {len(lines)} messages"
                     for t0, t1, lines in filler_gaps(case))
    for attempt in range(2):
        problems = list(errors or []) + (["previous output was not valid JSON"] if attempt else [])
        err = ("Fix these problems from your previous attempt:\n" + "\n".join(f"- {e}" for e in problems)) if problems else ""
        try:
            raw = complete(pack.filler_prompt.format(senders=senders, gaps=gaps, errors=err))
        except LLMUnavailable:
            break
        msgs = _parse(raw, case)
        if msgs is not None:
            last_source = "llm"
            return msgs
    last_source = "stub"
    return stub_filler(case)
