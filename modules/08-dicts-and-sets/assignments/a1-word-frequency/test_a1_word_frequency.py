import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello, World! Hello...", ["hello", "world", "hello"]),
        ("It's 5 o'clock", ["it's", "o'clock"]),
        ("", []),
        ("  ...  ", []),
    ],
)
def test_words(text, expected):
    assert m.words(text) == expected


def test_count_words():
    assert m.count_words("a b a") == {"a": 2, "b": 1}


def test_count_words_ignores_case_and_punctuation():
    assert m.count_words("The cat. THE hat!") == {"the": 2, "cat": 1, "hat": 1}


def test_count_words_empty():
    assert m.count_words("") == {}


def test_count_words_returns_plain_dict():
    assert type(m.count_words("a")) is dict


def test_top_words_orders_by_count():
    assert m.top_words("b a b c a b", 2) == [("b", 3), ("a", 2)]


def test_top_words_ties_are_alphabetical():
    assert m.top_words("c b a", 2) == [("a", 1), ("b", 1)]


def test_top_words_fewer_than_n():
    assert m.top_words("b a c", 5) == [("a", 1), ("b", 1), ("c", 1)]


def test_top_words_default_n_is_three():
    assert len(m.top_words("a b c d e")) == 3


def test_unique_words():
    assert m.unique_words("b a b c A") == ["a", "b", "c"]
    assert m.unique_words("") == []
