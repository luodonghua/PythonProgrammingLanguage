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
    row = conn.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,)).fetchone()
    if row is None:
        raise LookupError(f"no account {account_id}")
    return row[0]


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
    if amount <= 0:
        raise ValueError("amount must be positive")
    if from_id == to_id:
        raise ValueError("cannot transfer to the same account")
    with conn.transaction():
        row = conn.execute(
            "SELECT balance FROM accounts WHERE id = %s FOR UPDATE", (from_id,)
        ).fetchone()
        if row is None:
            raise LookupError(f"no account {from_id}")
        if row[0] < amount:
            raise InsufficientFunds(f"account {from_id} has {row[0]}, needs {amount}")
        conn.execute(
            "UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, from_id)
        )
        deposited = conn.execute(
            "UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, to_id)
        )
        if deposited.rowcount == 0:
            raise LookupError(f"no account {to_id}")


def transfer_many(
    conn: psycopg.Connection, moves: list[tuple[int, int, Decimal]]
) -> int:
    """Run several (from_id, to_id, amount) transfers as ONE transaction and
    return how many were done. If any of them fails, none of them happens and
    the exception propagates.
    """
    with conn.transaction():
        for from_id, to_id, amount in moves:
            transfer(conn, from_id, to_id, amount)
    return len(moves)


if __name__ == "__main__":
    print("Run the tests: uv run pytest modules/22-postgresql/assignments/a3-transfer")
