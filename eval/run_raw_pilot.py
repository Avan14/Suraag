"""Gate 1 part B: the LLM writes the whole chat from the fixture world model (raw mode), and the
same code checks that score hybrid cases score it. Chat-only: calls come from the renderer and
the photo is not involved, so only chat failures count.

Usage: python -m eval.run_raw_pilot --n 10 --out eval/raw_pilot.json
"""
import argparse
import json
from collections import Counter
from pathlib import Path

from suraag.llm import LLMUnavailable
from suraag.parse import Artifacts
from suraag.rawmode import raw_chat
from suraag.render import render_calls
from suraag.verify import check_anchors, check_chat_consistency
from tests.helpers import load_case


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--out", type=Path, default=Path("eval/raw_pilot.json"))
    args = ap.parse_args()
    case = load_case()
    samples, by_code, unavailable = [], Counter(), 0
    for i in range(1, args.n + 1):
        try:
            chat = raw_chat(case, nonce=i)
        except LLMUnavailable as e:
            unavailable += 1
            print(f"sample {i}: LLM unavailable ({e})")
            continue
        arts = Artifacts(chat=chat, calls=render_calls(case))
        fails = [f for f in check_anchors(case, arts, "raw") + check_chat_consistency(case, arts, "raw")
                 if f.artifact == "chat"]
        by_code.update({f.code for f in fails})
        samples.append({"i": i, "codes": sorted({f.code for f in fails}), "messages": [f.message for f in fails]})
        print(f"sample {i}: {'FAILED ' + ','.join(sorted({f.code for f in fails})) if fails else 'ok'}")
    completed = len(samples)
    failed = sum(1 for s in samples if s["codes"])
    result = {"n_requested": args.n, "completed": completed, "unavailable": unavailable, "failed": failed,
              "by_code": dict(by_code), "samples": samples,
              "note": "one world model, raw mode, chat checks only, synthetic data"}
    args.out.write_text(json.dumps(result, indent=1), "utf-8")
    print(f"{failed}/{completed} failed ({unavailable} unavailable) -> {args.out}")


if __name__ == "__main__":
    main()
