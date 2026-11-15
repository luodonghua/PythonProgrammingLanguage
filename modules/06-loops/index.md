---
layout: module
module: 06-loops
kind: learn
title: Loops
permalink: /modules/06-loops/
---

<div class="box key" markdown="1">

## Key learning points

- `for item in sequence:` visits each item once. Use it when you know what to loop over.
- `range(stop)`, `range(start, stop)` and `range(start, stop, step)` make counting sequences. The **stop value is never included**.
- `enumerate(seq, start=1)` gives `(index, item)` pairs. `zip(a, b)` walks two sequences together and stops at the shorter one.
- `while condition:` repeats as long as the condition is true. Something inside the loop must change the condition.
- `break` leaves the loop. `continue` skips to the next item. A loop's `else` block runs only if the loop **did not** hit `break`.
- The **accumulator pattern** (start a variable, update it in the loop, use it after) solves sums, counts, maximums and lists.

</div>

## 1. for loops

```python
for fruit in ["apple", "pear"]:
    print(fruit)
```

```text
apple
pear
```

You can loop over anything iterable: a list, a string, a `range`, a dictionary, a file. Strings give one character at a time:

```python
for ch in "abc":
    print(ch, end=" ")    # a b c
```

`print(..., end=" ")` replaces the final new line with a space.

## 2. range

```python
print(list(range(5)))          # [0, 1, 2, 3, 4]
print(list(range(2, 8, 2)))    # [2, 4, 6]
print(list(range(5, 0, -1)))   # [5, 4, 3, 2, 1]
print(list(range(0)))          # []
```

`range(1, 5)` has `5 - 1 = 4` items. `list(...)` is only for showing the values. A `range` takes almost no memory, even for `range(10_000_000)`.

## 3. enumerate and zip

```python
for i, fruit in enumerate(["a", "b"], start=1):
    print(i, fruit)
```

```text
1 a
2 b
```

```python
names = ["Ann", "Bob", "Cy"]
ages = [30, 25]
for name, age in zip(names, ages):
    print(name, age)
```

```text
Ann 30
Bob 25
```

`zip` stops at the shortest input, so `"Cy"` is dropped without any error. Prefer `enumerate` over `range(len(items))`.

## 4. Accumulator patterns

```python
total = 0
for n in range(1, 6):
    total += n
print(total)        # 15
```

```python
words = ["a", "bb", "ccc"]
longest = ""
for word in words:
    if len(word) > len(longest):
        longest = word
print(longest)      # ccc
```

```python
squares = []
for n in range(1, 6):
    squares.append(n * n)
print(squares)      # [1, 4, 9, 16, 25]
```

Three steps: **initialise** before the loop, **update** inside, **use** after. (For sums of numbers, `sum(range(1, 6))` is shorter, and you will meet list comprehensions in the next topics.)

## 5. while loops

```python
n = 3
while n > 0:
    print(n)
    n -= 1
print("liftoff")
```

```text
3
2
1
liftoff
```

If `n -= 1` were missing, the condition would stay true forever (an **infinite loop**). Press `Ctrl+C` to stop one. Use `while` when you do not know the number of repetitions in advance, such as reading input until it is valid.

## 6. break, continue and else

```python
for n in [3, 8, 12, 5]:
    if n > 10:
        print("found", n)
        break
else:
    print("none")
```

```text
found 12
```

The `else` belongs to the `for`. It runs only when the loop finishes **without** `break`. Here the loop broke at 12, so `"none"` is not printed.

```python
for n in range(6):
    if n % 2:          # odd numbers
        continue       # skip the rest of this round
    print(n, end=" ")  # 0 2 4
```

## 7. Nested loops

```python
for i in range(1, 4):
    for j in range(1, 4):
        print(i * j, end="\t")
    print()
```

```text
1	2	3	
2	4	6	
3	6	9	
```

The inner loop runs completely for every step of the outer loop: 3 x 3 = 9 rounds. A `break` only leaves the **innermost** loop. A function with `return` is the cleanest way to leave both.

## 8. Looping over a dictionary

```python
d = {"a": 1, "b": 2}
for key in d:
    print(key, end=" ")             # a b
for key, value in d.items():
    print(key, value, end="; ")     # a 1; b 2;
```

Dictionaries get their own topic. For now remember that a plain `for` gives the keys and `.items()` gives key and value.

## 9. Avoiding off-by-one errors

- `range(n)` gives `n` items from `0` to `n - 1`. For `1` to `n` write `range(1, n + 1)`.
- After the loop `for i in range(3)`, the variable `i` is still `2`.
- Test the edges: an empty list, one item, and the last item.

<div class="box warn" markdown="1">

## Common mistakes

- **Forgetting the stop value is excluded.** `range(1, 5)` stops at 4.
- **Changing a list while looping over it.** With `items = [2, 4, 6, 7]`, removing evens inside `for x in items:` leaves `[4, 7]`, because the loop skips items. Loop over a copy (`items[:]`) or build a new list.
- **An infinite `while`.** Check that the loop body moves the condition toward false.
- **`range(len(items))` for everything.** Use `for item in items` or `enumerate(items)`.
- **Expecting `zip` to complain about different lengths.** It silently stops at the shorter one.

</div>

## Try it yourself

1. Print the numbers from 10 down to 1 with `range`, then again with `while`.
2. Use a loop and an accumulator to compute the average of `[3, 9, 4]`.
3. Print a 5 x 5 grid of `*` characters with two nested loops.

## Where this comes from

*Introducing Python*, chapter 7 (For and While). *Learn Python the Hard Way*, exercises 32 and 33 (loops and lists, while loops).

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="06-loops:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/06-loops/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/06-loops/assignments/' | relative_url }}).
