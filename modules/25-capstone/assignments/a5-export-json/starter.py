"""Stage 5 (stretch) of the expense tracker: export to JSON and import it back.

JSON has no Decimal and no date type, so both are written as strings.
Writing money as a string ("45.50") avoids float rounding errors.
"""

import json  # noqa: F401
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation  # noqa: F401
from pathlib import Path


@dataclass(frozen=True)
class Expense:
    date: date
    category: str
    description: str
    amount: Decimal


def export_json(expenses: list[Expense], path: Path) -> None:
    """Write the expenses to `path` as JSON.

    The document is an object with exactly these keys:
        "count":    the number of expenses (int)
        "total":    the sum of all amounts as a string with two decimals
        "expenses": a list of objects, sorted by date (equal dates keep their
                    input order), each with the keys "date" (ISO text),
                    "category", "description" and "amount" (string with two
                    decimals, e.g. "45.50").

    Write with indent=2, ensure_ascii=False and encoding="utf-8", and end the
    file with a newline.
    """
    # TODO: build a dict, then json.dumps(..., indent=2, ensure_ascii=False).
    ...


def import_json(path: Path) -> list[Expense]:
    """Read a file written by export_json and return the expenses in file order.

    Raise ValueError (with a clear message) when:
    - the text is not valid JSON (json.JSONDecodeError is already a ValueError),
    - the top level is not an object with an "expenses" list,
    - an item is not an object or lacks one of the four keys,
    - a date or an amount cannot be parsed (remember: Decimal("x") raises
      InvalidOperation, not ValueError),
    - "count" is present and differs from the number of items.
    """
    # TODO
    ...


def monthly_totals(expenses: list[Expense]) -> dict[str, str]:
    """Return {"YYYY-MM": "total with two decimals"}, sorted by month."""
    # TODO
    ...


if __name__ == "__main__":
    import tempfile

    sample = [
        Expense(date(2024, 3, 5), "food", "Café", Decimal("12.25")),
        Expense(date(2024, 3, 1), "food", "Groceries", Decimal("45.5")),
    ]
    target = Path(tempfile.gettempdir()) / "expenses_demo.json"
    export_json(sample, target)
    print(target.read_text(encoding="utf-8"))
    print(import_json(target) == sorted(sample, key=lambda e: e.date))
