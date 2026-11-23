"""Gate 1: ask a plain LLM for whole cases (chat, call log, EXIF, answer key) to hand-check.

Usage: python -m eval.run_plain_baseline --n 10 --out eval/plain_baseline
Score each case with eval/baseline_rubric.md into <out>/scores.csv.
"""
import argparse
import csv
from pathlib import Path

from suraag.llm import LLMUnavailable, complete

PLAIN_PROMPT = """Create a fictional Indian UPI-fraud forensic training case for university students.
Include:
1. A WhatsApp-style group chat export in Hinglish, about 25 numbered lines, each with a date and time.
2. A call log as CSV with columns row,datetime,direction,number,contact_name,duration_s (about 6 rows).
3. The EXIF metadata of one photo: DateTimeOriginal and GPS coordinates.
4. A list of 3 candidate places with coordinates.
5. Three questions: who instructed deleting the transfer record, when, and where the mule was when the photo was taken.
6. An answer key that cites the exact chat line numbers and call-log rows supporting each answer.
Include at least one plausible wrong suspect. All names fictional; all phone numbers must start with +91-5."""

COLUMNS = ["case", "R1", "R2", "R3", "R4", "R5", "R6", "broken", "checker", "notes"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--out", type=Path, default=Path("eval/plain_baseline"))
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for i in range(1, args.n + 1):
        path = args.out / f"case_{i:02d}.md"
        if path.exists():
            print(f"skip {path} (exists)")
            continue
        try:  # the nonce makes each request distinct, so the cache doesn't return case 1 ten times
            text = complete(f"{PLAIN_PROMPT}\n\nnonce: {i}")
        except LLMUnavailable as e:
            print(f"case {i}: FAILED ({e}); rerun later to fill the gap")
            continue
        path.write_text(text, "utf-8")
        print(f"wrote {path}")
    scores = args.out / "scores.csv"
    if not scores.exists():
        with scores.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(COLUMNS)
            for i in range(1, args.n + 1):
                w.writerow([f"case_{i:02d}"] + [""] * (len(COLUMNS) - 1))
        print(f"wrote blank {scores}")


if __name__ == "__main__":
    main()
