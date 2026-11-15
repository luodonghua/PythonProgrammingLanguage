"""Capstone stage 4: streamed progress events with trace ids.

While the workers run, a user interface wants to hear what is going on. The
runner becomes an *async generator*: it yields small event dicts as they happen.
Every event carries a ``trace_id``, and the id is also stored in a ``ContextVar``
so that workers and log lines can read it without a parameter.

The models of stage 1 are included so that this file works on its own.
"""

import uuid
from collections.abc import AsyncIterator
from contextvars import ContextVar

import asyncio
import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

trace_id_var: ContextVar[str] = ContextVar("trace_id", default="-")


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


async def run_with_events(
    worker: Callable[[ResearchTask], object],
    tasks: list[ResearchTask],
    *,
    trace_id: str | None = None,
    max_concurrency: int = 3,
) -> AsyncIterator[dict]:
    """Run all tasks and yield progress events as they happen.

    Events are dicts, and every one has the key ``"trace_id"``:

    * ``{"type": "started", "task_id": id}`` when a worker starts (after it got
      a free slot of the ``max_concurrency`` limit);
    * ``{"type": "finished", "task_id": id, "confidence": finding.confidence}``
      when ``await worker(task)`` returns a ``Finding``;
    * ``{"type": "failed", "task_id": id, "error": "<ExcType>: <message>"}``
      when the worker raises an ``Exception`` (the run goes on);
    * ``{"type": "done", "ok": n_finished, "failed": n_failed}``, always the last event.

    Rules:

    * ``trace_id`` defaults to ``uuid.uuid4().hex[:8]``. Set ``trace_id_var`` to
      it BEFORE the workers are created, so that they (and the tasks they start)
      can read it. Restore the old value when the generator ends (``Token`` from
      ``set``; ignore a ``ValueError`` from ``reset``).
    * For one task, ``started`` comes before ``finished`` or ``failed``.
    * Use an ``asyncio.Queue`` between the workers and the generator: one
      background task (``asyncio.create_task``) runs the workers in a
      ``TaskGroup`` and puts events into the queue; the generator takes events
      out and yields them. Put ``None`` into the queue after the ``done`` event
      as the end marker.
    * If the consumer stops early (``aclose()``), cancel the background task and
      wait for it, so no worker keeps running.
    """
    # TODO: set trace_id_var, start a background task that fills an asyncio.Queue,
    # and yield events from the queue until the end marker None.
    # The "yield" below makes this an async generator; replace it with your own.
    yield {}


if __name__ == "__main__":

    async def demo() -> None:
        async def worker(task: ResearchTask) -> Finding:
            await asyncio.sleep(0)
            if "bad" in task.question:
                raise RuntimeError("model offline")
            return Finding(task_id=task.id, answer="ok", confidence=0.8)

        tasks = [ResearchTask(id=f"t{i}", question=q) for i, q in enumerate(["tides", "bad idea"], 1)]
        async for event in run_with_events(worker, tasks, trace_id="demo", max_concurrency=1):
            print(event)

    asyncio.run(demo())
