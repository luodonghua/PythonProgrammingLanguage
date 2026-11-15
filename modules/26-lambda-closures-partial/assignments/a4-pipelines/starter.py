"""Assignment 4: Function tables, pipelines and callbacks."""

import operator  # noqa: F401


def pipeline(*funcs):
    """Return a function that passes a value through `funcs`, left to right.

        clean = pipeline(str.strip, str.lower)
        clean("  HeLLo ")      ->  "hello"

    With no functions, the result returns its argument unchanged.
    """
    # TODO: write a closure `run(value)` that loops over funcs.
    ...


OPERATORS = {
    # TODO: map "+", "-", "*", "/" and "//" to functions from the operator module.
}


def calculate(expression: str) -> float:
    """Evaluate "<number> <operator> <number>", e.g. "3 + 4" or "7.5 * 2".

    The three parts are separated by spaces. Numbers are floats.
    Look the operator up in OPERATORS (a function table, no if/elif chain).
    - Wrong number of parts            -> ValueError("expected: number operator number")
    - Unknown operator, e.g. "3 ^ 2"   -> ValueError("unknown operator: ^")
    - A number that is not a number    -> ValueError (float() raises it)
    - Division by zero                 -> let ZeroDivisionError propagate
    """
    # TODO
    ...


def make_event_bus():
    """Return a pair of functions (subscribe, publish) that share a table of callbacks.

    subscribe(event_name, callback)  registers a callback for that event name.
    publish(event_name, *args)       calls every callback registered for that
                                     name with *args, in subscription order, and
                                     returns the list of their return values.
                                     An event with no subscribers returns [].
    Two calls to make_event_bus() give two independent buses.

    Hint: a dict of lists in the enclosing function; use setdefault.
    """
    # TODO
    ...


def apply_all(value, funcs: list) -> list:
    """Return [f(value) for each f in funcs], but a function that raises an
    exception gives the string "error: <ExceptionName>" in its place.

        apply_all(4, [str, lambda x: 1 / (x - 4)]) -> ["4", "error: ZeroDivisionError"]
    """
    # TODO: use type(exc).__name__.
    ...


if __name__ == "__main__":
    print(pipeline(str.strip, str.lower, str.title)("  hELLO wORLD "))
    print(calculate("3 + 4"))
