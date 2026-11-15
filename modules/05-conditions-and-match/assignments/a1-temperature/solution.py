"""Assignment 1: Describe the temperature."""


def classify(celsius: float) -> str:
    """Return a word for the temperature.

    celsius <= 0   -> "freezing"
    celsius < 10   -> "cold"
    celsius < 20   -> "mild"
    celsius < 30   -> "warm"
    otherwise      -> "hot"

    Use if / elif / else.
    """
    if celsius <= 0:
        return "freezing"
    elif celsius < 10:
        return "cold"
    elif celsius < 20:
        return "mild"
    elif celsius < 30:
        return "warm"
    else:
        return "hot"


if __name__ == "__main__":
    for t in (-5, 0, 7.5, 15, 25, 35):
        print(t, classify(t))
