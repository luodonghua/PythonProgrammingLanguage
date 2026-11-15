"""Stage 5 (stretch) of the expense tracker: export to JSON and import it back.

JSON has no Decimal and no date type, so both are written as strings.
Writing money as a string ("45.50") avoids float rounding errors.
"""

import json
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

KEYS = ("date", "category", "description", "amount")


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
    ordered = sorted(expenses, key=lambda e: e.date)  # sorted() is stable
    document = {
        "count": len(ordered),
        "total": f"{sum((e.amount for e in ordered), Decimal(0)):.2f}",
        "expenses": [
            {
                "date": e.date.isoformat(),
                "category": e.category,
                "description": e.description,
                "amount": f"{e.amount:.2f}",
            }
            for e in ordered
        ],
    }
    text = json.dumps(document, indent=2, ensure_ascii=False) + "\n"
    Path(path).write_text(text, encoding="utf-8")


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
    document = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(document, dict) or not isinstance(document.get("expenses"), list):
        raise ValueError('expected an object with an "expenses" list')
    items = document["expenses"]
    if "count" in document and document["count"] != len(items):
        raise ValueError(f"count is {document['count']} but there are {len(items)} items")

    result = []
    for number, item in enumerate(items, 1):
        if not isinstance(item, dict) or any(key not in item for key in KEYS):
            raise ValueError(f"item {number}: expected an object with keys {', '.join(KEYS)}")
        try:
            when = date.fromisoformat(item["date"])
            amount = Decimal(item["amount"])
        except (ValueError, TypeError, InvalidOperation):
            raise ValueError(f"item {number}: invalid date or amount") from None
        result.append(Expense(when, item["category"], item["description"], amount))
    return result


def monthly_totals(expenses: list[Expense]) -> dict[str, str]:
    """Return {"YYYY-MM": "total with two decimals"}, sorted by month."""
    totals: dict[str, Decimal] = {}
    for e in expenses:
        month = e.date.isoformat()[:7]
        totals[month] = totals.get(month, Decimal(0)) + e.amount
    return {month: f"{totals[month]:.2f}" for month in sorted(totals)}


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
