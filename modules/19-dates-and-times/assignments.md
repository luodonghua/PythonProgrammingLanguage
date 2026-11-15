---
layout: module
module: 19-dates-and-times
kind: assignments
title: Dates and times - assignments
permalink: /modules/19-dates-and-times/assignments/
---
Four tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

Time zone names such as `America/New_York` need the IANA time zone database. Linux and macOS have it. On Windows, `uv sync` installs the `tzdata` package for you. If you see `ZoneInfoNotFoundError`, run `uv add tzdata`.

None of the tests depend on today's date. Your functions receive `today` as a parameter, so never call `date.today()` inside them.

Run all tests for this topic:

```bash
uv run pytest modules/19-dates-and-times
```

---

<div class="assignment" markdown="1">

## Assignment 1: Age and birthday calculator

**Goal:** Compute a person's age, the next birthday and the days until it, for a `today` that the caller passes in. Practises `date` comparison and subtraction, and the February 29 edge case.

**Files:** [`starter.py`]({{ 'modules/19-dates-and-times/assignments/a1-birthdays/starter.py' | relative_url }}), test file `test_a1_birthdays.py` in the same folder.

```python
{% include_relative assignments/a1-birthdays/starter.py %}
```

Run: `uv run pytest modules/19-dates-and-times/assignments/a1-birthdays`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-birthdays/solution.py %}
```

A small helper finds the date on which a birthday is celebrated in a given year. The age is the year difference, minus one if this year's anniversary has not happened yet. `next_birthday` tries this year first and moves to next year when that date is already past.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Business days

**Goal:** Count the business days between two dates and add business days to a date, skipping weekends and a set of holidays. Practises `weekday()`, `timedelta` and loops.

**Files:** [`starter.py`]({{ 'modules/19-dates-and-times/assignments/a2-business-days/starter.py' | relative_url }}), test file `test_a2_business_days.py` in the same folder.

```python
{% include_relative assignments/a2-business-days/starter.py %}
```

Run: `uv run pytest modules/19-dates-and-times/assignments/a2-business-days`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-business-days/solution.py %}
```

`date.weekday()` is 0 to 4 for Monday to Friday. The count steps over the range one day at a time with `timedelta(days=1)`. `add_business_days` moves forward one day and counts only the days that pass `is_business_day`, so weekends and holidays are skipped automatically.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Time zone conversion

**Goal:** Convert local times between IANA zones and measure real elapsed hours across a daylight saving change. Practises `zoneinfo`, `astimezone` and UTC arithmetic.

**Files:** [`starter.py`]({{ 'modules/19-dates-and-times/assignments/a3-time-zones/starter.py' | relative_url }}), test file `test_a3_time_zones.py` in the same folder.

```python
{% include_relative assignments/a3-time-zones/starter.py %}
```

Run: `uv run pytest modules/19-dates-and-times/assignments/a3-time-zones`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-time-zones/solution.py %}
```

`strptime` gives a naive value, so `.replace(tzinfo=ZoneInfo(zone))` says which zone it was in. `astimezone` then converts the moment. `elapsed_hours` converts both ends to UTC first, because subtracting two values in the same zone uses wall-clock time and would report 24 hours for a 23-hour day.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Parse log timestamps

**Goal:** Read timestamps from a web server log, skip broken lines, and report the busiest hour and the time span in UTC. Practises `strptime` with `%z`, `Counter` and error handling.

**Files:** [`starter.py`]({{ 'modules/19-dates-and-times/assignments/a4-log-timestamps/starter.py' | relative_url }}), test file `test_a4_log_timestamps.py` in the same folder. The log file `access.log` is in the same folder.

```python
{% include_relative assignments/a4-log-timestamps/starter.py %}
```

Run: `uv run pytest modules/19-dates-and-times/assignments/a4-log-timestamps`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-log-timestamps/solution.py %}
```

`%z` reads the offset, so `strptime` returns an aware value, and `astimezone(UTC)` puts every line on one clock. Lines that do not parse raise `ValueError` and are skipped. Truncating with `replace(minute=0, second=0, microsecond=0)` gives the hour bucket for the `Counter`.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="19-dates-and-times:assignments"> I have finished the assignments</label></li>
</ul>
