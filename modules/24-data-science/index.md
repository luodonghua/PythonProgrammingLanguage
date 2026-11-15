---
layout: module
module: 24-data-science
kind: learn
title: Data science basics
permalink: /modules/24-data-science/
---

<div class="box key" markdown="1">

## Key learning points

- A pandas **Series** is one labelled column. A **DataFrame** is a table of Series that share an index.
- `pd.read_csv` loads a CSV file into a DataFrame. `df.head()`, `df.shape` and `df.describe()` give a first look.
- Select columns with `df["name"]`. Filter rows with a **boolean mask**: `df[df["units"] > 4]`. Combine masks with `&`, `|` and `~`, each condition in parentheses.
- `groupby(...).agg(...)` summarises per group. `merge` joins two tables on a shared column.
- Missing values appear as `NaN`. Find them with `isna()`, then fill them with `fillna()` or remove rows with `dropna()`.
- matplotlib draws charts. Use the `Agg` backend and `fig.savefig(...)` to write an image file without opening a window.

</div>

pandas and matplotlib are third-party packages. Install them with `uv add pandas matplotlib`. The outputs below were produced with pandas 3.1 and matplotlib 3.11. Other versions can format some output slightly differently.

## 1. Series and DataFrame

```python
import pandas as pd

s = pd.Series([10, 5, 3], index=["Mon", "Tue", "Wed"])
print(s["Tue"], s.sum(), s.mean())   # 5 18 6.0
print(s * 2)
```

```text
Mon    20
Tue    10
Wed     6
dtype: int64
```

Arithmetic applies to every element at once. This is called **vectorised** arithmetic, and it replaces most `for` loops over rows.

## 2. Reading a CSV file

Here the CSV text is inline, so the example runs anywhere. With a real file you would write `pd.read_csv("sales.csv")`.

```python
import io
import pandas as pd

csv_text = """date,region,product,units,price
2024-01-05,North,Pen,10,1.5
2024-01-06,South,Pen,5,1.5
2024-01-06,North,Notebook,3,4.0
2024-01-07,East,Notebook,,4.0
2024-01-08,South,Ink,2,7.25
2024-01-09,East,Pen,8,1.5
"""
df = pd.read_csv(io.StringIO(csv_text))
print(df.shape)              # (6, 5)  rows, columns
print(df.head(3))
print(df.columns.tolist())
```

```text
         date region   product  units  price
0  2024-01-05  North       Pen   10.0    1.5
1  2024-01-06  South       Pen    5.0    1.5
2  2024-01-06  North  Notebook    3.0    4.0
['date', 'region', 'product', 'units', 'price']
```

The empty `units` cell on row 3 became `NaN`. A column with `NaN` is stored as `float`, which is why `units` shows `10.0` and not `10`.

## 3. Selecting and filtering

```python
print(df[df["units"] > 4])
print(df[(df["region"] == "East") & (df["price"] < 5)])
print(df.loc[2, "product"], df.iloc[0, 1])   # Notebook North
```

```text
         date region product  units  price
0  2024-01-05  North     Pen   10.0    1.5
1  2024-01-06  South     Pen    5.0    1.5
5  2024-01-09   East     Pen    8.0    1.5
         date region   product  units  price
3  2024-01-07   East  Notebook    NaN    4.0
5  2024-01-09   East     Pen    8.0    1.5
```

`df["units"] > 4` makes a column of `True` and `False`. Putting it inside `df[...]` keeps the `True` rows. Use `&` and `|`, not `and` and `or`, and wrap each condition in parentheses. `loc` selects by label and `iloc` by position. A comparison with `NaN` is `False`, so row 3 is not in the first result.

## 4. New columns and sorting

```python
df["revenue"] = df["units"] * df["price"]
print(df.sort_values("revenue", ascending=False).head(2))
```

```text
         date region product  units  price  revenue
0  2024-01-05  North     Pen   10.0   1.50     15.0
4  2024-01-08  South     Ink    2.0   7.25     14.5
```

## 5. Missing data

```python
print(df.isna().sum())
print(df["units"].fillna(0).tolist())   # [10.0, 5.0, 3.0, 0.0, 2.0, 8.0]
print(df.dropna().shape)                # (5, 6)
```

```text
date       0
region     0
product    0
units      1
price      0
revenue    1
dtype: int64
```

`fillna(0)` replaces each `NaN` with 0. `dropna()` removes every row that has a `NaN`. Decide which is right for your data. Filling with 0 changes an average, and dropping rows loses information. Also note that `sum()` and `mean()` skip `NaN` by default.

## 6. Group, aggregate, merge

```python
print(df.groupby("region")["revenue"].sum())
print(df.groupby("product").agg(total_units=("units", "sum"), avg_price=("price", "mean")))
```

```text
region
East     12.0
North    27.0
South    22.0
Name: revenue, dtype: float64
          total_units  avg_price
product                         
Ink               2.0       7.25
Notebook          3.0       4.00
Pen              23.0       1.50
```

`groupby` splits the rows by a column, `agg` computes one summary per group. In `agg`, each keyword names an output column and gets a pair `(column, function)`.

```python
cats = pd.DataFrame({"product": ["Pen", "Notebook", "Ink"],
                     "category": ["Writing", "Paper", "Writing"]})
merged = df.merge(cats, on="product", how="left")
print(merged[["product", "category"]].head(3))
```

```text
    product category
0       Pen  Writing
1       Pen  Writing
2  Notebook    Paper
```

`how="left"` keeps every row of `df` and adds the matching `category`. The other common choices are `inner` (only matching rows), `right` and `outer`.

To get a quick statistical summary of numeric columns, call `describe()`:

```python
print(df[["units", "price"]].describe())
```

```text
           units     price
count   5.000000  6.000000
mean    5.600000  3.291667
std     3.361547  2.293560
min     2.000000  1.500000
25%     3.000000  1.500000
50%     5.000000  2.750000
75%     8.000000  4.000000
max    10.000000  7.250000
```

## 7. A chart with matplotlib

```python
import matplotlib
matplotlib.use("Agg")            # draw to files, no window needed
import matplotlib.pyplot as plt

totals = df.groupby("region")["revenue"].sum()
fig, ax = plt.subplots()
totals.plot.bar(ax=ax)
ax.set_title("Revenue by region")
ax.set_ylabel("Revenue")
fig.savefig("revenue.png")
plt.close(fig)                   # free the memory
```

`Agg` is a backend that renders to image files. Call `matplotlib.use("Agg")` before importing `pyplot`. This works on servers and in tests, where no screen exists. Always label axes and give the chart a title.

<div class="box warn" markdown="1">

## Common mistakes

- **`and` / `or` in a filter.** `df[df.a > 1 and df.b < 2]` raises `ValueError`. Write `df[(df.a > 1) & (df.b < 2)]`.
- **Forgetting parentheses** around each condition. `&` binds tighter than `>`.
- **Changing a copy by accident.** `df[df["a"] > 1]["b"] = 0` does not reliably change `df`. Use `df.loc[df["a"] > 1, "b"] = 0`.
- **Dropping or filling `NaN` without thinking.** Both change your results. Count missing values with `isna().sum()` first.
- **Looping over rows** with `for` when a vectorised column operation or `groupby` does the job in one line.

</div>

## Try it yourself

1. Load the CSV above. Print the three rows with the highest `price` using `sort_values` and `head`.
2. Compute total `units` per `product` and print the product with the highest total.
3. Make a bar chart of total `units` per `region`, give it a title, and save it as `units.png`.

## Where this comes from

*Introducing Python*, chapter 25 (Data Science). *Learn Python the Hard Way* does not cover pandas, so this topic goes beyond that book; see the [pandas user guide](https://pandas.pydata.org/docs/user_guide/index.html) and the [matplotlib tutorials](https://matplotlib.org/stable/tutorials/index.html).

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="24-data-science:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/24-data-science/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/24-data-science/assignments/' | relative_url }}).
