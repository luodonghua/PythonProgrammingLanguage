"""Stage 2 of the expense tracker: store expenses in SQLite.

A "repository" hides the SQL behind methods. The rest of the program works
with Expense objects and never sees a cursor.

Money rule: store the amount as an INTEGER number of cents, never as a float.
"""

import sqlite3
from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Expense:
    date: date
    category: str
    description: str
    amount: Decimal


class ExpenseRepository:
    """Table `expenses`: id INTEGER PRIMARY KEY, day TEXT (ISO date),
    category TEXT, description TEXT, cents INTEGER."""

    def __init__(self, db_path: str = ":memory:"):
        """Open the database and create the table if it does not exist.

        Use sqlite3.connect(db_path). Keep the connection in self.conn.
        """
        # TODO: connect and run CREATE TABLE IF NOT EXISTS.
        ...

    def add(self, expense: Expense) -> int:
        """Insert one expense and return its new id (cursor.lastrowid).

        Use "?" parameters. Convert the Decimal to cents with
        int(expense.amount * 100).
        """
        # TODO
        ...

    def list_expenses(self, month: str | None = None) -> list[Expense]:
        """Return expenses ordered by date, then by id (insertion order).

        month is "YYYY-MM" or None. With a month, return only the expenses of
        that month (compare substr(day, 1, 7) = ? using a parameter).
        Convert back: date.fromisoformat(day) and Decimal(cents).scaleb(-2)
        (this keeps two decimals: Decimal("45.50")).
        """
        # TODO
        ...

    def totals_by_category(self, month: str | None = None) -> dict[str, Decimal]:
        """Return {category: total amount}, biggest total first.

        Ties are ordered by category name A-Z. Optional month filter as above.
        Use SQL: SELECT category, SUM(cents) ... GROUP BY category.
        The totals are Decimal values with two decimal places,
        e.g. Decimal("57.75").
        """
        # TODO
        ...

    def close(self) -> None:
        """Close the connection."""
        # TODO
        ...


if __name__ == "__main__":
    repo = ExpenseRepository()
    repo.add(Expense(date(2024, 3, 1), "food", "Groceries", Decimal("45.50")))
    repo.add(Expense(date(2024, 3, 5), "food", "Lunch", Decimal("12.25")))
    print(repo.list_expenses())
    print(repo.totals_by_category())
    repo.close()
