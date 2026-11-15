"""Assignment 2: Group, invert and merge dictionaries.

Practises dict building, `setdefault` / `defaultdict`, dict comprehensions
and the `|` merge operator.
"""

from collections import defaultdict
from collections.abc import Callable, Hashable, Iterable


def group_by(items: Iterable, key: Callable) -> dict:
    """Group `items` by the value of `key(item)`.

    Return a dict that maps each key to the list of items that produced it.
    Items keep their original order inside each list.

    group_by(["apple", "avocado", "bean"], lambda s: s[0])
        -> {"a": ["apple", "avocado"], "b": ["bean"]}
    group_by([], len)  -> {}
    """
    groups = defaultdict(list)
    for item in items:
        groups[key(item)].append(item)
    return dict(groups)


def invert(mapping: dict) -> dict:
    """Swap keys and values. Return a dict that maps each value to a sorted
    list of the keys that had that value.

    invert({"a": 1, "b": 2, "c": 1})  -> {1: ["a", "c"], 2: ["b"]}
    invert({})                        -> {}
    """
    result: dict = {}
    for k, v in mapping.items():
        result.setdefault(v, []).append(k)
    return {v: sorted(keys) for v, keys in result.items()}


def with_defaults(settings: dict, defaults: dict) -> dict:
    """Return a new dict with `defaults` overridden by `settings`.

    Neither argument may be changed.

    with_defaults({"color": "red"}, {"color": "blue", "size": 3})
        -> {"color": "red", "size": 3}
    """
    return defaults | settings


def squares_of_evens(numbers: Iterable[int]) -> dict[int, int]:
    """Return {n: n * n} for each even number n in `numbers`, with a dict comprehension.

    squares_of_evens([1, 2, 3, 4])  -> {2: 4, 4: 16}
    """
    return {n: n * n for n in numbers if n % 2 == 0}


def first_duplicate(items: Iterable[Hashable]):
    """Return the first item that appears for the second time, or None.

    Use a set of the items you have already seen.

    first_duplicate([3, 1, 4, 1, 5, 3])  -> 1
    first_duplicate(["a", "b"])          -> None
    """
    seen = set()
    for item in items:
        if item in seen:
            return item
        seen.add(item)
    return None


if __name__ == "__main__":
    print(group_by(["apple", "avocado", "bean"], lambda s: s[0]))
    print(invert({"a": 1, "b": 2, "c": 1}))
