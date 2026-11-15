"""Assignment 1: A shape hierarchy with an abstract base class."""

import math
from abc import ABC, abstractmethod


class Shape(ABC):
    """Abstract base class. Shape() itself cannot be created.

    Subclasses must implement:
        area()       -> float
        perimeter()  -> float
    Shape provides:
        describe()   -> "<ClassName>: area=<area:.2f> perimeter=<perimeter:.2f>"
                        e.g. "Square: area=4.00 perimeter=8.00"
    """

    @abstractmethod
    def area(self) -> float:
        ...

    @abstractmethod
    def perimeter(self) -> float:
        ...

    def describe(self) -> str:
        return f"{type(self).__name__}: area={self.area():.2f} perimeter={self.perimeter():.2f}"


class Rectangle(Shape):
    """Rectangle(width, height). Negative or zero sides raise ValueError."""

    def __init__(self, width: float, height: float) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("sides must be positive")
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Square(Rectangle):
    """Square(side). A square is a rectangle with equal sides (reuse Rectangle)."""

    def __init__(self, side: float) -> None:
        super().__init__(side, side)


class Circle(Shape):
    """Circle(radius). Radius must be positive, else ValueError. Use math.pi."""

    def __init__(self, radius: float) -> None:
        if radius <= 0:
            raise ValueError("radius must be positive")
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius**2

    def perimeter(self) -> float:
        return 2 * math.pi * self.radius


def total_area(shapes) -> float:
    """Return the sum of area() over an iterable of shapes (0 for an empty one)."""
    return sum(shape.area() for shape in shapes)


def largest(shapes):
    """Return the shape with the biggest area. Raise ValueError for no shapes."""
    shapes = list(shapes)
    if not shapes:
        raise ValueError("no shapes")
    return max(shapes, key=lambda shape: shape.area())


if __name__ == "__main__":
    items = [Rectangle(2, 3), Square(2), Circle(1)]
    for item in items:
        print(item.describe())
    print(round(total_area(items), 2), type(largest(items)).__name__)
