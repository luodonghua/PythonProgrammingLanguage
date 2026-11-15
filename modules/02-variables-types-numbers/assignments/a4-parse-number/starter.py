"""Assignment 4: Safe numeric parsing and a BMI classifier.

Real input is messy. These functions turn text into numbers without crashing.
"""


def parse_number(text: str) -> int | float | None:
    """Convert text to a number, or return None if it is not one.

    Return an int when the text is a whole number, otherwise a float.
    Spaces around the text and underscores like "1_000" are accepted.
    Reject "nan" and "inf" (return None).

    parse_number("42")      -> 42
    parse_number(" 3.5 ")   -> 3.5
    parse_number("1_000")   -> 1000
    parse_number("-7")      -> -7
    parse_number("abc")     -> None
    parse_number("")        -> None
    parse_number("nan")     -> None
    """
    # TODO: try int(text), then float(text), catching ValueError.
    # Check math.isfinite() for the float case.
    ...


def bmi(weight_kg: float, height_m: float) -> float:
    """Return the body mass index: weight / height ** 2, rounded to 1 decimal.

    bmi(70, 1.75) -> 22.9

    Raise ValueError if weight or height is not positive.
    """
    # TODO
    ...


def bmi_category(value: float) -> str:
    """Classify a BMI value.

    below 18.5          -> "underweight"
    18.5 up to below 25 -> "normal"
    25 up to below 30   -> "overweight"
    30 and above        -> "obese"
    """
    # TODO: use if / elif / else.
    ...


def describe(weight_text: str, height_text: str) -> str:
    """Parse two texts and describe the result.

    describe("70", "1.75")  -> "BMI 22.9 (normal)"
    describe("95", "1.70")  -> "BMI 32.9 (obese)"
    describe("abc", "1.70") -> "invalid weight"
    describe("70", "tall")  -> "invalid height"
    describe("70", "0")     -> "invalid height"
    describe("-5", "1.70")  -> "invalid weight"

    Check the weight first, then the height.
    """
    # TODO: use parse_number and bmi; a non-positive number is invalid too.
    ...


if __name__ == "__main__":
    print(parse_number(" 12 "), parse_number("x"))
    print(describe("70", "1.75"))
