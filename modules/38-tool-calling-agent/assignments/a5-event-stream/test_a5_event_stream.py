import json

from practice import load

m = load(__file__)


class ScriptedModel:
    def __init__(self, replies):
        self.replies = list(replies)

    async def complete(self, messages):
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
    def whoami() -> str:
        return "trace=" + m.trace_id_var.get()

    return reg


async def collect(model, registry, text="go", **kwargs):
    return [event async for event in m.run_agent_events(model, registry, text, **kwargs)]


async def test_answer_without_tools_is_one_event():
    events = await collect(ScriptedModel([say("hi")]), make_registry(), trace_id="t1")
    assert events == [{"type": "final", "content": "hi", "trace_id": "t1"}]


async def test_tool_round_trip_events():
    model = ScriptedModel([ask("add", {"a": 2, "b": 3}), say("5")])
    events = await collect(model, make_registry(), trace_id="t2")
    assert events == [
        {"type": "tool_call", "name": "add", "arguments": '{"a": 2, "b": 3}', "trace_id": "t2"},
        {"type": "tool_result", "name": "add", "content": "5", "trace_id": "t2"},
        {"type": "final", "content": "5", "trace_id": "t2"},
    ]


async def test_tool_errors_are_events_not_exceptions():
    model = ScriptedModel([ask("nope", {}), say("sorry")])
    events = await collect(model, make_registry(), trace_id="t3")
    assert [e["type"] for e in events] == ["tool_call", "tool_result", "final"]
    assert events[1]["content"].startswith("error:")


async def test_tools_can_read_the_trace_id():
    model = ScriptedModel([ask("whoami", {}), say("ok")])
    events = await collect(model, make_registry(), trace_id="abc123")
    assert events[1]["content"] == "trace=abc123"


async def test_trace_id_is_generated_and_consistent():
    model = ScriptedModel([ask("add", {"a": 1, "b": 1}), say("2")])
    events = await collect(model, make_registry())
    ids = {e["trace_id"] for e in events}
    assert len(ids) == 1
    (generated,) = ids
    assert isinstance(generated, str) and len(generated) == 8


async def test_two_runs_get_different_generated_ids():
    first = await collect(ScriptedModel([say("a")]), make_registry())
    second = await collect(ScriptedModel([say("b")]), make_registry())
    assert first[0]["trace_id"] != second[0]["trace_id"]


async def test_context_variable_is_restored_after_the_run():
    assert m.trace_id_var.get() == "-"
    events = await collect(ScriptedModel([say("a")]), make_registry(), trace_id="temp")
    assert events[0]["trace_id"] == "temp"
    assert m.trace_id_var.get() == "-"


async def test_max_steps_gives_an_error_event():
    model = ScriptedModel([ask("add", {"a": 1, "b": 1}, id=str(i)) for i in range(5)])
    events = await collect(model, make_registry(), max_steps=2, trace_id="t4")
    assert events[-1] == {"type": "error", "content": "no final answer after 2 steps", "trace_id": "t4"}
    assert [e["type"] for e in events[:-1]] == ["tool_call", "tool_result", "tool_call", "tool_result"]


async def test_events_arrive_one_by_one_and_the_run_can_stop_early():
    model = ScriptedModel([ask("add", {"a": 1, "b": 1}), say("2")])
    stream = m.run_agent_events(model, make_registry(), "go", trace_id="t5")
    first = await anext(stream)
    assert first["type"] == "tool_call"
    await stream.aclose()
    assert model.replies  # the second reply was never requested
