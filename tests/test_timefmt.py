"""Tests for timefmt."""
from datetime import datetime

import pytest

from suraag.model import IST
from suraag.timefmt import (chat_time, chat_ts, csv_hm, csv_ts, exif_ts, parse_chat_ts,
                            parse_csv_ts, parse_exif_ts)


@pytest.mark.parametrize("hh,mm,expected", [(0, 5, "12:05 am"), (12, 30, "12:30 pm"),
                                            (21, 14, "9:14 pm"), (9, 0, "9:00 am")])
def test_chat_time(hh, mm, expected):
    assert chat_time(datetime(2026, 3, 4, hh, mm, tzinfo=IST)) == expected


def test_formats_match_the_documented_examples():
    t = datetime(2026, 3, 4, 21, 14, tzinfo=IST)
    assert chat_ts(t) == "04/03/26, 9:14 pm"
    assert csv_ts(t) == "2026-03-04T21:14:00+05:30"
    assert csv_hm(t) == "21:14"
    assert exif_ts(t) == "2026:03:04 21:14:00"


def test_parse_chat_ts_accepts_narrow_nbsp():
    assert parse_chat_ts("04/03/26, 9:14 pm") == datetime(2026, 3, 4, 21, 14, tzinfo=IST)


def test_roundtrips_at_midnight_and_noon():
    for t in (datetime(2026, 3, 4, 0, 5, tzinfo=IST), datetime(2026, 3, 4, 12, 0, tzinfo=IST)):
        assert parse_chat_ts(chat_ts(t)) == t
        assert parse_csv_ts(csv_ts(t)) == t
        assert parse_exif_ts(exif_ts(t)) == t


def test_formats_convert_other_timezones_to_ist():
    from datetime import timezone
    utc = datetime(2026, 3, 4, 15, 44, tzinfo=timezone.utc)  # = 21:14 IST
    assert chat_time(utc) == "9:14 pm"


def test_parse_rejects_garbage():
    with pytest.raises(ValueError):
        parse_chat_ts("not a time")
