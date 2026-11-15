import json

import pytest

from practice import load

m = load(__file__)


class ScriptedModel:
    """The test's own fake model: replays replies and keeps a copy of every request."""

    def __init__(self, replies):
        self.replies = list(replies)
        self.requests = []

    async def complete(self, messages):
        self.requests.append(list(messages))
        return self.replies.pop(0)


def ask(name, arguments, id="c1"):
    return {"role": "assistant", "content": None, "tool_calls": [{"id": id, "name": name, "arguments": json.dumps(arguments)}]}


def say(text):
    return {"role": "assistant", "content": text}


def make_registry():
    reg = m.ToolRegistry()

    @reg.tool
    def add(a: int, b: int) -> int:
        return a + b

    @reg.tool
    def shout(text: str) -> str:
        return text.upper()

    return reg


async def test_answer_without_tools():
    model = ScriptedModel([say("Hello!")])
    result = await m.run_agent(model, make_registry(), "Hi")
    assert result.answer == "Hello!"
    assert result.steps == 1
    assert result.messages == [{"role": "user", "content": "Hi"}, say("Hello!")]


async def test_one_tool_round_trip():
    model = ScriptedModel([ask("add", {"a": 2, "b": 3}), say("The sum is 5")])
    result = await m.run_agent(model, make_registry(), "2+3?")
    assert result.answer == "The sum is 5"
    assert result.steps == 2
    roles = [msg["role"] for msg in result.messages]
    assert roles == ["user", "assistant", "tool", "assistant"]
    assert result.messages[2] == {"role": "tool", "tool_call_id": "c1", "content": "5"}


async def test_model_sees_the_tool_result_on_the_next_step():
    model = ScriptedModel([ask("add", {"a": 1, "b": 1}), say("two")])
    await m.run_agent(model, make_registry(), "1+1?")
    first_request, second_request = model.requests
    assert [msg["role"] for msg in first_request] == ["user"]
    assert [msg["role"] for msg in second_request] == ["user", "assistant", "tool"]
    assert second_request[-1]["content"] == "2"


async def test_system_message_comes_first():
    model = ScriptedModel([say("ok")])
    result = await m.run_agent(model, make_registry(), "Hi", system="Be brief.")
    assert result.messages[0] == {"role": "system", "content": "Be brief."}
    assert result.messages[1] == {"role": "user", "content": "Hi"}


async def test_several_tool_calls_in_one_reply_run_in_order():
    reply = {
        "role": "assistant",
        "content": None,
        "tool_calls": [
            {"id": "a", "name": "shout", "arguments": '{"text": "hi"}'},
            {"id": "b", "name": "add", "arguments": '{"a": 1, "b": 2}'},
        ],
    }
    model = ScriptedModel([reply, say("done")])
    result = await m.run_agent(model, make_registry(), "go")
    tool_messages = [msg for msg in result.messages if msg["role"] == "tool"]
    assert [(t["tool_call_id"], t["content"]) for t in tool_messages] == [("a", "HI"), ("b", "3")]


async def test_a_tool_error_is_given_to_the_model_which_can_recover():
    model = ScriptedModel(
        [
            ask("add", {"a": "many", "b": 2}, id="bad"),
            ask("add", {"a": 4, "b": 2}, id="good"),
            say("It is 6"),
        ]
    )
    result = await m.run_agent(model, make_registry(), "sum?")
    assert result.answer == "It is 6"
    assert result.steps == 3
    tool_messages = [msg for msg in result.messages if msg["role"] == "tool"]
    assert tool_messages[0]["content"].startswith("error:")
    assert tool_messages[1]["content"] == "6"


async def test_unknown_tool_does_not_stop_the_loop():
    model = ScriptedModel([ask("teleport", {}), say("I cannot do that")])
    result = await m.run_agent(model, make_registry(), "go")
    assert result.answer == "I cannot do that"
    assert result.messages[2]["content"].startswith("error:")


async def test_max_steps_stops_a_model_that_never_answers():
    model = ScriptedModel([ask("add", {"a": 1, "b": 1}, id=f"c{i}") for i in range(10)])
    with pytest.raises(m.MaxStepsError, match="max_steps=3"):
        await m.run_agent(model, make_registry(), "loop", max_steps=3)
    assert len(model.requests) == 3


async def test_final_answer_on_the_last_allowed_step_is_accepted():
    model = ScriptedModel([ask("add", {"a": 1, "b": 1}), say("done")])
    result = await m.run_agent(model, make_registry(), "go", max_steps=2)
    assert result.answer == "done"
    assert result.steps == 2


@pytest.mark.parametrize("reply", [{"role": "assistant", "content": "x", "tool_calls": []}, {"role": "assistant", "content": "x", "tool_calls": None}])
async def test_empty_tool_calls_count_as_a_final_answer(reply):
    result = await m.run_agent(ScriptedModel([reply]), make_registry(), "go")
    assert result.answer == "x"


async def test_missing_content_gives_empty_answer():
    result = await m.run_agent(ScriptedModel([{"role": "assistant", "content": None}]), make_registry(), "go")
    assert result.answer == ""
