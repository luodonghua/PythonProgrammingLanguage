"""Assignment 2: A thread-safe counter."""

import threading
from collections.abc import Callable


class SafeCounter:
    """A counter that several threads can change at the same time.

    - It starts at 0 (or at `start`).
    - increment(n=1) adds n and returns nothing.
    - value is a read-only property with the current count.
    - reset() sets the count back to 0.

    Protect every change with one lock created by `threading.Lock()` in __init__
    (write `threading.Lock()`, not `from threading import Lock`), and use it in
    a `with` statement.
    """

    def __init__(self, start: int = 0) -> None:
        # TODO: store the count and create a Lock.
        ...

    def increment(self, n: int = 1) -> None:
        """Add n to the counter. Must not lose updates when called from many threads."""
        # TODO: update the count while holding the lock.
        ...

    @property
    def value(self) -> int:
        """The current count."""
        # TODO: return the count.
        ...

    def reset(self) -> None:
        """Set the count back to 0."""
        # TODO: reset under the lock.
        ...


def run_in_threads(task: Callable[[], None], thread_count: int) -> None:
    """Run `task()` in `thread_count` threads at once and wait for all of them.

    Raise ValueError if thread_count is less than 1.
    """
    # TODO: create, start and join the threads.
    ...


if __name__ == "__main__":
    counter = SafeCounter()
    run_in_threads(lambda: [counter.increment() for _ in range(10_000)], 4)
    print(counter.value)
