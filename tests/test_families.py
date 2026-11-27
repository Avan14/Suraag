"""Case families: every tier verifies, every trap really misleads, the control case has no culprit, the photo
tamper question is read from EXIF, and the 14 UPI cases still rebuild byte for byte."""
import json
from pathlib import Path

import pytest

from suraag.explain import walkthrough
from suraag.families import FAMILIES, build_any, build_family_case, shortcut_family, trigger_keys
from suraag.grade import Citation, Claim, answer_matches, grade_claim
from suraag.hints import TIERS, base_hint
from suraag.lang import get_pack
from suraag.model import NO_ONE, Case
from suraag.norm import norm
from suraag.parse import Artifacts, load_exif
from suraag.render import render_calls, render_chat, render_photo, stub_filler
from suraag.solver import UNSOLVABLE, solve
from suraag.verify import check_depth, verify

ROOT = Path(__file__).parent.parent
TIERED = [(f, lvl) for f in FAMILIES for lvl in FAMILIES[f]]


def make(case: Case) -> Artifacts:
    return Artifacts(render_chat(case, stub_filler(case)), render_calls(case), render_photo(case))


def role(case: Case, r: str):
    return next(p for p in case.people if p.role == r)


@pytest.mark.parametrize("lang", ["en", "hinglish"])
@pytest.mark.parametrize("family,level", TIERED)
def test_every_tier_verifies_and_the_solver_reproduces_the_key(family, level, lang):
    for seed in range(1, 11):
        case = build_family_case(family, seed, lang, level)
        arts = make(case)
        assert case.family == case.brief.family == family and case.twists == list(FAMILIES[family][level])
        assert verify(case, arts) == [], (seed, [f.message for f in verify(case, arts)])
        assert solve(arts, case.brief, lang) == {q.id: q.answer for q in case.questions}


@pytest.mark.parametrize("family,level", TIERED)
def test_every_tier_sets_traps_on_a_stock_photo(family, level):
    case = build_family_case(family, 4, "en", level)
    assert case.twists and case.photo.image and (ROOT / "suraag" / "data" / "photos" / case.photo.image).exists()
    assert load_exif(render_photo(case))["ImageDescription"].startswith("SYNTHETIC")


@pytest.mark.parametrize("lang", ["en", "hinglish"])
def test_each_shortcut_lands_on_the_wrong_answer_it_was_built_for(lang):
    da = build_family_case("da", 5, lang, 2)
    short = shortcut_family(make(da), da.brief, lang)
    assert short["handover"] == ("Q1", role(da, "associate").id)
    assert short["forwarded"] == ("Q1", role(da, "distractor").id)
    assert short["software_tag"] == ("Q3", "no") and da.questions[2].answer == "yes"

    nc = build_family_case("nc", 5, lang, 2)
    short = shortcut_family(make(nc), nc.brief, lang)
    assert nc.questions[0].answer == NO_ONE
    assert short["stranger_call"] == ("Q1", role(nc, "associate").id)
    assert short["forwarded"] == ("Q1", role(nc, "distractor").id)
    assert short["software_tag"] == ("Q2", "yes") and nc.questions[1].answer == "no"

    ts = build_family_case("ts", 5, lang, 2)
    short, key = shortcut_family(make(ts), ts.brief, lang), int(ts.questions[1].answer)
    assert int(short["payout"][1]) > key and int(short["escalation"][1]) > key
    assert short["handover"] == ("Q1", role(ts, "associate").id)

    cc = build_family_case("cc", 5, lang, 2)
    short = shortcut_family(make(cc), cc.brief, lang)
    assert short["callback"] == ("Q1", role(cc, "associate").id)
    assert short["install_vs_control"][1] < cc.questions[1].answer  # the request comes before the handover


def test_a_trap_that_does_not_mislead_fails_the_depth_check():
    case = build_family_case("da", 3, "en", 2)
    tagged = case.model_copy(update={"photo": case.photo.model_copy(update={"software": "Generic Photo Editor 2.1"})})
    fails = check_depth(case, make(tagged))
    assert [(f.code, f.params["twist"]) for f in fails] == [("trap_not_set", "software_tag")]


def test_tamper_is_read_from_the_exif_dates():
    tier1, tier2 = build_family_case("da", 2, "en", 1), build_family_case("da", 2, "en", 2)
    e1, e2 = load_exif(render_photo(tier1)), load_exif(render_photo(tier2))
    assert e1["Software"] and e1["ModifyDate"] > e1["DateTimeOriginal"]
    assert "Software" not in e2 and e2["ModifyDate"] > e2["DateTimeOriginal"]
    clean = load_exif(render_photo(build_family_case("nc", 2, "en", 2)))
    assert "firmware" in clean["Software"] and clean["ModifyDate"] == clean["DateTimeOriginal"]


def test_the_id_card_is_fictional_and_marked():
    card = build_family_case("da", 1, "en", 1).photo.card
    assert "SAMPLE" in card[0] and any("FICTIONAL" in x for x in card) and any("TRAINING" in x for x in card)


def test_control_case_names_no_one_and_grades_a_culprit_as_wrong():
    case = build_family_case("nc", 6, "en", 1)
    arts, q = make(case), case.questions[0]
    assert q.answer == NO_ONE and answer_matches(case, q, "none")
    assert not answer_matches(case, q, role(case, "associate").id)
    line = case.fact("F1").anchors[0].line
    row = case.fact("F1").anchors[1].row
    r = grade_claim(case, arts, Claim("Q1", NO_ONE, (Citation("chat", line=line), Citation("calls", row=row))))
    assert r.points == 2


def test_amount_and_yes_no_answers_are_read_leniently():
    ts = build_family_case("ts", 2, "en", 1)
    q = ts.questions[1]
    total = int(q.answer)
    for given in (str(total), f"Rs {total:,}", f"₹{total}", f"{total}.00", f"rs. {total:,}/-"):
        assert answer_matches(ts, q, given), given
    assert not answer_matches(ts, q, str(total + 1)) and not answer_matches(ts, q, "a lot")
    da = build_family_case("da", 2, "en", 1)
    yes = da.questions[2]
    assert answer_matches(da, yes, "Yes") and answer_matches(da, yes, "haan") and not answer_matches(da, yes, "no")


def test_every_deposit_must_be_cited():
    case = build_family_case("ts", 7, "hinglish", 1)
    arts, q = make(case), case.questions[1]
    lines = [case.fact(f).anchors[0].line for f in q.answer_facts]
    some = grade_claim(case, arts, Claim(q.id, q.answer, tuple(Citation("chat", line=n) for n in lines[:-1])))
    assert some.answer_correct and not some.citation_valid
    assert grade_claim(case, arts, Claim(q.id, q.answer, tuple(Citation("chat", line=n) for n in lines))).points == 2


@pytest.mark.parametrize("lang", ["en", "hi"])
@pytest.mark.parametrize("family,level", TIERED)
def test_the_worked_solution_cites_real_lines_and_names_every_trap(family, level, lang):
    case = build_family_case(family, 8, "en", level)
    walks = walkthrough(case, make(case), lang)
    assert [w.question_id for w in walks] == [q.id for q in case.questions]
    assert sum(len(w.traps) for w in walks) == len(case.twists)
    text = " ".join(s for w in walks for s in w.steps)
    for q in case.questions:
        for a in (a for f in q.answer_facts for a in case.fact(f).anchors):
            loc = {"chat": f"chat.txt:{a.line}", "calls": f"calls.csv:{a.row}", "photo": f"photo.jpg:{a.exif_tag}"}
            assert loc[a.artifact] in text, (q.id, a)


@pytest.mark.parametrize("lang", ["en", "hinglish"])
def test_stub_filler_never_reads_like_family_evidence(lang):
    pack = get_pack(lang)
    for family in FAMILIES:
        for k in trigger_keys(family):
            assert not [s for s in pack.stub_lines if pack.triggers[k].search(norm(s))], (family, k)


def test_filler_that_reads_like_a_demand_is_caught():
    case = build_family_case("da", 9, "en", 1)
    arts = make(case)
    lines = arts.chat.split("\n")
    n = next(i for i in range(1, len(lines)) if i + 1 not in {a.line for a in case.chat_anchors} and lines[i])
    head = lines[n].rsplit(": ", 1)[0]
    lines[n] = f"{head}: please transfer it all to the safe account"
    fails = verify(case, Artifacts("\n".join(lines), arts.calls, arts.photo))
    assert "trigger_in_filler" in {f.code for f in fails}


def test_hints_never_leak_the_culprit_or_the_evidence():
    for family, level in TIERED:
        case = build_family_case(family, 10, "en", level)
        secrets = [m for f in case.facts for a in f.anchors for m in a.must_contain]
        if family != "nc":
            boss = role(case, "boss")
            secrets += [boss.name, *boss.aliases]
        for q in case.questions:
            for tier in range(1, TIERS + 1):
                h = norm(base_hint(case, q.id, tier))
                assert not [s for s in secrets if norm(s) in h], (family, q.id, tier)


def test_every_shipped_case_rebuilds_byte_identically():
    """The world model and the code-rendered files of every committed case (all 14 UPI cases and the
    family cases) come out of today's code unchanged; chat.txt holds LLM filler, so its hash is checked."""
    dirs = sorted(p.parent for p in (ROOT / "cases").glob("*/manifest.json"))
    assert len([d for d in dirs if d.name.startswith(("upi-", "L"))]) == 14
    for d in dirs:
        case = Case.model_validate_json((d / "case.json").read_text("utf-8"))
        assert build_any(case.family, case.seed, case.lang, case.level) == case, d.name
        arts = Artifacts.from_dir(d)
        assert render_calls(case).encode("utf-8") == arts.calls_bytes()[3:], d.name
        assert render_photo(case) == arts.photo, d.name
        assert arts.sha256() == json.loads((d / "manifest.json").read_text("utf-8"))["files"], d.name
        assert verify(case, arts) == [], d.name
        assert UNSOLVABLE not in solve(arts, case.brief, case.lang).values(), d.name
