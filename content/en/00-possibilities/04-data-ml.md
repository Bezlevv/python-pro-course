---
title: Data and AI: analytics, neural networks, LLMs
summary: How Python analyzes data, trains neural networks, and powers large language models like ChatGPT. First steps into the world of data.
order: 4
duration: 30 min
difficulty: beginner
tags: data, analytics, ai, neural networks, llm, pandas
---

## Data is the new oil; Python is the drilling rig

Every day humanity creates huge volumes of data: purchases, posts, sensors, videos, orders. But data by itself is worth nothing — value appears when it is **analyzed** and turned into conclusions: "who buys more in winter", "which topic is gaining popularity", "tomorrow's weather forecast". This is where Python is the king.

In this lesson we'll walk from simple statistics to neural networks and large language models (LLMs) — the very ones behind ChatGPT and similar assistants.

## Analytics: Pandas and NumPy

The main analytics tools in Python:

- **Pandas** — working with data tables: loading, filtering, grouping, pivot tables. The name comes from "panel data".
- **NumPy** — fast computations with arrays of numbers: math, linear algebra, random values.
- **Matplotlib** — charts and visualization: lines, bars, heatmaps.

Here is what classic analytics with Pandas looks like:

```python
import pandas as pd

# A table of student grades
data = {
    "Name": ["Anna", "Boris", "Victor"],
    "Grade": [5, 4, 3],
}
df = pd.DataFrame(data)

print(df)                  # the whole table
print(df["Grade"].mean())  # average grade
```

Install pandas (`pip install pandas`), and you get a mini-analytics center. But even without pandas, the Python standard library can compute statistics — let's check.

## Demo: statistics without third-party libraries

```python
import statistics

grades = [4, 5, 3, 5, 4, 4, 5, 3]
print("Average grade:", statistics.mean(grades))
print("Median:", statistics.median(grades))
print("Most common grade:", statistics.mode(grades))
print("Maximum:", max(grades), "Minimum:", min(grades))
```

`statistics.mean()` is the arithmetic mean, `median()` is the median (the middle of the series), `mode()` is the most frequent value. This set is already enough to tell the most important things about data.

## Machine learning: how computers learn

Machine learning (ML) is when we don't write rules by hand but show the program examples, and it finds patterns itself. The **scikit-learn** library makes this accessible:

```python
# Example: prediction by a simple rule
# (simplified — real ML needs data and a model)
X = [[1], [2], [3], [4]]
y = [2, 4, 6, 8]  # y = 2 * x

from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X, y)
print("Prediction for x=5:", model.predict([[5]]))
```

The model "guessed" by itself that the relation is doubling. This is how price, demand, and forecast predictions work.

## Neural networks: PyTorch and TensorFlow

A neural network is a program inspired by the brain's structure: millions of "neurons" learn to recognize patterns. Neural networks in Python are built with two main frameworks:

- **PyTorch** (developed by Meta) — the favorite of AI researchers;
- **TensorFlow** (Google) — widely used in industry.

It's on Python that models are trained to recognize faces, translate speech, write code, and draw pictures. You don't have to understand the math inside right away — at the start it's important to see that a neural network's input is just numbers (pixels, words), and the output is a prediction.

## LLMs: large language models

An LLM (Large Language Model) is a neural network trained on enormous volumes of text. It can continue text, answer questions, write code, and translate. ChatGPT, Claude, Gemini — all are built on such models, and Python is the main language used to create and use them.

Python connects to LLMs via APIs. For example, through the OpenAI API you can send a prompt and get an answer:

```python
# Simplified scheme of a real request to an LLM
import openai

client = openai.OpenAI(api_key=[redacted])
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Write a greeting in Python"}],
)
print(response.choices[0].message.content)
```

The API key is the "pass" to the service. We won't spend keys in this lesson, but the main thing is clear: Python is the remote control for AI. Researchers and engineers write both the models themselves and the apps around them in Python.

## Lesson summary

Today we learned:

- that Python is the main data analysis language (Pandas, NumPy, Matplotlib);
- how to compute statistics even with the standard library;
- how machine learning works with scikit-learn example;
- what neural networks are and which frameworks build them (PyTorch, TensorFlow);
- what LLMs are and how Python connects to models like ChatGPT.

Now let's try on the analyst's role.

<!--TASK-->
### Task 1
Write a program `grades_stats.py` that for the grade list `[3, 4, 5, 4, 4, 5, 3, 5, 5, 4]` computes and prints: the average grade (rounded to two decimal places, use `round(..., 2)`), the median, the most common grade, and the maximum and minimum grades. Use the `statistics` module. Print results with labels, e.g.: `Average grade: 4.2`.

### Task 2
Write a program `word_frequency.py` that takes the text `"python is fun to learn python is powerful python is a simple language"`, splits it into words with `.split()`, and counts how many times each word appears. Use `Counter` from the `collections` module. Print the top-3 most frequent words in the format `word: count`. At the end print the total number of words in the text.

### Task 3
Write a program `students_groups.py` that divides students into groups by performance. There is a dictionary: `grades = {"Anna": 5, "Boris": 3, "Victor": 4, "Gosha": 2, "Dasha": 5}`. Split them into two lists: `excellent` (grade >= 4) and `need_work` (grade < 4). Print both lists with labels. Use the loop `for name, grade in grades.items():` and an `if` condition.

### Task 4
Write a program `csv_analyzer.py` that creates a file `marks.csv` with columns `name,grade` (3–5 rows), then reads it with the `csv` module and computes the sum of all grades and the average. Print `Sum of grades: N` and `Average grade: M` (rounded to two decimals). Use `csv.writer` for writing and `csv.reader` for reading.

### Task 5
Mini-experiment: collect your own data! Write a program `name_stats.py` that takes your name (e.g., `"Alexander"`), splits it into letters, and counts each letter's frequency with `Counter`. Then print: the name length, the most frequent letter, and how many unique letters the name has (the length of the Counter dictionary). Run it and share the result with yourself — these are the first real data you analyzed.
<!--/TASK-->

<!--HINT-->
### Hint 1
Add `import statistics`. For the average: `statistics.mean(grades)`, rounding: `round(statistics.mean(grades), 2)`. Median — `statistics.median(grades)`, mode — `statistics.mode(grades)`. Maximum and minimum — built-in `max(grades)` and `min(grades)`.

### Hint 2
`text.split()` splits the string by spaces and returns a list of words. `Counter(words)` immediately counts the frequency of all words. To print the top-3, use `counter.most_common(3)`, which returns a list of `(word, count)` pairs. The total word count is `len(words)`.

### Hint 3
Create two empty lists. The loop `for name, grade in grades.items():` iterates over "name — grade" pairs. If `grade >= 4` — add the name to the excellent list with `.append(name)`, otherwise to the second list. At the end print both lists with `print("Excellent:", excellent)`.

### Hint 4
Writing: `with open("marks.csv", "w", newline="", encoding="utf-8") as f: writer = csv.writer(f); writer.writerow(["name", "grade"]); ...`. Reading: `with open("marks.csv", encoding="utf-8") as f: rows = list(csv.reader(f))`. Count the sum in a loop over rows, skipping the header, e.g. `for name, grade in rows[1:]: total += int(grade)`. The average is `total / len(rows[1:])`.

### Hint 5
`Counter("Alexander")` immediately gives a letter frequency dictionary. The name length is `len("Alexander")`. The most frequent letter is `counter.most_common(1)[0][0]`. The number of unique letters is `len(counter)` (in a Counter dictionary every key is unique). Print everything with labels.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
import statistics

grades = [3, 4, 5, 4, 4, 5, 3, 5, 5, 4]
print("Average grade:", round(statistics.mean(grades), 2))
print("Median:", statistics.median(grades))
print("Most common grade:", statistics.mode(grades))
print("Maximum:", max(grades), "Minimum:", min(grades))
```

Result:

```
Average grade: 4.2
Median: 4.0
Most common grade: 4
Maximum: 5 Minimum: 3
```

What happens here? `statistics.mean(grades)` adds all grades and divides by their count. `round(..., 2)` keeps two decimal places. The median `statistics.median()` is the value "in the middle" of the ordered series: half the students are above it, half below. The mode `statistics.mode()` is the most frequent value. This set of measures is the standard of any analytical report, from a school gradebook to salary statistics of a whole company.

### Solution 2
Solution:

```python
from collections import Counter

text = "python is fun to learn python is powerful python is a simple language"
words = text.split()
frequency = Counter(words)

print("Top-3 words:")
for word, count in frequency.most_common(3):
    print(word, ":", count)

print("Total words:", len(words))
```

Result:

```
Top-3 words:
python : 3
is : 2
a : 1
Total words: 10
```

What happens here? The string `text.split()` splits by spaces into a list of ten words. `Counter(words)` immediately builds a frequency dictionary: which word appears how many times. `most_common(3)` returns the three most frequent `(word, count)` pairs, which we print. Such word frequency is the basis of text analysis: from keyword search to training models. Natural language processing starts with such simple counters.

### Solution 3
Solution:

```python
grades = {"Anna": 5, "Boris": 3, "Victor": 4, "Gosha": 2, "Dasha": 5}

excellent = []
need_work = []

for name, grade in grades.items():
    if grade >= 4:
        excellent.append(name)
    else:
        need_work.append(name)

print("Excellent:", excellent)
print("Need work:", need_work)
```

Result:

```
Excellent: ['Anna', 'Victor', 'Dasha']
Need work: ['Boris', 'Gosha']
```

What happens here? `grades.items()` returns "key — value" pairs, and we "unpack" them into `name` and `grade` variables. The condition `if grade >= 4:` decides which list gets the name. This grouping is essentially a `groupby` operation from pandas, done by hand: we split data into categories. This is how analysts divide customers into segments, products into categories, students into groups.

### Solution 4
Solution:

```python
import csv

with open("marks.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "grade"])
    writer.writerow(["Anna", 5])
    writer.writerow(["Boris", 4])
    writer.writerow(["Victor", 3])
    writer.writerow(["Gosha", 5])
    writer.writerow(["Dasha", 4])

with open("marks.csv", encoding="utf-8") as f:
    rows = list(csv.reader(f))

total = 0
for name, grade in rows[1:]:
    total += int(grade)

average = round(total / len(rows[1:]), 2)
print("Sum of grades:", total)
print("Average grade:", average)
```

Result:

```
Sum of grades: 21
Average grade: 4.2
```

What happens here? `csv.writer` writes table rows to a file. `csv.reader` reads them back as lists. `rows[1:]` drops the header row. We go through the rows, convert the grade string to a number with `int(grade)`, and accumulate the sum. This script is a prototype of a real ETL process: extract data from a file, transform, and compute. CSV is a universal data exchange format understood by Excel, Google Sheets, and all programming languages.

### Solution 5
Solution:

```python
from collections import Counter

name = "Alexander"
counter = Counter(name)

print("Name:", name)
print("Name length:", len(name))
print("Most frequent letter:", counter.most_common(1)[0][0])
print("Unique letters:", len(counter))
```

Result:

```
Name: Alexander
Name length: 9
Most frequent letter: a
Unique letters: 8
```

What happens here? `Counter(name)` takes a string and counts each character. `most_common(1)` returns a list with one `(letter, count)` pair, so `[0]` takes the pair, and `[0][0]` takes the letter from the pair. `len(counter)` is the number of keys, i.e., unique letters. You just ran a full mini-experiment: collected data, computed metrics, drew conclusions. That is how any research project starts — with curiosity about your own data.
<!--/SOLUTION-->

<!--QUIZ-->
What does statistics.mean(list) do?
- Computes the arithmetic mean
- Computes the sum of all elements
- Finds the largest element
* Correct answer: Computes the arithmetic mean
mean() divides the sum of elements by their count.

What is the median?
- The value in the middle of an ordered data series
- The most frequent value
- The maximum value
* Correct answer: The value in the middle of an ordered data series
The median splits an ordered dataset in half.

Which module counts element frequencies?
- collections.Counter
- statistics.mean
- random
* Correct answer: collections.Counter
Counter creates a dictionary where keys are elements and values are their counts.

What does counter.most_common(3) do?
- Returns the three most frequent elements with their counts
- Returns the three rarest elements
- Deletes three elements
* Correct answer: Returns the three most frequent elements with their counts
most_common(n) returns the n most frequent (element, count) pairs.

What is the pandas library for?
- Working with tabular data: loading, filtering, grouping
- Drawing games
- Sending emails
* Correct answer: Working with tabular data: loading, filtering, grouping
Pandas is the main data analytics tool in Python.

What does LinearRegression from scikit-learn do?
- Finds a linear relationship in data and predicts values
- Draws charts
- Sorts data
* Correct answer: Finds a linear relationship in data and predicts values
LinearRegression learns from examples and predicts new values by the found relationship.

What is a neural network?
- A program trained on examples that recognizes patterns
- A program for drawing
- A virus
* Correct answer: A program trained on examples that recognizes patterns
A neural network learns from data to later recognize or predict.

What does LLM stand for?
- Large Language Model
- Little Logic Machine
- Long List Maker
* Correct answer: Large Language Model
An LLM is a neural network trained on enormous volumes of text; this is how ChatGPT and similar models work.

Which neural network framework did Meta create?
- PyTorch
- Flask
- Django
* Correct answer: PyTorch
PyTorch was developed at Meta and became the standard for AI researchers.

What does len(counter) return for Counter("hello")?
- The number of unique characters
- The string length
- The sum of all frequencies
* Correct answer: The number of unique characters
In a Counter dictionary each character is one key, so len() shows the number of unique letters.
<!--/QUIZ-->
