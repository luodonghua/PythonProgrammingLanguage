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
        self._count = start
        self._lock = threading.Lock()

    def increment(self, n: int = 1) -> None:
        """Add n to the counter. Must not lose updates when called from many threads."""
        with self._lock:
            self._count += n

    @property
    def value(self) -> int:
        """The current count."""
        with self._lock:
            return self._count

    def reset(self) -> None:
        """Set the count back to 0."""
        with self._lock:
            self._count = 0


def run_in_threads(task: Callable[[], None], thread_count: int) -> None:
    """Run `task()` in `thread_count` threads at once and wait for all of them.

    Raise ValueError if thread_count is less than 1.
    """
    if thread_count < 1:
        raise ValueError("thread_count must be at least 1")
    threads = [threading.Thread(target=task) for _ in range(thread_count)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    counter = SafeCounter()
    run_in_threads(lambda: [counter.increment() for _ in range(10_000)], 4)
    print(counter.value)
