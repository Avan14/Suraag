"""Rule-based solver: answers each question from the artifacts and the student brief only.

It never receives the Case, so it cannot read the answer key. If it reproduces the key, the
case is solvable from what a student actually sees. (It proves the case is consistent with
the templates; human solvability is shown separately by the blind solve and the playtest.)
"""
from suraag.geo import haversine_m  # noqa: F401  (re-exported)
from suraag.lang import get_pack
from suraag.model import Brief, Lang
from suraag.norm import norm
from suraag.parse import Artifacts, load_calls, load_chat, load_exif

UNSOLVABLE = "UNSOLVABLE"
PLACE_RADIUS_M = 500


def solve(arts: Artifacts, brief: Brief, lang: Lang) -> dict[str, str]:
    trigger = get_pack(lang).triggers["instruction"]
    instr = [ln for ln in load_chat(arts.chat) if ln.sender is not None and trigger.search(norm(ln.text))]
    calls = load_calls(arts.calls)
    exif = load_exif(arts.photo) if arts.photo is not None else {}

    out: dict[str, str] = {}
    for q in brief.questions:
        if q.kind in ("who", "when"):
            if len(instr) != 1:  # none, or ambiguous
                out[q.id] = UNSOLVABLE
            elif q.kind == "when":
                out[q.id] = instr[0].t.isoformat()
            else:
                numbers = {r.number for r in calls if norm(r.contact_name) == norm(instr[0].sender)}
                match = [s.id for s in brief.suspects if len(numbers) == 1 and s.phone in numbers]
                out[q.id] = match[0] if match else UNSOLVABLE
        else:  # where
            try:
                lat, lon = float(exif["GPSLatitude"]), float(exif["GPSLongitude"])
            except (KeyError, ValueError):
                out[q.id] = UNSOLVABLE
                continue
            dist, place = min((haversine_m(lat, lon, p.lat, p.lon), p.id) for p in brief.places)
            out[q.id] = place if dist <= PLACE_RADIUS_M else UNSOLVABLE
    return out
