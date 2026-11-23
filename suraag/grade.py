"""Deterministic grader: answer + citation points per question. The overclaim check is advisory only.

Scoring (decided with the user):
- Answer point: the structured answer matches the key (a time within the case tolerance).
- Citation point, all-or-nothing: every artifact the question's facts are anchored in has at least
  one VALID cited line, and no cited line is WRONG. Extra lines that genuinely support the fact are
  fine, even if they are not the designated anchor. A PARTIAL line (some but not all of the needed
  strings) neither earns nor costs, and the feedback names what is missing.
Explanations come from the verifier's own data as (code, params) pairs; i18n renders them.
The same input always gives the same score. Nothing here calls an LLM unless a classifier is passed in.
"""
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Literal

from suraag.model import ArtifactName, Case, Question
from suraag.norm import norm
from suraag.parse import Artifacts, text_at
from suraag.timefmt import parse_chat_ts

FILES = {"chat": "chat.txt", "calls": "calls.csv", "photo": "photo.jpg"}


@dataclass(frozen=True)
class Citation:
    artifact: ArtifactName
    line: int | None = None
    row: int | None = None
    exif_tag: str | None = None

    @property
    def label(self) -> str:
        loc = {"chat": self.line, "calls": self.row, "photo": self.exif_tag}[self.artifact]
        return f"{FILES[self.artifact]}:{loc}"


@dataclass(frozen=True)
class Claim:
    question_id: str
    answer: str
    citations: tuple[Citation, ...] = ()
    rationale: str = ""


@dataclass(frozen=True)
class Expl:
    code: str
    params: dict = field(default_factory=dict)


@dataclass(frozen=True)
class CitationMark:
    citation: Citation
    label: Literal["valid", "partial", "wrong"]


@dataclass(frozen=True)
class ClaimResult:
    question_id: str
    answer_correct: bool
    citation_valid: bool
    points: int
    marks: tuple[CitationMark, ...]
    explanations: tuple[Expl, ...]
    rationale_flag: str | None  # None, "could_not_verify", "overclaim" or "ok": advisory, never scored


def _anchor_loc(a) -> str:
    loc = {"chat": a.line, "calls": a.row, "photo": a.exif_tag}[a.artifact]
    return f"{FILES[a.artifact]}:{loc}"


_HM = re.compile(r"^(\d{1,2}):(\d{2})$")


def _parse_time(answer: str, ref: datetime) -> datetime | None:
    """Accept ISO with offset, 24-hour HH:MM, or h:mm am/pm; a bare time uses the key's date."""
    s = answer.strip()
    try:
        t = datetime.fromisoformat(s)
        return t if t.tzinfo else None
    except ValueError:
        pass
    m = _HM.match(s)
    if m and int(m[1]) < 24 and int(m[2]) < 60:
        return ref.replace(hour=int(m[1]), minute=int(m[2]), second=0, microsecond=0)
    try:
        t = parse_chat_ts(f"{ref:%d/%m/%y}, {s}")
        return t
    except ValueError:
        return None


def answer_matches(case: Case, q: Question, answer: str) -> bool:
    if q.kind == "when":
        key = datetime.fromisoformat(q.answer)
        given = _parse_time(answer, key)
        return given is not None and abs((given - key).total_seconds()) / 60 <= case.tolerance_minutes
    return norm(answer) == norm(q.answer)


def rationale_flag(rationale: str, *, classify: Callable[[str], str] | None = None) -> str | None:
    """Advisory only. Without a classifier, free text is always 'could_not_verify' (flagged for the
    instructor, never silently scored). A classifier may answer 'ok' or 'overclaim'; anything else
    or any failure falls back to 'could_not_verify'."""
    if not rationale.strip():
        return None
    if classify is None:
        return "could_not_verify"
    try:
        verdict = classify(rationale)
    except Exception:
        return "could_not_verify"
    return verdict if verdict in ("ok", "overclaim") else "could_not_verify"


def grade_claim(case: Case, arts: Artifacts, claim: Claim, *,
                classify: Callable[[str], str] | None = None) -> ClaimResult:
    q = next(x for x in case.questions if x.id == claim.question_id)
    anchors = [a for fid in q.answer_facts for a in case.fact(fid).anchors]
    expls: list[Expl] = []

    correct = answer_matches(case, q, claim.answer)
    expls.append(Expl("answer_ok" if correct else "answer_wrong", {"question": q.id}))

    marks: list[CitationMark] = []
    wrong = False
    for c in claim.citations:
        same = [a for a in anchors if a.artifact == c.artifact]
        if not same:
            marks.append(CitationMark(c, "wrong"))
            expls.append(Expl("cite_irrelevant", {"loc": c.label, "artifact": FILES[c.artifact]}))
            wrong = True
            continue
        text = text_at(arts, c.artifact, line=c.line, row=c.row, exif_tag=c.exif_tag)
        if text is None:
            marks.append(CitationMark(c, "wrong"))
            expls.append(Expl("cite_nonexistent", {"loc": c.label}))
            wrong = True
            continue
        have = norm(text)
        if any(all(norm(m) in have for m in a.must_contain) for a in same):
            marks.append(CitationMark(c, "valid"))
            expls.append(Expl("cite_valid", {"loc": c.label}))
            continue
        support = _anchor_loc(same[0])
        best = max(same, key=lambda a: sum(norm(m) in have for m in a.must_contain))
        present = [m for m in best.must_contain if norm(m) in have]
        if present:
            marks.append(CitationMark(c, "partial"))
            expls.append(Expl("cite_partial", {"loc": c.label, "has": present,
                                               "missing": [m for m in best.must_contain if m not in present],
                                               "support": support}))
        else:
            marks.append(CitationMark(c, "wrong"))
            expls.append(Expl("cite_wrong", {"loc": c.label, "needles": list(best.must_contain), "support": support}))
            wrong = True

    covered = {m.citation.artifact for m in marks if m.label == "valid"}
    missing_art = []
    for art in dict.fromkeys(a.artifact for a in anchors):  # required artifacts, in anchor order
        if art not in covered:
            missing_art.append(art)
            expls.append(Expl("cite_missing_artifact", {"artifact": FILES[art],
                                                        "support": _anchor_loc(next(a for a in anchors if a.artifact == art))}))
    cited = not wrong and not missing_art
    return ClaimResult(q.id, correct, cited, int(correct) + int(cited), tuple(marks), tuple(expls),
                       rationale_flag(claim.rationale, classify=classify))


def grade_all(case: Case, arts: Artifacts, claims: list[Claim], *,
              classify: Callable[[str], str] | None = None) -> list[ClaimResult]:
    """One result per question in key order; an unanswered question scores zero."""
    by_q = {c.question_id: c for c in claims}
    return [grade_claim(case, arts, by_q.get(q.id, Claim(q.id, "")), classify=classify) for q in case.questions]
