import pytest

from practice import load

m = load(__file__)


def param_names(obj):
    return [p.__name__ for p in getattr(obj, "__type_params__", ())]


def test_first_and_last():
    assert param_names(m.first) == ["T"]
    assert param_names(m.last) == ["T"]
    assert m.first([3, 4]) == 3
    assert m.first("xyz") == "x"
    assert m.last((1, 2, 3)) == 3
    assert m.first([]) is None
    assert m.last("") is None


def test_pairs():
    assert param_names(m.pairs) == ["A", "B"]
    assert m.pairs([1, 2], "ab") == [(1, "a"), (2, "b")]
    assert m.pairs([], []) == []


def test_pairs_length_mismatch():
    assert m.pairs([1], [2]) == [(1, 2)]
    with pytest.raises(ValueError):
        m.pairs([1, 2], [1])


def test_box_is_generic():
    assert param_names(m.Box) == ["T"]
    assert param_names(m.Box.map) == ["U"]


def test_box_get_and_repr():
    b = m.Box(3)
    assert b.get() == 3
    assert repr(b) == "Box(3)"
    assert repr(m.Box("a")) == "Box('a')"


def test_box_map_returns_a_new_box():
    b = m.Box(3)
    c = b.map(str)
    assert isinstance(c, m.Box)
    assert c.get() == "3"
    assert b.get() == 3
    assert c is not b


def test_box_map_chain():
    assert m.Box(2).map(lambda n: n * 10).map(lambda n: n + 1).get() == 21
