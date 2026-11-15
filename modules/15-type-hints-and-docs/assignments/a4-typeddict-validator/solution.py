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


def _is_instance(value: object, expected: type) -> bool:
    if expected is int and isinstance(value, bool):
        return False
    return isinstance(value, expected)


def _matches(value: object, expected: object) -> bool:
    if get_origin(expected) is list:
        (item_type,) = get_args(expected)
        return isinstance(value, list) and all(_is_instance(v, item_type) for v in value)
    return _is_instance(value, expected)


def _type_name(expected: object) -> str:
    if get_origin(expected) is list:
        (item_type,) = get_args(expected)
        return f"list[{item_type.__name__}]"
    return expected.__name__


def validate(data: dict, schema: type) -> list[str]:
    errors = []
    hints = get_type_hints(schema)
    for name, expected in hints.items():
        if name not in data:
            errors.append(f"missing key: {name}")
        elif not _matches(data[name], expected):
            errors.append(f"{name} must be {_type_name(expected)}")
    for key in sorted(set(data) - set(hints)):
        errors.append(f"unexpected key: {key}")
    return errors


def describe(book: Book) -> str:
    return f"{book['title']} ({book['pages']} pages, {len(book['tags'])} tags)"


if __name__ == "__main__":
    good = {"title": "Dune", "pages": 412, "tags": ["sf", "classic"]}
    bad = {"title": 5, "pages": True, "extra": 1}
    print(validate(good, Book), validate(bad, Book))
    print(describe(good))
