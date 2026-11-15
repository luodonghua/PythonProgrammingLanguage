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
    """One question to research.

    Fields: ``id`` (str, at least 1 character) and ``question`` (str, at least
    3 characters). Spaces at both ends of every string are removed BEFORE the
    length check (see ``ConfigDict(str_strip_whitespace=True)``).
    """

    # TODO: add model_config and the two fields.


class Finding(BaseModel):
    """The answer to one task.

    Fields: ``task_id`` (str), ``answer`` (str, at least 1 character),
    ``confidence`` (float from 0 to 1, both included) and ``sources`` (list of
    str, default empty list). Strip spaces from strings as in ``ResearchTask``.
    A validator for ``sources`` strips every item, drops items that are empty
    and removes duplicates, keeping the first occurrence and the order.
    """

    # TODO: add model_config, the fields and the validator.


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
    # TODO: strip a Markdown code fence, parse the JSON, build the Finding.
    ...


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
        # TODO: copy the script and create the prompts list.
        ...

    async def ask(self, prompt: str) -> str:
        # TODO: follow steps 1 to 4 of the class docstring.
        ...


if __name__ == "__main__":

    async def demo() -> None:
        llm = FakeLLM({"tides": ['{"answer": "The Moon.", "confidence": 0.9, "sources": ["a", "a"]}']})
        reply = await llm.ask("Research question [t1]: What causes tides?")
        print(parse_finding("t1", reply))

    asyncio.run(demo())
