"""Each planted defect must be caught by the check meant for it."""
import pytest

from suraag.defects import EXPECTED, inject
from suraag.parse import Artifacts
from suraag.render import render_calls, render_chat, render_photo, stub_filler
from suraag.skeleton import build_case
from suraag.verify import verify
from tests.helpers import load_case

KINDS = list(EXPECTED)


def arts_from(case) -> Artifacts:
    return Artifacts(chat=render_chat(case, stub_filler(case)), calls=render_calls(case), photo=render_photo(case))


def cases():
    yield "fixture", load_case()
    for lang in ("en", "hinglish"):
        for seed in range(1, 6):
            yield f"{lang}-{seed}", build_case(seed, lang)


@pytest.mark.parametrize("kind,target", [("timestamp_clash", "chat"), ("timestamp_clash", "calls"),
                                         ("alias_conflict", "chat"), ("missing_anchor", "chat"),
                                         ("unsolvable_question", "calls")])
def test_defect_is_caught_by_its_intended_check(kind, target):
    for name, case in cases():
        clean = arts_from(case)
        assert verify(case, clean) == [], name
        bad = inject(case, clean, kind, target=target)
        assert EXPECTED[kind] in [f.code for f in verify(case, bad)], f"{name}: {kind}/{target} not caught"


def test_inject_returns_new_artifacts_and_leaves_the_input_alone():
    case = load_case()
    clean = arts_from(case)
    before = (clean.chat, clean.calls)
    bad = inject(case, clean, "missing_anchor")
    assert (clean.chat, clean.calls) == before and bad.chat != clean.chat


def test_clash_target_changes_only_the_named_artifact():
    case = load_case()
    clean = arts_from(case)
    assert inject(case, clean, "timestamp_clash", target="calls").chat == clean.chat
    assert inject(case, clean, "timestamp_clash", target="chat").calls == clean.calls


def test_four_defect_kinds_exist():
    assert KINDS == ["timestamp_clash", "alias_conflict", "missing_anchor", "unsolvable_question"]
