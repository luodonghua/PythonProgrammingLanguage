"""Assignment 4: Use a process pool for CPU-bound work.

Functions sent to a ProcessPoolExecutor must be picklable. Built-in functions
such as sum, math.factorial and os.getpid are, and so is any function defined
at the top level of a module. Lambdas are not.
"""

from collections.abc import Callable, Iterable
from typing import Any


def process_map(func: Callable[[Any], Any], items: Iterable, workers: int = 2) -> list:
    """Apply `func` to every item in a pool of `workers` processes.

    Return the results in input order. Raise ValueError if workers < 1.
    """
    # TODO: use concurrent.futures.ProcessPoolExecutor and its map method.
    ...


def split_chunks(numbers: list[int], parts: int) -> list[list[int]]:
    """Split `numbers` into `parts` consecutive chunks of nearly equal size.

    The chunks are in order, the first (len % parts) chunks get one extra
    item, and no chunk is dropped even if it is empty.
    split_chunks([1, 2, 3, 4, 5], 2)  -> [[1, 2, 3], [4, 5]]
    split_chunks([1, 2], 3)           -> [[1], [2], []]
    Raise ValueError if parts < 1.
    """
    # TODO: use divmod(len(numbers), parts) to get the size and the remainder.
    ...


def parallel_sum(numbers: list[int], workers: int = 2) -> int:
    """Sum `numbers` by summing `workers` chunks in separate processes.

    Use split_chunks, then process_map(sum, chunks, workers), then add the
    partial sums together. An empty list gives 0.
    """
    # TODO: combine split_chunks and process_map.
    ...


def worker_pids(jobs: int, workers: int = 2) -> set[int]:
    """Run os.getpid in the pool `jobs` times and return the set of process ids
    that answered. None of them may be the id of the calling process."""
    # TODO: submit os.getpid `jobs` times to a ProcessPoolExecutor.
    ...


if __name__ == "__main__":
    print(parallel_sum(list(range(1_000_000)), workers=4))
    print(len(worker_pids(8)) >= 1)
