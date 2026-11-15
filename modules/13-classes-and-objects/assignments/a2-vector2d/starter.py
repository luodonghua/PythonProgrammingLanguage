"""Assignment 2: A 2D vector with operators."""

import math


class Vector2D:
    """An immutable-style 2D vector.

    Vector2D(x, y)       stores x and y as attributes.
    repr(v)              "Vector2D(1, 2)"  (use !r for the numbers)
    v1 == v2             True when both x and y are equal.
                         Comparing with a non-Vector2D gives False (return NotImplemented).
    v1 + v2, v1 - v2     return a new Vector2D.
    v * k and k * v      scalar multiplication (k is an int or float), new Vector2D.
    -v                   the vector with both signs flipped.
    abs(v)               the length, math.hypot(x, y).
    x, y = v             unpacking works (define __iter__ yielding x then y).
    bool(v)              False only for the zero vector.
    Operators with an unsupported type return NotImplemented (so Python raises TypeError).
    """

    def __init__(self, x, y):
        # TODO: store x and y.
        ...

    # TODO: add __repr__, __eq__, __add__, __sub__, __mul__, __rmul__,
    # __neg__, __abs__, __iter__ and __bool__.


if __name__ == "__main__":
    a, b = Vector2D(3, 4), Vector2D(1, 2)
    print(a + b, a - b, 2 * a, abs(a))
