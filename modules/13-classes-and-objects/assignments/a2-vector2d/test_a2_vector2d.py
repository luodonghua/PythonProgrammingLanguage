import math

import pytest

from practice import load

m = load(__file__)
V = m.Vector2D


def test_attributes_and_repr():
    v = V(1, 2)
    assert (v.x, v.y) == (1, 2)
    assert repr(v) == "Vector2D(1, 2)"
    assert repr(V(1.5, -2)) == "Vector2D(1.5, -2)"


def test_equality():
    assert V(1, 2) == V(1, 2)
    assert V(1, 2) != V(2, 1)
    assert (V(1, 2) == (1, 2)) is False


def test_add_and_sub():
    assert V(1, 2) + V(3, 4) == V(4, 6)
    assert V(5, 5) - V(1, 2) == V(4, 3)


def test_scalar_multiplication_both_sides():
    assert V(1, 2) * 3 == V(3, 6)
    assert 3 * V(1, 2) == V(3, 6)
    assert 0.5 * V(4, 2) == V(2.0, 1.0)


def test_negation():
    assert -V(1, -2) == V(-1, 2)


def test_abs_is_length():
    assert abs(V(3, 4)) == 5
    assert abs(V(1, 1)) == pytest.approx(math.sqrt(2))


def test_unpacking():
    x, y = V(7, 8)
    assert (x, y) == (7, 8)
    assert list(V(1, 2)) == [1, 2]


def test_bool():
    assert not V(0, 0)
    assert V(0, 1)
    assert V(-1, 0)


def test_operators_do_not_mutate():
    a = V(1, 1)
    _ = a + V(1, 1)
    _ = a * 5
    assert a == V(1, 1)


def test_unsupported_types_raise_type_error():
    assert V(1, 2) + V(1, 1) == V(2, 3)  # supported operands still work
    with pytest.raises(TypeError):
        V(1, 2) + 5
    with pytest.raises(TypeError):
        V(1, 2) * "a"
    with pytest.raises(TypeError):
        V(1, 2) * V(1, 2)
