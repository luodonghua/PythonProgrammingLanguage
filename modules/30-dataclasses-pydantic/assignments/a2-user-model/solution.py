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

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator


class User(BaseModel):
    """A person who signs up."""

    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=50)
    age: int = Field(ge=0, le=150)
    email: str
    tags: list[str] = []

    @field_validator("email")
    @classmethod
    def check_email(cls, value):
        local, at, domain = value.partition("@")
        if not (local and at and domain) or "@" in domain:
            raise ValueError("email must look like name@host")
        return value.lower()


def parse_user(data):
    """Build a User from a dict (raises ValidationError)."""
    return User.model_validate(data)


def problems(exc):
    """Return the sorted names of the fields that failed validation."""
    return sorted({str(error["loc"][0]) for error in exc.errors() if error["loc"]})


def parse_users(rows):
    """Return (valid users, {row index: failing field names})."""
    users = []
    bad = {}
    for index, row in enumerate(rows):
        try:
            users.append(parse_user(row))
        except ValidationError as exc:
            bad[index] = problems(exc)
    return users, bad


if __name__ == "__main__":
    print(parse_user({"name": " Ada ", "age": "36", "email": "ADA@example.com"}))
