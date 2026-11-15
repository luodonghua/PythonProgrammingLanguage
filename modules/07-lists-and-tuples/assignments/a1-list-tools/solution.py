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
    if not items:
        return []
    k %= len(items)
    return items[-k:] + items[:-k] if k else items[:]


def flatten(nested: list) -> list:
    """Flatten ONE level: items that are lists are spread out, others are kept.

    flatten([1, [2, 3], [], [4]])     -> [1, 2, 3, 4]
    flatten([[1, [2]], 3])            -> [1, [2], 3]      (only one level)
    flatten([])                       -> []
    """
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(item)
        else:
            result.append(item)
    return result


def dedupe(items: list) -> list:
    """Remove duplicates but keep the first occurrence and the original order.

    The items can be numbers or strings (anything that supports `in`).

    dedupe([3, 1, 3, 2, 1])      -> [3, 1, 2]
    dedupe(["b", "a", "b"])      -> ["b", "a"]
    dedupe([])                   -> []
    """
    result = []
    for item in items:
        if item not in result:
            result.append(item)
    return result


def running_totals(numbers: list[float]) -> list[float]:
    """Return the running (cumulative) sums.

    running_totals([1, 2, 3, 4])   -> [1, 3, 6, 10]
    running_totals([5])            -> [5]
    running_totals([])             -> []
    """
    totals = []
    total = 0
    for number in numbers:
        total += number
        totals.append(total)
    return totals


if __name__ == "__main__":
    print(rotate([1, 2, 3, 4, 5], 2))
    print(flatten([1, [2, 3], [], [4]]))
    print(dedupe([3, 1, 3, 2, 1]))
    print(running_totals([1, 2, 3, 4]))
