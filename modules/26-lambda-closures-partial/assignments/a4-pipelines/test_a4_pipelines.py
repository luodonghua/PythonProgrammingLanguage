import operator

import pytest

from practice import load

m = load(__file__)


def test_pipeline_runs_left_to_right():
    clean = m.pipeline(str.strip, str.lower, str.title)
    assert clean("  hELLO wORLD ") == "Hello World"


def test_pipeline_order_matters():
    assert m.pipeline(lambda x: x + 1, lambda x: x * 10)(1) == 20
    assert m.pipeline(lambda x: x * 10, lambda x: x + 1)(1) == 11


def test_pipeline_without_functions_is_identity():
    value = object()
    assert m.pipeline()(value) is value


def test_pipeline_can_be_reused():
    double = m.pipeline(lambda x: x * 2)
    assert [double(1), double(2)] == [2, 4]


def test_operator_table_uses_operator_module():
    assert m.OPERATORS["+"] is operator.add
    assert set(m.OPERATORS) == {"+", "-", "*", "/", "//"}


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("3 + 4", 7.0),
        ("7.5 * 2", 15.0),
        ("10 - 12", -2.0),
        ("9 / 2", 4.5),
        ("9 // 2", 4.0),
        ("  1   +   1  ", 2.0),
    ],
)
def test_calculate(text, expected):
    assert m.calculate(text) == expected


@pytest.mark.parametrize("text", ["", "3 +", "1 + 2 + 3", "3 ^ 2", "x + 1", "1 + y"])
def test_calculate_value_errors(text):
    with pytest.raises(ValueError):
        m.calculate(text)


def test_calculate_error_messages():
    with pytest.raises(ValueError, match="unknown operator: \\^"):
        m.calculate("3 ^ 2")
    with pytest.raises(ValueError, match="expected: number operator number"):
        m.calculate("3 +")


def test_calculate_division_by_zero_propagates():
    with pytest.raises(ZeroDivisionError):
        m.calculate("1 / 0")


def test_event_bus():
    subscribe, publish = m.make_event_bus()
    seen = []
    subscribe("greet", lambda name: seen.append(name) or "first")
    subscribe("greet", lambda name: name.upper())
    assert publish("greet", "ana") == ["first", "ANA"]
    assert seen == ["ana"]


def test_event_bus_unknown_event_and_multiple_args():
    subscribe, publish = m.make_event_bus()
    assert publish("nothing") == []
    subscribe("add", lambda a, b: a + b)
    assert publish("add", 2, 3) == [5]
    assert publish("other", 1) == []


def test_event_buses_are_independent():
    sub1, pub1 = m.make_event_bus()
    _, pub2 = m.make_event_bus()
    sub1("x", lambda: 1)
    assert pub1("x") == [1]
    assert pub2("x") == []


def test_apply_all():
    assert m.apply_all(4, [str, lambda x: 1 / (x - 4), lambda x: x * 2]) == [
        "4",
        "error: ZeroDivisionError",
        8,
    ]


def test_apply_all_error_names():
    assert m.apply_all("a", [int, lambda s: s + 1]) == ["error: ValueError", "error: TypeError"]
    assert m.apply_all(1, []) == []
