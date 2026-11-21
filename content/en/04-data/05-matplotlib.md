---
title: Visualization: Matplotlib
summary: Line plots, bar charts, histograms, scatter plots and customization.
order: 5
duration: 40 min
difficulty: intermediate
tags: matplotlib, plots, charts
---

Matplotlib creates plots from data.

## Basic line

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4]
y = [1, 4, 9, 16]
plt.plot(x, y)
plt.title("Squares")
plt.show()
```

## Bar chart

```python
plt.bar(["A", "B", "C"], [3, 7, 5])
```

## Histogram

```python
plt.hist(data, bins=10)
```

## Scatter

```python
plt.scatter(x, y)
```

## Customization

- labels: plt.xlabel/ylabel;
- legend: plt.legend();
- grid: plt.grid(True);
- save: plt.savefig("plot.png").

## Lesson summary

Matplotlib covers line, bar, histogram, scatter; customize and save.

<!--TASK-->
### Task 1 — Line
Plot y=x^2 for x 0..9 with a title.

### Task 2 — Labels
Add xlabel, ylabel and grid.

### Task 3 — Bar
Bar chart of [4,7,2] with bars ["a","b","c"].

### Task 4 — Histogram
Create data = [1,1,2,2,2,3] and histogram bins=3.

### Task 5 — Scatter
Scatter plot of 10 random points.

### Task 6 — Save
Save a figure to plot.png and check the file exists.

### Task 7 — Multiple lines
Plot two lines with a legend.
<!--/TASK-->

<!--HINT-->
### Hint 1
plt.plot(x, [v*v for v in x]).

### Hint 2
plt.xlabel("x"); plt.grid(True).

### Hint 3
plt.bar(labels, values).

### Hint 4
plt.hist(data, bins=3).

### Hint 5
plt.scatter(x, y).

### Hint 6
plt.savefig("plot.png").

### Hint 7
label parameter and plt.legend().
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import matplotlib.pyplot as plt
x = range(10)
plt.plot(x, [v * v for v in x])
plt.title("Squares")
plt.show()
```

### Solution 2
```python
plt.plot(x, y)
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
```

### Solution 3
```python
plt.bar(["a", "b", "c"], [4, 7, 2])
plt.show()
```

### Solution 4
```python
data = [1, 1, 2, 2, 2, 3]
plt.hist(data, bins=3)
plt.show()
```

### Solution 5
```python
import numpy as np
x = np.random.rand(10)
y = np.random.rand(10)
plt.scatter(x, y)
plt.show()
```

### Solution 6
```python
plt.plot([1, 2, 3], [1, 4, 9])
plt.savefig("plot.png")
```

### Solution 7
```python
plt.plot(x, y1, label="first")
plt.plot(x, y2, label="second")
plt.legend()
plt.show()
```
<!--/SOLUTION-->

<!--QUIZ-->
What does plt.plot do?
- Draws a line chart
- Bar
- Histogram
- Scatter
* Correct answer: Draws a line chart
Basic plot.

What does plt.bar do?
- Bar chart
- Line
- Hist
- Scatter
* Correct answer: Bar chart
Categorical.

What does plt.hist do?
- Histogram
- Line
- Bar
- Scatter
* Correct answer: Histogram
Distribution.

What does plt.scatter do?
- Scatter plot
- Line
- Bar
- Hist
* Correct answer: Scatter plot
Points.

What does plt.title do?
- Sets the title
- Labels axis
- Grid
- Legend
* Correct answer: Sets the title
Plot heading.

What does plt.xlabel do?
- X-axis label
- Title
- Legend
- Grid
* Correct answer: X-axis label
Axis naming.

What does plt.legend do?
- Shows legend
- Grid
- Title
- Save
* Correct answer: Shows legend
For labeled lines.

How to save?
- plt.savefig("f.png")
- plt.safe
- plt.export
- plt.write
* Correct answer: plt.savefig("f.png")
To file.

What does plt.show do?
- Displays the plot
- Saves
- Clears
- Closes
* Correct answer: Displays the plot
Render window.

What does plt.grid(True) do?
- Shows gridlines
- Hides
- Sorts
- None
* Correct answer: Shows gridlines
Readability.

What is a legend for?
- Distinguishing series
- Labels axis
- Title
- Grid
* Correct answer: Distinguishing series
Names.

How to make two lines?
- plot twice with labels
- bar twice
- hist twice
- scatter once
* Correct answer: plot twice with labels
With legend.
<!--/QUIZ-->
