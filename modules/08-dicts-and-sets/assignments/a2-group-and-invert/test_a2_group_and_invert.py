from practice import load

m = load(__file__)


def test_group_by_first_letter():
    result = m.group_by(["apple", "avocado", "bean"], lambda s: s[0])
    assert result == {"a": ["apple", "avocado"], "b": ["bean"]}


def test_group_by_keeps_order():
    assert m.group_by([5, 3, 4, 1, 2], lambda n: n % 2) == {1: [5, 3, 1], 0: [4, 2]}


def test_group_by_empty():
    assert m.group_by([], len) == {}


def test_group_by_returns_plain_dict():
    result = m.group_by(["a"], len)
    assert type(result) is dict


def test_invert():
    assert m.invert({"a": 1, "b": 2, "c": 1}) == {1: ["a", "c"], 2: ["b"]}


def test_invert_sorts_keys():
    assert m.invert({"z": 0, "m": 0, "a": 0}) == {0: ["a", "m", "z"]}


def test_invert_empty():
    assert m.invert({}) == {}


def test_with_defaults():
    assert m.with_defaults({"color": "red"}, {"color": "blue", "size": 3}) == {
        "color": "red",
        "size": 3,
    }


def test_with_defaults_does_not_change_arguments():
    settings = {"a": 1}
    defaults = {"a": 0, "b": 2}
    result = m.with_defaults(settings, defaults)
    assert result == {"a": 1, "b": 2}
    assert settings == {"a": 1}
    assert defaults == {"a": 0, "b": 2}
    assert result is not settings and result is not defaults


def test_squares_of_evens():
    assert m.squares_of_evens([1, 2, 3, 4]) == {2: 4, 4: 16}
    assert m.squares_of_evens([]) == {}
    assert m.squares_of_evens(range(1, 10, 2)) == {}


def test_first_duplicate():
    assert m.first_duplicate([3, 1, 4, 1, 5, 3]) == 1
    assert m.first_duplicate(["a", "b", "a"]) == "a"


def test_first_duplicate_none():
    assert m.first_duplicate([1, 1]) == 1
    assert m.first_duplicate(["a", "b", "a"]) == "a"  # not None
    assert m.first_duplicate(["a", "b"]) is None
    assert m.first_duplicate([]) is None


def test_first_duplicate_works_with_generators():
    assert m.first_duplicate(n % 3 for n in range(10)) == 0
