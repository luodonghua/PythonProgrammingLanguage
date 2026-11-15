"""Assignment 3: a lazy log pipeline.

The file ``app.log`` (same folder) has lines like
``2024-05-01 12:01:15 ERROR cannot open database``.

Build a pipeline of small generators. Nothing may read the whole file into
memory: each stage handles one line at a time.

``read_lines(path)``     generator over the lines of a UTF-8 text file, without
                         the trailing newline. Closes the file when finished.
``parse_lines(lines)``   generator of ``(level, message)`` tuples. A record is
                         ``date time LEVEL message...``. ``level`` is upper-cased
                         and the message keeps its inner spaces. Blank lines and
                         lines with fewer than four words are skipped.
``only_levels(records, levels)``
                         generator that keeps records whose level is in
                         ``levels`` (a collection of upper-case names).
``count_levels(records)``
                         consumes the records and returns a dict
                         ``{level: count}`` (levels in order of first appearance).
``error_report(path)``   uses the stages above and returns the list of
                         messages whose level is ERROR or CRITICAL.
"""


def read_lines(path):
    """Yield the lines of a file, one at a time, without newlines."""
    with open(path, encoding="utf-8") as file:
        for line in file:
            yield line.rstrip("\n")


def parse_lines(lines):
    """Yield (level, message) for every valid log line."""
    for line in lines:
        parts = line.split(maxsplit=3)
        if len(parts) < 4:
            continue
        yield parts[2].upper(), parts[3]


def only_levels(records, levels):
    """Yield only the records whose level is in ``levels``."""
    for level, message in records:
        if level in levels:
            yield level, message


def count_levels(records):
    """Return a dict with the number of records per level."""
    counts = {}
    for level, _ in records:
        counts[level] = counts.get(level, 0) + 1
    return counts


def error_report(path):
    """Return the messages of ERROR and CRITICAL records in the file."""
    records = only_levels(parse_lines(read_lines(path)), {"ERROR", "CRITICAL"})
    return [message for _, message in records]


if __name__ == "__main__":
    from pathlib import Path

    log = Path(__file__).parent / "app.log"
    print(count_levels(parse_lines(read_lines(log))))
    print(error_report(log))
