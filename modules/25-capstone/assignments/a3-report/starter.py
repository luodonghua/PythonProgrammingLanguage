"""Stage 3 of the expense tracker: format a monthly report as a text table.

This stage is pure formatting: a list of Expense objects goes in, a string
comes out. That makes it easy to test, and the CLI (stage 4) just prints it.
"""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Expense:
    date: date
    category: str
    description: str
    amount: Decimal


def format_report(expenses: list[Expense], month: str) -> str:
    """Build the report for `month` ("YYYY-MM") from ALL given expenses.

    Only expenses whose date is in that month count (date.isoformat()[:7]).

    With no expenses in the month, return exactly: "No expenses for 2024-03"
    (with the month inserted).

    Otherwise return these lines joined by "\\n" (no trailing newline):

        Expenses for 2024-03
        Category     Count       Total
        ------------------------------
        food             2       57.75
        transport        1       30.00
        ------------------------------
        TOTAL            3       87.75

    Layout rules:
    - Title line: f"Expenses for {month}".
    - Header: "Category" left-aligned in 12 columns, "Count" right-aligned in 6,
      "Total" right-aligned in 12 (so every table line is 30 characters wide).
    - The separator is 30 hyphens.
    - One row per category: name left-aligned in 12 columns (cut longer names
      to 12 characters), count right-aligned in 6, total right-aligned in 12
      with two decimals and a thousands separator (format spec ">12,.2f").
    - Rows are sorted by total, biggest first. Ties are sorted by name A-Z.
    - The last row starts with "TOTAL" and uses the same widths; its count is
      the number of expenses, its total is the grand total.
    """
    # TODO: filter by month, group by category (dict or Counter), then build
    # the lines with f-strings such as f"{name:<12}{count:>6}{total:>12,.2f}".
    ...


def top_category(expenses: list[Expense], month: str) -> str | None:
    """Return the name of the category with the largest total in `month`.

    Ties go to the name that comes first alphabetically. Return None when the
    month has no expenses.
    """
    # TODO
    ...


if __name__ == "__main__":
    sample = [
        Expense(date(2024, 3, 1), "food", "Groceries", Decimal("45.50")),
        Expense(date(2024, 3, 5), "food", "Lunch", Decimal("12.25")),
        Expense(date(2024, 3, 3), "transport", "Bus pass", Decimal("30.00")),
    ]
    print(format_report(sample, "2024-03"))
