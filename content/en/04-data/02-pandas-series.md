---
title: Pandas: Series
summary: Creating Series, indexing, vectorized ops, NaN and methods.
order: 2
duration: 35 min
difficulty: intermediate
tags: pandas, series
---

A Series is a labeled one-dimensional array.

## Create

```python
import pandas as pd

s = pd.Series([10, 20, 30])
s = pd.Series([10, 20, 30], index=["a", "b", "c"])
```

## Access

```python
s["b"]
s[0]
s[["a", "c"]]
```

## Operations

```python
s + 5
s * 2
s.sum(), s.mean()
```

## NaN

```python
s = pd.Series([1, None, 3])
s.isna()
s.dropna()
s.fillna(0)
```

## Methods

```python
s.sort_values()
s.unique()
s.value_counts()
```

## Lesson summary

Series: labeled data with NumPy-backed operations.

<!--TASK-->
### Task 1 — Create
Create Series [5,10,15] with index ["x","y","z"]; print.

### Task 2 — Access
Print s["y"], s[0], s[["x","z"]].

### Task 3 — Vector ops
Compute s*2 and s+1; print.

### Task 4 — Summary
Print sum, mean, max, min, count.

### Task 5 — NaN handling
Create Series with None; show isna, dropna, fillna(0).

### Task 6 — Sorting
Sort ascending and show unique values.

### Task 7 — value_counts
For ["a","b","a","c","a"] count values.
<!--/TASK-->

<!--HINT-->
### Hint 1
pd.Series(data, index=...).

### Hint 2
Label or position access.

### Hint 3
Vectorized arithmetic.

### Hint 4
s.sum(); s.mean(); etc.

### Hint 5
None becomes NaN.

### Hint 6
s.sort_values(); s.unique().

### Hint 7
s.value_counts().
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import pandas as pd
s = pd.Series([5, 10, 15], index=["x", "y", "z"])
print(s)
```

### Solution 2
```python
print(s["y"])
print(s[0])
print(s[["x", "z"]])
```

### Solution 3
```python
print(s * 2)
print(s + 1)
```

### Solution 4
```python
print(s.sum(), s.mean(), s.max(), s.min(), s.count())
```

### Solution 5
```python
s2 = pd.Series([1, None, 3])
print(s2.isna())
print(s2.dropna())
print(s2.fillna(0))
```

### Solution 6
```python
print(s.sort_values())
print(s.unique())
```

### Solution 7
```python
s3 = pd.Series(["a", "b", "a", "c", "a"])
print(s3.value_counts())
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a Series?
- Labeled 1D array
- DataFrame
- List
- Set
* Correct answer: Labeled 1D array
Pandas structure.

How to label Series?
- index parameter
- columns
- keys
- fill
* Correct answer: index parameter
["a","b"].

How to access by label?
- s["b"]
- s[0] only
- s.b
- s(1)
* Correct answer: s["b"]
Label index.

What does s + 5 do?
- Adds 5 element-wise
- Errors
- Appends
- Rounds
* Correct answer: Adds 5 element-wise
Vectorized.

What is NaN?
- Missing value
- Zero
- Negative
- Text
* Correct answer: Missing value
Not a Number.

What does dropna do?
- Removes NaN
- Fills
- Sorts
- Copies
* Correct answer: Removes NaN
Filter.

What does fillna(0) do?
- Replaces NaN with 0
- Removes
- Sorts
- Counts
* Correct answer: Replaces NaN with 0
Impute.

What does value_counts do?
- Counts unique values
- Sorts
- Sums
- Transposes
* Correct answer: Counts unique values
Frequencies.

What does unique return?
- Unique values
- Counts
- Sorted
- Series
* Correct answer: Unique values
Array.

What does s.mean() do?
- Average
- Sum
- Max
- Count
* Correct answer: Average
Mean.

How to create from dict?
- pd.Series({"a":1})
- Series dict fails
- pd.DataFrame
- pd.array
* Correct answer: pd.Series({"a":1})
Keys become index.

What does sort_values do?
- Sorts values
- Sorts index
- Reverses
- Counts
* Correct answer: Sorts values
By values.
<!--/QUIZ-->
