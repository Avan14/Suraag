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
    monkeypatch.setattr(llm, "_down_until", 0.0)
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


def test_circuit_breaker_skips_the_api_after_a_failure(env, monkeypatch):
    from google.genai import errors

    class Down:
        calls = 0

        def generate_content(self, **kw):
            Down.calls += 1
            raise errors.ServerError(503, {"error": {"code": 503, "message": "overloaded"}})

    monkeypatch.setattr(llm, "_get_client", lambda: type("C", (), {"models": Down()})())
    monkeypatch.setattr(llm.time, "sleep", lambda s: None)
    with pytest.raises(llm.LLMUnavailable):
        llm.complete("first")
    after_first = Down.calls
    assert after_first == 2  # one retry, then give up
    with pytest.raises(llm.LLMUnavailable, match="moment ago"):
        llm.complete("second")
    assert Down.calls == after_first  # the breaker was open: no new API call


def test_patient_mode_waits_out_an_overloaded_api_and_never_opens_the_breaker(env, monkeypatch):
    from google.genai import errors

    class Flaky:
        calls = 0

        def generate_content(self, **kw):
            Flaky.calls += 1
            if Flaky.calls < 4:
                raise errors.ServerError(503, {"error": {"code": 503, "message": "high demand"}})
            return type("R", (), {"text": "finally"})()

    sleeps = []
    monkeypatch.setenv("SURAAG_LLM_PATIENT", "1")
    monkeypatch.setattr(llm, "_get_client", lambda: type("C", (), {"models": Flaky()})())
    monkeypatch.setattr(llm.time, "sleep", sleeps.append)
    assert llm.complete("patient") == "finally"
    assert Flaky.calls == 4 and sleeps == [5, 10, 20]  # growing waits
    assert llm._down_until == 0.0


def test_cached_replies_still_work_while_the_breaker_is_open(env, monkeypatch):
    fake = FakeModels()
    monkeypatch.setattr(llm, "_get_client", lambda: type("C", (), {"models": fake})())
    assert llm.complete("warm") == "hello"
    monkeypatch.setattr(llm, "_down_until", llm.time.time() + 999)
    assert llm.complete("warm") == "hello"


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
