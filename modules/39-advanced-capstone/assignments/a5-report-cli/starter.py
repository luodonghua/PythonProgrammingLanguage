"""Capstone stage 5: the final report and the command line.

The pipeline is finished (models, worker, orchestrator). It is included below,
together with a ``DemoLLM`` that answers without a network. Your job is the
last layer: read the questions, format the report, and wire it all into a
command-line program.

Run the demo:  python starter.py questions.txt
"""

import argparse
import sys
from pathlib import Path

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


def parse_finding(task_id: str, raw: str) -> Finding:
    """Turn the model's reply ``raw`` into a ``Finding`` for ``task_id``.

    The reply should be a JSON object with ``answer``, ``confidence`` and
    optionally ``sources``. Models often wrap JSON in a Markdown code fence, so:

    1. If the stripped text starts with three backticks, drop the first line
       and, if the last line is three backticks, drop that line too.
    2. Parse the JSON. Text that is not JSON raises ``BadModelOutput`` with a
       message that contains ``"not valid JSON"``. JSON that is not an object
       raises ``BadModelOutput`` with ``"expected a JSON object"``.
    3. Build ``Finding`` from the object plus ``task_id`` (the ``task_id`` you
       pass in always wins over one in the reply). Invalid fields raise
       ``BadModelOutput`` with a message that starts with ``"invalid fields: "``
       followed by ``"<field>: <message>"`` items joined with ``"; "``.
    """
    text = raw.strip()
    if text.startswith("```"):
        lines = text.splitlines()[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise BadModelOutput(f"not valid JSON: {exc.msg}") from exc
    if not isinstance(data, dict):
        raise BadModelOutput("expected a JSON object")
    try:
        return Finding.model_validate({**data, "task_id": task_id})
    except ValidationError as exc:
        problems = "; ".join(f"{'.'.join(str(p) for p in e['loc'])}: {e['msg']}" for e in exc.errors())
        raise BadModelOutput(f"invalid fields: {problems}") from exc


def build_prompt(task: ResearchTask, feedback: str | None = None) -> str:
    """The text sent to the model. After a rejected reply, ``feedback`` says why."""
    prompt = f"Research question [{task.id}]: {task.question}\nReturn JSON with answer, confidence and sources."
    if feedback:
        prompt += f"\nYour previous answer was rejected: {feedback}\nReturn valid JSON only."
    return prompt


class WorkerFailed(Exception):
    """A worker gave up on a task. ``task_id`` names the task."""

    def __init__(self, task_id: str, reason: str) -> None:
        super().__init__(f"task {task_id} failed: {reason}")
        self.task_id = task_id
        self.reason = reason


async def run_worker(
    llm,
    task: ResearchTask,
    *,
    attempts: int = 3,
    timeout: float = 5.0,
    base_delay: float = 0.1,
    sleep=asyncio.sleep,
) -> Finding:
    """Ask the model about ``task`` and return a validated ``Finding``.

    Make at most ``attempts`` tries. In each try:

    * send ``build_prompt(task, feedback)`` with ``llm.ask`` and wait for the
      reply at most ``timeout`` seconds (``asyncio.timeout``);
    * ``parse_finding(task.id, reply)``. If that raises ``BadModelOutput``, the
      next try uses ``str(error)`` as ``feedback``. No waiting before it;
    * if the call raises ``TimeoutError`` or ``ConnectionError`` (temporary
      problems), wait ``await sleep(base_delay * 2 ** (n - 1))`` before the next
      try, where n is the number of the try that just failed (1, 2, ...).
      No sleep after the last try;
    * the first successful ``Finding`` is returned at once.

    After the last failed try raise ``WorkerFailed(task.id, reason)``, where
    ``reason`` is ``f"{type(error).__name__}: {error}"`` of the last error.
    Any other exception is a bug in the caller or in the model client. Let it propagate.
    """
    feedback: str | None = None
    last_error: Exception | None = None
    for n in range(1, attempts + 1):
        try:
            async with asyncio.timeout(timeout):
                reply = await llm.ask(build_prompt(task, feedback))
            return parse_finding(task.id, reply)
        except BadModelOutput as exc:
            last_error = exc
            feedback = str(exc)
        except (TimeoutError, ConnectionError) as exc:
            last_error = exc
            if n < attempts:
                await sleep(base_delay * 2 ** (n - 1))
    assert last_error is not None
    raise WorkerFailed(task.id, f"{type(last_error).__name__}: {last_error}")
    feedback: str | None = None
    last_error: Exception | None = None
    for n in range(1, attempts + 1):
        try:
            async with asyncio.timeout(timeout):
                reply = await llm.ask(build_prompt(task, feedback))
            return parse_finding(task.id, reply)
        except BadModelOutput as exc:
            last_error = exc
            feedback = str(exc)
        except (TimeoutError, ConnectionError) as exc:
            last_error = exc
            if n < attempts:
                await sleep(base_delay * 2 ** (n - 1))
    assert last_error is not None
    raise WorkerFailed(task.id, f"{type(last_error).__name__}: {last_error}")


@dataclass
class RunResult:
    """What a research run produced."""

    findings: list[Finding] = field(default_factory=list)  # successes, in task order
    failures: dict[str, str] = field(default_factory=dict)  # task id -> error text


async def run_all(worker: Callable, tasks: list[ResearchTask], *, max_concurrency: int = 3) -> RunResult:
    """Run the worker for every task (see stage 3). Failures are recorded, not raised."""
    semaphore = asyncio.Semaphore(max_concurrency)
    outcomes: dict[str, Finding | Exception] = {}

    async def run_one(task: ResearchTask) -> None:
        async with semaphore:
            try:
                outcomes[task.id] = await worker(task)
            except Exception as exc:
                outcomes[task.id] = exc

    async with asyncio.TaskGroup() as group:
        for task in tasks:
            group.create_task(run_one(task))
    result = RunResult()
    for task in tasks:
        outcome = outcomes[task.id]
        if isinstance(outcome, Exception):
            result.failures[task.id] = f"{type(outcome).__name__}: {outcome}"
        else:
            result.findings.append(outcome)
    return result


class DemoLLM:
    """Answers every question with a canned reply. A question that contains the
    word "unreachable" makes the model raise ``ConnectionError`` every time."""

    async def ask(self, prompt: str) -> str:
        question = prompt.split("]: ", 1)[1].splitlines()[0]
        if "unreachable" in question:
            raise ConnectionError("model offline")
        reply = {"answer": f"Notes about: {question}", "confidence": 0.8, "sources": ["demo://notes"]}
        return json.dumps(reply)


async def research(tasks: list[ResearchTask], llm, concurrency: int = 3) -> RunResult:
    """Answer all tasks with ``llm``: two tries per task, no waiting between tries."""

    async def worker(task: ResearchTask) -> Finding:
        return await run_worker(llm, task, attempts=2, timeout=5.0, base_delay=0.0)

    return await run_all(worker, tasks, max_concurrency=concurrency)


def load_tasks(path: Path) -> list[ResearchTask]:
    """Read questions from a text file, one per line, and return tasks.

    * The file is UTF-8 text. Lines are stripped. Blank lines and lines that
      start with ``#`` are skipped.
    * The kept lines get the ids ``"q1"``, ``"q2"``, ... in order.
    * A missing file raises ``FileNotFoundError`` (do not catch it here).
    """
    # TODO: read the file, skip blank and comment lines, number the rest.
    ...


def build_report(tasks: list[ResearchTask], result: RunResult) -> str:
    """Format a plain-text (Markdown) report. Every task has a finding or a failure.

    Layout (``N`` questions, ``A`` answered, ``F`` failed). Sections follow the
    order of ``tasks`` and are separated by one blank line. The text ends with
    exactly one newline:

        # Research report
        Questions: N | answered: A | failed: F

        ## q1: What causes the tides?
        <answer text>
        Confidence: 80%
        Sources: demo://notes, other

        ## q2: Is the unreachable server up?
        FAILED: <failure text>

    * ``Confidence`` is the confidence as a whole percent (``f"{value:.0%}"``).
    * The ``Sources:`` line is left out when there are no sources.
    * ``failed`` counts ``result.failures``; ``answered`` counts ``result.findings``.
    """
    # TODO: build the list of lines described above and join them with newlines.
    ...


def main(argv: list[str] | None = None, *, llm=None) -> int:
    """Command-line entry point. Return the exit code (do not call ``sys.exit``).

        research QUESTIONS_FILE [--concurrency N] [--format text|json] [-o FILE]

    * ``QUESTIONS_FILE``: path for ``load_tasks``.
    * ``--concurrency N``: int, default 3. A value below 1 prints
      ``error: --concurrency must be at least 1`` to stderr and returns 2.
    * ``--format``: ``text`` (default, ``build_report``) or ``json``. The JSON is
      ``json.dumps({"findings": [finding.model_dump() ...], "failures": {...}}, indent=2)``.
    * ``-o FILE`` / ``--output FILE``: write the report to FILE (UTF-8) and
      print ``Report written to FILE`` instead of the report.
    * ``llm`` defaults to ``DemoLLM()``. Tests pass their own.
    * A file that does not exist prints ``error: cannot read PATH`` to stderr
      and returns 2. A file without questions prints ``error: no questions found``
      to stderr and returns 2.
    * Run the pipeline with ``asyncio.run(research(tasks, llm, concurrency))``
      and print the report to stdout with ``print(text, end="")``.
    * Exit code: 0 when every task was answered, 1 when at least one failed.

    ``argparse`` handles bad options itself (it exits with code 2).
    """
    # TODO: argparse, load_tasks, asyncio.run(research(...)), print the report, return the exit code.
    ...


if __name__ == "__main__":
    sys.exit(main())
