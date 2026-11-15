"""Assignment 4: A formatted receipt.

Practise f-string format specs: width, alignment, precision, thousands separators.
"""

WIDTH = 30


def format_line(name: str, qty: int, price: float) -> str:
    """Return one receipt line exactly WIDTH (30) characters wide.

    Layout, from left to right:
    * the name, left-aligned in 14 characters (longer names are cut to 14)
    * the quantity, right-aligned in 3 characters
    * the line total (qty * price), right-aligned in 13 characters, with
      2 decimals and a thousands separator

    format_line("Tea", 2, 3.5)         -> "Tea             2         7.00"
    format_line("Laptop", 1, 1299.99)  -> "Laptop          1     1,299.99"
    """
    return f"{name[:14]:<14}{qty:>3}{qty * price:>13,.2f}"


def format_receipt(items: list[tuple[str, int, float]], title: str = "RECEIPT") -> str:
    """Build a complete receipt as one string. Lines are joined with a newline.

    Each item is a tuple (name, qty, price). The lines, in order, are:
    1. the title centred in WIDTH characters
    2. WIDTH hyphens
    3. one format_line() for each item
    4. WIDTH hyphens
    5. "TOTAL" left-aligned in 14 characters, then the sum of all line totals
       right-aligned in 16 characters, with 2 decimals and a thousands separator

    The result has no newline at the end and no line is stripped, so every
    line is exactly WIDTH characters wide.

    format_receipt([("Tea", 2, 3.5)]) has these five lines:
        "           RECEIPT            "
        "------------------------------"
        "Tea             2         7.00"
        "------------------------------"
        "TOTAL                     7.00"
    """
    total = sum(qty * price for _, qty, price in items)
    lines = [f"{title:^{WIDTH}}", "-" * WIDTH]
    lines += [format_line(name, qty, price) for name, qty, price in items]
    lines += ["-" * WIDTH, f"{'TOTAL':<14}{total:>16,.2f}"]
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_receipt([("Tea", 2, 3.5), ("Laptop", 1, 1299.99)]))
