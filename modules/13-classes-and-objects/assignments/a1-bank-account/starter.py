"""Assignment 1: A bank account that protects its balance."""


class BankAccount:
    """A simple account.

    BankAccount(owner, balance=0)
        * owner must be a non-empty string (after strip), else ValueError.
        * balance must not be negative, else ValueError.
    .owner    the owner name, stripped of outer spaces.
    .balance  read-only property (assigning to it raises AttributeError).
    .deposit(amount)   add amount and return the new balance.
                       amount must be greater than 0, else ValueError.
    .withdraw(amount)  subtract amount and return the new balance.
                       amount must be greater than 0, else ValueError.
                       Withdrawing more than the balance raises ValueError
                       and leaves the balance unchanged.
    repr(account) looks like:  BankAccount('Ada', 100)
    """

    def __init__(self, owner, balance=0):
        # TODO: validate and store owner and balance (keep the balance in self._balance).
        ...

    # TODO: add a read-only `balance` property.

    def deposit(self, amount):
        # TODO
        ...

    def withdraw(self, amount):
        # TODO
        ...

    def __repr__(self):
        # TODO
        ...


if __name__ == "__main__":
    acct = BankAccount("Ada", 100)
    acct.deposit(50)
    acct.withdraw(30)
    print(acct, acct.balance)
