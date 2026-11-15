"""Assignment 4: Bisect to find the first bad version.

A project has versions numbered 0 to n - 1. Version 0 is the oldest. Once a bug
appears in some version, every later version has it too ("good good good BAD BAD").
You have a function is_bad(version) that is slow, so call it as few times as possible.
"""

from collections.abc import Callable


def first_bad(n: int, is_bad: Callable[[int], bool]) -> int | None:
    """Return the number of the first bad version, or None if no version is bad.

    n         how many versions there are (n >= 0).
    is_bad    is_bad(k) is True when version k has the bug.

    Use binary search (bisecting): never call is_bad more than
    n.bit_length() + 1 times. Do not call it for a number outside 0..n-1.

    first_bad(0, ...)               -> None
    first_bad(10, lambda k: k >= 6) -> 6
    first_bad(10, lambda k: False)  -> None
    """
    low, high = 0, n          # the answer is in low..high, where high means "none"
    while low < high:
        middle = (low + high) // 2
        if is_bad(middle):
            high = middle
        else:
            low = middle + 1
    return low if low < n else None


def bisect_report(n: int, is_bad: Callable[[int], bool]) -> dict:
    """Run first_bad and return a report with a count of the calls made.

    Return {"first_bad": <result of first_bad>, "calls": <how many times is_bad was called>}.
    """
    calls = 0

    def counted(version: int) -> bool:
        nonlocal calls
        calls += 1
        return is_bad(version)

    result = first_bad(n, counted)
    return {"first_bad": result, "calls": calls}


if __name__ == "__main__":
    print(bisect_report(1000, lambda k: k >= 618))
