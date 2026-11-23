"""Tiered hints built from the case model in code, never by the LLM.

Tier 1 names the files, tier 2 the rows or lines to look at, tier 3 the exact locations. A hint
never contains the culprit's name or aliases, an anchor's evidence strings, or a line's text.
A persona only wraps the hint in a short fixed line; Plain returns the bare hint.
"""
from suraag.grade import FILES
from suraag.i18n import t
from suraag.model import Case

TIERS = 3
PERSONAS = ("plain", "vetaal", "birbal")
# Read-aloud settings per persona: speed and pitch only. No imitation of any real person's voice.
SPEECH = {"plain": {"rate": 1.0, "pitch": 1.0}, "vetaal": {"rate": 0.85, "pitch": 0.7},
          "birbal": {"rate": 0.95, "pitch": 1.1}}


def _anchors(case: Case, question_id: str):
    q = next(x for x in case.questions if x.id == question_id)
    return [a for fid in q.answer_facts for a in case.fact(fid).anchors]


def _join(parts: list[str]) -> str:
    return ", ".join(dict.fromkeys(parts))  # order kept, duplicates dropped


def base_hint(case: Case, question_id: str, tier: int, lang: str = "en") -> str:
    if tier not in range(1, TIERS + 1):
        raise ValueError(f"tier must be 1 to {TIERS}")
    anchors = _anchors(case, question_id)
    if tier == 1:
        files = _join([FILES[a.artifact] for a in anchors])
        return t("hint.t1", lang, files=files)
    if tier == 2:
        pieces = []
        for art in dict.fromkeys(a.artifact for a in anchors):
            mine = [a for a in anchors if a.artifact == art]
            if art == "chat":
                line = mine[0].line
                pieces.append(t("hint.where.chat", lang, a=max(2, line - 3), b=min(case.chat_length, line + 3)))
            elif art == "calls":
                rows = [r.row for r in case.calls]
                pieces.append(t("hint.where.calls", lang, a=max(min(rows), mine[0].row - 1),
                                b=min(max(rows), mine[0].row + 1)))
            else:
                pieces.append(t("hint.where.photo", lang, tags=", ".join(dict.fromkeys(a.exif_tag for a in mine))))
        return t("hint.t2", lang, where="; ".join(pieces))
    locs = []
    for a in anchors:
        loc = {"chat": a.line, "calls": a.row, "photo": a.exif_tag}[a.artifact]
        locs.append(f"{FILES[a.artifact]}:{loc}")
    return t("hint.t3", lang, locs=_join(locs))


def hint(case: Case, question_id: str, tier: int, lang: str = "en", persona: str = "plain") -> str:
    if persona not in PERSONAS:
        raise ValueError(f"unknown persona {persona!r}")
    body = base_hint(case, question_id, tier, lang)
    return t(f"hint.persona.{persona}.pre", lang) + body + t(f"hint.persona.{persona}.post", lang)
