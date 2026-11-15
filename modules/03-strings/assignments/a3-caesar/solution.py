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
    if "a" <= char <= "z":
        base = ord("a")
    elif "A" <= char <= "Z":
        base = ord("A")
    else:
        return char
    return chr((ord(char) - base + shift) % 26 + base)


def encrypt(text: str, shift: int) -> str:
    """Shift every character of text.

    encrypt("Hello, World!", 3) -> "Khoor, Zruog!"
    encrypt("abc xyz", 1)       -> "bcd yza"
    encrypt("abc", 26)          -> "abc"
    """
    return "".join(shift_char(char, shift) for char in text)


def decrypt(text: str, shift: int) -> str:
    """Undo encrypt(text, shift).

    decrypt("Khoor, Zruog!", 3) -> "Hello, World!"
    """
    return encrypt(text, -shift)


def crack(text: str, known_word: str) -> int | None:
    """Find the shift (0 to 25) that makes decrypt(text, shift) contain known_word.

    The search ignores case. Return the smallest matching shift, or None.

    crack("Khoor, Zruog!", "world") -> 3
    crack("Khoor", "xyz")           -> None
    """
    for shift in range(26):
        if known_word.lower() in decrypt(text, shift).lower():
            return shift
    return None


if __name__ == "__main__":
    secret = encrypt("Attack at dawn", 5)
    print(secret, "->", decrypt(secret, 5))
