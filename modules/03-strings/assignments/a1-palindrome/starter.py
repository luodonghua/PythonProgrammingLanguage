"""Assignment 1: Palindromes and word tools.

Practise slicing, methods such as lower(), split() and join(), and str.isalnum().
"""


def is_palindrome(text: str) -> bool:
    """Return True if text reads the same forwards and backwards.

    Ignore case, spaces and punctuation: only letters and digits count.
    An empty text (or one with no letters or digits) counts as a palindrome.

    is_palindrome("racecar")                        -> True
    is_palindrome("A man, a plan, a canal: Panama") -> True
    is_palindrome("Hello")                          -> False
    is_palindrome("")                               -> True
    """
    # TODO: keep only c.lower() for characters where c.isalnum(), then compare with its reverse (s[::-1]).
    ...


def title_case(text: str) -> str:
    """Capitalise every word and squeeze repeated spaces into one.

    Only the first letter of each word is upper case, the rest is lower case.
    Leading and trailing spaces are removed.

    title_case("hello   WORLD")      -> "Hello World"
    title_case("  python is fun ")   -> "Python Is Fun"
    title_case("")                   -> ""
    """
    # TODO: split(), capitalise each word, join with " ".
    ...


def count_words(text: str) -> dict[str, int]:
    """Count how often each word appears. Ignore case and the punctuation . , ! ? ; :

    A word is a run of characters between spaces after the punctuation is removed.
    Return a dict from word to count.

    count_words("the cat and The dog.") -> {"the": 2, "cat": 1, "and": 1, "dog": 1}
    count_words("")                     -> {}
    """
    # TODO: lower(), remove punctuation (replace or a loop), split(), count in a dict.
    ...


if __name__ == "__main__":
    print(is_palindrome("A man, a plan, a canal: Panama"))
    print(title_case("hello   WORLD"))
    print(count_words("the cat and The dog."))
