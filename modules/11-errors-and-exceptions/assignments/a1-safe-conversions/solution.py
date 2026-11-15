"""Assignment 1: Catch specific exceptions.

Each function must catch only the exceptions named in its docstring.
Never use a bare `except:`.
"""


def safe_int(text, default=None):
    """Convert `text` to an int. Return `default` if that is impossible.

    safe_int("42")        -> 42
    safe_int(" 7 ")       -> 7
    safe_int("4.5")       -> None
    safe_int("abc", 0)    -> 0
    safe_int(None, -1)    -> -1     (int(None) raises TypeError)
    """
    try:
        return int(text)
    except (ValueError, TypeError):
        return default


def safe_divide(a, b):
    """Return a / b, or None when b is zero.

    safe_divide(6, 3)  -> 2.0
    safe_divide(1, 0)  -> None
    Other errors (for example a str argument) must NOT be hidden.
    """
    try:
        return a / b
    except ZeroDivisionError:
        return None


def get_or_default(items, index, default=None):
    """Return items[index], or `default` if the index is out of range.

    get_or_default([10, 20], 1)        -> 20
    get_or_default([10, 20], 5, "x")   -> "x"
    get_or_default([10, 20], -1)       -> 20
    """
    try:
        return items[index]
    except IndexError:
        return default


def read_number(data: dict, key: str) -> int | None:
    """Return int(data[key]), or None if the key is missing or the value
    cannot be converted.

    read_number({"n": "5"}, "n")      -> 5
    read_number({"n": "five"}, "n")   -> None
    read_number({}, "n")              -> None
    """
    try:
        return int(data[key])
    except (KeyError, ValueError, TypeError):
        return None


def error_name(func) -> str | None:
    """Call `func()` with no arguments. Return the class name of the exception
    it raises (for example "ZeroDivisionError"), or None if it finishes normally.

    error_name(lambda: 1 / 0)      -> "ZeroDivisionError"
    error_name(lambda: [][0])      -> "IndexError"
    error_name(lambda: 1 + 1)      -> None
    """
    try:
        func()
    except Exception as exc:
        return type(exc).__name__
    return None


if __name__ == "__main__":
    print(safe_int("42"), safe_int("abc", 0))
    print(error_name(lambda: int("x")))
