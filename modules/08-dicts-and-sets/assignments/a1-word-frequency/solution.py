"""Assignment 1: Word frequency.

Count how often each word appears in a text. Practises dict counting,
`dict.get`, `collections.Counter` and sorting with a key.
"""

import re


def words(text: str) -> list[str]:
    """Return the lowercase words in `text`, in order.

    A word is a run of letters or apostrophes. Everything else separates words.

    words("Hello, World! Hello...")  -> ["hello", "world", "hello"]
    words("It's 5 o'clock")          -> ["it's", "o'clock"]
    words("")                        -> []

    Hint: re.findall(r"[a-z']+", text.lower())
    """
    return re.findall(r"[a-z']+", text.lower())


def count_words(text: str) -> dict[str, int]:
    """Return a dict that maps each word (see `words`) to its count.

    Build it with a plain dict and `counts.get(word, 0) + 1`.
    Do not use collections.Counter here.

    count_words("a b a")  -> {"a": 2, "b": 1}
    count_words("")       -> {}
    """
    counts: dict[str, int] = {}
    for word in words(text):
        counts[word] = counts.get(word, 0) + 1
    return counts


def top_words(text: str, n: int = 3) -> list[tuple[str, int]]:
    """Return the `n` most common words as (word, count) pairs.

    Sort by count, highest first. Words with equal counts are sorted
    alphabetically. If there are fewer than `n` distinct words, return them all.

    top_words("b a b c a b", 2)  -> [("b", 3), ("a", 2)]
    top_words("b a c", 5)        -> [("a", 1), ("b", 1), ("c", 1)]
    """
    ranked = sorted(count_words(text).items(), key=lambda pair: (-pair[1], pair[0]))
    return ranked[:n]


def unique_words(text: str) -> list[str]:
    """Return the distinct words of `text` in alphabetical order, using a set.

    unique_words("b a b c")  -> ["a", "b", "c"]
    """
    return sorted(set(words(text)))


if __name__ == "__main__":
    sample = "The cat and the hat. The end!"
    print(count_words(sample))
    print(top_words(sample, 2))
