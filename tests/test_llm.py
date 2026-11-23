"""Tests for llm."""
import os

import pytest

from suraag import llm


class FakeModels:
    def __init__(self, text="hello"):
        self.calls = 0
        self.text = text

    def generate_content(self, *, model, contents, config=None):
        self.calls += 1
        return type("R", (), {"text": self.text})()


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # no .env here, so the real key is never loaded
    monkeypatch.setenv("SURAAG_LLM_CACHE", str(tmp_path / "cache"))
    monkeypatch.setenv("SURAAG_MODEL_FILLER", "fake-model")
    monkeypatch.delenv("SURAAG_OFFLINE", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    return tmp_path


def test_second_identical_call_hits_cache(env, monkeypatch):
    fake = FakeModels()
    monkeypatch.setattr(llm, "_get_client", lambda: type("C", (), {"models": fake})())
    assert llm.complete("hi") == "hello"
    assert llm.complete("hi") == "hello"
    assert fake.calls == 1


def test_offline_cache_miss_raises(env, monkeypatch):
    monkeypatch.setenv("SURAAG_OFFLINE", "1")
    with pytest.raises(llm.LLMUnavailable):
        llm.complete("never cached")


def test_missing_key_raises(env):
    with pytest.raises(llm.LLMUnavailable):
        llm.complete("hi")


def test_daily_quota_fails_fast_without_retrying(env, monkeypatch):
    from google.genai import errors

    class Quota:
        calls = 0

        def generate_content(self, **kw):
            Quota.calls += 1
            raise errors.ClientError(429, {"error": {"code": 429, "message": "Generate content requests per day limit exceeded on Free Tier"}})

    monkeypatch.setattr(llm, "_get_client", lambda: type("C", (), {"models": Quota()})())
    with pytest.raises(llm.LLMUnavailable, match="daily quota"):
        llm.complete("hi")
    assert Quota.calls == 1


def test_empty_response_raises(env, monkeypatch):
    fake = FakeModels(text="")
    monkeypatch.setattr(llm, "_get_client", lambda: type("C", (), {"models": fake})())
    with pytest.raises(llm.LLMUnavailable):
        llm.complete("hi")


def test_prompt_hash_is_short_and_stable():
    assert llm.prompt_hash("abc") == llm.prompt_hash("abc")
    assert len(llm.prompt_hash("abc")) == 12


@pytest.mark.live
def test_model_id_works():
    llm._load_dotenv()
    if not os.environ.get("GEMINI_API_KEY"):
        pytest.skip("no GEMINI_API_KEY")
    os.environ["SURAAG_OFFLINE"] = "0"
    assert llm.complete("Reply with the single word OK.", max_tokens=2000).strip()
