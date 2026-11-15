"""Assignment 2: Make URL slugs.

A slug is the readable part of a web address: "Hello, World!" becomes "hello-world".
"""


def slugify(title: str) -> str:
    """Turn a title into a slug.

    Rules:
    * lower case
    * letters a-z and digits are kept
    * every run of any other characters becomes ONE hyphen
    * no hyphen at the start or the end

    slugify("Hello, World!")          -> "hello-world"
    slugify("  Python   3.14 -- new") -> "python-3-14-new"
    slugify("---")                    -> ""
    slugify("C++ & Rust")             -> "c-rust"
    """
    # TODO: loop over the characters. Build the result in a list and add a hyphen
    # only when the previous character was not a hyphen. Then strip("-").
    ...


def unique_slug(title: str, taken: set[str]) -> str:
    """Return a slug that is not in `taken`, adding -2, -3, ... when needed.

    unique_slug("Hello", set())                    -> "hello"
    unique_slug("Hello", {"hello"})                -> "hello-2"
    unique_slug("Hello", {"hello", "hello-2"})     -> "hello-3"

    Do not change `taken`.
    """
    # TODO: use slugify, then a while loop with a counter.
    ...


def truncate(text: str, width: int, suffix: str = "...") -> str:
    """Shorten text to at most `width` characters, ending with `suffix` if cut.

    Text that already fits is returned unchanged.

    truncate("Hello, World", 20) -> "Hello, World"
    truncate("Hello, World", 8)  -> "Hello..."
    truncate("Hello", 5)         -> "Hello"

    Raise ValueError if width is smaller than the length of suffix.
    """
    # TODO: slice with text[: width - len(suffix)].
    ...


if __name__ == "__main__":
    print(slugify("Hello, World!"))
    print(unique_slug("Hello", {"hello"}))
    print(truncate("Hello, World", 8))
