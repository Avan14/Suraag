"""Tests for the photo renderer and EXIF reader."""
from suraag.parse import Artifacts, load_exif, text_at
from suraag.render import render_photo
from tests.helpers import load_case

CASE = load_case()


def test_exif_fields_round_trip():
    exif = load_exif(render_photo(CASE))
    assert exif["GPSLatitude"] == "19.0729" and exif["GPSLongitude"] == "72.8841"
    assert exif["DateTimeOriginal"] == "2026:03:04 21:40:00"
    assert exif["OffsetTimeOriginal"] == "+05:30"
    assert exif["ImageDescription"].startswith("SYNTHETIC CASE")
    assert (exif["Make"], exif["Model"]) == ("Redmi", "Note 12")


def test_photo_bytes_are_repeatable():
    assert render_photo(CASE) == render_photo(CASE)


def test_southern_and_western_coordinates_keep_their_signs():
    case = CASE.model_copy(update={"photo": CASE.photo.model_copy(update={"lat": -33.8688, "lon": -151.2093})})
    exif = load_exif(render_photo(case))
    assert exif["GPSLatitude"] == "-33.8688" and exif["GPSLongitude"] == "-151.2093"


def test_text_at_reads_exif_tags_and_missing_tag_is_none():
    arts = Artifacts(chat="x\n", calls="x\n", photo=render_photo(CASE))
    assert text_at(arts, "photo", exif_tag="GPSLatitude") == "19.0729"
    assert text_at(arts, "photo", exif_tag="NoSuchTag") is None


def test_load_exif_on_garbage_is_empty():
    assert load_exif(b"not a jpeg") == {}


def test_clean_photo_has_the_full_date_and_offset_tag_set():
    """Rule F-08: CreateDate and ModifyDate equal the capture time; every OffsetTime tag is +05:30; no Software tag."""
    exif = load_exif(render_photo(CASE))
    assert exif["CreateDate"] == exif["ModifyDate"] == exif["DateTimeOriginal"] == "2026:03:04 21:40:00"
    assert exif["OffsetTime"] == exif["OffsetTimeOriginal"] == exif["OffsetTimeDigitized"] == "+05:30"
    assert "Software" not in exif
