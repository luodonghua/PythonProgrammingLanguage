import json

import pytest
from pydantic import ValidationError

from practice import load

m = load(__file__)


def test_task_strips_spaces_and_validates():
    task = m.ResearchTask(id=" t1 ", question="  What causes tides?  ")
    assert task.id == "t1"
    assert task.question == "What causes tides?"


@pytest.mark.parametrize("kwargs", [{"id": "", "question": "What is X?"}, {"id": "t1", "question": "  "}, {"id": "t1", "question": "ab"}])
def test_task_rejects_bad_values(kwargs):
    with pytest.raises(ValidationError):
        m.ResearchTask(**kwargs)


def test_finding_defaults_and_source_cleaning():
    finding = m.Finding(task_id="t1", answer="Because.", confidence=0.5, sources=[" a ", "b", "a", "", "  "])
    assert finding.sources == ["a", "b"]
    assert m.Finding(task_id="t1", answer="x", confidence=1).sources == []


@pytest.mark.parametrize("confidence", [-0.1, 1.1])
def test_finding_confidence_range(confidence):
    with pytest.raises(ValidationError):
        m.Finding(task_id="t1", answer="x", confidence=confidence)


def test_finding_needs_an_answer():
    with pytest.raises(ValidationError):
        m.Finding(task_id="t1", answer="   ", confidence=0.5)


def test_parse_finding_plain_json():
    raw = json.dumps({"answer": "The Moon.", "confidence": 0.9, "sources": ["wiki"]})
    finding = m.parse_finding("t7", raw)
    assert finding == m.Finding(task_id="t7", answer="The Moon.", confidence=0.9, sources=["wiki"])


def test_parse_finding_accepts_a_code_fence():
    raw = '```json\n{"answer": "Yes.", "confidence": "0.75"}\n```'
    finding = m.parse_finding("t1", raw)
    assert finding.answer == "Yes."
    assert finding.confidence == 0.75
    assert finding.sources == []


def test_parse_finding_fence_without_closing_line():
    finding = m.parse_finding("t1", '```\n{"answer": "Yes.", "confidence": 1}')
    assert finding.confidence == 1


def test_task_id_argument_wins():
    raw = json.dumps({"task_id": "evil", "answer": "x", "confidence": 0.1})
    assert m.parse_finding("t1", raw).task_id == "t1"


def test_not_json():
    with pytest.raises(m.BadModelOutput, match="not valid JSON"):
        m.parse_finding("t1", "Sure! The answer is 42.")


@pytest.mark.parametrize("raw", ["[1, 2]", '"text"', "null", "5"])
def test_json_that_is_not_an_object(raw):
    with pytest.raises(m.BadModelOutput, match="expected a JSON object"):
        m.parse_finding("t1", raw)


def test_invalid_fields_are_listed():
    raw = json.dumps({"answer": "", "confidence": 3})
    with pytest.raises(m.BadModelOutput) as info:
        m.parse_finding("t1", raw)
    text = str(info.value)
    assert text.startswith("invalid fields: ")
    assert "answer" in text and "confidence" in text
    assert "; " in text


def test_missing_field_is_named():
    with pytest.raises(m.BadModelOutput, match="confidence"):
        m.parse_finding("t1", '{"answer": "x"}')


async def test_fake_llm_replays_replies_by_key():
    llm = m.FakeLLM({"tides": ["one", "two"], "stars": ["three"]})
    assert await llm.ask("Research question [a]: What about stars?") == "three"
    assert await llm.ask("Research question [b]: What causes tides?") == "one"
    assert await llm.ask("tides again") == "two"
    assert len(llm.prompts) == 3
    assert llm.prompts[0].endswith("stars?")


async def test_fake_llm_raises_exception_items():
    llm = m.FakeLLM({"q": [ConnectionError("offline"), "ok"]})
    with pytest.raises(ConnectionError, match="offline"):
        await llm.ask("q")
    assert await llm.ask("q") == "ok"


async def test_fake_llm_complains_about_unscripted_calls():
    llm = m.FakeLLM({"known": ["x"]})
    with pytest.raises(AssertionError, match="no script"):
        await llm.ask("something else")
    await llm.ask("known")
    with pytest.raises(AssertionError, match="exhausted"):
        await llm.ask("known")


async def test_fake_llm_copies_the_script_and_yields_to_other_tasks():
    import asyncio

    script = {"q": ["a"]}
    llm = m.FakeLLM(script)
    seen = []

    async def other():
        seen.append("ran")

    task = asyncio.create_task(other())
    assert await llm.ask("q") == "a"
    assert seen == ["ran"]
    assert script == {"q": ["a"]}
    await task


async def test_first_matching_key_wins():
    llm = m.FakeLLM({"alpha": ["first"], "beta": ["second"]})
    assert await llm.ask("alpha and beta") == "first"
