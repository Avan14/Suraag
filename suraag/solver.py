"""Rule-based solver: answers each question from the artifacts and the student brief only.

It never receives the Case, so it cannot read the answer key. If it reproduces the key, the
case is solvable from what a student actually sees. (It proves the case is consistent with
the templates; human solvability is shown separately by the blind solve and the playtest.)

Reading rules, each one needed by a practice level (suraag/levels.py) and silent on level 1:
- a line that defines a code ('when anyone writes "<phrase>", delete ...') is a rule, not the order;
  a later line containing the phrase is the order;
- with several orders, the one carried out is the last one before the mule's confirmation;
- a sender with no saved contact is linked to the one answered call in the minutes before an order that
  says it follows a call;
- the photo time is EXIF DateTimeOriginal read in the camera's own zone (OffsetTimeOriginal), then IST.

shortcut_answers() is the opposite: what a hurried reader answers. verify.check_depth requires each
level's shortcut to give a wrong answer, which is what makes the level deeper than level 1.
"""
import re
from datetime import datetime, timedelta

from suraag.geo import haversine_m  # noqa: F401  (re-exported)
from suraag.lang import LangPack, get_pack
from suraag.model import IST, Brief, Lang, question_about
from suraag.norm import norm
from suraag.parse import Artifacts, CallRow, ChatLine, load_calls, load_chat, load_exif
from suraag.timefmt import parse_exif_ts, tz_of

UNSOLVABLE = "UNSOLVABLE"
PLACE_RADIUS_M = 500
CALL_WINDOW_MIN = 2  # the cases' tolerance: an order "after the call" comes within this many minutes
_QUOTED = re.compile(r'"([^"]+)"')


def _is_def(ln: ChatLine, pack: LangPack) -> bool:
    return bool(pack.triggers["code_def"].search(norm(ln.text)))


def instruction_candidates(lines: list[ChatLine], pack: LangPack) -> list[ChatLine]:
    """Lines that order a deletion: the instruction phrase or a defined code phrase, minus the defining lines."""
    codes = [norm(c) for ln in lines if _is_def(ln, pack) for c in _QUOTED.findall(ln.text)]
    return [ln for ln in lines if not _is_def(ln, pack)
            and (pack.triggers["instruction"].search(norm(ln.text)) or any(c in norm(ln.text) for c in codes))]


def instruction_line(lines: list[ChatLine], pack: LangPack) -> ChatLine | None:
    cands = instruction_candidates(lines, pack)
    if len(cands) == 1:
        return cands[0]
    done = next((ln for ln in lines if pack.triggers["confirm"].search(norm(ln.text))), None)
    before = [c for c in cands if done is not None and c.line < done.line]
    return before[-1] if before else None


def _suspect(numbers: set[str], brief: Brief) -> str:
    match = [s.id for s in brief.suspects if len(numbers) == 1 and s.phone in numbers]
    return match[0] if match else UNSOLVABLE


def caller(order: ChatLine, calls: list[CallRow], brief: Brief, pack: LangPack) -> str:
    numbers = {r.number for r in calls if norm(r.contact_name) == norm(order.sender)}
    if not numbers and pack.triggers["call_ref"].search(norm(order.text)):
        numbers = {r.number for r in calls if r.direction != "missed"
                   and timedelta(0) <= order.t - r.t <= timedelta(minutes=CALL_WINDOW_MIN)}
    return _suspect(numbers, brief)


def photo_time(exif: dict[str, str]) -> str:
    try:
        zone = tz_of(exif.get("OffsetTimeOriginal") or exif["OffsetTime"])
        t = datetime.strptime(exif["DateTimeOriginal"].strip(), "%Y:%m:%d %H:%M:%S").replace(tzinfo=zone)
    except (KeyError, ValueError, IndexError):
        return UNSOLVABLE  # without the camera's zone the clock time cannot be placed
    return t.astimezone(IST).isoformat()


def photo_place(exif: dict[str, str], brief: Brief) -> str:
    try:
        lat, lon = float(exif["GPSLatitude"]), float(exif["GPSLongitude"])
    except (KeyError, ValueError):
        return UNSOLVABLE
    dist, place = min((haversine_m(lat, lon, p.lat, p.lon), p.id) for p in brief.places)
    return place if dist <= PLACE_RADIUS_M else UNSOLVABLE


def _read(arts: Artifacts) -> tuple[list[ChatLine], list[CallRow], dict[str, str]]:
    lines = [ln for ln in load_chat(arts.chat) if ln.sender is not None]
    return lines, load_calls(arts.calls), load_exif(arts.photo) if arts.photo is not None else {}


def solve(arts: Artifacts, brief: Brief, lang: Lang) -> dict[str, str]:
    pack = get_pack(lang)
    lines, calls, exif = _read(arts)
    order = instruction_line(lines, pack)
    out: dict[str, str] = {}
    for q in brief.questions:
        if question_about(q) == "photo":
            out[q.id] = photo_time(exif) if q.kind == "when" else photo_place(exif, brief)
        elif order is None:  # no order, or several and no confirmation to tell them apart
            out[q.id] = UNSOLVABLE
        elif q.kind == "when":
            out[q.id] = order.t.isoformat()
        else:
            out[q.id] = caller(order, calls, brief, pack)
    return out


def shortcut_answers(arts: Artifacts, brief: Brief, lang: Lang) -> dict[str, tuple[str | None, str]]:
    """twist -> (question id, the answer a hurried reader gives). Each shortcut skips exactly one rule above."""
    pack = get_pack(lang)
    lines, calls, exif = _read(arts)
    qid = {f"{question_about(q)}:{q.kind}": q.id for q in brief.questions}

    def by_saved_name(sender: str, first_word: bool = False) -> str:
        key = (lambda s: norm(s).split()[0]) if first_word else norm
        return _suspect({r.number for r in calls if norm(r.contact_name) and key(r.contact_name) == key(sender)}, brief)

    order = instruction_line(lines, pack)
    phrase = [ln for ln in lines if pack.triggers["instruction"].search(norm(ln.text))]
    cands = instruction_candidates(lines, pack)
    named = [p.id for ln in lines for p in brief.places if norm(p.name) in norm(ln.text)]
    try:
        exif_as_ist = parse_exif_ts(exif["DateTimeOriginal"]).isoformat()
    except (KeyError, ValueError):
        exif_as_ist = UNSOLVABLE
    return {
        # the order's sender is not saved, so match the first word of the name ("Raju bhai" ~ "Raju B.")
        "unsaved_caller": (qid.get("instruction:who"), by_saved_name(order.sender, True) if order else UNSOLVABLE),
        # search for the word "delete" and take the first hit, which is the line that sets up the code
        "code_word": (qid.get("instruction:when"), phrase[0].t.isoformat() if phrase else UNSOLVABLE),
        # take the latest request to delete an entry, ignoring the confirmation that came before it
        "decoy": (qid.get("instruction:who"), by_saved_name(cands[-1].sender) if cands else UNSOLVABLE),
        # believe the place the chat names
        "alibi": (qid.get("photo:where"), named[-1] if named else UNSOLVABLE),
        # read the EXIF clock as if it were IST
        "camera_clock": (qid.get("photo:when"), exif_as_ist),
    }
