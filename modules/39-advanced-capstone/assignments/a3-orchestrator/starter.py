"""Capstone stage 3: a fan-out orchestrator with partial failures.

The *orchestrator* starts one worker per task, runs several at the same time,
and collects the results. One failed task must not lose the others, unless the
caller asks for fail-fast behaviour. Structured concurrency (``TaskGroup``,
topic 33) guarantees that no task is left running when the function returns.

The models of stage 1 are included so that this file works on its own. The
worker is passed in as a function, so tests can use a tiny fake worker.
"""

import asyncio
import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator


class ResearchTask(BaseModel):
    """One question to research. ``id`` and ``question`` are stripped of outer spaces."""

    model_config = ConfigDict(str_strip_whitespace=True)

    id: str = Field(min_length=1)
    question: str = Field(min_length=3)


class Finding(BaseModel):
    """The answer to one task. ``sources`` has no blanks and no duplicates."""

    model_config = ConfigDict(str_strip_whitespace=True)

    task_id: str
    answer: str = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    sources: list[str] = Field(default_factory=list)

    @field_validator("sources")
    @classmethod
    def clean_sources(cls, value: list[str]) -> list[str]:
        return list(dict.fromkeys(s.strip() for s in value if s.strip()))


class BadModelOutput(Exception):
    """The text from the model could not be turned into a ``Finding``."""


@dataclass
class RunResult:
    """What a research run produced."""

    findings: list[Finding] = field(default_factory=list)  # successes, in task order
    failures: dict[str, str] = field(default_factory=dict)  # task id -> error text


async def run_all(
    worker: Callable[[ResearchTask], object],
    tasks: list[ResearchTask],
    *,
    max_concurrency: int = 3,
    fail_fast: bool = False,
) -> RunResult:
    """Run ``await worker(task)`` for every task and collect a ``RunResult``.

    * ``worker`` is an async function that takes a ``ResearchTask`` and returns
      a ``Finding``.
    * Duplicate task ids raise ``ValueError`` (before anything runs).
    * Use ``asyncio.TaskGroup`` and an ``asyncio.Semaphore(max_concurrency)``,
      so that at most ``max_concurrency`` workers run at the same time.
    * ``result.findings`` has the successful findings in the ORDER OF ``tasks``
      (not in the order of completion).
    * Default mode (``fail_fast=False``): an ``Exception`` raised by a worker is
      recorded as ``result.failures[task.id] = f"{type(exc).__name__}: {exc}"``
      and the other tasks continue.
    * ``fail_fast=True``: do not catch worker exceptions. The ``TaskGroup``
      cancels the other workers (their ``finally`` blocks run) and raises an
      ``ExceptionGroup``, which you let propagate.
    * No tasks: return an empty ``RunResult``.
    """
    # TODO: check for duplicate ids, create one task per ResearchTask in a TaskGroup,
    # limit them with a Semaphore, then build the RunResult in the order of ``tasks``.
    ...


if __name__ == "__main__":

    async def demo() -> None:
        async def worker(task: ResearchTask) -> Finding:
            if "bad" in task.question:
                raise RuntimeError("model offline")
            return Finding(task_id=task.id, answer=f"About {task.question}", confidence=0.7)

        tasks = [ResearchTask(id=f"t{i}", question=q) for i, q in enumerate(["tides", "bad idea", "stars"], 1)]
        result = await run_all(worker, tasks)
        print([f.task_id for f in result.findings], result.failures)

    asyncio.run(demo())
