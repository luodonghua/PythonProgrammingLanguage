import math

import pytest

from practice import load

m = load(__file__)


def test_shape_is_abstract():
    assert m.Circle(1).area() > 0  # concrete shapes work
    with pytest.raises(TypeError):
        m.Shape()


def test_incomplete_subclass_cannot_be_created():
    class Half(m.Shape):
        def area(self):
            return 1

    assert m.Square(1).perimeter() == 4  # complete subclasses work
    with pytest.raises(TypeError):
        Half()


def test_rectangle():
    r = m.Rectangle(2, 3)
    assert r.area() == 6
    assert r.perimeter() == 10
    assert isinstance(r, m.Shape)


def test_square_reuses_rectangle():
    s = m.Square(2)
    assert isinstance(s, m.Rectangle)
    assert s.area() == 4
    assert s.perimeter() == 8
    assert (s.width, s.height) == (2, 2)


def test_circle():
    c = m.Circle(1)
    assert c.area() == pytest.approx(math.pi)
    assert c.perimeter() == pytest.approx(2 * math.pi)


@pytest.mark.parametrize("make", [
    lambda: m.Rectangle(0, 1),
    lambda: m.Rectangle(1, -1),
    lambda: m.Square(0),
    lambda: m.Circle(-2),
])
def test_invalid_sizes(make):
    with pytest.raises(ValueError):
        make()


def test_describe():
    assert m.Square(2).describe() == "Square: area=4.00 perimeter=8.00"
    assert m.Circle(1).describe() == "Circle: area=3.14 perimeter=6.28"


def test_total_area():
    shapes = [m.Rectangle(2, 3), m.Square(2)]
    assert m.total_area(shapes) == 10
    assert m.total_area([]) == 0
    assert m.total_area(iter(shapes)) == 10


def test_largest():
    big = m.Rectangle(10, 10)
    assert m.largest([m.Circle(1), big, m.Square(3)]) is big


def test_largest_empty():
    with pytest.raises(ValueError):
        m.largest([])
