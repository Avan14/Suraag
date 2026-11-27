"""Rule L-05: the answer rests on the anchored lines, not on the rest of the case."""
from suraag.levels import build_level_case
from suraag.parse import Artifacts
from suraag.render import render_calls, render_chat, render_photo, stub_filler
from suraag.verify import check_insufficient_alone


def make(case) -> Artifacts:
    return Artifacts(render_chat(case, stub_filler(case)), render_calls(case), render_photo(case))


def test_every_level_needs_its_anchored_lines():
    for level in (1, 2, 3, 4):
        for lang in ("en", "hinglish"):
            for seed in range(1, 8):
                case = build_level_case(seed, lang, level)
                assert check_insufficient_alone(case, make(case)) == [], (level, lang, seed)


def test_a_copy_of_the_order_outside_the_anchors_is_caught():
    case = build_level_case(5, "en", 1)
    arts = make(case)
    order = case.chat_anchors[0]
    lines = arts.chat.split("\n")
    lines[order.line - 3] = lines[order.line - 1]  # the same order, two lines earlier, where removal cannot reach it
    fails = check_insufficient_alone(case, Artifacts("\n".join(lines), arts.calls, arts.photo))
    # "when" now leaks from the copy; "who" still needs the removed call row, so it stays out of reach
    assert [(f.code, f.params["question"]) for f in fails] == [("anchors_not_needed", "Q2")]
