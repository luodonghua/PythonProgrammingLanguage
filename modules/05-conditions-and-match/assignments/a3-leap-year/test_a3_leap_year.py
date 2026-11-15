import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("year", "expected"),
    [(1996, True), (2024, True), (1900, False), (2000, True), (2023, False), (2100, False)],
)
def test_is_leap_year(year, expected):
    assert m.is_leap_year(year) is expected


@pytest.mark.parametrize(
    ("year", "month", "days"),
    [(2023, 1, 31), (2023, 4, 30), (2023, 2, 28), (2024, 2, 29), (2023, 12, 31), (2023, 11, 30)],
)
def test_days_in_month(year, month, days):
    assert m.days_in_month(year, month) == days


@pytest.mark.parametrize("month", [0, 13, -1])
def test_bad_month(month):
    with pytest.raises(ValueError):
        m.days_in_month(2023, month)
