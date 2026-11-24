"""Draft about 20 student answers, some deliberately wrong, and a worksheet to label them BY HAND.

Writes eval/answers.json (labels left null) and eval/grader_worksheet.md (what each cited line says).
The labels must be a human's: read each cited line, then say whether the answer is correct and whether
the citations support it, using the rule in the worksheet. Cases are rebuilt from seed + language with
real-filler replies from the committed cache (run with SURAAG_OFFLINE=1), so the lines a labeller reads are the lines in cases/.

Usage: python -m eval.make_answers
"""
import json
from pathlib import Path

from suraag.parse import Artifacts, text_at
from suraag.render import render_calls, render_chat, render_photo, stub_filler
from suraag.skeleton import build_case

SCENARIOS = ["right", "wrong_line", "wrong_answer", "missing_artifact", "nonexistent", "extra_line",
             "irrelevant_artifact", "no_citation", "partial_line", "right"]


def arts_for(case) -> Artifacts:
    """The shipped files: real LLM filler replayed from the committed cache through the repair loop."""
    import tempfile
    from suraag.filler import llm_filler
    from suraag.pipeline import generate_case
    with tempfile.TemporaryDirectory() as tmp:
        res = generate_case(case.seed, case.lang, "hybrid", Path(tmp) / "c", filler_fn=llm_filler,
                            log_path=Path(tmp) / "f.jsonl")
    assert res.ok, f"seed {case.seed}: not replayable from the cache"
    return res.arts


def cit(a):
    return {"artifact": a.artifact, **{k: v for k, v in (("line", a.line), ("row", a.row), ("exif_tag", a.exif_tag)) if v is not None}}


def build(case, q, scenario, arts):
    anchors = [a for fid in q.answer_facts for a in case.fact(fid).anchors]
    answer, cites = q.answer, [cit(a) for a in anchors]
    if q.kind == "when":
        from suraag.timefmt import chat_time
        from datetime import datetime
        answer = chat_time(datetime.fromisoformat(q.answer))
    wrong_ans = {"who": next(s.id for s in case.brief.suspects if s.id != q.answer),
                 "when": "11:55 pm", "where": next(p.id for p in case.places if p.id != q.answer)}[q.kind]
    if scenario == "wrong_answer":
        answer = wrong_ans
    elif scenario == "wrong_line":
        cites = [{"artifact": "chat", "line": 2}] + [c for c in cites if c["artifact"] != "chat"]
    elif scenario == "missing_artifact":
        cites = cites[:1]
    elif scenario == "nonexistent":
        cites = cites + [{"artifact": "chat", "line": 999}]
    elif scenario == "extra_line":
        cites = cites + [{"artifact": "chat", "line": 2}]
    elif scenario == "irrelevant_artifact":
        cites = cites + [{"artifact": "photo", "exif_tag": "Make"}]
    elif scenario == "no_citation":
        cites = []
    elif scenario == "partial_line":
        cites = [dict(c) for c in cites]
        for c in cites:
            if c["artifact"] == "chat":
                c["line"] = case.chat_anchors[0].line + 1
    return {"question_id": q.id, "answer": answer, "citations": cites, "scenario": scenario}


def main() -> None:
    entries, sheet = [], ["# Grader worksheet: label these by hand\n",
                          "Rule. **Answer correct:** the answer is what the evidence supports (a time within 2 minutes counts).",
                          "**Evidence valid:** every file the question needs has at least one cited line that contains ALL the",
                          "strings needed for the claim, and NO cited line is wrong (a line is wrong if it contains none of them,",
                          "does not exist, or is in a file this question does not use). A line with only some of the strings",
                          "neither earns nor costs. Extra lines that genuinely support the claim are fine.\n",
                          "Fill `label_answer_correct` and `label_citation_valid` (true/false) in eval/answers.json for each entry.\n"]
    i = 0
    for seed in range(1, 11):
        lang = "en" if seed % 2 else "hinglish"
        case = build_case(seed, lang)
        arts = arts_for(case)
        for q in case.questions[:2] if seed % 2 else case.questions[1:]:
            i += 1
            if i > 20:
                break
            claim = build(case, q, SCENARIOS[(i - 1) % len(SCENARIOS)], arts)
            entries.append({"id": i, "seed": seed, "lang": lang, "claim": claim,
                            "label_answer_correct": None, "label_citation_valid": None})
            sheet.append(f"## Answer {i}: case {case.case_id} ({lang}), {q.id} ({q.kind})\n")
            sheet.append(f"Question: {q.text}  \nStudent answer: `{claim['answer']}`\n")
            facts = [a for fid in q.answer_facts for a in case.fact(fid).anchors]
            sheet.append("Strings the claim needs: " + "; ".join(
                f"{a.artifact}: " + " + ".join(repr(m) for m in a.must_contain) for a in facts) + "\n")
            sheet.append("Cited lines:")
            for c in claim["citations"] or [None]:
                if c is None:
                    sheet.append("- (no citations)")
                    continue
                text = text_at(arts, c["artifact"], line=c.get("line"), row=c.get("row"), exif_tag=c.get("exif_tag"))
                sheet.append(f"- {c['artifact']} {c.get('line') or c.get('row') or c.get('exif_tag')}: `{text}`")
            sheet.append("")
    Path("eval/answers.json").write_text(json.dumps(entries, indent=1, ensure_ascii=False), "utf-8")
    Path("eval/grader_worksheet.md").write_text("\n".join(sheet), "utf-8")
    print(f"wrote {len(entries)} answers to eval/answers.json and eval/grader_worksheet.md")


if __name__ == "__main__":
    main()
