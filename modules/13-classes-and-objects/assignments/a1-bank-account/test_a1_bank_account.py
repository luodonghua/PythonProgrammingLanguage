import pytest

from practice import load

m = load(__file__)


def test_create_and_balance():
    acct = m.BankAccount("Ada", 100)
    assert acct.owner == "Ada"
    assert acct.balance == 100


def test_default_balance_and_stripped_owner():
    acct = m.BankAccount("  Bob  ")
    assert acct.owner == "Bob"
    assert acct.balance == 0


@pytest.mark.parametrize("owner", ["", "   "])
def test_empty_owner_rejected(owner):
    with pytest.raises(ValueError):
        m.BankAccount(owner)


def test_negative_opening_balance_rejected():
    with pytest.raises(ValueError):
        m.BankAccount("Ada", -1)


def test_deposit_returns_new_balance():
    acct = m.BankAccount("Ada", 10)
    assert acct.deposit(5) == 15
    assert acct.balance == 15


def test_withdraw_returns_new_balance():
    acct = m.BankAccount("Ada", 10)
    assert acct.withdraw(4) == 6
    assert acct.balance == 6


def test_withdraw_everything_is_allowed():
    acct = m.BankAccount("Ada", 10)
    assert acct.withdraw(10) == 0


@pytest.mark.parametrize("amount", [0, -5])
def test_non_positive_amounts_rejected(amount):
    acct = m.BankAccount("Ada", 10)
    with pytest.raises(ValueError):
        acct.deposit(amount)
    with pytest.raises(ValueError):
        acct.withdraw(amount)
    assert acct.balance == 10


def test_overdraft_rejected_and_balance_unchanged():
    acct = m.BankAccount("Ada", 10)
    with pytest.raises(ValueError):
        acct.withdraw(11)
    assert acct.balance == 10


def test_balance_is_read_only():
    acct = m.BankAccount("Ada", 10)
    with pytest.raises(AttributeError):
        acct.balance = 1000


def test_repr():
    assert repr(m.BankAccount("Ada", 100)) == "BankAccount('Ada', 100)"
