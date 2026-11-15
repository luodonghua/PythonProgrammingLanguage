"""Assignment 2: FizzBuzz."""


def fizzbuzz(n: int) -> str:
    """Return the FizzBuzz word for n.

    - multiple of 3 and 5 -> "FizzBuzz"
    - multiple of 3       -> "Fizz"
    - multiple of 5       -> "Buzz"
    - anything else       -> the number as text, e.g. "7"

    Hint: check the "both" case first. Use the % operator.
    """
    # TODO
    ...


def fizzbuzz_up_to(n: int) -> list[str]:
    """Return fizzbuzz(1) ... fizzbuzz(n) as a list. (A for loop is fine.)"""
    # TODO
    ...


if __name__ == "__main__":
    print("\n".join(fizzbuzz_up_to(15)))
