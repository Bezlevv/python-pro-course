---
title: Data cleaning and analysis
summary: Missing values, duplicates, types, normalization and basic analysis.
order: 4
duration: 45 min
difficulty: intermediate
tags: pandas, cleaning, missing, duplicates
---

Real data is messy: missing values, duplicates, wrong types.

## Inspect

```python
df.head()
df.info()
df.describe()
```

## Missing values

```python
df.isna().sum()
df.dropna()
df.fillna(0)
```

## Duplicates

```python
df.duplicated().sum()
df.drop_duplicates()
```

## Types

```python
df["age"] = df["age"].astype(int)
```

## Cleanup helpers

```python
df["price"].str.strip()
df["name"].str.lower()
```

## Lesson summary

Cleaning steps: inspect, handle NaN, drop duplicates, fix types.

<!--TASK-->
### Task 1 — Create messy data
Create a DataFrame with NaN, duplicates and string numbers.

### Task 2 — Inspect
Show head, info, describe.

### Task 3 — Count missing
Count NaN per column with isna().sum().

### Task 4 — Fill
Fill NaN with 0 and with forward fill (method="ffill").

### Task 5 — Duplicates
Count duplicates and remove them.

### Task 6 — Type conversion
Convert the numeric column from strings to int.

### Task 7 — Clean text
Strip and lowercase a name column.
<!--/TASK-->

<!--HINT-->
### Hint 1
Include None values.

### Hint 2
df.head(); df.info().

### Hint 3
df.isna().sum().

### Hint 4
df.fillna(0); df.fillna(method="ffill").

### Hint 5
df.drop_duplicates().

### Hint 6
astype(int) after cleaning.

### Hint 7
df["name"].str.strip().str.lower().
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import pandas as pd
df = pd.DataFrame({
    "name": ["Anna", "Boris", "Anna", None],
    "age": ["21", "30", "21", "40"],
})
```

### Solution 2
```python
print(df.head())
print(df.info())
print(df.describe())
```

### Solution 3
```python
print(df.isna().sum())
```

### Solution 4
```python
print(df.fillna(0))
print(df.fillna(method="ffill"))
```

### Solution 5
```python
print(df.duplicated().sum())
clean = df.drop_duplicates()
```

### Solution 6
```python
df["age"] = df["age"].astype(int)
print(df.dtypes)
```

### Solution 7
```python
df["name"] = df["name"].str.strip().str.lower()
print(df)
```
<!--/SOLUTION-->

<!--QUIZ-->
What does isna() do?
- Flags missing values
- Fills
- Removes
- Counts
* Correct answer: Flags missing values
Boolean mask.

What does dropna() do?
- Removes rows with NaN
- Fills
- Sorts
- Copies
* Correct answer: Removes rows with NaN
Filter.

What does fillna(0) do?
- Replaces NaN with 0
- Removes
- Counts
- Errors
* Correct answer: Replaces NaN with 0
Impute.

What does duplicated() show?
- Duplicate rows
- Missing
- Sorted
- Types
* Correct answer: Duplicate rows
Boolean.

What does drop_duplicates do?
- Removes duplicates
- Adds
- Sorts
- Counts
* Correct answer: Removes duplicates
Keeps first.

What does astype(int) do?
- Converts type
- Rounds
- Sorts
- Deletes
* Correct answer: Converts type
Cast.

Why clean text?
- Consistency
- Speed
- Rename
- Plot
* Correct answer: Consistency
strip/lower.

What does info() show?
- Columns, types, nulls
- Data
- Plot
- Sum
* Correct answer: Columns, types, nulls
Overview.

What does str.strip() do?
- Removes edge spaces
- Lowercases
- Splits
- Joins
* Correct answer: Removes edge spaces
String method.

What does str.lower() do?
- Lowercases
- Strips
- Splits
- Replaces
* Correct answer: Lowercases
Normalize.

What is ffill?
- Forward fill
- Backward
- Drop
- Count
* Correct answer: Forward fill
Copies previous value.

Why drop duplicates?
- Data integrity
- Faster
- Required
- None
* Correct answer: Data integrity
Avoid bias.
<!--/QUIZ-->
