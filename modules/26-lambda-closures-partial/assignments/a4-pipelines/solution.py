"""Assignment 4: Function tables, pipelines and callbacks."""

import operator


def pipeline(*funcs):
    """Return a function that passes a value through `funcs`, left to right.

        clean = pipeline(str.strip, str.lower)
        clean("  HeLLo ")      ->  "hello"

    With no functions, the result returns its argument unchanged.
    """

    def run(value):
        for func in funcs:
            value = func(value)
        return value

    return run


OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "//": operator.floordiv,
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
    parts = expression.split()
    if len(parts) != 3:
        raise ValueError("expected: number operator number")
    left, symbol, right = parts
    if symbol not in OPERATORS:
        raise ValueError(f"unknown operator: {symbol}")
    return OPERATORS[symbol](float(left), float(right))


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
    callbacks: dict[str, list] = {}

    def subscribe(event_name, callback) -> None:
        callbacks.setdefault(event_name, []).append(callback)

    def publish(event_name, *args) -> list:
        return [callback(*args) for callback in callbacks.get(event_name, [])]

    return subscribe, publish


def apply_all(value, funcs: list) -> list:
    """Return [f(value) for each f in funcs], but a function that raises an
    exception gives the string "error: <ExceptionName>" in its place.

        apply_all(4, [str, lambda x: 1 / (x - 4)]) -> ["4", "error: ZeroDivisionError"]
    """
    results = []
    for func in funcs:
        try:
            results.append(func(value))
        except Exception as exc:
            results.append(f"error: {type(exc).__name__}")
    return results


if __name__ == "__main__":
    print(pipeline(str.strip, str.lower, str.title)("  hELLO wORLD "))
    print(calculate("3 + 4"))
