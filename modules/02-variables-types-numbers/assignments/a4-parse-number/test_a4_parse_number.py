import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("42", 42),
        (" 3.5 ", 3.5),
        ("1_000", 1000),
        ("-7", -7),
        ("0.5", 0.5),
        ("1e3", 1000.0),
    ],
)
def test_parse_number_ok(text, expected):
    result = m.parse_number(text)
    assert result == expected
    assert type(result) is type(expected)


@pytest.mark.parametrize("text", ["abc", "", "  ", "1,5", "nan", "inf", "-inf", "12abc"])
def test_parse_number_bad(text):
    assert m.parse_number("7") == 7  # the function must work at all
    assert m.parse_number(text) is None


def test_bmi():
    assert m.bmi(70, 1.75) == 22.9
    assert m.bmi(95, 1.70) == 32.9


@pytest.mark.parametrize(("w", "h"), [(0, 1.7), (70, 0), (-1, 1.7), (70, -1.7)])
def test_bmi_invalid(w, h):
    with pytest.raises(ValueError):
        m.bmi(w, h)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (10, "underweight"),
        (18.4, "underweight"),
        (18.5, "normal"),
        (24.9, "normal"),
        (25, "overweight"),
        (29.9, "overweight"),
        (30, "obese"),
        (45, "obese"),
    ],
)
def test_bmi_category(value, expected):
    assert m.bmi_category(value) == expected


@pytest.mark.parametrize(
    ("weight", "height", "expected"),
    [
        ("70", "1.75", "BMI 22.9 (normal)"),
        ("95", "1.70", "BMI 32.9 (obese)"),
        ("abc", "1.70", "invalid weight"),
        ("70", "tall", "invalid height"),
        ("70", "0", "invalid height"),
        ("-5", "1.70", "invalid weight"),
        ("abc", "tall", "invalid weight"),
    ],
)
def test_describe(weight, height, expected):
    assert m.describe(weight, height) == expected
