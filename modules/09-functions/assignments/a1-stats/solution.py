"""Assignment 1: Functions that return values.

Write small, pure functions: they take parameters, return a result and do
not print or change their arguments.
"""


def min_max(numbers: list[float]) -> tuple[float, float]:
    """Return (smallest, largest) of a non-empty list.

    min_max([3, 1, 4, 1, 5])  -> (1, 5)
    min_max([7])              -> (7, 7)

    You may assume the list is not empty.
    """
    return min(numbers), max(numbers)


def mean(numbers: list[float]) -> float | None:
    """Return the average, or None for an empty list.

    mean([1, 2, 3, 4])  -> 2.5
    mean([])            -> None
    """
    if not numbers:
        return None
    return sum(numbers) / len(numbers)


def median(numbers: list[float]) -> float | None:
    """Return the middle value, or None for an empty list.

    With an even number of items, return the average of the two middle values.
    Do not change the input list.

    median([5, 1, 3])      -> 3
    median([4, 1, 3, 2])   -> 2.5
    median([])             -> None
    """
    if not numbers:
        return None
    ordered = sorted(numbers)
    middle = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def stats(numbers: list[float]) -> dict:
    """Return a dict with the keys "count", "min", "max", "mean" and "median".

    For an empty list, "count" is 0 and every other value is None.

    stats([1, 2, 3, 4])
        -> {"count": 4, "min": 1, "max": 4, "mean": 2.5, "median": 2.5}
    stats([])
        -> {"count": 0, "min": None, "max": None, "mean": None, "median": None}
    """
    if not numbers:
        return {"count": 0, "min": None, "max": None, "mean": None, "median": None}
    low, high = min_max(numbers)
    return {
        "count": len(numbers),
        "min": low,
        "max": high,
        "mean": mean(numbers),
        "median": median(numbers),
    }


def split_name(full_name: str) -> tuple[str, str]:
    """Split "First Last" into (first, last).

    The first word is the first name. Everything after it is the last name.
    A single word has an empty last name. Outer spaces are ignored.

    split_name("Ada Lovelace")        -> ("Ada", "Lovelace")
    split_name("  Mary Ann Smith ")   -> ("Mary", "Ann Smith")
    split_name("Plato")               -> ("Plato", "")
    """
    parts = full_name.strip().split(maxsplit=1)
    if not parts:
        return "", ""
    first = parts[0]
    last = parts[1] if len(parts) > 1 else ""
    return first, last


if __name__ == "__main__":
    print(stats([1, 2, 3, 4]))
    print(split_name("Ada Lovelace"))
