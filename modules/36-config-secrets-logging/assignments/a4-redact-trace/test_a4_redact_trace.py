import asyncio
import io
import logging

import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("value", "visible", "expected"),
    [
        ("sk-1234567890abcdef", 4, "****cdef"),
        ("short", 4, "****"),
        ("12345678", 4, "****"),
        ("123456789", 4, "****6789"),
        ("", 4, "****"),
        ("abcdefghij", 2, "****ij"),
    ],
)
def test_mask_secret(value, visible, expected):
    assert m.mask_secret(value, visible) == expected


def make_logger(name, *filters, fmt="%(trace_id)s|%(message)s"):
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter(fmt))
    for f in filters:
        handler.addFilter(f)
    logger = logging.getLogger(name)
    logger.handlers = [handler]
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    return logger, stream


def test_redacts_secret_in_message():
    logger, stream = make_logger("a4.msg", m.RedactingFilter(["hunter2"]), fmt="%(message)s")
    logger.info("password is hunter2, really hunter2")
    assert stream.getvalue() == "password is [REDACTED], really [REDACTED]\n"


def test_redacts_secret_in_arguments():
    logger, stream = make_logger("a4.args", m.RedactingFilter(["tok-123"]), fmt="%(message)s")
    logger.info("token=%s user=%s", "tok-123", "ann")
    assert stream.getvalue() == "token=[REDACTED] user=ann\n"


def test_longer_secret_is_removed_first():
    logger, stream = make_logger("a4.long", m.RedactingFilter(["abc", "abcdef"]), fmt="%(message)s")
    logger.info("key abcdef end")
    assert stream.getvalue() == "key [REDACTED] end\n"


def test_empty_secret_is_ignored_and_record_is_kept():
    logger, stream = make_logger("a4.empty", m.RedactingFilter(["", "x-secret"]), fmt="%(message)s")
    logger.warning("nothing to hide")
    assert stream.getvalue() == "nothing to hide\n"


def test_filter_returns_true():
    record = logging.LogRecord("n", logging.INFO, __file__, 1, "msg %s", ("a",), None)
    assert m.RedactingFilter(["a"]).filter(record) is True
    assert record.getMessage() == "msg [REDACTED]"


def test_trace_id_default_and_set():
    logger, stream = make_logger("a4.trace", m.TraceIdFilter())
    logger.info("one")
    token = m.trace_id_var.set("req-9")
    try:
        logger.info("two")
    finally:
        m.trace_id_var.reset(token)
    assert stream.getvalue().splitlines() == ["-|one", "req-9|two"]


async def test_trace_id_is_separate_for_each_task():
    logger, stream = make_logger("a4.tasks", m.TraceIdFilter())

    async def job(name):
        m.trace_id_var.set(name)
        await asyncio.sleep(0)
        logger.info("working")
        await asyncio.sleep(0)
        logger.info("done")

    await asyncio.gather(job("A"), job("B"))
    lines = stream.getvalue().splitlines()
    assert sorted(lines) == ["A|done", "A|working", "B|done", "B|working"]
    assert m.trace_id_var.get() == "-"


def test_both_filters_together():
    logger, stream = make_logger("a4.both", m.TraceIdFilter(), m.RedactingFilter(["s3cret"]))
    token = m.trace_id_var.set("t1")
    try:
        logger.info("login s3cret")
    finally:
        m.trace_id_var.reset(token)
    assert stream.getvalue() == "t1|login [REDACTED]\n"
