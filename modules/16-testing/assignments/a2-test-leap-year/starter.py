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

# TODO: replace the empty list with your cases.
leap_year_cases: list[tuple[int, bool]] = []


if __name__ == "__main__":
    import implementations

    for year, expected in leap_year_cases:
        print(year, expected, implementations.correct(year) == expected)
