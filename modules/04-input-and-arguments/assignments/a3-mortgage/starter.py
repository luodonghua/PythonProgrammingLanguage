"""Assignment 3: A mortgage payment calculator (command line).

    python starter.py 200000 6 30
    Monthly payment: 1,199.10
    Total paid: 431,676.00
"""

import argparse  # noqa: F401  (you will need it)
import sys  # noqa: F401


def monthly_payment(principal: float, annual_rate: float, years: int) -> float:
    """Return the fixed monthly payment of a loan, rounded to 2 decimals.

    principal    the amount borrowed (greater than 0)
    annual_rate  the yearly interest rate in percent, for example 6 for 6 % (0 or more)
    years        the loan length in whole years (at least 1)

    With monthly rate r = annual_rate / 100 / 12 and n = years * 12 payments:

        payment = principal * r / (1 - (1 + r) ** -n)

    When the rate is 0 the formula divides by zero, so use principal / n.

    monthly_payment(200000, 6, 30)  -> 1199.1
    monthly_payment(120000, 0, 10)  -> 1000.0

    Raise ValueError for a principal that is not positive, a negative rate,
    or fewer than 1 year.
    """
    # TODO: validate the arguments, then apply the formula (rate 0 is a special case).
    ...


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point. Return the exit code.

    Arguments: principal (float), rate (float, percent), years (int).

    On success print two lines to stdout and return 0:

        Monthly payment: 1,199.10
        Total paid: 431,676.00

    Total paid is the monthly payment times the number of months, shown with
    a thousands separator and 2 decimals.

    If monthly_payment raises ValueError, print "error: <message>" to stderr,
    print nothing to stdout and return 1. A non-numeric argument makes
    argparse exit with code 2 by itself (use type=float and type=int).
    """
    # TODO: build an ArgumentParser with three arguments, parse argv, call
    # monthly_payment inside try/except ValueError, print the two lines.
    ...


if __name__ == "__main__":
    raise SystemExit(main())
