"""Assignment 2: Business days.

A business day is Monday to Friday that is not in the `holidays` set.
"""

from collections.abc import Collection
from datetime import date


def is_business_day(day: date, holidays: Collection[date] = ()) -> bool:
    """Return True if `day` is Monday to Friday and not in `holidays`."""
    # TODO: use day.weekday() (Monday is 0, Saturday is 5).
    ...


def business_days_between(start: date, end: date, holidays: Collection[date] = ()) -> int:
    """Count the business days from `start` up to but not including `end`.

    If `end` is on or before `start`, return 0.
    """
    # TODO: loop with a timedelta(days=1) step, or use a generator expression.
    ...


def add_business_days(start: date, n: int, holidays: Collection[date] = ()) -> date:
    """Return the date that is `n` business days after `start` (n >= 0).

    `start` itself does not count. add_business_days(friday, 1) is the next
    Monday (unless that Monday is a holiday). With n == 0 return `start`
    unchanged, even if it is not a business day.
    Raise ValueError if n is negative.
    """
    # TODO: step forward one day at a time and count only business days.
    ...


if __name__ == "__main__":
    print(business_days_between(date(2025, 3, 3), date(2025, 3, 10)))
    print(add_business_days(date(2025, 3, 7), 1))
