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


def _to_amount(cents: int) -> Decimal:
    return Decimal(cents).scaleb(-2)


class ExpenseRepository:
    """Table `expenses`: id INTEGER PRIMARY KEY, day TEXT (ISO date),
    category TEXT, description TEXT, cents INTEGER."""

    def __init__(self, db_path: str = ":memory:"):
        """Open the database and create the table if it does not exist.

        Use sqlite3.connect(db_path). Keep the connection in self.conn.
        """
        self.conn = sqlite3.connect(db_path)
        with self.conn:
            self.conn.execute(
                "CREATE TABLE IF NOT EXISTS expenses ("
                " id INTEGER PRIMARY KEY,"
                " day TEXT NOT NULL,"
                " category TEXT NOT NULL,"
                " description TEXT NOT NULL,"
                " cents INTEGER NOT NULL)"
            )

    def add(self, expense: Expense) -> int:
        """Insert one expense and return its new id (cursor.lastrowid).

        Use "?" parameters. Convert the Decimal to cents with
        int(expense.amount * 100).
        """
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO expenses (day, category, description, cents) VALUES (?, ?, ?, ?)",
                (
                    expense.date.isoformat(),
                    expense.category,
                    expense.description,
                    int(expense.amount * 100),
                ),
            )
        return cursor.lastrowid

    def list_expenses(self, month: str | None = None) -> list[Expense]:
        """Return expenses ordered by date, then by id (insertion order).

        month is "YYYY-MM" or None. With a month, return only the expenses of
        that month (compare substr(day, 1, 7) = ? using a parameter).
        Convert back: date.fromisoformat(day) and Decimal(cents).scaleb(-2)
        (this keeps two decimals: Decimal("45.50")).
        """
        sql = "SELECT day, category, description, cents FROM expenses"
        params: tuple = ()
        if month is not None:
            sql += " WHERE substr(day, 1, 7) = ?"
            params = (month,)
        sql += " ORDER BY day, id"
        rows = self.conn.execute(sql, params).fetchall()
        return [
            Expense(date.fromisoformat(day), category, description, _to_amount(cents))
            for day, category, description, cents in rows
        ]

    def totals_by_category(self, month: str | None = None) -> dict[str, Decimal]:
        """Return {category: total amount}, biggest total first.

        Ties are ordered by category name A-Z. Optional month filter as above.
        Use SQL: SELECT category, SUM(cents) ... GROUP BY category.
        The totals are Decimal values with two decimal places,
        e.g. Decimal("57.75").
        """
        sql = "SELECT category, SUM(cents) AS total FROM expenses"
        params: tuple = ()
        if month is not None:
            sql += " WHERE substr(day, 1, 7) = ?"
            params = (month,)
        sql += " GROUP BY category ORDER BY total DESC, category"
        return {category: _to_amount(total) for category, total in self.conn.execute(sql, params)}

    def close(self) -> None:
        """Close the connection."""
        self.conn.close()


if __name__ == "__main__":
    repo = ExpenseRepository()
    repo.add(Expense(date(2024, 3, 1), "food", "Groceries", Decimal("45.50")))
    repo.add(Expense(date(2024, 3, 5), "food", "Lunch", Decimal("12.25")))
    print(repo.list_expenses())
    print(repo.totals_by_category())
    repo.close()
