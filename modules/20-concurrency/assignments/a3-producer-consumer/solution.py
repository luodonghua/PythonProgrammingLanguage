"""Assignment 3: Producer and consumers connected by a Queue."""

import queue
import threading
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
    if consumers < 1:
        raise ValueError("consumers must be at least 1")
    work: queue.Queue = queue.Queue()
    results: list = [None] * len(items)

    def consume() -> None:
        while (job := work.get()) is not None:
            index, item = job
            try:
                results[index] = transform(item)
            except Exception as exc:
                results[index] = exc

    threads = [threading.Thread(target=consume) for _ in range(consumers)]
    for thread in threads:
        thread.start()
    for index, item in enumerate(items):
        work.put((index, item))
    for _ in threads:
        work.put(None)
    for thread in threads:
        thread.join()
    return results


def drain(q) -> list:
    """Return every item currently in queue `q` as a list, oldest first, without
    waiting. Use q.get_nowait() and stop when queue.Empty is raised."""
    items = []
    while True:
        try:
            items.append(q.get_nowait())
        except queue.Empty:
            return items


if __name__ == "__main__":
    print(run_pipeline([1, 2, 3, 4, 5], lambda x: x * 10))
