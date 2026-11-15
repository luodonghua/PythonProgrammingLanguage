---
layout: module
module: 28-iterators-generators
kind: learn
title: Iterators and generators
permalink: /modules/28-iterators-generators/
---

<div class="box key" markdown="1">

## Key learning points

- A `for` loop calls `iter()` on an **iterable** to get an **iterator**, then calls `next()` until `StopIteration`.
- A function with `yield` is a **generator function**. Calling it returns a generator and runs none of its body yet.
- Generators are **lazy**: each value is computed when asked for, so memory use stays small even for huge or endless streams.
- A generator can be used **once**. After it is exhausted, it yields nothing.
- A generator expression `(x * x for x in data)` is a one-line generator. `yield from` hands over to another iterable.
- `itertools` has fast building blocks (`islice`, `chain`, `pairwise`, `accumulate`, `batched`, `groupby`). Chain them into **pipelines**.

</div>

## 1. The iteration protocol

An **iterable** can give you an iterator (it has `__iter__`). An **iterator** gives one value at a time (it has `__next__`) and raises `StopIteration` when it has no more.

```python
nums = [10, 20]
it = iter(nums)
print(next(it), next(it))
try:
    next(it)
except StopIteration:
    print("done")
```

```text
10 20
done
```

`for x in nums:` does exactly this behind the scenes. Lists, strings, dicts, files and `range` are all iterable.

## 2. An iterator class

You can build an iterator by hand:

```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

print(list(Countdown(3)))   # [3, 2, 1]
```

It works, but you must manage the state yourself. A generator does the same job in four lines.

## 3. Generators with yield

```python
def countdown(start):
    while start > 0:
        yield start
        start -= 1

print(list(countdown(3)))   # [3, 2, 1]
```

`yield` hands a value to the caller and **pauses** the function. The next `next()` resumes right after the `yield`, with all local variables intact. Watch the order of events:

```python
def noisy():
    print("start")
    yield 1
    print("middle")
    yield 2
    print("end")

g = noisy()
print("created")
print(next(g))
print(next(g))
print(list(g))
```

```text
created
start
1
middle
2
end
[]
```

Creating the generator printed nothing. The body ran only when `next()` asked for a value. At the end, `list(g)` ran the rest of the body (printing `end`) and found no more values.

A generator is a one-shot object:

```python
g = countdown(3)
print(list(g), list(g))   # [3, 2, 1] []
```

## 4. Generator expressions

Like a list comprehension, with parentheses. It computes values one by one:

```python
squares = (n * n for n in range(1_000_000))
print(next(squares), next(squares), next(squares))   # 0 1 4
print(sum(n * n for n in range(5)))                  # 30
```

The generator for a million squares takes a few hundred bytes. The list `[n * n for n in range(1_000_000)]` would hold a million numbers. Use a list when you need to index or loop twice. Use a generator when you loop once.

## 5. yield from

`yield from other` passes every value of another iterable to the caller:

```python
def flatten(rows):
    for row in rows:
        yield from row

print(list(flatten([[1, 2], [3], []])))   # [1, 2, 3]
```

## 6. itertools

```python
import itertools

print(list(itertools.islice(countdown(100), 3)))        # [100, 99, 98]
print(list(itertools.chain("ab", [1, 2])))              # ['a', 'b', 1, 2]
print(list(itertools.pairwise([1, 4, 9, 16])))          # [(1, 4), (4, 9), (9, 16)]
print(list(itertools.accumulate([1, 2, 3, 4])))         # [1, 3, 6, 10]
print(list(itertools.batched(range(7), 3)))             # [(0, 1, 2), (3, 4, 5), (6,)]
```

- `islice(it, n)` takes the first `n` items without reading further. It is how you cut an endless generator.
- `batched` (Python 3.12+) splits a stream into tuples of a given size. It is the usual way to send work in chunks.
- `groupby` groups **neighbouring** items with the same key, so sort first if the data is not already grouped:

```python
words = ["apple", "avocado", "banana", "blueberry", "cherry"]
for letter, group in itertools.groupby(words, key=lambda w: w[0]):
    print(letter, list(group))
```

```text
a ['apple', 'avocado']
b ['banana', 'blueberry']
c ['cherry']
```

`heapq.merge` combines streams that are already sorted, lazily:

```python
import heapq
print(list(heapq.merge([1, 4, 9], [2, 3, 10])))   # [1, 2, 3, 4, 9, 10]
```

## 7. Lazy pipelines

Each stage is a generator that reads from the previous one. Only one item is in memory at a time, which is why this style handles huge log files:

```python
def lines_with(lines, word):
    for line in lines:
        if word in line:
            yield line.upper()

log = "ok 1\nerror disk\nok 2\nerror net"
print(list(lines_with(log.splitlines(), "error")))
```

```text
['ERROR DISK', 'ERROR NET']
```

With a real file, pass the open file object itself: `lines_with(open("app.log", encoding="utf-8"), "error")`. A file is an iterator over its lines, so a 10 GB log works the same way as this three-line one.

## 8. send and close (briefly)

A generator can also **receive** values. `send(x)` resumes the generator and makes the paused `yield` evaluate to `x`:

```python
def running_average():
    total = 0
    count = 0
    average = None
    while True:
        value = yield average
        total += value
        count += 1
        average = total / count

ra = running_average()
next(ra)                                  # run to the first yield
print(ra.send(10), ra.send(20), ra.send(60))
ra.close()                                # stop it
```

```text
10.0 15.0 30.0
```

You will rarely need `send`. It matters as background for `async` code in later topics.

<div class="box warn" markdown="1">

## Common mistakes

- **Using a generator twice.** The second loop sees nothing. Call the generator function again, or store the results in a list.
- **Using `return` where you meant `yield`.** The function then produces one value (or none) instead of a stream.
- **Expecting `len()` or indexing on a generator.** Neither works. Convert with `list()` if you need them, but only when the data is small.
- **`groupby` on unsorted data.** It starts a new group every time the key changes.
- **Calling `list()` on an endless generator.** It never returns and uses all memory. Cut it with `islice` first.

</div>

<div class="box" markdown="1">

## Where this appears in AI agents

Model APIs can **stream** a reply: the text arrives in many small chunks instead of one block. Code that reads such a stream is a loop over a generator (an async one, see topic 34). Generators also batch documents before sending them to an embedding API, and they read large log or data files one line at a time.

```python
def chunks_of_text(text, size):
    for start in range(0, len(text), size):
        yield text[start:start + size]
```

</div>

## Try it yourself

1. Write a generator `evens(limit)` that yields the even numbers below `limit`. Print `list(evens(10))`.
2. Write a generator `fibonacci()` that never ends. Print the first ten values with `itertools.islice`.
3. Use a generator expression to sum the lengths of all words in a sentence.

## Further reading

- [Iterator types](https://docs.python.org/3/library/stdtypes.html#iterator-types)
- [itertools](https://docs.python.org/3/library/itertools.html)
- [Generators](https://docs.python.org/3/howto/functional.html#generators)

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="28-iterators-generators:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/28-iterators-generators/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/28-iterators-generators/assignments/' | relative_url }}).
