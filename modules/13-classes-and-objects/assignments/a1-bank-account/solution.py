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

    def __init__(self, owner: str, balance: float = 0) -> None:
        owner = owner.strip()
        if not owner:
            raise ValueError("owner must not be empty")
        if balance < 0:
            raise ValueError("balance must not be negative")
        self.owner = owner
        self._balance = balance

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self._balance += amount
        return self._balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("withdrawal must be positive")
        if amount > self._balance:
            raise ValueError("insufficient funds")
        self._balance -= amount
        return self._balance

    def __repr__(self) -> str:
        return f"BankAccount({self.owner!r}, {self._balance!r})"


if __name__ == "__main__":
    acct = BankAccount("Ada", 100)
    acct.deposit(50)
    acct.withdraw(30)
    print(acct, acct.balance)
