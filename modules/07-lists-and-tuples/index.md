---
layout: module
module: 07-lists-and-tuples
kind: learn
title: Lists and tuples
permalink: /modules/07-lists-and-tuples/
---

<div class="box key" markdown="1">

## Key learning points

- A **list** is an ordered, **mutable** sequence: `[1, 2, 3]`. A **tuple** is an ordered, **immutable** sequence: `(1, 2, 3)`.
- Indexing and slicing work the same as for strings: `items[0]`, `items[-1]`, `items[1:3]`, `items[::-1]`.
- Mutating methods (`append`, `extend`, `insert`, `pop`, `remove`, `sort`) change the list and return `None`. `sorted()` returns a **new** list.
- `b = a` does **not** copy a list. Both names point to the same list. Use `a.copy()` or `a[:]` for a shallow copy.
- A **list comprehension** builds a list in one line: `[n * n for n in numbers if n > 0]`.
- **Unpacking** assigns the parts of a sequence to names: `x, y = point` and `first, *rest = items`.

</div>

## 1. Indexing and slicing

```python
nums = [10, 20, 30, 40, 50]
print(nums[0], nums[-1])      # 10 50
print(nums[1:3])              # [20, 30]
print(nums[::2])              # [10, 30, 50]
print(nums[::-1])             # [50, 40, 30, 20, 10]
print(len(nums))              # 5
```

A slice always makes a **new** list and never raises `IndexError`. A single bad index does.

## 2. Changing a list

```python
nums = [10, 20, 30, 40, 50]
nums.append(60)           # add one item at the end
nums.extend([70, 80])     # add several items
nums.insert(0, 5)         # insert at index 0
print(nums)               # [5, 10, 20, 30, 40, 50, 60, 70, 80]

print(nums.pop())         # 80   (remove and return the last item)
print(nums.pop(0))        # 5    (remove and return index 0)
nums.remove(30)           # remove the first item equal to 30
nums[1] = 99              # replace an item
print(nums)               # [10, 99, 40, 50, 60, 70]
```

`remove(x)` raises `ValueError` if `x` is not in the list. `del nums[0]` removes by index and `nums.clear()` empties the list.

Useful tools for reading a list:

```python
print(99 in nums, 21 in nums)       # True False
print(min(nums), max(nums), sum(nums))   # 10 99 329
print(nums.index(99), [1, 2, 2].count(2))   # 1 2
```

## 3. sort and sorted

```python
a = [3, 1, 2]
print(sorted(a), a)     # [1, 2, 3] [3, 1, 2]   (a is unchanged)
a.sort()                # sorts in place
print(a)                # [1, 2, 3]
a.sort(reverse=True)
print(a)                # [3, 2, 1]
print(sorted(["bb", "a", "ccc"], key=len))   # ['a', 'bb', 'ccc']
```

`key=` is a function that gives each item its sort value. `list.sort()` returns `None`, so `a = a.sort()` loses your list.

## 4. Aliasing and copying

```python
a = [1, 2, 3]
b = a            # alias: the same list
c = a.copy()     # a new list (so is a[:] or list(a))
b.append(0)
print(a, c)      # [1, 2, 3, 0] [1, 2, 3]
```

A copy is **shallow**: it copies the outer list, but inner lists are still shared.

```python
grid = [[0] * 2] * 2          # two references to ONE inner list
grid[0][0] = 1
print(grid)                   # [[1, 0], [1, 0]]

grid = [[0] * 2 for _ in range(2)]   # two separate inner lists
grid[0][0] = 1
print(grid)                   # [[1, 0], [0, 0]]
```

Use `copy.deepcopy(x)` when you need to copy nested lists completely.

## 5. List comprehensions

```python
print([n * n for n in range(5)])              # [0, 1, 4, 9, 16]
print([n for n in range(10) if n % 3 == 0])   # [0, 3, 6, 9]
print([(x, y) for x in "ab" for y in (1, 2)])
```

```text
[('a', 1), ('a', 2), ('b', 1), ('b', 2)]
```

The shape is `[expression for item in iterable if condition]`. It is the same as a loop with `append`, in one line. Use it when it stays easy to read. A long or nested one is better as a normal loop.

## 6. Tuples

```python
t = (1, 2, 3)
print(t[0], t[1:], len(t))    # 1 (2, 3) 3
t[0] = 9                      # TypeError: 'tuple' object does not support item assignment
```

A tuple is a fixed group of values, such as a point `(x, y)` or a record `("Ada", 36)`. Use a tuple when the number of items is fixed and the position has meaning. Use a list for a collection that grows or shrinks.

```python
single = (5,)         # a one-item tuple needs the comma
print(type(single), type((5)))   # <class 'tuple'> <class 'int'>
print((1, 2) < (1, 3))           # True   (compared item by item)
```

The comma makes the tuple, not the brackets: `pt = 3, 4`.

## 7. Unpacking

```python
x, y = 3, 4
first, *rest = [1, 2, 3, 4]
print(first, rest)            # 1 [2, 3, 4]
*init, last = [1, 2, 3, 4]
print(init, last)             # [1, 2, 3] 4
a, (b, c) = 1, (2, 3)         # nested
```

The number of names must match, except for one `*name`, which collects the rest as a list. A function that returns several values really returns a tuple, and you unpack it: `q, r = divmod(7, 2)`.

## 8. Nested lists

```python
m = [[1, 2, 3], [4, 5, 6]]
print(m[1][2])                   # 6   (row 1, column 2)
print([row[0] for row in m])     # [1, 4]   (first column)
print(list(zip(*m)))             # [(1, 4), (2, 5), (3, 6)]   (transpose)
print([x for row in m for x in row])   # [1, 2, 3, 4, 5, 6]   (flatten)
```

`zip(*m)` passes each row as a separate argument to `zip`, which pairs up the columns.

<div class="box warn" markdown="1">

## Common mistakes

- **`a = a.sort()`.** `sort()` returns `None`. Write `a.sort()` or `a = sorted(a)`.
- **Thinking `b = a` copies the list.** Use `a.copy()`.
- **`[[0] * n] * m` for a grid.** All rows are the same list. Use a comprehension.
- **Removing items while looping over the same list.** The loop skips items. Build a new list instead.
- **Forgetting the comma in a one-item tuple.** `(5)` is just `5`.

</div>

## Try it yourself

1. Make a list of the squares of the odd numbers from 1 to 9 with one comprehension.
2. Given `scores = [70, 95, 82, 60]`, print the three highest in order (use `sorted` and a slice).
3. Swap the first and last items of a list with tuple unpacking in one line.

## Where this comes from

*Introducing Python*, chapter 8 (Tuples and Lists). *Learn Python the Hard Way*, exercises 34 and 38 (accessing elements of lists, doing things to lists).

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="07-lists-and-tuples:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/07-lists-and-tuples/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/07-lists-and-tuples/assignments/' | relative_url }}).
