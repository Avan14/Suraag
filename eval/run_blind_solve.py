"""Experiment: blind solve (unscored). A DIFFERENT model than the filler gets only what a student gets
(the brief and the three files) and answers the questions; we report agreement with the key.
It shows whether a reader other than our rule-based solver can solve the case; it never changes a case.

Usage: python -m eval.run_blind_solve --n 10
"""
import argparse
import json
import os
import tempfile
from pathlib import Path

from eval.results import merge_results
from suraag.grade import answer_matches
from suraag.llm import LLMUnavailable, _load_dotenv, complete
from suraag.parse import Artifacts, load_exif
from suraag.pipeline import generate_case
from suraag.render import stub_filler
from suraag.skeleton import build_case

PROMPT = """You are a student solving a fictional forensic exercise. Use only the material below.

BRIEF
{summary}
Suspects: {suspects}
Places: {places}
Questions:
{questions}

chat.txt
{chat}

calls.csv
{calls}

photo.jpg EXIF values
{exif}

Reply with only JSON: {{"Q1": "<suspect id>", "Q2": "<time like 9:14 pm>", "Q3": "<place id>"}}"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=10)
    args = ap.parse_args()
    _load_dotenv()
    model = os.environ.get("SURAAG_MODEL_SOLVER")
    per_q = {"who": [0, 0], "when": [0, 0], "where": [0, 0]}
    done = unavailable = 0
    for seed in range(1, args.n + 1):
        lang = "en" if seed % 2 else "hinglish"
        case = build_case(seed, lang)
        with tempfile.TemporaryDirectory() as tmp:
            res = generate_case(seed, lang, "hybrid", Path(tmp) / "c", filler_fn=lambda c, e: stub_filler(c),
                                log_path=Path(tmp) / "f.jsonl")
            arts: Artifacts = res.arts
        b = case.brief
        prompt = PROMPT.format(
            summary=b.summary, suspects="; ".join(f"{s.id} {s.name} {s.phone}" for s in b.suspects),
            places="; ".join(f"{p.id} {p.name} ({p.lat}, {p.lon})" for p in b.places),
            questions="\n".join(f"{q.id}. {q.text}" for q in b.questions),
            chat=arts.chat, calls=arts.calls, exif=json.dumps(load_exif(arts.photo)))
        try:
            raw = complete(prompt, model=model, max_tokens=4096)
            answers = json.loads(raw[raw.find("{"):raw.rfind("}") + 1])
        except (LLMUnavailable, ValueError) as e:
            unavailable += 1
            print(f"case {seed}: skipped ({e})")
            continue
        done += 1
        for q in case.questions:
            per_q[q.kind][1] += 1
            per_q[q.kind][0] += answer_matches(case, q, str(answers.get(q.id, "")))
    result = {"model": model, "n_requested": args.n, "completed": done, "skipped": unavailable,
              "agreement_with_key": {k: {"agree": a, "of": n} for k, (a, n) in per_q.items()},
              "note": "unscored, answers only; the files were rendered with offline stub filler"}
    merge_results("blind_solve", result)
    print(result["agreement_with_key"])


if __name__ == "__main__":
    main()
