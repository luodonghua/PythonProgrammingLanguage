"""Assignment 2: Group and aggregate orders.

Data: orders.csv in this folder (order_id, customer, category, quantity, unit_price).
Practise new columns, groupby, agg and sorting.
"""

from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "orders.csv"


def add_total(df: pd.DataFrame) -> pd.DataFrame:
    """Return a COPY of `df` with a new column "total" = quantity * unit_price.

    The input DataFrame must not gain a column.
    """
    # TODO: df.copy(), then add the column (or use df.assign(total=...)).
    ...


def revenue_by_category(df: pd.DataFrame) -> dict[str, float]:
    """Total revenue per category as a plain dict, largest revenue first.

    Values are rounded to 2 decimals. The input has no "total" column yet,
    so compute it first (you may call add_total).
    Example shape: {"Games": 123.45, "Books": 67.0}
    """
    # TODO: groupby("category")["total"].sum(), sort_values(ascending=False),
    # round(2), then .to_dict().
    ...


def customer_summary(df: pd.DataFrame) -> pd.DataFrame:
    """One row per customer with columns, in this order:

        customer, orders (number of orders), total_spent (rounded to 2 decimals)

    Sorted by total_spent, largest first; ties are broken by customer name A-Z.
    The index is 0, 1, 2, ...
    """
    # TODO: groupby("customer").agg(orders=(...), total_spent=(...)),
    # then reset_index, round, sort_values(["total_spent", "customer"], ascending=[False, True]).
    ...


if __name__ == "__main__":
    orders = pd.read_csv(DATA)
    print(revenue_by_category(orders))
    print(customer_summary(orders))
