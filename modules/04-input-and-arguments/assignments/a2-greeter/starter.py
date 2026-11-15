"""Assignment 2: A command-line greeter with argparse.

Usage examples (after you finish the code):

    python starter.py Ada
    python starter.py Ada Lovelace --shout --times 2
    python starter.py Ada --greeting Hi
"""

import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    """Create the parser.

    * name: one or more words (nargs="+"), joined with spaces in the greeting
    * --times: int, default 1
    * --shout: flag, upper-case the greeting
    * --greeting: text, default "Hello"
    """
    # TODO: create an ArgumentParser and add the four arguments.
    ...


def main(argv: list[str] | None = None) -> int:
    """Parse argv, print the greeting `times` times (one per line), return an exit code.

    The greeting is "<greeting>, <name words joined by spaces>!"

    ["Ada"]                              prints "Hello, Ada!"
    ["Ada", "Lovelace", "--shout"]       prints "HELLO, ADA LOVELACE!"
    ["Ada", "--times", "2", "--greeting", "Hi"]
                                         prints "Hi, Ada!" twice

    If --times is less than 1, print "error: --times must be at least 1" to
    stderr, print nothing to stdout and return 1.
    On success return 0. Bad usage (no name, --times x) makes argparse exit
    with code 2 by itself.
    """
    # TODO: args = build_parser().parse_args(argv), then print and return.
    ...


if __name__ == "__main__":
    raise SystemExit(main())
