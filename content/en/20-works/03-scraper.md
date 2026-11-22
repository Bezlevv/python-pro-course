---
title: Price/news scraper
summary: Combine requests, BeautifulSoup, export.
order: 3
duration: 50 min
difficulty: intermediate
tags: scraping, project
---

Scrape and export structured data.

## Plan

1. Fetch page;
2. Parse with BeautifulSoup;
3. Extract fields;
4. Save to CSV.

## Code

```python
import csv
import requests
from bs4 import BeautifulSoup

resp = requests.get("https://example.com/items", timeout=10)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

rows = []
for item in soup.select(".item"):
    name = item.select_one(".name").text.strip()
    price = item.select_one(".price").text.strip()
    rows.append([name, price])

with open("items.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(rows)
```

## Lesson summary

Fetch → parse → extract → save.

<!--TASK-->
### Task 1 — Fetch
Get the page and check status.

### Task 2 — Parse
Parse with BeautifulSoup.

### Task 3 — Extract
Pull names and prices.

### Task 4 — Clean
Strip whitespace.

### Task 5 — CSV
Save to CSV.

### Task 6 — Error
Handle missing fields.

### Task 7 — Delay
Add politeness delay.
<!--/TASK-->

<!--HINT-->
### Hint 1
requests.

### Hint 2
BeautifulSoup.

### Hint 3
select.

### Hint 4
strip().

### Hint 5
csv.writer.

### Hint 6
try/except.

### Hint 7
time.sleep.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
resp = requests.get("https://example.com/items", timeout=10)
resp.raise_for_status()
```

### Solution 2
```python
soup = BeautifulSoup(resp.text, "html.parser")
```

### Solution 3
```python
for item in soup.select(".item"):
    name = item.select_one(".name").text
    price = item.select_one(".price").text
```

### Solution 4
```python
name = name.strip()
price = price.strip()
```

### Solution 5
```python
import csv
with open("items.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(rows)
```

### Solution 6
```python
el = item.select_one(".price")
price = el.text.strip() if el else "n/a"
```

### Solution 7
```python
import time
# между запросами
time.sleep(1)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is scraping?
- Extracting data
- Sending data
- Rendering
- None
* Correct answer: Extracting data
Web.

What is parse?
- Build tree
- Fetch
- Save
- None
* Correct answer: Build tree
Soup.

What is extract?
- Pick fields
- Fetch
- Save
- None
* Correct answer: Pick fields
Select.

What is clean?
- strip whitespace
- Fetch
- Log
- None
* Correct answer: strip whitespace
Normalize.

What is CSV?
- Table format
- Binary
- JSON
- None
* Correct answer: Table format
Writer.

What is newline=""?
- CSV safety
- Empty rows
- Error
- None
* Correct answer: CSV safety
Windows.

What is raise_for_status?
- Checks code
- Sends
- Saves
- None
* Correct answer: Checks code
Error.

What is timeout?
- Wait limit
- Retry
- Header
- None
* Correct answer: Wait limit
Seconds.

What is select_one?
- First match
- All
- None
- Text
* Correct answer: First match
Element.

What is .text?
- Inner text
- Tags
- Attrs
- None
* Correct answer: Inner text
String.

What is a row?
- Data line
- A column
- A file
- None
* Correct answer: Data line
List.

What is politeness?
- Respectful load
- Speed
- Ignoring
- None
* Correct answer: Respectful load
Delay.
<!--/QUIZ-->
