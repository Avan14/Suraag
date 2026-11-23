"""Seed -> world model, including the anchored evidence lines. Fully deterministic from the seed."""
import random
from datetime import datetime, timedelta

from suraag.lang import get_pack
from suraag.model import (Anchor, Brief, BriefQuestion, CallRow, Case, ChatAnchor, ChatMessage, Event, Fact,
                          IST, Lang, Person, PhotoMeta, Place, Question, Suspect)
from suraag.names import draw_people
from suraag.timefmt import chat_time, csv_hm

AMOUNTS = (18500, 24000, 32500, 48000, 56500, 72000)
MAKES = (("Redmi", "Note 12"), ("Samsung", "Galaxy A14"), ("Vivo", "Y22"), ("Realme", "C55"))


def _phones(rng: random.Random, n: int) -> list[str]:
    out: list[str] = []
    while len(out) < n:
        p = f"+91-5{rng.randrange(10000):04d}-{rng.randrange(100000):05d}"
        if p not in out:
            out.append(p)
    return out


def build_case(seed: int, lang: Lang) -> Case:
    rng = random.Random(seed)
    pack = get_pack(lang)
    tol = 2

    # People: names drawn independently of role; roles shuffled, so guilt is random.
    names = draw_people(rng, 4)
    roles = ["boss", "mule", "distractor", "associate"]
    rng.shuffle(roles)
    phones = _phones(rng, 4)
    boss_first = names[roles.index("boss")].first
    people = []
    for i, (n, role) in enumerate(zip(names, roles), start=1):
        own = f"{n.first} {n.surname[0]}"
        if role == "distractor":
            # Shares the boss's name token, but is never equal to or a prefix of any alias: the
            # trailing period stops "Raju B." from being a prefix of "Raju bhai".
            aliases = [f"{boss_first} {n.surname[0]}.", own]
        else:
            aliases = [pack.alias_patterns[0].format(first=n.first), own]
        people.append(Person(id=f"P{i}", name=n.full, name_deva=n.full_deva, role=role,
                             aliases=aliases, phone=phones[i - 1]))
    by_role = {p.role: p for p in people}
    boss, mule, distractor, associate = (by_role[r] for r in ("boss", "mule", "distractor", "associate"))

    # Time: a two-hour chat window; the instruction sits at 40-60% of it.
    day = datetime(2026, 3, 1, tzinfo=IST) + timedelta(days=rng.randint(0, 60))
    start = day.replace(hour=rng.randint(18, 20), minute=rng.choice([0, 15, 30, 45]))
    end = start + timedelta(minutes=120)
    minutes = lambda n: timedelta(minutes=n)  # noqa: E731
    t_instr = start + minutes(rng.randint(48, 72))
    t_transfer = t_instr - minutes(rng.randint(20, 40))
    t_call = t_instr - minutes(rng.randint(1, tol))
    t_photo = t_instr + minutes(rng.randint(15, 40))
    t_distr = t_instr + minutes(rng.choice([-1, 1]) * rng.randint(8, 28))
    t_missed = t_instr - minutes(rng.randint(8, 12))
    t_assoc = start + minutes(rng.randint(5, 15))

    timeline = [
        Event(id="E1", t=t_transfer, kind="transfer", actor=mule.id),
        Event(id="E2", t=t_call, kind="call", actor=boss.id, target=mule.id, depends_on=["E1"]),
        Event(id="E3", t=t_instr, kind="instruction", actor=boss.id, target=mule.id, depends_on=["E1"]),
        Event(id="E4", t=t_photo, kind="photo", actor=mule.id, depends_on=["E1"]),
        Event(id="E9", t=t_distr, kind="distractor_call", actor=distractor.id, target=mule.id),
    ]

    # Calls, as the mule's phone logs them: the boss's call, the distractor's, two other rows.
    raw_rows = [(t_assoc, "outgoing", associate, 60 + rng.randint(0, 120)),
                (t_missed, "missed", distractor, 0),
                (t_call, "incoming", boss, rng.randint(40, 200)),
                (t_distr, "incoming", distractor, rng.randint(20, 90))]
    order = sorted(range(4), key=lambda i: raw_rows[i][0])  # stable: ties keep the listed order
    calls, row_of = [], {}
    for row, i in enumerate(order, start=1):
        t, direction, who, dur = raw_rows[i]
        row_of[i] = row
        calls.append(CallRow(row=row, t=t, direction=direction, number=who.phone, contact_name=who.saved_as,
                             duration_s=dur))

    # Places and photo: three places, the photo within ~50 m of one of them.
    chosen = rng.sample(pack.places, 3)
    places = [Place(id=f"PL{i}", name=n, lat=la, lon=lo) for i, (n, la, lo) in enumerate(chosen, start=1)]
    answer = rng.choice(places)
    make, model = rng.choice(MAKES)
    photo = PhotoMeta(t=t_photo, lat=round(answer.lat + rng.uniform(-0.0004, 0.0004), 4),
                      lon=round(answer.lon + rng.uniform(-0.0004, 0.0004), 4), make=make, model=model)

    # Chat: the instruction is written verbatim at a fixed line near the middle.
    chat_length = rng.randint(20, 30)
    line = min(max(chat_length // 2 + rng.randint(-2, 2), 3), chat_length - 2)
    text = rng.choice(pack.instruction_templates).format(owner=mule.saved_as)
    anchor = ChatAnchor(line=line, message=ChatMessage(t=t_instr, sender=boss.saved_as, text=text))

    facts = [
        Fact(id="F1", claim=f"{boss.id} told {mule.id} to delete the transfer record at {chat_time(t_instr)}",
             event="E3", anchors=[
                 Anchor(artifact="chat", line=line, must_contain=[chat_time(t_instr), boss.saved_as]),
                 Anchor(artifact="calls", row=row_of[2], must_contain=[boss.phone, csv_hm(t_call)])]),
        Fact(id="F3", claim=f"{mule.id} took the payment screenshot photo near {answer.name}", event="E4",
             anchors=[Anchor(artifact="photo", exif_tag="GPSLatitude", must_contain=[f"{photo.lat:.4f}"]),
                      Anchor(artifact="photo", exif_tag="GPSLongitude", must_contain=[f"{photo.lon:.4f}"])]),
        Fact(id="F9", claim=f"{distractor.id} called {mule.id} at {chat_time(t_distr)} (an unrelated call)",
             event="E9", anchors=[Anchor(artifact="calls", row=row_of[3],
                                         must_contain=[distractor.phone, csv_hm(t_distr)])]),
    ]
    qt = pack.question_texts
    questions = [
        Question(id="Q1", kind="who", text=qt["who"], answer_facts=["F1"], answer=boss.id),
        Question(id="Q2", kind="when", text=qt["when"], answer_facts=["F1"], answer=t_instr.isoformat()),
        Question(id="Q3", kind="where", text=qt["where"], answer_facts=["F3"], answer=answer.id),
    ]
    brief = Brief(
        summary=pack.brief_summary.format(amount=f"{rng.choice(AMOUNTS):,}",
                                          date=f"{t_transfer.day} {t_transfer:%B %Y}"),
        device_owner=mule.id, mule=mule.id,
        suspects=[Suspect(id=p.id, name=p.name, phone=p.phone) for p in people if p.id != mule.id],
        places=places, questions=[BriefQuestion(id=q.id, kind=q.kind, text=q.text) for q in questions])
    return Case(case_id=f"upi-ring-{seed:03d}", lang=lang, seed=seed, tolerance_minutes=tol, people=people,
                places=places, timeline=timeline, facts=facts, questions=questions, distractors=["F9"],
                chat_members=[p.id for p in people], chat_window=(start, end), chat_length=chat_length,
                chat_anchors=[anchor], calls=calls, photo=photo, brief=brief)
