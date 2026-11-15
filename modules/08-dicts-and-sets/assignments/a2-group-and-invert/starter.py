"""Assignment 2: Group, invert and merge dictionaries.

Practises dict building, `setdefault` / `defaultdict`, dict comprehensions
and the `|` merge operator.
"""

from collections.abc import Callable, Hashable, Iterable


def group_by(items: Iterable, key: Callable) -> dict:
    """Group `items` by the value of `key(item)`.

    Return a dict that maps each key to the list of items that produced it.
    Items keep their original order inside each list.

    group_by(["apple", "avocado", "bean"], lambda s: s[0])
        -> {"a": ["apple", "avocado"], "b": ["bean"]}
    group_by([], len)  -> {}
    """
    # TODO: use collections.defaultdict(list) or dict.setdefault.
    ...


def invert(mapping: dict) -> dict:
    """Swap keys and values. Return a dict that maps each value to a sorted
    list of the keys that had that value.

    invert({"a": 1, "b": 2, "c": 1})  -> {1: ["a", "c"], 2: ["b"]}
    invert({})                        -> {}
    """
    # TODO: loop over mapping.items() and collect keys per value.
    ...


def with_defaults(settings: dict, defaults: dict) -> dict:
    """Return a new dict with `defaults` overridden by `settings`.

    Neither argument may be changed.

    with_defaults({"color": "red"}, {"color": "blue", "size": 3})
        -> {"color": "red", "size": 3}
    """
    # TODO: use the | operator.
    ...


def squares_of_evens(numbers: Iterable[int]) -> dict[int, int]:
    """Return {n: n * n} for each even number n in `numbers`, with a dict comprehension.

    squares_of_evens([1, 2, 3, 4])  -> {2: 4, 4: 16}
    """
    # TODO: write the comprehension.
    ...


def first_duplicate(items: Iterable[Hashable]):
    """Return the first item that appears for the second time, or None.

    Use a set of the items you have already seen.

    first_duplicate([3, 1, 4, 1, 5, 3])  -> 1
    first_duplicate(["a", "b"])          -> None
    """
    # TODO: keep a `seen` set.
    ...


if __name__ == "__main__":
    print(group_by(["apple", "avocado", "bean"], lambda s: s[0]))
    print(invert({"a": 1, "b": 2, "c": 1}))
