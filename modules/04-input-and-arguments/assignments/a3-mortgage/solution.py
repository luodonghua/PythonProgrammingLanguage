"""Assignment 3: A mortgage payment calculator (command line).

    python solution.py 200000 6 30
    Monthly payment: 1,199.10
    Total paid: 431,676.00
"""

import argparse
import sys


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
    if principal <= 0:
        raise ValueError("principal must be positive")
    if annual_rate < 0:
        raise ValueError("rate must not be negative")
    if years < 1:
        raise ValueError("years must be at least 1")
    payments = years * 12
    if annual_rate == 0:
        return round(principal / payments, 2)
    rate = annual_rate / 100 / 12
    return round(principal * rate / (1 - (1 + rate) ** -payments), 2)


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
    parser = argparse.ArgumentParser(description="Monthly loan payment.")
    parser.add_argument("principal", type=float, help="amount borrowed")
    parser.add_argument("rate", type=float, help="yearly interest rate in percent")
    parser.add_argument("years", type=int, help="loan length in years")
    args = parser.parse_args(argv)
    try:
        payment = monthly_payment(args.principal, args.rate, args.years)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    total = payment * args.years * 12
    print(f"Monthly payment: {payment:,.2f}")
    print(f"Total paid: {total:,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
