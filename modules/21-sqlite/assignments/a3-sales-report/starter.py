"""Assignment 3: An aggregate sales report.

The tests create this table and fill it:

    orders(id INTEGER PRIMARY KEY, customer TEXT NOT NULL, product TEXT NOT NULL,
           qty INTEGER NOT NULL, unit_price_cents INTEGER NOT NULL,
           ordered_on TEXT NOT NULL)        -- ISO date text such as 2025-03-14

Money is stored in cents (integers), so there are no rounding surprises.
Do the maths in SQL (SUM, COUNT, GROUP BY), not in Python loops.
"""

import sqlite3


def revenue_by_customer(conn: sqlite3.Connection) -> list[tuple[str, int]]:
    """Return (customer, total_cents) where total is the sum of
    qty * unit_price_cents. Highest total first, ties by customer name."""
    # TODO: SELECT customer, SUM(qty * unit_price_cents) ... GROUP BY customer.
    ...


def monthly_totals(conn: sqlite3.Connection) -> dict[str, int]:
    """Return {"YYYY-MM": total_cents} for every month that has orders.
    The dict keys are in calendar order. Hint: substr(ordered_on, 1, 7)."""
    # TODO: GROUP BY substr(ordered_on, 1, 7) ORDER BY that same value.
    ...


def best_product(conn: sqlite3.Connection) -> str | None:
    """Return the product with the most units sold in total (sum of qty).
    On a tie return the alphabetically first. Return None if there are no orders."""
    # TODO: GROUP BY product ORDER BY SUM(qty) DESC, product LIMIT 1.
    ...


def orders_above(conn: sqlite3.Connection, min_cents: int) -> list[int]:
    """Return the ids of orders whose own total (qty * unit_price_cents) is at
    least `min_cents`, in id order. Pass min_cents as a parameter."""
    # TODO: use a WHERE clause with a ? placeholder.
    ...


def format_report(conn: sqlite3.Connection) -> str:
    """Return a text report, one line per customer from revenue_by_customer:

        "Ann: 12.50"        (dollars with two decimals: cents / 100)

    Lines are joined with "\\n" and there is no trailing newline.
    No orders gives "No orders".
    """
    # TODO: reuse revenue_by_customer and format with f"{cents / 100:.2f}".
    ...


if __name__ == "__main__":
    db = sqlite3.connect(":memory:")
    db.execute(
        "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer TEXT NOT NULL, product TEXT NOT NULL,"
        " qty INTEGER NOT NULL, unit_price_cents INTEGER NOT NULL, ordered_on TEXT NOT NULL)"
    )
    db.execute("INSERT INTO orders VALUES (1, 'Ann', 'pen', 5, 250, '2025-03-01')")
    print(format_report(db))
