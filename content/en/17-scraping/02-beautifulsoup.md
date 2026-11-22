---
title: BeautifulSoup: parsing HTML
summary: Find elements, selectors, extraction.
order: 2
duration: 45 min
difficulty: intermediate
tags: html, beautifulsoup
---

BeautifulSoup turns HTML into a tree.

## Parse

```python
from bs4 import BeautifulSoup
html = "<div class='card'><h2>Title</h2><a href='/x'>Link</a></div>"
soup = BeautifulSoup(html, "html.parser")
```

## Find

```python
h2 = soup.find("h2").text
link = soup.find("a")["href"]
```

## Selectors

```python
for card in soup.select(".card"):
    print(card.h2.text)
```

## Lesson summary

find/select extract data from HTML.

<!--TASK-->
### Task 1 — Parse
Parse a small HTML string.

### Task 2 — Find
Get h2 text.

### Task 3 — Attribute
Get href.

### Task 4 — Select
Select .card elements.

### Task 5 — All
Find all links.

### Task 6 — Clean
Get text without tags.

### Task 7 — Real
Fetch a page and parse.
<!--/TASK-->

<!--HINT-->
### Hint 1
BeautifulSoup.

### Hint 2
find("h2").

### Hint 3
["href"].

### Hint 4
select.

### Hint 5
find_all("a").

### Hint 6
get_text().

### Hint 7
requests + bs4.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from bs4 import BeautifulSoup
html = "<div class='card'><h2>Title</h2><a href='/x'>Link</a></div>"
soup = BeautifulSoup(html, "html.parser")
```

### Solution 2
```python
print(soup.find("h2").text)   # Title
```

### Solution 3
```python
print(soup.find("a")["href"])   # /x
```

### Solution 4
```python
for card in soup.select(".card"):
    print(card.h2.text)
```

### Solution 5
```python
for a in soup.find_all("a"):
    print(a["href"])
```

### Solution 6
```python
text = soup.get_text()
```

### Solution 7
```python
import requests
from bs4 import BeautifulSoup
resp = requests.get("https://httpbin.org/html")
soup = BeautifulSoup(resp.text, "html.parser")
print(soup.title.text)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is HTML?
- Markup
- A library
- A protocol
- None
* Correct answer: Markup
Tags.

What is BeautifulSoup?
- HTML parser
- HTTP client
- Database
- None
* Correct answer: HTML parser
Tree.

What is find?
- First match
- All
- Select
- None
* Correct answer: First match
Element.

What is find_all?
- All matches
- First
- One
- None
* Correct answer: All matches
List.

What is select?
- CSS selectors
- One tag
- Text
- None
* Correct answer: CSS selectors
.card.

What is .text?
- Inner text
- Tags
- Attributes
- None
* Correct answer: Inner text
Clean.

What is ["href"]?
- Attribute access
- Text
- Tag
- None
* Correct answer: Attribute access
Link.

What is get_text()?
- All text
- First text
- Tags
- None
* Correct answer: All text
Without tags.

What is a tag?
- Element
- Attribute
- Text
- None
* Correct answer: Element
div.

What is a class?
- CSS group
- Text
- Tag
- None
* Correct answer: CSS group
.card.

What is a selector?
- Pattern
- Attribute
- Text
- None
* Correct answer: Pattern
CSS.

What is scraping?
- Extracting web data
- Sending
- Rendering
- None
* Correct answer: Extracting web data
Automation.
<!--/QUIZ-->
