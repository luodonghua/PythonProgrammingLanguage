import pytest

from practice import load

m = load(__file__)


def test_c_to_f():
    assert m.c_to_f(100) == pytest.approx(212.0)
    assert m.c_to_f(-40) == pytest.approx(-40.0)
    assert m.c_to_f(37) == pytest.approx(98.6)


def test_f_to_c():
    assert m.f_to_c(212) == pytest.approx(100.0)
    assert m.f_to_c(32) == pytest.approx(0.0)
    assert m.f_to_c(-40) == pytest.approx(-40.0)


def test_km_to_miles():
    assert m.km_to_miles(10) == 6.21
    assert m.km_to_miles(42.195) == 26.22
    assert m.km_to_miles(10, 4) == 6.2137
    assert m.km_to_miles(0) == 0


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("100 C", "212.0 F"),
        (" 98.6 f", "37.0 C"),
        ("0 c", "32.0 F"),
        ("-40 F", "-40.0 C"),
    ],
)
def test_convert_text(text, expected):
    assert m.convert_text(text) == expected


@pytest.mark.parametrize("text", ["100 K", "hot C", "100", "", "1 2 C"])
def test_convert_text_errors(text):
    with pytest.raises(ValueError):
        m.convert_text(text)
