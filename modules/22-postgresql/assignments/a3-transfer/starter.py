"""Assignment 3: Move money between accounts in one transaction.

The tests create this table and fill it:

    accounts(id INTEGER PRIMARY KEY, owner TEXT NOT NULL,
             balance NUMERIC(12, 2) NOT NULL CHECK (balance >= 0))

Every function takes an open psycopg connection first. A transfer must be
all-or-nothing: if anything goes wrong, no balance may change.
"""

from decimal import Decimal

import psycopg


class InsufficientFunds(Exception):
    """Raised when the source account holds less than the amount to move."""


def get_balance(conn: psycopg.Connection, account_id: int) -> Decimal:
    """Return the balance of an account. Raise LookupError if it does not exist."""
    # TODO: SELECT balance FROM accounts WHERE id = %s
    ...


def transfer(conn: psycopg.Connection, from_id: int, to_id: int, amount: Decimal) -> None:
    """Move `amount` from one account to another.

    Rules, in this order:
    1. amount <= 0, or from_id == to_id           -> ValueError (no database work)
    2. the source account does not exist          -> LookupError
    3. the source balance is smaller than amount  -> InsufficientFunds
    4. withdraw from the source, then deposit into the target; if the target
       does not exist                             -> LookupError, and the
       withdrawal must be undone

    Do the whole job inside `with conn.transaction():` so an exception rolls
    everything back. Lock the source row with SELECT ... FOR UPDATE so that two
    transfers cannot both spend the same money.
    """
    # TODO: lock and read the source, check the rules, run two UPDATE statements.
    ...


def transfer_many(
    conn: psycopg.Connection, moves: list[tuple[int, int, Decimal]]
) -> int:
    """Run several (from_id, to_id, amount) transfers as ONE transaction and
    return how many were done. If any of them fails, none of them happens and
    the exception propagates.
    """
    # TODO: one `with conn.transaction():` around a loop that calls transfer().
    # A nested conn.transaction() inside transfer() becomes a savepoint, which is fine.
    ...


if __name__ == "__main__":
    print("Run the tests: uv run pytest modules/22-postgresql/assignments/a3-transfer")
