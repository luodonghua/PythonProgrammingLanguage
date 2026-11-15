"""Assignment 2: Business days.

A business day is Monday to Friday that is not in the `holidays` set.
"""

from collections.abc import Collection
from datetime import date, timedelta


def is_business_day(day: date, holidays: Collection[date] = ()) -> bool:
    """Return True if `day` is Monday to Friday and not in `holidays`."""
    return day.weekday() < 5 and day not in holidays


def business_days_between(start: date, end: date, holidays: Collection[date] = ()) -> int:
    """Count the business days from `start` up to but not including `end`.

    If `end` is on or before `start`, return 0.
    """
    days = (end - start).days
    return sum(
        is_business_day(start + timedelta(days=offset), holidays)
        for offset in range(max(days, 0))
    )


def add_business_days(start: date, n: int, holidays: Collection[date] = ()) -> date:
    """Return the date that is `n` business days after `start` (n >= 0).

    `start` itself does not count. add_business_days(friday, 1) is the next
    Monday (unless that Monday is a holiday). With n == 0 return `start`
    unchanged, even if it is not a business day.
    Raise ValueError if n is negative.
    """
    if n < 0:
        raise ValueError("n must not be negative")
    current = start
    remaining = n
    while remaining > 0:
        current += timedelta(days=1)
        if is_business_day(current, holidays):
            remaining -= 1
    return current


if __name__ == "__main__":
    print(business_days_between(date(2025, 3, 3), date(2025, 3, 10)))
    print(add_business_days(date(2025, 3, 7), 1))
