"""Assignment 3: A Stack and a Queue."""

from collections import deque


class Stack:
    """Last in, first out.

    Stack()              starts empty. Stack([1, 2]) starts with 1 at the bottom, 2 on top.
    .push(item)          put item on top.
    .pop()               remove and return the top item.
                         On an empty stack raise IndexError("pop from empty stack").
    .peek()              return the top item without removing it (same IndexError when empty).
    len(s)               number of items.
    bool(s)              False when empty (comes for free from __len__).
    iter(s) / list(s)    items from top to bottom.
    repr(s)              "Stack([1, 2, 3])" listing bottom to top.
    """

    def __init__(self, items=()) -> None:
        self._items = list(items)

    def push(self, item) -> None:
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items[-1]

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(reversed(self._items))

    def __repr__(self) -> str:
        return f"Stack({self._items!r})"


class Queue:
    """First in, first out.

    Queue()              starts empty. Queue([1, 2]) has 1 at the front.
    .enqueue(item)       add item at the back.
    .dequeue()           remove and return the front item.
                         On an empty queue raise IndexError("dequeue from empty queue").
    len(q), bool(q)      number of items, and False when empty.
    iter(q) / list(q)    items from front to back.
    repr(q)              "Queue([1, 2, 3])" listing front to back.

    Use collections.deque so that dequeue is fast.
    """

    def __init__(self, items=()) -> None:
        self._items = deque(items)

    def enqueue(self, item) -> None:
        self._items.append(item)

    def dequeue(self):
        if not self._items:
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __repr__(self) -> str:
        return f"Queue({list(self._items)!r})"


if __name__ == "__main__":
    s = Stack([1, 2, 3])
    q = Queue([1, 2, 3])
    print(s.pop(), q.dequeue(), s, q)
