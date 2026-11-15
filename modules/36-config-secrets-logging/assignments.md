---
layout: module
module: 36-config-secrets-logging
kind: assignments
title: Config, secrets and logging - assignments
permalink: /modules/36-config-secrets-logging/assignments/
---
Four tasks on the plumbing every real program needs: read settings, keep secrets safe, and write logs that people and tools can use. Everything runs offline, and nothing reads your real environment or files.

{% include practice-setup.md %}

No extra libraries are needed. You use `logging`, `dataclasses`, `contextvars` and `json` from the standard library. The tests never read your real `os.environ`. They pass dictionaries.

Run all tests for this topic:

```bash
uv run pytest modules/36-config-secrets-logging
```

---

<div class="assignment" markdown="1">

## Assignment 1: Parse a .env file

**Goal:** Turn the text of a `.env` file into a dict. Handle comments, an `export` prefix, quotes, inline comments and bad lines (with line numbers). Practises string methods and clear error messages.

**Files:** [`starter.py`]({{ 'modules/36-config-secrets-logging/assignments/a1-dotenv/starter.py' | relative_url }}), test file `test_a1_dotenv.py` in the same folder.

```python
{% include_relative assignments/a1-dotenv/starter.py %}
```

Run: `uv run pytest modules/36-config-secrets-logging/assignments/a1-dotenv`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-dotenv/solution.py %}
```

`partition("=")` splits at the first `=` only, so values may contain `=`. A quoted value is taken as it is. Only an unquoted value loses its inline comment, which the regular expression `(?:^|\s)#` finds (a `#` at the start or after whitespace, so `color#fff` is safe).
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Load and validate config

**Goal:** Build a frozen `Config` from an environment mapping, convert types, apply defaults and report all problems in one `ConfigError`. The API key must stay out of `repr`.

**Files:** [`starter.py`]({{ 'modules/36-config-secrets-logging/assignments/a2-load-config/starter.py' | relative_url }}), test file `test_a2_load_config.py` in the same folder.

```python
{% include_relative assignments/a2-load-config/starter.py %}
```

Run: `uv run pytest modules/36-config-secrets-logging/assignments/a2-load-config`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-load-config/solution.py %}
```

Each variable is checked in its own `try` block. A problem is added to a list, and the function raises once at the end. `field(repr=False)` keeps the secret out of the printed form, and `not timeout > 0` also rejects `nan`.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: A JSON log formatter

**Goal:** Write a `logging.Formatter` that outputs one JSON object per line with time, level, logger, message, extra fields and the traceback. Add a helper that builds a ready logger.

**Files:** [`starter.py`]({{ 'modules/36-config-secrets-logging/assignments/a3-json-logs/starter.py' | relative_url }}), test file `test_a3_json_logs.py` in the same folder.

```python
{% include_relative assignments/a3-json-logs/starter.py %}
```

Run: `uv run pytest modules/36-config-secrets-logging/assignments/a3-json-logs`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-json-logs/solution.py %}
```

Extra fields are the record attributes that a plain `LogRecord` does not have, so the formatter compares `vars(record)` with a set of standard names. `json.dumps(..., default=str)` handles values JSON cannot encode. The helper removes old handlers first, so repeated setup does not duplicate output.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Redact secrets and add a trace id

**Goal:** Write `mask_secret`, a filter that replaces secrets in log messages, and a filter that adds the current `ContextVar` trace id to each record. Practises filters and `contextvars` with asyncio tasks.

**Files:** [`starter.py`]({{ 'modules/36-config-secrets-logging/assignments/a4-redact-trace/starter.py' | relative_url }}), test file `test_a4_redact_trace.py` in the same folder.

```python
{% include_relative assignments/a4-redact-trace/starter.py %}
```

Run: `uv run pytest modules/36-config-secrets-logging/assignments/a4-redact-trace`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-redact-trace/solution.py %}
```

The redacting filter uses `record.getMessage()`, so secrets that were passed as `%s` arguments are removed too, and it then clears `record.args`. Longer secrets are replaced first. The trace filter reads the `ContextVar` when the record is created, so each asyncio task sees its own id.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="36-config-secrets-logging:assignments"> I have finished the assignments</label></li>
</ul>
