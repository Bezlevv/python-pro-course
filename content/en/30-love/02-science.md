---
title: Python in science and analytics
summary: Jupyter, pandas, stats, visualization.
order: 2
duration: 45 min
difficulty: intermediate
tags: science, jupyter
---

Python is the language of data science.

## Jupyter

Notebooks combine code, text, and charts.

## Stack

pandas → statsmodels/scipy → matplotlib.

## Example

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv")
print(df.describe())
df["value"].hist()
plt.show()
```

## Lesson summary

Notebooks + pandas + plots.

<!--TASK-->
### Task 1 — Notebook
What are cells?

### Task 2 — Describe
Summarize a DataFrame.

### Task 3 — Hist
Plot a histogram.

### Task 4 — Corr
Correlation matrix.

### Task 5 — Group
Mean per group.

### Task 6 — Filter
Filter outliers.

### Task 7 — Export
Save a cleaned CSV.
<!--/TASK-->

<!--HINT-->
### Hint 1
Blocks.

### Hint 2
describe().

### Hint 3
hist().

### Hint 4
corr().

### Hint 5
groupby.

### Hint 6
df[df.x <].

### Hint 7
to_csv.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```text
Ячейки — блоки кода или текста,
которые выполняются по очереди
```

### Solution 2
```python
print(df.describe())
```

### Solution 3
```python
df["value"].hist()
plt.show()
```

### Solution 4
```python
print(df.corr())
```

### Solution 5
```python
print(df.groupby("category")["value"].mean())
```

### Solution 6
```python
clean = df[df["value"] < df["value"].quantile(0.99)]
```

### Solution 7
```python
clean.to_csv("clean.csv", index=False)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is Jupyter?
- Notebooks
- A compiler
- A database
- None
* Correct answer: Notebooks
Cells.

What is a cell?
- Code block
- File
- Chart
- None
* Correct answer: Code block
Run.

What is describe?
- Summary stats
- Plot
- Filter
- None
* Correct answer: Summary stats
Stats.

What is corr?
- Correlation
- Sort
- Filter
- None
* Correct answer: Correlation
Matrix.

What is quantile?
- Percentile
- Mean
- Sum
- None
* Correct answer: Percentile
0.99.

What is a histogram?
- Distribution
- Line
- Table
- None
* Correct answer: Distribution
Bins.

What is a notebook?
- Interactive doc
- Script
- Module
- None
* Correct answer: Interactive doc
.ipynb.

What is an outlier?
- Extreme value
- Normal
- Missing
- None
* Correct answer: Extreme value
Filter.

What is a statistic?
- Number summary
- Plot
- Cell
- None
* Correct answer: Number summary
Mean.

What is scipy?
- Scientific library
- Web
- GUI
- None
* Correct answer: Scientific library
Stats.

What is the stack?
- Tools together
- One tool
- None
- Always
* Correct answer: Tools together
pandas+plot.

What is the workflow?
- Load → analyze → plot
- Plot only
- Load only
- None
* Correct answer: Load → analyze → plot
Flow.
<!--/QUIZ-->
