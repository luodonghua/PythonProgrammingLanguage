import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("total", "expected"),
    [
        (0, (0, 0, 0, 0)),
        (59, (0, 0, 0, 59)),
        (60, (0, 0, 1, 0)),
        (3725, (0, 1, 2, 5)),
        (86_400, (1, 0, 0, 0)),
        (90_061, (1, 1, 1, 1)),
    ],
)
def test_split_seconds(total, expected):
    assert m.split_seconds(total) == expected


@pytest.mark.parametrize(
    ("total", "expected"),
    [
        (0, "0:00:00"),
        (5, "0:00:05"),
        (65, "0:01:05"),
        (3725, "1:02:05"),
        (90_061, "25:01:01"),
    ],
)
def test_clock(total, expected):
    assert m.clock(total) == expected


@pytest.mark.parametrize("name", ["split_seconds", "clock"])
def test_negative_raises(name):
    with pytest.raises(ValueError):
        getattr(m, name)(-1)
