"""Assignment 1: A parallel map that keeps the input order."""

from collections.abc import Callable, Iterable
from typing import Any


def parallel_map(func: Callable[[Any], Any], items: Iterable, workers: int = 4) -> list:
    """Apply `func` to every item using a pool of `workers` threads.

    - Return the results as a list in the same order as `items`, no matter
      which job finishes first.
    - If a job raises an exception, let that exception propagate to the caller.
    - Raise ValueError if `workers` is less than 1.
    - An empty `items` gives [].
    """
    # TODO: use concurrent.futures.ThreadPoolExecutor and its map method.
    ...


def parallel_lengths(texts: list[str], workers: int = 4) -> dict[str, int]:
    """Return {text: len(text)} for every text, computed with parallel_map.

    The dict keeps the order of `texts`. Duplicate texts appear once.
    """
    # TODO: call parallel_map(len, texts, workers) and build the dict.
    ...


if __name__ == "__main__":
    print(parallel_map(str.upper, ["a", "b", "c"]))
    print(parallel_lengths(["pear", "fig", "banana"]))
