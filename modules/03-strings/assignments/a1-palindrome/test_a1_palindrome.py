import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("racecar", True),
        ("A man, a plan, a canal: Panama", True),
        ("Was it a car or a cat I saw?", True),
        ("Hello", False),
        ("ab", False),
        ("", True),
        ("!!!", True),
        ("12321", True),
        ("12345", False),
    ],
)
def test_is_palindrome(text, expected):
    assert m.is_palindrome(text) is expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("hello   WORLD", "Hello World"),
        ("  python is fun ", "Python Is Fun"),
        ("a", "A"),
        ("", ""),
        ("   ", ""),
        ("mcDONALD farm", "Mcdonald Farm"),
    ],
)
def test_title_case(text, expected):
    assert m.title_case(text) == expected


def test_count_words():
    assert m.count_words("the cat and The dog.") == {"the": 2, "cat": 1, "and": 1, "dog": 1}


def test_count_words_punctuation():
    assert m.count_words("Yes, yes! No? yes; no: maybe.") == {"yes": 3, "no": 2, "maybe": 1}


def test_count_words_empty():
    result = m.count_words("   ")
    assert result == {}
    assert isinstance(result, dict)
