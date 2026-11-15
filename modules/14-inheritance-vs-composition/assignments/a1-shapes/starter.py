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
    def area(self):
        ...

    @abstractmethod
    def perimeter(self):
        ...

    def describe(self):
        # TODO: build the text from type(self).__name__, self.area(), self.perimeter().
        ...


class Rectangle(Shape):
    """Rectangle(width, height). Negative or zero sides raise ValueError."""

    def __init__(self, width, height):
        # TODO: validate and store width and height.
        ...

    # TODO: implement area() and perimeter().


class Square(Rectangle):
    """Square(side). A square is a rectangle with equal sides (reuse Rectangle)."""

    def __init__(self, side):
        # TODO: call super().__init__ with the right arguments.
        ...


class Circle(Shape):
    """Circle(radius). Radius must be positive, else ValueError. Use math.pi."""

    def __init__(self, radius):
        # TODO
        ...

    # TODO: implement area() and perimeter().


def total_area(shapes):
    """Return the sum of area() over an iterable of shapes (0 for an empty one)."""
    # TODO
    ...


def largest(shapes):
    """Return the shape with the biggest area. Raise ValueError for no shapes."""
    # TODO
    ...


if __name__ == "__main__":
    items = [Rectangle(2, 3), Square(2), Circle(1)]
    for item in items:
        print(item.describe())
    print(round(total_area(items), 2), type(largest(items)).__name__)
