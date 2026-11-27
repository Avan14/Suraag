"""Experiment: blind solve (unscored). A DIFFERENT model than the filler gets only what a student gets
(the brief and the three files) and answers the questions; we report agreement with the key.
It shows whether a reader other than our rule-based solver can solve the case; it never changes a case.

Usage: python -m eval.run_blind_solve --n 10
       python -m eval.run_blind_solve --cases cases/*/     (shipped cases, per level, with trap counts)
"""
import argparse
import json
import os
import tempfile
from pathlib import Path

from eval.results import merge_results
from suraag import filler as filler_module
from suraag.filler import llm_filler
from suraag.grade import answer_matches
from suraag.llm import LLMUnavailable, _load_dotenv, complete
from suraag.parse import Artifacts, load_exif
from suraag.pipeline import generate_case
from suraag.render import stub_filler
from suraag.model import Case
from suraag.skeleton import build_case
from suraag.solver import UNSOLVABLE, shortcut_answers

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


REPLY = {"who": "<suspect id>", "when": "<time like 9:14 pm>", "where": "<place id>"}


def _prompt(case: Case, arts: Artifacts) -> str:
    b = case.brief
    reply = ", ".join(f'"{q.id}": "{REPLY[q.kind]}"' for q in b.questions)
    return PROMPT.rsplit("Reply with only JSON", 1)[0].format(
        summary=b.summary, suspects="; ".join(f"{s.id} {s.name} {s.phone}" for s in b.suspects),
        places="; ".join(f"{p.id} {p.name} ({p.lat}, {p.lon})" for p in b.places),
        questions="\n".join(f"{q.id}. {q.text}" for q in b.questions),
        chat=arts.chat, calls=arts.calls, exif=json.dumps(load_exif(arts.photo))) + "Reply with only JSON: {" + reply + "}"


def solve_dirs(dirs: list[Path], model: str | None) -> None:
    """Blind solve of shipped case folders: agreement per level, and how often the model gave the exact
    wrong answer a level's trap is built to produce (the shortcut answer verify.check_depth computes)."""
    per_level: dict[int, dict] = {}
    for d in dirs:
        case = Case.model_validate_json((d / "case.json").read_text("utf-8"))
        arts = Artifacts.from_dir(d)
        try:
            raw = complete(_prompt(case, arts), model=model, max_tokens=8192)
            answers = json.loads(raw[raw.find("{"):raw.rfind("}") + 1])
        except (LLMUnavailable, ValueError) as e:
            print(f"{d.name}: skipped ({e})")
            continue
        row = per_level.setdefault(case.level, {"cases": 0, "questions": 0, "agree": 0, "traps": 0, "fell_for": 0})
        row["cases"] += 1
        for q in case.questions:
            row["questions"] += 1
            row["agree"] += answer_matches(case, q, str(answers.get(q.id, "")))
        short = shortcut_answers(arts, case.brief, case.lang)
        fell = []
        for tw in case.twists:
            qid, trap = short[tw]
            q = next(x for x in case.questions if x.id == qid)
            row["traps"] += 1
            if trap != UNSOLVABLE and answer_matches(case, q, str(answers.get(qid, ""))) is False and \
                    answer_matches(case, q.model_copy(update={"answer": trap}), str(answers.get(qid, ""))):
                row["fell_for"] += 1
                fell.append(tw)
        print(f"{d.name}: level {case.level}, answers {answers}, fell for {fell or 'none'}")
    result = {"model": model, "per_level": {str(k): v for k, v in sorted(per_level.items())},
              "note": "unscored, answers only; shipped cases in cases/ with their real LLM filler; 'fell_for' counts "
                      "answers equal to the wrong answer a trap is built to produce"}
    merge_results("blind_solve_levels", result)
    print(json.dumps(result["per_level"], indent=1))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--real", action="store_true", help="use real LLM filler (skip a case if it fell back to stub)")
    ap.add_argument("--cases", type=Path, nargs="+", help="solve these shipped case folders instead")
    args = ap.parse_args()
    _load_dotenv()
    if args.cases:
        solve_dirs([d for d in args.cases if (d / "case.json").exists()], os.environ.get("SURAAG_MODEL_SOLVER"))
        return
    model = os.environ.get("SURAAG_MODEL_SOLVER")
    per_q = {"who": [0, 0], "when": [0, 0], "where": [0, 0]}
    done = unavailable = 0
    for seed in range(1, args.n + 1):
        lang = "en" if seed % 2 else "hinglish"
        case = build_case(seed, lang)
        with tempfile.TemporaryDirectory() as tmp:
            res = generate_case(seed, lang, "hybrid", Path(tmp) / "c",
                                filler_fn=llm_filler if args.real else (lambda c, e: stub_filler(c)),
                                log_path=Path(tmp) / "f.jsonl")
            arts: Artifacts = res.arts
        if args.real and (arts is None or filler_module.last_source != "llm"):
            unavailable += 1
            print(f"case {seed}: skipped (no real filler)")
            continue
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
              "note": "unscored, answers only; the files were rendered with " + ("real LLM filler" if args.real else "offline stub filler")}
    merge_results("blind_solve_real" if args.real else "blind_solve", result)
    print(result["agreement_with_key"])


if __name__ == "__main__":
    main()
