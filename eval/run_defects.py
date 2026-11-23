"""Experiment: defect detection. 20 planted defects (4 kinds x 5 cases, English and Hinglish), no LLM needed.

Metric: share of defects the verifier catches, per type, and whether the check MEANT for that defect
caught it. Also verifies the same clean cases first, to count false positives.
Honest limit: the defects are planted by our own code, so this shows the checks work, not how often
real generators make these mistakes (see run_generator.py for that).

Usage: python -m eval.run_defects
"""
from eval.results import merge_results
from suraag.defects import EXPECTED, inject
from suraag.parse import Artifacts
from suraag.render import render_calls, render_chat, render_photo, stub_filler
from suraag.skeleton import build_case
from suraag.verify import verify

KINDS = list(EXPECTED)


def main() -> None:
    per = {k: {"n": 0, "caught_by_intended_check": 0, "caught_by_any_check": 0} for k in KINDS}
    clean_checked = false_pos = 0
    for kind in KINDS:
        for seed in range(1, 6):
            lang = "en" if seed % 2 else "hinglish"
            case = build_case(seed, lang)
            clean = Artifacts(render_chat(case, stub_filler(case)), render_calls(case), render_photo(case))
            if kind == KINDS[0]:  # verify each clean case once
                clean_checked += 1
                false_pos += bool(verify(case, clean))
            target = "calls" if kind == "unsolvable_question" or (kind == "timestamp_clash" and seed % 2 == 0) else "chat"
            codes = {f.code for f in verify(case, inject(case, clean, kind, target=target))}
            per[kind]["n"] += 1
            per[kind]["caught_by_intended_check"] += EXPECTED[kind] in codes
            per[kind]["caught_by_any_check"] += bool(codes)
    n = sum(v["n"] for v in per.values())
    result = {"n_defects": n, "per_type": per,
              "caught_by_intended_check": sum(v["caught_by_intended_check"] for v in per.values()),
              "caught_by_any_check": sum(v["caught_by_any_check"] for v in per.values()),
              "clean_cases_checked": clean_checked, "false_positives": false_pos,
              "note": "synthetic cases, defects planted by our own code, 5 per type; shows the checks work, not how often real generators err"}
    merge_results("defect_detection", result)
    print(f"{result['caught_by_intended_check']}/{n} caught by the intended check, "
          f"{result['caught_by_any_check']}/{n} by any check; {false_pos}/{clean_checked} false positives on clean cases")
    for k, v in per.items():
        print(f"  {k}: {v['caught_by_intended_check']}/{v['n']} intended, {v['caught_by_any_check']}/{v['n']} any")


if __name__ == "__main__":
    main()
