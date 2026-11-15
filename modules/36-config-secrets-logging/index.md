---
layout: module
module: 36-config-secrets-logging
kind: learn
title: Config, secrets and logging
permalink: /modules/36-config-secrets-logging/
---

<div class="box key" markdown="1">

## Key learning points

- Settings come from **outside** the code: environment variables or a `.env` file. Environment values are always strings, so convert and validate them once, at start-up.
- Put the checked settings into a **frozen dataclass** and pass it around. Report **all** problems at once.
- A **secret** (key, password, token) never goes into source code, `print`, logs or `repr`. Hide it with `field(repr=False)`, `SecretStr` or masking.
- Use the `logging` module, not `print`: loggers have names and **levels**, handlers decide where records go, and formatters decide how they look.
- A **filter** can add fields to every record (such as a `trace_id` read from a `ContextVar`) or remove secrets.

</div>

A program that runs on your laptop, in a test and on a server needs different settings in each place. A program that talks to other services needs secrets. When something goes wrong at 3 a.m., logs are all you have. This page covers all three.

## 1. Environment variables

`os.environ` behaves like a dict of strings.

```python
import os

os.environ["APP_PORT"] = "9000"
port = int(os.environ.get("APP_PORT", "8000"))
print(port, type(port).__name__)
print(os.environ.get("MISSING"))
try:
    os.environ["MISSING"]
except KeyError as e:
    print("KeyError", e)
```

```text
9000 int
None
KeyError 'MISSING'
```

- `os.environ.get(name, default)` returns the default when the variable is missing. `os.environ[name]` raises `KeyError`.
- Values are **always `str`**. `"false"` is a non-empty string, so `bool("false")` is `True`. Convert on purpose.
- The shell sets them: `APP_PORT=9000 python app.py` on Linux and macOS.

## 2. A validated, frozen config

Read the environment in one place and build a typed object. Later code never touches `os.environ` again.

```python
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Config:
    api_key: str = field(repr=False)   # never shown by repr()
    port: int = 8000


cfg = Config("sk-abc123456789", 9000)
print(cfg)
```

```text
Config(port=9000)
```

- `frozen=True` makes the object read-only (`cfg.port = 1` raises `FrozenInstanceError`). Nothing can change a setting by accident.
- A function `load_config(env: Mapping[str, str]) -> Config` that takes the mapping as a **parameter** is easy to test: pass a plain dict. In the real program call `load_config(os.environ)`.
- Collect every problem in a list and raise one error at the end. A user who must fix five variables one run at a time gets annoyed.

Topic 30 showed that `pydantic` can do the conversion and validation for you. Pydantic's `SecretStr` type hides a value when printed:

```python
from pydantic import BaseModel, SecretStr


class Settings(BaseModel):
    api_key: SecretStr


s = Settings(api_key="sk-abc123456789")
print(s)
print(s.api_key.get_secret_value()[:5])
```

```text
api_key=SecretStr('**********')
sk-ab
```

You must call `get_secret_value()` on purpose to read the real value.

## 3. .env files

A `.env` file stores settings for one machine as `NAME=value` lines. It is **not committed to git** (add it to `.gitignore`). You may commit a `.env.example` with fake values to show which names exist. The format is simple enough to parse yourself, which is the first assignment:

```text
# database
DB_HOST=localhost
DB_NAME="my app"
DEBUG=true   # dev only
```

Rules to decide: how to treat comments, quotes, spaces around `=`, and bad lines. The usual choice is to fail with the line number on a bad line. Tools such as `python-dotenv` or `pydantic-settings` do this for you, but you now know what they do.

## 4. Secret hygiene

- Keep secrets out of source code and out of git. Read them from the environment or a secrets manager.
- Never log or print a secret. Also avoid logging whole request headers or whole config objects that contain one.
- Show at most the last few characters (`****cdef`) when you must identify a key. Hide short secrets completely.
- If a secret leaks, **rotate** it (create a new one and disable the old one). Deleting the commit is not enough, because copies exist.

A logging **filter** is a safety net. It cannot know every secret, so it does not replace care:

```python
class RedactingFilter(logging.Filter):
    def __init__(self, secrets):
        super().__init__()
        self.secrets = [s for s in secrets if s]

    def filter(self, record):
        message = record.getMessage()
        for secret in self.secrets:
            message = message.replace(secret, "[REDACTED]")
        record.msg, record.args = message, ()
        return True
```

## 5. Logging basics

```python
import logging
import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("jobs.runner")
log.debug("hidden")
log.info("started %s jobs", 3)
log.warning("slow job: %s", "backup")
try:
    1 / 0
except ZeroDivisionError:
    log.exception("job failed")
```

```text
18:49:49 INFO jobs.runner: started 3 jobs
18:49:49 WARNING jobs.runner: slow job: backup
18:49:49 ERROR jobs.runner: job failed
Traceback (most recent call last):
  ...
ZeroDivisionError: division by zero
```

(The time on your computer will differ.)

- **Levels**, from low to high: `DEBUG` (10), `INFO` (20), `WARNING` (30), `ERROR` (40), `CRITICAL` (50). A logger drops records below its level, so `log.debug("hidden")` printed nothing.
- `logging.getLogger("jobs.runner")` gives a logger by name. Names with dots form a tree: `jobs.runner` is a child of `jobs`. Use `getLogger(__name__)` in each module.
- Pass values as **arguments** (`"started %s jobs", 3`), not with an f-string. The text is built only if the record is really emitted.
- `log.exception(...)` inside `except` logs at `ERROR` level and adds the traceback.
- A **handler** sends records somewhere (console, file). A **formatter** turns a record into text. Libraries only create loggers. The application configures handlers once, at start-up.

## 6. JSON logs and trace ids

Plain text is good for people. Machines prefer **one JSON object per line**. A custom `logging.Formatter` builds it from the record: time, level, logger name, message, plus any fields passed with `extra={"job_id": 42}`.

To follow one request through many log lines, give each request an id and put it on every record. A global variable would be shared by all concurrent tasks. A `ContextVar` (topic 29) holds a separate value for each task, and a filter copies it onto the record:

```python
import logging
import sys
from contextvars import ContextVar

trace_id = ContextVar("trace_id", default="-")


class TraceFilter(logging.Filter):
    def filter(self, record):
        record.trace_id = trace_id.get()
        return True


handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(trace_id)s %(levelname)s %(message)s"))
handler.addFilter(TraceFilter())
log = logging.getLogger("x")
log.addHandler(handler)
log.setLevel(logging.INFO)
log.info("a")
trace_id.set("r1")
log.debug("b")
log.warning("c %s", 5)
```

```text
- INFO a
r1 WARNING c 5
```

`log.debug("b")` is below `INFO`, so it disappears. Returning `True` from a filter keeps the record, `False` drops it.

<div class="box warn" markdown="1">

## Common mistakes

- **Committing `.env` or a key.** Add `.env` to `.gitignore` before the first commit. A key in git history must be rotated.
- **Forgetting that environment values are strings.** `os.environ.get("PORT", 8000)` gives `"9000"` or `8000`, two different types. Convert once, in the config loader.
- **`bool("false")`.** Any non-empty string is true. Compare against known words.
- **Logging with f-strings or `print`.** Use `log.info("x=%s", x)`. `print` has no levels, no names and no way to switch it off.
- **Calling `basicConfig` or adding handlers in library code.** Doing it twice prints each message twice. Configure logging once, in the application.

</div>

<div class="box" markdown="1">

## Where this appears in AI agents

Agents need API keys for the model provider and for tools, so they load config from the environment and must never print it. A run that calls a model, then three tools, then the model again needs a `trace_id` on every log line to reconstruct what happened. Many agents log JSON so that a log tool can group the lines of one run. Redaction matters because prompts, tool arguments and tool results can contain secrets that a user typed.

```python
log.info("tool call", extra={"tool": "search", "trace_id": trace_id.get()})
```

</div>

## Try it yourself

1. Write `load_config(env)` for two settings, `HOST` (default `"localhost"`) and `PORT` (an int). Call it with a plain dict, then with `os.environ`.
2. Make a logger that writes at `DEBUG` level to the console and at `WARNING` level to a file named `app.log`. (Hint: two handlers, each with its own level.)
3. Write a filter that drops every record whose message contains the word `password`. What does `filter` return in that case?

## Further reading

- [`os.environ`](https://docs.python.org/3/library/os.html#os.environ)
- [`logging` module](https://docs.python.org/3/library/logging.html)
- [Logging HOWTO](https://docs.python.org/3/howto/logging.html)

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="36-config-secrets-logging:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/36-config-secrets-logging/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/36-config-secrets-logging/assignments/' | relative_url }}).
