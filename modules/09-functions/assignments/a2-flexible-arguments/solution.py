"""Assignment 2: Flexible arguments.

Practises default values, keyword-only parameters, `*args` and `**kwargs`.
"""


def join_path(*parts: str, sep: str = "/") -> str:
    """Join path parts with `sep` and avoid doubled separators.

    Strip `sep` from both ends of every part, skip parts that are empty
    after stripping, and keep a leading `sep` if the first part had one.

    join_path("a", "b", "c")             -> "a/b/c"
    join_path("a/", "/b")                -> "a/b"
    join_path("/usr", "local", "bin")    -> "/usr/local/bin"
    join_path("a", "", "b", sep="\\")    -> "a\\b"
    join_path()                          -> ""
    """
    if not parts:
        return ""
    prefix = sep if parts[0].startswith(sep) else ""
    cleaned = [part.strip(sep) for part in parts]
    return prefix + sep.join(part for part in cleaned if part)


def clamp(value: float, /, low: float = 0, high: float = 100) -> float:
    """Return `value` limited to the range low..high.

    `value` is positional-only (note the `/` in the signature).

    clamp(150)             -> 100
    clamp(-5)              -> 0
    clamp(5, 10, 20)       -> 10
    clamp(5, high=3, low=1) -> 3
    """
    return max(low, min(value, high))


def greet(name: str, *, greeting: str = "Hello", punctuation: str = "!") -> str:
    """Return a greeting. Everything after `*` must be given by keyword.

    greet("Ada")                         -> "Hello, Ada!"
    greet("Ada", greeting="Hi")          -> "Hi, Ada!"
    greet("Ada", punctuation="?")        -> "Hello, Ada?"
    """
    return f"{greeting}, {name}{punctuation}"


def average(first: float, *rest: float) -> float:
    """Return the average of one or more numbers.

    average(4)           -> 4
    average(1, 2, 3, 4)  -> 2.5
    """
    numbers = (first, *rest)
    return sum(numbers) / len(numbers)


def make_tag(name: str, text: str = "", **attributes: str) -> str:
    """Build a simple HTML tag. Attributes appear in the order given.

    make_tag("br")                               -> "<br></br>"
    make_tag("p", "hi")                          -> "<p>hi</p>"
    make_tag("a", "home", href="/", id="top")    -> '<a href="/" id="top">home</a>'
    """
    attrs = "".join(f' {key}="{value}"' for key, value in attributes.items())
    return f"<{name}{attrs}>{text}</{name}>"


def call_with(func, *args, **kwargs):
    """Call `func` with the given arguments and return its result.

    call_with(max, 3, 9, 4)                     -> 9
    call_with(sorted, [3, 1, 2], reverse=True)  -> [3, 2, 1]
    """
    return func(*args, **kwargs)


if __name__ == "__main__":
    print(join_path("a/", "/b", "c"))
    print(make_tag("a", "home", href="/"))
