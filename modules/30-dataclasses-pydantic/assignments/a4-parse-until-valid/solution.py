"""Assignment 4: "parse until valid" with error feedback.

A *producer* is any function ``producer(prompt: str) -> str`` that returns JSON
text. In real programs it could be a person, a web service or a language
model. Its answers may be invalid, so we validate them with Pydantic and, on
failure, ask again with a description of what was wrong.

``Ticket`` (given) is the model the answers must fit.

``format_feedback(exc)`` takes a ``ValidationError`` and returns a string with
one line per error, in order: ``"- <where>: <message>"``. ``<where>`` is the
error location joined with dots (``"estimate_hours"``, or ``"items.0.name"``
for nested places), or ``"input"`` when the location is empty (for example
when the text is not JSON at all). ``<message>`` is Pydantic's ``msg``.
Lines are joined with ``"\\n"``.

``GaveUp`` is an exception class with attributes ``attempts`` (int) and
``feedback`` (the feedback text of the last failure). Its message can be any
text.

``parse_until_valid(producer, model, task, max_tries=3)``:

1. ``prompt = task``.
2. Call ``producer(prompt)`` and validate the result with
   ``model.model_validate_json``.
3. If valid, return ``(instance, attempts)`` where ``attempts`` counts calls
   to the producer (1 for a first-try success).
4. If invalid, build the next prompt as
   ``task + "\\nFix these problems:\\n" + feedback`` (always starting from the
   original ``task``, not from the previous prompt) and try again.
5. After ``max_tries`` failed calls raise ``GaveUp``.
"""

from typing import Literal

from pydantic import BaseModel, Field, ValidationError


class Ticket(BaseModel):
    """A support ticket."""

    title: str = Field(min_length=3)
    priority: Literal["low", "medium", "high"]
    estimate_hours: int = Field(ge=1, le=40)


class GaveUp(Exception):
    """Raised when the producer never gives valid data."""

    def __init__(self, attempts, feedback):
        super().__init__(f"no valid answer after {attempts} attempts")
        self.attempts = attempts
        self.feedback = feedback


def format_feedback(exc):
    """Turn a ValidationError into lines of text for the producer."""
    lines = []
    for error in exc.errors():
        where = ".".join(str(part) for part in error["loc"]) or "input"
        lines.append(f"- {where}: {error['msg']}")
    return "\n".join(lines)


def parse_until_valid(producer, model, task, max_tries=3):
    """Return (model instance, attempts), asking again after each failure."""
    prompt = task
    feedback = ""
    for attempt in range(1, max_tries + 1):
        text = producer(prompt)
        try:
            return model.model_validate_json(text), attempt
        except ValidationError as exc:
            feedback = format_feedback(exc)
            prompt = task + "\nFix these problems:\n" + feedback
    raise GaveUp(max_tries, feedback)


if __name__ == "__main__":
    answers = iter(['{"title": "x"}', '{"title": "Printer", "priority": "high", "estimate_hours": 2}'])
    ticket, attempts = parse_until_valid(lambda prompt: next(answers), Ticket, "Describe the ticket")
    print(ticket, attempts)
