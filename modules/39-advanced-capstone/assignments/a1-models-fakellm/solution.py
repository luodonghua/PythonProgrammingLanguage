"""Capstone stage 1: data models and a scripted fake model.

The project is a *research runner*. It takes a list of questions, gives each
one to a sub-agent (a worker that asks a language model), and collects the
answers into a report. This stage builds the data layer:

* ``ResearchTask`` and ``Finding``: validated data (pydantic, topic 30);
* ``parse_finding``: turn the model's text reply into a ``Finding``, or fail
  with a clear error that can be sent back to the model;
* ``FakeLLM``: a scripted model, so everything stays offline and repeatable.
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


class FakeLLM:
    """A scripted stand-in for a language model (no network, no randomness).

    ``FakeLLM(script)``: ``script`` maps a piece of question text to a list of
    replies. A reply is a string (returned) or an exception instance (raised).

    ``await llm.ask(prompt)``:

    1. append ``prompt`` to ``self.prompts``;
    2. let other tasks run (``await asyncio.sleep(0)``);
    3. find the FIRST key of ``script`` (in insertion order) that occurs in
       ``prompt``. If there is none, raise ``AssertionError("no script for prompt")``;
    4. take the next reply of that key's list. If the list is empty, raise
       ``AssertionError("script exhausted")``. Raise it if it is an exception,
       otherwise return it.

    Keying by question text keeps tests deterministic even when many tasks
    call the model at the same time. The constructor copies the lists.
    """

    def __init__(self, script: Mapping[str, list]) -> None:
        self._script = {key: list(replies) for key, replies in script.items()}
        self.prompts: list[str] = []

    async def ask(self, prompt: str) -> str:
        self.prompts.append(prompt)
        await asyncio.sleep(0)
        for key, replies in self._script.items():
            if key in prompt:
                break
        else:
            raise AssertionError("no script for prompt")
        if not replies:
            raise AssertionError("script exhausted")
        reply = replies.pop(0)
        if isinstance(reply, BaseException):
            raise reply
        return reply


if __name__ == "__main__":

    async def demo() -> None:
        llm = FakeLLM({"tides": ['{"answer": "The Moon.", "confidence": 0.9, "sources": ["a", "a"]}']})
        reply = await llm.ask("Research question [t1]: What causes tides?")
        print(parse_finding("t1", reply))

    asyncio.run(demo())
