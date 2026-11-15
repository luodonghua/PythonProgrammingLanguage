"""Assignment 3: Generic functions and a generic class (Python 3.12+ syntax).

Use the new type-parameter syntax, for example  def first[T](...)  and
class Box[T]:  (not TypeVar). The tests check the type parameters.

    first[T](items: Sequence[T]) -> T | None
        The first item, or None for an empty sequence.
    last[T](items: Sequence[T]) -> T | None
        The last item, or None for an empty sequence.
    pairs[A, B](a: Sequence[A], b: Sequence[B]) -> list[tuple[A, B]]
        Items of a and b side by side. Raise ValueError if the lengths differ.
    class Box[T]
        Box(item)         holds one item.
        .get() -> T       returns it.
        .map[U](f: Callable[[T], U]) -> Box[U]
                          a NEW Box that holds f(item). The old box is unchanged.
        repr(box)         "Box(3)" (use !r for the item).
"""

from collections.abc import Callable, Sequence


def first[T](items: Sequence[T]) -> T | None:
    return items[0] if items else None


def last[T](items: Sequence[T]) -> T | None:
    return items[-1] if items else None


def pairs[A, B](a: Sequence[A], b: Sequence[B]) -> list[tuple[A, B]]:
    if len(a) != len(b):
        raise ValueError("sequences must have the same length")
    return list(zip(a, b))


class Box[T]:
    def __init__(self, item: T) -> None:
        self._item = item

    def get(self) -> T:
        return self._item

    def map[U](self, f: Callable[[T], U]) -> "Box[U]":
        return Box(f(self._item))

    def __repr__(self) -> str:
        return f"Box({self._item!r})"


if __name__ == "__main__":
    print(first([1, 2]), last("abc"), pairs([1, 2], "ab"), Box(3))
