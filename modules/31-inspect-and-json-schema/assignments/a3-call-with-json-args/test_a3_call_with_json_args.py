from typing import Literal

import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("value", "hint", "expected"),
    [
        (1, int, True),
        ("1", int, False),
        (True, int, False),
        (True, bool, True),
        (1, bool, False),
        (1, float, True),
        (1.5, float, True),
        (1.5, int, False),
        ("x", str, True),
        (None, str | None, True),
        ("x", str | None, True),
        (3, str | None, False),
        (["a", "b"], list[str], True),
        (["a", 1], list[str], False),
        ("ab", list[str], False),
        ([[1], [2, 3]], list[list[int]], True),
        ([1, 2], list[float], True),
        ("red", Literal["red", "blue"], True),
        ("green", Literal["red", "blue"], False),
    ],
)
def test_matches(value, hint, expected):
    assert m.matches(value, hint) is expected


def add(a: int, b: int = 1) -> int:
    return a + b


def test_calls_function():
    assert m.call_with_json_args(add, {"a": 2, "b": 5}) == 7


def test_defaults_are_kept():
    assert m.call_with_json_args(add, {"a": 2}) == 3


def test_missing_argument():
    with pytest.raises(m.ArgumentError) as info:
        m.call_with_json_args(add, {})
    assert info.value.errors == ["missing argument: a"]


def test_wrong_type_message():
    with pytest.raises(m.ArgumentError) as info:
        m.call_with_json_args(add, {"a": "2"})
    assert info.value.errors == ["argument a: expected int, got string"]


def test_bool_is_not_an_integer():
    with pytest.raises(m.ArgumentError) as info:
        m.call_with_json_args(add, {"a": True})
    assert info.value.errors == ["argument a: expected int, got boolean"]


def test_generic_hint_in_message():
    def total(values: list[int]) -> int:
        return sum(values)

    with pytest.raises(m.ArgumentError) as info:
        m.call_with_json_args(total, {"values": [1, "2"]})
    assert info.value.errors == ["argument values: expected list[int], got array"]
    assert m.call_with_json_args(total, {"values": [1, 2]}) == 3


def test_collects_all_errors_in_order():
    def f(x: int, y: str, z: float = 0.0):
        return None

    with pytest.raises(m.ArgumentError) as info:
        m.call_with_json_args(f, {"z": "a", "x": 1.5, "w": 1, "b": 2})
    assert info.value.errors == [
        "argument x: expected int, got number",
        "missing argument: y",
        "argument z: expected float, got string",
        "unknown argument: b",
        "unknown argument: w",
    ]


def test_untyped_parameter_accepts_anything():
    def echo(value):
        return value

    assert m.call_with_json_args(echo, {"value": [1, "x"]}) == [1, "x"]


def test_function_is_not_called_when_invalid():
    calls = []

    def record(n: int):
        calls.append(n)

    with pytest.raises(m.ArgumentError):
        m.call_with_json_args(record, {"n": "x"})
    assert calls == []

