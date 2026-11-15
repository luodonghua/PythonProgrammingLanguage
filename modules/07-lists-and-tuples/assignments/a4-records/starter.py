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
    # TODO: a comprehension over range(0, len(items), size) with a slice.
    ...


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
    # TODO: loop; split(","), strip each field, try int()/float(), skip bad lines with continue.
    ...


def summarize(records: list[Record]) -> tuple[int, int, float]:
    """Return (number of records, total quantity, total value).

    The total value is the sum of quantity * price, rounded to 2 decimals.

    summarize([("apple", 3, 0.5), ("pear", 2, 1.25)]) -> (2, 5, 4.0)
    summarize([])                                     -> (0, 0, 0.0)
    """
    # TODO: sums with unpacking: for _, quantity, price in records.
    ...


def most_valuable(records: list[Record]) -> str | None:
    """Return the name of the record with the highest quantity * price.

    If two records tie, the first one wins. Return None for an empty list.

    most_valuable([("apple", 3, 0.5), ("pear", 2, 1.25)]) -> "pear"
    most_valuable([])                                     -> None
    """
    # TODO: max(records, key=...) then unpack the tuple.
    ...


if __name__ == "__main__":
    lines = ["apple, 3, 0.5", "bad line", " pear,2,1.25 ", "fig, -1, 2"]
    data = parse_records(lines)
    print(data)
    print(summarize(data), most_valuable(data))
