---
title: httpx: modern HTTP client
summary: Sync/async requests, params, JSON, streaming, timeouts.
order: 19
duration: 45 min
difficulty: intermediate
tags: httpx, http, async
---

httpx is a modern client for sync and async HTTP.

## Sync

```python
import httpx

r = httpx.get("https://httpbin.org/get", timeout=10)
print(r.status_code, r.json())
```

## Params and headers

```python
r = httpx.get("https://httpbin.org/get", params={"q": "x"}, headers={"User-Agent": "app"}, timeout=10)
```

## Async

```python
import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as client:
        r = await client.get("https://httpbin.org/get", timeout=10)
        print(r.status_code)

asyncio.run(main())
```

## JSON POST

```python
r = httpx.post("https://httpbin.org/post", json={"name": "Anna"}, timeout=10)
```

## Lesson summary

httpx: sync + async, params, JSON, client sessions.

<!--TASK-->
### Task 1 — Sync GET
GET httpbin.org/get and print status.

### Task 2 — Params
Pass params and show them in the response.

### Task 3 — Headers
Send a custom header.

### Task 4 — Async
Write an async client request.

### Task 5 — POST JSON
Post JSON and echo it.

### Task 6 — Client reuse
Use an httpx.Client for two requests.

### Task 7 — Timeout
Set a timeout and explain its purpose.
<!--/TASK-->

<!--HINT-->
### Hint 1
httpx.get(url, timeout=10).

### Hint 2
params={"q": "x"}.

### Hint 3
headers={...}.

### Hint 4
AsyncClient + await.

### Hint 5
json={...}.

### Hint 6
Client() context.

### Hint 7
timeout=10.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import httpx
r = httpx.get("https://httpbin.org/get", timeout=10)
print(r.status_code)
```

### Solution 2
```python
r = httpx.get("https://httpbin.org/get", params={"q": "x"}, timeout=10)
print(r.json()["args"])
```

### Solution 3
```python
r = httpx.get("https://httpbin.org/get", headers={"User-Agent": "app"}, timeout=10)
print(r.json()["headers"]["User-Agent"])
```

### Solution 4
```python
import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as client:
        r = await client.get("https://httpbin.org/get", timeout=10)
        print(r.status_code)

asyncio.run(main())
```

### Solution 5
```python
r = httpx.post("https://httpbin.org/post", json={"name": "Anna"}, timeout=10)
print(r.json()["json"])
```

### Solution 6
```python
with httpx.Client() as client:
    r1 = client.get("https://httpbin.org/get", timeout=10)
    r2 = client.get("https://httpbin.org/headers", timeout=10)
```

### Solution 7
```python
# timeout защищает от зависаний:
r = httpx.get("https://httpbin.org/delay/10", timeout=3)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is httpx?
- Modern HTTP client
- ORM
- Framework
- Template
* Correct answer: Modern HTTP client
Sync/async.

What does httpx.get return?
- Response
- JSON
- None
- Dict
* Correct answer: Response
.status_code.

What is params?
- Query parameters
- Headers
- Body
- Cookies
* Correct answer: Query parameters
?q=.

How to do async?
- AsyncClient + await
- get only
- sync
- threads
* Correct answer: AsyncClient + await
Coroutines.

What is json= in post?
- JSON body
- Form
- File
- Query
* Correct answer: JSON body
Serialized.

What is a Client?
- Reused session
- One request
- Plugin
- URL
* Correct answer: Reused session
Connection pool.

What is timeout?
- Wait limit
- Retry
- Size
- Header
* Correct answer: Wait limit
Avoid hangs.

Does httpx support streaming?
- Yes
- No
- Only sync
- Never
* Correct answer: Yes
stream().

What is r.json()?
- Parsed JSON
- Text
- Bytes
- Status
* Correct answer: Parsed JSON
Method.

What is r.status_code?
- HTTP status
- Body
- URL
- Time
* Correct answer: HTTP status
Integer.

Can httpx be used in FastAPI tests?
- Yes, TestClient uses httpx
- No
- Only requests
- Only curl
* Correct answer: Yes, TestClient uses httpx
Under the hood.

What is async with?
- Context for async resources
- Loop
- List
- Error
* Correct answer: Context for async resources
Cleanup.
<!--/QUIZ-->
