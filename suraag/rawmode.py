"""Baseline: the LLM writes the whole chat from the world model (no fixed anchor lines)."""
from suraag.lang import get_pack
from suraag.llm import complete
from suraag.model import Case
from suraag.parse import HEADER
from suraag.timefmt import chat_ts


def raw_chat(case: Case, errors: list[str] | None = None, nonce: int | None = None,
             model: str | None = None) -> str:
    pack = get_pack(case.lang)
    senders = ", ".join(case.person(p).saved_as for p in case.chat_members)
    anchors = "\n".join(f"{chat_ts(a.message.t)} - {a.message.sender}: {a.message.text}" for a in case.chat_anchors)
    err = ("Fix these problems from your previous attempt:\n" + "\n".join(f"- {e}" for e in errors)) if errors else ""
    prompt = pack.raw_prompt.format(senders=senders, start=chat_ts(case.chat_window[0]),
                                    end=chat_ts(case.chat_window[1]), count=case.chat_length - 1,
                                    anchors=anchors, errors=err)
    if nonce is not None:  # makes the request distinct, so the cache doesn't return the same chat n times
        prompt += f"\nnonce: {nonce}"
    body = [ln.strip() for ln in complete(prompt, model=model).splitlines()
            if ln.strip() and not ln.strip().startswith("```")]
    return HEADER + "\n" + "\n".join(body) + "\n"
