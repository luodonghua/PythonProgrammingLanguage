"""Assignment 1: Sum a CSV column.

The file sales.csv (same folder) has the columns: product, qty, price.
Some product names contain commas inside quotes, so use the csv module.
"""

import csv
from pathlib import Path


def sum_column(path: str | Path, column: str) -> float:
    """Return the sum of all numbers in `column` of the CSV file at `path`.

    - Read with csv.DictReader, opening the file with newline="" and
      encoding="utf-8".
    - Convert each value with float().
    - If `column` is not a header of the file, raise KeyError(column).
    - An empty file or a file with no data rows gives 0.0.
    """
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is not None and column not in reader.fieldnames:
            raise KeyError(column)
        return sum(float(row[column]) for row in reader)


def revenue(path: str | Path) -> float:
    """Return the sum of qty * price over all rows (qty is an int, price a float)."""
    with open(path, newline="", encoding="utf-8") as f:
        return sum(int(row["qty"]) * float(row["price"]) for row in csv.DictReader(f))


if __name__ == "__main__":
    sales = Path(__file__).parent / "sales.csv"
    print(sum_column(sales, "qty"))
    print(revenue(sales))
