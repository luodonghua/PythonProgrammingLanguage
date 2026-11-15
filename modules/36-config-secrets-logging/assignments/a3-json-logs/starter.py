"""Assignment 3: write log records as one JSON object per line.

Programs that run on servers write logs that other programs read (search tools,
dashboards). One JSON object per line is easy for them to parse.
"""

import json
import logging
from datetime import UTC, datetime
from typing import TextIO

# Attribute names every LogRecord has. Anything else was added with ``extra=``.
STANDARD_ATTRS = set(vars(logging.LogRecord("", 0, "", 0, "", (), None))) | {
    "message",
    "asctime",
    "taskName",
}


class JsonFormatter(logging.Formatter):
    """Format a ``LogRecord`` as a JSON string (one line, no trailing newline).

    The object has these keys, in this order:

    * ``"time"``: ``record.created`` as an ISO 8601 UTC string, for example
      ``"2024-05-01T12:00:00+00:00"`` (use ``datetime.fromtimestamp(..., UTC)``).
    * ``"level"``: ``record.levelname``.
    * ``"logger"``: ``record.name``.
    * ``"message"``: ``record.getMessage()`` (the message with its arguments filled in).
    * every extra attribute passed with ``logger.info(..., extra={...})``
      (any attribute whose name is not in ``STANDARD_ATTRS``).
    * ``"exc"``: only when the record has exception info, the formatted
      traceback text from ``self.formatException(record.exc_info)``.

    Values that JSON cannot encode are converted with ``str`` (``default=str``).
    """

    def format(self, record: logging.LogRecord) -> str:
        # TODO: build a dict with the keys listed above, then json.dumps it.
        ...


def make_json_logger(name: str, stream: TextIO, level: int = logging.INFO) -> logging.Logger:
    """Return the logger called ``name`` set up to write JSON lines to ``stream``.

    * Remove any handlers the logger already has, so calling this twice does
      not print every message twice.
    * Add one ``logging.StreamHandler(stream)`` that uses ``JsonFormatter``.
    * Set the logger level to ``level`` and set ``propagate = False`` (so the
      root logger does not print the record a second time).
    """
    # TODO: get the logger, reset its handlers, add the JSON handler, set level and propagate.
    ...


if __name__ == "__main__":
    import sys

    log = make_json_logger("demo", sys.stdout)
    log.info("started %s", "worker-1", extra={"job_id": 42})
    try:
        1 / 0
    except ZeroDivisionError:
        log.exception("job failed")
