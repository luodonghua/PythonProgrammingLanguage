"""Assignment 2: Replace print with logging.

Part 1: configure_logger builds a logger that writes to a stream.
Part 2: process_orders reports what it does through a logger.
"""

import logging


def configure_logger(name: str, stream, level: int = logging.INFO) -> logging.Logger:
    """Return the logger called `name`, set up to write to `stream`.

    * The logger's level is `level`.
    * It has exactly ONE handler, a logging.StreamHandler(stream), with the format
      "%(levelname)s:%(name)s:%(message)s".
    * Calling configure_logger again with the same name must not add a second
      handler (otherwise every message would be written twice). Replace the
      existing handlers instead.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(message)s"))
    logger.addHandler(handler)
    return logger


def process_orders(orders: list[dict], logger: logging.Logger) -> float:
    """Return the total value of the valid orders and log what happens.

    Each order is a dict with keys "id", "qty" and "price"; its value is qty * price.

    Log with the given `logger`, using %-style arguments (logger.info("... %s", x)),
    not f-strings:
      * first, INFO:    "processing N orders"          (N = len(orders))
      * an order whose qty is 0 or negative is skipped, WARNING:
                        "skipping order <id>: bad quantity <qty>"
      * an order that lacks a key (KeyError) is skipped; use logger.exception
        (ERROR level, records the traceback) with the message "order <n> is broken"
        where <n> is its position in the list, counting from 1
      * last, INFO:     "total value 12.50"            (two decimals)
    """
    logger.info("processing %d orders", len(orders))
    total = 0.0
    for position, order in enumerate(orders, start=1):
        try:
            qty = order["qty"]
            price = order["price"]
            order_id = order["id"]
        except KeyError:
            logger.exception("order %d is broken", position)
            continue
        if qty <= 0:
            logger.warning("skipping order %s: bad quantity %s", order_id, qty)
            continue
        total += qty * price
    logger.info("total value %.2f", total)
    return total


if __name__ == "__main__":
    import sys

    log = configure_logger("orders-demo", sys.stdout, logging.DEBUG)
    orders = [{"id": "a1", "qty": 2, "price": 2.5}, {"id": "a2", "qty": 0, "price": 9}]
    print(process_orders(orders, log))
