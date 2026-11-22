---
title: HTTP and requests library
summary: GET/POST, headers, status codes.
order: 1
duration: 40 min
difficulty: intermediate
tags: http, requests
---

HTTP is how clients talk to servers.

## GET

```python
import requests
resp = requests.get("https://httpbin.org/get")
print(resp.status_code)   # 200
print(resp.json())
```

## POST

```python
resp = requests.post("https://httpbin.org/post", json={"key": "value"})
```

## Headers

```python
resp = requests.get(url, headers={"User-Agent": "MyApp/1.0"})
```

## Status codes

200 OK, 404 not found, 500 server error.

## Lesson summary

requests wraps HTTP; check status codes.

<!--TASK-->
### Task 1 — GET
Fetch a page.

### Task 2 — Status
Print and check status code.

### Task 3 — JSON
Parse JSON response.

### Task 4 — POST
Send data.

### Task 5 — Headers
Add a User-Agent.

### Task 6 — Timeout
Set a timeout.

### Task 7 — Errors
Handle network errors.
<!--/TASK-->

<!--HINT-->
### Hint 1
requests.get.

### Hint 2
status_code.

### Hint 3
resp.json().

### Hint 4
json=.

### Hint 5
headers=.

### Hint 6
timeout=.

### Hint 7
try/except.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import requests
resp = requests.get("https://httpbin.org/get")
```

### Solution 2
```python
print(resp.status_code)
if resp.status_code == 200:
    print("OK")
```

### Solution 3
```python
data = resp.json()
print(data["url"])
```

### Solution 4
```python
resp = requests.post("https://httpbin.org/post", json={"key": "value"})
```

### Solution 5
```python
resp = requests.get(url, headers={"User-Agent": "MyApp/1.0"})
```

### Solution 6
```python
resp = requests.get(url, timeout=10)
```

### Solution 7
```python
try:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
except requests.RequestException as e:
    print("request failed:", e)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is HTTP?
- Protocol
- A library
- A server
- None
* Correct answer: Protocol
Web.

What is GET?
- Fetch data
- Send data
- Delete
- None
* Correct answer: Fetch data
Read.

What is POST?
- Submit data
- Fetch
- Delete
- None
* Correct answer: Submit data
Create.

What is status_code?
- Response code
- Header
- Body
- None
* Correct answer: Response code
200/404.

What is 200?
- OK
- Error
- Redirect
- None
* Correct answer: OK
Success.

What is 404?
- Not found
- OK
- Error
- None
* Correct answer: Not found
Missing.

What is 500?
- Server error
- OK
- Not found
- None
* Correct answer: Server error
Broken.

What is resp.json()?
- Parses JSON
- Text
- Headers
- None
* Correct answer: Parses JSON
Dict.

What is a header?
- Metadata
- Body
- Status
- None
* Correct answer: Metadata
User-Agent.

What is timeout?
- Wait limit
- Retry
- Header
- None
* Correct answer: Wait limit
Seconds.

What is raise_for_status?
- Raises on error
- Returns
- Ignores
- None
* Correct answer: Raises on error
Check.

What is RequestException?
- Network error
- Response
- Status
- None
* Correct answer: Network error
Catch.
<!--/QUIZ-->
