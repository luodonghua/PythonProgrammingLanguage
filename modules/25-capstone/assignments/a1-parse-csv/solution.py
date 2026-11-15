"""Stage 1 of the expense tracker: read expenses.csv into dataclasses.

The file has a header line (date,category,description,amount) and some bad
rows. A bad row must not stop the program: collect an error message and go on.
"""

import csv
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
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
    text = {key: (row.get(key) or "").strip() for key in ("date", "category", "description", "amount")}

    try:
        when = date.fromisoformat(text["date"])
    except ValueError:
        raise ValueError(f"invalid date {text['date']!r}") from None

    category = text["category"].lower()
    if not category:
        raise ValueError("missing category")

    try:
        amount = Decimal(text["amount"])
    except InvalidOperation:
        raise ValueError(f"invalid amount {text['amount']!r}") from None
    if not amount.is_finite() or amount <= 0:
        raise ValueError(f"amount must be positive, got {text['amount']!r}")
    if amount.as_tuple().exponent < -2:
        raise ValueError(f"amount has more than two decimals: {text['amount']!r}")

    return Expense(when, category, text["description"], amount)


def parse_expenses(path: Path = DATA) -> tuple[list[Expense], list[str]]:
    """Read the CSV file and return (expenses, errors).

    - Good rows become Expense objects, in file order.
    - For every bad row add the string f"line {n}: {message}" to errors, where
      n is the line number in the file (the header is line 1, so the first
      data row is line 2). Use reader.line_num of a csv.DictReader.
    - Open the file with encoding="utf-8" and newline="".
    """
    expenses: list[Expense] = []
    errors: list[str] = []
    with open(path, encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            try:
                expenses.append(parse_row(row))
            except ValueError as exc:
                errors.append(f"line {reader.line_num}: {exc}")
    return expenses, errors


if __name__ == "__main__":
    good, bad = parse_expenses()
    print(len(good), "good rows")
    for message in bad:
        print(message)
