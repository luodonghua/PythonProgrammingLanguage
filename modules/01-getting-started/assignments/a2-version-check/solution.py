"""Assignment 2: Check your Python version."""

import sys

MINIMUM = (3, 14)  # this course needs Python 3.14 or later


def version_string() -> str:
    """Return the running Python version like 'Python 3.14.0'.

    Hint: sys.version_info has the attributes major, minor and micro.
    """
    v = sys.version_info
    return f"Python {v.major}.{v.minor}.{v.micro}"


def is_supported(version_info=sys.version_info) -> bool:
    """Return True if (major, minor) is at least MINIMUM.

    version_info can be sys.version_info or a plain tuple such as (3, 13, 2).
    Hint: tuples compare element by element, so (3, 15) >= (3, 14) is True.
    """
    return tuple(version_info[:2]) >= MINIMUM


if __name__ == "__main__":
    print(version_string())
    print("supported" if is_supported() else "please upgrade with: uv python install 3.14")
