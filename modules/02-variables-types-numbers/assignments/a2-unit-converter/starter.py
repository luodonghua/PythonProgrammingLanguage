"""Assignment 2: A small unit converter.

Practise float arithmetic, rounding and type conversion.
"""


def c_to_f(celsius: float) -> float:
    """Convert degrees Celsius to Fahrenheit: F = C * 9 / 5 + 32.

    c_to_f(100) -> 212.0
    c_to_f(-40) -> -40.0
    """
    # TODO: return the converted value.
    ...


def f_to_c(fahrenheit: float) -> float:
    """Convert degrees Fahrenheit to Celsius: C = (F - 32) * 5 / 9.

    f_to_c(212) -> 100.0
    f_to_c(32)  -> 0.0
    """
    # TODO
    ...


def km_to_miles(km: float, digits: int = 2) -> float:
    """Convert kilometres to miles (1 mile = 1.609344 km), rounded to `digits` places.

    km_to_miles(10)     -> 6.21
    km_to_miles(42.195) -> 26.22
    km_to_miles(10, 4)  -> 6.2137
    """
    # TODO: divide by 1.609344, then round(..., digits).
    ...


def convert_text(text: str) -> str:
    """Convert a text like "100 C" or "212 F" to the other scale.

    The number may be an int or a float. The unit is "C" or "F" (any case,
    spaces around are fine). Return the result rounded to 1 decimal with the
    new unit.

    convert_text("100 C")   -> "212.0 F"
    convert_text(" 98.6 f") -> "37.0 C"
    convert_text("0 c")     -> "32.0 F"

    Raise ValueError for an unknown unit or text that is not "<number> <unit>".
    """
    # TODO: split the text, convert the number with float(), pick the function.
    ...


if __name__ == "__main__":
    print(c_to_f(100), f_to_c(212), km_to_miles(10))
    print(convert_text("37 C"))
