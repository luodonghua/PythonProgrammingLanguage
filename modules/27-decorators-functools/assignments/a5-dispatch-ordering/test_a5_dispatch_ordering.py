import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (5, "int 5"),
        (True, "int True"),
        ("hi", "text 'hi'"),
        ([1, 2, 3], "list of 3"),
        ([], "list of 0"),
        ({"a": 1, "b": 2}, "dict with keys a, b"),
        (2.5, "object 2.5"),
        (None, "object None"),
    ],
)
def test_describe(value, expected):
    assert m.describe(value) == expected


def test_version_parts_and_repr():
    v = m.Version("1.10.2")
    assert v.parts == (1, 10, 2)
    assert repr(v) == "Version('1.10.2')"


def test_version_compares_numbers_not_text():
    assert m.Version("1.10") > m.Version("1.9")
    assert m.Version("1.9") < m.Version("1.10")


def test_version_all_operators():
    a, b = m.Version("1.2"), m.Version("1.3")
    assert a < b and a <= b and b > a and b >= a
    assert a <= m.Version("1.2") and a >= m.Version("1.2")
    assert a == m.Version("1.2")
    assert a != b


def test_version_sorted():
    versions = [m.Version(t) for t in ("2.0", "1.10", "1.9", "1.9.1")]
    assert [v.parts for v in sorted(versions)] == [(1, 9), (1, 9, 1), (1, 10), (2, 0)]


def test_version_with_other_types():
    v = m.Version("1.0")
    assert (v == "1.0") is False
    with pytest.raises(TypeError):
        v < 3
