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
    rows = []
    for i in range(1, size + 1):
        row = ""
        for j in range(1, size + 1):
            row += f"{i * j:4d}"
        rows.append(row)
    return rows


def triangle(height: int) -> list[str]:
    """Return a left-aligned triangle of "*" characters.

    triangle(3) -> ["*", "**", "***"]
    triangle(0) -> []
    """
    return ["*" * row for row in range(1, height + 1)]


def pyramid(height: int) -> list[str]:
    """Return a centred pyramid of "*" characters.

    Row r (starting at 1) has 2*r - 1 stars, padded on the left with
    spaces so that all rows are centred. Rows have NO trailing spaces.

    pyramid(3) -> ["  *", " ***", "*****"]
    pyramid(1) -> ["*"]
    pyramid(0) -> []
    """
    rows = []
    for row in range(1, height + 1):
        spaces = " " * (height - row)
        rows.append(spaces + "*" * (2 * row - 1))
    return rows


def checkerboard(size: int) -> list[str]:
    """Return a size x size board. The top-left square is "#", then they alternate.

    checkerboard(3) -> ["#.#", ".#.", "#.#"]
    checkerboard(0) -> []
    """
    rows = []
    for row in range(size):
        line = ""
        for col in range(size):
            line += "#" if (row + col) % 2 == 0 else "."
        rows.append(line)
    return rows


if __name__ == "__main__":
    for line in pyramid(4):
        print(line)
    print()
    for line in multiplication_table(4):
        print(line)
