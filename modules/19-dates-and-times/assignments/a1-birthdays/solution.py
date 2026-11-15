"""Assignment 1: Age and birthday calculator.

Never call date.today() in these functions. The caller passes `today`, which
keeps the code testable.

People born on February 29 celebrate on March 1 in years that are not leap
years.
"""

from calendar import isleap
from datetime import date


def _anniversary(birthday: date, year: int) -> date:
    """The date on which `birthday` is celebrated in `year`."""
    if birthday.month == 2 and birthday.day == 29 and not isleap(year):
        return date(year, 3, 1)
    return date(year, birthday.month, birthday.day)


def age_on(birthday: date, today: date) -> int:
    """Return the age in whole years on `today`.

    The age goes up on the birthday itself. For a Feb 29 birthday in a non-leap
    year the age goes up on March 1. Return 0 if `today` is before the
    birthday's first anniversary. Raise ValueError if `today` is before
    `birthday`.
    """
    if today < birthday:
        raise ValueError("today is before the birthday")
    years = today.year - birthday.year
    if today < _anniversary(birthday, today.year):
        years -= 1
    return years


def next_birthday(birthday: date, today: date) -> date:
    """Return the date of the next birthday on or after `today`.

    If today is the birthday, return today. A Feb 29 birthday falls on March 1
    in non-leap years.
    """
    this_year = _anniversary(birthday, today.year)
    if this_year >= today:
        return this_year
    return _anniversary(birthday, today.year + 1)


def days_until_birthday(birthday: date, today: date) -> int:
    """Return how many days from `today` until the next birthday (0 if today)."""
    return (next_birthday(birthday, today) - today).days


if __name__ == "__main__":
    b = date(2000, 2, 29)
    t = date(2025, 2, 27)
    print(age_on(b, t), next_birthday(b, t), days_until_birthday(b, t))
