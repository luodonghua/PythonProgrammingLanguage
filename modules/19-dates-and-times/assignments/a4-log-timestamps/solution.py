"""Assignment 4: Parse timestamps from a web server log.

The file access.log (same folder) has lines like

    10.0.0.1 - - [14/Mar/2025:09:05:10 +0000] "GET /index.html" 200

The timestamp sits in square brackets, in the format
"%d/%b/%Y:%H:%M:%S %z" (day, English month abbreviation, year, time, offset).
Some lines are not log entries, and some have a broken timestamp.
"""

import re
from collections import Counter
from datetime import UTC, datetime, timedelta
from pathlib import Path

TIMESTAMP_FORMAT = "%d/%b/%Y:%H:%M:%S %z"
BRACKETS = re.compile(r"\[([^\]]*)\]")


def parse_timestamp(text: str) -> datetime:
    """Parse text such as "14/Mar/2025:11:15:00 +0200" into an aware datetime
    converted to UTC (so the example gives 2025-03-14 09:15:00+00:00).
    Raise ValueError if the text does not match TIMESTAMP_FORMAT."""
    return datetime.strptime(text, TIMESTAMP_FORMAT).astimezone(UTC)


def read_timestamps(path: str | Path) -> list[datetime]:
    """Return the UTC timestamps of all valid log lines, sorted oldest first.

    A timestamp is the text between the first "[" and the next "]" on the
    line. Skip lines without brackets and lines whose timestamp does not parse.
    """
    stamps = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            found = BRACKETS.search(line)
            if found is None:
                continue
            try:
                stamps.append(parse_timestamp(found.group(1)))
            except ValueError:
                continue
    return sorted(stamps)


def busiest_hour(stamps: list[datetime]) -> tuple[datetime, int]:
    """Return (hour_start, count) for the clock hour (in UTC) that contains the
    most timestamps. hour_start is the first instant of that hour, for example
    2025-03-14 09:00:00+00:00. On a tie return the earliest hour.
    Raise ValueError for an empty list.
    """
    if not stamps:
        raise ValueError("no timestamps")
    counts = Counter(
        s.astimezone(UTC).replace(minute=0, second=0, microsecond=0) for s in stamps
    )
    best = max(counts.values())
    hour = min(h for h, n in counts.items() if n == best)
    return hour, best


def time_span(stamps: list[datetime]) -> timedelta:
    """Return the time between the earliest and the latest timestamp.
    An empty list gives timedelta(0)."""
    if not stamps:
        return timedelta(0)
    return max(stamps) - min(stamps)


if __name__ == "__main__":
    stamps = read_timestamps(Path(__file__).parent / "access.log")
    print(len(stamps), "valid lines")
    print(busiest_hour(stamps))
    print(time_span(stamps))
