"""Cached Gemini client: complete(prompt) -> str.

Every reply is cached on disk (.llm_cache/, committed) so demo takes and eval runs replay
exactly. SURAAG_OFFLINE=1 serves only from the cache. Any failure raises LLMUnavailable,
which callers turn into the stub-filler fallback.
"""
import hashlib
import json
import os
import time
from pathlib import Path


class LLMUnavailable(Exception):
    pass


def _load_dotenv(path: str = ".env") -> None:
    """Minimal .env reader; real environment variables win."""
    p = Path(path)
    if not p.exists():
        return
    for line in p.read_text("utf-8").splitlines():
        k, sep, v = line.strip().partition("=")
        if sep and k and not k.startswith("#") and v and k not in os.environ:
            os.environ[k] = v


def prompt_hash(template: str) -> str:
    return hashlib.sha256(template.encode("utf-8")).hexdigest()[:12]


_client = None
_down_until = 0.0  # circuit breaker: after a failure, skip the API until this time (seconds since epoch)


def _get_client():
    global _client
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise LLMUnavailable("GEMINI_API_KEY is not set")
    if _client is None:
        from google import genai
        _client = genai.Client(api_key=key)
    return _client


def complete(prompt: str, *, system: str | None = None, model: str | None = None,
             max_tokens: int = 8192) -> str:
    # max_tokens is generous because Gemini's thinking tokens count against it.
    _load_dotenv()
    model = model or os.environ.get("SURAAG_MODEL_FILLER")
    if not model:
        raise LLMUnavailable("SURAAG_MODEL_FILLER is not set")
    key = hashlib.sha256(f"{model}\0{system or ''}\0{prompt}".encode("utf-8")).hexdigest()
    path = Path(os.environ.get("SURAAG_LLM_CACHE", ".llm_cache")) / f"{key}.json"
    if path.exists():
        return json.loads(path.read_text("utf-8"))["text"]
    if os.environ.get("SURAAG_OFFLINE") == "1":
        raise LLMUnavailable("offline mode and reply not cached")

    global _down_until
    patient = os.environ.get("SURAAG_LLM_PATIENT") == "1"  # batch experiments: wait out an overloaded API
    if not patient and time.time() < _down_until:
        raise LLMUnavailable("the LLM was unavailable a moment ago; using the offline fallback")
    client = _get_client()
    from google.genai import errors, types
    config = types.GenerateContentConfig(
        system_instruction=system, max_output_tokens=max_tokens,
        http_options=types.HttpOptions(timeout=20_000))
    attempts = 5 if patient else 2
    for attempt in range(attempts):
        try:
            text = client.models.generate_content(model=model, contents=prompt, config=config).text
            break
        except errors.APIError as e:  # 429 (per-minute limit) and 5xx are worth retrying
            if e.code == 429 and "per day" in (e.message or "").lower():
                _down_until = time.time() + 3600  # a daily quota will not recover soon
                raise LLMUnavailable(f"Gemini daily quota used up: {e.message}") from e
            if not (e.code == 429 or (e.code or 0) >= 500) or attempt == attempts - 1:
                _down_until = 0.0 if patient else time.time() + 300
                raise LLMUnavailable(f"Gemini API error {e.code}: {e.message}") from e
        except Exception as e:  # network errors
            if attempt == attempts - 1:
                _down_until = 0.0 if patient else time.time() + 300
                raise LLMUnavailable(f"Gemini call failed: {e}") from e
        time.sleep(5 * 2 ** attempt if patient else 3)
    if not text:
        raise LLMUnavailable("Gemini returned an empty reply")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"model": model, "system": system, "prompt": prompt, "text": text},
                               ensure_ascii=False, indent=1), "utf-8")
    return text
