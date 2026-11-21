---
title: Pandas: DataFrame and reading data
summary: Creating DataFrames, reading CSV, selecting columns, filtering, groupby.
order: 3
duration: 40 min
difficulty: intermediate
tags: pandas, dataframe, csv, groupby
---

A DataFrame is a 2D labeled table.

## Create

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Anna", "Boris"],
    "age": [21, 30],
})
```

## Read/write CSV

```python
df.to_csv("data.csv", index=False)
df = pd.read_csv("data.csv")
```

## Selecting

```python
df["name"]           # column
df[["name", "age"]]
df.iloc[0]           # row by position
df.loc[0]            # row by label
```

## Filtering

```python
df[df["age"] > 25]
```

## Summaries

```python
df.info()
df.describe()
df["age"].mean()
```

## groupby

```python
df.groupby("city")["age"].mean()
```

## Lesson summary

DataFrame: rows/columns, CSV IO, selection, filtering, summaries.

<!--TASK-->
### Task 1 — Create DataFrame
Create a DataFrame with name, city, age for 4 rows.

### Task 2 — Columns
Print one column, two columns, and df.shape.

### Task 3 — Rows
Select first and second row via iloc; select by label with loc.

### Task 4 — Filter
Filter rows where age >= 25; then where city == "Moscow".

### Task 5 — CSV
Save to CSV, read it back, compare shape.

### Task 6 — Statistics
Show df.describe() and the mean age.

### Task 7 — groupby
Group by city and compute mean age per city.
<!--/TASK-->

<!--HINT-->
### Hint 1
pd.DataFrame({...}).

### Hint 2
df["name"]; df[["name","age"]]; df.shape.

### Hint 3
df.iloc[0]; df.loc[0].

### Hint 4
df[df["age"] >= 25].

### Hint 5
to_csv; read_csv.

### Hint 6
df.describe(); df["age"].mean().

### Hint 7
df.groupby("city")["age"].mean().
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import pandas as pd
df = pd.DataFrame({
    "name": ["Anna", "Boris", "Vika", "Ivan"],
    "city": ["Moscow", "SPb", "Moscow", "Kazan"],
    "age": [21, 30, 19, 40],
})
print(df)
```

### Solution 2
```python
print(df["name"])
print(df[["name", "age"]])
print(df.shape)
```

### Solution 3
```python
print(df.iloc[0])
print(df.iloc[1])
print(df.loc[0])
```

### Solution 4
```python
print(df[df["age"] >= 25])
print(df[df["city"] == "Moscow"])
```

### Solution 5
```python
df.to_csv("data.csv", index=False)
df2 = pd.read_csv("data.csv")
print(df2.shape)
```

### Solution 6
```python
print(df.describe())
print(df["age"].mean())
```

### Solution 7
```python
print(df.groupby("city")["age"].mean())
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a DataFrame?
- 2D labeled table
- Series
- List
- CSV
* Correct answer: 2D labeled table
Rows/columns.

How to select a column?
- df["name"]
- df.name? both
- df[0]
- df(0)
* Correct answer: df["name"]
Column by name.

What is iloc?
- Position-based selection
- Label-based
- Filter
- Copy
* Correct answer: Position-based selection
Integer positions.

What is loc?
- Label-based selection
- Position
- Boolean
- None
* Correct answer: Label-based selection
Index labels.

How to filter?
- df[df["age"] > 25]
- df > 25
- df.filter()
- df.where all
* Correct answer: df[df["age"] > 25]
Boolean mask.

What does df.shape return?
- (rows, columns)
- Values
- Size
- Index
* Correct answer: (rows, columns)
Tuple.

What does describe do?
- Summary statistics
- Prints all
- Sorts
- Counts
* Correct answer: Summary statistics
mean/std/min/...

What does groupby do?
- Aggregates groups
- Sorts
- Merges
- Renames
* Correct answer: Aggregates groups
Split-apply-combine.

How to read CSV?
- pd.read_csv("data.csv")
- open()
- csv.read
- df.read
* Correct answer: pd.read_csv("data.csv")
Pandas reader.

What does to_csv(index=False) do?
- Saves without index column
- Saves with
- Prints
- Deletes
* Correct answer: Saves without index column
Cleaner.

What does df.info() show?
- Data types and memory
- Sum
- Plot
- Unique
* Correct answer: Data types and memory
Overview.

What does copy["age"].mean() give?
- Average of column
- Sum
- Count
- Max
* Correct answer: Average of column
Column statistic.
<!--/QUIZ-->
