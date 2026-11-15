"""Stage 1 of the expense tracker: read expenses.csv into dataclasses.

The file has a header line (date,category,description,amount) and some bad
rows. A bad row must not stop the program: collect an error message and go on.
"""

import csv  # noqa: F401
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation  # noqa: F401
from pathlib import Path

DATA = Path(__file__).parent / "expenses.csv"


@dataclass(frozen=True)
class Expense:
    date: date
    category: str
    description: str
    amount: Decimal


def parse_row(row: dict) -> Expense:
    """Turn one CSV row (a dict with the four column names) into an Expense.

    Rules:
    - date: ISO text such as "2024-03-01" (date.fromisoformat).
    - category: stripped and lower-cased ("Food " -> "food"). Must not be empty.
    - description: stripped. May be empty.
    - amount: a Decimal that is finite, greater than 0 and has at most two
      decimal places ("15" and "12.5" are fine, "3.999" and "-5" are not).
    - If a value is None (the row was too short), treat it as an empty string.

    Raise ValueError with a short message for every broken rule.
    Note that Decimal("abc") raises decimal.InvalidOperation, which is NOT a
    ValueError, so catch it and raise ValueError yourself.
    """
    # TODO
    ...


def parse_expenses(path: Path = DATA) -> tuple[list[Expense], list[str]]:
    """Read the CSV file and return (expenses, errors).

    - Good rows become Expense objects, in file order.
    - For every bad row add the string f"line {n}: {message}" to errors, where
      n is the line number in the file (the header is line 1, so the first
      data row is line 2). Use reader.line_num of a csv.DictReader.
    - Open the file with encoding="utf-8" and newline="".
    """
    # TODO: csv.DictReader, call parse_row in a try/except ValueError.
    ...


if __name__ == "__main__":
    good, bad = parse_expenses()
    print(len(good), "good rows")
    for message in bad:
        print(message)
