"""Assignment 1: A module with a command-line entry point.

This file is both a module (other code can `import` it and call its
functions) and a script (`python starter.py 1 2 3` prints a summary).
The `if __name__ == "__main__":` block at the bottom makes that possible.
"""

import statistics
import sys


def parse_numbers(args: list[str]) -> list[float]:
    """Convert command-line words to floats.

    parse_numbers(["1", "2.5"])  -> [1.0, 2.5]
    Raise ValueError("not a number: 'x'") for the first bad word
    (use {word!r} in the message).
    """
    # TODO: loop, call float(), and re-raise with your own message.
    ...


def summary(numbers: list[float]) -> dict:
    """Return {"count": ..., "mean": ..., "median": ..., "stdev": ...}.

    Use the `statistics` module. `stdev` is the sample standard deviation,
    or None when there are fewer than 2 numbers. Raise ValueError("no numbers")
    for an empty list.

    summary([1, 2, 3, 4])  -> {"count": 4, "mean": 2.5, "median": 2.5, "stdev": 1.2909944487358056}
    """
    # TODO: statistics.mean, statistics.median, statistics.stdev.
    ...


def format_summary(numbers: list[float]) -> str:
    """Return a one-line text: "count=4 mean=2.50 median=2.50".

    Mean and median use two decimals. Do not include the stdev.
    """
    # TODO: build the line from summary(numbers).
    ...


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point. Return the exit code (do not call sys.exit here).

    argv is the list of arguments WITHOUT the program name. If it is None,
    use sys.argv[1:].

    - no arguments      -> print "usage: numstats NUMBER [NUMBER ...]" to stderr, return 2
    - a bad number      -> print the ValueError message to stderr, return 2
    - otherwise         -> print format_summary(...) to stdout, return 0
    """
    # TODO: write it.
    ...


if __name__ == "__main__":
    raise SystemExit(main())
