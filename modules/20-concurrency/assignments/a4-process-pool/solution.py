"""Assignment 4: Use a process pool for CPU-bound work.

Functions sent to a ProcessPoolExecutor must be picklable. Built-in functions
such as sum, math.factorial and os.getpid are, and so is any function defined
at the top level of a module. Lambdas are not.
"""

import os
from collections.abc import Callable, Iterable
from concurrent.futures import ProcessPoolExecutor
from typing import Any


def process_map(func: Callable[[Any], Any], items: Iterable, workers: int = 2) -> list:
    """Apply `func` to every item in a pool of `workers` processes.

    Return the results in input order. Raise ValueError if workers < 1.
    """
    if workers < 1:
        raise ValueError("workers must be at least 1")
    with ProcessPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(func, items))


def split_chunks(numbers: list[int], parts: int) -> list[list[int]]:
    """Split `numbers` into `parts` consecutive chunks of nearly equal size.

    The chunks are in order, the first (len % parts) chunks get one extra
    item, and no chunk is dropped even if it is empty.
    split_chunks([1, 2, 3, 4, 5], 2)  -> [[1, 2, 3], [4, 5]]
    split_chunks([1, 2], 3)           -> [[1], [2], []]
    Raise ValueError if parts < 1.
    """
    if parts < 1:
        raise ValueError("parts must be at least 1")
    size, extra = divmod(len(numbers), parts)
    chunks = []
    start = 0
    for i in range(parts):
        end = start + size + (1 if i < extra else 0)
        chunks.append(numbers[start:end])
        start = end
    return chunks


def parallel_sum(numbers: list[int], workers: int = 2) -> int:
    """Sum `numbers` by summing `workers` chunks in separate processes.

    Use split_chunks, then process_map(sum, chunks, workers), then add the
    partial sums together. An empty list gives 0.
    """
    chunks = split_chunks(numbers, workers)
    return sum(process_map(sum, chunks, workers))


def worker_pids(jobs: int, workers: int = 2) -> set[int]:
    """Run os.getpid in the pool `jobs` times and return the set of process ids
    that answered. None of them may be the id of the calling process."""
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(os.getpid) for _ in range(jobs)]
        return {future.result() for future in futures}


if __name__ == "__main__":
    print(parallel_sum(list(range(1_000_000)), workers=4))
    print(len(worker_pids(8)) >= 1)
