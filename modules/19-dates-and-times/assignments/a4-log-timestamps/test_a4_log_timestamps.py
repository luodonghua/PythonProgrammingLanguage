from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path

import pytest

from practice import load

m = load(__file__)
LOG = Path(__file__).parent / "access.log"


def utc(*args):
    return datetime(*args, tzinfo=UTC)


def test_parse_timestamp_converts_to_utc():
    result = m.parse_timestamp("14/Mar/2025:11:15:00 +0200")
    assert result == utc(2025, 3, 14, 9, 15, 0)
    assert result.utcoffset() == timedelta(0)


def test_parse_timestamp_negative_offset():
    assert m.parse_timestamp("14/Mar/2025:08:30:00 -0100") == utc(2025, 3, 14, 9, 30)


def test_parse_timestamp_is_aware():
    assert m.parse_timestamp("01/Jan/2025:00:00:00 +0000").tzinfo is not None


@pytest.mark.parametrize("bad", ["", "bad timestamp", "2025-03-14 09:00:00", "14/Mar/2025:09:00:00"])
def test_parse_timestamp_bad(bad):
    assert m.parse_timestamp("14/Mar/2025:09:00:00 +0000") == utc(2025, 3, 14, 9)
    with pytest.raises(ValueError):
        m.parse_timestamp(bad)


def test_read_timestamps_sorted_and_filtered():
    stamps = m.read_timestamps(LOG)
    assert stamps == [
        utc(2025, 3, 14, 9, 5, 10),
        utc(2025, 3, 14, 9, 15, 0),
        utc(2025, 3, 14, 9, 30, 0),
        utc(2025, 3, 14, 9, 59, 59),
        utc(2025, 3, 14, 12, 1, 2),
    ]


def test_read_timestamps_from_tmp_file(tmp_path):
    p = tmp_path / "x.log"
    p.write_text('a [01/Feb/2025:00:00:00 +0000] b\nno brackets\nz [oops] q\n', encoding="utf-8")
    assert m.read_timestamps(p) == [utc(2025, 2, 1)]


def test_busiest_hour_from_log():
    stamps = m.read_timestamps(LOG)
    assert m.busiest_hour(stamps) == (utc(2025, 3, 14, 9), 4)


def test_busiest_hour_tie_returns_earliest():
    stamps = [utc(2025, 1, 1, 10, 5), utc(2025, 1, 1, 8, 59), utc(2025, 1, 1, 10, 20), utc(2025, 1, 1, 8, 1)]
    assert m.busiest_hour(stamps) == (utc(2025, 1, 1, 8), 2)


def test_busiest_hour_uses_utc():
    plus2 = timezone(timedelta(hours=2))
    stamps = [datetime(2025, 1, 1, 11, 10, tzinfo=plus2), utc(2025, 1, 1, 9, 50)]
    assert m.busiest_hour(stamps) == (utc(2025, 1, 1, 9), 2)


def test_busiest_hour_empty():
    assert m.busiest_hour([utc(2025, 1, 1, 1)]) == (utc(2025, 1, 1, 1), 1)
    with pytest.raises(ValueError):
        m.busiest_hour([])


def test_time_span():
    stamps = m.read_timestamps(LOG)
    assert m.time_span(stamps) == timedelta(hours=2, minutes=55, seconds=52)
    assert m.time_span([utc(2025, 1, 1)]) == timedelta(0)
    assert m.time_span([]) == timedelta(0)
    assert m.time_span([utc(2025, 1, 2), utc(2025, 1, 1)]) == timedelta(days=1)
