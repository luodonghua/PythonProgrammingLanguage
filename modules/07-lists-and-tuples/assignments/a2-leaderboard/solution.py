"""Assignment 2: A leaderboard built from (name, score) tuples.

Practise sorted() with key=, slicing, tuple unpacking and enumerate.
"""

Score = tuple[str, int]


def top_n(scores: list[Score], n: int) -> list[Score]:
    """Return the n best scores, highest first.

    Ties are broken by name in alphabetical order. If there are fewer than n
    scores, return all of them. The input list must not change.

    top_n([("Ann", 70), ("Bob", 90), ("Cy", 70)], 2) -> [("Bob", 90), ("Ann", 70)]
    top_n([("Zed", 50), ("Amy", 50)], 5)             -> [("Amy", 50), ("Zed", 50)]
    top_n([], 3)                                     -> []
    top_n([("Ann", 70)], 0)                          -> []
    """
    ranked = sorted(scores, key=lambda entry: (-entry[1], entry[0]))
    return ranked[:n]


def best_and_worst(scores: list[Score]) -> tuple[Score, Score]:
    """Return (best, worst) as two (name, score) tuples.

    On ties the entry that comes first in the list wins, for both.

    best_and_worst([("Ann", 70), ("Bob", 90), ("Cy", 55)]) -> (("Bob", 90), ("Cy", 55))

    Raise ValueError for an empty list.
    """
    if not scores:
        raise ValueError("no scores")
    best = worst = scores[0]
    for entry in scores[1:]:
        if entry[1] > best[1]:
            best = entry
        if entry[1] < worst[1]:
            worst = entry
    return best, worst


def ranking(scores: list[Score]) -> list[tuple[int, str, int]]:
    """Return (rank, name, score) rows, best first. Equal scores share a rank.

    Use "competition ranking": after a tie, the next rank skips numbers.
    Order rows like top_n (score descending, then name).

    ranking([("Ann", 90), ("Bob", 80), ("Cy", 80), ("Di", 70)])
        -> [(1, "Ann", 90), (2, "Bob", 80), (2, "Cy", 80), (4, "Di", 70)]
    ranking([]) -> []
    """
    rows = []
    previous_score = None
    rank = 0
    for position, (name, score) in enumerate(top_n(scores, len(scores)), start=1):
        if score != previous_score:
            rank = position
            previous_score = score
        rows.append((rank, name, score))
    return rows


def average(scores: list[Score]) -> float:
    """Return the mean score rounded to 1 decimal. Return 0.0 for an empty list.

    average([("Ann", 70), ("Bob", 91)]) -> 80.5
    """
    if not scores:
        return 0.0
    return round(sum(score for _, score in scores) / len(scores), 1)


if __name__ == "__main__":
    data = [("Ann", 90), ("Bob", 80), ("Cy", 80), ("Di", 70)]
    print(top_n(data, 2))
    print(ranking(data))
