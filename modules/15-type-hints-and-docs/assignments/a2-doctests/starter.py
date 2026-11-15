"""Assignment 2: Document functions with doctest examples.

The functions work already. Add `>>>` examples to each docstring:

    * at least 3 examples for every function, each one calling that function;
    * `safe_div` must also have one example that shows the ValueError;
    * every example must give the real output (the tests run them with doctest).

Run your examples yourself with:  python -m doctest -v starter.py
Example of the format:

    >>> double(4)
    8
"""


def double(n: int) -> int:
    """Return n multiplied by 2."""
    # TODO: add at least 3 doctest examples to the docstring above.
    return n * 2


def slugify(text: str) -> str:
    """Return text in lower case with words joined by single hyphens.

    Leading, trailing and repeated spaces are ignored.
    """
    # TODO: add at least 3 doctest examples to the docstring above.
    return "-".join(text.lower().split())


def safe_div(a: float, b: float) -> float:
    """Return a / b. Raise ValueError("cannot divide by zero") when b is 0."""
    # TODO: add at least 3 doctest examples, one of them showing the ValueError.
    # An exception example looks like this:
    #     >>> safe_div(1, 0)
    #     Traceback (most recent call last):
    #         ...
    #     ValueError: cannot divide by zero
    if b == 0:
        raise ValueError("cannot divide by zero")
    return a / b


if __name__ == "__main__":
    import doctest

    print(doctest.testmod())
