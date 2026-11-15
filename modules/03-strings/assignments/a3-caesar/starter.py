"""Assignment 3: Caesar cipher.

Shift every letter by a fixed number of places in the alphabet. Other
characters stay as they are. Practise loops over strings, ord(), chr() and %.
"""


def shift_char(char: str, shift: int) -> str:
    """Shift one character. Keep its case. Non-letters (a-z, A-Z only) are unchanged.

    shift_char("a", 3)  -> "d"
    shift_char("Z", 1)  -> "A"
    shift_char("b", -3) -> "y"
    shift_char("!", 5)  -> "!"
    shift_char("é", 5)  -> "é"
    """
    # TODO: for a letter, compute (ord(char) - ord(base) + shift) % 26 and add base back.
    ...


def encrypt(text: str, shift: int) -> str:
    """Shift every character of text.

    encrypt("Hello, World!", 3) -> "Khoor, Zruog!"
    encrypt("abc xyz", 1)       -> "bcd yza"
    encrypt("abc", 26)          -> "abc"
    """
    # TODO: use shift_char for every character and join the results.
    ...


def decrypt(text: str, shift: int) -> str:
    """Undo encrypt(text, shift).

    decrypt("Khoor, Zruog!", 3) -> "Hello, World!"
    """
    # TODO
    ...


def crack(text: str, known_word: str) -> int | None:
    """Find the shift (0 to 25) that makes decrypt(text, shift) contain known_word.

    The search ignores case. Return the smallest matching shift, or None.

    crack("Khoor, Zruog!", "world") -> 3
    crack("Khoor", "xyz")           -> None
    """
    # TODO: try every shift from 0 to 25.
    ...


if __name__ == "__main__":
    secret = encrypt("Attack at dawn", 5)
    print(secret, "->", decrypt(secret, 5))
