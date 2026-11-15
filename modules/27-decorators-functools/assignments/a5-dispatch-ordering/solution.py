"""Assignment 5: singledispatch and total_ordering.

Part 1. ``describe(value)`` is a ``functools.singledispatch`` function that
returns a string by type:

* int   -> ``"int 5"``
* str   -> ``"text 'hi'"``       (uses repr of the string)
* list  -> ``"list of 3"``       (number of items)
* dict  -> ``"dict with keys a, b"``  (keys in insertion order, joined by ", ")
* anything else -> ``"object <repr>"``, for example ``"object 2.5"``

Note: ``bool`` is a subclass of ``int``, so ``describe(True)`` gives ``"int True"``.

Part 2. ``Version`` is a class built from text like ``"1.10.2"``.

* ``Version("1.10.2").parts`` is the tuple ``(1, 10, 2)``
* ``==`` and ``<`` compare ``parts`` (so ``"1.10" > "1.9"``)
* use ``functools.total_ordering`` so that ``<=``, ``>`` and ``>=`` work too
* comparing with a non-Version returns ``NotImplemented``
* ``repr`` is ``Version('1.10.2')``
* ``sorted([...])`` of Versions must work.
"""

import functools


@functools.singledispatch
def describe(value):
    """Describe a value by its type."""
    return f"object {value!r}"


@describe.register
def _(value: int):
    return f"int {value}"


@describe.register
def _(value: str):
    return f"text {value!r}"


@describe.register
def _(value: list):
    return f"list of {len(value)}"


@describe.register
def _(value: dict):
    return "dict with keys " + ", ".join(str(key) for key in value)


@functools.total_ordering
class Version:
    """A dotted version number such as 1.10.2."""

    def __init__(self, text):
        self.text = text
        self.parts = tuple(int(part) for part in text.split("."))

    def __eq__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self.parts == other.parts

    def __lt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self.parts < other.parts

    def __hash__(self):
        return hash(self.parts)

    def __repr__(self):
        return f"Version({self.text!r})"


if __name__ == "__main__":
    print(describe(5), describe([1, 2]), describe(2.5))
