"""Assignment 4: Validate data against a TypedDict (hints are not enforced at run time).

    class Book(TypedDict)   title: str, pages: int, tags: list[str]
                            (already defined below)

    validate(data, schema) -> list[str]
        Check the dict `data` against the TypedDict class `schema`, using
        typing.get_type_hints(schema). Return a list of error messages
        (an empty list means the data is valid). Messages, in this order:

          1. for each field of the schema, in schema order:
               missing key        -> "missing key: <name>"
               wrong type         -> "<name> must be <type>"
          2. then for each extra key in data, sorted: "unexpected key: <key>"

        <type> is the class name ("str", "int") or, for list[X], "list[X]".
        A value is the right type if isinstance(value, type) is true, EXCEPT
        that a bool is not accepted where int is expected.
        For list[X] the value must be a list and every item must be an X
        (apply the same bool rule). Only plain classes (str, int, float, bool)
        and list[X] of those need to work.

    describe(book) -> str
        "<title> (<pages> pages, <n> tags)"  e.g.  "Dune (412 pages, 2 tags)"
"""

from typing import TypedDict, get_args, get_origin, get_type_hints


class Book(TypedDict):
    title: str
    pages: int
    tags: list[str]


def validate(data, schema):
    """Return the list of error messages described in the module docstring."""
    # TODO: loop over get_type_hints(schema).items(); add a helper for the
    # type check (remember: bool is not an int, and list[X] needs get_origin / get_args).
    ...


def describe(book):
    """Return "<title> (<pages> pages, <n> tags)"."""
    # TODO
    ...


if __name__ == "__main__":
    good = {"title": "Dune", "pages": 412, "tags": ["sf", "classic"]}
    bad = {"title": 5, "pages": True, "extra": 1}
    print(validate(good, Book), validate(bad, Book))
    print(describe(good))
