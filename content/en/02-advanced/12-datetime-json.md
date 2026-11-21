---
title: datetime and JSON
summary: Working with dates and times, formatting, parsing and serializing JSON.
order: 12
duration: 45 min
difficulty: intermediate
tags: datetime, json, strftime, serialization
---

Real programs deal with dates and data exchange. `datetime` and `json` are the core tools.

## datetime basics

```python
from datetime import datetime, date, timedelta

now = datetime.now()
print(now.year, now.month, now.day)
print(now.strftime("%d.%m.%Y %H:%M"))
```

## Parsing dates

```python
dt = datetime.strptime("25-01-2026", "%d-%m-%Y")
```

## timedelta

```python
tomorrow = date.today() + timedelta(days=1)
```

## JSON

```python
import json

data = {"name": "Anna", "age": 21}
s = json.dumps(data, ensure_ascii=False)
obj = json.loads(s)
```

## Files with JSON

```python
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
with open("data.json", encoding="utf-8") as f:
    loaded = json.load(f)
```

## Lesson summary

We learned datetime creation/formatting/parsing and JSON serialization.

<!--TASK-->
### Task 1 — Now
Print current year, month, day using datetime.now().

### Task 2 — Formatting
Print now in formats: "%d.%m.%Y" and "%H:%M:%S".

### Task 3 — Parsing
Parse "25-01-2026" with strptime and print the resulting date.

### Task 4 — timedelta
Print the date 7 days from today and 30 days ago.

### Task 5 — JSON dump/load
Create a dict, dump to a string with ensure_ascii=False, load it back and compare.

### Task 6 — JSON file
Save a list of dicts to a JSON file with indent=2; read it back.

### Task 7 — Dates difference
Compute the number of days between two dates (date objects).
<!--/TASK-->

<!--HINT-->
### Hint 1
from datetime import datetime.

### Hint 2
strftime codes: %Y, %m, %d, %H, %M, %S.

### Hint 3
strptime uses the same codes.

### Hint 4
timedelta(days=...).

### Hint 5
json.dumps(...); json.loads(...).

### Hint 6
json.dump(obj, f, ensure_ascii=False, indent=2).

### Hint 7
(d2 - d1).days.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from datetime import datetime
now = datetime.now()
print(now.year, now.month, now.day)
```

### Solution 2
```python
print(now.strftime("%d.%m.%Y"))
print(now.strftime("%H:%M:%S"))
```

### Solution 3
```python
dt = datetime.strptime("25-01-2026", "%d-%m-%Y")
print(dt.date())
```

### Solution 4
```python
from datetime import date, timedelta
today = date.today()
print(today + timedelta(days=7))
print(today - timedelta(days=30))
```

### Solution 5
```python
import json
data = {"name": "Anna", "age": 21}
s = json.dumps(data, ensure_ascii=False)
obj = json.loads(s)
print(obj == data)   # True
```

### Solution 6
```python
rows = [{"name": "Anna", "age": 21}, {"name": "Boris", "age": 30}]
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
with open("data.json", encoding="utf-8") as f:
    loaded = json.load(f)
print(loaded)
```

### Solution 7
```python
d1 = date(2026, 1, 1)
d2 = date(2026, 2, 1)
print((d2 - d1).days)   # 31
```
<!--/SOLUTION-->

<!--QUIZ-->
What does datetime.now() return?
- Current date and time
- Only date
- String
- Timestamp
* Correct answer: Current date and time
datetime object.

What does strftime do?
- Formats date to string
- Parses string
- Adds days
- Nothing
* Correct answer: Formats date to string
Format codes.

What does strptime do?
- Parses string to datetime
- Formats datetime
- Returns now
- Converts
* Correct answer: Parses string to datetime
Inverse of strftime.

What does timedelta represent?
- A duration
- A date
- A timezone
- A format
* Correct answer: A duration
Add/subtract.

How to add 7 days?
- date.today() + timedelta(days=7)
- date.today() + 7
- today + days(7)
- date+7
* Correct answer: date.today() + timedelta(days=7)
Correct API.

What does json.dumps do?
- Serializes to string
- Loads
- Formats file
- Parses
* Correct answer: Serializes to string
Python → JSON string.

What does json.loads do?
- Parses JSON string
- Dumps
- Opens file
- Converts
* Correct answer: Parses JSON string
JSON string → Python.

Why ensure_ascii=False?
- To keep non-ASCII characters
- To escape
- To speed up
- To sort
* Correct answer: To keep non-ASCII characters
For Russian text.

What does json.dump(obj, f) do?
- Writes JSON to a file
- Returns string
- Reads file
- Deletes
* Correct answer: Writes JSON to a file
File version of dumps.

What does json.load(f) do?
- Reads JSON from a file
- Returns string
- Writes
- Deletes
* Correct answer: Reads JSON from a file
File version of loads.

What is indent=2 for?
- Readable pretty-printing
- Compression
- Speed
- Sorting
* Correct answer: Readable pretty-printing
Indentation in the file.

How to compute difference in days?
- (d2 - d1).days
- d2 - d1
- days(d2 - d1)
- d2.days
* Correct answer: (d2 - d1).days
Attribute .days.
<!--/QUIZ-->
