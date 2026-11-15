from datetime import UTC, datetime

import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("text", "src", "dst", "expected"),
    [
        ("2025-03-14 09:00", "America/New_York", "Europe/Paris", "2025-03-14T14:00+01:00"),
        ("2025-03-14 09:00", "UTC", "Asia/Tokyo", "2025-03-14T18:00+09:00"),
        ("2025-07-04 15:00", "America/New_York", "Asia/Tokyo", "2025-07-05T04:00+09:00"),
        ("2025-12-31 23:30", "Europe/London", "UTC", "2025-12-31T23:30+00:00"),
        ("2025-07-01 12:00", "Europe/London", "Europe/Paris", "2025-07-01T13:00+02:00"),
        ("2025-01-01 00:15", "Asia/Kolkata", "UTC", "2024-12-31T18:45+00:00"),
    ],
)
def test_convert_time(text, src, dst, expected):
    assert m.convert_time(text, src, dst) == expected


@pytest.mark.parametrize("bad", ["", "2025-03-14", "14/03/2025 09:00", "2025-13-01 09:00"])
def test_convert_time_bad_text(bad):
    assert m.convert_time("2025-03-14 09:00", "UTC", "UTC") == "2025-03-14T09:00+00:00"
    with pytest.raises(ValueError):
        m.convert_time(bad, "UTC", "UTC")


def test_to_utc():
    result = m.to_utc("2025-03-14 09:00", "America/New_York")
    assert result == datetime(2025, 3, 14, 13, 0, tzinfo=UTC)
    assert result.utcoffset().total_seconds() == 0
    assert result.tzinfo is UTC


def test_to_utc_winter_and_summer_offsets_differ():
    winter = m.to_utc("2025-01-15 12:00", "America/New_York")
    summer = m.to_utc("2025-07-15 12:00", "America/New_York")
    assert winter.hour == 17
    assert summer.hour == 16


@pytest.mark.parametrize(
    ("start", "end", "zone", "hours"),
    [
        ("2025-03-09 00:00", "2025-03-10 00:00", "America/New_York", 23.0),
        ("2025-11-02 00:00", "2025-11-03 00:00", "America/New_York", 25.0),
        ("2025-06-01 00:00", "2025-06-02 00:00", "America/New_York", 24.0),
        ("2025-06-01 08:00", "2025-06-01 09:30", "Europe/Paris", 1.5),
        ("2025-06-02 00:00", "2025-06-01 00:00", "Europe/Paris", -24.0),
        ("2025-03-30 00:00", "2025-03-31 00:00", "Europe/Paris", 23.0),
    ],
)
def test_elapsed_hours(start, end, zone, hours):
    assert m.elapsed_hours(start, end, zone) == hours
