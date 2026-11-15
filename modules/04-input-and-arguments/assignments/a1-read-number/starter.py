"""Assignment 1: Reading numbers safely.

Both functions take the input function as a parameter (default: the real
input). Tests pass a fake one that returns scripted answers.
"""


def read_int(
    prompt: str,
    input_fn=input,
    minimum: int | None = None,
    maximum: int | None = None,
    max_tries: int | None = None,
) -> int | None:
    """Ask until the user types a whole number inside the allowed range.

    * Call input_fn(prompt) for every attempt (the same prompt each time).
    * Spaces around the number are fine ("  5 " is 5).
    * If the text is not a whole number, or it is below `minimum` or above
      `maximum` (when those are not None), print "Invalid input." and ask again.
    * If max_tries is not None and that many attempts all failed, return None.
      With max_tries=None, ask forever.

    Scripted answers ["x", "50", "7"] with minimum=1, maximum=10 -> 7
    (prints "Invalid input." twice)
    """
    # TODO: a while loop, try/except ValueError, range checks, a tries counter.
    ...


def read_yes_no(prompt: str, input_fn=input) -> bool:
    """Ask until the user answers yes or no. Return True for yes.

    Accept "y", "yes", "n", "no" in any case, with spaces around.
    For any other text print "Please answer y or n." and ask again.

    "Y" -> True    " no " -> False    ["maybe", "y"] -> True
    """
    # TODO
    ...


if __name__ == "__main__":
    age = read_int("Age (0-120): ", minimum=0, maximum=120, max_tries=3)
    print("You typed:", age)
    print("Sure?", read_yes_no("Continue? (y/n) "))
