"""Assignment 1: Add type hints to working functions.

The functions below already work. Your job is to add annotations, using
exactly these types:

    total(prices, tax_rate=0.0)      prices: list[float]; tax_rate: float; returns float
    find_user(users, name)           users: dict[str, int]; name: str; returns int | None
    shout(words)                     words: list[str]; returns str
    apply_twice(f, x)                f: Callable[[int], int]; x: int; returns int
    set_mode(mode)                   mode: Literal["r", "w"]; returns str
    log(message)                     message: str; returns None

Import what you need (Callable from collections.abc, Literal from typing).
Do not change the function bodies.
"""


# TODO: add the hints to every function below.
def total(prices, tax_rate=0.0):
    return sum(prices) * (1 + tax_rate)


def find_user(users, name):
    return users.get(name)


def shout(words):
    return " ".join(words).upper() + "!"


def apply_twice(f, x):
    return f(f(x))


def set_mode(mode):
    return f"mode={mode}"


def log(message):
    print(message)


if __name__ == "__main__":
    print(total([10.0, 5.0], 0.1), find_user({"ann": 1}, "bob"), shout(["hi", "there"]))
