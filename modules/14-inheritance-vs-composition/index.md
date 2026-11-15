---
layout: module
module: 14-inheritance-vs-composition
kind: learn
title: Inheritance vs composition
permalink: /modules/14-inheritance-vs-composition/
---

<div class="box key" markdown="1">

## Key learning points

- **Inheritance** models *is-a* (a `Dog` is an `Animal`). **Composition** models *has-a* (a `Car` has an `Engine`).
- A subclass inherits attributes and methods, can **override** them, and calls the parent with `super()`.
- **Polymorphism**: code calls `shape.area()` and each class supplies its own version.
- An **abstract base class** (`ABC` with `@abstractmethod`) forces subclasses to implement the required methods. A **`Protocol`** describes the methods a function needs, with no inheritance at all.
- Prefer composition when you only want to *reuse* behaviour. Inheritance couples the subclass to every detail of its parent.

</div>

## 1. Inheritance and `super()`

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

    def intro(self):
        return f"{self.name} says {self.speak()}"

class Dog(Animal):
    def speak(self):              # override
        return "Woof"

class Puppy(Dog):
    def __init__(self, name, age_weeks):
        super().__init__(name)    # let the parent set up name
        self.age_weeks = age_weeks

    def speak(self):
        return super().speak() + "!"

for a in [Animal("Generic"), Dog("Rex"), Puppy("Bit", 8)]:
    print(a.intro())
```

```text
Generic says ...
Rex says Woof
Bit says Woof!
```

- `Dog` has no `__init__` or `intro`, so it uses the ones from `Animal`.
- `intro` calls `self.speak()`. Python looks up `speak` on the real type of the object, so each class's own version runs.
- If a subclass defines `__init__`, it should usually call `super().__init__(...)` first.

```python
print(isinstance(Puppy("x", 1), Animal), issubclass(Dog, Animal))
print([c.__name__ for c in Puppy.__mro__])
```

```text
True True
['Puppy', 'Dog', 'Animal', 'object']
```

`__mro__` (method resolution order) is the list of classes Python searches, in order, when it looks up an attribute. Every class ends with `object`.

## 2. Polymorphism and abstract base classes

When a base class is only a template, make it abstract:

```python
import math
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self): ...

    def describe(self):
        return f"{type(self).__name__} with area {self.area():.2f}"

class Circle(Shape):
    def __init__(self, r):
        self.r = r

    def area(self):
        return math.pi * self.r ** 2

class Square(Shape):
    def __init__(self, s):
        self.s = s

    def area(self):
        return self.s ** 2

try:
    Shape()
except TypeError as e:
    print(e)

for s in (Circle(1), Square(2)):
    print(s.describe())
```

```text
Can't instantiate abstract class Shape without an implementation for abstract method 'area'
Circle with area 3.14
Square with area 4.00
```

(The wording of the error message can differ between Python versions.) A subclass that forgets `area` cannot be instantiated, so the mistake shows up early.

## 3. Multiple inheritance and mixins

A class can have several parents. A **mixin** is a small parent class that adds one feature and is not meant to be used alone:

```python
import json

class JsonMixin:
    def to_json(self):
        return json.dumps(self.__dict__)

class User(JsonMixin):
    def __init__(self, name):
        self.name = name

print(User("ann").to_json())
```

```text
{"name": "ann"}
```

With several parents, `super()` follows the MRO, not just "the parent":

```python
class A:
    def hi(self): return "A"

class B(A):
    def hi(self): return "B>" + super().hi()

class C(A):
    def hi(self): return "C>" + super().hi()

class D(B, C):
    def hi(self): return "D>" + super().hi()

print(D().hi(), [k.__name__ for k in D.__mro__])
```

```text
D>B>C>A ['D', 'B', 'C', 'A', 'object']
```

Note that `B`'s `super()` reached `C`, not `A`. Keep multiple inheritance to simple mixins.

## 4. Composition and delegation

Composition means an object **holds** other objects and hands work to them (*delegation*).

```python
class Engine:
    def __init__(self, hp):
        self.hp = hp

    def start(self):
        return f"{self.hp} hp engine running"

class Car:
    def __init__(self, engine):
        self.engine = engine          # a Car has an Engine

    def start(self):
        return "Car: " + self.engine.start()

print(Car(Engine(120)).start())
```

```text
Car: 120 hp engine running
```

A `Car` is not an `Engine`, so inheritance would be wrong here. You can also swap the engine for another one, or for a test double.

## 5. A worked refactor: from `Stack(list)` to a stack that has a list

```python
class Stack(list):                    # "a Stack is a list"?
    def push(self, x):
        self.append(x)

s = Stack()
s.push(1)
s.push(2)
s.insert(0, 99)    # works, but breaks the idea of a stack
```

The subclass inherits dozens of list methods (`insert`, `sort`, `remove`), so anyone can break the stack rule. Hold a list instead:

```python
class Stack:
    def __init__(self):
        self._items = []

    def push(self, x):
        self._items.append(x)

    def pop(self):
        return self._items.pop()

    def __len__(self):
        return len(self._items)

print(hasattr(Stack(), "insert"))
```

```text
False
```

Now the public interface is only what you chose. You can switch the list for a `deque` later without changing any user code.

The same idea makes code testable. An `Order` that receives its logger can be given a fake:

```python
class Order:
    def __init__(self, logger):
        self.logger = logger

    def place(self):
        self.logger.log("order placed")

class FakeLogger:
    def __init__(self):
        self.lines = []

    def log(self, msg):
        self.lines.append(msg)

fake = FakeLogger()
Order(fake).place()
print(fake.lines)
```

```text
['order placed']
```

## 6. Protocols: duck typing with a checkable contract

Python only needs the right methods ("if it quacks like a duck"). A `Protocol` writes that contract down for readers and type checkers:

```python
from typing import Protocol

class SupportsSpeak(Protocol):
    def speak(self) -> str: ...

class Robot:                          # no inheritance from anything
    def speak(self):
        return "beep"

def talk(x: SupportsSpeak) -> str:
    return x.speak()

print(talk(Robot()), talk(Dog("a")))
```

```text
beep Woof
```

Python does not check the annotation when the code runs. A type checker such as mypy does (topic 15).

## 7. Which one to choose

| Question | Inheritance | Composition |
|---|---|---|
| Relationship | *is-a*, with the same interface | *has-a* or *uses-a* |
| Reuse | Everything the parent has | Only what you call |
| Change later | Hard, the parent leaks into children | Easy, swap the part |
| Testing | Needs the real parent | Pass a fake |

A rule of thumb: use inheritance for a real *is-a* with a shared interface (shapes, exceptions). Use composition to reuse code.

<div class="box warn" markdown="1">

## Common mistakes

- **Inheriting just to reuse code.** `class Stack(list)` exposes list methods you do not want. Hold the list instead.
- **Forgetting `super().__init__()`.** The parent's attributes are then missing, and you get an `AttributeError` later.
- **Deep hierarchies.** Four or five levels are hard to read. Keep them shallow.
- **Overriding with a different meaning.** A subclass must work wherever the parent works. A `Square` that breaks a `Rectangle`'s rules is a classic example.
- **Calling `super()` in a diamond and expecting only "the parent".** It follows the MRO.

</div>

## Try it yourself

1. Create `Shape` with `area()` and subclasses `Rectangle` and `Circle`. Write a function that sums the areas of a list of shapes.
2. Write `Report` that receives a `formatter` object with a `format(data)` method. Pass in two different formatter classes.
3. Print `__mro__` for a class with two parents. Change the order of the parents and see what changes.

## Where this comes from

*Introducing Python*, chapter 11 (Objects: inheritance, `super()`, mixins, composition). *Learn Python the Hard Way*, exercises 42 to 44 (Is-A, Has-A, objects and classes; inheritance versus composition). Protocols and abstract classes are described in the Python docs: [`abc`](https://docs.python.org/3/library/abc.html) and [`typing.Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol).

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="14-inheritance-vs-composition:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/14-inheritance-vs-composition/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/14-inheritance-vs-composition/assignments/' | relative_url }}).
