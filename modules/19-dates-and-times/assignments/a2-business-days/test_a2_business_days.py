from datetime import date

import pytest

from practice import load

m = load(__file__)

MON = date(2025, 3, 3)
FRI = date(2025, 3, 7)
SAT = date(2025, 3, 8)
SUN = date(2025, 3, 9)
NEXT_MON = date(2025, 3, 10)


def test_is_business_day():
    assert m.is_business_day(MON) is True
    assert m.is_business_day(FRI) is True
    assert m.is_business_day(SAT) is False
    assert m.is_business_day(SUN) is False


def test_holiday_is_not_business_day():
    assert m.is_business_day(MON, {MON}) is False
    assert m.is_business_day(FRI, {MON}) is True


def test_between_one_week():
    assert m.business_days_between(MON, NEXT_MON) == 5


def test_between_excludes_end_includes_start():
    assert m.business_days_between(MON, date(2025, 3, 4)) == 1
    assert m.business_days_between(MON, MON) == 0


def test_between_weekend_only():
    assert m.business_days_between(SAT, NEXT_MON) == 0


def test_between_reversed_is_zero():
    assert m.business_days_between(NEXT_MON, MON) == 0
    assert m.business_days_between(MON, NEXT_MON) == 5


def test_between_with_holidays():
    assert m.business_days_between(MON, NEXT_MON, {date(2025, 3, 5), SAT}) == 4


def test_between_long_range():
    assert m.business_days_between(date(2025, 1, 1), date(2026, 1, 1)) == 261


def test_add_over_weekend():
    assert m.add_business_days(FRI, 1) == NEXT_MON
    assert m.add_business_days(MON, 5) == NEXT_MON
    assert m.add_business_days(SAT, 1) == NEXT_MON


def test_add_zero_returns_start():
    assert m.add_business_days(SAT, 0) == SAT
    assert m.add_business_days(MON, 0) == MON


def test_add_skips_holidays():
    assert m.add_business_days(FRI, 1, {NEXT_MON}) == date(2025, 3, 11)


def test_add_negative_raises():
    assert m.add_business_days(MON, 1) == date(2025, 3, 4)
    with pytest.raises(ValueError):
        m.add_business_days(MON, -1)
