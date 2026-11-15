"""Assignment 3: Bill splitter with exact money arithmetic.

Floats are not exact, so use decimal.Decimal for money. Always build a Decimal
from a string (or an int), never from a float.
"""

from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


def to_money(value: str | int | Decimal) -> Decimal:
    """Return value as a Decimal rounded to cents, rounding halves up.

    to_money("2.675") -> Decimal("2.68")
    to_money("10")    -> Decimal("10.00")
    to_money(3)       -> Decimal("3.00")
    """
    return Decimal(value).quantize(CENT, rounding=ROUND_HALF_UP)


def add_tip(bill: str, tip_percent: str) -> Decimal:
    """Return bill plus a tip, rounded to cents (halves up).

    add_tip("80.00", "15")   -> Decimal("92.00")
    add_tip("19.99", "10")   -> Decimal("21.99")
    add_tip("50", "0")       -> Decimal("50.00")
    """
    total = Decimal(bill) * (1 + Decimal(tip_percent) / 100)
    return to_money(total)


def split_bill(total: str, people: int) -> list[Decimal]:
    """Split a total into `people` shares that add up to the total exactly.

    Every share is rounded down to cents. The leftover cents are added, one
    cent each, to the first shares.

    split_bill("100.00", 3) -> [Decimal("33.34"), Decimal("33.33"), Decimal("33.33")]
    split_bill("10.00", 4)  -> [Decimal("2.50")] * 4
    split_bill("0.02", 3)   -> [Decimal("0.01"), Decimal("0.01"), Decimal("0.00")]

    Raise ValueError if people is less than 1.
    """
    if people < 1:
        raise ValueError("people must be at least 1")
    cents = int(to_money(total) * 100)
    base, extra = divmod(cents, people)
    return [to_money(Decimal(base + (i < extra)) / 100) for i in range(people)]


if __name__ == "__main__":
    print(add_tip("80.00", "15"))
    print(split_bill("100.00", 3))
