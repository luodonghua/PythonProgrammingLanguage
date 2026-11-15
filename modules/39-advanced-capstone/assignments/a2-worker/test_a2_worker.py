import asyncio
import json

import pytest

from practice import load

m = load(__file__)

GOOD = json.dumps({"answer": "The Moon.", "confidence": 0.9, "sources": ["wiki"]})
TASK = m.ResearchTask(id="t1", question="What causes tides?")


class RecordingSleep:
    def __init__(self):
        self.delays = []

    async def __call__(self, seconds):
        self.delays.append(seconds)


async def test_success_on_first_try():
    llm = m.FakeLLM({"tides": [GOOD]})
    sleep = RecordingSleep()
    finding = await m.run_worker(llm, TASK, sleep=sleep)
    assert finding.task_id == "t1"
    assert finding.answer == "The Moon."
    assert len(llm.prompts) == 1
    assert sleep.delays == []


async def test_invalid_reply_is_retried_with_feedback_and_no_sleep():
    llm = m.FakeLLM({"tides": ["I think it is the Moon", GOOD]})
    sleep = RecordingSleep()
    finding = await m.run_worker(llm, TASK, sleep=sleep)
    assert finding.answer == "The Moon."
    assert len(llm.prompts) == 2
    assert "rejected" not in llm.prompts[0]
    assert "rejected" in llm.prompts[1]
    assert "not valid JSON" in llm.prompts[1]
    assert sleep.delays == []


async def test_validation_error_text_reaches_the_model():
    bad = json.dumps({"answer": "x", "confidence": 7})
    llm = m.FakeLLM({"tides": [bad, GOOD]})
    await m.run_worker(llm, TASK, sleep=RecordingSleep())
    assert "confidence" in llm.prompts[1]


async def test_connection_errors_back_off_exponentially():
    llm = m.FakeLLM({"tides": [ConnectionError("offline"), ConnectionError("still offline"), GOOD]})
    sleep = RecordingSleep()
    finding = await m.run_worker(llm, TASK, attempts=3, base_delay=0.5, sleep=sleep)
    assert finding.confidence == 0.9
    assert sleep.delays == [0.5, 1.0]


async def test_gives_up_with_worker_failed_and_no_sleep_after_the_last_try():
    llm = m.FakeLLM({"tides": [ConnectionError("a"), ConnectionError("b")]})
    sleep = RecordingSleep()
    with pytest.raises(m.WorkerFailed) as info:
        await m.run_worker(llm, TASK, attempts=2, base_delay=1, sleep=sleep)
    assert info.value.task_id == "t1"
    assert info.value.reason == "ConnectionError: b"
    assert "t1" in str(info.value)
    assert sleep.delays == [1]
    assert len(llm.prompts) == 2


async def test_bad_output_every_time_fails_with_the_last_error():
    llm = m.FakeLLM({"tides": ["nope", "[1]", "still nope"]})
    with pytest.raises(m.WorkerFailed) as info:
        await m.run_worker(llm, TASK, attempts=3, sleep=RecordingSleep())
    assert info.value.reason.startswith("BadModelOutput: not valid JSON")
    assert len(llm.prompts) == 3


async def test_timeout_is_a_temporary_problem():
    class SlowThenFast:
        def __init__(self):
            self.calls = 0
            self.never = asyncio.Event()

        async def ask(self, prompt):
            self.calls += 1
            if self.calls == 1:
                await self.never.wait()  # hangs until the worker's timeout cancels it
            return GOOD

    llm = SlowThenFast()
    sleep = RecordingSleep()
    finding = await m.run_worker(llm, TASK, timeout=0.01, base_delay=2, sleep=sleep)
    assert finding.answer == "The Moon."
    assert llm.calls == 2
    assert sleep.delays == [2]


async def test_other_exceptions_propagate_at_once():
    llm = m.FakeLLM({"tides": [KeyError("bug"), GOOD]})
    sleep = RecordingSleep()
    with pytest.raises(KeyError):
        await m.run_worker(llm, TASK, sleep=sleep)
    assert len(llm.prompts) == 1
    assert sleep.delays == []


async def test_single_attempt():
    llm = m.FakeLLM({"tides": ["bad", GOOD]})
    with pytest.raises(m.WorkerFailed):
        await m.run_worker(llm, TASK, attempts=1, sleep=RecordingSleep())
    assert len(llm.prompts) == 1
