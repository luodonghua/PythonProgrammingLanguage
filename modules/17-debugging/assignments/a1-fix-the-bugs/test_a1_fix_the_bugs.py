from practice import load

m = load(__file__)


def test_add_to_cart():
    # a new cart each time
    assert m.add_to_cart("pen") == ["pen"]
    assert m.add_to_cart("ink") == ["ink"]
    # a given cart is extended and returned
    cart = ["book"]
    result = m.add_to_cart("pen", cart)
    assert result is cart
    assert cart == ["book", "pen"]


def test_sum_to():
    for n, expected in [(0, 0), (1, 1), (5, 15), (100, 5050)]:
        assert m.sum_to(n) == expected, f"sum_to({n})"


def test_percent():
    cases = [(1, 3, 33.3), (3, 4, 75.0), (0, 5, 0.0), (5, 5, 100.0), (2, 3, 66.7), (1, 0, 0.0)]
    for correct, total, expected in cases:
        assert m.percent(correct, total) == expected, f"percent({correct}, {total})"


def test_make_grid():
    assert m.make_grid(2, 3) == [[0, 0, 0], [0, 0, 0]]
    assert m.make_grid(1, 2, fill=7) == [[7, 7]]
    assert m.make_grid(0, 3) == []
    grid = m.make_grid(3, 2)
    grid[0][0] = 9
    assert grid == [[9, 0], [0, 0], [0, 0]], "rows must be independent lists"


def test_longest_word():
    cases = [
        ("a quick brown fox", "quick"),
        ("cat dog", "cat"),
        ("  spaced   out  words ", "spaced"),
        ("", ""),
        ("one", "one"),
    ]
    for text, expected in cases:
        assert m.longest_word(text) == expected, f"longest_word({text!r})"


def test_no_variable_called_max():
    import inspect

    source = inspect.getsource(m.longest_word)
    assert "max =" not in source, "do not shadow the built-in max"
    assert m.longest_word("ab c") == "ab"
