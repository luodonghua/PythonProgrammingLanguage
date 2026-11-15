"""Assignment 1: Sort with key= functions.

Use `key=` (lambdas, tuples, operator.itemgetter). Do not write your own
sorting loops.
"""

from operator import itemgetter


def rank_students(students: list[dict]) -> list[str]:
    """Return student names ranked best first.

    Each student is {"name": str, "score": int}. Higher score comes first.
    Equal scores are ordered by name, ignoring case (A-Z).
    Example: [{"name": "bo", "score": 80}, {"name": "Al", "score": 80},
              {"name": "Cy", "score": 95}]  ->  ["Cy", "Al", "bo"]
    Do not change the input list.
    """
    ranked = sorted(students, key=lambda s: (-s["score"], s["name"].lower()))
    return [s["name"] for s in ranked]


def longest_words(words: list[str], n: int) -> list[str]:
    """Return the `n` longest words, longest first.

    Words of the same length are ordered A-Z (plain string order).
    If n is larger than the list, return all words in that order.
    """
    return sorted(words, key=lambda w: (-len(w), w))[:n]


def sort_by_fields(rows: list[dict], *fields: str, reverse: bool = False) -> list[dict]:
    """Return a new list of dicts sorted by the given fields, in order.

    sort_by_fields(rows, "city", "age") sorts by city, then by age.
    With no fields, return a copy in the original order.
    Use operator.itemgetter(*fields) as the key. Careful: itemgetter() with
    no names raises TypeError, so handle the "no fields" case first.
    """
    if not fields:
        return list(rows)
    return sorted(rows, key=itemgetter(*fields), reverse=reverse)


def cheapest_and_priciest(prices: dict[str, float]) -> tuple[str, str]:
    """Return (name of the cheapest item, name of the most expensive item).

    Use min() and max() with key=prices.get. Raise ValueError for an empty dict.
    """
    if not prices:
        raise ValueError("no prices")
    return min(prices, key=prices.get), max(prices, key=prices.get)


if __name__ == "__main__":
    people = [{"name": "bo", "score": 80}, {"name": "Al", "score": 80}, {"name": "Cy", "score": 95}]
    print(rank_students(people))
    print(longest_words(["pear", "fig", "banana", "kiwi"], 2))
