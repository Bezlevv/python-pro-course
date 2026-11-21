---
title: Web scraping: BeautifulSoup and Selenium
summary: Fetching pages, parsing HTML, CSS selectors, dynamic pages with Selenium.
order: 9
duration: 45 min
difficulty: intermediate
tags: scraping, beautifulsoup, selenium
---

Scraping extracts data from websites.

## Requests + BeautifulSoup

```python
import requests
from bs4 import BeautifulSoup

r = requests.get("https://example.com", timeout=10)
soup = BeautifulSoup(r.text, "html.parser")
print(soup.title.text)
```

## Selectors

```python
soup.find("h1")
soup.find_all("a")
soup.select("div.item")
soup.select_one("p.price")
```

## Selenium for dynamic pages

```python
from selenium import webdriver
driver = webdriver.Chrome()
driver.get("https://example.com")
html = driver.page_source
driver.quit()
```

## Etiquette

Add headers, delays; respect robots.txt.

## Lesson summary

Use requests+BeautifulSoup for static pages; Selenium for dynamic ones.

<!--TASK-->
### Task 1 — Fetch
Fetch example.com and print the HTTP status.

### Task 2 — Parse title
Parse with BeautifulSoup and print the title text.

### Task 3 — find_all
Find all links and print their hrefs.

### Task 4 — CSS selectors
Select items with class and print texts.

### Task 5 — Single selector
Use select_one to get the first paragraph.

### Task 6 — Selenium basics
Open a page with Selenium and print driver.title.

### Task 7 — Cleanup
Write a function scrape_titles(url) returning all h2 texts.
<!--/TASK-->

<!--HINT-->
### Hint 1
requests.get(url).status_code.

### Hint 2
soup.title.text.

### Hint 3
soup.find_all("a") → get("href").

### Hint 4
soup.select(".item").

### Hint 5
soup.select_one("p").

### Hint 6
driver.get(url); driver.title.

### Hint 7
soup.find_all("h2") → [t.text].
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import requests
r = requests.get("https://example.com", timeout=10)
print(r.status_code)
```

### Solution 2
```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(r.text, "html.parser")
print(soup.title.text)
```

### Solution 3
```python
for a in soup.find_all("a"):
    print(a.get("href"))
```

### Solution 4
```python
for item in soup.select(".item"):
    print(item.text)
```

### Solution 5
```python
print(soup.select_one("p").text)
```

### Solution 6
```python
from selenium import webdriver
driver = webdriver.Chrome()
driver.get("https://example.com")
print(driver.title)
driver.quit()
```

### Solution 7
```python
def scrape_titles(url):
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    return [h.text for h in soup.find_all("h2")]
```
<!--/SOLUTION-->

<!--QUIZ-->
What does requests.get do?
- Fetches a page
- Parses HTML
- Clicks
- Saves
* Correct answer: Fetches a page
HTTP GET.

What is BeautifulSoup?
- HTML parser
- HTTP client
- Browser
- Framework
* Correct answer: HTML parser
Parses markup.

What does find_all return?
- List of tags
- First tag
- Strings
- None
* Correct answer: List of tags
All matches.

What is a CSS selector?
- s.select(".class")
- find_all only
- regex
- xpath
* Correct answer: s.select(".class")
Query syntax.

What does select_one do?
- Returns first match
- All matches
- None
- List
* Correct answer: Returns first match
Single element.

When use Selenium?
- Dynamic JS pages
- Static HTML
- API
- Never
* Correct answer: Dynamic JS pages
Rendered content.

What is driver.page_source?
- Rendered HTML
- JS
- Title
- Status
* Correct answer: Rendered HTML
After JS.

What should you respect?
- robots.txt
- Nothing
- Only HTML
- CSS
* Correct answer: robots.txt
Etiquette.

What is a User-Agent?
- A header identifying client
- A tag
- A parser
- A URL
* Correct answer: A header identifying client
Set politely.

What does .text do?
- Extracts text
- Extracts href
- Gets title
- Parses
* Correct answer: Extracts text
Tag content.

How to get an attribute?
- tag.get("href")
- tag.text
- tag.attr
- tag.href
* Correct answer: tag.get("href")
Attribute access.

What is timeout in requests?
- Max waiting seconds
- Min wait
- Retry count
- Header
* Correct answer: Max waiting seconds
Avoid hangs.
<!--/QUIZ-->
