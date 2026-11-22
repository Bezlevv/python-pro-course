---
title: HTTP for scraping: sessions, headers, proxies
summary: Why a scraper should behave like a browser: sessions and cookies, headers, User-Agent, timeouts, retries, and proxies in requests.
order: 1
duration: 40 min
difficulty: advanced
tags: http, requests, sessions, headers, proxies, retries
---

In the previous module you already mastered the `requests` library. But scraping places special demands on an HTTP client: many sites defend themselves against scripts, serve different content to different clients, and don't like being hammered at a steady pace. In this lesson we'll build a "battle-ready" HTTP client: with sessions, proper headers, timeouts, retries, and proxies. This is the foundation of any scraper — without it, even beautiful HTML work won't bring you any data.

## Sessions: why a single requests.get() isn't enough

Every `requests.get()` is an independent visit. The server won't remember you between requests unless you save its "markers" yourself — cookies. Cookies are small pieces of data (usually a string like `sessionid=abc123`) that the server issues on your first visit and checks afterwards. That's how logins, shopping carts, and "remember me" work.

To make cookies persist automatically, use a `requests.Session()` object:

```python
import requests

s = requests.Session()
# the server will issue two cookies
s.get("https://httpbin.org/cookies/set?name=anya&role=student")
# check that they were saved
print(s.get("https://httpbin.org/cookies").json())
```

A session is a "container" that holds cookies, default headers, and even proxy settings. If you create a new session, it starts from a clean slate.

## Headers: introducing ourselves properly

The server sees not only the URL, but also the request headers. The most important one is `User-Agent`: in it the client tells who it is (a browser, a mobile app, a script). Some sites block an empty `User-Agent` or serve a "trimmed" version of the page to scripts:

```python
headers = {
    "User-Agent": "MyCourseScraper/1.0 (student@example.com)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}
r = requests.get("https://httpbin.org/headers", headers=headers, timeout=10)
print(r.json()["headers"]["User-Agent"])
```

Important: the purpose of headers is to politely identify yourself — not to pretend to be a real browser in order to deceive the site. The `Accept` header tells the server which response formats you're willing to accept, and `Accept-Language` — which language you prefer.

## Timeouts: so you never hang forever

A scraper that runs forever is worse than a scraper that fails. If the server goes silent, `requests` without `timeout` will wait indefinitely. Always pass `timeout` — the number of seconds to wait for a response:

```python
r = requests.get("https://httpbin.org/delay/2", timeout=5)
```

If the server doesn't make it in time, a `requests.Timeout` exception is raised. Catch it and decide what to do: try again or skip the page.

## Retries: when the error is temporary

Status codes `500`, `502`, `503`, `504` mean the server is temporarily unwell, and a repeated request a second or two later may succeed. You can write loops with `time.sleep` by hand, but `requests` offers an elegant way — `HTTPAdapter` combined with `Retry` from `urllib3`:

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

s = requests.Session()
retry = Retry(total=3, backoff_factor=0.5,
              status_forcelist=[500, 502, 503, 504])
s.mount("https://", HTTPAdapter(max_retries=retry))
```

`total=3` — the maximum number of attempts, `backoff_factor=0.5` — the pause between attempts grows (0.5 s, 1 s, 2 s...), `status_forcelist` — which codes count as temporary. Now `s.get()` will re-ask the server on 502-style errors all by itself.

## Proxies: leaving through another door

A proxy is an intermediate server through which your request travels. From the site's point of view, traffic comes from the proxy's IP, not yours. This is used for spreading load, bypassing IP-based blocks, and testing geo-availability:

```python
proxies = {
    "http": "http://user:pass@127.0.0.1:8080",
    "https": "http://user:pass@127.0.0.1:8080",
}
r = requests.get("https://httpbin.org/ip", proxies=proxies, timeout=10)
print(r.json())
```

A proxy is given as a dictionary: separately for `http` and `https`. Keep in mind: a proxy does not make you anonymous "by magic" — over HTTPS the site still sees the final address, and the data in the channel is encrypted.

## Summary

A battle-ready HTTP client for scraping looks like this: `Session()` for cookies, meaningful headers, `timeout` on every request, `HTTPAdapter` with `Retry` for temporary failures, and `proxies` for changing your IP. Remember these four pillars — they'll be in every scraper you write. Let's solidify the skills on real services.

<!--TASK-->
### Task 1

Write a program `session_cookies.py`. Create a `requests.Session()`, make a GET request to `https://httpbin.org/cookies/set?name=anya&role=student`, then a GET to `https://httpbin.org/cookies`. Print the status code of the second request and the contents of the `json` field of the response — the server should return both cookies. Then create a second, new session, repeat the request to `https://httpbin.org/cookies` inside it and print the result. Old cookies must not get into the new session. Explain in a comment why the results differ.

### Task 2

Write a function `make_headers()` that returns a dictionary with headers: `User-Agent` — any realistic string, for example `"MyCourseScraper/1.0 (student@example.com)"`, `Accept` — `"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"`, `Accept-Language` — `"en-US,en;q=0.9"`. Send a GET request to `https://httpbin.org/headers` with these headers and `timeout=10`. Print three values from the response: `accept`, `accept-language`, and `user-agent` — exactly as the server saw them. This will show that your headers really reach the server.

### Task 3

Create a session with retries: `Retry(total=2, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])` and `HTTPAdapter(max_retries=retry)`, mount the adapter to `https://`. Send a GET to `https://httpbin.org/status/503` inside a `try/except` — catch the exception (for example `requests.exceptions.ConnectionError`), print its type and the error message. Then, with the same adapter, fetch `https://httpbin.org/get` and print `status_code`. Explain in a comment why such retries are useful in practice and why `503` is a temporary error.

### Task 4

Send a GET request to `https://httpbin.org/delay/5` (the server will respond after 5 seconds) with `timeout=2`. The program should catch `requests.Timeout` and print the phrase `Timeout: the server did not respond within 2 s`. Then repeat the request with `timeout=10` and print `status_code` — this time the response should make it. Hint: `httpbin.org/delay/N` deliberately delays the response by N seconds — it's a perfect testing ground for timeouts.

### Task 5

Write a function `fetch_page(url, session=None, timeout=15)` that returns a tuple of three values: the status code, the `Content-Type` from the response headers, and the length of the response text (`len(r.text)`). Inside the function, create a session if none was passed, and fill in the default headers: `User-Agent` and `Accept-Language`. Call the function for `https://quotes.toscrape.com/page/1/` and for `https://books.toscrape.com/`. For each address print a line like `URL -> status, type, length`. First, take a look at what sites these addresses are — they are popular training playgrounds for scraping.
<!--/TASK-->

<!--HINT-->
### Hint 1

A `Session` object stores cookies between requests within the same session. After `s.get("https://httpbin.org/cookies/set?name=anya&role=student")` the `name` and `role` cookies settle in the session. The `/cookies` response's `json` field contains a `cookies` dictionary. A new session knows nothing about the first one's cookies — so its response will be `{"cookies": {}}`.

### Hint 2

Headers are passed as the `headers=` argument to `requests.get()`. The httpbin server returns a `headers` field in the response — a dictionary with all the headers it received. Take values by the keys `accept`, `accept-language`, `user-agent`. Note: in the response the keys are lowercase, even if you sent them differently.

### Hint 3

`Retry` from `urllib3` controls retries. `status_forcelist` — the codes that should trigger a retry. When attempts run out, `requests` raises `ConnectionError` (internally — `MaxRetryError`). Catch the general `requests.RequestException` to cover both timeouts and connection failures.

### Hint 4

`timeout` is the limit for waiting for a response. `httpbin.org/delay/5` responds after 5 seconds, so `timeout=2` won't make it and will raise `requests.Timeout`. Catch exactly `requests.Timeout` (or the general `requests.RequestException`). With `timeout=10` the response makes it, and you'll see `200`.

### Hint 5

The function should accept a URL and optionally a session. If `session` is `None`, create a `requests.Session()`. Default headers are convenient to set via `session.headers.update({...})` — then they apply to any request of that session. Return `(r.status_code, r.headers.get("Content-Type"), len(r.text))`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1

```python
import requests

# First session: get cookies
s1 = requests.Session()
s1.get("https://httpbin.org/cookies/set?name=anya&role=student")

r = s1.get("https://httpbin.org/cookies")
print("Status:", r.status_code)
print("Cookies in session 1:", r.json()["cookies"])

# Second, new session
s2 = requests.Session()
r2 = s2.get("https://httpbin.org/cookies")
print("Cookies in session 2:", r2.json()["cookies"])
```

Step-by-step breakdown:

- `requests.Session()` creates a container in which `requests` automatically saves cookies from every response and attaches them to subsequent requests.
- The address `/cookies/set?name=anya&role=student` is a special httpbin endpoint: it "issues" the cookies listed in the query parameters and redirects. The cookies settle in the session.
- `s1.get("https://httpbin.org/cookies")` returns JSON in which the `cookies` field is a dictionary with the session's cookies. We'll see `{'name': 'anya', 'role': 'student'}`.
- `s2` is a completely new session. It has no cookies, so the response will be `{'cookies': {}}`. This clearly shows why a session is needed: without it, every `requests.get()` would be just as "empty" a visit as `s2`'s, and login wouldn't work.
- The comment in the task should explain exactly this: cookies live inside a session and are not shared between different sessions.

### Solution 2

```python
import requests

def make_headers():
    return {
        "User-Agent": "MyCourseScraper/1.0 (student@example.com)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

r = requests.get("https://httpbin.org/headers", headers=make_headers(), timeout=10)
headers_seen = r.json()["headers"]
print("accept:", headers_seen["Accept"])
print("accept-language:", headers_seen["Accept-Language"])
print("user-agent:", headers_seen["User-Agent"])
```

Step-by-step breakdown:

- The `make_headers()` function returns a dictionary — a single place where headers are defined. It's convenient to reuse in all of the scraper's requests.
- `headers=make_headers()` passes them to the request; `timeout=10` guards against hanging.
- `httpbin.org/headers` replies with JSON whose `headers` field is exactly the set of headers the server actually received. By comparing them with what you sent, you can see nothing was lost or distorted.
- Note: in the response the keys are capitalized (`Accept`, `User-Agent`), just as you wrote them in the dictionary. If you passed `accept` in a different case, the server would still see `Accept`, because HTTP headers are case-insensitive — but for cleanliness it's better to write the canonical form right away.
- This "echo" trick with headers is a great way to debug your client before working with a real site.

### Solution 3

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests

s = requests.Session()
retry = Retry(total=2, backoff_factor=0.5,
              status_forcelist=[500, 502, 503, 504])
s.mount("https://", HTTPAdapter(max_retries=retry))

try:
    r = s.get("https://httpbin.org/status/503", timeout=10)
    print(r.status_code)
except requests.RequestException as e:
    print("Exception type:", type(e).__name__)
    print("Message:", e)
```

Step-by-step breakdown:

- `Retry(total=2, ...)` says: make up to three attempts in total (the first plus two retries). `backoff_factor=0.5` sets a growing pause: 0.5 s, then 1 s. This way the client doesn't hammer the server without pauses.
- `status_forcelist=[500, 502, 503, 504]` — these are the "server is temporarily unwell" codes. On `503`, urllib3 retries the request itself, without our code.
- But `httpbin.org/status/503` always answers 503, so after three attempts the retries run out and `requests` raises `ConnectionError` (inside it — `MaxRetryError` with a helpful message).
- We catch the general `requests.RequestException` — the parent class for all `requests` errors, including timeouts and connection problems. This is more robust than catching a specific type.
- Code `503` is a temporary error: the server is alive but overloaded. That's why retries are appropriate here. But retrying on 404 or 403 is pointless — the resource is not found or access is permanently denied. That's why only 5xx codes are included in `Retry`.

### Solution 4

```python
import requests

try:
    r = requests.get("https://httpbin.org/delay/5", timeout=2)
    print(r.status_code)
except requests.Timeout:
    print("Timeout: the server did not respond within 2 s")

r = requests.get("https://httpbin.org/delay/5", timeout=10)
print(r.status_code)
```

Step-by-step breakdown:

- `httpbin.org/delay/5` is a training endpoint that deliberately waits 5 seconds before responding.
- `timeout=2` is less than that delay, so after 2 seconds `requests` interrupts the wait and raises `requests.Timeout`.
- The `except requests.Timeout` block catches exactly this case and prints a clear message. A good scraper, in place of `print`, would decide: skip the page, wait and retry, or log the error.
- The second request with `timeout=10` manages to wait for the response, and we see `200`.
- Remember: timeout is a mandatory parameter in any scraper. Without it, one hung page would stop the whole data collection forever.

### Solution 5

```python
import requests

def fetch_page(url, session=None, timeout=15):
    if session is None:
        session = requests.Session()
        session.headers.update({
            "User-Agent": "MyCourseScraper/1.0 (student@example.com)",
            "Accept-Language": "en-US,en;q=0.9",
        })
    r = session.get(url, timeout=timeout)
    return r.status_code, r.headers.get("Content-Type"), len(r.text)

for url in (
    "https://quotes.toscrape.com/page/1/",
    "https://books.toscrape.com/",
):
    status, ctype, length = fetch_page(url)
    print(f"{url} -> {status}, {ctype}, {length}")
```

Step-by-step breakdown:

- The `fetch_page()` function encapsulates the whole request "ritual": creating a session, headers, timeout. The scraper just calls it and gets data.
- If `session` is not passed, a new session is created and default headers are put into `session.headers`. They will now be on every request of this session — no need to pass `headers=` each time.
- A tuple `(status_code, content_type, length)` is returned. `r.headers.get("Content-Type")` gets the content type (e.g. `text/html; charset=utf-8`), `len(r.text)` — the size of the response text in characters.
- Both sites are training playgrounds for scraping: `quotes.toscrape.com` (quotes) and `books.toscrape.com` (books). They serve plain HTML, so `Content-Type` will be `text/html`, and the length — several tens of thousands of characters.
- Such a wrapper is the first step toward a collection pipeline: it separates the "network" part from the data extraction logic, which you'll tackle in the next lessons.
<!--/SOLUTION-->

<!--QUIZ-->
What does requests.Session() do as opposed to a single requests.get()?
- Sends requests faster
- Keeps cookies and other settings between requests
- Encrypts all requests
- Always uses a proxy
* Correct answer: Keeps cookies and other settings between requests
A session is a container: cookies, headers, and adapters live in it between requests.

Why should a scraper send the User-Agent header?
- So the server knows who the client is and can serve suitable content
- To make the request anonymous
- To speed up the network
- It's not needed, it's just decoration
* Correct answer: So the server knows who the client is and can serve suitable content
Many sites block an empty or suspicious User-Agent, or serve scripts a trimmed version of the page.

What happens if you don't specify timeout in requests.get()?
- The request will wait for a response forever
- The request will immediately fail with an error
- timeout will be set automatically to 1 second
- The server will break the connection itself
* Correct answer: The request will wait for a response forever
Without timeout, a scraper can hang forever if the server stays silent.

Which HTTP codes make sense to include in status_forcelist for retries?
- 200, 301, 302
- 500, 502, 503, 504
- 401, 403, 404
- 100, 102, 103
* Correct answer: 500, 502, 503, 504
These are "server is temporarily unwell" errors — a repeated request may succeed. Retrying 404 or 403 is pointless.

What are proxies used for in scraping?
- To speed up page loading
- To replace HTML with JSON
- To change the outgoing IP address and spread load
- To log in to a site automatically
* Correct answer: To change the outgoing IP address and spread load
A proxy is an intermediate server: the site sees its IP. This helps bypass IP-based blocks and avoids loading a single address.

Why are cookies from one session not visible in another?
- Because sessions are created with different protocols
- Because each session stores its own cookies independently
- Because cookies are blocked by encryption
- They are visible, the question is wrong
* Correct answer: Because each session stores its own cookies independently
Cookies live inside their own session container and are not shared between different sessions.

What does Retry from urllib3 do together with HTTPAdapter?
- Repeats the request on temporary errors with a growing pause
- Encrypts the connection between client and server
- Changes the IP address of outgoing requests
- Compresses transmitted responses
* Correct answer: Repeats the request on temporary errors with a growing pause
Retry(total=3) makes up to three attempts, backoff_factor sets a growing pause, and status_forcelist lists the codes treated as temporary.

How do you pass a proxy to requests?
- A proxies dictionary with separate keys for the http and https schemes
- The string proxies="http://user:pass@host:port"
- Through the Proxy-Header header
- The proxy_url=... parameter
* Correct answer: A proxies dictionary with separate keys for the http and https schemes
The address format is scheme://login:password@host:port, and the dictionary itself is passed as proxies=proxies.
<!--/QUIZ-->
