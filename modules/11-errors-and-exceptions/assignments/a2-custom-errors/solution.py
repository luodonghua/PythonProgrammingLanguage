"""Assignment 2: Raise and define your own exceptions.

Practises `raise`, custom exception classes, extra data on an exception and
chaining with `raise ... from ...`.
"""


class ValidationError(ValueError):
    """Raised when a value is not acceptable. Subclass of ValueError."""


class ConfigError(Exception):
    """Raised for a bad configuration value."""


class InsufficientFunds(Exception):
    """Raised when a withdrawal is larger than the balance.

    Must store the numbers as attributes `balance` and `amount`,
    and its message (str(error)) must read "need <amount>, have <balance>".

    InsufficientFunds(balance=30, amount=50)  ->  str() == "need 50, have 30"
    """

    def __init__(self, balance, amount):
        super().__init__(f"need {amount}, have {balance}")
        self.balance = balance
        self.amount = amount


def validate_age(value) -> int:
    """Return `value` as an int if it is a whole number from 0 to 150.

    Accept ints and numeric strings like "42".
    Raise ValidationError for everything else, with these messages:
      not a whole number ("abc", None, 4.5 as a string...)  -> "age must be a whole number"
      below 0 or above 150                                  -> "age must be between 0 and 150"

    validate_age("42")  -> 42
    validate_age(200)   -> raises ValidationError("age must be between 0 and 150")
    """
    try:
        age = int(value)
    except (ValueError, TypeError) as exc:
        raise ValidationError("age must be a whole number") from exc
    if not 0 <= age <= 150:
        raise ValidationError("age must be between 0 and 150")
    return age


def validate_username(name: str) -> str:
    """Return the name if it has 3 to 12 characters and only letters and digits.
    Otherwise raise ValidationError with one of these messages:
      wrong length   -> "username must have 3 to 12 characters"
      other chars    -> "username may only contain letters and digits"
    Check the length first.

    validate_username("ada99")  -> "ada99"
    """
    if not 3 <= len(name) <= 12:
        raise ValidationError("username must have 3 to 12 characters")
    if not name.isalnum():
        raise ValidationError("username may only contain letters and digits")
    return name


def withdraw(balance: float, amount: float) -> float:
    """Return the new balance after taking out `amount`.

    Raise ValueError("amount must be positive") if amount <= 0.
    Raise InsufficientFunds(balance, amount) if amount > balance.

    withdraw(100, 30)  -> 70
    """
    if amount <= 0:
        raise ValueError("amount must be positive")
    if amount > balance:
        raise InsufficientFunds(balance, amount)
    return balance - amount


def parse_port(text: str) -> int:
    """Return the port number in `text` (an int from 1 to 65535).

    Raise ConfigError for a bad value:
      not a number   -> ConfigError("bad port: 'abc'")   (use {text!r}), and
                        chain the original ValueError: `raise ... from exc`
      out of range   -> ConfigError("port out of range: 70000")

    parse_port("8080")  -> 8080
    """
    try:
        port = int(text)
    except ValueError as exc:
        raise ConfigError(f"bad port: {text!r}") from exc
    if not 1 <= port <= 65535:
        raise ConfigError(f"port out of range: {port}")
    return port


if __name__ == "__main__":
    try:
        withdraw(30, 50)
    except InsufficientFunds as error:
        print(error, error.balance, error.amount)
