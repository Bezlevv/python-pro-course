---
title: Project: dashboard with Streamlit
summary: Data app with pandas, charts and widgets.
order: 5
duration: 60 min
difficulty: intermediate
tags: project, streamlit, dashboard
---

Build an interactive dashboard.

## Plan

1. Load data (pandas);
2. Widgets: selectbox, slider;
3. Charts;
4. Metrics.

## Skeleton

```python
import pandas as pd
import streamlit as st

@st.cache_data
def load():
    return pd.read_csv("sales.csv")

df = load()
city = st.selectbox("City", df["city"].unique())
filtered = df[df["city"] == city]
st.line_chart(filtered.groupby("date")["revenue"].sum())
```

## Lesson summary

Data + widgets + charts = dashboard.

<!--TASK-->
### Task 1 — Load
Load a CSV with st.cache_data.

### Task 2 — Selectbox
Let the user choose a city.

### Task 3 — Filter
Filter rows by selection.

### Task 4 — Chart
Plot revenue over time.

### Task 5 — Metric
Show total revenue.

### Task 6 — Slider
Add a price filter slider.

### Task 7 — Column layout
Place metric and chart side by side.
<!--/TASK-->

<!--HINT-->
### Hint 1
st.cache_data.

### Hint 2
st.selectbox.

### Hint 3
df[df["city"] == city].

### Hint 4
st.line_chart.

### Hint 5
st.metric.

### Hint 6
st.slider.

### Hint 7
st.columns(2).
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import pandas as pd
import streamlit as st

@st.cache_data
def load():
    return pd.read_csv("sales.csv")

df = load()
```

### Solution 2
```python
city = st.selectbox("City", df["city"].unique())
```

### Solution 3
```python
filtered = df[df["city"] == city]
```

### Solution 4
```python
st.line_chart(filtered.groupby("date")["revenue"].sum())
```

### Solution 5
```python
st.metric("Total revenue", filtered["revenue"].sum())
```

### Solution 6
```python
max_price = st.slider("Max price", 0, 100, 50)
filtered = filtered[filtered["price"] <= max_price]
```

### Solution 7
```python
col1, col2 = st.columns(2)
with col1:
    st.metric("Revenue", filtered["revenue"].sum())
with col2:
    st.line_chart(filtered.groupby("date")["revenue"].sum())
```
<!--/SOLUTION-->

<!--QUIZ-->
What is Streamlit?
- Web data apps
- API framework
- ORM
- Template
* Correct answer: Web data apps
Python.

What does selectbox do?
- Dropdown
- Slider
- Button
- Chart
* Correct answer: Dropdown
Choice.

What is st.cache_data?
- Caches function
- Deletes
- Charts
- None
* Correct answer: Caches function
Speed.

What does st.metric do?
- Shows a number
- Chart
- Input
- Layout
* Correct answer: Shows a number
KPI.

What does st.line_chart do?
- Plots series
- Table
- Input
- Map
* Correct answer: Plots series
Trend.

What is groupby?
- Aggregates
- Filters
- Sorts
- Joins
* Correct answer: Aggregates
Per group.

What does filtered mean?
- Subset of data
- All
- Model
- Chart
* Correct answer: Subset of data
After filter.

What is a slider?
- Range input
- Dropdown
- Text
- Checkbox
* Correct answer: Range input
Number.

What does st.columns do?
- Layout
- Data
- Chart
- Input
* Correct answer: Layout
Side by side.

What is a DataFrame?
- Table
- Series
- List
- Dict
* Correct answer: Table
Pandas.

Why cache load?
- Avoid reload
- Faster
- Memory
- None
* Correct answer: Avoid reload
On rerun.

What is rerun?
- Script reruns on widget change
- Pause
- End
- None
* Correct answer: Script reruns on widget change
Streamlit.
<!--/QUIZ-->
