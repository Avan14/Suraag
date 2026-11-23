"""Experiment: grader agreement with a HUMAN's manual grading, per check, against a baseline.

Reads eval/answers.json after the human has filled `label_answer_correct` and `label_citation_valid`.
Baseline for the citation check: exact string match alone, i.e. valid only when the student cited exactly
the designated anchor locations and nothing else. Unlabelled entries are skipped and counted.

Usage: python -m eval.run_grader_agreement
"""
import json
from pathlib import Path

from eval.make_answers import arts_for
from eval.results import merge_results
from suraag.grade import Citation, Claim, grade_claim
from suraag.skeleton import build_case


def anchor_locs(case, q) -> set:
    return {(a.artifact, a.line, a.row, a.exif_tag) for fid in q.answer_facts for a in case.fact(fid).anchors}


def main() -> None:
    entries = json.loads(Path("eval/answers.json").read_text("utf-8"))
    agree = {"answer_correct": 0, "citation_valid": 0, "citation_valid_baseline": 0}
    n = skipped = 0
    for e in entries:
        if e["label_answer_correct"] is None or e["label_citation_valid"] is None:
            skipped += 1
            continue
        case = build_case(e["seed"], e["lang"])
        c = e["claim"]
        claim = Claim(c["question_id"], c["answer"], tuple(Citation(**x) for x in c["citations"]))
        res = grade_claim(case, arts_for(case), claim)
        q = next(x for x in case.questions if x.id == c["question_id"])
        cited = {(x["artifact"], x.get("line"), x.get("row"), x.get("exif_tag")) for x in c["citations"]}
        n += 1
        agree["answer_correct"] += res.answer_correct == e["label_answer_correct"]
        agree["citation_valid"] += res.citation_valid == e["label_citation_valid"]
        agree["citation_valid_baseline"] += (cited == anchor_locs(case, q)) == e["label_citation_valid"]
    if n == 0:
        print("No labelled answers yet: fill label_answer_correct / label_citation_valid in eval/answers.json first. Nothing written.")
        return
    result = {"n_labelled": n, "n_unlabelled_skipped": skipped, "agreement": agree,
              "note": "labelled by one person unless a second label column was added; synthetic answers; small n"}
    merge_results("grader_agreement", result)
    print(result)


if __name__ == "__main__":
    main()
