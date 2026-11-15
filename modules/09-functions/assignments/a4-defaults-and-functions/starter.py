"""Assignment 4: Defaults, scope and functions as values.

Functions are objects. You can store them, pass them to other functions
and return them from functions.
"""


def add_item(item, items=None):
    """Return a list that has `item` at the end.

    If `items` is given, append to it and return that same list.
    If `items` is None, start a NEW empty list on every call.

    add_item("a")             -> ["a"]
    add_item("b")             -> ["b"]        (not ["a", "b"])
    add_item("c", ["x"])      -> ["x", "c"]

    This is the safe version of the classic bug `def add_item(item, items=[])`.
    """
    # TODO: create the list inside the function when items is None.
    ...


def apply_n_times(func, n: int, x):
    """Apply `func` to `x`, n times in a row, and return the result.

    apply_n_times(lambda v: v * 2, 3, 1)  -> 8
    apply_n_times(str.strip, 0, " a ")    -> " a "
    """
    # TODO: loop n times, feeding each result back in.
    ...


def compose(*funcs):
    """Return a new function that applies `funcs` from left to right.

    inc = lambda v: v + 1
    dbl = lambda v: v * 2
    compose(inc, dbl)(5)   -> 12     (inc first, then dbl)
    compose()(5)           -> 5      (no functions: return the value unchanged)
    """
    # TODO: define and return an inner function.
    ...


def make_counter(start: int = 0):
    """Return a function. Each call to it returns the next number.

    counter = make_counter(10)
    counter()  -> 10
    counter()  -> 11
    Two counters from separate make_counter calls are independent.
    """
    # TODO: use a variable in the enclosing scope and `nonlocal`.
    ...


def apply_all(functions: dict, value):
    """Call every function in the dict on `value`.
    Return a dict with the same keys and the results as values.

    apply_all({"upper": str.upper, "length": len}, "abc")
        -> {"upper": "ABC", "length": 3}
    """
    # TODO: a dict comprehension works well here.
    ...


if __name__ == "__main__":
    print(apply_n_times(lambda v: v * 2, 3, 1))
    counter = make_counter()
    print(callable(counter))
    print(apply_all({"upper": str.upper, "length": len}, "abc"))
