"""Assignment 2: Write the test cases.

This time YOU write the tests. `leap_year_cases` is a list of (year, expected)
pairs that describe how a leap-year function must behave, for example
(2024, True) and (2023, False).

The grader (the test file in this folder) runs your cases against several
implementations, all in implementations.py:

  * `correct` must agree with every one of your cases;
  * each of the `bug_*` functions has a different mistake, and your cases must
    catch every one of them (at least one case where the buggy function gives a
    different answer from the expected value).

Rules: use at least 5 cases, years must be positive ints, expected values must
be bools. Read the buggy functions to see which mistakes people make, then
think about which years expose each one.
"""

leap_year_cases: list[tuple[int, bool]] = [
    (2024, True),   # divisible by 4
    (2023, False),  # not divisible by 4
    (1900, False),  # century year, not divisible by 400
    (2000, True),   # divisible by 400
    (1800, False),  # catches a "divisible by 200" rule
    (1600, True),   # catches a "divisible by 1000" rule
    (4, True),
    (1, False),
]


if __name__ == "__main__":
    import implementations

    for year, expected in leap_year_cases:
        print(year, expected, implementations.correct(year) == expected)
