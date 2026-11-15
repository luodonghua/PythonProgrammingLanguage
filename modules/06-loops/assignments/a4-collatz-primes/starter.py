"""Assignment 4: Collatz chains and the sieve of Eratosthenes.

Two classic loop problems. Both are easy to state and good practice for
while loops, nested loops and boolean lists.
"""


def collatz_steps(n: int) -> int:
    """Count the steps for n to reach 1 in the Collatz process.

    Repeat: if n is even, halve it (n // 2); otherwise replace it by 3 * n + 1.
    Count the steps until n is 1.

    collatz_steps(1)   -> 0
    collatz_steps(6)   -> 8      (6 3 10 5 16 8 4 2 1)
    collatz_steps(27)  -> 111

    Raise ValueError if n is less than 1.
    """
    # TODO: a while loop that runs until n == 1, with a step counter.
    ...


def longest_collatz(limit: int) -> int:
    """Return the start number below `limit` (from 1) with the most Collatz steps.

    If two numbers tie, return the smaller one.

    longest_collatz(10)  -> 9      (19 steps)
    longest_collatz(2)   -> 1

    Raise ValueError if limit is less than 2.
    """
    # TODO: loop over range(2, limit) and remember the best start so far.
    ...


def primes_up_to(n: int) -> list[int]:
    """Return all prime numbers from 2 up to and including n, using a sieve.

    The sieve: make a list `is_prime` of n + 1 booleans (all True except
    0 and 1). For each number p from 2 while p * p <= n, if p is still marked
    prime, mark p * p, p * p + p, ... as not prime. Collect the numbers that
    are left.

    primes_up_to(20) -> [2, 3, 5, 7, 11, 13, 17, 19]
    primes_up_to(2)  -> [2]
    primes_up_to(1)  -> []
    """
    # TODO: the sieve described above; enumerate(is_prime) helps at the end.
    ...


if __name__ == "__main__":
    print(collatz_steps(27))
    print(longest_collatz(1000))
    print(primes_up_to(50))
