"""Assignment 1: Sum a CSV column.

The file sales.csv (same folder) has the columns: product, qty, price.
Some product names contain commas inside quotes, so use the csv module.
"""

from pathlib import Path


def sum_column(path: str | Path, column: str) -> float:
    """Return the sum of all numbers in `column` of the CSV file at `path`.

    - Read with csv.DictReader, opening the file with newline="" and
      encoding="utf-8".
    - Convert each value with float().
    - If `column` is not a header of the file, raise KeyError(column).
    - An empty file or a file with no data rows gives 0.0.
    """
    # TODO: read the file and add up the column.
    ...


def revenue(path: str | Path) -> float:
    """Return the sum of qty * price over all rows (qty is an int, price a float)."""
    # TODO: use csv.DictReader and multiply the two columns per row.
    ...


if __name__ == "__main__":
    sales = Path(__file__).parent / "sales.csv"
    print(sum_column(sales, "qty"))
    print(revenue(sales))
