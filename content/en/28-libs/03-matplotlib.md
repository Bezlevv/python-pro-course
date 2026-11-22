---
title: Matplotlib: visualization
summary: Line, bar, histogram, plt.
order: 3
duration: 45 min
difficulty: intermediate
tags: matplotlib
---

Matplotlib creates charts.

## Line

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4]
y = [10, 20, 15, 25]

plt.plot(x, y)
plt.title("Sales")
plt.xlabel("Month")
plt.ylabel("Amount")
plt.show()
```

## Bar and histogram

```python
plt.bar(["A", "B"], [5, 7])
plt.hist(data, bins=10)
```

## Lesson summary

plot/bar/hist cover most charts.

<!--TASK-->
### Task 1 — Line
Plot a line.

### Task 2 — Labels
Add title and axes.

### Task 3 — Bar
Bar chart.

### Task 4 — Histogram
Histogram.

### Task 5 — Scatter
Scatter plot.

### Task 6 — Save
Save PNG.

### Task 7 — Subplots
Two charts side-by-side.
<!--/TASK-->

<!--HINT-->
### Hint 1
plt.plot.

### Hint 2
title.

### Hint 3
bar.

### Hint 4
hist.

### Hint 5
scatter.

### Hint 6
savefig.

### Hint 7
subplots.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [1, 4, 9])
plt.show()
```

### Solution 2
```python
plt.title("Sales")
plt.xlabel("Month")
plt.ylabel("Amount")
```

### Solution 3
```python
plt.bar(["A", "B", "C"], [5, 7, 3])
```

### Solution 4
```python
import random
data = [random.randint(0, 100) for _ in range(100)]
plt.hist(data, bins=10)
```

### Solution 5
```python
plt.scatter([1, 2, 3], [4, 5, 6])
```

### Solution 6
```python
plt.savefig("chart.png", dpi=150)
```

### Solution 7
```python
fig, axes = plt.subplots(1, 2)
axes[0].plot(x, y)
axes[1].bar(["A", "B"], [5, 7])
```
<!--/SOLUTION-->

<!--QUIZ-->
What is plt?
- Pyplot interface
- A database
- A browser
- None
* Correct answer: Pyplot interface
Module.

What is plot?
- Line chart
- Bar
- Hist
- None
* Correct answer: Line chart
Lines.

What is bar?
- Bars
- Line
- Scatter
- None
* Correct answer: Bars
Categories.

What is hist?
- Histogram
- Line
- Bar
- None
* Correct answer: Histogram
Distribution.

What is scatter?
- Points
- Lines
- Bars
- None
* Correct answer: Points
XY.

What is title?
- Chart name
- Axis
- Data
- None
* Correct answer: Chart name
Label.

What is xlabel?
- X-axis label
- Title
- Legend
- None
* Correct answer: X-axis label
Name.

What is show?
- Displays
- Saves
- Hides
- None
* Correct answer: Displays
Window.

What is savefig?
- Saves file
- Shows
- Clears
- None
* Correct answer: Saves file
PNG.

What is bins?
- Histogram bars
- Data
- Colors
- None
* Correct answer: Histogram bars
Count.

What is subplots?
- Multiple charts
- One
- Data
- None
* Correct answer: Multiple charts
Axes.

What is dpi?
- Resolution
- Size
- Color
- None
* Correct answer: Resolution
Quality.
<!--/QUIZ-->
