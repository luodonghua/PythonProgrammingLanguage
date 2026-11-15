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
    rows = conn.execute(
        """
        SELECT customer, SUM(qty * unit_price_cents) AS total
        FROM orders
        GROUP BY customer
        ORDER BY total DESC, customer
        """
    )
    return [(row[0], row[1]) for row in rows]


def monthly_totals(conn: sqlite3.Connection) -> dict[str, int]:
    """Return {"YYYY-MM": total_cents} for every month that has orders.
    The dict keys are in calendar order. Hint: substr(ordered_on, 1, 7)."""
    rows = conn.execute(
        """
        SELECT substr(ordered_on, 1, 7) AS month, SUM(qty * unit_price_cents)
        FROM orders
        GROUP BY month
        ORDER BY month
        """
    )
    return {row[0]: row[1] for row in rows}


def best_product(conn: sqlite3.Connection) -> str | None:
    """Return the product with the most units sold in total (sum of qty).
    On a tie return the alphabetically first. Return None if there are no orders."""
    row = conn.execute(
        """
        SELECT product
        FROM orders
        GROUP BY product
        ORDER BY SUM(qty) DESC, product
        LIMIT 1
        """
    ).fetchone()
    return row[0] if row else None


def orders_above(conn: sqlite3.Connection, min_cents: int) -> list[int]:
    """Return the ids of orders whose own total (qty * unit_price_cents) is at
    least `min_cents`, in id order. Pass min_cents as a parameter."""
    rows = conn.execute(
        "SELECT id FROM orders WHERE qty * unit_price_cents >= ? ORDER BY id",
        (min_cents,),
    )
    return [row[0] for row in rows]


def format_report(conn: sqlite3.Connection) -> str:
    """Return a text report, one line per customer from revenue_by_customer:

        "Ann: 12.50"        (dollars with two decimals: cents / 100)

    Lines are joined with "\\n" and there is no trailing newline.
    No orders gives "No orders".
    """
    rows = revenue_by_customer(conn)
    if not rows:
        return "No orders"
    return "\n".join(f"{customer}: {cents / 100:.2f}" for customer, cents in rows)


if __name__ == "__main__":
    db = sqlite3.connect(":memory:")
    db.execute(
        "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer TEXT NOT NULL, product TEXT NOT NULL,"
        " qty INTEGER NOT NULL, unit_price_cents INTEGER NOT NULL, ordered_on TEXT NOT NULL)"
    )
    db.execute("INSERT INTO orders VALUES (1, 'Ann', 'pen', 5, 250, '2025-03-01')")
    print(format_report(db))
