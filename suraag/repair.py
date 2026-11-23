"""Verify/repair loop (max 3 repairs), sealing with SHA-256, and the failure log.

Chat failures are repaired by regenerating the LLM filler with the error messages as input.
Calls and photo are deterministic, so they are re-rendered from the clean model. Nothing is
written to disk until every check passes; a case that cannot be repaired is discarded and one
line is appended to the failure log (the data for the evaluation).
"""
import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable, Literal

from suraag.defects import DefectKind, inject
from suraag.llm import LLMUnavailable
from suraag.model import Case, ChatMessage
from suraag.parse import Artifacts
from suraag.rawmode import raw_chat
from suraag.render import FillerShortError, render_calls, render_chat, render_photo, write_artifacts
from suraag.verify import Failure, verify


@dataclass
class GenMeta:
    seed: int
    model: str
    prompt_hashes: dict[str, str]
    mode: str
    lang: str


@dataclass
class Attempt:
    n: int
    failures: list[Failure]
    action: str  # "initial", or what the repair did


@dataclass
class RepairResult:
    ok: bool
    attempts: list[Attempt] = field(default_factory=list)
    arts: Artifacts | None = None
    manifest: dict | None = None


def seal(case: Case, arts: Artifacts, meta: GenMeta, out_dir) -> dict:
    """Write the artifacts, then record their SHA-256 (integrity only, not authenticity)."""
    out = Path(out_dir)
    write_artifacts(arts, out)
    manifest = {"case_id": case.case_id, "files": arts.sha256(), "seed": meta.seed, "model": meta.model,
                "prompt_hashes": meta.prompt_hashes, "mode": meta.mode, "lang": meta.lang,
                "sealed_at": datetime.now().astimezone().isoformat(timespec="seconds")}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), "utf-8")
    return manifest


def _make_chat(case: Case, errors: list[str], mode: str,
               filler_fn: Callable[[Case, list[str]], list[ChatMessage]]) -> tuple[str | None, Failure | None]:
    try:
        return (raw_chat(case, errors) if mode == "raw" else render_chat(case, filler_fn(case, errors))), None
    except FillerShortError as e:
        return None, Failure("filler_count", "chat", "filler_short", {"needed": e.needed, "got": e.got},
                             f"chat.txt: filler has {e.got} messages, {e.needed} needed")
    except LLMUnavailable as e:
        return None, Failure("filler_count", "chat", "llm_unavailable", {}, f"chat.txt: the LLM is unavailable ({e})")


def run(case: Case, *, filler_fn: Callable[[Case, list[str]], list[ChatMessage]], meta: GenMeta, out_dir,
        mode: Literal["hybrid", "raw"] = "hybrid", defect: DefectKind | None = None,
        defect_target: Literal["chat", "calls"] = "chat", max_repairs: int = 3,
        log_path: Path = Path("logs/failures.jsonl"),
        on_attempt: Callable[[Attempt], None] | None = None) -> RepairResult:
    calls, photo = render_calls(case), render_photo(case)
    chat, chat_fail = _make_chat(case, [], mode, filler_fn)
    attempts: list[Attempt] = []

    def evaluate(n: int, action: str, first: bool) -> list[Failure]:
        if chat is None:
            failures = [chat_fail]
        else:
            arts = Artifacts(chat, calls, photo)
            if defect and first:
                arts = inject(case, arts, defect, target=defect_target)
            failures = verify(case, arts, mode)
        attempts.append(Attempt(n, failures, action))
        if on_attempt:
            on_attempt(attempts[-1])
        return failures

    failures = evaluate(1, "initial", True)
    n = 1
    while failures and n <= max_repairs and not any(f.artifact == "model" for f in failures):
        n += 1
        fix_chat = any(f.artifact == "chat" and f.code != "cross_time" for f in failures)
        fix_calls = any(f.artifact == "calls" or f.check == "solvability" for f in failures)
        fix_photo = any(f.artifact == "photo" or f.check == "solvability" for f in failures)
        if not (fix_chat or fix_calls or fix_photo):  # e.g. only a cross-artifact time clash
            fix_chat = fix_calls = fix_photo = True
        actions = []
        if fix_chat:
            chat, chat_fail = _make_chat(case, [f.message for f in failures if f.artifact == "chat"],
                                         mode, filler_fn)
            actions.append("regenerate chat (LLM)")
        if fix_calls:
            calls = render_calls(case)
            actions.append("re-render calls")
        if fix_photo and any(f.artifact == "photo" for f in failures):
            photo = render_photo(case)
            actions.append("re-render photo")
        failures = evaluate(n, " + ".join(actions) or "re-render", False)

    if failures:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"case_id": case.case_id, "mode": mode, "lang": case.lang,
                                "codes": sorted({x.code for x in failures}), "tries": len(attempts)}) + "\n")
        return RepairResult(False, attempts)
    arts = Artifacts(chat, calls, photo)
    return RepairResult(True, attempts, arts, seal(case, arts, meta, out_dir))
