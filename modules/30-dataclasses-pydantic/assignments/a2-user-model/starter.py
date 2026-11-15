"""Assignment 2: a validated Pydantic model.

``User`` is a ``pydantic.BaseModel`` with these fields:

* ``name: str``       1 to 50 characters after stripping spaces; stored
                      stripped (use a ``field_validator`` in mode "before" or
                      ``Field(min_length=..)`` plus ``str_strip_whitespace``).
* ``age: int``        0 to 150 (Pydantic converts ``"36"`` to ``36``).
* ``email: str``      must contain exactly one ``"@"`` with text on both sides;
                      stored lower-case. Otherwise it is invalid.
* ``tags: list[str]`` default: empty list.

``parse_user(data)`` returns ``User.model_validate(data)``.

``problems(exc)`` takes a ``ValidationError`` and returns a sorted list of the
names of the top-level fields that have an error, without repeats, for
example ``["age", "email"]``.

``parse_users(rows)`` takes a list of dicts and returns ``(users, bad)``:
``users`` is the list of valid ``User`` objects, ``bad`` is a dict that maps
the row index (starting at 0) to the ``problems`` list of that row.
"""

from pydantic import BaseModel, Field, ValidationError, field_validator


class User(BaseModel):
    """A person who signs up."""

    # TODO: fields and validators
    ...


def parse_user(data):
    """Build a User from a dict (raises ValidationError)."""
    # TODO
    ...


def problems(exc):
    """Return the sorted names of the fields that failed validation."""
    # TODO
    ...


def parse_users(rows):
    """Return (valid users, {row index: failing field names})."""
    # TODO
    ...


if __name__ == "__main__":
    print(parse_user({"name": " Ada ", "age": "36", "email": "ADA@example.com"}))
