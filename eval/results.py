"""Tiny helper: each experiment merges its numbers into eval/results.json (read by the Evaluation tab)."""
import json
from pathlib import Path

RESULTS = Path(__file__).parent / "results.json"


def merge_results(key: str, value: dict) -> None:
    data = json.loads(RESULTS.read_text("utf-8")) if RESULTS.exists() else {}
    data[key] = value
    RESULTS.write_text(json.dumps(data, indent=1, ensure_ascii=False), "utf-8")
