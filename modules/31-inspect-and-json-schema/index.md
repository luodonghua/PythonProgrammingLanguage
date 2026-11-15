---
layout: module
module: 31-inspect-and-json-schema
kind: learn
title: inspect, runtime type hints and JSON Schema
permalink: /modules/31-inspect-and-json-schema/
---

<div class="box key" markdown="1">

## Key learning points

- `inspect.signature(func)` returns a `Signature`. Its `parameters` hold each name, **kind**, default and annotation.
- `typing.get_type_hints(func)` returns the real type objects. `get_origin` and `get_args` take a hint such as `list[int]` apart.
- Python does not enforce type hints. Code that gets data from outside must check it.
- A **JSON Schema** is a JSON description of the shape of some data. You can build one from a function signature and use it to describe the function to other programs.
- `Signature.bind` and pydantic can check a dict of arguments against a function before you call it.

</div>

## 1. Reading a signature

A **signature** is the list of parameters a function accepts. `inspect` gives it to you as an object.

```python
import inspect

def send(to: str, body: str = "hi", /, *, retries: int = 3, tags: list[str] | None = None) -> bool:
    """Send a message.

    More detail here.
    """
    return True

sig = inspect.signature(send)
print(sig)
```

```text
(to: str, body: str = 'hi', /, *, retries: int = 3, tags: list[str] | None = None) -> bool
```

Each entry of `sig.parameters` is a `Parameter`:

```python
for name, p in sig.parameters.items():
    print(name, p.kind.name, p.default is inspect.Parameter.empty)
```

```text
to POSITIONAL_ONLY True
body POSITIONAL_ONLY False
retries KEYWORD_ONLY False
tags KEYWORD_ONLY False
```

- `p.kind` is one of `POSITIONAL_ONLY`, `POSITIONAL_OR_KEYWORD`, `VAR_POSITIONAL` (`*args`), `KEYWORD_ONLY`, `VAR_KEYWORD` (`**kwargs`).
- `p.default` is the default value, or the marker `inspect.Parameter.empty` when there is none. Compare with `is`, because `None` is a valid default.
- `inspect.getdoc(send)` returns the docstring with the indentation removed. Its first line makes a good short description.

## 2. Type hints at runtime

`p.annotation` shows the hint, but it can be a string. `typing.get_type_hints` resolves strings into real objects:

```python
from typing import get_type_hints

print(get_type_hints(send))
```

```text
{'to': <class 'str'>, 'body': <class 'str'>, 'retries': <class 'int'>, 'tags': list[str] | None, 'return': <class 'bool'>}
```

To look inside a hint, use `get_origin` and `get_args`:

```python
from typing import Literal, get_args, get_origin

print(get_origin(list[int]), get_args(list[int]))
print(get_origin(int | None), get_args(int | None))
print(get_origin(Literal["a", "b"]), get_args(Literal["a", "b"]))
print(get_origin(int), get_args(int))
```

```text
<class 'list'> (<class 'int'>,)
<class 'types.UnionType'> (<class 'int'>, <class 'NoneType'>)
typing.Literal ('a', 'b')
None ()
```

For a plain class such as `int`, `get_origin` returns `None`. The origin of `int | None` depends on the version: it is `types.UnionType` in 3.12 and 3.13. In Python 3.14, `types.UnionType` and `typing.Union` became the same object, so the result is `typing.Union` there. Code that works on every version compares with both: `origin in (typing.Union, types.UnionType)`.

### Python 3.14: annotations are evaluated lazily

*Python 3.14 and later.* Before 3.14, Python evaluated annotations when it ran the `def` line. In 3.14 (PEP 649 and PEP 749) annotations are stored and evaluated only when something asks for them. A forward reference to a class defined later no longer needs quotes. The new `annotationlib` module reads them, with `get_annotations(func, format=...)`. The formats are `VALUE` (real objects, like older versions), `FORWARDREF` (undefined names become placeholders) and `STRING`. `inspect.signature` also gained an `annotation_format` argument.

Nothing changes for the code in this topic. `get_type_hints` still works, and so does `inspect.get_annotations` for simple cases. Read hints through these functions, not by reaching into `__annotations__` yourself. See [What's New in Python 3.14](https://docs.python.org/3/whatsnew/3.14.html).

## 3. From signature to JSON Schema

**JSON Schema** is a standard way to describe JSON data: `{"type": "integer"}` means "an integer". A plugin system, a web API or a tool runner can publish one schema per function so callers know which arguments to send.

Here is a small builder that handles `int` and `str`:

```python
def to_schema(tp):
    if tp is int:
        return {"type": "integer"}
    if tp is str:
        return {"type": "string"}
    raise TypeError(f"unsupported type: {tp!r}")

def tool_schema(func):
    hints = get_type_hints(func)
    props, required = {}, []
    for name, p in inspect.signature(func).parameters.items():
        props[name] = to_schema(hints[name])
        if p.default is p.empty:
            required.append(name)
    return {"type": "object", "properties": props, "required": required}

def repeat(text: str, times: int = 2) -> str:
    """Repeat text."""
    return text * times

print(tool_schema(repeat))
```

```text
{'type': 'object', 'properties': {'text': {'type': 'string'}, 'times': {'type': 'integer'}}, 'required': ['text']}
```

Extend `to_schema` with `float` (`"number"`), `bool` (`"boolean"`), `list[T]` (`{"type": "array", "items": ...}`) and `X | None` (`{"anyOf": [..., {"type": "null"}]}`). You do this in the assignments.

Pydantic can build schemas too. `TypeAdapter` works on any type hint:

```python
from pydantic import TypeAdapter

print(TypeAdapter(list[int] | None).json_schema())
```

```text
{'anyOf': [{'items': {'type': 'integer'}, 'type': 'array'}, {'type': 'null'}]}
```

For a whole function, build a model with `pydantic.create_model` from its parameters (assignment 4).

## 4. Calling a function with JSON arguments

Hints are not enforced. This runs without error:

```python
def double(n: int):
    return n * 2

print(double("ab"))   # abab
```

When the arguments come from a file, a web request or a program you do not control, check them first. `Signature.bind` checks the *shape* (names and count):

```python
sig = inspect.signature(repeat)
bound = sig.bind(**{"text": "ab", "times": 3})
print(bound.arguments, repeat(*bound.args, **bound.kwargs))

try:
    sig.bind(text="x", color="red")
except TypeError as exc:
    print(exc)
```

```text
{'text': 'ab', 'times': 3} ababab
got an unexpected keyword argument 'color'
```

`bind` does not check types. For that, compare each value with its hint (assignment 3) or let pydantic do it. `pydantic.validate_call` wraps a function so that arguments are validated and coerced on every call:

```python
from pydantic import validate_call

@validate_call
def add(a: int, b: int = 1) -> int:
    return a + b

print(add("2", b=3))   # 5
```

A bad value such as `add("x")` raises `pydantic.ValidationError`.

### Listing what an object can do

`inspect.getmembers(obj, callable)` returns `(name, member)` pairs. Filter out names that start with `_` and you have the public methods of a plugin. `inspect.signature` on a bound method leaves out `self`.

<div class="box warn" markdown="1">

## Common mistakes

- **Trusting type hints.** `def f(n: int)` accepts a string. Hints document and help tools. Validate data at the edge of your program.
- **Testing `p.default == inspect.Parameter.empty` or `if p.default:`.** A default of `0` or `None` is still a default. Use `p.default is inspect.Parameter.empty`.
- **Reading `__annotations__` directly.** It can hold strings, and in 3.14 it is built on demand. Use `get_type_hints` or `inspect.get_annotations`.
- **Forgetting that `bool` is an `int`.** `isinstance(True, int)` is `True`, so a check for "integer" lets `true` from JSON through. Test `bool` first.
- **Putting `*args` and `**kwargs` in a schema.** They are not named parameters. Skip them.

</div>

## Try it yourself

1. Write `show(func)` that prints one line per parameter: its name, kind and default (or `required`).
2. Extend `to_schema` to handle `list[int]` and `bool`. Test it with `get_origin` and `get_args`.
3. Write `call(func, args)` that uses `Signature.bind` to report missing or unknown names before calling `func`.

<div class="box" markdown="1">

## Where this appears in AI agents

An agent sends a list of **tool descriptions** to the language model: a name, a one-line description and a JSON Schema for the arguments. The model replies with a tool name and a dict of arguments. That dict is untrusted input, so the agent validates it before it calls anything. Both steps use what you learned here: the description is built from `inspect.signature`, `get_type_hints` and `getdoc`, and the check is a schema or pydantic validation.

```python
tool = {"name": "repeat", "description": "Repeat text.", "parameters": tool_schema(repeat)}
```

</div>

## Where this comes from

Beyond the two reference books. *Introducing Python*, chapter 14 (Type Hints and Documentation) covers the hints themselves. For the tools in this topic see the Python docs for [`inspect`](https://docs.python.org/3/library/inspect.html), [`typing.get_type_hints`](https://docs.python.org/3/library/typing.html#typing.get_type_hints) and [`annotationlib`](https://docs.python.org/3/library/annotationlib.html), and the [JSON Schema](https://json-schema.org/) site.

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="31-inspect-and-json-schema:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/31-inspect-and-json-schema/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/31-inspect-and-json-schema/assignments/' | relative_url }}).
