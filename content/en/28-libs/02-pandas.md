---
title: pandas: DataFrames and Series
summary: Create, read, filter, group.
order: 2
duration: 50 min
difficulty: intermediate
tags: pandas
---

pandas makes data analysis fast.

## Series

```python
import pandas as pd
s = pd.Series([1, 2, 3], index=["a", "b", "c"])
```

## DataFrame

```python
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Carol"],
    "age": [30, 25, 35],
})
```

## Read CSV

```python
df = pd.read_csv("data.csv")
print(df.head())
```

## Filter

```python
adults = df[df["age"] >= 30]
```

## Group

```python
df.groupby("name")["age"].mean()
```

## Lesson summary

DataFrame = table + powerful operations.

<!--TASK-->
### Task 1 — Series
Create a Series.

### Task 2 — DataFrame
Create from a dict.

### Task 3 — Read
Read CSV.

### Task 4 — Head
Show first rows.

### Task 5 — Filter
Filter by age.

### Task 6 — Group
Group and aggregate.

### Task 7 — Save
Write to CSV.
<!--/TASK-->

<!--HINT-->
### Hint 1
pd.Series.

### Hint 2
pd.DataFrame.

### Hint 3
read_csv.

### Hint 4
head().

### Hint 5
df[df.age >=].

### Hint 6
groupby.

### Hint 7
to_csv.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import pandas as pd
s = pd.Series([1, 2, 3], index=["a", "b", "c"])
print(s["b"])
```

### Solution 2
```python
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Carol"],
    "age": [30, 25, 35],
})
```

### Solution 3
```python
df = pd.read_csv("data.csv")
```

### Solution 4
```python
print(df.head())
```

### Solution 5
```python
adults = df[df["age"] >= 30]
```

### Solution 6
```python
print(df.groupby("name")["age"].mean())
```

### Solution 7
```python
df.to_csv("out.csv", index=False)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a Series?
- One-dimensional
- Table
- DataFrame
- None
* Correct answer: One-dimensional
Column.

What is a DataFrame?
- Two-dimensional table
- Series
- List
- None
* Correct answer: Two-dimensional table
Rows/cols.

What is index?
- Row labels
- Columns
- Values
- None
* Correct answer: Row labels
Keys.

What is read_csv?
- Imports CSV
- Exports
- Creates
- None
* Correct answer: Imports CSV
File.

What is head?
- First rows
- Last
- All
- None
* Correct answer: First rows
5.

What is filtering?
- Condition
- Sort
- Group
- None
* Correct answer: Condition
Boolean.

What is groupby?
- Groups
- Filters
- Sorts
- None
* Correct answer: Groups
Aggregate.

What is mean?
- Average
- Sum
- Count
- None
* Correct answer: Average
Group.

What is to_csv?
- Saves
- Loads
- Prints
- None
* Correct answer: Saves
File.

What is index=False?
- No row numbers
- With
- Required
- None
* Correct answer: No row numbers
Clean.

What is a column?
- Named series
- Row
- Index
- None
* Correct answer: Named series
df["age"].

What is NaN?
- Missing value
- Zero
- Error
- None
* Correct answer: Missing value
None.
<!--/QUIZ-->
