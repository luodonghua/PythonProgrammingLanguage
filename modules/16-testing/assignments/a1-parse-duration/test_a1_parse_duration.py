import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("text", "seconds"),
    [
        ("0s", 0),
        ("90s", 90),
        ("5m", 300),
        ("2h", 7200),
        ("1d", 86400),
        ("1h30m", 5400),
        ("1m1s", 61),
        ("2d4h", 187200),
        ("1d1h1m1s", 90061),
        ("  10m  ", 600),
        ("007s", 7),
    ],
)
def test_valid_durations(text, seconds):
    assert m.parse_duration(text) == seconds


@pytest.mark.parametrize(
    "text",
    [
        "",
        "   ",
        "10",
        "m",
        "5x",
        "1h1h",
        "30m1h",
        "1h 30m",
        "-5s",
        "1.5h",
        "5M",
        "1h30",
        "abc",
    ],
)
def test_invalid_durations_raise_value_error(text):
    with pytest.raises(ValueError):
        m.parse_duration(text)


def test_result_is_an_int():
    assert type(m.parse_duration("1m")) is int
