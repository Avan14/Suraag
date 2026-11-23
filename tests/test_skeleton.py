"""Tests for names and the seeded skeleton."""
import random

import pytest

from suraag.geo import haversine_m
from suraag.names import draw_people, load_names
from suraag.norm import norm
from suraag.skeleton import build_case
from suraag.timefmt import chat_time

LANGS = ("en", "hinglish")


def test_names_are_nfc_and_draws_are_reproducible():
    import unicodedata
    for region in load_names()["regions"].values():
        for _, deva, *_rest in region["first"] + region["surname"]:
            assert deva == unicodedata.normalize("NFC", deva)
    assert draw_people(random.Random(5)) == draw_people(random.Random(5))


def test_blocklisted_names_are_never_drawn():
    block = load_names()["blocklist"]
    for seed in range(200):
        assert not any(p.full.casefold() in block for p in draw_people(random.Random(seed)))


def test_haversine_known_distance():
    assert 6000 < haversine_m(19.0726, 72.8845, 19.0178, 72.8478) < 7500  # Kurla West to Dadar


def test_build_case_is_deterministic_and_seeds_differ():
    assert build_case(7, "hinglish") == build_case(7, "hinglish")
    a, b = build_case(1, "hinglish"), build_case(2, "hinglish")
    assert a.case_id == "upi-ring-001" and b.case_id == "upi-ring-002"
    assert [p.name for p in a.people] != [p.name for p in b.people]


@pytest.mark.parametrize("lang", LANGS)
def test_invariants_over_many_seeds(lang):
    for seed in range(1, 51):
        c = build_case(seed, lang)  # model validation already checks phones, initials, ids, aware times
        # every alias belongs to exactly one person
        aliases = [norm(a) for p in c.people for a in p.aliases]
        assert len(aliases) == len(set(aliases)), seed
        # exactly one boss, one mule, one distractor
        roles = sorted(p.role for p in c.people)
        assert roles == ["associate", "boss", "distractor", "mule"], seed
        # call and chat times agree within tolerance
        instr = next(e for e in c.timeline if e.kind == "instruction")
        call = next(e for e in c.timeline if e.kind == "call")
        assert 0 < (instr.t - call.t).total_seconds() / 60 <= c.tolerance_minutes, seed
        # photo within 500 m of the answer place
        place = next(p for p in c.places if p.id == next(q for q in c.questions if q.kind == "where").answer)
        assert haversine_m(c.photo.lat, c.photo.lon, place.lat, place.lon) < 500, seed
        # every dependency is earlier than the event that depends on it
        by_id = {e.id: e for e in c.timeline}
        assert all(by_id[d].t < e.t for e in c.timeline for d in e.depends_on), seed
        # the instruction sits mid-chat, the places are far apart
        assert 3 <= c.chat_anchors[0].line <= c.chat_length - 2 and 20 <= c.chat_length <= 30
        assert all(haversine_m(a.lat, a.lon, b.lat, b.lon) > 1500 for a in c.places for b in c.places if a.id != b.id)
        # no saved name is contained in anyone else's alias, so an anchor really identifies its sender
        for p in c.people:
            for q in c.people:
                if p.id != q.id:
                    assert all(norm(p.saved_as) not in norm(a) for a in q.aliases), (seed, p.saved_as, q.aliases)
        # the distractor shares a name token with the boss alias, without equalling any alias
        boss = next(p for p in c.people if p.role == "boss")
        distractor = next(p for p in c.people if p.role == "distractor")
        assert norm(boss.aliases[0].split()[0]) == norm(distractor.aliases[0].split()[0]), seed
        # the anchor strings really are what the renderers will print
        f1 = c.fact("F1")
        assert f1.anchors[0].must_contain == [chat_time(instr.t), boss.saved_as]
        # the brief never leaks the answers or the roles
        text = c.brief.model_dump_json()
        assert "boss" not in text and "distractor" not in text and '"answer' not in text


def test_guilt_is_not_tied_to_region():
    """Over many seeds the boss's first name comes from every region, not one."""
    data = load_names()["regions"]
    region_of = {en: r for r, v in data.items() for en, *_ in v["first"]}
    def boss_first(seed):
        return next(p for p in build_case(seed, "en").people if p.role == "boss").name.split()[0]

    assert len({region_of[boss_first(s)] for s in range(1, 60)}) == 4


def test_hinglish_forms_of_address_follow_gender():
    gender = {en: g for r in load_names()["regions"].values() for en, _, g in r["first"]}
    seen = set()
    for seed in range(1, 60):
        for p in build_case(seed, "hinglish").people:
            if p.role == "distractor":
                continue  # the decoy is saved under the boss's name token, not its own
            first = p.name.split()[0]
            assert p.saved_as == f"{first} {'didi' if gender[first] == 'f' else 'bhai'}", (seed, p.saved_as)
            seen.add(gender[first])
    assert seen == {"m", "f"}
