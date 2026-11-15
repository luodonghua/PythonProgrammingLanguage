import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("value", "expected"),
    [("42", 42), (" 7 ", 7), ("-3", -3), ("4.5", -1), ("abc", -1), ("", -1), (None, -1), (9, 9)],
)
def test_safe_int(value, expected):
    assert m.safe_int(value, -1) == expected


@pytest.mark.parametrize("value", ["4.5", "abc", "", None])
def test_safe_int_default_is_none(value):
    assert m.safe_int(value) is None
    assert m.safe_int("1") == 1


def test_safe_int_default():
    assert m.safe_int("abc", 0) == 0
    assert m.safe_int(None, -1) == -1
    assert m.safe_int("12", -1) == 12


def test_safe_divide():
    assert m.safe_divide(6, 3) == 2.0
    assert m.safe_divide(1, 0) is None
    assert m.safe_divide(0, 5) == 0


def test_safe_divide_does_not_hide_other_errors():
    assert m.safe_divide(4, 2) == 2
    with pytest.raises(TypeError):
        m.safe_divide("a", 2)


def test_get_or_default():
    assert m.get_or_default([10, 20], 1) == 20
    assert m.get_or_default([10, 20], -1) == 20
    assert m.get_or_default([10, 20], 5, "x") == "x"
    assert m.get_or_default([], 0) is None
    assert m.get_or_default("abc", 1) == "b"


def test_get_or_default_hides_nothing_else():
    assert m.get_or_default([1], 0) == 1
    with pytest.raises(TypeError):
        m.get_or_default([1], "0")


def test_read_number():
    assert m.read_number({"n": "5"}, "n") == 5
    assert m.read_number({"n": 7}, "n") == 7
    assert m.read_number({"n": "five"}, "n") is None
    assert m.read_number({"n": None}, "n") is None
    assert m.read_number({}, "n") is None


def test_error_name():
    assert m.error_name(lambda: 1 / 0) == "ZeroDivisionError"
    assert m.error_name(lambda: [][0]) == "IndexError"
    assert m.error_name(lambda: {}["k"]) == "KeyError"
    assert m.error_name(lambda: int("x")) == "ValueError"


def test_error_name_no_error():
    assert m.error_name(lambda: 1 + 1) is None
    assert m.error_name(lambda: 1 / 0) is not None
