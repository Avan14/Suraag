"""Experiment: generator quality. Hybrid + verifier vs the raw-LLM baseline, per language.

Metric: share of cases that pass every check on the first try, and after repair (<= 3 tries).
Baseline: raw mode, i.e. the same LLM writing the whole chat with no verifier in front of it, scored
by the same checks. Cases where the LLM was unavailable (quota, no key) are counted separately and
EXCLUDED from the rates, so a quota outage can never look like a generator failure.

Usage: python -m eval.run_generator --n 30 [--langs en hinglish]
"""
import argparse
import tempfile
import time
from collections import Counter
from pathlib import Path

from eval.results import merge_results
from suraag import filler as filler_module
from suraag.filler import llm_filler
from suraag.pipeline import generate_case


def run_mode(mode: str, lang: str, n: int) -> dict:
    first = final = done = unavailable = 0
    by_code: Counter = Counter()
    secs = 0.0
    for seed in range(1, n + 1):
        sources: list[str] = []

        def tracked(case, errors):
            msgs = llm_filler(case, errors)
            sources.append(filler_module.last_source)
            return msgs

        t0 = time.time()
        with tempfile.TemporaryDirectory() as tmp:
            res = generate_case(seed, lang, mode, Path(tmp) / "c", filler_fn=tracked if mode == "hybrid" else None,
                                log_path=Path(tmp) / "failures.jsonl")
        secs += time.time() - t0
        codes_first = {f.code for f in res.attempts[0].failures}
        if "llm_unavailable" in codes_first or (mode == "hybrid" and "stub" in sources):
            unavailable += 1
            continue
        done += 1
        first += not res.attempts[0].failures
        final += res.ok
        by_code.update(codes_first)
    return {"n_requested": n, "completed": done, "llm_unavailable_excluded": unavailable,
            "first_try_pass": first, "pass_after_repair": final, "failures_first_try_by_code": dict(by_code),
            "seconds_per_case": round(secs / max(done + unavailable, 1), 2)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=30)
    ap.add_argument("--langs", nargs="+", default=["en", "hinglish"])
    args = ap.parse_args()
    from eval.results import RESULTS
    import json
    old = json.loads(RESULTS.read_text("utf-8")).get("generator_quality", {}) if RESULTS.exists() else {}
    out = {**old, "note": "synthetic cases; one case family; LLM-unavailable cases excluded from the rates"}  # keep other languages
    for lang in args.langs:
        out[lang] = {m: run_mode(m, lang, args.n) for m in ("hybrid", "raw")}
        for m, r in out[lang].items():
            print(f"{lang}/{m}: first try {r['first_try_pass']}/{r['completed']}, after repair "
                  f"{r['pass_after_repair']}/{r['completed']} ({r['llm_unavailable_excluded']} excluded)")
    merge_results("generator_quality", out)


if __name__ == "__main__":
    main()
