"""Assignment 3: Leap years and month lengths."""


def is_leap_year(year: int) -> bool:
    """Gregorian rule: divisible by 4, except century years,
    which must be divisible by 400.

    1996 -> True, 1900 -> False, 2000 -> True, 2023 -> False
    """
    # TODO
    ...


def days_in_month(year: int, month: int) -> int:
    """Return the number of days in the month (1 = January ... 12 = December).

    Use a match statement. Hint: an or-pattern such as `case 4 | 6 | 9 | 11:`
    Raise ValueError for a month outside 1..12:  raise ValueError("bad month")
    """
    # TODO
    ...


if __name__ == "__main__":
    print(is_leap_year(2024), days_in_month(2024, 2))
