"""Rule R-03: guilt is assigned at random, never from the name pool's region. No LLM involved."""
from collections import Counter

import pytest

from suraag.levels import build_level_case
from suraag.names import load_names
from suraag.skeleton import build_case

CHI2_CRITICAL_DF3_P001 = 11.345  # four regions, so three degrees of freedom, p < 0.01


def region_of():
    return {en: r for r, v in load_names()["regions"].items() for en, *_ in v["first"]}


def test_culprit_region_share_matches_the_draw_share_over_1000_seeds():
    region, draws, culprits = region_of(), Counter(), Counter()
    for seed in range(1000):
        for p in build_case(seed, "en").people:
            r = region[p.name.split()[0]]
            draws[r] += 1
            culprits[r] += p.role == "boss"
    n, total = sum(culprits.values()), sum(draws.values())
    assert n == 1000 and set(draws) == set(load_names()["regions"])
    chi2 = sum((culprits[r] - n * draws[r] / total) ** 2 / (n * draws[r] / total) for r in draws)
    assert chi2 < CHI2_CRITICAL_DF3_P001, (chi2, dict(culprits), dict(draws))


def test_every_role_is_equally_likely_for_each_gender():
    """The role shuffle ignores who the person is: over 1000 seeds both genders become the boss at about their share."""
    gender = {en: g for v in load_names()["regions"].values() for en, _, g in v["first"]}
    boss, people = Counter(), Counter()
    for seed in range(1000):
        for p in build_case(seed, "hinglish").people:
            g = gender[p.name.split()[0]]
            people[g] += 1
            boss[g] += p.role == "boss"
    n, total = sum(boss.values()), sum(people.values())
    chi2 = sum((boss[g] - n * people[g] / total) ** 2 / (n * people[g] / total) for g in people)
    assert chi2 < 6.635  # one degree of freedom, p < 0.01


@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_culprit_region_is_not_tied_to_guilt_on_every_level(level):
    """Same audit on every practice level, by surname region: from level 2 the decoy shares the boss's first name,
    and level 2 and 4 add a fifth suspect, so first names would double-count."""
    region = {s: r for r, v in load_names()["regions"].items() for s, *_ in v["surname"]}
    draws, culprits = Counter(), Counter()
    for seed in range(400):
        case = build_level_case(seed, "en", level)
        culprit = next(q.answer for q in case.questions if q.kind == "who")
        for p in case.people:
            r = region[p.name.split()[-1]]
            draws[r] += 1
            culprits[r] += p.id == culprit
    n, total = sum(culprits.values()), sum(draws.values())
    assert n == 400
    chi2 = sum((culprits[r] - n * draws[r] / total) ** 2 / (n * draws[r] / total) for r in draws)
    assert chi2 < CHI2_CRITICAL_DF3_P001, (level, chi2, dict(culprits), dict(draws))
