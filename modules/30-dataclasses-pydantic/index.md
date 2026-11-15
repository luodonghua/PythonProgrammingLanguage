---
layout: module
module: 30-dataclasses-pydantic
kind: learn
title: Dataclasses and Pydantic
permalink: /modules/30-dataclasses-pydantic/
---

<div class="box key" markdown="1">

## Key learning points

- `@dataclass` writes `__init__`, `__repr__` and `__eq__` for you from the annotated fields. It does **not** check types at run time.
- Useful options: `frozen=True` (read-only), `slots=True` (smaller, faster), `order=True` (sortable), and `field(default_factory=list)` for mutable defaults.
- Use `__post_init__` for checks after the fields are set. `replace()` makes a modified copy and `asdict()` converts to a dict.
- A **Pydantic** `BaseModel` looks similar but **validates and converts** data when you create it. Bad data raises `ValidationError`.
- Pydantic gives you constraints (`Field(ge=0)`), custom checks (`field_validator`), nested models, and JSON in and out (`model_validate_json`, `model_dump`).
- Use dataclasses for trusted data inside your program. Use Pydantic at the **edges**, where data comes from files, users or other programs.

</div>

## 1. A first dataclass

```python
from dataclasses import dataclass

@dataclass
class Item:
    name: str
    price: float
    qty: int = 1

    def total(self):
        return self.price * self.qty

i = Item("pen", 1.5, 4)
print(i)
print(i.total(), i == Item("pen", 1.5, 4))
```

```text
Item(name='pen', price=1.5, qty=4)
6.0 True
```

Fields with defaults must come after fields without. The generated `__eq__` compares all fields.

Type hints are **not enforced**: `Item("pen", "cheap", "many")` is accepted without complaint. That is the main difference from Pydantic.

## 2. Options: frozen, slots, order

```python
from dataclasses import dataclass, replace, asdict, FrozenInstanceError

@dataclass(frozen=True, slots=True, order=True)
class Point:
    x: int
    y: int = 0

p = Point(1, 2)
try:
    p.x = 5
except FrozenInstanceError as e:
    print("error:", e)

print(Point(1, 2) < Point(1, 3), replace(p, y=9), asdict(p))
```

```text
error: cannot assign to field 'x'
True Point(x=1, y=9) {'x': 1, 'y': 2}
```

- `frozen=True` makes instances read-only. They also become hashable, so they can be dict keys.
- `slots=True` stores fields in a compact layout and blocks accidental new attributes.
- `order=True` adds `<`, `<=`, `>`, `>=`, comparing the fields in order as tuples.
- `replace(obj, y=9)` returns a new object with one field changed.

## 3. Mutable defaults, post-init and nesting

A list as a default would be shared by all instances, so `@dataclass` refuses it. Use `field(default_factory=...)`:

```python
from dataclasses import field

@dataclass
class Order:
    customer: str
    items: list[Item] = field(default_factory=list)
    discount: float = 0.0

    def __post_init__(self):
        if not 0 <= self.discount <= 1:
            raise ValueError("discount must be between 0 and 1")

    @property
    def total(self):
        return sum(i.total() for i in self.items) * (1 - self.discount)

o = Order("ann", [Item("pen", 2.0, 3), Item("book", 10.0)], discount=0.25)
print(o.total)
print(asdict(o))
```

```text
12.0
{'customer': 'ann', 'items': [{'name': 'pen', 'price': 2.0, 'qty': 3}, {'name': 'book', 'price': 10.0, 'qty': 1}], 'discount': 0.25}
```

`asdict` converts nested dataclasses too. `__post_init__` runs right after the generated `__init__`.

## 4. Pydantic: validation and coercion

Pydantic is a third-party package (`uv add pydantic`). A model class looks like a dataclass, but creating an instance **checks and converts** the input:

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(min_length=1)
    age: int = Field(ge=0, le=150)
    email: str | None = None
    tags: list[str] = []

u = User(name="ada", age="36")
print(u)
print(repr(u.age))
```

```text
name='ada' age=36 email=None tags=[]
36
```

The string `"36"` was **coerced** to the integer `36`. Pydantic copies the default `[]` for each instance, so unlike a dataclass, a plain list default is safe here.

## 5. ValidationError

```python
from pydantic import ValidationError

try:
    User(name="", age=-1)
except ValidationError as e:
    print(e.error_count())
    for err in e.errors():
        print(err["loc"], err["type"])
```

```text
2
('name',) string_too_short
('age',) greater_than_equal
```

`e.errors()` returns a list of dicts with the location (`loc`), a machine-readable `type`, and a readable `msg`. Pydantic reports **all** problems at once, not just the first. Programs can use `loc` and `type` to react, and the text of `msg` to show to people.

## 6. Custom validators and nested models

```python
from pydantic import field_validator

class Person(BaseModel):
    name: str
    age: int

    @field_validator("name")
    @classmethod
    def tidy_name(cls, value):
        return value.strip().title()

print(Person(name="  ada lovelace ", age=36))
```

```text
name='Ada Lovelace' age=36
```

Models can contain other models. Errors point to the exact place:

```python
class Address(BaseModel):
    city: str

class Customer(BaseModel):
    name: str
    address: Address

c = Customer.model_validate({"name": "z", "address": {"city": "Oslo"}})
print(c.address.city)

try:
    Customer.model_validate({"name": "z", "address": {}})
except ValidationError as e:
    print(e.errors()[0]["loc"])
```

```text
Oslo
('address', 'city')
```

## 7. JSON in, JSON out, and strict mode

```python
user = User.model_validate_json('{"name": "cy", "age": 7, "tags": ["a"]}')
print(user.model_dump())
print(user.model_dump_json())
```

```text
{'name': 'cy', 'age': 7, 'email': None, 'tags': ['a']}
{"name":"cy","age":7,"email":null,"tags":["a"]}
```

- `model_validate(dict)` builds a model from a dict, `model_validate_json(text)` from a JSON string.
- `model_dump()` returns a plain dict and `model_dump_json()` a JSON string.

By default Pydantic coerces (`"5"` becomes `5`). Strict mode refuses:

```python
class Strict(BaseModel):
    model_config = {"strict": True}
    n: int

try:
    Strict(n="5")
except ValidationError as e:
    print(e.errors()[0]["type"])   # int_type
```

## 8. Which one to use?

| | dataclass | Pydantic model |
|---|---|---|
| Part of the standard library | yes | no (install it) |
| Checks types at run time | no | yes |
| Converts input (`"5"` to `5`) | no | yes |
| Parses JSON | no | yes |
| Best for | internal data you already trust | untrusted input: files, APIs, config |

<div class="box warn" markdown="1">

## Common mistakes

- **Expecting a dataclass to check types.** `Item("pen", "x", "y")` works. Add `__post_init__` checks or use Pydantic.
- **A mutable default** such as `items: list = []` in a dataclass. It raises `ValueError`. Use `field(default_factory=list)`.
- **Putting a field with a default before one without** in a dataclass. It raises `TypeError`.
- **Surprise coercion in Pydantic.** `age="36"` is accepted as `36`. Use `strict` mode when you do not want that.
- **Catching only the first problem.** A `ValidationError` holds a list of errors. Read all of `e.errors()`.
- **Mutating a frozen dataclass.** Use `replace()` to get a changed copy.

</div>

<div class="box" markdown="1">

## Where this appears in AI agents

A language model returns text, and text can be wrong: a missing field, a number written as a word, a wrong key. Agent code therefore validates the model's output with a Pydantic model before using it. When validation fails, the program can send `e.errors()` back to the model and ask it to try again. Tool arguments are checked the same way before a tool runs.

```python
class SearchArgs(BaseModel):
    query: str = Field(min_length=1)
    limit: int = Field(default=5, ge=1, le=20)

args = SearchArgs.model_validate_json(model_output)   # raises ValidationError
```

</div>

## Try it yourself

1. Write a frozen dataclass `Money(amount: int, currency: str)`. Create two and compare them with `==`.
2. Write a Pydantic model `Product` with `name` (not empty) and `price` (greater than 0). Try `Product(name="x", price="2.5")` and `Product(name="", price=0)`.
3. Parse the JSON text `'{"name": "tea", "price": 3}'` into your `Product` and print `model_dump()`.

## Where this comes from

*Introducing Python*, chapter 11 (Objects) covers classes, and chapter 14 (Type Hints and Documentation) covers annotations. *Learn Python the Hard Way*, exercises 40 to 44 cover classes, but not dataclasses or Pydantic. Those parts go beyond both books. See the Python docs: [dataclasses](https://docs.python.org/3/library/dataclasses.html), and the [Pydantic documentation](https://docs.pydantic.dev/latest/).

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="30-dataclasses-pydantic:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/30-dataclasses-pydantic/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/30-dataclasses-pydantic/assignments/' | relative_url }}).
