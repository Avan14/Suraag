"""Case families: Indian cyber-fraud types beyond the UPI ring, on the same machinery as the practice levels
(code writes every evidence line verbatim; a solver reads only the files and the brief; each trap is a named
shortcut that verify.check_depth proves gives a real wrong answer; worked solutions are built here, in code).

The device is the victim's phone. chat.txt is the victim's WhatsApp messages of that day, all chats in one
file in time order; a sender the victim never saved shows as a phone number, as in a real export. Filler (LLM
or stub) is only the victim chatting with a relative; every line from a stranger is written by code.
See docs/CASE_FAMILIES.md for how each fraud works and the sources.

    da  digital arrest. A stranger's call hands the victim to a fake officer, who sends an ID-card photo and
        demands the balance be moved to a "safe account". Who, when, and: was the ID photo edited?
    nc  control case, nothing happened. A courier calls and delivers a parcel; a relative forwards a warning
        about parcel scams. Who demanded money (honest answer: no one), was the delivery photo edited (no), where.
    ts  job / task scam. Paid "tasks", small commission credits as bait, then escalating deposits.
        Who asked for the deposits, and how much was deposited in total.
    cc  fake customer care. The victim dials a number found online; a "technician" calls back and asks for a
        screen-sharing app and the code on screen. Who asked for the install, and when control passed.

Traps (shortcut -> where it leads):
    handover, stranger_call  blame the first unsaved caller in calls.csv
    callback            blame the number the victim dialled
    forwarded           search for the demand words and take the first hit: a forwarded warning
    camera_original     trust DateTimeOriginal and call the photo unedited
    software_tag        judge editing by the Software tag alone (absent on an edited file; the phone's own
                        firmware on a clean one)
    payout              add the commission credits to the deposits
    escalation          add every demand, including the last one the victim never paid
    install_vs_control  take the install request as the moment control passed
"""
import random
import re
from datetime import datetime, timedelta

from suraag.explain import Walk
from suraag.geo import haversine_m
from suraag.grade import answer_matches
from suraag.i18n import t
from suraag.lang import get_pack
from suraag.levels import _place_lines
from suraag.model import (IST, NO_ONE, Anchor, Brief, BriefQuestion, CallRow, Case, ChatAnchor, ChatMessage,
                          Event, Fact, Lang, Person, PhotoMeta, Place, Question, Suspect)
from suraag.names import draw_people
from suraag.norm import norm
from suraag.parse import Artifacts, load_exif
from suraag.skeleton import MAKES, _phones
from suraag.solver import UNSOLVABLE, _read, _suspect, photo_place
from suraag.timefmt import chat_time, csv_hm, exif_ts, parse_exif_ts

FAMILIES: dict[str, dict[int, tuple[str, ...]]] = {
    "da": {1: ("handover", "camera_original"), 2: ("handover", "forwarded", "software_tag")},
    "nc": {1: ("stranger_call",), 2: ("stranger_call", "forwarded", "software_tag")},
    "ts": {1: ("payout", "escalation"), 2: ("payout", "escalation", "handover")},
    "cc": {1: ("callback", "install_vs_control"), 2: ("callback", "install_vs_control", "forwarded")},
}
CODE = {"da": "DA", "nc": "NC", "ts": "TS", "cc": "CC"}      # case folder prefix, e.g. cases/DA-L1-...
SLUG = {"da": "arrest", "nc": "parcel", "ts": "task", "cc": "care"}
DEMAND = {"da": "da_demand", "nc": "da_demand", "ts": "ts_demand", "cc": "cc_demand"}
DESK_PHOTOS = ("desk-notebook.jpg", "desk-office.jpg", "cafe-table.jpg")  # where the fake ID card lies
SCENE_PHOTOS = ("platform.jpg", "bus-bay.jpg", "bus-shelter.jpg", "foggy-road.jpg", "apartments.jpg",
                "construction.jpg", "cafe-table.jpg")
EDITOR = "Generic Photo Editor 2.1"  # a made-up editor name
CHAT_LENGTH = {1: (24, 30), 2: (30, 36)}
AMOUNT = re.compile(r"\brs\.? ?([\d,]+)")
PHONE = re.compile(r"^\+91-5\d{4}-\d{5}$")


def trigger_keys(family: str) -> tuple[str, ...]:
    """The pack triggers that only code may write in this family (verify flags filler that matches one)."""
    return ("fwd", DEMAND[family]) + {"ts": ("ts_deposit", "ts_payout"), "cc": ("cc_control",)}.get(family, ())


# ------------------------------------------------------------------------------------------------ builder
def build_any(family: str, seed: int, lang: Lang, level: int = 1) -> Case:
    """The one entry point for every family; 'upi' is the practice-level builder, unchanged."""
    if family == "upi":
        from suraag.levels import build_level_case
        return build_level_case(seed, lang, level)
    return build_family_case(family, seed, lang, level)


def build_family_case(family: str, seed: int, lang: Lang, level: int = 1) -> Case:
    if family not in FAMILIES or level not in FAMILIES[family]:
        raise ValueError(f"unknown family/level {family!r}/{level}; known: { {f: sorted(v) for f, v in FAMILIES.items()} }")
    twists = FAMILIES[family][level]
    rng = random.Random(f"suraag-{family}-{level}-{seed}")
    pack = get_pack(lang)
    fx, common = pack.families[family], pack.families["common"]
    mins = lambda n: timedelta(minutes=n)  # noqa: E731

    # People: names are drawn independently of role. Strangers are never saved: the export shows their number.
    roles = ["victim", "witness" if family == "nc" else "boss", "associate", "distractor"]
    unsaved = {"associate"} | ({"boss"} if family == "cc" else set())
    people = []
    for i, (n, role, phone) in enumerate(zip(draw_people(rng, 4), roles, _phones(rng, 4)), start=1):
        own = f"{n.first} {n.surname[0]}"
        if role == "victim":
            aliases = [own]
        elif role in unsaved:
            aliases = [phone, own]
        elif role == "boss":
            aliases = [fx["boss_alias"].format(first=n.first, surname=n.surname), own]
        else:
            aliases = [pack.alias_patterns[n.gender].format(first=n.first), own]
        people.append(Person(id=f"P{i}", name=n.full, name_deva=n.full_deva, role=role, aliases=aliases, phone=phone))
    victim, other, assoc, rel = people
    owner = victim.name.split()[0]

    day = datetime(2026, 4, 1, tzinfo=IST) + timedelta(days=rng.randint(0, 150))
    start = day.replace(hour=rng.randint(10, 16), minute=rng.choice([0, 15, 30, 45]))
    end = start + mins(150)
    chosen = rng.sample(pack.places, 3)
    places = [Place(id=f"PL{i}", name=n, lat=la, lon=lo) for i, (n, la, lo) in enumerate(chosen, start=1)]
    where = rng.choice(places)
    make, model = rng.choice(MAKES)

    msgs: dict[str, tuple[datetime, Person, str]] = {}     # key -> (time, sender, verbatim text)
    calls: dict[str, tuple[datetime, str, Person, int]] = {}  # key -> (time, direction, other party, seconds)
    photo_t, modified, software, card, image = None, None, None, None, rng.choice(SCENE_PHOTOS)
    fwd_text = common["fwd_care" if family == "cc" else "fwd_parcel"]

    if family == "da":
        t_first = start + mins(rng.randint(4, 12))          # the "courier" call that hands the victim over
        t_id = t_first + mins(rng.randint(18, 30))
        t_dem = t_id + mins(rng.randint(25, 45))
        calls["first"] = (t_first, "incoming", assoc, rng.randint(300, 900))
        calls["video"] = (t_id - mins(rng.randint(3, 6)), "incoming", other, rng.randint(1200, 2400))
        calls["demand"] = (t_dem - mins(rng.randint(1, 2)), "incoming", other, rng.randint(200, 600))
        msgs["id"] = (t_id, other, fx["id"].format(owner=owner))
        msgs["demand"] = (t_dem, other, fx["demand"].format(owner=owner))
        if "forwarded" in twists:
            msgs["fwd"] = (t_dem - mins(rng.randint(6, 20)), rel, fwd_text)
        t_rel = t_dem + mins(rng.choice([-1, 1]) * rng.randint(8, 25))
        calls["rel"] = (t_rel, "missed", rel, 0)
        image = rng.choice(DESK_PHOTOS)
        photo_t = (t_id - timedelta(days=rng.randint(3, 40))).replace(hour=rng.randint(9, 18), minute=rng.randint(0, 59))
        modified = t_id - mins(rng.randint(2, 9))
        software = EDITOR if "software_tag" not in twists else None  # tier 2: the editor left no Software tag
        card = ["IDENTITY CARD - SAMPLE", "FICTIONAL, NOT A REAL ID", f"Name: {other.name}", "Rank: Inspector",
                f"Card no.: {rng.randint(1000, 9999)}-X", "FOR TRAINING ONLY"]
    elif family == "nc":
        t_call = start + mins(rng.randint(30, 60))
        t_msg = t_call + mins(rng.randint(1, 2))
        calls["first"] = (t_call, "incoming", assoc, rng.randint(30, 90))
        msgs["courier"] = (t_msg, assoc, fx["courier"])
        if "forwarded" in twists:
            msgs["fwd"] = (t_msg + mins(rng.randint(30, 50)), rel, fwd_text)
        t_rel = t_call + mins(rng.randint(8, 25))
        calls["rel"] = (t_rel, "incoming", rel, rng.randint(40, 200))
        calls["friend"] = (t_call + mins(rng.randint(60, 80)), "outgoing", other, rng.randint(40, 200))
        photo_t = t_msg - mins(1)
        if "software_tag" in twists:  # the phone's own firmware string: present on a clean original
            software = f"{make} camera firmware {rng.randint(10, 14)}.{rng.randint(0, 9)}.{rng.randint(1, 30)}"
    elif family == "ts":
        t_job = start + mins(rng.randint(8, 14))
        msgs["job"] = (t_job, assoc, fx["job"])
        if "handover" in twists:
            calls["first"] = (t_job - mins(rng.randint(1, 2)), "incoming", assoc, rng.randint(60, 240))
        t = t_job
        for i in (1, 2):
            t += mins(rng.randint(12, 18) if i == 1 else rng.randint(8, 14))
            msgs[f"payout{i}"] = (t, other, fx["payout"].format(i=i, amount=f"{rng.choice((150, 180, 210, 240, 300)):,}"))
        ladder = ((1000, 1500, 2000), (3000, 4000, 5000), (8000, 10000, 12000), (15000, 20000, 25000))
        paid = [rng.choice(step) for step in ladder[: 3 if level == 1 else 4]]
        for k, amount in enumerate(paid, start=1):
            t += mins(rng.randint(8, 14) if k == 1 else rng.randint(6, 10))
            msgs[f"demand{k}"] = (t, other, fx["demand"].format(i=k + 2, amount=f"{amount:,}"))
            t += mins(rng.randint(3, 6))
            msgs[f"deposit{k}"] = (t, victim, fx["deposit"].format(amount=f"{amount:,}"))
        t += mins(rng.randint(6, 10))
        last = rng.choice((30000, 40000, 50000))
        msgs["last"] = (t, other, fx["last"].format(amount=f"{last:,}"))
        msgs["refuse"] = (t + mins(rng.randint(2, 5)), victim, fx["refuse"])
        t_dem = msgs["demand1"][0]
        calls["demand"] = (t_dem - mins(rng.randint(1, 2)), "incoming", other, rng.randint(120, 400))
        calls["rel"] = (t_dem + mins(rng.choice([-1, 1]) * rng.randint(8, 25)), "incoming", rel, rng.randint(40, 200))
        photo_t = msgs["deposit1"][0] + mins(rng.randint(2, 4))
    else:  # cc
        t_dial = start + mins(rng.randint(5, 12))
        t_desk = t_dial + mins(rng.randint(1, 2))
        t_tech = t_desk + mins(rng.randint(15, 30))
        t_dem = t_tech + mins(rng.randint(1, 2))
        t_ctrl = t_dem + mins(rng.randint(4, 9))
        calls["dial"] = (t_dial, "outgoing", assoc, rng.randint(120, 400))
        calls["demand"] = (t_tech, "incoming", other, rng.randint(400, 900))
        msgs["desk"] = (t_desk, assoc, fx["desk"])
        msgs["demand"] = (t_dem, other, fx["demand"].format(owner=owner))
        code = f"{rng.randint(100, 999)} {rng.randint(100, 999)}"
        msgs["control"] = (t_ctrl, victim, fx["control"].format(code=code))
        if "forwarded" in twists:
            msgs["fwd"] = (t_dem - mins(rng.randint(3, 10)), rel, fwd_text)
        calls["rel"] = (t_dem + mins(rng.choice([-1, 1]) * rng.randint(8, 25)), "incoming", rel, rng.randint(40, 200))
        photo_t = t_ctrl + mins(rng.randint(15, 40))

    # ---- files: chat anchors at lines proportional to their time; calls sorted by time
    order = sorted(msgs, key=lambda k: msgs[k][0])
    length = rng.randint(*CHAT_LENGTH[level])
    line_of = dict(zip(order, _place_lines([msgs[k][0] for k in order], start, end, length)))
    anchors = [ChatAnchor(line=line_of[k], message=ChatMessage(t=msgs[k][0], sender=msgs[k][1].saved_as, text=msgs[k][2]))
               for k in order]
    call_order = sorted(calls, key=lambda k: calls[k][0])
    row_of = {k: i for i, k in enumerate(call_order, start=1)}
    call_rows = [CallRow(row=row_of[k], t=calls[k][0], direction=calls[k][1], number=calls[k][2].phone,
                         contact_name="" if calls[k][2].saved_as == calls[k][2].phone else calls[k][2].saved_as,
                         duration_s=calls[k][3]) for k in call_order]
    lat = round(where.lat + rng.uniform(-0.0004, 0.0004), 4)
    lon = round(where.lon + rng.uniform(-0.0004, 0.0004), 4)
    photo = PhotoMeta(t=photo_t, lat=lat, lon=lon, make=make, model=model, image=image, card=card,
                      software=software, modified=modified)

    def chat(k: str, *needles: str) -> Anchor:
        return Anchor(artifact="chat", line=line_of[k], must_contain=[chat_time(msgs[k][0]), *needles])

    def call(k: str) -> Anchor:
        return Anchor(artifact="calls", row=row_of[k], must_contain=[calls[k][2].phone, csv_hm(calls[k][0])])

    def exif(tag: str, when: datetime) -> Anchor:
        return Anchor(artifact="photo", exif_tag=tag, must_contain=[exif_ts(when)])

    # ---- facts and events. F1 the demand (nc: the courier), F2 cc's handover, F3/F4 the photo clocks,
    # F5 the first stranger, F6 the GPS, F9/F10 distractors, F11+ deposits, F21+ payouts, F30/F31 the last demand.
    timeline, facts = [], []

    def fact(fid: str, eid: str, kind: str, actor: Person, t: datetime, claim: str, anchors: list[Anchor]) -> None:
        timeline.append(Event(id=eid, t=t, kind=kind, actor=actor.id))
        facts.append(Fact(id=fid, claim=claim, event=eid, anchors=anchors))

    if family == "nc":
        fact("F1", "E1", "call", assoc, calls["first"][0], f"{assoc.id} called and only delivered a parcel",
             [chat("courier", assoc.phone), call("first")])
    else:
        dem = "demand1" if family == "ts" else "demand"
        fact("F1", "E3", "instruction", other, msgs[dem][0], f"{other.id} made the demand at {chat_time(msgs[dem][0])}",
             [chat(dem, other.saved_as), call("demand")])
    if family == "cc":
        fact("F2", "E2", "control_handover", victim, msgs["control"][0], f"{victim.id} read out the screen code",
             [chat("control", code)])
        fact("F5", "E1", "call", assoc, calls["dial"][0], f"{victim.id} dialled {assoc.id}, who promised a callback",
             [chat("desk", assoc.phone), call("dial")])
    if family in ("da", "nc"):
        fact("F3", "E4", "photo", other if family == "da" else assoc, photo_t, "the photo was taken",
             [exif("DateTimeOriginal", photo_t)])
        fact("F4", "E5", "photo", other if family == "da" else assoc, modified or photo_t, "the file was last saved",
             [exif("ModifyDate", modified or photo_t)])
    if family == "da":
        fact("F5", "E1", "call", assoc, calls["first"][0], f"{assoc.id} made the first call", [call("first")])
    if family == "ts":
        fact("F5", "E1", "message", assoc, msgs["job"][0], f"{assoc.id} sent the job offer",
             [chat("job", assoc.phone)] + ([call("first")] if "first" in calls else []))
    if family != "da":
        fact("F6", "E6", "photo", assoc if family == "nc" else victim, photo_t, f"the photo was taken near {where.name}",
             [Anchor(artifact="photo", exif_tag="GPSLatitude", must_contain=[f"{lat:.4f}"]),
              Anchor(artifact="photo", exif_tag="GPSLongitude", must_contain=[f"{lon:.4f}"])])
    fact("F9", "E9", "distractor_call", rel, calls["rel"][0], f"{rel.id} called (an unrelated call)", [call("rel")])
    if "fwd" in msgs:
        fact("F10", "E10", "forwarded_message", rel, msgs["fwd"][0], f"{rel.id} forwarded a warning, not a demand",
             [chat("fwd", rel.saved_as)])
    deposits = [k for k in order if k.startswith("deposit")]
    for n, k in enumerate(deposits, start=1):
        fact(f"F1{n}", f"E1{n}", "deposit", victim, msgs[k][0], f"{victim.id} paid {msgs[k][2]}",
             [chat(k, AMOUNT.search(norm(msgs[k][2])).group(0).replace("rs", "Rs"))])
    for n, k in enumerate((k for k in order if k.startswith("payout")), start=1):
        fact(f"F2{n}", f"E2{n}", "payout", other, msgs[k][0], f"{other.id} credited a small commission as bait",
             [chat(k, AMOUNT.search(norm(msgs[k][2])).group(0).replace("rs", "Rs"))])
    if family == "ts":
        fact("F30", "E30", "instruction", other, msgs["last"][0], "the last, unpaid demand",
             [chat("last", AMOUNT.search(norm(msgs["last"][2])).group(0).replace("rs", "Rs"))])
        fact("F31", "E31", "message", victim, msgs["refuse"][0], f"{victim.id} refused to pay it",
             [chat("refuse", victim.saved_as)])

    # ---- questions
    q, qc = fx["q"], common
    questions = []
    if family == "nc":
        questions += [Question(id="Q1", kind="who", text=q["who"], answer=NO_ONE,
                               answer_facts=["F1"] + (["F10"] if "fwd" in msgs else [])),
                      Question(id="Q2", kind="yesno", text=q["yesno"], answer="no", answer_facts=["F3", "F4"]),
                      Question(id="Q3", kind="where", text=q["where"], answer=where.id, answer_facts=["F6"])]
    else:
        questions.append(Question(id="Q1", kind="who", text=q["who"], answer=other.id, answer_facts=["F1"]))
        if family == "da":
            questions += [Question(id="Q2", kind="when", text=q["when"], answer=msgs["demand"][0].isoformat(),
                                   answer_facts=["F1"]),
                          Question(id="Q3", kind="yesno", text=q["yesno"], answer="yes", answer_facts=["F3", "F4"])]
        elif family == "ts":
            total = sum(int(AMOUNT.search(norm(msgs[k][2])).group(1).replace(",", "")) for k in deposits)
            questions += [Question(id="Q2", kind="amount", text=q["amount"], answer=str(total),
                                   answer_facts=[f"F1{n}" for n in range(1, len(deposits) + 1)]),
                          Question(id="Q3", kind="where", text=qc["photo_where"], answer=where.id, answer_facts=["F6"])]
        else:
            questions += [Question(id="Q2", kind="when", text=q["when"], answer=msgs["control"][0].isoformat(),
                                   answer_facts=["F2"]),
                          Question(id="Q3", kind="where", text=qc["photo_where"], answer=where.id, answer_facts=["F6"])]
    summary = fx["summary"].format(date=f"{start.day} {start:%B %Y}") + " " + common["files"].format(photo=fx["photo"])
    brief = Brief(summary=summary, device_owner=victim.id, mule=victim.id, family=family,
                  suspects=[Suspect(id=p.id, name=p.name, phone=p.phone) for p in people if p.id != victim.id],
                  places=places if family != "da" else [],
                  questions=[BriefQuestion(id=x.id, kind=x.kind, text=x.text) for x in questions])
    return Case(case_id=f"{family}-{SLUG[family]}-{seed:03d}-l{level}", lang=lang, seed=seed, family=family,
                level=level, twists=list(twists), tolerance_minutes=2, people=people, places=places,
                timeline=timeline, facts=facts, questions=questions,
                distractors=["F9"] + (["F10"] if "fwd" in msgs and family != "nc" else []),
                chat_members=[victim.id, rel.id] + ([other.id] if family == "nc" else []),
                chat_window=(start, end), chat_length=length, chat_anchors=anchors, calls=call_rows, photo=photo,
                brief=brief)


# ------------------------------------------------------------------------------------------------ solver
def _hits(lines, pack, key: str):
    return [ln for ln in lines if pack.triggers[key].search(norm(ln.text))]


def _rupees(lines) -> int:
    return sum(int(a.replace(",", "") or 0) for ln in lines for a in AMOUNT.findall(norm(ln.text)))


def _sender(ln, calls, brief) -> str:
    """A saved sender is matched to the call log by its exact contact name; an unsaved one IS its number."""
    numbers = {r.number for r in calls if r.contact_name and norm(r.contact_name) == norm(ln.sender)}
    if not numbers and PHONE.match(ln.sender.strip()):
        numbers = {ln.sender.strip()}
    return _suspect(numbers, brief)


def _edited(exif: dict[str, str]) -> str:
    """Edited means the file was saved again after it was taken: ModifyDate later than DateTimeOriginal."""
    try:
        return "yes" if parse_exif_ts(exif["ModifyDate"]) > parse_exif_ts(exif["DateTimeOriginal"]) else "no"
    except (KeyError, ValueError):
        return UNSOLVABLE


def _demands(lines, pack, family: str):
    """Lines that ask for the money or the install, minus forwarded warnings that only quote the words."""
    return [ln for ln in _hits(lines, pack, DEMAND[family]) if not pack.triggers["fwd"].search(norm(ln.text))]


def solve_family(arts: Artifacts, brief: Brief, lang: Lang) -> dict[str, str]:
    """Reads only the files and the brief, like solver.solve."""
    pack = get_pack(lang)
    lines, calls, exif = _read(arts)
    demands = _demands(lines, pack, brief.family)
    out = {}
    for q in brief.questions:
        if q.kind == "where":
            out[q.id] = photo_place(exif, brief)
        elif q.kind == "yesno":
            out[q.id] = _edited(exif)
        elif q.kind == "amount":  # what the victim says they paid; credits and unpaid demands are not deposits
            out[q.id] = str(_rupees(_hits(lines, pack, "ts_deposit")))
        elif q.kind == "who":
            if not demands:
                out[q.id] = NO_ONE  # the honest answer: no such instruction in the files
            else:
                out[q.id] = _sender(demands[0], calls, brief) if len({d.sender for d in demands}) == 1 else UNSOLVABLE
        else:  # when: the demand, or in cc the moment the victim read out the code
            hits = _hits(lines, pack, "cc_control") if brief.family == "cc" else demands
            out[q.id] = hits[0].t.isoformat() if hits else UNSOLVABLE
    return out


def shortcut_family(arts: Artifacts, brief: Brief, lang: Lang) -> dict[str, tuple[str | None, str]]:
    """twist -> (question id, the answer a hurried reader gives)."""
    pack = get_pack(lang)
    lines, calls, exif = _read(arts)
    qid = {q.kind: q.id for q in brief.questions}
    demands = _demands(lines, pack, brief.family)
    words = _hits(lines, pack, DEMAND[brief.family])
    stranger = next((r for r in calls if r.direction == "incoming" and not r.contact_name), None)
    dialled = next((r for r in calls if r.direction == "outgoing"), None)
    by_row = lambda r: _suspect({r.number}, brief) if r else UNSOLVABLE  # noqa: E731
    return {
        # blame the first stranger who rang
        "handover": (qid.get("who"), by_row(stranger)),
        "stranger_call": (qid.get("who"), by_row(stranger)),
        # blame the number the victim dialled
        "callback": (qid.get("who"), by_row(dialled)),
        # search for the demand words and take the first hit
        "forwarded": (qid.get("who"), _sender(words[0], calls, brief) if words else UNSOLVABLE),
        # a photo with a capture time is an original
        "camera_original": (qid.get("yesno"), "no" if "DateTimeOriginal" in exif else UNSOLVABLE),
        # a Software tag means an editor; none means untouched
        "software_tag": (qid.get("yesno"), "yes" if "Software" in exif else "no"),
        # add every amount that moved: the deposits and the commission credits
        "payout": (qid.get("amount"), str(_rupees(_hits(lines, pack, "ts_deposit") + _hits(lines, pack, "ts_payout")))),
        # add every amount asked for
        "escalation": (qid.get("amount"), str(_rupees(demands))),
        # control passed when the install was asked for
        "install_vs_control": (qid.get("when"), demands[0].t.isoformat() if demands else UNSOLVABLE),
    }


# ------------------------------------------------------------------------------------------------ worked solution
def walkthrough_family(case: Case, arts: Artifacts, lang: str = "en") -> list[Walk]:
    w = lambda key, **kw: t(f"walk.{key}", lang, **kw)  # noqa: E731
    name = {p.id: p.name for p in case.people} | {p.id: p.name for p in case.places}
    said = {a.line: a.message for a in case.chat_anchors}
    facts = {f.id for f in case.facts}
    exif = load_exif(arts.photo) if arts.photo is not None else {}
    line = lambda fid: next(a.line for a in case.fact(fid).anchors if a.artifact == "chat")  # noqa: E731
    row = lambda fid: next(a.row for a in case.fact(fid).anchors if a.artifact == "calls")  # noqa: E731
    msg = lambda fid: said[line(fid)]  # noqa: E731
    loc = lambda fid: f"chat.txt:{line(fid)}"  # noqa: E731
    rupee = lambda n: f"Rs {int(n):,}"  # noqa: E731
    calls = {r.row: r for r in case.calls}

    def link(fid: str) -> str:
        r = calls[row(fid)]
        if r.contact_name:
            return w("fam.call_saved", loc=f"calls.csv:{r.row}", alias=msg(fid).sender, phone=r.number, hm=csv_hm(r.t))
        return w("fam.call_number", loc=f"calls.csv:{r.row}", phone=r.number, hm=csv_hm(r.t))

    fwd = [w("fam.fwd", loc=loc("F10"), sender=msg("F10").sender)] if "F10" in facts else []
    demand = [w("fam.demand", loc=loc("F1"), time=chat_time(msg("F1").t), sender=msg("F1").sender, text=msg("F1").text)]
    who_q = next(q for q in case.questions if q.kind == "who")
    if who_q.answer == NO_ONE:
        who = fwd + [w("fam.courier", loc=loc("F1"), phone=msg("F1").sender, text=msg("F1").text), link("F1"),
                     w("fam.no_demand")]
        who_answer = w("fam.no_one")
    else:
        boss = case.person(who_q.answer)
        who = fwd + demand + [link("F1"), w("suspect", phone=boss.phone, name=boss.name)]
        who_answer = boss.name

    out = []
    for q in case.questions:
        if q.kind == "who":
            steps, answer = who, who_answer
        elif q.kind == "when" and case.family == "cc":
            steps = demand + [w("fam.control", loc=loc("F2"), time=chat_time(msg("F2").t), text=msg("F2").text)]
            answer = chat_time(msg("F2").t)
        elif q.kind == "when":
            r = calls[row("F1")]
            steps = demand + [w("when_call", loc=f"calls.csv:{r.row}", hm=csv_hm(r.t), tol=case.tolerance_minutes)]
            answer = chat_time(msg("F1").t)
        elif q.kind == "yesno":
            steps = [w("fam.dto", loc="photo.jpg:DateTimeOriginal", value=exif.get("DateTimeOriginal", "")),
                     w("fam.modify", loc="photo.jpg:ModifyDate", value=exif.get("ModifyDate", ""))]
            if "Software" in exif:
                steps.append(w("fam.software", loc="photo.jpg:Software", value=exif["Software"]))
            steps.append(w("fam.edited" if q.answer == "yes" else "fam.unedited"))
            answer = w(f"fam.{q.answer}")
        elif q.kind == "amount":
            parts = [msg(f) for f in q.answer_facts]
            amounts = [int(AMOUNT.search(norm(m.text)).group(1).replace(",", "")) for m in parts]
            steps = [w("fam.deposit", loc=loc(f), time=chat_time(m.t), amount=rupee(a))
                     for f, m, a in zip(q.answer_facts, parts, amounts)]
            steps.append(w("fam.unpaid", loc=loc("F30"), amount=case.fact("F30").anchors[0].must_contain[1],
                           refuse=loc("F31")))
            steps.append(w("fam.sum", parts=" + ".join(rupee(a) for a in amounts), total=rupee(q.answer)))
            answer = rupee(q.answer)
        else:  # where
            lat, lon = float(exif["GPSLatitude"]), float(exif["GPSLongitude"])
            (d1, p1), (d2, p2) = sorted((haversine_m(lat, lon, p.lat, p.lon), p.name) for p in case.places)[:2]
            steps = [w("gps", loc="photo.jpg:GPSLatitude, photo.jpg:GPSLongitude", lat=exif["GPSLatitude"],
                       lon=exif["GPSLongitude"]),
                     w("nearest", d=round(d1), place=p1, place2=p2, d2=f"{d2 / 1000:.1f}")]
            answer = name[q.answer]
        out.append(Walk(q.id, tuple(steps), answer, ()))

    # traps: only the ones the shortcut reader really falls into on these files (as verify.check_depth)
    traps: dict[str, list[str]] = {}
    first_in = next((r for r in case.calls if r.direction == "incoming" and not r.contact_name), None)
    first_out = next((r for r in case.calls if r.direction == "outgoing"), None)
    for tw, (qid, got) in shortcut_family(arts, case.brief, case.lang).items():
        q = next((x for x in case.questions if x.id == qid), None)
        if tw not in case.twists or q is None or got == UNSOLVABLE or answer_matches(case, q, got):
            continue
        key, params = tw, {}
        if tw in ("handover", "stranger_call"):
            params = {"loc": f"calls.csv:{first_in.row}", "got": name[got]}
        elif tw == "callback":
            params = {"loc": f"calls.csv:{first_out.row}", "got": name[got]}
        elif tw == "forwarded":
            params = {"loc": loc("F10"), "got": name[got]}
        elif tw == "software_tag":
            key, params = ("software_tag_firmware", {"sw": exif.get("Software", "")}) if q.answer == "no" \
                else ("software_tag_absent", {})
        elif tw == "payout":
            params = {"got": rupee(got)}
        elif tw == "escalation":
            params = {"loc": loc("F30"), "got": rupee(got)}
        elif tw == "install_vs_control":
            params = {"loc": loc("F1"), "got": chat_time(datetime.fromisoformat(got))}
        traps.setdefault(qid, []).append(w(f"trap.{key}", **params))
    return [Walk(x.question_id, x.steps, x.answer, tuple(traps.get(x.question_id, []))) for x in out]
