"""Assignment 4: Bisect to find the first bad version.

A project has versions numbered 0 to n - 1. Version 0 is the oldest. Once a bug
appears in some version, every later version has it too ("good good good BAD BAD").
You have a function is_bad(version) that is slow, so call it as few times as possible.
"""


def first_bad(n, is_bad):
    """Return the number of the first bad version, or None if no version is bad.

    n         how many versions there are (n >= 0).
    is_bad    is_bad(k) is True when version k has the bug.

    Use binary search (bisecting): never call is_bad more than
    n.bit_length() + 1 times. Do not call it for a number outside 0..n-1.

    first_bad(0, ...)               -> None
    first_bad(10, lambda k: k >= 6) -> 6
    first_bad(10, lambda k: False)  -> None
    """
    # TODO: binary search. Keep low and high, test the middle, halve the range.
    ...


def bisect_report(n, is_bad):
    """Run first_bad and return a report with a count of the calls made.

    Return {"first_bad": <result of first_bad>, "calls": <how many times is_bad was called>}.
    """
    # TODO: wrap is_bad in a function that counts calls (nonlocal), then call first_bad.
    ...


if __name__ == "__main__":
    print(bisect_report(1000, lambda k: k >= 618))
