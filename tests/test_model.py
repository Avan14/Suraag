"""Tests for model."""
import json
from datetime import datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

from suraag.model import IST, Anchor, Case, Event, Person

FIXTURE = Path(__file__).parent / "fixtures" / "case_001" / "world.json"


def load() -> dict:
    return json.loads(FIXTURE.read_text("utf-8"))


def test_fixture_validates():
    case = Case.model_validate(load())
    assert case.filler_needed() == 22
    assert case.person("P1").saved_as == "Raju bhai"
    assert case.fact("F1").event == "E3"


def test_rejects_real_looking_phone():
    with pytest.raises(ValidationError):
        Person(id="X", name="A B", name_deva="अ ब", role="boss", aliases=["A"], phone="+91-90000-00001")


def test_rejects_naive_datetime():
    with pytest.raises(ValidationError):
        Event(id="E", t=datetime(2026, 3, 4, 21, 14), kind="call", actor="P1")


def test_alias_cannot_contain_chat_syntax():
    for bad in ("Raju: bhai", "Raju\nbhai"):
        with pytest.raises(ValidationError):
            Person(id="X", name="A B", name_deva="अ ब", role="boss", aliases=[bad], phone="+91-50000-00009")


def test_anchor_needs_exactly_one_locator():
    with pytest.raises(ValidationError):
        Anchor(artifact="chat", must_contain=["x"])
    with pytest.raises(ValidationError):
        Anchor(artifact="calls", line=1, row=2, must_contain=["x"])
    assert Anchor(artifact="photo", exif_tag="GPSLatitude", must_contain=["19.0729"]).exif_tag == "GPSLatitude"


def test_duplicate_phone_rejected():
    d = load()
    d["people"][1]["phone"] = d["people"][0]["phone"]
    with pytest.raises(ValidationError, match="phone"):
        Case.model_validate(d)


def test_duplicate_initials_rejected():
    d = load()
    d["people"][2]["name"] = "Raj Verma"  # same initials as Raju Verma
    with pytest.raises(ValidationError, match="initials"):
        Case.model_validate(d)


def test_dangling_references_rejected():
    for mutate in (lambda d: d["facts"][0].update(event="E99"),
                   lambda d: d["questions"][0].update(answer_facts=["F99"]),
                   lambda d: d["timeline"][1].update(depends_on=["E99"]),
                   lambda d: d["distractors"].append("F99"),
                   lambda d: d["questions"][0].update(answer="P99")):
        d = load()
        mutate(d)
        with pytest.raises(ValidationError):
            Case.model_validate(d)


def test_model_allows_a_fact_without_anchors_so_the_verifier_can_catch_it():
    d = load()
    d["facts"][0]["anchors"] = []
    Case.model_validate(d)  # traceability is a verifier check, not a model rule


def test_when_answer_must_be_an_aware_iso_time():
    d = load()
    d["questions"][1]["answer"] = "2026-03-04T21:14:00"  # no offset
    with pytest.raises(ValidationError, match="ISO"):
        Case.model_validate(d)
    assert datetime.fromisoformat(load()["questions"][1]["answer"]).tzinfo is not None
    assert IST.utcoffset(None).total_seconds() == 19800
