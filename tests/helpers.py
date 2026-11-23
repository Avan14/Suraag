"""Shared test helpers: the fixture case and a hand-built correct chat for it."""
import json
from datetime import datetime, timedelta
from pathlib import Path

from suraag.model import IST, Case
from suraag.lang import get_pack
from suraag.parse import HEADER
from suraag.timefmt import chat_ts

FIXTURE = Path(__file__).parent / "fixtures" / "case_001" / "world.json"


def load_case() -> Case:
    return Case.model_validate(json.loads(FIXTURE.read_text("utf-8")))


def good_chat(case: Case) -> str:
    """24 lines: header, anchor at line 12, increasing times, senders that are real aliases."""
    anchor = case.chat_anchors[0]
    senders = [case.person(p).saved_as for p in case.chat_members]
    lines = [HEADER]
    start = datetime(2026, 3, 4, 20, 34, tzinfo=IST)
    after = datetime(2026, 3, 4, 21, 16, tzinfo=IST)
    for n in range(2, case.chat_length + 1):
        if n == anchor.line:
            m = anchor.message
            lines.append(f"{chat_ts(m.t)} - {m.sender}: {m.text}")
        else:
            if n < anchor.line:
                t = start + timedelta(minutes=4 * (n - 2))
            else:
                t = after + timedelta(minutes=2 * (n - anchor.line - 1))
            stub = get_pack("hinglish").stub_lines
            lines.append(f"{chat_ts(t)} - {senders[n % len(senders)]}: {stub[n % len(stub)]}")
    return "\n".join(lines) + "\n"
