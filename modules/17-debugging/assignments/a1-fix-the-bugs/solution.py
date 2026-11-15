"""Assignment 1: Fix five bugs.

Each function below has one bug from a common family. The docstring says what
the function SHOULD do. Run the tests, read each failure, find the bug and fix
it. Change as little as possible.
"""


def add_to_cart(item: str, cart: list[str] | None = None) -> list[str]:
    """Return a cart (list) that contains `item` as its last element.

    When no cart is passed, start a NEW empty cart every time. When a cart is
    passed, append to it and return that same list.
    """
    if cart is None:
        cart = []
    cart.append(item)
    return cart


def sum_to(n: int) -> int:
    """Return 1 + 2 + ... + n (both ends included). sum_to(0) is 0."""
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


def percent(correct: int, total: int) -> float:
    """Return correct / total as a percentage rounded to 1 decimal place.

    percent(1, 3) -> 33.3     percent(3, 4) -> 75.0
    When total is 0, return 0.0.
    """
    if total == 0:
        return 0.0
    return round(correct / total * 100, 1)


def make_grid(rows: int, cols: int, fill: int = 0) -> list[list[int]]:
    """Return a list of `rows` lists, each with `cols` copies of `fill`.

    The rows must be independent: changing grid[0][0] must not change grid[1][0].
    """
    return [[fill] * cols for _ in range(rows)]


def longest_word(text: str) -> str:
    """Return the longest word in text (words are separated by whitespace).

    If several words tie, return the first one. Return "" for empty text.
    """
    best = ""
    for word in text.split():
        if len(word) > len(best):
            best = word
    return best


if __name__ == "__main__":
    print(add_to_cart("pen"), add_to_cart("ink"))
    print(sum_to(5), percent(1, 3), make_grid(2, 2), longest_word("a quick brown fox"))
