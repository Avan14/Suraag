"""Deterministic checks -> list of failures. Plain code only; an LLM never verifies.
Six checks on every case, plus a depth check on practice levels 2-4 (each trap must really mislead)."""
from dataclasses import dataclass
from typing import Literal

from suraag.fillerrules import filler_violation
from suraag.i18n import t
from suraag.lang import get_pack
from suraag.model import Anchor, Case, question_about
from suraag.norm import norm
from suraag.parse import Artifacts, load_calls, load_chat, load_exif, text_at
from suraag.timefmt import chat_time

Mode = Literal["hybrid", "raw"]
FILES = {"chat": "chat.txt", "calls": "calls.csv", "photo": "photo.jpg"}


@dataclass(frozen=True)
class Failure:
    check: Literal["anchor", "traceability", "contradiction", "solvability", "distractor", "filler_count", "depth"]
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
                    out.append(Failure("anchor", a.artifact, "anchor_missing", {"fact": fact.id, "file": FILES[a.artifact], "wanted": wanted},
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
            out.append(Failure("contradiction", "chat", "time_order", {"line": ln.line, "prev": prev.line, "t": chat_time(ln.t), "prev_t": chat_time(prev.t)},
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

    if mode == "hybrid":  # rule L-09: filler adds no facts (raw mode is the baseline and is not held to it)
        for ln in lines:
            reason = filler_violation(ln.text) if ln.sender is not None and ln.line not in allowed_lines else None
            if reason:
                out.append(Failure("contradiction", "chat", "filler_content", {"line": ln.line, "reason": reason},
                                   f"chat.txt:{ln.line} filler contains {t('filler.reason.' + reason, 'en')}"))
    from suraag.solver import instruction_candidates
    said = [ln for ln in lines if ln.sender is not None]
    orders = {ln.line for ln in instruction_candidates(said, pack)}  # the instruction phrase, or a defined code phrase
    cues = {ln.line for ln in said if any(pack.triggers[k].search(norm(ln.text)) for k in ("code_def", "confirm"))}
    for ln in said:
        if is_allowed(ln):
            continue
        if ln.line in orders:
            out.append(Failure("contradiction", "chat", "trigger_in_filler", {"line": ln.line},
                               f"chat.txt:{ln.line} matches the instruction phrase but is not the instruction line"))
        elif ln.line in cues:
            out.append(Failure("contradiction", "chat", "cue_in_filler", {"line": ln.line},
                               f"chat.txt:{ln.line} reads like a code rule or a confirmation but is not one"))
    return out


def check_traceability(case: Case) -> list[Failure]:
    out = []
    for f in case.facts:
        if not f.anchors:
            out.append(Failure("traceability", "model", "fact_no_anchor", {"fact": f.id},
                               f"{f.id} has no anchor in any artifact"))
    for q in case.questions:
        if not q.answer_facts:
            out.append(Failure("traceability", "model", "question_no_fact", {"question": q.id},
                               f"{q.id} does not map to any fact"))
    return out


def check_cross_time(case: Case, arts: Artifacts) -> list[Failure]:
    """The chat time and call-log time of the same fact must agree within the tolerance.
    Compared as real datetimes read back from the artifacts, so a window that spans midnight works."""
    out = []
    chat_lines = load_chat(arts.chat)
    calls = {r.row: r for r in load_calls(arts.calls)}
    for f in case.facts:
        ca = next((a for a in f.anchors if a.artifact == "chat"), None)
        ra = next((a for a in f.anchors if a.artifact == "calls"), None)
        if not (ca and ra and 1 <= ca.line <= len(chat_lines) and ra.row in calls):
            continue  # a missing location is the anchor check's finding
        chat_t, call_t = chat_lines[ca.line - 1].t, calls[ra.row].t
        if chat_t is None:
            continue
        diff = abs((chat_t - call_t).total_seconds()) / 60
        if diff > case.tolerance_minutes:
            out.append(Failure(
                "contradiction", "chat", "cross_time",
                {"fact": f.id, "chat_line": ca.line, "row": ra.row, "chat_t": chat_time(chat_t),
                 "call_t": f"{call_t:%H:%M}", "diff": diff, "tol": case.tolerance_minutes},
                f"{f.id}: chat.txt:{ca.line} at {chat_time(chat_t)} vs calls.csv row {ra.row} at "
                f"{call_t:%H:%M} differs by {diff:g} min (tolerance {case.tolerance_minutes})"))
    return out


def check_causality(case: Case) -> list[Failure]:
    by_id = {e.id: e for e in case.timeline}
    return [Failure("contradiction", "model", "cause_after_effect", {"event": e.id, "cause": d},
                    f"{e.id} happens before its cause {d}")
            for e in case.timeline for d in e.depends_on if by_id[d].t > e.t]


def check_solvability(case: Case, arts: Artifacts) -> list[Failure]:
    from suraag.solver import solve
    solved = solve(arts, case.brief, case.lang)
    artifact = lambda q: "photo" if question_about(q) == "photo" else {"who": "calls", "when": "chat"}[q.kind]  # noqa: E731
    return [Failure("solvability", artifact(q), "solver_mismatch", {"question": q.id, "got": solved.get(q.id), "key": q.answer},
                    f"{q.id}: solver answered {solved.get(q.id)}, key is {q.answer}")
            for q in case.questions if solved.get(q.id) != q.answer]


def _tokens(person) -> set[str]:
    return {t for a in person.aliases for t in norm(a).split() if len(t) >= 3}


def check_distractor(case: Case, arts: Artifacts) -> list[Failure]:
    if not case.distractors:
        return [Failure("distractor", "model", "no_distractor", {}, "the case has no distractor fact")]
    from suraag.solver import solve
    out = []
    key = next((e for e in case.timeline if e.kind == "instruction"), None)
    who = next((q for q in case.questions if q.kind == "who"), None)
    answer_person = case.person(who.answer) if who else None
    solved = solve(arts, case.brief, case.lang)
    for fid in case.distractors:
        event = next(e for e in case.timeline if e.id == case.fact(fid).event)
        actor = case.person(event.actor)
        near = key is not None and abs((event.t - key.t).total_seconds()) <= 30 * 60
        similar = answer_person is not None and bool(_tokens(actor) & _tokens(answer_person))
        if not (near or similar):
            out.append(Failure("distractor", "model", "distractor_implausible", {"fact": fid},
                               f"{fid} is not plausible: far from the key event and no similar alias"))
        if who and solved.get(who.id) == actor.id and actor.id != who.answer:
            out.append(Failure("distractor", "calls", "solver_picked_distractor", {"fact": fid, "actor": actor.id, "question": who.id},
                               f"the solver picked the distractor {actor.id} for {who.id}"))
    return out


# The file a broken trap is repaired in: chat traps by regenerating the filler, the others are rendered from the model.
TWIST_ARTIFACT = {"unsaved_caller": "calls", "alibi": "chat", "code_word": "chat", "decoy": "chat", "camera_clock": "photo"}


def check_depth(case: Case, arts: Artifacts) -> list[Failure]:
    """Each twist's shortcut must give a real, wrong answer (not the key, not 'unsolvable'): a trap that does
    not mislead makes the level no deeper than level 1."""
    if not case.twists:
        return []
    from suraag.grade import answer_matches
    from suraag.solver import UNSOLVABLE, shortcut_answers
    short = shortcut_answers(arts, case.brief, case.lang)
    out = []
    for tw in case.twists:
        qid, got = short[tw]
        q = next((x for x in case.questions if x.id == qid), None)
        if q is None or got == UNSOLVABLE or answer_matches(case, q, got):
            out.append(Failure("depth", TWIST_ARTIFACT[tw], "trap_not_set", {"twist": tw, "question": qid, "got": got},
                               f"twist {tw}: a shortcut reader answers {got} for {qid}, which is not a plausible "
                               f"wrong answer"))
    return out


def check_insufficient_alone(case: Case, arts: Artifacts) -> list[Failure]:
    """Rule L-05: the answer must rest on the anchored lines. Remove every chat line and call row that a who/when
    answer is anchored in, keep everything else (distractors, decoys, filler), and the solver must no longer
    reach the key. Photo questions rest on single EXIF tags, so there is no "everything else" to test them on."""
    from suraag.solver import solve
    out = []
    for q in case.questions:
        if question_about(q) == "photo":
            continue
        anchors = [a for fid in q.answer_facts for a in case.fact(fid).anchors]
        lines = {a.line for a in anchors if a.artifact == "chat"}
        rows = {str(a.row) for a in anchors if a.artifact == "calls"}
        chat = "".join(ln for n, ln in enumerate(arts.chat.splitlines(True), start=1) if n not in lines)
        calls = "".join(ln for ln in arts.calls.splitlines(True) if ln.split(",", 1)[0] not in rows)
        got = solve(Artifacts(chat, calls, arts.photo), case.brief, case.lang).get(q.id)
        if got == q.answer:
            out.append(Failure("distractor", "chat", "anchors_not_needed", {"question": q.id, "key": q.answer},
                               f"{q.id}: the solver still answers {q.answer} with every anchored line removed"))
    return out


def verify(case: Case, arts: Artifacts, mode: Mode = "hybrid") -> list[Failure]:
    return (check_anchors(case, arts, mode) + check_traceability(case) + check_chat_consistency(case, arts, mode)
            + check_cross_time(case, arts) + check_causality(case) + check_solvability(case, arts)
            + check_distractor(case, arts) + check_insufficient_alone(case, arts) + check_depth(case, arts))
