"""Assignment 3: functools.partial.

Pre-fill arguments of a general function to get small, configured functions.
"""

from functools import partial


def log(sink: list, level: str, prefix: str, message: str) -> None:
    """Append the text f"[{level}] {prefix}{message}" to the list `sink`."""
    sink.append(f"[{level}] {prefix}{message}")


def make_loggers(sink: list, prefix: str = "") -> tuple:
    """Return three functions (debug, info, error) built with partial.

    Each takes only `message`. Calling info("started") appends
    "[INFO] <prefix>started" to `sink` (levels are "DEBUG", "INFO", "ERROR").
    Build them with partial(log, sink, "INFO", prefix) and so on.
    """
    return (
        partial(log, sink, "DEBUG", prefix),
        partial(log, sink, "INFO", prefix),
        partial(log, sink, "ERROR", prefix),
    )


def make_parsers() -> dict:
    """Return a dict of number parsers built with partial(int, base=...):

        "bin" (base 2), "oct" (base 8), "hex" (base 16)

    make_parsers()["hex"]("ff") -> 255
    """
    return {
        "bin": partial(int, base=2),
        "oct": partial(int, base=8),
        "hex": partial(int, base=16),
    }


def my_partial(func, /, *fixed_args, **fixed_kwargs):
    """Write your own version of functools.partial (using a closure).

    Return a function `call(*args, **kwargs)` that calls
    func(*fixed_args, *args, **{**fixed_kwargs, **kwargs}).
    Keyword arguments given later override the fixed ones.

        double = my_partial(pow, 2)        # pow(2, x)
        double(5)                          # 32
    """

    def call(*args, **kwargs):
        return func(*fixed_args, *args, **{**fixed_kwargs, **kwargs})

    return call


def apply_discount(price: float, *, percent: float, minimum: float = 0.0) -> float:
    """Reduce `price` by `percent` percent, but never below `minimum`.

    Round the result to 2 decimals. apply_discount(80, percent=25) -> 60.0
    """
    return round(max(price * (1 - percent / 100), minimum), 2)


def make_discounts() -> dict:
    """Return {"half": f, "tenth": g} where f and g take only a price.

    half   = 50 % off, tenth = 10 % off, both with a minimum price of 1.0.
    Build them with partial(apply_discount, percent=..., minimum=1.0).
    """
    return {
        "half": partial(apply_discount, percent=50, minimum=1.0),
        "tenth": partial(apply_discount, percent=10, minimum=1.0),
    }


if __name__ == "__main__":
    out: list = []
    debug, info, error = make_loggers(out, "app: ")
    info("started")
    error("boom")
    print(out)
    print(make_parsers()["hex"]("ff"))
