"""Assignment 4: Clean a messy CSV and report every bad row.

The file people.csv (same folder) has the columns: name, age, email.
Several rows are bad. Good rows must be kept, bad rows must be reported,
and one bad row must never stop the whole run.
"""

import csv
import re
from pathlib import Path

EMAIL = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


def clean_rows(path: str | Path) -> tuple[list[dict], list[tuple[int, str]]]:
    """Read the CSV file and return (good_rows, errors).

    good_rows: a list of {"name": str, "age": int, "email": str}. The name is
        stripped, the email is lower-cased.
    errors: a list of (line_number, reason). The header is line 1, so the
        first data row is line 2. Check the problems in this order and report
        only the first one found for a row:

        1. fewer or more than 3 fields      -> "wrong field count"
        2. name empty after stripping       -> "missing name"
        3. age is not an int, or not 0..130 -> "bad age"
        4. email does not match name@host.tld (no spaces, one "@", a dot in
           the host part)                   -> "bad email"

    Hint: csv.DictReader puts missing values as None and extra values under the
    key None, so csv.reader (which gives lists) may be easier here. Use
    enumerate(reader, start=1) so the header is line 1. This is valid because
    no field in the file contains a line break.
    """
    good: list[dict] = []
    errors: list[tuple[int, str]] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for line_no, row in enumerate(reader, start=1):
            if line_no == 1:
                continue
            if len(row) != 3:
                errors.append((line_no, "wrong field count"))
                continue
            name, age_text, email = (field.strip() for field in row)
            if not name:
                errors.append((line_no, "missing name"))
                continue
            try:
                age = int(age_text)
            except ValueError:
                age = -1
            if not 0 <= age <= 130:
                errors.append((line_no, "bad age"))
                continue
            if not EMAIL.fullmatch(email):
                errors.append((line_no, "bad email"))
                continue
            good.append({"name": name, "age": age, "email": email.lower()})
    return good, errors


def summarize(path: str | Path) -> str:
    """Return a one-line summary such as "2 good rows, 5 errors".

    Use "1 good row" or "1 error" in the singular (0 and 2 or more are plural).
    """
    good, errors = clean_rows(path)
    rows = "1 good row" if len(good) == 1 else f"{len(good)} good rows"
    errs = "1 error" if len(errors) == 1 else f"{len(errors)} errors"
    return f"{rows}, {errs}"


if __name__ == "__main__":
    people = Path(__file__).parent / "people.csv"
    good, errors = clean_rows(people)
    print(good)
    print(errors)
    print(summarize(people))
