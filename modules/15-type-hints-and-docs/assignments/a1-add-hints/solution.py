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

from collections.abc import Callable
from typing import Literal


def total(prices: list[float], tax_rate: float = 0.0) -> float:
    return sum(prices) * (1 + tax_rate)


def find_user(users: dict[str, int], name: str) -> int | None:
    return users.get(name)


def shout(words: list[str]) -> str:
    return " ".join(words).upper() + "!"


def apply_twice(f: Callable[[int], int], x: int) -> int:
    return f(f(x))


def set_mode(mode: Literal["r", "w"]) -> str:
    return f"mode={mode}"


def log(message: str) -> None:
    print(message)


if __name__ == "__main__":
    print(total([10.0, 5.0], 0.1), find_user({"ann": 1}, "bob"), shout(["hi", "there"]))
