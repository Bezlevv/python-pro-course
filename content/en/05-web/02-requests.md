---
title: HTTP client requests
summary: GET/POST, params, headers, JSON, sessions, timeouts, errors.
order: 2
duration: 40 min
difficulty: intermediate
tags: requests, http, api
---

`requests` is the friendly HTTP client.

## GET

```python
import requests

r = requests.get("https://httpbin.org/get", timeout=10)
print(r.status_code, r.text[:100])
```

## Params

```python
r = requests.get("https://httpbin.org/get", params={"q": "python"}, timeout=10)
```

## Headers and JSON

```python
r = requests.get("https://api.github.com/users/python", headers={"User-Agent": "app"}, timeout=10)
data = r.json()
print(data["login"])
```

## POST

```python
r = requests.post("https://httpbin.org/post", json={"name": "Anna"}, timeout=10)
```

## Sessions

```python
s = requests.Session()
s.headers.update({"Authorization": "Bearer x"})
r = s.get("https://httpbin.org/get", timeout=10)
```

## Errors

```python
try:
    r = requests.get("https://httpbin.org/status/404", timeout=10)
    r.raise_for_status()
except requests.HTTPError as e:
    print(e)
```

## Lesson summary

requests: params, headers, JSON, sessions, timeouts, clean errors.

<!--TASK-->
### Task 1 — GET
GET httpbin.org/get and print status + first 100 chars.

### Task 2 — Params
Pass params and verify they appear in the response JSON.

### Task 3 — Headers
Send User-Agent and read it back from the response.

### Task 4 — JSON
GET the GitHub user endpoint and print login and followers.

### Task 5 — POST
POST JSON to httpbin.org/post and print the sent data.

### Task 6 — Session
Create a session with a header; make two requests.

### Task 7 — Error handling
Use raise_for_status on a 404 and catch HTTPError.
<!--/TASK-->

<!--HINT-->
### Hint 1
requests.get(url, timeout=10).

### Hint 2
params={"q": "python"}.

### Hint 3
headers={"User-Agent": "app"}.

### Hint 4
r.json()["login"].

### Hint 5
json={"name": "Anna"}.

### Hint 6
requests.Session(); s.headers.update.

### Hint 7
r.raise_for_status().
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import requests
r = requests.get("https://httpbin.org/get", timeout=10)
print(r.status_code)
print(r.text[:100])
```

### Solution 2
```python
r = requests.get("https://httpbin.org/get", params={"q": "python"}, timeout=10)
print(r.json()["args"])
```

### Solution 3
```python
r = requests.get("https://httpbin.org/get", headers={"User-Agent": "my-app"}, timeout=10)
print(r.json()["headers"]["User-Agent"])
```

### Solution 4
```python
r = requests.get("https://api.github.com/users/python", headers={"User-Agent": "app"}, timeout=10)
d = r.json()
print(d["login"], d["followers"])
```

### Solution 5
```python
r = requests.post("https://httpbin.org/post", json={"name": "Anna"}, timeout=10)
print(r.json()["json"])
```

### Solution 6
```python
s = requests.Session()
s.headers.update({"User-Agent": "my-app"})
r1 = s.get("https://httpbin.org/get", timeout=10)
r2 = s.get("https://httpbin.org/headers", timeout=10)
```

### Solution 7
```python
try:
    r = requests.get("https://httpbin.org/status/404", timeout=10)
    r.raise_for_status()
except requests.HTTPError as e:
    print("HTTP error:", e)
```
<!--/SOLUTION-->

<!--QUIZ-->
What returns requests.get?
- Response object
- JSON
- Dict
- None
* Correct answer: Response object
With .status_code.

What does params do?
- Adds query params
- Headers
- Body
- Cookies
* Correct answer: Adds query params
?key=value.

How to get JSON?
- r.json()
- r.text
- r.data
- r.body
* Correct answer: r.json()
Parsed.

How to send JSON in POST?
- json={...}
- data={...} only
- body
- payload
* Correct answer: json={...}
Auto serializes.

What is a Session?
- Reused connection/state
- A request
- A header
- A URL
* Correct answer: Reused connection/state
Efficient.

What does headers.update do?
- Adds headers to session
- Removes
- Reads
- Prints
* Correct answer: Adds headers to session
Default headers.

What does raise_for_status do?
- Raises for 4xx/5xx
- Always
- Never
- Returns
* Correct answer: Raises for 4xx/5xx
Error check.

What is timeout?
- Seconds to wait
- Retries
- Headers
- Limit size
* Correct answer: Seconds to wait
Avoid hangs.

What is r.status_code?
- HTTP status
- Text
- JSON
- Length
* Correct answer: HTTP status
Integer.

What is r.text?
- Response as text
- JSON
- Bytes
- Status
* Correct answer: Response as text
Raw body.

What is requests.HTTPError?
- Exception for bad status
- A type
- A module
- A code
* Correct answer: Exception for bad status
Via raise_for_status.

What is r.headers?
- Response headers
- Request
- Body
- JSON
* Correct answer: Response headers
Dict-like.
<!--/QUIZ-->
