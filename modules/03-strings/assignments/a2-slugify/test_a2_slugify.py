import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("title", "expected"),
    [
        ("Hello, World!", "hello-world"),
        ("  Python   3.14 -- new", "python-3-14-new"),
        ("---", ""),
        ("", ""),
        ("C++ & Rust", "c-rust"),
        ("already-a-slug", "already-a-slug"),
        ("UPPER lower 42", "upper-lower-42"),
        ("tabs\tand\nnewlines", "tabs-and-newlines"),
    ],
)
def test_slugify(title, expected):
    assert m.slugify(title) == expected


def test_unique_slug_free():
    assert m.unique_slug("Hello", set()) == "hello"


def test_unique_slug_taken():
    assert m.unique_slug("Hello", {"hello"}) == "hello-2"
    assert m.unique_slug("Hello", {"hello", "hello-2"}) == "hello-3"
    assert m.unique_slug("Hello", {"hello", "hello-3"}) == "hello-2"


def test_unique_slug_does_not_change_taken():
    taken = {"hello"}
    assert m.unique_slug("Hello", taken) == "hello-2"
    assert taken == {"hello"}


@pytest.mark.parametrize(
    ("text", "width", "expected"),
    [
        ("Hello, World", 20, "Hello, World"),
        ("Hello, World", 8, "Hello..."),
        ("Hello", 5, "Hello"),
        ("Hello!", 5, "He..."),
        ("abcdef", 3, "..."),
    ],
)
def test_truncate(text, width, expected):
    result = m.truncate(text, width)
    assert result == expected
    assert len(result) <= width


def test_truncate_custom_suffix():
    assert m.truncate("Hello, World", 7, "~") == "Hello,~"


def test_truncate_bad_width():
    with pytest.raises(ValueError):
        m.truncate("Hello, World", 2)
