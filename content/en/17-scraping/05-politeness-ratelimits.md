---
title: Scraping ethics: limits and throttling
summary: Polite scraping: robots.txt, terms of use, identification, throttling, and exponential backoff on errors.
order: 5
duration: 35 min
difficulty: intermediate
tags: ethics, robots.txt, throttling, rate limit, polite scraping
---

Scraping is not "looting" data — it's interacting with a server. A good scraper thinks not only about how to take everything faster, but also about how not to cause harm. Too-frequent requests overload the server, break sites for people, and lead to your IP being blocked. In this lesson — the rules of polite data collection and the tools that follow them.

## First ask permission: robots.txt

Almost every site has a `robots.txt` file — it sits in the domain root and describes what can be crawled and what cannot:

```python
import urllib.robotparser

rp = urllib.robotparser.RobotFileParser()
rp.set_url("https://quotes.toscrape.com/robots.txt")
rp.read()

print(rp.can_fetch("*", "https://quotes.toscrape.com/page/1/"))
print(rp.can_fetch("*", "https://quotes.toscrape.com/login"))
```

`can_fetch("*", url)` answers the question: "may my agent (`*` — any) load this URL?". The `urllib.robotparser` module is standard — nothing to install. Check `robots.txt` before walking a site — especially if it's not a training playground.

## Terms of use and personal data

`robots.txt` is a technical signal, but legally what's written in the site's terms of use also matters. Usually collecting personal data (names, addresses, phone numbers) and reselling it is prohibited. Scraping "for yourself" and "for research" isn't bad in itself, but if the data concerns people — think about whether you have the right to collect and store it. If a site explicitly forbids scraping in its terms — respect that. For experiments, use training sites like `quotes.toscrape.com` and `books.toscrape.com`: they were made specifically for practice.

## Introduce yourself: your own User-Agent

Servers look at `User-Agent` to understand who's come to them. An honest scraper states who it is and leaves a contact:

```python
HEADERS = {
    "User-Agent": "StudyScraper/1.0 (contact: student@example.com)",
}
```

If something goes wrong (for example, your script loops), the site owner can reach you. Anonymity isn't the goal here: polite identification lowers the chance of being blocked.

## Throttling: pauses between requests

Even if a site allows scraping, sending dozens of requests per second isn't wise. Add a pause between requests — **throttling**:

```python
import time
import requests

for page in range(1, 4):
    r = requests.get(f"https://quotes.toscrape.com/page/{page}/", timeout=10)
    print(page, r.status_code)
    time.sleep(2)  # at least 2 seconds between requests
```

A pause of 1–3 seconds is a reasonable minimum for a small walk. For serious projects, add a random "jitter" — a small random variation of the pause so traffic doesn't look perfectly rhythmic: `time.sleep(1 + random.random())`.

## Limits and error codes: 429

If you're too fast, the server responds with code **429 Too Many Requests** — "too many requests". That's an official signal: slow down. Some servers even say how long to wait via the `Retry-After` header:

```python
import time

delay = 1
for attempt in range(5):
    r = requests.get("https://httpbin.org/status/429", timeout=10)
    if r.status_code == 429:
        wait = float(r.headers.get("Retry-After", delay))
        print(f"429: waiting {wait} s")
        time.sleep(wait)
        delay *= 2
    else:
        r.raise_for_status()
        print("Success:", r.status_code)
        break
```

This is **exponential backoff**: with each failure we wait twice as long (1 s, 2 s, 4 s...). This algorithm gives the server time to recover and doesn't turn the scraper into a "hammer".

## Other polite techniques

- **Cache** already-downloaded pages — don't download the same thing twice.
- **Limit concurrency**: don't run 50 threads against one site.
- **Work off-peak hours** if the site is small.
- **Stop outside working hours** if the site explicitly says so.

## Summary

A polite scraper: checks `robots.txt`, reads the terms of use, introduces itself with its `User-Agent`, pauses between requests, and responds to `429` correctly with exponential backoff. This is not only ethical but also practical: polite guests are blocked less often, and data is collected more reliably. Let's build a polite client!

<!--TASK-->
### Task 1

Write a program `check_robots.py` that checks permissions for two training sites: `https://quotes.toscrape.com/` and `https://books.toscrape.com/`. For each, use `urllib.robotparser.RobotFileParser()`, set the `robots.txt` URL via `set_url`, load it via `read()`, and print the results of `can_fetch("*", ...)` for the main page and for the `/admin` address (if it falls under a ban — you'll see `False`). Output format: `Site: main -> True/False, /admin -> True/False`.

### Task 2

Write a class `PoliteFetcher` with a constructor `__init__(self, delay=2.0)`. Inside, store `self.delay` and a dictionary `self.headers` with a standard `User-Agent`: `"StudyScraper/1.0 (contact: student@example.com)"`. The method `get(self, url)` does `requests.get(url, headers=self.headers, timeout=10)`, pausing `self.delay` seconds between consecutive requests. Test it: collect the first 3 pages of `https://quotes.toscrape.com/page/{n}/`, and for each print the number, the status code, and how many seconds passed since the previous request (`time.time()`).

### Task 3

Write a function `fetch_with_backoff(url, max_attempts=5)` that makes a GET request with a 10-second timeout. If the status is `429` — read the `Retry-After` header (if it's missing, use the current delay) and wait that many seconds, then double the delay and try again. If the status is different — call `raise_for_status()` and return the response. Test it on `https://httpbin.org/status/429` with `max_attempts=2`: the program should print two warnings and fail with a `RuntimeError` after attempts run out.

### Task 4

Collect the contents of the first two pages of `https://books.toscrape.com/` the polite way: the `PoliteFetcher` class from task 2 with `delay=1`. For each page, print the number and the count of book cards (`article.product_pod`), computed via BeautifulSoup. Make sure the pause between requests is at least 1 second. Print the total number of books over the two requests.

### Task 5

Put it all together: write a class `PoliteScraper` that combines a `robots.txt` check (caching the result in a dictionary `self.robots`), standard headers, and throttling with a delay. The method `fetch(self, url)` first checks the site's `robots.txt` via `can_fetch("*", url)`; if disallowed — prints `Forbidden by robots.txt: <url>` and returns `None`. If allowed — makes the request with a pause. Test it on `https://quotes.toscrape.com/page/1/` (should return a response) and on `https://quotes.toscrape.com/login` (the result may be anything — print what the method returned).
<!--/TASK-->

<!--HINT-->
### Hint 1

`RobotFileParser` is a standard module `urllib.robotparser`. The order: create, `set_url` (robots.txt file URL), `read()`, then `can_fetch("*", url)`. Training sites usually allow almost everything, but `/admin` is often closed. Print results with f-strings.

### Hint 2

In the class, store `self.last_request_time` — the moment of the last request. Before a new request, compute `elapsed = time.time() - self.last_request_time` and, if `elapsed < self.delay`, sleep `self.delay - elapsed` seconds. After the request, update `self.last_request_time = time.time()`. That's precise throttling, not just "sleep after every request".

### Hint 3

Keep the delay in a `delay` variable, starting at 1. On `429`: `wait = float(r.headers.get("Retry-After", delay))`, then `time.sleep(wait)` and `delay *= 2`. After `max_attempts` attempts — `raise RuntimeError("Rate limit did not let go")`. Keep in mind: `httpbin.org/status/429` always answers 429.

### Hint 4

Parsing bookstore pages: `BeautifulSoup(r.text, "lxml")` and `soup.select("article.product_pod")`. Use the class from task 2 — but since you're writing a separate file, copy the class into it. Measure the pause via `time.time()` before and after `get()`.

### Hint 5

Split the URL via `urllib.parse.urlparse(url)` — the domain: `parsed.netloc`. In `self.robots` store a dictionary `{domain: RobotFileParser}`. If the domain isn't there — create a parser, `set_url(f"https://{domain}/robots.txt")`, `read()` and save it. Then `self.robots[domain].can_fetch("*", url)`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1

```python
import urllib.robotparser

for site in ("https://quotes.toscrape.com", "https://books.toscrape.com"):
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(site + "/robots.txt")
    rp.read()

    main = rp.can_fetch("*", site + "/")
    admin = rp.can_fetch("*", site + "/admin")
    print(f"{site}: main -> {main}, /admin -> {admin}")
```

Step-by-step breakdown:

- `RobotFileParser` is a standard class from `urllib.robotparser`. It can download `robots.txt` and answer permission questions.
- `set_url(site + "/robots.txt")` points to the file's address; `read()` loads and parses it.
- `can_fetch("*", url)` returns `True`/`False`: may agent `*` (any) load `url`.
- Training sites usually allow crawling pages but close service paths like `/admin` — there you'll see `False`.
- Note: `robots.txt` is checked per domain, before the walk. That's the first line of a "polite scraper" — learn the rules before visiting.

### Solution 2

```python
import time
import requests

class PoliteFetcher:
    def __init__(self, delay=2.0):
        self.delay = delay
        self.headers = {
            "User-Agent": "StudyScraper/1.0 (contact: student@example.com)",
        }
        self.last_request_time = 0.0

    def get(self, url):
        if self.last_request_time:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.delay:
                time.sleep(self.delay - elapsed)
        r = requests.get(url, headers=self.headers, timeout=10)
        self.last_request_time = time.time()
        return r

fetcher = PoliteFetcher(delay=2.0)
prev = None
for page in range(1, 4):
    r = fetcher.get(f"https://quotes.toscrape.com/page/{page}/")
    now = time.time()
    gap = now - prev if prev else 0.0
    prev = now
    print(f"Page {page}: status {r.status_code}, elapsed {gap:.1f} s")
```

Step-by-step breakdown:

- The class wraps polite behavior: headers, throttling, a single point for all requests.
- `self.last_request_time` stores the moment of the previous request. Before a new one we compare `elapsed` with `self.delay`: has enough time passed. If not — we sleep exactly as long as is missing. This is more precise than "sleep after every request" — the interval between requests doesn't accumulate error.
- `self.headers` — honest identification: a `User-Agent` with a contact. It lets the site owner reach you if there are problems.
- In the test, `gap` shows the actual pause between requests — it's not less than 2 seconds. If a request took long, `gap` would account for it.
- Such a class is the foundation of any serious scraper: the rules of politeness live in one place.

### Solution 3

```python
import time
import requests

def fetch_with_backoff(url, max_attempts=5):
    delay = 1.0
    for attempt in range(max_attempts):
        r = requests.get(url, timeout=10)
        if r.status_code == 429:
            wait = float(r.headers.get("Retry-After", delay))
            print(f"Attempt {attempt + 1}: 429, waiting {wait} s")
            time.sleep(wait)
            delay *= 2
            continue
        r.raise_for_status()
        return r
    raise RuntimeError("Rate limit did not let go")

try:
    fetch_with_backoff("https://httpbin.org/status/429", max_attempts=2)
except RuntimeError as e:
    print("Result:", e)
```

Step-by-step breakdown:

- `delay = 1.0` — the initial pause. On each failure it doubles: 1 s, 2 s, 4 s, 8 s...
- On `429` we first try to take `Retry-After` — a header in which the server itself says how long to wait. If it's missing — we use the current `delay`.
- `time.sleep(wait)` — the actual wait. `delay *= 2` prepares the next, longer pause.
- `continue` moves to the next attempt. If the status isn't 429 — `raise_for_status()` checks the remaining errors, and success returns `r`.
- After `max_attempts` failures — `RuntimeError`: the scraper won't hammer forever; it honestly reports it couldn't get past the limit.
- The test on `httpbin.org/status/429` always answers 429, so the program prints the warning twice and fails with `RuntimeError` — exactly as designed.

### Solution 4

```python
import time
import requests
from bs4 import BeautifulSoup

class PoliteFetcher:
    def __init__(self, delay=1.0):
        self.delay = delay
        self.headers = {"User-Agent": "StudyScraper/1.0 (contact: student@example.com)"}
        self.last_request_time = 0.0

    def get(self, url):
        if self.last_request_time:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.delay:
                time.sleep(self.delay - elapsed)
        r = requests.get(url, headers=self.headers, timeout=10)
        self.last_request_time = time.time()
        return r

fetcher = PoliteFetcher(delay=1.0)
total = 0

for page in range(1, 3):
    t0 = time.time()
    r = fetcher.get(f"https://books.toscrape.com/catalogue/page-{page}.html")
    soup = BeautifulSoup(r.text, "lxml")
    books = soup.select("article.product_pod")
    total += len(books)
    print(f"Page {page}: {len(books)} books, request took {time.time() - t0:.1f} s")

print("Total books:", total)
```

Step-by-step breakdown:

- Pay attention to the addresses: the bookstore's pagination isn't `page/1/` but `catalogue/page-1.html` — every site does it its way. A scraper must be able to notice that.
- Fetching through `PoliteFetcher` guarantees a pause of at least 1 second between requests.
- `BeautifulSoup(r.text, "lxml")` + `select("article.product_pod")` count the book cards on the page (there are 20).
- Measuring `time.time() - t0` shows how long the whole "request + pause" cycle took. Even on a fast network the interval between requests will be at least the specified one.
- Summing books across pages gives the total. This is a training example: collection with pagination and respect for the server.

### Solution 5

```python
import time
import requests
from urllib.parse import urlparse
import urllib.robotparser

class PoliteScraper:
    def __init__(self, delay=1.0):
        self.delay = delay
        self.headers = {"User-Agent": "StudyScraper/1.0 (contact: student@example.com)"}
        self.last_request_time = 0.0
        self.robots = {}

    def _check_robots(self, url):
        domain = urlparse(url).netloc
        if domain not in self.robots:
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(f"https://{domain}/robots.txt")
            rp.read()
            self.robots[domain] = rp
        return self.robots[domain].can_fetch("*", url)

    def fetch(self, url):
        if not self._check_robots(url):
            print(f"Forbidden by robots.txt: {url}")
            return None
        if self.last_request_time:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.delay:
                time.sleep(self.delay - elapsed)
        r = requests.get(url, headers=self.headers, timeout=10)
        self.last_request_time = time.time()
        return r

scraper = PoliteScraper(delay=1.0)

r = scraper.fetch("https://quotes.toscrape.com/page/1/")
print("Main page:", r.status_code if r else None)

r = scraper.fetch("https://quotes.toscrape.com/login")
print("/login:", r.status_code if r else None)
```

Step-by-step breakdown:

- `_check_robots(url)` determines the domain via `urlparse(url).netloc` and checks the `self.robots` cache: if this domain hasn't been checked yet — it creates and stores a `RobotFileParser`. A repeated check doesn't re-download the file.
- If `robots.txt` forbids the URL — the method prints a warning and returns `None`. The scraper doesn't break the rules even by accident.
- Throttling is the same as in `PoliteFetcher`: a pause up to the minimum interval between requests.
- An honest `User-Agent` with a contact is set once in `self.headers`.
- Test: `/page/1/` is usually allowed and will return a response; `/login` is a service page, its status can be anything — the important thing is that the program honestly reports the check result.
- Such a class is a ready "skeleton" of a polite scraper: rules, limits, and identification are gathered in one place.
<!--/SOLUTION-->

<!--QUIZ-->
What is robots.txt?
- A file with site visit statistics
- A file with rules about which parts of a site can be crawled
- An encrypted file with passwords
- A service file for server configuration
* Correct answer: A file with rules about which parts of a site can be crawled
robots.txt sits in the site root and describes what is allowed/forbidden for crawlers.

How do you check a robots.txt permission in Python?
- requests.get("robots.txt")
- urllib.robotparser.RobotFileParser().can_fetch()
- bs4.BeautifulSoup
- os.stat("robots.txt")
* Correct answer: urllib.robotparser.RobotFileParser().can_fetch()
RobotFileParser loads the file; can_fetch("*", url) answers whether it can be downloaded.

What does the HTTP code 429 mean?
- The page was not found
- Too many requests (rate limit)
- Authorization is required
- Internal server error
* Correct answer: Too many requests (rate limit)
429 Too Many Requests — the server asks you to slow down; a Retry-After header is often included.

What is throttling?
- Speeding up requests through concurrency
- Limiting the request rate with pauses
- Compressing transmitted data
- Encrypting requests
* Correct answer: Limiting the request rate with pauses
Throttling inserts delays between requests so as not to overload the server.

Why double the delay in exponential backoff?
- To finish the walk faster
- To give the server time to recover and not "hammer" it
- To bypass an IP block
- To save traffic
* Correct answer: To give the server time to recover and not "hammer" it
With each failure we wait twice as long — the load on the server drops, the chance of success grows.

Why specify your contact in the User-Agent?
- Without it requests aren't sent
- So the site owner can reach you if there are problems
- To speed up the server's response
- To hide your IP
* Correct answer: So the site owner can reach you if there are problems
Honest identification lowers the risk of blocking and allows problems to be solved politely.

What does the HTTP code 403 mean during scraping?
- Access is denied — retrying the request is pointless
- The page was not found
- The server is temporarily overloaded
- A redirect is required
* Correct answer: Access is denied — retrying the request is pointless
403 is a permanent refusal; retries won't help here. Unlike 5xx, only temporary errors are retried.

Why add a random "jitter" to the pause between requests?
- So traffic doesn't look perfectly rhythmic
- To speed up data collection
- To bypass robots.txt bans
- It's a requirement of the smtplib module
* Correct answer: So traffic doesn't look perfectly rhythmic
The expression time.sleep(1 + random.random()) makes intervals uneven — the load looks more natural.
<!--/QUIZ-->
