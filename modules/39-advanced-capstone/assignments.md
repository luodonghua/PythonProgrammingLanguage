---
layout: module
module: 39-advanced-capstone
kind: assignments
title: Advanced capstone: multi-agent research runner - assignments
permalink: /modules/39-advanced-capstone/assignments/
---
Five stages of one project: a multi-agent research runner. Stage by stage you build validated data models and a scripted fake model, a worker with retry and timeout, a fan-out orchestrator that survives partial failures, a stream of progress events with trace ids, and finally the report and the command line. Everything runs offline and the tests are deterministic.

{% include practice-setup.md %}

This topic uses `pydantic`, which the project already lists. Each stage is self-contained: `starter.py` of stages 2 to 5 includes the finished code of the earlier stages that it needs, so you can start at any stage, or build the stages in order as one project. The tests are `async def` functions where needed. The project runs `pytest-asyncio` in auto mode, so they need no decorator. Stage 5 comes with a data file, `questions.txt`, and you can run it yourself with `python solution.py questions.txt` from that folder.

Run all tests for this topic:

```bash
uv run pytest modules/39-advanced-capstone
```

---

<div class="assignment" markdown="1">

## Assignment 1: Models, parsing and a fake model

**Goal:** Write the pydantic models `ResearchTask` and `Finding`, a `parse_finding` function that cleans and validates a model's text reply, and a scripted `FakeLLM` keyed by question text. Practises validation, error messages and test doubles.

**Files:** [`starter.py`]({{ 'modules/39-advanced-capstone/assignments/a1-models-fakellm/starter.py' | relative_url }}), test file `test_a1_models_fakellm.py` in the same folder.

```python
{% include_relative assignments/a1-models-fakellm/starter.py %}
```

Run: `uv run pytest modules/39-advanced-capstone/assignments/a1-models-fakellm`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-models-fakellm/solution.py %}
```

`str_strip_whitespace` strips before the length checks, and a `field_validator` cleans `sources` with `dict.fromkeys`, which removes duplicates and keeps the order. `parse_finding` turns JSON and validation problems into one `BadModelOutput`, so a caller can show the text to the model. `FakeLLM` finds its script by checking which key occurs in the prompt.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Worker with retry, timeout and feedback

**Goal:** Write `run_worker`: ask the model, validate the reply, retry bad output at once with feedback, retry timeouts and connection errors with exponential backoff, and give up with `WorkerFailed`. Practises `asyncio.timeout`, retry design and dependency injection of `sleep`.

**Files:** [`starter.py`]({{ 'modules/39-advanced-capstone/assignments/a2-worker/starter.py' | relative_url }}), test file `test_a2_worker.py` in the same folder.

```python
{% include_relative assignments/a2-worker/starter.py %}
```

Run: `uv run pytest modules/39-advanced-capstone/assignments/a2-worker`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-worker/solution.py %}
```

Each kind of error has its own `except` clause. Bad output keeps its message as feedback for the next prompt and does not sleep. Temporary errors sleep `base_delay * 2 ** (n - 1)`, but not after the last try. Other exceptions are not caught, so bugs stay visible.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Fan-out orchestrator

**Goal:** Write `run_all`, which runs one worker per task in a `TaskGroup` with a concurrency limit, keeps the task order, collects failures, and can stop everything at the first error with `fail_fast=True`.

**Files:** [`starter.py`]({{ 'modules/39-advanced-capstone/assignments/a3-orchestrator/starter.py' | relative_url }}), test file `test_a3_orchestrator.py` in the same folder.

```python
{% include_relative assignments/a3-orchestrator/starter.py %}
```

Run: `uv run pytest modules/39-advanced-capstone/assignments/a3-orchestrator`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-orchestrator/solution.py %}
```

Outcomes are stored by task id while the workers run. After the group has finished, the result is built by going through the tasks in order. In collect mode each task catches its own exception. In fail-fast mode the exception goes to the `TaskGroup`, which cancels the rest and raises an `ExceptionGroup`.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Streamed progress events with trace ids

**Goal:** Turn the runner into an async generator that yields `started`, `finished`, `failed` and `done` events. Each event has a trace id, and workers can read the id from a `ContextVar`. Closing the stream early must cancel the workers.

**Files:** [`starter.py`]({{ 'modules/39-advanced-capstone/assignments/a4-progress-events/starter.py' | relative_url }}), test file `test_a4_progress_events.py` in the same folder.

```python
{% include_relative assignments/a4-progress-events/starter.py %}
```

Run: `uv run pytest modules/39-advanced-capstone/assignments/a4-progress-events`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-progress-events/solution.py %}
```

A background task runs the `TaskGroup` and puts events into an `asyncio.Queue`. The generator yields from the queue until it takes the `None` marker. The `finally` block cancels and awaits the background task, and resets the `ContextVar`. The variable is set before the task is created, because a new task copies the current context.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 5: Report and command line

**Goal:** Finish the project: read questions from a file, format the report, and write `main(argv)` with `argparse`, a JSON option, an output file and meaningful exit codes. The pipeline from the earlier stages is provided.

**Files:** [`starter.py`]({{ 'modules/39-advanced-capstone/assignments/a5-report-cli/starter.py' | relative_url }}), test file `test_a5_report_cli.py` in the same folder. The data file `questions.txt` in the same folder has three demo questions. The third one makes the demo model fail on purpose.

```python
{% include_relative assignments/a5-report-cli/starter.py %}
```

Run: `uv run pytest modules/39-advanced-capstone/assignments/a5-report-cli`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a5-report-cli/solution.py %}
```

`main` returns the exit code instead of calling `sys.exit`, so tests can call it directly and read stdout and stderr with `capsys`. Bad input gives 2 and a message on stderr. Failed tasks give 1. `build_report` goes through the tasks in order and looks up each one in a dict of findings.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="39-advanced-capstone:assignments"> I have finished the assignments</label></li>
</ul>
