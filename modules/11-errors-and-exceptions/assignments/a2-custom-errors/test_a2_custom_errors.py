import pytest

from practice import load

m = load(__file__)


def test_exception_hierarchy():
    assert issubclass(m.ValidationError, ValueError)
    with pytest.raises(ValueError):  # a ValidationError is also a ValueError
        m.validate_age("abc")
    assert issubclass(m.ConfigError, Exception)
    assert issubclass(m.InsufficientFunds, Exception)


def test_insufficient_funds_attributes():
    error = m.InsufficientFunds(balance=30, amount=50)
    assert error.balance == 30
    assert error.amount == 50
    assert str(error) == "need 50, have 30"


@pytest.mark.parametrize(("value", "expected"), [("42", 42), (0, 0), (150, 150), (" 7 ", 7)])
def test_validate_age_ok(value, expected):
    assert m.validate_age(value) == expected


@pytest.mark.parametrize("value", ["abc", None, "4.5", ""])
def test_validate_age_not_a_number(value):
    with pytest.raises(m.ValidationError, match="whole number"):
        m.validate_age(value)


@pytest.mark.parametrize("value", [-1, 151, "200"])
def test_validate_age_out_of_range(value):
    with pytest.raises(m.ValidationError, match="between 0 and 150"):
        m.validate_age(value)


def test_validate_age_chains_the_original_error():
    with pytest.raises(m.ValidationError) as info:
        m.validate_age("abc")
    assert isinstance(info.value.__cause__, ValueError)


def test_validate_username():
    assert m.validate_username("ada99") == "ada99"
    assert m.validate_username("abc") == "abc"


@pytest.mark.parametrize("name", ["ab", "", "a" * 13])
def test_validate_username_length(name):
    with pytest.raises(m.ValidationError, match="3 to 12"):
        m.validate_username(name)


@pytest.mark.parametrize("name", ["ada lovelace", "ada!", "a_b_c"])
def test_validate_username_characters(name):
    with pytest.raises(m.ValidationError, match="letters and digits"):
        m.validate_username(name)


def test_withdraw():
    assert m.withdraw(100, 30) == 70
    assert m.withdraw(100, 100) == 0


def test_withdraw_too_much():
    with pytest.raises(m.InsufficientFunds) as info:
        m.withdraw(30, 50)
    assert info.value.balance == 30
    assert info.value.amount == 50


@pytest.mark.parametrize("amount", [0, -5])
def test_withdraw_needs_positive_amount(amount):
    with pytest.raises(ValueError, match="amount must be positive"):
        m.withdraw(100, amount)


def test_parse_port():
    assert m.parse_port("8080") == 8080
    assert m.parse_port("1") == 1
    assert m.parse_port("65535") == 65535


def test_parse_port_not_a_number_is_chained():
    with pytest.raises(m.ConfigError) as info:
        m.parse_port("abc")
    assert str(info.value) == "bad port: 'abc'"
    assert isinstance(info.value.__cause__, ValueError)


@pytest.mark.parametrize("text", ["0", "70000", "-1"])
def test_parse_port_out_of_range(text):
    with pytest.raises(m.ConfigError, match="out of range"):
        m.parse_port(text)
