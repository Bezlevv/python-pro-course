---
title: Data visualization with seaborn
summary: Statistical charts, styling.
order: 3
duration: 45 min
difficulty: intermediate
tags: seaborn
---

Seaborn makes statistical charts easy.

## Example

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")
sns.scatterplot(data=tips, x="total_bill", y="tip", hue="time")
plt.show()
```

## Common plots

- histplot — distribution;
- boxplot — spread;
- countplot — categories.

## Lesson summary

Seaborn: beautiful stats in one line.

<!--TASK-->
### Task 1 — Load
Load the tips dataset.

### Task 2 — Scatter
Scatter with hue.

### Task 3 — Hist
Histogram.

### Task 4 — Box
Boxplot.

### Task 5 — Count
Countplot.

### Task 6 — Style
Set a theme.

### Task 7 — Save
Save the figure.
<!--/TASK-->

<!--HINT-->
### Hint 1
load_dataset.

### Hint 2
scatterplot.

### Hint 3
histplot.

### Hint 4
boxplot.

### Hint 5
countplot.

### Hint 6
set_theme.

### Hint 7
savefig.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import seaborn as sns
tips = sns.load_dataset("tips")
```

### Solution 2
```python
sns.scatterplot(data=tips, x="total_bill", y="tip", hue="time")
plt.show()
```

### Solution 3
```python
sns.histplot(data=tips, x="total_bill", bins=20)
```

### Solution 4
```python
sns.boxplot(data=tips, x="day", y="tip")
```

### Solution 5
```python
sns.countplot(data=tips, x="time")
```

### Solution 6
```python
sns.set_theme(style="whitegrid")
```

### Solution 7
```python
plt.savefig("tips.png", dpi=150)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is seaborn?
- Stats plotting
- Data manipulation
- Web
- None
* Correct answer: Stats plotting
High-level.

What is a dataset?
- Built-in data
- Plot
- Model
- None
* Correct answer: Built-in data
tips.

What is scatterplot?
- Points
- Bars
- Boxes
- None
* Correct answer: Points
XY.

What is hue?
- Color group
- Size
- Shape
- None
* Correct answer: Color group
Third var.

What is histplot?
- Distribution
- Points
- Bars by category
- None
* Correct answer: Distribution
Bins.

What is boxplot?
- Quartiles
- Points
- Counts
- None
* Correct answer: Quartiles
Outliers.

What is countplot?
- Category counts
- Distribution
- Points
- None
* Correct answer: Category counts
Bars.

What is set_theme?
- Global style
- Data
- Plot
- None
* Correct answer: Global style
Whitegrid.

What is a figure?
- Canvas
- Data
- Axis
- None
* Correct answer: Canvas
Save.

What is dpi?
- Resolution
- Size
- Color
- None
* Correct answer: Resolution
150.

What is the benefit?
- Easy stats charts
- Drawing by hand
- Required
- None
* Correct answer: Easy stats charts
Beautiful.

What is matplotlib?
- Base plotting
- Stats
- Data
- None
* Correct answer: Base plotting
plt.
<!--/QUIZ-->
