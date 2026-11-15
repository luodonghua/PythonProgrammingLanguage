"""Assignment 4: Records as tuples.

Turn messy text lines into (name, quantity, price) tuples, then summarise them.
Practise lists, tuples, unpacking, slicing and comprehensions together.
"""

Record = tuple[str, int, float]


def chunk(items: list, size: int) -> list[list]:
    """Split a list into consecutive pieces of `size`. The last piece may be shorter.

    chunk([1, 2, 3, 4, 5], 2) -> [[1, 2], [3, 4], [5]]
    chunk([1, 2, 3], 3)       -> [[1, 2, 3]]
    chunk([], 4)              -> []

    Raise ValueError if size is less than 1.
    """
    if size < 1:
        raise ValueError("size must be at least 1")
    return [items[start : start + size] for start in range(0, len(items), size)]


def parse_records(lines: list[str]) -> list[Record]:
    """Parse lines like "apple, 3, 0.5" into tuples ("apple", 3, 0.5).

    * Each line has three comma-separated fields: name, whole-number
      quantity, price. Spaces around the fields are ignored.
    * Skip a line (do not raise) if it is blank, has the wrong number of
      fields, has an empty name, has a quantity that is not a whole number or
      a price that is not a number, or has a negative quantity or price.
    * Keep the order of the valid lines.

    parse_records(["apple, 3, 0.5", "bad line", " pear,2,1.25 "])
        -> [("apple", 3, 0.5), ("pear", 2, 1.25)]
    """
    records: list[Record] = []
    for line in lines:
        fields = [field.strip() for field in line.split(",")]
        if len(fields) != 3 or not fields[0]:
            continue
        name, qty_text, price_text = fields
        try:
            quantity = int(qty_text)
            price = float(price_text)
        except ValueError:
            continue
        if quantity < 0 or price < 0:
            continue
        records.append((name, quantity, price))
    return records


def summarize(records: list[Record]) -> tuple[int, int, float]:
    """Return (number of records, total quantity, total value).

    The total value is the sum of quantity * price, rounded to 2 decimals.

    summarize([("apple", 3, 0.5), ("pear", 2, 1.25)]) -> (2, 5, 4.0)
    summarize([])                                     -> (0, 0, 0.0)
    """
    total_quantity = sum(quantity for _, quantity, _ in records)
    total_value = sum(quantity * price for _, quantity, price in records)
    return len(records), total_quantity, round(total_value, 2)


def most_valuable(records: list[Record]) -> str | None:
    """Return the name of the record with the highest quantity * price.

    If two records tie, the first one wins. Return None for an empty list.

    most_valuable([("apple", 3, 0.5), ("pear", 2, 1.25)]) -> "pear"
    most_valuable([])                                     -> None
    """
    if not records:
        return None
    name, _, _ = max(records, key=lambda record: record[1] * record[2])
    return name


if __name__ == "__main__":
    lines = ["apple, 3, 0.5", "bad line", " pear,2,1.25 ", "fig, -1, 2"]
    data = parse_records(lines)
    print(data)
    print(summarize(data), most_valuable(data))
