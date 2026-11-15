"""Assignment 1: Make the tests pass (parse a duration like "1h30m").

Read test_a1_parse_duration.py first. It is the specification. Then write
parse_duration so that every test passes.
"""

import re

UNITS = {"d": 86400, "h": 3600, "m": 60, "s": 1}
PART = re.compile(r"(\d+)([dhms])")


def parse_duration(text: str) -> int:
    """Convert a duration string to a whole number of seconds.

    A duration is one or more parts written as <number><unit>, where the unit is
    d (days), h (hours), m (minutes) or s (seconds). Parts must appear in that
    order (d, h, m, s), at most once each. Letters are lower case. Spaces around
    the whole text are ignored.

    "90s" -> 90, "5m" -> 300, "1h30m" -> 5400, "1d" -> 86400

    Raise ValueError for an empty string, a missing unit or number, an unknown
    unit, repeated or out-of-order parts, and any other stray characters.
    """
    text = text.strip()
    if not text:
        raise ValueError("empty duration")
    total = 0
    position = 0
    last_unit_index = -1
    order = "dhms"
    while position < len(text):
        match = PART.match(text, position)
        if match is None:
            raise ValueError(f"bad duration: {text!r}")
        number, unit = match.groups()
        index = order.index(unit)
        if index <= last_unit_index:
            raise ValueError(f"unit out of order or repeated: {text!r}")
        last_unit_index = index
        total += int(number) * UNITS[unit]
        position = match.end()
    return total


if __name__ == "__main__":
    for example in ("90s", "1h30m", "2d4h"):
        print(example, "->", parse_duration(example))
