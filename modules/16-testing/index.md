---
layout: module
module: 16-testing
kind: learn
title: Testing with pytest
permalink: /modules/16-testing/
---

<div class="box key" markdown="1">

## Key learning points

- A **test** is code that calls your code and checks the result with `assert`. Tests find bugs early and let you change code with confidence.
- pytest finds files named `test_*.py` and functions named `test_*`. Run them with `uv run pytest`.
- `@pytest.mark.parametrize` runs one test with many inputs. `pytest.raises` checks that an error happens.
- A **fixture** prepares something a test needs (`tmp_path` gives a clean temporary folder). `monkeypatch` swaps things such as `input` or environment variables for one test.
- Structure each test as **arrange, act, assert**. Test behaviour and edge cases, not how the code is written inside.
- **TDD**: write a failing test, make it pass with the simplest code, then clean up.

</div>

## 1. Your first test

Suppose `cart.py` holds this function:

```python
def total(prices, discount=0.0):
    if not 0 <= discount <= 1:
        raise ValueError("discount must be between 0 and 1")
    return round(sum(prices) * (1 - discount), 2)
```

Put tests in `test_cart.py`, next to it:

```python
from cart import total


def test_total_adds_prices():
    assert total([10, 5]) == 15


def test_total_empty_cart_is_zero():
    assert total([]) == 0
```

Run `uv run pytest`. A passing run prints a dot per test:

```text
..                                                                   [100%]
2 passed in 0.04s
```

pytest rewrites `assert` so that a failure shows the values. If the expected value were wrong:

```python
def test_wrong():
    assert total([1, 2]) == 4
```

```text
    def test_wrong():
>       assert total([1, 2]) == 4
E       assert 3.0 == 4
E        +  where 3.0 = total([1, 2])

test_fail.py:3: AssertionError
1 failed in 0.11s
```

Use plain `assert`. There is no need for `assertEqual` and friends.

## 2. Arrange, act, assert

```python
def test_discount_is_applied():
    prices = [100]                 # arrange: set up the input
    result = total(prices, 0.1)    # act: call the code once
    assert result == 90            # assert: check the outcome
```

One test should check one behaviour. A clear name (`test_total_empty_cart_is_zero`) tells you what broke without reading the body.

## 3. Many inputs with parametrize

```python
import pytest

@pytest.mark.parametrize(
    ("prices", "discount", "expected"),
    [
        ([100], 0.1, 90),
        ([10, 10], 0.5, 10),
        ([19.99], 0, 19.99),
    ],
)
def test_total_with_discount(prices, discount, expected):
    assert total(prices, discount) == expected
```

pytest runs the function three times and reports each case separately (`test_total_with_discount[prices0-0.1-90]` and so on).

## 4. Testing errors

```python
def test_bad_discount_raises():
    with pytest.raises(ValueError, match="between 0 and 1"):
        total([1], 2)
```

The test passes only if the block raises `ValueError` and the message matches the pattern.

## 5. Fixtures and tmp_path

A fixture is a function marked `@pytest.fixture`. A test asks for it by naming it as a parameter. Each test gets a fresh value.

```python
import json
import pytest

@pytest.fixture
def config_file(tmp_path):
    path = tmp_path / "config.json"
    path.write_text(json.dumps({"debug": True}))
    return path

def test_reads_config(config_file):
    assert json.loads(config_file.read_text())["debug"] is True
```

`tmp_path` is built into pytest. It is a `pathlib.Path` to a new temporary folder, so tests never touch your real files.

A fixture can also clean up. Code after `yield` runs after the test:

```python
@pytest.fixture
def numbers():
    print("setup")
    yield [3, 1, 2]
    print("teardown")
```

## 6. monkeypatch and capsys

```python
def test_env(monkeypatch):
    import os
    monkeypatch.setenv("APP_MODE", "test")
    assert os.environ["APP_MODE"] == "test"

def test_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt="": "Ann")
    assert input("name? ") == "Ann"

def test_prints(capsys):
    print("hi")
    assert capsys.readouterr().out == "hi\n"
```

`monkeypatch` undoes every change when the test ends. `capsys` captures what the code prints, so you can check it. Design code so that it takes parameters (a file path, an `input_fn`) and these tricks are rarely needed.

## 7. Markers: skip and xfail

```python
@pytest.mark.skip(reason="not written yet")
def test_later(): ...

@pytest.mark.xfail(reason="known bug")
def test_known_bug():
    assert 1 == 2
```

The summary then reads `s` for skipped and `x` for an expected failure. Use `skipif(condition, reason=...)` for tests that only make sense on some systems.

## 8. What to test, and the TDD loop

- The normal case, the **edges** (empty input, zero, one item, the maximum), and the **errors**.
- Each bug you fix gets a test first, so it cannot come back.
- Do not test Python itself, and do not test private details. A test should survive a rewrite that keeps the behaviour.
- Tests must be fast, repeatable and independent. Do not rely on the clock, the network or the order of tests.

The **TDD** loop has three steps:

1. **Red:** write a small failing test for the next behaviour.
2. **Green:** write the simplest code that passes.
3. **Refactor:** clean up while the tests stay green.

Tests are only worth trusting if they can fail. A useful check is to break the code on purpose and see whether a test notices. That is the idea of the "write your own tests" assignment.

<div class="box warn" markdown="1">

## Common mistakes

- **A test file or function without the `test_` prefix.** pytest silently ignores it. Check that the count of tests is what you expect.
- **Tests that depend on each other or on order.** Each test must set up its own data.
- **Comparing floats with `==`.** Use `pytest.approx(0.3)` for results such as `0.1 + 0.2`.
- **Asserting too little or too much.** `assert result` passes for almost anything. Checking a whole long string makes tests fragile.
- **Writing to real paths or reading real input.** Use `tmp_path` and `monkeypatch`.

</div>

## Try it yourself

1. Write a function `is_palindrome(text)` and four tests for it, including an empty string.
2. Turn those tests into one `parametrize` test.
3. Do TDD for `fizzbuzz(n)`: write the failing test for 3, make it pass, then add 5 and 15.

## Where this comes from

*Introducing Python*, chapter 15 (Testing). *Learn Python the Hard Way*, exercise 47 (automated testing). The [pytest documentation](https://docs.pytest.org/en/stable/getting-started.html) is the best reference.

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="16-testing:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/16-testing/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/16-testing/assignments/' | relative_url }}).
