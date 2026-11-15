import pytest
from pydantic import BaseModel, ValidationError

from practice import load

m = load(__file__)

GOOD = '{"title": "Printer jam", "priority": "high", "estimate_hours": 2}'


class ScriptedProducer:
    """A fake producer that returns prepared answers and records prompts."""

    def __init__(self, *answers):
        self.answers = list(answers)
        self.prompts = []

    def __call__(self, prompt):
        self.prompts.append(prompt)
        return self.answers.pop(0)


def error_of(model, text):
    with pytest.raises(ValidationError) as info:
        model.model_validate_json(text)
    return info.value


def test_first_try_success():
    producer = ScriptedProducer(GOOD)
    ticket, attempts = m.parse_until_valid(producer, m.Ticket, "Describe it")
    assert ticket.title == "Printer jam"
    assert ticket.estimate_hours == 2
    assert attempts == 1
    assert producer.prompts == ["Describe it"]


def test_second_try_gets_feedback_in_prompt():
    producer = ScriptedProducer('{"title": "Printer jam", "priority": "urgent", "estimate_hours": 2}', GOOD)
    ticket, attempts = m.parse_until_valid(producer, m.Ticket, "Describe it")
    assert attempts == 2
    assert ticket.priority == "high"
    first, second = producer.prompts
    assert first == "Describe it"
    assert second.startswith("Describe it\nFix these problems:\n- priority: ")


def test_feedback_mentions_every_problem():
    producer = ScriptedProducer('{"title": "x", "priority": "low", "estimate_hours": 99}', GOOD)
    m.parse_until_valid(producer, m.Ticket, "T")
    second = producer.prompts[1]
    assert "- title: " in second
    assert "- estimate_hours: " in second
    assert "- priority: " not in second


def test_prompt_is_built_from_original_task_each_time():
    bad = '{"title": "x", "priority": "low", "estimate_hours": 1}'
    producer = ScriptedProducer(bad, bad, GOOD)
    _, attempts = m.parse_until_valid(producer, m.Ticket, "T", max_tries=3)
    assert attempts == 3
    assert producer.prompts[1] == producer.prompts[2]
    assert producer.prompts[2].count("Fix these problems:") == 1


def test_not_json_is_handled():
    producer = ScriptedProducer("sorry, I cannot do JSON", GOOD)
    _, attempts = m.parse_until_valid(producer, m.Ticket, "T")
    assert attempts == 2
    assert "- input: " in producer.prompts[1]


def test_gives_up_after_max_tries():
    producer = ScriptedProducer("{}", "{}")
    with pytest.raises(m.GaveUp) as info:
        m.parse_until_valid(producer, m.Ticket, "T", max_tries=2)
    assert info.value.attempts == 2
    assert "- title: " in info.value.feedback
    assert len(producer.prompts) == 2


def test_works_with_any_model():
    class Point(BaseModel):
        x: int

    producer = ScriptedProducer('{"x": "left"}', '{"x": 3}')
    point, attempts = m.parse_until_valid(producer, Point, "give x")
    assert point.x == 3
    assert attempts == 2


def test_format_feedback_lines():
    exc = error_of(m.Ticket, '{"title": "x", "priority": "low", "estimate_hours": 1}')
    text = m.format_feedback(exc)
    assert text.startswith("- title: ")
    assert "\n" not in text


def test_format_feedback_nested_location_and_order():
    class Item(BaseModel):
        name: str

    class Box(BaseModel):
        items: list[Item]
        label: int

    exc = error_of(Box, '{"items": [{"name": "a"}, {}], "label": "x"}')
    lines = m.format_feedback(exc).split("\n")
    assert lines[0].startswith("- items.1.name: ")
    assert lines[1].startswith("- label: ")
    assert len(lines) == 2


def test_format_feedback_whole_input():
    exc = error_of(m.Ticket, "not json")
    assert m.format_feedback(exc).startswith("- input: ")
