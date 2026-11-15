"""Assignment 1: Four list utilities.

None of these functions may change the list they receive. Return a new list.
"""


def rotate(items: list, k: int) -> list:
    """Return a new list rotated `k` places to the right.

    A negative k rotates to the left. k may be larger than the list length.
    An empty list stays empty.

    rotate([1, 2, 3, 4, 5], 2)   -> [4, 5, 1, 2, 3]
    rotate([1, 2, 3, 4, 5], -1)  -> [2, 3, 4, 5, 1]
    rotate([1, 2, 3], 7)         -> [3, 1, 2]
    rotate([], 3)                -> []
    """
    # TODO: use % to reduce k, then join two slices. Be careful with k == 0.
    ...


def flatten(nested: list) -> list:
    """Flatten ONE level: items that are lists are spread out, others are kept.

    flatten([1, [2, 3], [], [4]])     -> [1, 2, 3, 4]
    flatten([[1, [2]], 3])            -> [1, [2], 3]      (only one level)
    flatten([])                       -> []
    """
    # TODO: loop; extend() for lists, append() for everything else.
    ...


def dedupe(items: list) -> list:
    """Remove duplicates but keep the first occurrence and the original order.

    The items can be numbers or strings (anything that supports `in`).

    dedupe([3, 1, 3, 2, 1])      -> [3, 1, 2]
    dedupe(["b", "a", "b"])      -> ["b", "a"]
    dedupe([])                   -> []
    """
    # TODO: keep a result list and add an item only if it is not in it yet.
    ...


def running_totals(numbers: list[float]) -> list[float]:
    """Return the running (cumulative) sums.

    running_totals([1, 2, 3, 4])   -> [1, 3, 6, 10]
    running_totals([5])            -> [5]
    running_totals([])             -> []
    """
    # TODO: an accumulator that you append to the result in every round.
    ...


if __name__ == "__main__":
    print(rotate([1, 2, 3, 4, 5], 2))
    print(flatten([1, [2, 3], [], [4]]))
    print(dedupe([3, 1, 3, 2, 1]))
    print(running_totals([1, 2, 3, 4]))
