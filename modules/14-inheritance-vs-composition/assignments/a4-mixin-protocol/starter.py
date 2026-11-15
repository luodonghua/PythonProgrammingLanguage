"""Assignment 4: Mixins and a Protocol."""

import json
from collections.abc import Iterable
from typing import Protocol, runtime_checkable


class ReprMixin:
    """Gives any class a readable __repr__ built from its instance attributes.

    repr(obj) -> "ClassName(a=1, b='x')"  (attributes in the order they were set,
    values shown with repr, class name from type(self).__name__).
    An object with no attributes gives "ClassName()".
    """

    def __repr__(self):
        # TODO: use vars(self).items()
        ...


class JsonMixin:
    """Gives any class a to_json() method.

    obj.to_json() -> json.dumps(vars(self), sort_keys=True)
    """

    def to_json(self):
        # TODO
        ...


class Person(ReprMixin, JsonMixin):
    """Person(name, age) with both mixins. Store the arguments as .name and .age."""

    def __init__(self, name, age):
        # TODO
        ...


@runtime_checkable
class Renderable(Protocol):
    """Anything with a render() method that returns a str."""

    def render(self) -> str: ...


class Heading:
    """Heading(text, level=1). render() -> "#" * level + " " + text.
    level must be between 1 and 6, else ValueError. Do not inherit from anything."""

    def __init__(self, text, level=1):
        # TODO
        ...

    # TODO: add render().


class Paragraph:
    """Paragraph(text). render() -> the text with outer spaces removed.
    Do not inherit from anything."""

    def __init__(self, text):
        # TODO
        ...

    # TODO: add render().


def render_all(items: Iterable[Renderable], sep: str = "\n\n") -> str:
    """Call render() on every item and join the results with sep."""
    # TODO
    ...


if __name__ == "__main__":
    print(repr(Person("Ann", 30)), Person("Ann", 30).to_json())
    print(render_all([Heading("Title"), Paragraph("  Some text.  ")]))
