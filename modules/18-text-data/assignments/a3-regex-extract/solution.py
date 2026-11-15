"""Assignment 3: Pull data out of text with regular expressions."""

import re

EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
DATE = re.compile(r"(?<!\d)(\d{4})-(\d{2})-(\d{2})(?!\d)")
LOG_LINE = re.compile(
    r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) "
    r"\[(?P<level>[A-Z]+)\] (?P<message>.*)"
)


def extract_emails(text: str) -> list[str]:
    """Return the unique e-mail addresses in `text`, lower-cased, in order of
    first appearance.

    An address is: word characters, dots, plus or minus signs, then "@", then
    a domain with at least one dot, such as  ann.lee+news@example.co.uk
    A trailing full stop at the end of a sentence is not part of the address.
    """
    found = (address.lower() for address in EMAIL.findall(text))
    return list(dict.fromkeys(found))


def find_dates(text: str) -> list[tuple[int, int, int]]:
    """Return every ISO date YYYY-MM-DD in `text` as a (year, month, day) tuple
    of ints, in order. Only match exactly four, two and two digits.
    Do not check that the date exists (2025-13-45 is returned as it is).
    A longer digit run such as 12025-01-01 must not match.
    """
    return [(int(y), int(m), int(d)) for y, m, d in DATE.findall(text)]


def parse_log_line(line: str) -> dict | None:
    """Parse a log line of the form

        2025-03-01 12:30:05 [ERROR] disk full

    into {"date": "2025-03-01", "time": "12:30:05", "level": "ERROR",
    "message": "disk full"}. The level is one or more capital letters. The
    message is everything after "] " (it may contain brackets and spaces).
    Return None if the line does not have this form.
    """
    match = LOG_LINE.fullmatch(line)
    return match.groupdict() if match else None


if __name__ == "__main__":
    print(extract_emails("Mail Ann@Example.com or bob@test.org."))
    print(find_dates("From 2025-01-31 to 2025-02-03"))
    print(parse_log_line("2025-03-01 12:30:05 [WARN] low memory"))
