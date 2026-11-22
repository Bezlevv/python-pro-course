---
title: Pagination, APIs, and JSON
summary: Walking through pages: the page parameter, cursors, Next links, working with APIs and JSON, protecting against infinite loops.
order: 4
duration: 40 min
difficulty: advanced
tags: pagination, api, json, requests, cursors, loops
---

Rare is the site that serves all its data on a single page. Usually data is split across pages — this is called **pagination**. A scraper must be able to walk through all the pages to the end without getting stuck in an infinite loop. In this lesson we'll cover three kinds of pagination: by page number, via a "Next" link, and via a cursor — and along the way we'll learn to take data straight from an API, bypassing HTML.

## Pagination by page number

The simplest kind — a page parameter in the address: `?page=2`, `?page=3`. Many sites and APIs work this way:

```python
import requests

for page in range(1, 4):
    r = requests.get(
        "https://jsonplaceholder.typicode.com/todos",
        params={"_page": page, "_limit": 10},
        timeout=10,
    )
    items = r.json()
    if not items:
        break  # an empty page means the end
    print(f"Page {page}: {len(items)} tasks")
```

The key idea: a **stop condition**. The loop runs while the page isn't empty. An empty response is a signal that the data has run out. If you don't check this, the loop will go infinite or hammer the server with hundreds of empty requests.

## Pagination via a "Next" link

On HTML sites there's often no numbering in the URL — only a "Next page" button. We already peeked at walking such pages: take the link, follow it while it exists:

```python
import requests
from bs4 import BeautifulSoup

base = "https://quotes.toscrape.com"
url = "/page/1/"
authors = set()

while url:
    r = requests.get(base + url, timeout=10)
    soup = BeautifulSoup(r.text, "lxml")
    for small in soup.select("small.author"):
        authors.add(small.get_text())

    next_link = soup.select_one("li.next a")
    url = next_link["href"] if next_link else None

print("Unique authors:", len(authors))
```

Here the `while url:` loop runs while there is a next page. `None` in place of the link ends the walk. That's the second stop condition.

## Pagination in APIs: the Link header

APIs often don't show the total number of pages; instead they return a special `Link` header — a list of links to the next/previous/last page:

```python
r = requests.get(
    "https://api.github.com/users/python/repos",
    params={"per_page": 5, "page": 1},
    headers={"User-Agent": "my-app"},
    timeout=10,
)
print(r.headers.get("Link"))
```

The response looks roughly like this: `<https://api.github.com/user/...?page=2&per_page=5>; rel="next", ...`. A header parser splits it into individual links and follows `rel="next"`. That's cursor pagination, which comes next.

## Cursor pagination

A cursor is a "bookmark": the server doesn't say "give me page 5", but gives a cursor token that determines the position after the last record delivered. This is convenient when data keeps changing: inserting a new record doesn't shift pages. An example is the GitHub API with the `since` parameter when listing repositories. The principle is the same: you request with a cursor, get a batch of data and a new cursor, repeat until the batch runs empty.

## Why API is better than HTML

If a site has an official API — use it. It's faster (clean JSON without HTML clutter), more stable (markup changes; APIs less often), and more polite (the site itself expects such requests). JSON turns into Python structures with a single `r.json()` call:

```python
data = r.json()
print(data[0]["title"])  # title of the first task
```

## Protection against infinite loops

Any page walk should have at least two safeguards:

1. **A natural stop** — an empty page, the absence of a "Next" link, a cursor of `None`.
2. **An artificial limit** — a maximum number of pages, e.g. `max_pages=50`. Even if something on the site breaks, the program will stop.

```python
MAX_PAGES = 50
for page in range(1, MAX_PAGES + 1):
    ...
```

## Summary

Pagination comes by number, by a "Next" link, and by cursor. Stop conditions — an empty batch, a missing link, or a page limit. And if a JSON API is available, prefer it over HTML: less traffic and more reliable. Let's verify in practice.

<!--TASK-->
### Task 1

Write a program `json_loop.py` that collects all tasks from the API `https://jsonplaceholder.typicode.com/todos` via pagination on the `_page` parameter (10 tasks per page: `params={"_page": page, "_limit": 10}`). Walk pages from 1 until the response becomes an empty list. Count the total number of tasks (`len` of all batches) and print `Total tasks: N`. Then print the first three task titles from the first page.

### Task 2

Collect all public repositories of the user `python` from the GitHub API: `https://api.github.com/users/python/repos` with the parameters `per_page=100` and `page=1,2,...`. Add the `User-Agent` header and `timeout=10`. The loop runs while the batch is not empty. Print the total number of repositories and the first three names from the `name` field. Note: if the server returned fewer than 100 repositories, less than `per_page`, that's also a sign of the end.

### Task 3

Walk all pages of the site `https://quotes.toscrape.com/` via the "Next" link. Start at `/page/1/`, on each page collect authors (`small.author`) into a set. Continue while a `li.next a` link exists; on the last page it's absent. Print the total number of unique authors across the whole site and the first five names in alphabetical order. Keep a 1-second pause between requests (`time.sleep(1)`).

### Task 4

Write a function `collect_authors(max_pages=3)` that collects authors from the quote site's pages, but stops no later than `max_pages` pages, even if a "Next" link still exists. Inside the loop, print the page number. Call the function with `max_pages=3` and show that it collected data from exactly three pages, then explain in a comment why such an artificial limit is needed.

### Task 5

Write a `Link` header parser and use it with the GitHub API. The function `parse_link_header(header)` should return a dictionary like `{"next": "...", "prev": "..."}`, parsing the string: parts are separated by commas, inside each — a URL in `<...>` and `rel="..."`. Then use it to walk the repository pages of `python` (the first page with `per_page=5`), following `next` while it exists. Print how many pages were walked and how many repositories were collected in total.
<!--/TASK-->

<!--HINT-->
### Hint 1

`requests.get(..., params={"_page": page, "_limit": 10})` — parameters in the address. `r.json()` returns a list; check `if not items: break`. Collect all batches into one big list: `all_items.extend(items)` or simply add `len(items)` to a counter.

### Hint 2

The GitHub API requires `User-Agent` — without it the request may be rejected. Pages: `params={"per_page": 100, "page": page}`. A sign of the end: an empty list or a length below 100. Take the repository name: `repo["name"]`.

### Hint 3

Use `while url:` — the loop runs while the URL isn't `None`. Find the link via `soup.select_one("li.next a")`, the attribute — `["href"]`. On the last page `select_one` returns `None` — the loop ends. Between requests — `time.sleep(1)`.

### Hint 4

The `max_pages` parameter limits the number of iterations: `for page in range(1, max_pages + 1)`. Inside the loop, after processing the page, check the "Next" link and `break` if it's missing. An artificial limit guards against an infinite loop when the markup is broken.

### Hint 5

Each header part is `"<URL>; rel=\"next\""`. Split by comma: `header.split(",")`, then for each part: `part.split(";")` — the first element is the URL (strip `<` and `>`), the second is `rel="..."` (strip `rel="` and `"`). Follow: `requests.get(next_url, headers={"User-Agent": "my-app"}, timeout=10)`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1

```python
import requests

total = 0
all_items = []

for page in range(1, 100):
    r = requests.get(
        "https://jsonplaceholder.typicode.com/todos",
        params={"_page": page, "_limit": 10},
        timeout=10,
    )
    items = r.json()
    if not items:
        break
    all_items.extend(items)
    total += len(items)

print("Total tasks:", total)
for item in all_items[:3]:
    print("-", item["title"])
```

Step-by-step breakdown:

- `range(1, 100)` — a safety frame: if something goes wrong (the server stops returning empty pages), the loop will still stop at page 99.
- `params={"_page": page, "_limit": 10}` — JSONPlaceholder supports pagination with the `_page` and `_limit` parameters. It's an imitation of real APIs.
- `r.json()` turns the response into a list of dictionaries. `if not items: break` — the stop condition: an empty list means the data has run out.
- `all_items.extend(items)` accumulates all tasks in one list; `total += len(items)` counts them in parallel.
- JSONPlaceholder contains 200 tasks. 10 per page — 20 pages, the last one returns 10 tasks, and the 21st returns an empty list, ending the loop.
- Result: `Total tasks: 200`, then three first titles. That's what a standard "pages by number" walk looks like.

### Solution 2

```python
import requests

repos = []
page = 1

while True:
    r = requests.get(
        "https://api.github.com/users/python/repos",
        params={"per_page": 100, "page": page},
        headers={"User-Agent": "my-app"},
        timeout=10,
    )
    r.raise_for_status()
    batch = r.json()
    if not batch:
        break
    repos.extend(batch)
    page += 1

print("Total repositories:", len(repos))
for repo in repos[:3]:
    print("-", repo["name"])
```

Step-by-step breakdown:

- `while True:` with an explicit `break` — a typical form of walking pages when the number of pages isn't known in advance.
- `per_page=100` — the maximum batch size of the GitHub API: fewer requests, faster collection.
- `r.raise_for_status()` turns HTTP errors into exceptions — if the API returns 403 or 404, we'll find out immediately instead of parsing empty JSON.
- `if not batch: break` — an empty batch means the end. An additional sign: if `len(batch) < 100` — that's the last page, but an empty list is more reliable.
- `repos.extend(batch)` collects repository dictionaries; `repo["name"]` — the name (e.g. `Python-2.x`, `python-docs-zh-tw`...).
- The GitHub API without a token allows ~60 requests per hour per IP. Our walk spends 2 requests — easily within the limit. Respect limits: we discuss them in the next lesson.

### Solution 3

```python
import time
import requests
from bs4 import BeautifulSoup

base = "https://quotes.toscrape.com"
url = "/page/1/"
authors = set()

while url:
    r = requests.get(base + url, timeout=10)
    soup = BeautifulSoup(r.text, "lxml")
    for small in soup.select("small.author"):
        authors.add(small.get_text())

    next_link = soup.select_one("li.next a")
    url = next_link["href"] if next_link else None

    time.sleep(1)

print("Unique authors:", len(authors))
for name in sorted(authors)[:5]:
    print("-", name)
```

Step-by-step breakdown:

- `while url:` — the loop lives while there's an address for the current page.
- `soup.select("small.author")` — the authors of the current page; `authors.add(...)` puts them into a set with deduplication.
- `soup.select_one("li.next a")` looks for the "Next" link. On the last page it's absent — `next_link` becomes `None`, and `url = None` ends the loop.
- `time.sleep(1)` — a polite pause between requests: we don't hammer the server, we let it breathe. More details in the ethics lesson.
- The site has 10 pages, ~100 quotes, and several dozen unique authors. The set handles repeats perfectly.
- This is a universal site-walking algorithm: "follow Next while it exists". It doesn't depend on page numbering in the URL.

### Solution 4

```python
import requests
from bs4 import BeautifulSoup

def collect_authors(max_pages=3):
    authors = set()
    for page in range(1, max_pages + 1):
        r = requests.get(f"https://quotes.toscrape.com/page/{page}/", timeout=10)
        soup = BeautifulSoup(r.text, "lxml")
        for small in soup.select("small.author"):
            authors.add(small.get_text())
        next_link = soup.select_one("li.next a")
        if next_link is None:
            break
        print(f"Processed page {page}")
    return authors

authors = collect_authors(max_pages=3)
print("Collected authors:", len(authors))
```

Step-by-step breakdown:

- `for page in range(1, max_pages + 1)` — a hard limit on iterations: the `max_pages` parameter bounds the depth of the walk.
- Inside the loop, after collecting data, the "Next" link is checked: if it's absent (`None`) — `break`, we reached the end before the limit.
- The function returns the set of authors. Calling with `max_pages=3` processes exactly three pages, even if the site allows going further.
- Why is an artificial limit needed? If the site's markup breaks (the "Next" link starts pointing to itself) or an infinite feed appears, a loop without a limit would run forever and take the server down. The limit is a safety fuse.
- Such a function is a reusable building block: `collect_authors(3)` — a quick collection, `collect_authors(100)` — a full walk.

### Solution 5

```python
import requests

def parse_link_header(header):
    result = {}
    if not header:
        return result
    for part in header.split(","):
        section = part.split(";")
        url = section[0].strip().strip("<>")
        rel = section[1].split("=")[1].strip('"')
        result[rel] = url
    return result

repos = []
page_url = "https://api.github.com/users/python/repos?per_page=5&page=1"
pages = 0

while page_url:
    r = requests.get(page_url, headers={"User-Agent": "my-app"}, timeout=10)
    r.raise_for_status()
    repos.extend(r.json())
    pages += 1
    links = parse_link_header(r.headers.get("Link"))
    page_url = links.get("next")

print("Pages walked:", pages)
print("Repositories collected:", len(repos))
```

Step-by-step breakdown:

- `parse_link_header()` parses the `Link` header. Each comma-separated part looks like this: `<https://...?page=2&per_page=5>; rel="next"`. `split(";")` splits it into the URL and the `rel` parameter, then `strip("<>")` and `strip('"')` remove the framing.
- The result is a dictionary `{"next": "...", "prev": "..."}`. This is the RFC 5988 standard, used by GitHub, GitLab, and many other APIs.
- `while page_url:` — we follow `next` while it exists. GitHub returns a link to the last page without `next` — and the loop ends correctly.
- `repos.extend(r.json())` accumulates repositories. With `per_page=5`, `python` (~150 repositories) would need ~30 requests — so in real collection `per_page=100` is better.
- That's how cursor pagination works: the client doesn't guess page numbers; it follows the links the server gives. It's the most reliable way in APIs.
<!--/SOLUTION-->

<!--QUIZ-->
Which sign indicates that pagination by page numbers has ended?
- The page returned an empty list
- The page returned code 200
- The page parameter became greater than 100
- The Content-Type header changed
* Correct answer: The page returned an empty list
An empty batch is a signal that the data has run out; the loop should be ended.

How do you correctly walk the pages of a site that only has a "Next" button?
- Iterate page numbers from 1 to 1000
- Follow the "Next" link while it exists
- Download only the first page
- Use random navigation
* Correct answer: Follow the "Next" link while it exists
We find the li.next a link and follow it while it exists; on the last page it's absent.

What does the Link header in a GitHub API response contain?
- The response size in bytes
- Links to neighboring pages (next, prev, etc.)
- The session cookie
- The page encoding
* Correct answer: Links to neighboring pages (next, prev, etc.)
Link (RFC 5988) lists page URLs with rel="next", rel="prev", etc.

Why does a scraper need an artificial page limit (max_pages)?
- To speed up the program
- To protect against an infinite loop on site errors
- To bypass blocking
- To reduce code size
* Correct answer: To protect against an infinite loop on site errors
If the "Next" link points to itself or the site is broken, the limit stops the program.

Why is an API preferable to HTML for data collection?
- HTML isn't used anywhere anymore
- An API returns clean structured data (JSON), faster and more stable
- An API is always free and unlimited
- HTML can't be downloaded with requests
* Correct answer: An API returns clean structured data (JSON), faster and more stable
JSON doesn't need to be parsed like HTML, markup changes less often, and there's less traffic.

What is cursor pagination?
- Walking pages via numbered URLs
- Using a cursor token that determines the position after the last delivered record
- Downloading all data in one request
- Pagination without stop conditions
* Correct answer: Using a cursor token that determines the position after the last delivered record
A cursor is resilient to inserts of new records: the server gives a "bookmark" instead of a page number.

What does r.json() do?
- Parses the response body as JSON and returns lists/dictionaries
- Saves the response to a file on disk
- Prints the page's raw HTML
- Returns the response status code
* Correct answer: Parses the response body as JSON and returns lists/dictionaries
json() turns a JSON response into regular Python structures — convenient to work with directly.

Which sign indicates that pagination via a "Next" link has ended?
- The page has no "Next" link: select_one returned None
- The page returned code 404
- The response has an empty Content-Type header
- The page number reached 99
* Correct answer: The page has no "Next" link: select_one returned None
On the last page there's no li.next block, so url becomes None and the while url: loop ends.
<!--/QUIZ-->
