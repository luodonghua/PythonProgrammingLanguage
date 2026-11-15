---
layout: module
module: 08-dicts-and-sets
kind: learn
title: Dictionaries and sets
permalink: /modules/08-dicts-and-sets/
---

<div class="box key" markdown="1">

## Key learning points

- A **dict** maps **keys** to **values**. Lookup by key is fast, and dicts keep the order in which keys were added.
- `d[key]` raises `KeyError` if the key is missing. `d.get(key, default)` returns a default instead.
- Keys must be **hashable**: numbers, strings and tuples of those work, lists and dicts do not.
- A **set** holds unique items with no order. Use it for membership tests, removing duplicates and maths on groups (`|`, `&`, `-`, `^`).
- `collections.Counter` counts things and `collections.defaultdict` creates missing values for you.

</div>

## 1. Creating and reading a dict

```python
ages = {"Ann": 31, "Bo": 25}
ages["Cy"] = 40            # add a new key
ages["Bo"] += 1            # change a value
print(ages)                # {'Ann': 31, 'Bo': 26, 'Cy': 40}
print(ages["Ann"])         # 31
print(ages.get("Zed"))     # None
print(ages.get("Zed", 0))  # 0
print("Bo" in ages)        # True
```

`in` tests the **keys**. Reading a missing key with square brackets fails:

```python
ages["nope"]               # KeyError: 'nope'
```

Remove entries with `del ages["Cy"]` or `ages.pop("Ann")`. `pop` returns the removed value.

## 2. Looping over a dict

```python
d = {"a": 1, "b": 2, "c": 3}
for key, value in d.items():
    print(key, value)
print(list(d.keys()))      # ['a', 'b', 'c']
print(list(d.values()))    # [1, 2, 3]
```

Looping over `d` alone gives the keys. Since Python 3.7 a dict remembers insertion order. Do not add or remove keys while you loop over it, because Python raises `RuntimeError: dictionary changed size during iteration`.

## 3. Comprehensions and merging

```python
print({w: len(w) for w in ["apple", "fig"]})   # {'apple': 5, 'fig': 3}

a = {"x": 1, "y": 2}
b = {"y": 20, "z": 30}
print(a | b)               # {'x': 1, 'y': 20, 'z': 30}
```

`a | b` builds a new dict. When both have a key, the **right-hand** value wins. `a |= b` updates `a` in place.

## 4. Counting and grouping

The classic way to count with a plain dict:

```python
counts = {}
for word in "to be or not to be".split():
    counts[word] = counts.get(word, 0) + 1
print(counts)              # {'to': 2, 'be': 2, 'or': 1, 'not': 1}
```

`Counter` does the same in one line, and a missing key counts as 0:

```python
from collections import Counter

c = Counter("to be or not to be".split())
print(c.most_common(2))    # [('to', 2), ('be', 2)]
print(c["zzz"])            # 0
```

`defaultdict(list)` creates an empty list the first time you use a key:

```python
from collections import defaultdict

groups = defaultdict(list)
for word in ["apple", "avocado", "bean"]:
    groups[word[0]].append(word)
print(dict(groups))        # {'a': ['apple', 'avocado'], 'b': ['bean']}
```

`d.setdefault(key, [])` does a similar job on a normal dict.

## 5. Hashability

A key must have a value that never changes, so Python can compute a fixed number (a **hash**) from it. Strings, numbers and tuples of them are hashable. Lists, dicts and sets are not:

```python
{[1]: 2}                   # TypeError: unhashable type: 'list'
spots = {(1, 2): "a"}      # a tuple works as a key
```

## 6. Sets

```python
s = {1, 2, 3, 2, 1}
print(s)                   # {1, 2, 3}
print(set())               # set()   (write {} and you get an empty dict)
```

Set maths:

```python
a = {1, 2, 3}
b = {3, 4}
print(a | b)    # {1, 2, 3, 4}   union
print(a & b)    # {3}            intersection
print(a - b)    # {1, 2}         difference
print(a ^ b)    # {1, 2, 4}      in exactly one of them
print(a <= {1, 2, 3, 4})       # True  (subset)
```

Use a set when you only care whether something is present. `x in some_set` takes about the same time for 10 items or 10 million, while `x in some_list` checks items one by one.

Remove duplicates but keep the order with `dict.fromkeys`:

```python
print(list(dict.fromkeys([3, 1, 3, 2, 1])))   # [3, 1, 2]
```

A `frozenset` is an immutable set. It is hashable, so it can be a dict key or a member of another set.

<div class="box warn" markdown="1">

## Common mistakes

- **`{}` is an empty dict, not an empty set.** Write `set()` for an empty set.
- **Using `d[key]` when the key may be missing.** Use `d.get(key, default)` or test with `in`.
- **Changing a dict while looping over it.** Loop over `list(d)` or build a new dict instead.
- **Expecting a set to keep order or support indexing.** `s[0]` is a `TypeError`. Use `sorted(s)` when you need an order.
- **Mutable keys.** A list cannot be a key. Convert it to a tuple first.

</div>

## Try it yourself

1. Count the letters in `"mississippi"` with a plain dict, then with `Counter`.
2. Given `{"a": 1, "b": 2}`, build `{1: "a", 2: "b"}` with a comprehension.
3. Two lists of friends overlap. Print who is on both lists and who is on only one.

## Where this comes from

*Introducing Python*, chapter 9 (Dictionaries and Sets). *Learn Python the Hard Way*, exercise 39 (dictionaries).

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="08-dicts-and-sets:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/08-dicts-and-sets/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/08-dicts-and-sets/assignments/' | relative_url }}).
