"""Assignment 1: Describe a function and list an object's public methods.

`inspect.signature` tells you how a function wants to be called. This is the
first step of every tool that builds a call from data, such as a plugin runner.
"""

import inspect


def describe_params(func) -> list[dict]:
    """Describe each parameter of `func`, in order.

    Return a list of dicts with exactly these keys:
      "name"     the parameter name
      "kind"     the lower-case kind name, e.g. "positional_or_keyword",
                 "keyword_only", "var_positional" (see `Parameter.kind.name`)
      "required" True if the caller must supply a value. A parameter with a
                 default is not required. `*args` and `**kwargs` are never
                 required.
      "default"  the default value, or None when there is no default

    describe_params(lambda a, b=2: 0) ->
        [{"name": "a", "kind": "positional_or_keyword", "required": True, "default": None},
         {"name": "b", "kind": "positional_or_keyword", "required": False, "default": 2}]
    """
    result = []
    for param in inspect.signature(func).parameters.values():
        has_default = param.default is not inspect.Parameter.empty
        is_var = param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD)
        result.append(
            {
                "name": param.name,
                "kind": param.kind.name.lower(),
                "required": not has_default and not is_var,
                "default": param.default if has_default else None,
            }
        )
    return result


def summary_line(func) -> str:
    """Return the first line of the cleaned docstring, or "" if there is none.

    Use `inspect.getdoc` so that indentation is removed. For a docstring that
    starts with a blank line or has several paragraphs, only the first
    non-empty line counts.
    """
    doc = inspect.getdoc(func)
    if not doc:
        return ""
    return doc.strip().splitlines()[0]


def public_methods(obj) -> dict[str, str]:
    """Map the name of each public method of `obj` to its signature text.

    "Public" means the name does not start with an underscore. Include only
    callable attributes. Use the signature of the bound method, so `self` is
    not shown. Return the dict sorted by method name.

    class Greeter:
        def hello(self, name: str, excited: bool = False) -> str: ...
    public_methods(Greeter()) ->
        {"hello": "(name: str, excited: bool = False) -> str"}
    """
    methods = {}
    for name, member in inspect.getmembers(obj, callable):
        if not name.startswith("_"):
            methods[name] = str(inspect.signature(member))
    return dict(sorted(methods.items()))


if __name__ == "__main__":
    def send(to: str, body: str = "hi", *, retries: int = 3) -> bool:
        """Send a message."""
        return True

    for item in describe_params(send):
        print(item)
    print(summary_line(send))
