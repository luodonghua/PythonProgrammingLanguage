"""Assignment 1: Seconds to a clock string.

Use divmod to split a number of seconds into days, hours, minutes and seconds.
"""


def split_seconds(total: int) -> tuple[int, int, int, int]:
    """Return (days, hours, minutes, seconds) for a non-negative number of seconds.

    split_seconds(0)      -> (0, 0, 0, 0)
    split_seconds(3725)   -> (0, 1, 2, 5)
    split_seconds(90061)  -> (1, 1, 1, 1)

    Raise ValueError if total is negative.
    """
    # TODO: use divmod twice or three times.
    ...


def clock(total: int) -> str:
    """Format seconds as "H:MM:SS". Hours may be more than 24 and have no padding.

    clock(5)      -> "0:00:05"
    clock(3725)   -> "1:02:05"
    clock(90061)  -> "25:01:01"

    Raise ValueError if total is negative.
    """
    # TODO: use divmod, then an f-string with :02d for minutes and seconds.
    ...


if __name__ == "__main__":
    print(split_seconds(90061))
    print(clock(3725))
