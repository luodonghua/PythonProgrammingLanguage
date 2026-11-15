"""Assignment 4: keep secrets out of logs and tag each record with a trace id.

Two logging filters:

* ``RedactingFilter`` removes secret values from messages.
* ``TraceIdFilter`` adds the id of the current request or job to every record.
  The id lives in a ``ContextVar``, so concurrent asyncio tasks each see their own.
"""

import logging
from collections.abc import Iterable
from contextvars import ContextVar

trace_id_var: ContextVar[str] = ContextVar("trace_id", default="-")


def mask_secret(value: str, visible: int = 4) -> str:
    """Hide most of a secret for display.

    * A value with at most ``2 * visible`` characters is hidden completely:
      return ``"****"``. (Showing half of a short secret leaks too much.)
    * A longer value becomes ``"****"`` followed by its last ``visible`` characters.

    >>> mask_secret("sk-1234567890abcdef")
    '****cdef'
    >>> mask_secret("short")
    '****'
    """
    if len(value) <= 2 * visible:
        return "****"
    return "****" + value[-visible:]


class RedactingFilter(logging.Filter):
    """Replace every secret in a record's message with ``"[REDACTED]"``.

    ``secrets`` is an iterable of strings. Empty strings are ignored (they would
    match everywhere). In ``filter(record)``:

    1. Get the final message with ``record.getMessage()``.
    2. Replace each secret in it with ``"[REDACTED]"``.
    3. Store the result in ``record.msg`` and set ``record.args = ()``, so
       formatters see the cleaned text. (Doing this also hides secrets that were
       passed as ``%s`` arguments.)
    4. Return ``True`` so the record is still logged.

    Replace longer secrets first, so that a secret that contains another secret
    is removed completely.
    """

    def __init__(self, secrets: Iterable[str]):
        super().__init__()
        self.secrets = sorted({s for s in secrets if s}, key=len, reverse=True)

    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        for secret in self.secrets:
            message = message.replace(secret, "[REDACTED]")
        record.msg = message
        record.args = ()
        return True


class TraceIdFilter(logging.Filter):
    """Set ``record.trace_id`` to the current value of ``trace_id_var``.

    Always return ``True``. A format string can then use ``%(trace_id)s``.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = trace_id_var.get()
        return True


if __name__ == "__main__":
    import sys

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(trace_id)s %(levelname)s %(message)s"))
    handler.addFilter(TraceIdFilter())
    handler.addFilter(RedactingFilter(["hunter2"]))
    log = logging.getLogger("demo4")
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    trace_id_var.set("req-1")
    log.info("login with password %s", "hunter2")
    print(mask_secret("sk-1234567890abcdef"))
