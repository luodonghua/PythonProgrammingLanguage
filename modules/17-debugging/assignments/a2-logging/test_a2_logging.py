import io
import logging
import uuid

import pytest

from practice import load

m = load(__file__)

ORDERS = [
    {"id": "a1", "qty": 2, "price": 2.5},
    {"id": "a2", "qty": 0, "price": 9.0},
    {"id": "a3", "qty": 1, "price": 7.5},
]


@pytest.fixture
def name():
    """A unique logger name for each test, so tests cannot affect each other."""
    return "practice." + uuid.uuid4().hex


def test_configure_logger_writes_to_the_stream(name):
    stream = io.StringIO()
    logger = m.configure_logger(name, stream)
    assert logger is logging.getLogger(name)
    logger.info("hello %s", "world")
    logger.debug("hidden")
    assert stream.getvalue() == f"INFO:{name}:hello world\n"


def test_configure_logger_level(name):
    stream = io.StringIO()
    logger = m.configure_logger(name, stream, logging.DEBUG)
    logger.debug("shown")
    logger.setLevel(logging.ERROR)
    logger.warning("hidden")
    assert stream.getvalue() == f"DEBUG:{name}:shown\n"
    assert m.configure_logger(name, io.StringIO(), logging.WARNING).level == logging.WARNING


def test_configure_logger_twice_keeps_one_handler(name):
    first, second = io.StringIO(), io.StringIO()
    m.configure_logger(name, first)
    logger = m.configure_logger(name, second)
    assert len(logger.handlers) == 1
    logger.info("once")
    assert first.getvalue() == ""
    assert second.getvalue() == f"INFO:{name}:once\n"


def records(caplog):
    return [(r.levelname, r.getMessage()) for r in caplog.records]


def test_process_orders_logs_and_returns_total(caplog):
    logger = logging.getLogger("practice.orders.main")
    with caplog.at_level(logging.DEBUG, logger=logger.name):
        total = m.process_orders(ORDERS, logger)
    assert total == 12.5
    assert records(caplog) == [
        ("INFO", "processing 3 orders"),
        ("WARNING", "skipping order a2: bad quantity 0"),
        ("INFO", "total value 12.50"),
    ]


def test_process_orders_broken_order_logs_exception(caplog):
    logger = logging.getLogger("practice.orders.broken")
    orders = [{"id": "x", "qty": 1, "price": 3.0}, {"id": "y", "qty": 1}]
    with caplog.at_level(logging.DEBUG, logger=logger.name):
        total = m.process_orders(orders, logger)
    assert total == 3.0
    assert records(caplog) == [
        ("INFO", "processing 2 orders"),
        ("ERROR", "order 2 is broken"),
        ("INFO", "total value 3.00"),
    ]
    error = caplog.records[1]
    assert error.exc_info is not None
    assert error.exc_info[0] is KeyError


def test_process_orders_uses_lazy_formatting(caplog):
    logger = logging.getLogger("practice.orders.lazy")
    with caplog.at_level(logging.DEBUG, logger=logger.name):
        m.process_orders([{"id": "z", "qty": -1, "price": 1}], logger)
    warning = [r for r in caplog.records if r.levelno == logging.WARNING][0]
    assert warning.msg == "skipping order %s: bad quantity %s"
    assert warning.args == ("z", -1)


def test_process_orders_empty(caplog):
    logger = logging.getLogger("practice.orders.empty")
    with caplog.at_level(logging.DEBUG, logger=logger.name):
        assert m.process_orders([], logger) == 0
    assert records(caplog) == [("INFO", "processing 0 orders"), ("INFO", "total value 0.00")]
