import io
import json
import logging

from practice import load

m = load(__file__)


def make_record(msg="hello", args=(), exc_info=None, extra=None):
    record = logging.LogRecord("app.jobs", logging.WARNING, __file__, 10, msg, args, exc_info)
    record.created = 1714564800.0  # 2024-05-01T12:00:00 UTC
    for key, value in (extra or {}).items():
        setattr(record, key, value)
    return record


def test_basic_fields_and_order():
    line = m.JsonFormatter().format(make_record("hello %s", ("world",)))
    data = json.loads(line)
    assert data == {
        "time": "2024-05-01T12:00:00+00:00",
        "level": "WARNING",
        "logger": "app.jobs",
        "message": "hello world",
    }
    assert list(data) == ["time", "level", "logger", "message"]


def test_output_is_a_single_line():
    line = m.JsonFormatter().format(make_record("two\nlines"))
    assert "\n" not in line
    assert json.loads(line)["message"] == "two\nlines"


def test_extra_fields_are_included():
    record = make_record(extra={"job_id": 42, "tags": ["a", "b"]})
    data = json.loads(m.JsonFormatter().format(record))
    assert data["job_id"] == 42
    assert data["tags"] == ["a", "b"]
    assert "args" not in data and "msg" not in data and "lineno" not in data


def test_unserialisable_extra_uses_str():
    record = make_record(extra={"where": {1, 2}})
    data = json.loads(m.JsonFormatter().format(record))
    assert data["where"] == str({1, 2})


def test_exception_text_is_added():
    try:
        raise ValueError("bad value")
    except ValueError:
        import sys

        record = make_record("failed", exc_info=sys.exc_info())
    data = json.loads(m.JsonFormatter().format(record))
    assert "Traceback" in data["exc"]
    assert "ValueError: bad value" in data["exc"]


def test_no_exc_key_without_exception():
    data = json.loads(m.JsonFormatter().format(make_record()))
    assert "exc" not in data


def test_make_json_logger_writes_json_lines():
    stream = io.StringIO()
    logger = m.make_json_logger("test.a3.lines", stream)
    logger.info("started %s", "w1", extra={"job_id": 7})
    logger.debug("not shown at INFO level")
    lines = stream.getvalue().splitlines()
    assert len(lines) == 1
    data = json.loads(lines[0])
    assert data["message"] == "started w1"
    assert data["job_id"] == 7
    assert data["level"] == "INFO"
    assert data["logger"] == "test.a3.lines"


def test_make_json_logger_twice_does_not_duplicate():
    first, second = io.StringIO(), io.StringIO()
    m.make_json_logger("test.a3.twice", first)
    logger = m.make_json_logger("test.a3.twice", second, level=logging.DEBUG)
    logger.debug("once")
    assert first.getvalue() == ""
    assert len(second.getvalue().splitlines()) == 1
    assert len(logger.handlers) == 1


def test_logger_does_not_propagate():
    logger = m.make_json_logger("test.a3.prop", io.StringIO())
    assert logger.propagate is False
    assert logger.level == logging.INFO
