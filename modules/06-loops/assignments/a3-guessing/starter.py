"""Assignment 3: The logic of a number-guessing game.

The functions do not ask the user. They get the guesses as a list, so the
game can be tested with scripted guesses.
"""


def judge(secret: int, guess: int) -> str:
    """Compare one guess with the secret number.

    judge(50, 30) -> "too low"
    judge(50, 80) -> "too high"
    judge(50, 50) -> "correct"
    """
    # TODO: compare with <, > and return one of the three strings.
    ...


def play(secret: int, guesses: list[int], max_tries: int = 7) -> tuple[bool, list[str]]:
    """Play the game with scripted guesses.

    Go through the guesses in order, but make at most `max_tries` guesses.
    Record judge(secret, guess) for each guess. Stop at the first "correct".

    Return (won, feedback) where `won` tells whether the secret was found and
    `feedback` is the list of judgements for the guesses that were used.

    play(7, [3, 9, 7, 1])     -> (True, ["too low", "too high", "correct"])
    play(7, [1, 2, 3], 2)     -> (False, ["too low", "too low"])
    play(7, [])               -> (False, [])
    """
    # TODO: loop over guesses[:max_tries]; stop at the first "correct".
    ...


def best_strategy(low: int, high: int, secret: int) -> int:
    """Count the guesses a binary-search player needs to find the secret.

    The player always guesses the middle of the remaining range
    (low + high) // 2, then narrows the range. low and high are inclusive
    and the secret is between them.

    best_strategy(1, 100, 50) -> 1
    best_strategy(1, 100, 1)  -> 6
    best_strategy(1, 10, 10)  -> 4
    """
    # TODO: while loop: guess the middle, then move low or high.
    ...


if __name__ == "__main__":
    print(play(7, [3, 9, 7, 1]))
    print(best_strategy(1, 100, 1))
