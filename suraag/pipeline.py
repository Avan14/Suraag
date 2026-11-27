"""generate_case() and the command-line entry point.

    python -m suraag.pipeline --seed 7 --lang hinglish --mode hybrid --out cases/upi-ring-007 \
        [--level 1-4] [--defect timestamp_clash] [--defect-target chat|calls] [--offline]
"""
import argparse
import os
from pathlib import Path
from typing import Callable, Literal

from suraag import filler as filler_module
from suraag.defects import EXPECTED, DefectKind
from suraag.explain import solution_markdown
from suraag.filler import llm_filler
from suraag.i18n import t
from suraag.levels import LEVELS, build_level_case
from suraag.lang import get_pack
from suraag.llm import _load_dotenv, prompt_hash
from suraag.model import Case, ChatMessage, Lang
from suraag.repair import Attempt, GenMeta, RepairResult, run

FilledBy = Callable[[Case, list[str]], list[ChatMessage]]


def brief_markdown(case: Case) -> str:
    """The student brief as a printable sheet for paper playtests. Never contains answers."""
    b = case.brief
    rows = "\n".join(f"| {s.name} | {s.phone} |" for s in b.suspects)
    places = "\n".join(f"| {p.name} | {p.lat:.4f} | {p.lon:.4f} |" for p in b.places)
    qs = "\n\n".join(f"**{q.id}. {q.text}**\n\nAnswer: ____\n\nCite (chat.txt:line, calls.csv:row or photo.jpg:tag): ____"
                     for q in b.questions)
    return f"""# Case {case.case_id}: student brief

> SYNTHETIC CASE - fictional, for teaching only. Not real data.

{b.summary}

**{t(f"level.{case.level}.name")}.** {t(f"level.{case.level}.skills")}

## Files
- chat.txt: the mule's WhatsApp-style chat export
- calls.csv: the mule's call log
- photo.jpg: one photo from the same phone

## Suspects
| Name | Phone |
|---|---|
{rows}

## Places
| Place | Latitude | Longitude |
|---|---|---|
{places}

## Questions
{qs}

## Lab team
{", ".join(b.lab_cast)}

SHA-256 hashes in manifest.json show the files are unchanged since generation, not that they are authentic.
"""


def generate_case(seed: int, lang: Lang, mode: Literal["hybrid", "raw"], out_dir, *,
                  level: int = 1, defect: DefectKind | None = None, defect_target: Literal["chat", "calls"] = "chat",
                  filler_fn: FilledBy | None = None, on_attempt: Callable[[Attempt], None] | None = None,
                  log_path: Path = Path("logs/failures.jsonl")) -> RepairResult:
    _load_dotenv()
    case = build_level_case(seed, lang, level)
    pack = get_pack(lang)
    model = os.environ.get("SURAAG_MODEL_FILLER") or "stub"
    meta = GenMeta(seed=seed, model="stub", prompt_hashes={"filler": prompt_hash(pack.filler_prompt),
                                                           "raw": prompt_hash(pack.raw_prompt)},
                   mode=mode, lang=lang)
    use_llm = filler_fn is None
    base = filler_fn or llm_filler

    def tracked(c: Case, errors: list[str]) -> list[ChatMessage]:
        msgs = base(c, errors)
        # Record what actually wrote the filler: the manifest must not claim an LLM that was offline.
        meta.model = model if use_llm and filler_module.last_source == "llm" else "stub"
        return msgs

    if mode == "raw":
        meta.model = model
    res = run(case, filler_fn=tracked, meta=meta, out_dir=out_dir, mode=mode, defect=defect,
              defect_target=defect_target, log_path=log_path, on_attempt=on_attempt)
    if res.ok:
        out = Path(out_dir)
        (out / "case.json").write_text(case.model_dump_json(indent=2), "utf-8")  # the answer key
        (out / "brief.json").write_text(case.brief.model_dump_json(indent=2), "utf-8")
        (out / "brief.md").write_text(brief_markdown(case), "utf-8")
        (out / "solution.md").write_text(solution_markdown(case, res.arts), "utf-8")  # instructor only, like case.json
    return res


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Generate one verified Suraag case.")
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--lang", choices=["en", "hinglish"], default="hinglish")
    ap.add_argument("--mode", choices=["hybrid", "raw"], default="hybrid")
    ap.add_argument("--level", type=int, choices=sorted(LEVELS), default=1, help="practice level (suraag/levels.py)")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--defect", choices=list(EXPECTED))
    ap.add_argument("--defect-target", choices=["chat", "calls"], default="chat")
    ap.add_argument("--offline", action="store_true", help="never call the LLM; use cached replies or stub filler")
    args = ap.parse_args(argv)
    if args.offline:
        os.environ["SURAAG_OFFLINE"] = "1"

    def show(a: Attempt) -> None:
        verdict = "pass" if not a.failures else "; ".join(f.message for f in a.failures)
        print(f"attempt {a.n} ({a.action}): {verdict}")

    res = generate_case(args.seed, args.lang, args.mode, args.out, level=args.level, defect=args.defect,
                        defect_target=args.defect_target, on_attempt=show)
    if res.ok:
        print(f"SEALED {args.out}")
        return 0
    print("DISCARDED (" + ", ".join(sorted({f.code for f in res.attempts[-1].failures})) + ")")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
