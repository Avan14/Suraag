"""Six deterministic checks -> list of failures. Plain code only; an LLM never verifies."""
from dataclasses import dataclass
from typing import Literal

from suraag.lang import get_pack
from suraag.model import Anchor, Case
from suraag.norm import norm
from suraag.parse import Artifacts, load_calls, load_chat, load_exif, text_at
from suraag.timefmt import chat_time

Mode = Literal["hybrid", "raw"]
FILES = {"chat": "chat.txt", "calls": "calls.csv", "photo": "photo.jpg"}


@dataclass(frozen=True)
class Failure:
    check: Literal["anchor", "traceability", "contradiction", "solvability", "distractor", "filler_count"]
    artifact: Literal["chat", "calls", "photo", "model"]
    code: str
    params: dict
    message: str


def _loc(a: Anchor) -> str:
    if a.artifact == "chat":
        return f"chat.txt:{a.line}"
    if a.artifact == "calls":
        return f"calls.csv:{a.row}"
    return f"photo.jpg:{a.exif_tag}"


def _all_texts(arts: Artifacts, artifact: str) -> list[str]:
    """Every location's text in one artifact, for raw mode's search-by-text anchors."""
    if artifact == "chat":
        return [ln.raw for ln in load_chat(arts.chat)]
    if artifact == "calls":
        return [t for r in load_calls(arts.calls) if (t := text_at(arts, "calls", row=r.row)) is not None]
    return list(load_exif(arts.photo).values()) if arts.photo is not None else []


def check_anchors(case: Case, arts: Artifacts, mode: Mode = "hybrid") -> list[Failure]:
    out = []
    for fact in case.facts:
        for a in fact.anchors:
            if mode == "raw":
                needles = [norm(m) for m in a.must_contain]
                if not any(all(n in norm(t) for n in needles) for t in _all_texts(arts, a.artifact)):
                    wanted = " and ".join(repr(m) for m in a.must_contain)
                    out.append(Failure("anchor", a.artifact, "anchor_missing", {"fact": fact.id},
                                       f"{FILES[a.artifact]}: no line contains {wanted}"))
                continue
            text = text_at(arts, a.artifact, line=a.line, row=a.row, exif_tag=a.exif_tag)
            if text is None:
                out.append(Failure("anchor", a.artifact, "anchor_missing", {"fact": fact.id, "loc": _loc(a)},
                                   f"{_loc(a)} does not exist"))
                continue
            for m in a.must_contain:
                if norm(m) not in norm(text):
                    out.append(Failure("anchor", a.artifact, "anchor_missing",
                                       {"fact": fact.id, "loc": _loc(a), "needle": m},
                                       f"{_loc(a)} does not contain {m!r}"))
    return out


def check_chat_consistency(case: Case, arts: Artifacts, mode: Mode = "hybrid") -> list[Failure]:
    out = []
    lines = [ln for ln in load_chat(arts.chat) if ln.line > 1]
    pack = get_pack(case.lang)

    prev = None
    for ln in lines:
        if ln.t is None:
            continue
        if prev is not None and ln.t < prev.t:
            out.append(Failure("contradiction", "chat", "time_order", {"line": ln.line, "prev": prev.line},
                               f"chat.txt:{ln.line} time {chat_time(ln.t)} is earlier than "
                               f"chat.txt:{prev.line} time {chat_time(prev.t)}"))
        prev = ln

    for ln in lines:
        if ln.sender is None:
            continue
        n = sum(norm(ln.sender) in {norm(a) for a in p.aliases} for p in case.people)
        if n != 1:
            out.append(Failure("contradiction", "chat", "alias_unresolved",
                               {"line": ln.line, "sender": ln.sender, "count": n},
                               f"chat.txt:{ln.line} sender {ln.sender!r} resolves to {n} people"))

    if mode == "hybrid":
        allowed_lines = {a.line for a in case.chat_anchors}

        def is_allowed(ln) -> bool:
            return ln.line in allowed_lines
    else:
        anchor_texts = [norm(a.message.text) for a in case.chat_anchors]

        def is_allowed(ln) -> bool:
            return any(t in norm(ln.text) for t in anchor_texts)

    for ln in lines:
        if ln.sender is not None and pack.triggers["instruction"].search(norm(ln.text)) and not is_allowed(ln):
            out.append(Failure("contradiction", "chat", "trigger_in_filler", {"line": ln.line},
                               f"chat.txt:{ln.line} matches the instruction phrase but is not the instruction line"))
    return out
