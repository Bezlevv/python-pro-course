---
title: How the web works and HTTP
summary: Requests, responses, methods, status codes, URLs.
order: 1
duration: 35 min
difficulty: intermediate
tags: http, web, requests, status
---

The web is a client-server exchange over HTTP.

## Request — response

Browser sends a request; server returns a response with a status code.

## Methods

GET (read), POST (create), PUT (update), DELETE (remove), PATCH (partial).

## Status codes

- 2xx success (200 OK, 201 Created);
- 3xx redirects;
- 4xx client errors (404 Not Found, 401 Unauthorized);
- 5xx server errors.

## URL structure

`https://site.com/path?query=1#fragment` → protocol, host, path, query, fragment.

## Headers

Metadata: Content-Type, User-Agent, Authorization.

## Lesson summary

HTTP: methods, statuses, URLs, headers; everything else in web dev builds on this.

<!--TASK-->
### Task 1 — Methods
List HTTP methods and their purposes in comments.

### Task 2 — Statuses
Match codes: 200, 404, 500, 302 with descriptions.

### Task 3 — URL parts
Parse a URL and identify protocol, host, path, query.

### Task 4 — Python request
Use urllib to GET httpbin.org/get and print the status.

### Task 5 — Headers
Send a custom User-Agent header with requests.

### Task 6 — JSON endpoint
GET https://httpbin.org/json and print a field.

### Task 7 — Error handling
Handle HTTPError for a 404 URL gracefully.
<!--/TASK-->

<!--HINT-->
### Hint 1
GET/POST/PUT/DELETE/PATCH.

### Hint 2
200 OK, 404 not found, 500 server error, 302 redirect.

### Hint 3
urllib.parse.urlsplit.

### Hint 4
urlopen(url).status.

### Hint 5
requests.get(url, headers={...}).

### Hint 6
resp.json()["slideshow"]["title"].

### Hint 7
except HTTPError.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
# GET — read
# POST — create
# PUT — full update
# PATCH — partial update
# DELETE — remove
```

### Solution 2
```python
codes = {200: "OK", 404: "Not Found", 500: "Server Error", 302: "Found"}
```

### Solution 3
```python
from urllib.parse import urlsplit
u = urlsplit("https://site.com/path?a=1#frag")
print(u.scheme, u.netloc, u.path, u.query)
```

### Solution 4
```python
from urllib.request import urlopen
print(urlopen("https://httpbin.org/get", timeout=10).status)   # 200
```

### Solution 5
```python
import requests
r = requests.get("https://httpbin.org/get", headers={"User-Agent": "my-app"}, timeout=10)
print(r.status_code)
```

### Solution 6
```python
r = requests.get("https://httpbin.org/json", timeout=10)
print(r.json()["slideshow"]["title"])
```

### Solution 7
```python
from urllib.error import HTTPError
try:
    urlopen("https://httpbin.org/status/404", timeout=10)
except HTTPError as e:
    print(e.code)   # 404
```
<!--/SOLUTION-->

<!--QUIZ-->
What is HTTP?
- Protocol for web exchange
- A language
- A browser
- A server
* Correct answer: Protocol for web exchange
Foundation.

Which method reads data?
- GET
- POST
- DELETE
- PATCH
* Correct answer: GET
Safe.

Which creates resources?
- POST
- GET
- HEAD
- OPTIONS
* Correct answer: POST
Create.

What does 404 mean?
- Not Found
- OK
- Error
- Redirect
* Correct answer: Not Found
Missing resource.

What does 200 mean?
- OK
- Not Found
- Created
- Error
* Correct answer: OK
Success.

What does 500 mean?
- Server error
- Client error
- OK
- Redirect
* Correct answer: Server error
Internal.

What is a URL?
- Uniform Resource Locator
- A file
- A code
- A header
* Correct answer: Uniform Resource Locator
Address.

What are headers?
- Metadata
- Body
- Status
- Query
* Correct answer: Metadata
Context.

What is a client?
- Browser/application
- Server
- Database
- Router
* Correct answer: Browser/application
Requester.

What is a server?
- Responds to requests
- Sends queries
- Stores only
- Routes
* Correct answer: Responds to requests
Host.

What is a query string?
- ?key=value
- /path
- #fragment
- Host
* Correct answer: ?key=value
Parameters.

What is Content-Type?
- Header describing body format
- Status
- Method
- URL
* Correct answer: Header describing body format
e.g., application/json.
<!--/QUIZ-->
