"""Assignment 2: A command-line greeter with argparse.

Usage examples (after you finish the code):

    python solution.py Ada
    python solution.py Ada Lovelace --shout --times 2
    python solution.py Ada --greeting Hi
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
    parser = argparse.ArgumentParser(description="Greet someone.")
    parser.add_argument("name", nargs="+", help="who to greet")
    parser.add_argument("--times", type=int, default=1, help="how many times")
    parser.add_argument("--shout", action="store_true", help="use capital letters")
    parser.add_argument("--greeting", default="Hello", help="the greeting word")
    return parser


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
    args = build_parser().parse_args(argv)
    if args.times < 1:
        print("error: --times must be at least 1", file=sys.stderr)
        return 1
    text = f"{args.greeting}, {' '.join(args.name)}!"
    if args.shout:
        text = text.upper()
    for _ in range(args.times):
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
