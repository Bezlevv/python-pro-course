---
title: pandas: advanced techniques
summary: Merge, concat, pivot, melt, groupby aggregations, time series.
order: 11
duration: 60 min
difficulty: advanced
tags: pandas, merge, pivot, groupby, timeseries
---

Beyond basics: combining, reshaping and aggregating data efficiently.

## Merge

```python
import pandas as pd
orders = pd.DataFrame({"user_id": [1, 2], "total": [100, 200]})
users = pd.DataFrame({"user_id": [1, 2], "name": ["Anna", "Boris"]})
merged = pd.merge(orders, users, on="user_id")
```

## concat

```python
df = pd.concat([df1, df2], ignore_index=True)
```

## pivot / melt

```python
wide = sales.pivot(index="date", columns="product", values="revenue")
long = wide.reset_index().melt(id_vars="date")
```

## groupby aggregations

```python
df.groupby("category")["price"].agg(["count", "mean", "sum"])
```

## Time series

```python
df["date"] = pd.to_datetime(df["date"])
df.set_index("date", inplace=True)
df.resample("M").sum()
```

## Lesson summary

Advanced pandas: join, reshape, multi-metrics groupby, time series.

<!--TASK-->
### Task 1 — Merge
Merge two DataFrames on a key; print columns.

### Task 2 — Left join
Use how="left" and show NaN for missing.

### Task 3 — concat
Concatenate two frames vertically; reset index.

### Task 4 — pivot
Pivot sales by date/product/revenue.

### Task 5 — melt
Melt the wide table back to long form.

### Task 6 — groupby agg
Aggregate count/mean/sum per category.

### Task 7 — resample
Create a daily series and resample by week with sum.
<!--/TASK-->

<!--HINT-->
### Hint 1
pd.merge(a, b, on="key").

### Hint 2
how="left".

### Hint 3
pd.concat([a, b], ignore_index=True).

### Hint 4
df.pivot(index=..., columns=..., values=...).

### Hint 5
melt(id_vars=...).

### Hint 6
groupby("c").agg([...]).

### Hint 7
set_index + resample("W").sum().
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
merged = pd.merge(orders, users, on="user_id")
print(merged)
```

### Solution 2
```python
merged = pd.merge(orders, users, on="user_id", how="left")
print(merged)
```

### Solution 3
```python
df = pd.concat([df1, df2], ignore_index=True)
```

### Solution 4
```python
wide = sales.pivot(index="date", columns="product", values="revenue")
```

### Solution 5
```python
long = wide.reset_index().melt(id_vars="date", value_name="revenue")
```

### Solution 6
```python
out = df.groupby("category")["price"].agg(["count", "mean", "sum"])
print(out)
```

### Solution 7
```python
s = pd.Series(range(14), index=pd.date_range("2026-01-01", periods=14))
print(s.resample("W").sum())
```
<!--/SOLUTION-->

<!--QUIZ-->
What does merge do?
- Combines by key
- Concatenates rows
- Pivots
- Filters
* Correct answer: Combines by key
SQL-like join.

What is how="left"?
- Keeps left rows
- Inner
- Outer
- Right
* Correct answer: Keeps left rows
Left join.

What does concat do?
- Stacks frames
- Merges
- Pivots
- Sorts
* Correct answer: Stacks frames
Rows/columns.

What does pivot do?
- Makes wide table
- Long
- Merge
- Filter
* Correct answer: Makes wide table
Index/columns/values.

What does melt do?
- Makes long table
- Wide
- Merge
- Copy
* Correct answer: Makes long table
Tidy.

What does groupby("c").agg(...) do?
- Multi-metric summary
- Sorts
- Filters
- Plots
* Correct answer: Multi-metric summary
Per group.

What does resample("W") do?
- Weekly aggregation
- Daily
- Monthly
- Filter
* Correct answer: Weekly aggregation
Time window.

What is id_vars?
- Columns kept in melt
- Values
- Index
- Keys
* Correct answer: Columns kept in melt
Identifiers.

What does ignore_index=True do?
- Resets index
- Keeps
- Sorts
- Drops
* Correct answer: Resets index
0..n.

What is to_datetime?
- Converts to datetime
- Formats
- Parses string
- None
* Correct answer: Converts to datetime
Type conversion.

What is set_index?
- Sets index column
- Resets
- Drops
- Sorts
* Correct answer: Sets index column
For resample.

How to combine frames vertically?
- pd.concat
- pd.merge
- df.join
- pivot
* Correct answer: pd.concat
axis 0 default.
<!--/QUIZ-->
