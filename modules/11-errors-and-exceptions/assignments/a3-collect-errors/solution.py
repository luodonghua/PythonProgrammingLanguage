"""Assignment 3: Keep going after errors and report them at the end.

Real programs rarely stop at the first bad row. They collect the problems
and carry on. Practises try/except/else, `continue` and error reports.
"""

from pathlib import Path


def parse_records(lines: list[str]) -> tuple[list[tuple[str, int]], list[tuple[int, str]]]:
    """Parse lines of the form "name,age" and collect the problems.

    Return (records, errors):
      records: list of (name, age) with name stripped and age as int
      errors:  list of (line_number, reason), line numbers start at 1

    Blank lines (only whitespace) are skipped silently but still count for
    line numbers. A bad line adds one error (the first problem found) and
    parsing continues. The reasons are exactly:
      "expected 2 fields"       the line does not split into exactly 2 parts on ","
      "empty name"              the name is empty after stripping
      "age is not a number"     int(age) fails
      "age out of range"        age below 0 or above 150

    parse_records(["Ada,36", "", "Bob,x", "Cy"])
        -> ([("Ada", 36)], [(3, "age is not a number"), (4, "expected 2 fields")])
    """
    records: list[tuple[str, int]] = []
    errors: list[tuple[int, str]] = []
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        parts = line.split(",")
        if len(parts) != 2:
            errors.append((number, "expected 2 fields"))
            continue
        name = parts[0].strip()
        if not name:
            errors.append((number, "empty name"))
            continue
        try:
            age = int(parts[1])
        except ValueError:
            errors.append((number, "age is not a number"))
            continue
        if not 0 <= age <= 150:
            errors.append((number, "age out of range"))
            continue
        records.append((name, age))
    return records, errors


def read_or_default(path: Path, default: str = "") -> str:
    """Return the text of the file at `path`, or `default` if the file is missing.
    A file that exists but cannot be decoded as UTF-8 also gives `default`.
    """
    try:
        return Path(path).read_text(encoding="utf-8")
    except (FileNotFoundError, UnicodeDecodeError):
        return default


def sum_numbers(items: list) -> tuple[float, list]:
    """Add the numbers in `items`. Strings that look like numbers count as well.

    Return (total, bad_items), where bad_items holds the items that could not
    be converted with float(), in their original order.

    sum_numbers([1, "2.5", "x", None, 4])  -> (7.5, ["x", None])
    """
    total = 0.0
    bad = []
    for item in items:
        try:
            total += float(item)
        except (ValueError, TypeError):
            bad.append(item)
    return total, bad


def run_all(tasks: list) -> list[tuple[str, object]]:
    """Call every zero-argument function in `tasks`, one after the other.

    For each task return ("ok", result) if it finishes, or
    ("error", "<ExceptionName>: <message>") if it raises an Exception.
    A failing task must not stop the others.

    run_all([lambda: 1, lambda: 1 / 0])
        -> [("ok", 1), ("error", "ZeroDivisionError: division by zero")]
    """
    results: list[tuple[str, object]] = []
    for task in tasks:
        try:
            value = task()
        except Exception as exc:
            results.append(("error", f"{type(exc).__name__}: {exc}"))
        else:
            results.append(("ok", value))
    return results


if __name__ == "__main__":
    print(parse_records(["Ada,36", "", "Bob,x", "Cy"]))
    print(sum_numbers([1, "2.5", "x"]))
