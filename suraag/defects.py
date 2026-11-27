"""Plants the 4 defect types for the demo and the evaluation.

Defects edit the rendered files, never the world model, so a repair can always re-render a
clean artifact from the model.
"""
import csv
import io
from dataclasses import replace
from datetime import timedelta
from typing import Callable, Literal

from suraag.model import Case
from suraag.norm import norm
from suraag.parse import Artifacts, load_chat
from suraag.timefmt import chat_ts, csv_ts, parse_csv_ts

DefectKind = Literal["timestamp_clash", "alias_conflict", "missing_anchor", "unsolvable_question"]
# The failure code each defect must trigger. A defect may trigger others too; this one is required.
EXPECTED: dict[str, str] = {"timestamp_clash": "cross_time", "alias_conflict": "alias_unresolved",
                            "missing_anchor": "anchor_missing", "unsolvable_question": "solver_mismatch"}


def _edit_calls(text: str, fn: Callable[[list[str]], list[str]]) -> str:
    sep = "\r\n" if "\r\n" in text else "\n"
    out = []
    for line in text.split(sep):
        if not line or line.startswith("#") or line.startswith('"row"') or line.startswith("row,"):
            out.append(line)
            continue
        buf = io.StringIO()
        csv.writer(buf, lineterminator="", quoting=csv.QUOTE_ALL).writerow(fn(next(csv.reader([line]))))
        out.append(buf.getvalue())
    return sep.join(out)


def _rewrite_chat_line(chat: str, line: int, *, sender: str | None = None, ts: str | None = None) -> str:
    lines = chat.split("\n")
    ln = load_chat(chat)[line - 1]
    lines[line - 1] = f"{ts or ln.raw.partition(' - ')[0]} - {sender if sender is not None else ln.sender}: {ln.text}"
    return "\n".join(lines)


def inject(case: Case, arts: Artifacts, kind: DefectKind, *,
           target: Literal["chat", "calls"] = "chat") -> Artifacts:
    boss = next(p for p in case.people if p.role == "boss")
    anchor_lines = {a.line for a in case.chat_anchors}
    if kind == "timestamp_clash":
        shift = timedelta(minutes=case.tolerance_minutes + 4)
        fact = next(f for f in case.facts if {"chat", "calls"} <= {a.artifact for a in f.anchors})
        if target == "chat":
            line = next(a.line for a in fact.anchors if a.artifact == "chat")
            ln = load_chat(arts.chat)[line - 1]
            return replace(arts, chat=_rewrite_chat_line(arts.chat, line, ts=chat_ts(ln.t + shift)))
        row = next(a.row for a in fact.anchors if a.artifact == "calls")
        return replace(arts, calls=_edit_calls(
            arts.calls, lambda r: [r[0], csv_ts(parse_csv_ts(r[1]) + shift)] + r[2:] if int(r[0]) == row else r))
    if kind == "alias_conflict":
        token = boss.saved_as.split()[0]
        aliases = {norm(a) for p in case.people for a in p.aliases}
        while norm(token) in aliases:  # make sure the sender really matches nobody
            token = token[:-1] or "x"
        line = next(ln.line for ln in load_chat(arts.chat) if ln.line > 1 and ln.line not in anchor_lines and ln.sender)
        return replace(arts, chat=_rewrite_chat_line(arts.chat, line, sender=token))
    if kind == "missing_anchor":
        line = next(a.line for a in case.chat_anchors if a.message.sender == boss.saved_as)  # the order line
        other = next(case.person(p).saved_as for p in case.chat_members if case.person(p).id != boss.id)
        return replace(arts, chat=_rewrite_chat_line(arts.chat, line, sender=other))
    if kind == "unsolvable_question":
        # No saved name and no answered call: nothing links the order to a number, on any level.
        return replace(arts, calls=_edit_calls(
            arts.calls, lambda r: [r[0], r[1], "missed", r[3], "", "0"] if r[3] == boss.phone else r))
    raise ValueError(f"unknown defect {kind!r}")
