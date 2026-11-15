"""Assignment 2: Text patterns with nested loops.

Every function RETURNS a list of strings (one per line) instead of printing,
so it is easy to test. The demo at the bottom prints them.
"""


def multiplication_table(size: int) -> list[str]:
    """Return a multiplication table with `size` rows and columns.

    Every number is right-aligned in a field 4 characters wide.
    Row i (starting at 1) holds i*1, i*2, ... i*size.

    multiplication_table(3) -> [
        "   1   2   3",
        "   2   4   6",
        "   3   6   9",
    ]
    multiplication_table(0) -> []
    """
    # TODO: two nested loops; f"{i * j:4d}" pads each number.
    ...


def triangle(height: int) -> list[str]:
    """Return a left-aligned triangle of "*" characters.

    triangle(3) -> ["*", "**", "***"]
    triangle(0) -> []
    """
    # TODO: one loop with "*" * row.
    ...


def pyramid(height: int) -> list[str]:
    """Return a centred pyramid of "*" characters.

    Row r (starting at 1) has 2*r - 1 stars, padded on the left with
    spaces so that all rows are centred. Rows have NO trailing spaces.

    pyramid(3) -> ["  *", " ***", "*****"]
    pyramid(1) -> ["*"]
    pyramid(0) -> []
    """
    # TODO: for each row build spaces + stars.
    ...


def checkerboard(size: int) -> list[str]:
    """Return a size x size board. The top-left square is "#", then they alternate.

    checkerboard(3) -> ["#.#", ".#.", "#.#"]
    checkerboard(0) -> []
    """
    # TODO: nested loops; the square is "#" when (row + col) is even.
    ...


if __name__ == "__main__":
    for line in pyramid(4):
        print(line)
    print()
    for line in multiplication_table(4):
        print(line)
