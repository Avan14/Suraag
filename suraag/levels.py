"""Practice levels: the level 1 world from skeleton.build_case, plus the traps ("twists") a level adds.

Each twist makes one named shortcut give a plausible wrong answer, and adds the evidence the right reasoning
needs. On every level above 1 the decoy is also the boss's namesake (two suspects called "Sunil"), so the chat
name alone never picks a suspect: only a phone number does. verify.check_depth proves every shortcut really
misleads; explain.py tells the student why.
Level 1 is build_case unchanged, so the shipped cases and the LLM cache still match.

    unsaved_caller  the boss's call row has no saved name; the order says it follows a phone call, and a second
                    unsaved suspect also calls (so "the unsaved suspect" is not unique). Shortcut: first-name match.
    alibi           the mule writes "I'm at <another place>" just before the photo. Shortcut: believe the chat.
    code_word       the associate sets a code earlier ("when anyone writes '<phrase>', delete the entry"); the
                    boss later writes only the phrase. Shortcut: search for "delete" (finds the rule line).
    decoy           the mule confirms "done"; afterwards the decoy asks to remove a different entry.
                    Shortcut: take the latest delete request.
    camera_clock    the photo's EXIF clock is on UTC (OffsetTimeOriginal +00:00) and a question asks the photo
                    time in IST. Shortcut: read the EXIF time as IST.
"""
import random
from datetime import timedelta

from suraag.lang import get_pack
from suraag.model import (Anchor, BriefQuestion, CallRow, Case, ChatAnchor, ChatMessage, Event, Fact, Lang,
                          Person, Question, Suspect)
from suraag.names import draw_people
from suraag.skeleton import _phones, build_case
from suraag.timefmt import chat_time, csv_hm, exif_ts

LEVELS: dict[int, tuple[str, ...]] = {
    1: (),
    2: ("unsaved_caller", "alibi"),
    3: ("code_word", "decoy", "camera_clock"),
    4: ("unsaved_caller", "alibi", "code_word", "decoy", "camera_clock"),
}
CHAT_LENGTH = {2: (26, 32), 3: (30, 36), 4: (34, 42)}
CAMERA_OFFSET = "+00:00"  # a phone whose clock was left on UTC


def _extra_suspect(rng: random.Random, people: list[Person], lang: Lang, phone: str) -> Person:
    """A fifth person who only appears in the call log, from an unsaved number."""
    pack = get_pack(lang)
    firsts = {p.name.split()[0] for p in people}
    initials = {p.initials for p in people}
    surnames = {p.name.split()[-1][0] for p in people}
    for _ in range(500):
        n = draw_people(rng, 1)[0]
        cand = Person(id=f"P{len(people) + 1}", name=n.full, name_deva=n.full_deva, role="witness",
                      aliases=[pack.alias_patterns[n.gender].format(first=n.first), f"{n.first} {n.surname[0]}"],
                      phone=phone)
        if n.first not in firsts and cand.initials not in initials and n.surname[0] not in surnames:
            return cand
    raise RuntimeError("could not draw a distinct extra suspect")


def _place_lines(times: list, start, end, length: int) -> list[int]:
    """Chat lines for anchors sorted by time: proportional to time in the window, strictly increasing,
    never line 1 (the header) and never the last line."""
    out: list[int] = []
    n = len(times)
    for i, t in enumerate(times):
        want = 2 + round((t - start) / (end - start) * (length - 2))
        lo = out[-1] + 1 if out else 2
        hi = length - 1 - (n - 1 - i)
        out.append(min(max(want, lo), hi))
    return out


def build_level_case(seed: int, lang: Lang, level: int = 1) -> Case:
    if level not in LEVELS:
        raise ValueError(f"level must be one of {sorted(LEVELS)}")
    base = build_case(seed, lang)
    if level == 1:
        return base
    twists = LEVELS[level]
    rng = random.Random(f"suraag-level-{level}-{seed}")  # its own stream: the level 1 draws stay untouched
    pack = get_pack(lang)
    minutes = lambda n: timedelta(minutes=n)  # noqa: E731
    role = {p.role: p for p in base.people}
    boss, mule, distr, assoc = (role[r] for r in ("boss", "mule", "distractor", "associate"))
    # Namesake: the decoy takes the boss's first name, so "Sunil ji" in the chat matches two suspects.
    first, first_deva = boss.name.split(" ", 1)[0], boss.name_deva.split(" ", 1)[0]
    surname, surname_deva = distr.name.split(" ", 1)[1], distr.name_deva.split(" ", 1)[1]
    distr = distr.model_copy(update={"name": f"{first} {surname}", "name_deva": f"{first_deva} {surname_deva}",
                                     "aliases": [distr.saved_as, f"{first} {surname[0]}"]})
    ev = {e.id: e for e in base.timeline}
    t_instr, t_call, t_photo, t_distr = ev["E3"].t, ev["E2"].t, ev["E4"].t, ev["E9"].t
    start, end = base.chat_window
    people, timeline = [distr if p.id == distr.id else p for p in base.people], list(base.timeline)
    answer_place = next(q.answer for q in base.questions if q.kind == "where")

    # ---- calls: the level 1 rows, one more call from the associate well away from the order, and twists
    rows = [(r.t, r.direction, r.number, r.contact_name, r.duration_s) for r in base.calls]
    rows.append((t_instr + minutes(rng.randint(30, 45)), "incoming", assoc.phone, assoc.saved_as, rng.randint(30, 180)))
    if "unsaved_caller" in twists:
        rows = [(t, d, n, "" if n == boss.phone else c, s) for t, d, n, c, s in rows]
        phone = next(p for p in _phones(rng, 12) if p not in {x.phone for x in people})
        extra = _extra_suspect(rng, people, lang, phone)
        people.append(extra)
        rows.append((start + minutes(rng.randint(20, 35)), "incoming", extra.phone, "", rng.randint(25, 90)))
    rows.sort(key=lambda r: r[0])  # stable: equal times keep their listed order
    calls = [CallRow(row=i, t=t, direction=d, number=n, contact_name=c, duration_s=s)
             for i, (t, d, n, c, s) in enumerate(rows, start=1)]
    boss_row = next(r.row for r in calls if r.number == boss.phone and r.t == t_call)
    distr_row = next(r.row for r in calls if r.number == distr.phone and r.t == t_distr and r.direction == "incoming")

    # ---- chat anchors: (key, time, sender, text). The order's time is fixed; the others avoid its minute.
    call = pack.call_ref if "unsaved_caller" in twists else ""
    code = rng.choice(pack.code_words) if "code_word" in twists else None
    order_text = (rng.choice(pack.code_go_templates).format(owner=mule.saved_as, call=call, code=code) if code
                  else rng.choice(pack.go_templates).format(owner=mule.saved_as, call=call))
    msgs = {"order": (t_instr, boss.saved_as, order_text)}
    if code:
        msgs["code"] = (start + minutes(rng.randint(8, 20)), assoc.saved_as,
                        rng.choice(pack.code_def_templates).format(code=code))
    if "decoy" in twists:
        t_conf = t_instr + minutes(rng.randint(1, 3))
        msgs["confirm"] = (t_conf, mule.saved_as, rng.choice(pack.confirm_templates))
        msgs["decoy"] = (t_conf + minutes(rng.randint(6, 18)), distr.saved_as,
                         rng.choice(pack.decoy_templates).format(owner=mule.saved_as))
    if "alibi" in twists:
        other = rng.choice([p for p in base.places if p.id != answer_place])
        msgs["alibi"] = (t_photo - minutes(rng.randint(2, 6)), mule.saved_as,
                         rng.choice(pack.alibi_templates).format(place=other.name))
    used = {t_instr}
    for key in sorted((k for k in msgs if k != "order"), key=lambda k: msgs[k][0]):
        t, s, x = msgs[key]
        while t in used:
            t += minutes(1)
        used.add(t)
        msgs[key] = (t, s, x)
    order = sorted(msgs, key=lambda k: msgs[k][0])
    length = rng.randint(*CHAT_LENGTH[level])
    line_of = dict(zip(order, _place_lines([msgs[k][0] for k in order], start, end, length)))
    anchors = [ChatAnchor(line=line_of[k], message=ChatMessage(t=msgs[k][0], sender=msgs[k][1], text=msgs[k][2]))
               for k in order]
    tm = lambda k: msgs[k][0]  # noqa: E731

    def chat(k: str, *needles: str) -> Anchor:
        return Anchor(artifact="chat", line=line_of[k], must_contain=[chat_time(tm(k)), *needles])

    # ---- facts, in the order a student would reason through them
    the_call = Anchor(artifact="calls", row=boss_row, must_contain=[boss.phone, csv_hm(t_call)])
    facts = [Fact(id="F1", claim=f"{boss.id} told {mule.id} to delete the transfer record at {chat_time(t_instr)}",
                  event="E3", anchors=[chat("order", boss.saved_as), the_call])]
    if code:
        timeline.append(Event(id="E5", t=tm("code"), kind="code_definition", actor=assoc.id))
        facts.append(Fact(id="F2", claim=f"{assoc.id} set the code {code!r} for deleting the entry", event="E5",
                          anchors=[chat("code", code)]))
    if "decoy" in twists:
        timeline += [Event(id="E6", t=tm("confirm"), kind="confirmation", actor=mule.id, depends_on=["E3"]),
                     Event(id="E7", t=tm("decoy"), kind="decoy_message", actor=distr.id, target=mule.id)]
        facts += [Fact(id="F5", claim=f"{mule.id} confirmed the deletion at {chat_time(tm('confirm'))}", event="E6",
                       anchors=[chat("confirm", msgs["confirm"][2])]),  # its words: the decoy names the mule too
                  Fact(id="F10", claim=f"{distr.id} asked {mule.id} to remove an unrelated list entry", event="E7",
                       anchors=[chat("decoy", distr.saved_as)])]
    if "alibi" in twists:
        timeline.append(Event(id="E8", t=tm("alibi"), kind="alibi_message", actor=mule.id))
        facts.append(Fact(id="F11", claim=f"{mule.id} claimed to be at {other.name}", event="E8",
                          anchors=[chat("alibi", other.name)]))
    facts.append(base.fact("F3"))
    photo = base.photo
    if "camera_clock" in twists:
        photo = photo.model_copy(update={"offset": CAMERA_OFFSET})
        facts.append(Fact(id="F4", claim=f"the photo was taken at {chat_time(t_photo)} IST", event="E4", anchors=[
            Anchor(artifact="photo", exif_tag="DateTimeOriginal", must_contain=[exif_ts(t_photo, CAMERA_OFFSET)]),
            Anchor(artifact="photo", exif_tag="OffsetTimeOriginal", must_contain=[CAMERA_OFFSET])]))
    facts.append(Fact(id="F9", claim=base.fact("F9").claim, event="E9",
                      anchors=[Anchor(artifact="calls", row=distr_row, must_contain=[distr.phone, csv_hm(t_distr)])]))

    chain = (["F2"] if code else []) + ["F1"] + (["F5"] if "decoy" in twists else [])  # who/when reasoning steps
    qt = pack.question_texts
    questions = [q.model_copy(update={"answer_facts": chain}) if q.kind in ("who", "when") else q
                 for q in base.questions]
    if "camera_clock" in twists:
        questions.append(Question(id="Q4", kind="when", about="photo", text=qt["photo_time"], answer_facts=["F4"],
                                  answer=t_photo.isoformat()))
    brief = base.brief.model_copy(update={
        "suspects": [Suspect(id=p.id, name=p.name, phone=p.phone) for p in people if p.id != mule.id],
        "questions": [BriefQuestion(id=q.id, kind=q.kind, text=q.text, about=q.about) for q in questions]})
    return Case(case_id=f"upi-ring-{seed:03d}-l{level}", lang=lang, seed=seed, level=level, twists=list(twists),
                tolerance_minutes=base.tolerance_minutes, people=people, places=base.places, timeline=timeline,
                facts=facts, questions=questions, distractors=["F9"] + (["F10"] if "decoy" in twists else []),
                chat_members=base.chat_members, chat_window=base.chat_window, chat_length=length,
                chat_anchors=anchors, calls=calls, photo=photo, brief=brief)
