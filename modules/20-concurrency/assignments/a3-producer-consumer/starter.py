"""Assignment 3: Producer and consumers connected by a Queue."""

from collections.abc import Callable
from typing import Any


def run_pipeline(
    items: list,
    transform: Callable[[Any], Any],
    consumers: int = 3,
) -> list:
    """Apply `transform` to every item using one producer and several consumers.

    Design:
    - Create a queue.Queue. The calling thread (or one producer thread) puts
      (index, item) pairs on the queue.
    - Start `consumers` threads. Each one takes pairs from the queue, computes
      transform(item) and stores the result at position `index` of a results
      list that was created with the right length in advance.
    - To stop the consumers, put one None per consumer on the queue after the
      last item. A consumer ends when it gets None.
    - Wait for every consumer thread with join(), then return the results.
      The result list is in the same order as `items`.

    Raise ValueError if consumers is less than 1.
    If `transform` raises an exception for an item, store that exception
    object (not raise it) as the result for that item, and carry on.
    """
    # TODO: build the queue, start the consumer threads, feed them, join them.
    ...


def drain(q) -> list:
    """Return every item currently in queue `q` as a list, oldest first, without
    waiting. Use q.get_nowait() and stop when queue.Empty is raised."""
    # TODO: loop with get_nowait() inside try/except queue.Empty.
    ...


if __name__ == "__main__":
    print(run_pipeline([1, 2, 3, 4, 5], lambda x: x * 10))
