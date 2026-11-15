---
layout: module
module: 39-advanced-capstone
kind: learn
title: "Advanced capstone: multi-agent research runner"
permalink: /modules/39-advanced-capstone/
---

<div class="box key" markdown="1">

## Key learning points

- The capstone joins the second half of the course in one program: **validated data**, **retry and timeout**, **structured concurrency**, **streamed events**, **trace ids** and a **command line**.
- Build it in **layers**, bottom up: models, worker, orchestrator, events, report and CLI. Each layer can be tested alone.
- Every slow or random part is **injected**: the model (`FakeLLM`), `sleep`, the trace id. Then the whole project runs offline and tests are exact.
- Plan failure first: what is a temporary error, what is a permanent one, and what happens to the other tasks when one fails?
- A finished program is a **tool someone can run**: a clear exit code, errors on stderr, and output in a format other programs can read.

</div>

## 1. What you will build

A **research runner**. You give it a file with questions, one per line:

```text
What causes the tides?
Why is the sky blue?
Is the unreachable server up?
```

For each question the runner starts a **sub-agent**, a worker that asks a language model and validates the reply. Several workers run at once. The runner prints progress while they work, and at the end writes a report with the answers, their confidence and sources, and the questions that failed.

No real model is used. A `FakeLLM` (scripted replies) stands in for it, so the project runs offline and the tests are deterministic. If you later write a class with the same `ask(prompt)` method that calls a real API, the rest of the code does not change. That is the point of the design.

## 2. The layers

```text
  questions.txt
       |
       v
  load_tasks ----> [ResearchTask ...]            stage 5
       |
       v
  run_all / run_with_events   (TaskGroup, Semaphore, Queue)   stages 3 and 4
       |  one per task
       v
  run_worker   (timeout, retry, feedback)        stage 2
       |
       v
  llm.ask(prompt) -> text -> parse_finding -> Finding   stage 1
       |
       v
  RunResult(findings, failures) -> build_report / JSON -> stdout or file   stage 5
```

| Stage | Assignment | Main ideas | Topics used |
|---|---|---|---|
| 1 | `a1-models-fakellm` | pydantic models, parsing a model reply, a scripted fake | 30, 37 |
| 2 | `a2-worker` | timeout, retry with backoff, error feedback to the model | 27, 33, 35 |
| 3 | `a3-orchestrator` | fan-out with `TaskGroup`, partial failure, `fail_fast` | 32, 33 |
| 4 | `a4-progress-events` | async generator, `Queue`, `ContextVar` trace id | 29, 34 |
| 5 | `a5-report-cli` | report text, `argparse`, exit codes | 4, 25 |

Each assignment is **self-contained**. Stages 2 to 5 include a copy of the earlier code that they need, so you can start at any stage. If you build it as one project, put the pieces in one package, for example `research/models.py`, `worker.py`, `runner.py`, `events.py`, `report.py`, `cli.py`, and a `tests/` folder next to it.

## 3. Stage 1: data you can trust

A model returns text. The text may be valid JSON, JSON in a Markdown fence, or chat. Turn it into a typed object at the edge of your program, and fail with a clear message when it does not fit:

```python
class Finding(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    task_id: str
    answer: str = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
```

```python
try:
    Finding(task_id="q1", answer="  ", confidence=1.5)
except ValidationError as exc:
    for e in exc.errors():
        print(e["loc"], e["type"])
```

```text
('answer',) string_too_short
('confidence',) less_than_equal
```

pydantic reports **all** problems, and each has a location and a type. `parse_finding` turns them into one `BadModelOutput` message. In stage 2 that message is sent back to the model ("your previous answer was rejected: ..."), which usually repairs the answer.

`FakeLLM` is keyed by **question text**, not by call order. With many workers running at once, the order of calls is not fixed, but the question in each prompt is. Keying by text keeps the tests deterministic.

## 4. Stage 2: the worker decides what to retry

Not every error deserves a retry:

| Problem | Kind | Action |
|---|---|---|
| `TimeoutError`, `ConnectionError` | temporary | wait (exponential backoff), try again |
| `BadModelOutput` | the model can fix it | try again at once, with the error text as feedback |
| Anything else (`KeyError`, a bug) | permanent | let it propagate |
| Out of tries | give up | raise `WorkerFailed(task_id, reason)` |

`sleep` is a parameter, as in topics 35 and 37, so tests never wait. The timeout uses `asyncio.timeout`, and a test that needs a hanging model uses an `asyncio.Event` that is never set.

## 5. Stage 3: fan-out with partial failure

```python
async with asyncio.TaskGroup() as group:
    for task in tasks:
        group.create_task(run_one(task))
```

A `TaskGroup` is **structured concurrency**: the block ends only when every task has ended, and no task outlives it. Two policies are possible:

- **Collect** (default): each `run_one` catches `Exception` and stores it. The group never sees an error, and the other tasks finish. The report lists the failed tasks.
- **Fail fast**: do not catch. The first error cancels all other tasks (their `finally` blocks run) and the group raises an `ExceptionGroup`. Use `except*` to handle it:

```python
async def fail(name):
    await asyncio.sleep(0)
    raise ValueError(name)


try:
    async with asyncio.TaskGroup() as group:
        group.create_task(fail("a"))
        group.create_task(fail("b"))
except* ValueError as eg:
    print(sorted(str(e) for e in eg.exceptions))
```

```text
['a', 'b']
```

Results must come back **in task order**, not in the order of completion, so the report is stable. A `Semaphore(max_concurrency)` limits the load on the model.

## 6. Stage 4: progress events

The runner becomes an async generator. Workers run in a background task and put events into an `asyncio.Queue`. The generator takes them out and yields them, until it sees an end marker:

```python
while (item := await queue.get()) is not None:
    print("got", item)
```

If a producer task puts `0`, `1`, `2` and then `None` into the queue, this loop prints `got 0`, `got 1` and `got 2`. The same pattern with event dicts gives this output for two tasks and `max_concurrency=1`:

```text
{'type': 'started', 'task_id': 't1', 'trace_id': 'demo'}
{'type': 'finished', 'task_id': 't1', 'confidence': 0.8, 'trace_id': 'demo'}
{'type': 'started', 'task_id': 't2', 'trace_id': 'demo'}
{'type': 'failed', 'task_id': 't2', 'error': 'RuntimeError: model offline', 'trace_id': 'demo'}
{'type': 'done', 'ok': 1, 'failed': 1, 'trace_id': 'demo'}
```

Three details matter:

- The `trace_id` goes into a `ContextVar` **before** the workers are created. Tasks copy the current context when they are created, so each worker can read the id.
- If the consumer stops early (`aclose()`), the `finally` block cancels the background task and waits for it. Otherwise workers would keep running with nobody listening.
- The queue decouples the producer (workers) from the consumer (the UI). A bounded queue (`Queue(maxsize=...)`) would also add **backpressure**, so a slow consumer slows the producers.

## 7. Stage 5: the report and the command line

The last layer is plain Python: format text, parse arguments, return an **exit code**.

```text
# Research report
Questions: 3 | answered: 2 | failed: 1

## q1: What causes the tides?
Notes about: What causes the tides?
Confidence: 80%
Sources: demo://notes
...
```

This is the output of `python solution.py questions.txt` for the file at the top of this page (the full text is in the assignment). The exit code was 1, because one question failed. A script can test that code.

Design rules for the CLI: `main(argv)` takes the argument list and **returns** the code (topic 4), so tests call it directly. Errors go to stderr. Output goes to stdout, or to a file with `-o`. Machine-readable JSON is available with `--format json`.

## 8. Testing strategy

- **Unit tests** per layer with fakes: `FakeLLM` for the worker, a small `async def worker` for the orchestrator.
- **Property checks** where the exact order is not defined: with five concurrent tasks, the events of each task are in order, and `done` is last.
- **Deterministic concurrency**: use `asyncio.sleep(0)` to hand over control, and use events to make tasks wait for each other. A test with `asyncio.timeout(2)` around it fails instead of hanging.
- **One test through the CLI**: `main([...])` with `capsys` checks the whole stack.

<div class="box warn" markdown="1">

## Common mistakes

- **Building everything at once.** Finish and test one layer before the next. Debugging five untested layers together is slow.
- **Catching `Exception` everywhere.** Catch what you can handle (temporary errors, bad output). Let bugs propagate, or you will hide them.
- **Result order depends on timing.** Store results by task id and build the final list in task order.
- **Forgetting cleanup on cancel.** Put cleanup in `finally`, and `await` a cancelled task so that its cleanup runs.
- **Real `sleep` or real models in tests.** Inject them.
- **Ignoring exit codes.** A program that always returns 0 cannot be used in scripts.

</div>

<div class="box" markdown="1">

## Where this appears in AI agents

This is a miniature of a real **multi-agent** system: an orchestrator splits a job into sub-tasks, sub-agents work on them in parallel, and the orchestrator merges the results. The hard parts in production are the same as here: model replies that do not match the format, calls that time out, one failing branch among many, progress that the user can watch, and a trace id that ties all the log lines of one run together. A real model client replaces `FakeLLM`. Tool calls (topic 38) would go inside the worker.

</div>

## Try it yourself

1. Add a `--attempts N` option to the CLI and pass it to the worker. Add a test.
2. Add a per-question timeout to `research` and a `FakeLLM` entry that hangs (an `Event` that is never set). What does the report say for that question?
3. Write a second output format, `--format csv`, with the columns `task_id`, `answer`, `confidence`. Use the `csv` module (topic 18).

## Further reading

- [`asyncio.TaskGroup`](https://docs.python.org/3/library/asyncio-task.html#task-groups)
- [`asyncio.Queue`](https://docs.python.org/3/library/asyncio-queue.html)
- [`contextvars`](https://docs.python.org/3/library/contextvars.html)
- [`argparse`](https://docs.python.org/3/library/argparse.html)
- [pydantic models](https://docs.pydantic.dev/latest/concepts/models/)

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="39-advanced-capstone:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/39-advanced-capstone/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/39-advanced-capstone/assignments/' | relative_url }}).
