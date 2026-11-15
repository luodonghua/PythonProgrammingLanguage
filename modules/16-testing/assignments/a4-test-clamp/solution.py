"""Assignment 4: Write the test cases for clamp(x, low, high).

clamp limits a number to a range:
    * below low  -> returns low
    * above high -> returns high
    * otherwise  -> returns x unchanged (floats stay floats)
    * low > high -> raises ValueError   (low == high is allowed)

`clamp_cases` is a list of (x, low, high, expected) tuples. `expected` is either
the number clamp must return or the exception class (ValueError) it must raise.
Example:  (15, 0, 10, 10)   and   (1, 5, 2, ValueError)

The grader runs your cases against the functions in implementations.py:
`correct` must agree with every case, and each `bug_*` function must be caught
by at least one case. Use at least 6 cases. Read each bug to find the input
that exposes it.
"""

clamp_cases: list[tuple] = [
    (5, 0, 10, 5),            # inside the range
    (-3, 0, 10, 0),           # below
    (99, 0, 10, 10),          # above
    (0, 0, 10, 0),            # exactly on the lower edge
    (10, 0, 10, 10),          # exactly on the upper edge
    (2.5, 0, 10, 2.5),        # floats keep their fraction
    (3, 3, 3, 3),             # low == high is allowed
    (1, 5, 2, ValueError),    # low > high is an error
    (5, -5, -1, -1),          # negative range, above it
]


if __name__ == "__main__":
    import implementations

    for x, low, high, expected in clamp_cases:
        try:
            result = implementations.correct(x, low, high)
        except ValueError:
            result = ValueError
        print((x, low, high), expected, result == expected)
