"""Assignment 4: Retry, clean up and fall back.

Practises `finally`, re-raising, `raise ... from ...` and choosing which
exceptions to catch.
"""


def retry(func, times: int = 3, exceptions: tuple = (Exception,)):
    """Call `func()` up to `times` times and return its result.

    If the call raises one of `exceptions`, try again. If the last attempt
    also fails, let that exception propagate. Exceptions that are not in
    `exceptions` propagate at once without another attempt.
    Raise ValueError if `times` is less than 1.

    Flaky function that fails twice then works: retry(f, 3) -> its result.
    A function that always raises KeyError: retry(f, 3, (KeyError,)) calls it
    3 times and then raises KeyError.
    """
    if times < 1:
        raise ValueError("times must be at least 1")
    for attempt in range(1, times + 1):
        try:
            return func()
        except exceptions:
            if attempt == times:
                raise


def run_with_cleanup(action, log: list) -> object:
    """Call `action()` and return its result. Always append "cleanup" to `log`
    afterwards, whether `action` succeeded or raised. Do not hide the error.

    log = []; run_with_cleanup(lambda: 5, log)   -> 5, log == ["cleanup"]
    run_with_cleanup(lambda: 1 / 0, log)         -> raises ZeroDivisionError,
                                                    and log still gets "cleanup"
    """
    try:
        return action()
    finally:
        log.append("cleanup")


def first_success(funcs: list):
    """Call each function in turn and return the first result that does not raise.

    If every function raises an Exception, raise RuntimeError("all failed")
    chained from the last exception (`raise ... from last`).
    An empty list also raises RuntimeError("all failed") (nothing to chain).

    first_success([lambda: 1 / 0, lambda: "ok"])  -> "ok"
    """
    last_error = None
    for func in funcs:
        try:
            return func()
        except Exception as exc:
            last_error = exc
    raise RuntimeError("all failed") from last_error


def parse_or_none(text: str, parser) -> object:
    """Return parser(text), or None if the parser raises ValueError.
    Other exceptions must pass through.

    parse_or_none("12", int)    -> 12
    parse_or_none("x", int)     -> None
    parse_or_none(None, int)    -> raises TypeError
    """
    try:
        return parser(text)
    except ValueError:
        return None


if __name__ == "__main__":
    attempts = []

    def flaky():
        attempts.append(1)
        if len(attempts) < 3:
            raise ConnectionError("try again")
        return "connected"

    print(retry(flaky, 5), "after", len(attempts), "attempts")
