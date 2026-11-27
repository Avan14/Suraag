"""Pydantic world model for one case (people, timeline, facts, anchors, questions, brief).

The model enforces only what must never be broken (fake phone numbers, timezone-aware times,
distinct initials, ids that point at something). Rules the verifier must be able to *fail*
(a fact with no anchor, an alias that resolves to two people) are deliberately NOT enforced here.
"""
from datetime import datetime, timedelta, timezone
from typing import Annotated, Literal

from pydantic import (AwareDatetime, BaseModel, StringConstraints, field_validator,
                      model_validator)

IST = timezone(timedelta(hours=5, minutes=30))
Lang = Literal["en", "hinglish", "hi"]
ArtifactName = Literal["chat", "calls", "photo"]
Role = Literal["boss", "mule", "victim", "witness", "distractor", "associate"]
# +91-5xxxx-xxxxx: a leading 5 is never a valid Indian mobile prefix, so these can't be real numbers.
Phone = Annotated[str, StringConstraints(pattern=r"^\+91-5\d{4}-\d{5}$")]


class Person(BaseModel):
    id: str
    name: str
    name_deva: str
    role: Role
    aliases: list[str]  # aliases[0] is the name saved in the device owner's phone
    phone: Phone

    @field_validator("aliases")
    @classmethod
    def _aliases_safe(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError("a person needs at least one alias")
        for a in v:
            if ":" in a or "\n" in a:  # would break the "<sender>: <text>" chat line format
                raise ValueError(f"alias {a!r} must not contain ':' or a newline")
        return v

    @property
    def saved_as(self) -> str:
        return self.aliases[0]

    @property
    def initials(self) -> str:
        return "".join(w[0].upper() for w in self.name.split())


class Place(BaseModel):
    id: str
    name: str
    lat: float
    lon: float


class Event(BaseModel):
    id: str
    t: AwareDatetime
    kind: Literal["transfer", "call", "instruction", "photo", "distractor_call",
                  "code_definition", "confirmation", "decoy_message", "alibi_message", "unknown_call",
                  "forwarded_message", "deposit", "payout", "control_handover", "message"]
    actor: str
    target: str | None = None
    depends_on: list[str] = []


class Anchor(BaseModel):
    artifact: ArtifactName
    line: int | None = None
    row: int | None = None
    exif_tag: str | None = None
    must_contain: list[str]

    @model_validator(mode="after")
    def _one_locator(self) -> "Anchor":
        if sum(x is not None for x in (self.line, self.row, self.exif_tag)) != 1:
            raise ValueError("an anchor needs exactly one of line, row or exif_tag")
        return self


class Fact(BaseModel):
    id: str
    claim: str
    event: str
    anchors: list[Anchor]  # may be empty here; the verifier's traceability check reports it


QuestionAbout = Literal["instruction", "photo"]
# yesno: "yes"/"no" (was the photo edited); amount: whole rupees as digits. Both come from case families.
QuestionKind = Literal["who", "when", "where", "yesno", "amount"]
Family = Literal["upi", "da", "nc", "ts", "cc"]  # see suraag/families.py
NO_ONE = "none"  # the honest answer to a "who" question when the files hold no such instruction


def question_about(q) -> str:
    """What a question asks about: 'where' and 'yesno' are the photo; other kinds default to the instruction."""
    return q.about or ("photo" if q.kind in ("where", "yesno") else "instruction")


class Question(BaseModel):
    id: str
    kind: QuestionKind
    text: str
    about: QuestionAbout | None = None  # None: the default for the kind (see question_about)
    answer_facts: list[str]
    answer: str  # who: person id or NO_ONE | when: ISO time with offset | where: place id | yesno | amount


class ChatMessage(BaseModel):
    t: AwareDatetime
    sender: str
    text: str


class ChatAnchor(BaseModel):
    line: int
    message: ChatMessage  # written verbatim by code


class CallRow(BaseModel):
    row: int
    t: AwareDatetime
    direction: Literal["incoming", "outgoing", "missed"]
    number: Phone
    contact_name: str
    duration_s: int


class PhotoMeta(BaseModel):
    t: AwareDatetime
    lat: float
    lon: float
    make: str
    model: str
    offset: Annotated[str, StringConstraints(pattern=r"^[+-]\d{2}:\d{2}$")] = "+05:30"  # the camera clock's zone
    # Case families only; the defaults render today's plain image, so older cases stay byte-identical.
    image: str | None = None          # a stock photo in suraag/data/photos/
    card: list[str] | None = None     # text lines of a fictional ID card drawn onto the photo
    software: str | None = None       # EXIF Software (an editor, or the phone's own firmware)
    modified: AwareDatetime | None = None  # EXIF ModifyDate; None means it equals the capture time


class BriefQuestion(BaseModel):
    id: str
    kind: QuestionKind
    text: str
    about: QuestionAbout | None = None


class Suspect(BaseModel):
    id: str
    name: str
    phone: Phone


class Brief(BaseModel):
    """What students see. It never contains answers."""
    summary: str
    lab_cast: list[str] = ["Inspector Meera Rao", "Dr. Arvind Nair", "Farhan Qureshi"]
    device_owner: str
    mule: str
    suspects: list[Suspect]
    places: list[Place]
    questions: list[BriefQuestion]
    family: Family = "upi"


class Case(BaseModel):
    case_id: str
    lang: Lang
    seed: int
    family: Family = "upi"   # the crime the case is about; see suraag/families.py
    level: int = 1           # practice level 1-4; see suraag/levels.py
    twists: list[str] = []   # the traps this level sets; each one is checked by verify.check_depth
    tolerance_minutes: int = 2
    people: list[Person]
    places: list[Place]
    timeline: list[Event]
    facts: list[Fact]
    questions: list[Question]
    distractors: list[str]  # fact ids
    chat_members: list[str]  # person ids
    chat_window: tuple[AwareDatetime, AwareDatetime]
    chat_length: int  # lines in chat.txt, including the SYNTHETIC header
    chat_anchors: list[ChatAnchor]
    calls: list[CallRow]
    photo: PhotoMeta | None = None
    brief: Brief

    def person(self, pid: str) -> Person:
        return next(p for p in self.people if p.id == pid)

    def fact(self, fid: str) -> Fact:
        return next(f for f in self.facts if f.id == fid)

    def filler_needed(self) -> int:
        return self.chat_length - 1 - len(self.chat_anchors)

    @model_validator(mode="after")
    def _consistent(self) -> "Case":
        phones = [p.phone for p in self.people]
        if len(set(phones)) != len(phones):
            raise ValueError("phone numbers must be unique within a case")
        initials = [p.initials for p in self.people]
        if len(set(initials)) != len(initials):
            raise ValueError("people in a case must have distinct initials")

        people = {p.id for p in self.people}
        places = {p.id for p in self.places}
        events = {e.id for e in self.timeline}
        facts = {f.id for f in self.facts}

        def need(ids, known, what):
            missing = [i for i in ids if i not in known]
            if missing:
                raise ValueError(f"unknown {what}: {missing}")

        for e in self.timeline:
            need([e.actor] + ([e.target] if e.target else []), people, "person in timeline")
            need(e.depends_on, events, "event in depends_on")
        need([f.event for f in self.facts], events, "event in a fact")
        need(self.distractors, facts, "distractor fact")
        need(self.chat_members, people, "chat member")
        need([self.brief.device_owner, self.brief.mule], people, "person in brief")
        for q in self.questions:
            need(q.answer_facts, facts, "answer fact")
            if q.kind == "who":
                need([q.answer], people | {NO_ONE}, "who answer")
            elif q.kind == "where":
                need([q.answer], places, "where answer")
            elif q.kind == "yesno":
                if q.answer not in ("yes", "no"):
                    raise ValueError(f"{q.id}: a 'yesno' answer must be yes or no")
            elif q.kind == "amount":
                if not q.answer.isdigit():
                    raise ValueError(f"{q.id}: an 'amount' answer must be whole rupees in digits")
            else:
                try:
                    ok = datetime.fromisoformat(q.answer).tzinfo is not None
                except ValueError:
                    ok = False
                if not ok:
                    raise ValueError(f"{q.id}: a 'when' answer must be an ISO time with an offset")
        return self
