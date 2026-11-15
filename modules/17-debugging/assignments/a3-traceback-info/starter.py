"""Assignment 3: Pull facts out of a traceback with the traceback module.

Handy modules: traceback.extract_tb(exc.__traceback__) gives a list of frames
(oldest call first). Each frame has .name (function name), .lineno (line number)
and .line (the source text of that line, with outer spaces already removed).
"""

import traceback


def last_frame(exc):
    """Return (function_name, line_number, source_line) of the frame where `exc`
    was raised (the LAST frame of its traceback).

    Raise ValueError if the exception has no traceback (it was never raised).
    """
    # TODO
    ...


def call_chain(exc):
    """Return the function names of the traceback, outermost call first.

    Example: main() calls helper(), which raises  ->  ["main", "helper"]
    (the frame of the code that caught the exception is the first one,
    whatever its name). Return [] if the exception has no traceback.
    """
    # TODO
    ...


def run_safely(func, *args):
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
    # TODO
    ...


if __name__ == "__main__":
    def inverse(n):
        return 1 / n

    print(run_safely(inverse, 0))
