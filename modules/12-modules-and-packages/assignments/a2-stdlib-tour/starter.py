"""Assignment 2: A tour of the standard library.

Python ships with many modules. Use the right one for each job instead of
writing the code yourself. Needs Python 3.12+ (for `itertools.batched`).
"""

import collections
import itertools
import json
import math
import random
import statistics


def chunks(items: list, size: int) -> list[tuple]:
    """Split `items` into tuples of `size` items. The last one may be shorter.

    chunks([1, 2, 3, 4, 5], 2)  -> [(1, 2), (3, 4), (5,)]
    chunks([], 3)               -> []

    Use itertools.batched.
    """
    # TODO: list(itertools.batched(items, size)).
    ...


def running_totals(numbers: list[float]) -> list[float]:
    """Return the running (cumulative) sums.

    running_totals([1, 2, 3, 4])  -> [1, 3, 6, 10]

    Use itertools.accumulate.
    """
    # TODO: list(itertools.accumulate(numbers)).
    ...


def pair_count(items: list) -> int:
    """Return how many different pairs can be chosen from `items`
    (order does not matter, no item is paired with itself).

    pair_count(["a", "b", "c", "d"])  -> 6
    pair_count(["a"])                 -> 0

    Use math.comb or itertools.combinations.
    """
    # TODO: math.comb(len(items), 2).
    ...


def distance(p: tuple[float, float], q: tuple[float, float]) -> float:
    """Return the straight-line distance between two points.

    distance((0, 0), (3, 4))  -> 5.0

    Use math.dist.
    """
    # TODO: math.dist(p, q).
    ...


def most_common_word(text: str) -> str | None:
    """Return the most frequent word of `text` (compare in lower case, words
    are separated by whitespace). When several words tie, return the one that
    appears first in the text. Return None for empty text.

    most_common_word("the cat and the hat")  -> "the"
    most_common_word("b a b a")              -> "b"

    Use collections.Counter (its most_common keeps first-seen order for ties).
    """
    # TODO: Counter(text.lower().split()).most_common(1).
    ...


def rolls(count: int, seed: int) -> list[int]:
    """Return `count` dice rolls (integers from 1 to 6) using a random number
    generator seeded with `seed`, so the same seed always gives the same list.

    Create `random.Random(seed)` and call its `randint(1, 6)`. Do not use the
    module-level functions, because they share global state.
    """
    # TODO: rng = random.Random(seed); [rng.randint(1, 6) for _ in range(count)]
    ...


def to_json(data: dict) -> str:
    """Return `data` as JSON text with sorted keys and an indent of 2 spaces.

    to_json({"b": 1, "a": [1, 2]})  ->
    {
      "a": [
        1,
        2
      ],
      "b": 1
    }
    """
    # TODO: json.dumps(..., sort_keys=True, indent=2).
    ...


def spread(numbers: list[float]) -> float:
    """Return the sample standard deviation, or 0.0 for fewer than 2 numbers.

    Use statistics.stdev.
    """
    # TODO: guard the short case, then statistics.stdev.
    ...


if __name__ == "__main__":
    print(chunks([1, 2, 3, 4, 5], 2))
    print(rolls(5, seed=42))
    print(to_json({"b": 1, "a": [1, 2]}))
