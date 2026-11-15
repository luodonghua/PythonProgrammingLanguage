---
layout: module
module: 24-data-science
kind: assignments
title: "Data science basics - assignments"
permalink: /modules/24-data-science/assignments/
---
Four tasks with small CSV files. You load, filter, summarise, clean and plot data with pandas and matplotlib. The tests check exact values, so read each docstring for the rules (rounding, sort order, index).

{% include practice-setup.md %}

These tasks need two third-party libraries. Install them once in your project:

```bash
uv add pandas matplotlib
```

Data files sit next to each starter in the assignment folder and are loaded through `Path(__file__).parent`, so you can run the tests from any directory. The charts in assignment 4 are drawn with the `Agg` backend, so no window opens.

Run all tests for this topic:

```bash
uv run pytest modules/24-data-science
```

---

<div class="assignment" markdown="1">

## Assignment 1: Top movies

**Goal:** Load a CSV, return the top N rows by a column and list the titles that pass two filters. Practises `read_csv`, `sort_values`, `head` and boolean masks.

**Files:** [`starter.py`]({{ 'modules/24-data-science/assignments/a1-top-movies/starter.py' | relative_url }}), test file `test_a1_top_movies.py` in the same folder. Data file: `movies.csv`.

```python
{% include_relative assignments/a1-top-movies/starter.py %}
```

Run: `uv run pytest modules/24-data-science/assignments/a1-top-movies`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-top-movies/solution.py %}
```

`kind="stable"` keeps tied rows in their original order, so the result is the same on every run. The mask uses `&` with parentheses around each comparison.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Orders by category and customer

**Goal:** Add a computed column and summarise orders with `groupby` and `agg`. Practises new columns, sorting with several keys, and returning plain Python values.

**Files:** [`starter.py`]({{ 'modules/24-data-science/assignments/a2-orders/starter.py' | relative_url }}), test file `test_a2_orders.py` in the same folder. Data file: `orders.csv`.

```python
{% include_relative assignments/a2-orders/starter.py %}
```

Run: `uv run pytest modules/24-data-science/assignments/a2-orders`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-orders/solution.py %}
```

`df.assign(...)` returns a new DataFrame, so the input stays unchanged. Named aggregation (`orders=("order_id", "count")`) gives clear column names. Sorting by `[total, name]` with `ascending=[False, True]` makes ties predictable.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Clean sensor data

**Goal:** Report missing values, then clean a table by dropping bad rows, removing duplicates and filling gaps with group means and a median. Practises `isna`, `dropna`, `drop_duplicates`, `fillna` and `groupby().transform`.

**Files:** [`starter.py`]({{ 'modules/24-data-science/assignments/a3-clean-sensors/starter.py' | relative_url }}), test file `test_a3_clean_sensors.py` in the same folder. Data file: `sensors.csv`.

```python
{% include_relative assignments/a3-clean-sensors/starter.py %}
```

Run: `uv run pytest modules/24-data-science/assignments/a3-clean-sensors`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-clean-sensors/solution.py %}
```

The order of the steps matters, because the median and the station means are computed after the bad and duplicate rows are gone. `transform("mean")` returns one value per row, so it can be passed straight to `fillna`.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Merge tables and draw a chart

**Goal:** Join scores to students, compute class averages and each student's best subject, then save a bar chart as a PNG. Practises `merge`, `groupby`, `idxmax` and matplotlib with the `Agg` backend.

**Files:** [`starter.py`]({{ 'modules/24-data-science/assignments/a4-scores-chart/starter.py' | relative_url }}), test file `test_a4_scores_chart.py` in the same folder. Data files: `scores.csv` and `students.csv`.

```python
{% include_relative assignments/a4-scores-chart/starter.py %}
```

Run: `uv run pytest modules/24-data-science/assignments/a4-scores-chart`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-scores-chart/solution.py %}
```

`idxmax` gives the index label of the highest score in each group, and `loc` turns those labels into rows. The chart function closes its figure with `plt.close(fig)`, so repeated calls do not pile up open figures.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="24-data-science:assignments"> I have finished the assignments</label></li>
</ul>
