---
layout: module
module: 13-classes-and-objects
kind: learn
title: Classes and objects
permalink: /modules/13-classes-and-objects/
---

<div class="box key" markdown="1">

## Key learning points

- A **class** is a blueprint. Calling it (`Dog("Rex", 3)`) builds an **object** (an *instance*). `__init__` sets up the new instance.
- **Instance attributes** (`self.name`) belong to one object. **Class attributes** are shared by all instances.
- A method is a function inside a class. Python passes the instance as the first argument, named `self` by convention.
- `__repr__` is for developers (and debugging). `__str__` is for users. Define `__repr__` first.
- `@property` makes a method read like an attribute, and a setter can validate new values.
- Special ("dunder") methods such as `__eq__`, `__lt__`, `__len__`, `__iter__` and `__add__` let your objects work with `==`, `<`, `len()`, `for` and `+`.

</div>

## 1. A first class

```python
class Dog:
    species = "Canis familiaris"      # class attribute

    def __init__(self, name, age):
        self.name = name              # instance attributes
        self.age = age

    def speak(self):
        return f"{self.name} says woof"

rex = Dog("Rex", 3)
print(rex.speak())
```

```text
Rex says woof
```

`rex.speak()` is the same as `Dog.speak(rex)`. Python fills in `self` for you.

## 2. Instance vs class attributes

```python
print(rex.species, Dog.species)
rex.species = "wolf"
print(rex.species, Dog.species, Dog("Fido", 1).species)
```

```text
Canis familiaris Canis familiaris
wolf Canis familiaris Canis familiaris
```

Reading `rex.species` looks in the object first, then in the class. Assigning `rex.species = ...` creates a new attribute **on the object** and leaves the class value alone.

Take care with mutable class attributes. All instances share one list:

```python
class Counter:
    items = []

c1, c2 = Counter(), Counter()
c1.items.append(1)
print(c2.items)
```

```text
[1]
```

Create per-object lists in `__init__` (`self.items = []`).

## 3. `__repr__` and `__str__`

Printing a plain object is not helpful:

```python
print(rex)
```

```text
<__main__.Dog object at 0x736594e3ccb0>
```

(The address differs on every run.) Define the two methods:

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x!r}, {self.y!r})"

    def __str__(self):
        return f"({self.x}, {self.y})"

p = Point(1, 2)
print(p)
print(repr(p))
print([p])
```

```text
(1, 2)
Point(1, 2)
[Point(1, 2)]
```

`print` uses `__str__`. `repr()`, the REPL and containers such as lists use `__repr__`. If you only define `__repr__`, `print` uses it too. A good `__repr__` looks like the code that would build the object.

## 4. Properties

A property keeps a simple attribute syntax while you control access:

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius        # goes through the setter

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self):             # read-only, computed
        return self._celsius * 9 / 5 + 32

t = Temperature(100)
print(t.fahrenheit)
try:
    t.celsius = -300
except ValueError as e:
    print("error:", e)
```

```text
212.0
error: below absolute zero
```

The leading underscore in `_celsius` is a convention that means "internal, do not touch from outside". Python does not enforce it.

## 5. `@classmethod` and `@staticmethod`

```python
class Date:
    def __init__(self, year, month, day):
        self.year, self.month, self.day = year, month, day

    @classmethod
    def from_string(cls, text):       # alternative constructor
        year, month, day = map(int, text.split("-"))
        return cls(year, month, day)

    @staticmethod
    def is_leap(year):                # no self, no cls
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

d = Date.from_string("2024-02-29")
print(d.year, d.month, d.day, Date.is_leap(2100))
```

```text
2024 2 29 False
```

- A **class method** receives the class (`cls`). Use it for alternative constructors.
- A **static method** receives neither. It is a plain function that lives in the class for organisation.

## 6. Special methods

```python
class Money:
    def __init__(self, cents):
        self.cents = cents

    def __repr__(self):
        return f"Money({self.cents})"

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.cents == other.cents

    def __lt__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.cents < other.cents

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return Money(self.cents + other.cents)

print(Money(150) + Money(250))
print(Money(5) == Money(5), Money(5) < Money(7))
print(sorted([Money(30), Money(10), Money(20)]))
print(Money(1) == 1)
```

```text
Money(400)
True True
[Money(10), Money(20), Money(30)]
False
```

Returning `NotImplemented` (not raising an error) tells Python to try the other operand, and finally to give a sensible answer or a `TypeError`. Without your own `__eq__`, two objects are equal only if they are the *same* object.

Defining `__eq__` sets `__hash__` to `None`, so such objects cannot be dict keys or set members until you also define `__hash__`. Make the class immutable if you do.

Containers use `__len__` and `__iter__`:

```python
class Playlist:
    def __init__(self, *songs):
        self._songs = list(songs)

    def __len__(self):
        return len(self._songs)

    def __iter__(self):
        return iter(self._songs)

pl = Playlist("a", "b", "c")
print(len(pl), list(pl), "b" in pl)
```

```text
3 ['a', 'b', 'c'] True
```

`in` works because Python falls back to iterating when there is no `__contains__`.

## 7. A preview of `@dataclass`

Many classes only store data. `@dataclass` writes `__init__`, `__repr__` and `__eq__` from type-annotated fields:

```python
from dataclasses import dataclass

@dataclass
class Item:
    name: str
    price: float = 0.0

print(Item("pen", 1.5), Item("pen", 1.5) == Item("pen", 1.5))
```

```text
Item(name='pen', price=1.5) True
```

Topic 30 covers dataclasses in full.

<div class="box warn" markdown="1">

## Common mistakes

- **Forgetting `self`.** `def speak():` inside a class fails with "takes 0 positional arguments but 1 was given". Inside methods, use `self.name`, not `name`.
- **A shared mutable class attribute.** `items = []` at class level is shared by every instance. Create it in `__init__`.
- **Raising `TypeError` inside `__eq__` or `__add__`.** For unsupported types, return `NotImplemented` and let Python decide.
- **Comparing with `==` when you mean `is`.** Without `__eq__`, `A() == A()` is `False`: two separate objects.
- **Writing the setter without the getter.** `@x.setter` only works after `@property def x`. The setter must have the same name.

</div>

## Try it yourself

1. Write a `Rectangle(width, height)` class with an `area` property and a `__repr__`.
2. Add `__eq__` and `__lt__` (compare by area). Sort a list of rectangles.
3. Add a `@classmethod square(cls, side)` that builds a square.

## Further reading

- [Python data model](https://docs.python.org/3/reference/datamodel.html#special-method-names)

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="13-classes-and-objects:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/13-classes-and-objects/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/13-classes-and-objects/assignments/' | relative_url }}).
