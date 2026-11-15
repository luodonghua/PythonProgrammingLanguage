"""Assignment 3: Pull facts out of a traceback with the traceback module.

Handy modules: traceback.extract_tb(exc.__traceback__) gives a list of frames
(oldest call first). Each frame has .name (function name), .lineno (line number)
and .line (the source text of that line, with outer spaces already removed).
"""

import traceback
from collections.abc import Callable


def last_frame(exc: BaseException) -> tuple[str, int, str]:
    """Return (function_name, line_number, source_line) of the frame where `exc`
    was raised (the LAST frame of its traceback).

    Raise ValueError if the exception has no traceback (it was never raised).
    """
    if exc.__traceback__ is None:
        raise ValueError("exception has no traceback")
    frame = traceback.extract_tb(exc.__traceback__)[-1]
    return frame.name, frame.lineno, frame.line


def call_chain(exc: BaseException) -> list[str]:
    """Return the function names of the traceback, outermost call first.

    Example: main() calls helper(), which raises  ->  ["main", "helper"]
    (the frame of the code that caught the exception is the first one,
    whatever its name). Return [] if the exception has no traceback.
    """
    if exc.__traceback__ is None:
        return []
    return [frame.name for frame in traceback.extract_tb(exc.__traceback__)]


def run_safely(func: Callable, *args) -> dict | None:
    """Call func(*args). If it works, return None.

    If it raises an Exception, return a dict with these keys:
        "type"      the class name, e.g. "ZeroDivisionError"
        "message"   str(exc)
        "function"  name of the function where it was raised (last frame)
        "line"      the line number there
        "code"      the source text of that line
        "depth"     how many frames the traceback has
    Do not catch BaseException (KeyboardInterrupt must still stop the program).
    """
    try:
        func(*args)
    except Exception as exc:
        name, lineno, code = last_frame(exc)
        return {
            "type": type(exc).__name__,
            "message": str(exc),
            "function": name,
            "line": lineno,
            "code": code,
            "depth": len(call_chain(exc)),
        }
    return None


if __name__ == "__main__":
    def inverse(n):
        return 1 / n

    print(run_safely(inverse, 0))
