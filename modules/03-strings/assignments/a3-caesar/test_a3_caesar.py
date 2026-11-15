import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("char", "shift", "expected"),
    [
        ("a", 3, "d"),
        ("Z", 1, "A"),
        ("b", -3, "y"),
        ("!", 5, "!"),
        (" ", 5, " "),
        ("é", 5, "é"),
        ("m", 0, "m"),
        ("a", 52, "a"),
    ],
)
def test_shift_char(char, shift, expected):
    assert m.shift_char(char, shift) == expected


@pytest.mark.parametrize(
    ("text", "shift", "expected"),
    [
        ("Hello, World!", 3, "Khoor, Zruog!"),
        ("abc xyz", 1, "bcd yza"),
        ("abc", 26, "abc"),
        ("", 7, ""),
        ("Café 42", 1, "Dbgé 42"),
    ],
)
def test_encrypt(text, shift, expected):
    assert m.encrypt(text, shift) == expected


@pytest.mark.parametrize("shift", [0, 1, 3, 13, 25, -4, 30])
def test_decrypt_round_trip(shift):
    message = "The Quick Brown Fox, 123!"
    assert m.decrypt(m.encrypt(message, shift), shift) == message


def test_decrypt_example():
    assert m.decrypt("Khoor, Zruog!", 3) == "Hello, World!"


def test_crack():
    assert m.crack("Khoor, Zruog!", "world") == 3
    assert m.crack(m.encrypt("Meet me at noon", 11), "NOON") == 11


def test_crack_not_found():
    assert m.crack("Khoor", "xyz") is None
    assert m.crack("Khoor", "hello") == 3
