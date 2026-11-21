---
title: Streamlit: dashboards
summary: Building data apps with widgets, charts and caching.
order: 9
duration: 40 min
difficulty: intermediate
tags: streamlit, dashboard, widgets
---

Streamlit turns Python scripts into web apps.

## First app

```python
import streamlit as st

st.title("Hello")
st.write("Data app")
```

Run: `streamlit run app.py`.

## Widgets

```python
name = st.text_input("Name")
number = st.slider("Number", 0, 100, 50)
if st.button("Go"):
    st.write(name, number)
```

## Charts

```python
import pandas as pd
df = pd.DataFrame({"x": [1,2,3], "y": [2,4,6]})
st.line_chart(df)
```

## Caching

```python
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")
```

## Lesson summary

Streamlit: widgets → charts → caching; instantly web.

<!--TASK-->
### Task 1 — Title
Create an app with a title and text.

### Task 2 — Input
Add a text_input and show it.

### Task 3 — Slider
Add a slider and display its value.

### Task 4 — Button
Run logic on button click.

### Task 5 — Chart
Plot a line chart from a small DataFrame.

### Task 6 — Cache
Decorate a data-loading function with st.cache_data.

### Task 7 — Columns
Use st.columns to show two metrics side by side.
<!--/TASK-->

<!--HINT-->
### Hint 1
st.title; st.write.

### Hint 2
st.text_input.

### Hint 3
st.slider.

### Hint 4
if st.button("Go"): ....

### Hint 5
st.line_chart(df).

### Hint 6
@st.cache_data.

### Hint 7
st.columns(2).
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import streamlit as st
st.title("Hello")
st.write("Data app")
```

### Solution 2
```python
name = st.text_input("Name")
st.write(name)
```

### Solution 3
```python
n = st.slider("Number", 0, 100, 50)
st.write(n)
```

### Solution 4
```python
if st.button("Go"):
    st.success("Clicked")
```

### Solution 5
```python
import pandas as pd
df = pd.DataFrame({"x": [1, 2, 3], "y": [2, 4, 6]})
st.line_chart(df)
```

### Solution 6
```python
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")
```

### Solution 7
```python
col1, col2 = st.columns(2)
col1.metric("A", 10)
col2.metric("B", 20)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is Streamlit?
- Turns scripts into web apps
- Framework for APIs
- ORM
- Template
* Correct answer: Turns scripts into web apps
Data apps.

How to run?
- streamlit run app.py
- python app.py
- django run
- flask run
* Correct answer: streamlit run app.py
Default.

What does st.title do?
- Header
- Input
- Chart
- Button
* Correct answer: Header
Big text.

What is a widget?
- Interactive control
- Chart
- Page
- Data
* Correct answer: Interactive control
Input.

What does st.text_input do?
- Text field
- Slider
- Button
- Chart
* Correct answer: Text field
Input.

What does st.slider do?
- Range slider
- Text
- Button
- Select
* Correct answer: Range slider
Number.

What does st.button do?
- Clickable button
- Input
- Chart
- Title
* Correct answer: Clickable button
Action.

What does st.line_chart do?
- Plots a line chart
- Table
- Input
- Map
* Correct answer: Plots a line chart
Data viz.

What does st.cache_data do?
- Caches function results
- Deletes
- Plots
- Runs
* Correct answer: Caches function results
Performance.

What does st.columns do?
- Layout columns
- Data
- Chart
- Input
* Correct answer: Layout columns
Side by side.

What does st.metric do?
- Shows a metric
- Table
- Button
- Slider
* Correct answer: Shows a metric
Value + label.

Is Streamlit good for internal tools?
- Yes, quickly
- No
- Only APIs
- Only games
* Correct answer: Yes, quickly
Dashboards.
<!--/QUIZ-->
