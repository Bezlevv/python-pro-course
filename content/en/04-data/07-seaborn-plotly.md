---
title: Seaborn and Plotly
summary: Statistical plots with Seaborn and interactive charts with Plotly.
order: 7
duration: 40 min
difficulty: intermediate
tags: seaborn, plotly, charts
---

Seaborn makes statistical plots beautiful; Plotly adds interactivity.

## Seaborn

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")
sns.histplot(tips["total_bill"])
sns.boxplot(x="day", y="total_bill", data=tips)
plt.show()
```

Common: histplot, boxplot, scatterplot, heatmap.

## Plotly

```python
import plotly.express as px

df = px.data.gapminder().query("year == 2007")
fig = px.scatter(df, x="gdpPercap", y="lifeExp", size="pop", color="continent")
fig.show()
```

Plotly figures are interactive: hover, zoom.

## Save

```python
fig.write_html("chart.html")
sns_plot.figure.savefig("plot.png")
```

## Lesson summary

Seaborn for statistical storytelling; Plotly for interactive dashboards.

<!--TASK-->
### Task 1 — Seaborn hist
Load tips; plot a histogram of total_bill.

### Task 2 — Boxplot
Boxplot of total_bill by day.

### Task 3 — Scatterplot
Scatterplot of tip vs total_bill.

### Task 4 — Heatmap
Correlation matrix via heatmap.

### Task 5 — Plotly scatter
Scatter of gapminder 2007 with colors.

### Task 6 — Plotly bar
Bar chart of populations of top 5 countries.

### Task 7 — Save
Save a Plotly figure as HTML and a Seaborn figure as PNG.
<!--/TASK-->

<!--HINT-->
### Hint 1
sns.histplot(tips["total_bill"]).

### Hint 2
sns.boxplot(x="day", y="total_bill", data=tips).

### Hint 3
sns.scatterplot(x="total_bill", y="tip", data=tips).

### Hint 4
sns.heatmap(tips.corr(numeric_only=True), annot=True).

### Hint 5
px.scatter(df, x=..., y=..., color="continent").

### Hint 6
px.bar(df, x="country", y="pop").

### Hint 7
fig.write_html("chart.html").
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")
sns.histplot(tips["total_bill"])
plt.show()
```

### Solution 2
```python
sns.boxplot(x="day", y="total_bill", data=tips)
plt.show()
```

### Solution 3
```python
sns.scatterplot(x="total_bill", y="tip", data=tips)
plt.show()
```

### Solution 4
```python
sns.heatmap(tips.corr(numeric_only=True), annot=True)
plt.show()
```

### Solution 5
```python
import plotly.express as px
df = px.data.gapminder().query("year == 2007")
fig = px.scatter(df, x="gdpPercap", y="lifeExp", color="continent", size="pop")
fig.show()
```

### Solution 6
```python
df2 = df.nlargest(5, "pop")
fig = px.bar(df2, x="country", y="pop")
fig.show()
```

### Solution 7
```python
fig.write_html("chart.html")
sns.histplot(tips["total_bill"]).figure.savefig("plot.png")
```
<!--/SOLUTION-->

<!--QUIZ-->
What does Seaborn provide?
- Statistical plots
- Games
- Web
- Tables
* Correct answer: Statistical plots
High-level.

What is histplot?
- Histogram
- Box
- Scatter
- Heat
* Correct answer: Histogram
Distribution.

What is boxplot?
- Box plot
- Hist
- Line
- Bar
* Correct answer: Box plot
Quartiles.

What is heatmap?
- Matrix heatmap
- Scatter
- Hist
- Bar
* Correct answer: Matrix heatmap
Correlations.

What does Plotly add?
- Interactivity
- Speed
- Sound
- Text
* Correct answer: Interactivity
Hover/zoom.

What is px?
- plotly.express
- pandas
- seaborn
- numpy
* Correct answer: plotly.express
Quick figures.

How to save Plotly?
- fig.write_html(...)
- plt.savefig
- fig.save
- fig.png
* Correct answer: fig.write_html(...)
Interactive HTML.

What dataset is tips?
- Seaborn built-in
- CSV custom
- Random
- None
* Correct answer: Seaborn built-in
load_dataset.

What is gapminder?
- Built-in dataset
- Custom
- Empty
- Random
* Correct answer: Built-in dataset
px.data.

Which plot shows categories?
- boxplot
- histplot
- line
- scatter
* Correct answer: boxplot
By category.

What does annot=True do?
- Shows values
- Hides
- Sorts
- Colors
* Correct answer: Shows values
In cells.

What is fig.show()?
- Opens the figure
- Saves
- Prints
- Closes
* Correct answer: Opens the figure
Render.
<!--/QUIZ-->
