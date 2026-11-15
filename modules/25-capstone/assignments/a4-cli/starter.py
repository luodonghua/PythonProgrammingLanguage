"""Stage 4 of the expense tracker: the command-line interface.

Usage (what you will build):

    python solution.py [--db PATH] add DATE CATEGORY AMOUNT [-d TEXT]
    python solution.py [--db PATH] list [--month YYYY-MM]
    python solution.py [--db PATH] report YYYY-MM

Design rule: main(argv) takes the arguments as a list and RETURNS an exit
code, so tests can call it without starting a new process.
"""

import argparse
import re
import sqlite3
import sys
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation

# ---------------------------------------------------------------------------
# Provided code from stages 2 and 3. Read it, but you do not need to change it.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Expense:
    date: date
    category: str
    description: str
    amount: Decimal


class ExpenseRepository:
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        with self.conn:
            self.conn.execute(
                "CREATE TABLE IF NOT EXISTS expenses ("
                " id INTEGER PRIMARY KEY, day TEXT NOT NULL, category TEXT NOT NULL,"
                " description TEXT NOT NULL, cents INTEGER NOT NULL)"
            )

    def add(self, expense: Expense) -> int:
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO expenses (day, category, description, cents) VALUES (?, ?, ?, ?)",
                (expense.date.isoformat(), expense.category, expense.description,
                 int(expense.amount * 100)),
            )
        return cursor.lastrowid

    def list_expenses(self, month: str | None = None) -> list[Expense]:
        sql = "SELECT day, category, description, cents FROM expenses"
        params: tuple = ()
        if month is not None:
            sql += " WHERE substr(day, 1, 7) = ?"
            params = (month,)
        rows = self.conn.execute(sql + " ORDER BY day, id", params).fetchall()
        return [Expense(date.fromisoformat(d), c, t, Decimal(n).scaleb(-2)) for d, c, t, n in rows]

    def close(self) -> None:
        self.conn.close()


def format_report(expenses: list[Expense], month: str) -> str:
    totals: dict[str, Decimal] = {}
    counts: dict[str, int] = {}
    for e in expenses:
        if e.date.isoformat()[:7] == month:
            totals[e.category] = totals.get(e.category, Decimal(0)) + e.amount
            counts[e.category] = counts.get(e.category, 0) + 1
    if not totals:
        return f"No expenses for {month}"
    rule = "-" * 30
    lines = [f"Expenses for {month}", f"{'Category':<12}{'Count':>6}{'Total':>12}", rule]
    for name, total in sorted(totals.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"{name[:12]:<12}{counts[name]:>6}{total:>12,.2f}")
    lines += [rule, f"{'TOTAL':<12}{sum(counts.values()):>6}{sum(totals.values()):>12,.2f}"]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Your work starts here.
# ---------------------------------------------------------------------------


def parse_amount(text: str) -> Decimal:
    """Convert text to a Decimal amount, or raise ValueError.

    The amount must be finite, greater than 0, and have at most two decimal
    places. Decimal("abc") raises InvalidOperation (not a ValueError), so
    catch that and raise ValueError("invalid amount: ...") yourself.
    """
    # TODO
    ...


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser.

    - Global option --db PATH (default "expenses.db").
    - Required sub-commands (add_subparsers(dest="command", required=True)):
        add     positional date, category, amount (all strings);
                option -d / --description (default "")
        list    option --month (default None)
        report  positional month
    Let argparse handle usage errors (it exits with status 2).
    """
    # TODO
    ...


def main(argv: list[str] | None = None) -> int:
    """Run the command and return the exit code. Do not call sys.exit here.

    add:    validate with date.fromisoformat and parse_amount. The category is
            stripped and lower-cased, and must not be empty. On success print
            f"Added #{id}: {date} {category} {amount:.2f}" and return 0.
    list:   print one line per expense, in repository order:
            f"{e.date.isoformat()}  {e.category:<12}{e.amount:>9.2f}  {e.description}"
            with trailing spaces removed (rstrip). With no expenses print
            "No expenses." A --month value must look like YYYY-MM (month 01-12).
    report: month must look like YYYY-MM (month 01-12). Print
            format_report(all expenses, month).
    On invalid input (bad date, amount, category or month) print
    f"error: {message}" to sys.stderr and return 1. Return 0 on success.
    Always close the repository, even after an error (try/finally).
    """
    # TODO: args = build_parser().parse_args(argv); repo = ExpenseRepository(args.db)
    ...


if __name__ == "__main__":
    sys.exit(main())
