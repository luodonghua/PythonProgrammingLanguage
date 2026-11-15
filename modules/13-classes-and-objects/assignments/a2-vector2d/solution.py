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

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vector2D({self.x!r}, {self.y!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector2D):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __add__(self, other: "Vector2D") -> "Vector2D":
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2D") -> "Vector2D":
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, k: float) -> "Vector2D":
        if not isinstance(k, (int, float)):
            return NotImplemented
        return Vector2D(self.x * k, self.y * k)

    __rmul__ = __mul__

    def __neg__(self) -> "Vector2D":
        return Vector2D(-self.x, -self.y)

    def __abs__(self) -> float:
        return math.hypot(self.x, self.y)

    def __iter__(self):
        yield self.x
        yield self.y

    def __bool__(self) -> bool:
        return self.x != 0 or self.y != 0


if __name__ == "__main__":
    a, b = Vector2D(3, 4), Vector2D(1, 2)
    print(a + b, a - b, 2 * a, abs(a))
