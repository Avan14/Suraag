"""Worked solutions, built in code from the case model and the files, never by the LLM.

For each question: the reasoning steps in order, each naming the exact line it rests on; the answer; and the
traps the level sets for it. A trap is only shown if solver.shortcut_answers really gives a wrong answer for
it on these files (the same computation verify.check_depth runs), so every trap a student reads is real.
Shown to a student after they submit, and written to solution.md (instructor material) by the pipeline.
"""
from dataclasses import dataclass
from datetime import datetime, timedelta

from suraag.geo import haversine_m
from suraag.grade import answer_matches
from suraag.i18n import t
from suraag.model import Case, question_about
from suraag.parse import Artifacts, load_exif
from suraag.solver import UNSOLVABLE, shortcut_answers
from suraag.timefmt import chat_time, csv_hm, tz_of

IST_SHIFT = timedelta(hours=5, minutes=30)


@dataclass(frozen=True)
class Walk:
    question_id: str
    steps: tuple[str, ...]
    answer: str
    traps: tuple[str, ...]


def _shift(d: timedelta) -> str:
    m = int(d.total_seconds() // 60)
    return f"{'+' if m >= 0 else '-'}{abs(m) // 60} h {abs(m) % 60:02d} min"


def walkthrough(case: Case, arts: Artifacts, lang: str = "en") -> list[Walk]:
    w = lambda key, **kw: t(f"walk.{key}", lang, **kw)  # noqa: E731
    role = {p.role: p for p in case.people}
    boss, distr = role["boss"], role["distractor"]
    name = {p.id: p.name for p in case.people} | {p.id: p.name for p in case.places}
    said = {a.line: a.message for a in case.chat_anchors}
    line_of = lambda fid: next(a.line for a in case.fact(fid).anchors if a.artifact == "chat")  # noqa: E731
    has = lambda tw: tw in case.twists  # noqa: E731

    # who / when: the chain that finds the order, then the call that ties it to a number
    order_line = line_of("F1")
    order = said[order_line]
    call_row = next(a.row for a in case.fact("F1").anchors if a.artifact == "calls")
    call = next(r for r in case.calls if r.row == call_row)
    chain = []
    if has("code_word"):
        code = case.fact("F2").anchors[0].must_contain[1]
        chain.append(w("code_def", loc=f"chat.txt:{line_of('F2')}", sender=said[line_of("F2")].sender, code=code))
        chain.append(w("order_code", loc=f"chat.txt:{order_line}", time=chat_time(order.t), sender=order.sender,
                       text=order.text, code=code))
    else:
        chain.append(w("order", loc=f"chat.txt:{order_line}", time=chat_time(order.t), sender=order.sender, text=order.text))
    if has("decoy"):
        reply = said[line_of("F5")]
        chain.append(w("confirm", loc=f"chat.txt:{line_of('F5')}", text=reply.text, time=chat_time(reply.t)))
        chain.append(w("decoy_out", loc=f"chat.txt:{line_of('F10')}"))
    if call.contact_name:
        link = w("call_saved", loc=f"calls.csv:{call_row}", alias=order.sender, phone=call.number, hm=csv_hm(call.t))
    else:
        link = w("call_unsaved", loc=f"calls.csv:{call_row}", alias=order.sender, tol=case.tolerance_minutes,
                 phone=call.number)
    first = boss.name.split()[0]
    namesake = [w("namesake", first=first)] if sum(s.name.split()[0] == first for s in case.brief.suspects) > 1 else []
    who = chain + [link, w("suspect", phone=boss.phone, name=boss.name)] + namesake
    when = chain + [w("when_call", loc=f"calls.csv:{call_row}", hm=csv_hm(call.t), tol=case.tolerance_minutes)]

    # where: the GPS and the nearest place
    exif = load_exif(arts.photo) if arts.photo is not None else {}
    where, photo_time, shift = [], [], timedelta(0)
    if "GPSLatitude" in exif and "GPSLongitude" in exif:
        lat, lon = float(exif["GPSLatitude"]), float(exif["GPSLongitude"])
        (d1, p1), (d2, p2) = sorted((haversine_m(lat, lon, p.lat, p.lon), p.name) for p in case.places)[:2]
        where = [w("gps", loc="photo.jpg:GPSLatitude, photo.jpg:GPSLongitude", lat=exif["GPSLatitude"],
                   lon=exif["GPSLongitude"]),
                 w("nearest", d=round(d1), place=p1, place2=p2, d2=f"{d2 / 1000:.1f}")]
    if has("alibi"):
        where.append(w("alibi", loc=f"chat.txt:{line_of('F11')}", other=case.fact("F11").anchors[0].must_contain[1]))
    # photo time: the camera clock in its own zone, moved to IST
    if case.photo is not None and "DateTimeOriginal" in exif:
        shift = IST_SHIFT - tz_of(case.photo.offset).utcoffset(None)
        local = datetime.strptime(exif["DateTimeOriginal"], "%Y:%m:%d %H:%M:%S")
        photo_time = [w("dto", loc="photo.jpg:DateTimeOriginal", local=exif["DateTimeOriginal"]),
                      w("offset", loc="photo.jpg:OffsetTimeOriginal", offset=case.photo.offset),
                      w("convert", shift=_shift(shift), local_hm=f"{local:%H:%M}", ist=chat_time(case.photo.t))]

    # traps: only the ones the shortcut reader really falls into on these files
    traps: dict[str, list[str]] = {}
    short = shortcut_answers(arts, case.brief, case.lang)
    for tw in case.twists:
        qid, got = short[tw]
        q = next((x for x in case.questions if x.id == qid), None)
        if q is None or got == UNSOLVABLE or answer_matches(case, q, got):
            continue
        params = {
            "unsaved_caller": lambda: {"decoy_alias": distr.saved_as, "alias": order.sender, "got": name[got]},
            "code_word": lambda: {"loc": f"chat.txt:{line_of('F2')}", "got": chat_time(datetime.fromisoformat(got))},
            "decoy": lambda: {"loc": f"chat.txt:{line_of('F10')}", "got": name[got]},
            "alibi": lambda: {"loc": f"chat.txt:{line_of('F11')}", "got": name[got]},
            "camera_clock": lambda: {"got": chat_time(datetime.fromisoformat(got)), "shift": _shift(shift)[1:]},
        }[tw]()
        traps.setdefault(qid, []).append(w(f"trap.{tw}", **params))

    out = []
    for q in case.questions:
        if question_about(q) == "photo":
            steps, answer = (photo_time, chat_time(case.photo.t)) if q.kind == "when" else (where, name[q.answer])
        else:
            steps, answer = (when, chat_time(order.t)) if q.kind == "when" else (who, name[q.answer])
        out.append(Walk(q.id, tuple(steps), answer, tuple(traps.get(q.id, []))))
    return out


def solution_markdown(case: Case, arts: Artifacts, lang: str = "en") -> str:
    """The instructor's worked solution for one case. Contains the answers: never hand it to students."""
    texts = {q.id: q.text for q in case.questions}
    parts = [f"# Case {case.case_id}: worked solution (instructor copy)", "",
             "> SYNTHETIC CASE - fictional, for teaching only. Not real data. This file contains the answers.", "",
             f"{t(f'level.{case.level}.name', lang)}. {t(f'level.{case.level}.skills', lang)}"]
    for wk in walkthrough(case, arts, lang):
        parts += ["", f"## {wk.question_id}. {texts[wk.question_id]}", ""]
        parts += [f"{i}. {s}" for i, s in enumerate(wk.steps, 1)]
        parts += ["", f"**{t('walk.answer', lang, answer=wk.answer)}**"]
        parts += [""] + [f"- {x}" for x in wk.traps] if wk.traps else []
    return "\n".join(parts) + "\n"
