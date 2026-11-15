from datetime import date

import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("birthday", "today", "age"),
    [
        (date(2000, 6, 15), date(2025, 6, 14), 24),
        (date(2000, 6, 15), date(2025, 6, 15), 25),
        (date(2000, 6, 15), date(2025, 12, 31), 25),
        (date(2000, 1, 1), date(2025, 1, 1), 25),
        (date(2024, 5, 1), date(2024, 12, 1), 0),
        (date(2000, 2, 29), date(2025, 2, 28), 24),
        (date(2000, 2, 29), date(2025, 3, 1), 25),
        (date(2000, 2, 29), date(2024, 2, 29), 24),
    ],
)
def test_age_on(birthday, today, age):
    assert m.age_on(birthday, today) == age


def test_age_before_birth_raises():
    assert m.age_on(date(2000, 1, 1), date(2000, 1, 2)) == 0
    with pytest.raises(ValueError):
        m.age_on(date(2000, 1, 2), date(2000, 1, 1))


@pytest.mark.parametrize(
    ("birthday", "today", "expected"),
    [
        (date(1990, 8, 20), date(2025, 3, 1), date(2025, 8, 20)),
        (date(1990, 8, 20), date(2025, 8, 20), date(2025, 8, 20)),
        (date(1990, 8, 20), date(2025, 8, 21), date(2026, 8, 20)),
        (date(2000, 2, 29), date(2025, 1, 1), date(2025, 3, 1)),
        (date(2000, 2, 29), date(2025, 3, 2), date(2026, 3, 1)),
        (date(2000, 2, 29), date(2027, 3, 2), date(2028, 2, 29)),
    ],
)
def test_next_birthday(birthday, today, expected):
    assert m.next_birthday(birthday, today) == expected


@pytest.mark.parametrize(
    ("birthday", "today", "days"),
    [
        (date(1990, 8, 20), date(2025, 8, 20), 0),
        (date(1990, 8, 20), date(2025, 8, 19), 1),
        (date(1990, 8, 20), date(2025, 8, 21), 364),
        (date(1990, 1, 1), date(2024, 12, 31), 1),
        (date(2000, 2, 29), date(2025, 2, 27), 2),
    ],
)
def test_days_until_birthday(birthday, today, days):
    assert m.days_until_birthday(birthday, today) == days
