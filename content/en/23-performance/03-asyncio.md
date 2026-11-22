---
title: asyncio in practice
summary: Coroutines, gather, real async.
order: 3
duration: 50 min
difficulty: advanced
tags: asyncio
---

asyncio handles many I/O tasks at once.

## Basic

```python
import asyncio

async def fetch(url):
    await asyncio.sleep(0.1)
    return f"data from {url}"

async def main():
    tasks = [fetch(f"u{i}") for i in range(5)]
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())
```

## Real I/O

Use async libraries (aiohttp) for network.

## Lesson summary

await + gather parallelize I/O.

<!--TASK-->
### Task 1 — Coroutine
Write an async function.

### Task 2 — Run
Run with asyncio.run.

### Task 3 — Gather
Run several concurrently.

### Task 4 — Time
Compare sync vs async timing.

### Task 5 — aiohttp
Fetch URLs with aiohttp.

### Task 6 — GIL
Why not for CPU?

### Task 7 — Timeout
Add a timeout.
<!--/TASK-->

<!--HINT-->
### Hint 1
async def.

### Hint 2
asyncio.run.

### Hint 3
gather.

### Hint 4
perf_counter.

### Hint 5
aiohttp.

### Hint 6
I/O.

### Hint 7
wait_for.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import asyncio

async def hello():
    await asyncio.sleep(1)
    return "hi"
```

### Solution 2
```python
asyncio.run(hello())
```

### Solution 3
```python
async def main():
    results = await asyncio.gather(
        hello(), hello(), hello()
    )
    print(results)
```

### Solution 4
```python
import time
# sync: 3 × sleep(1) → ~3 с
# async: gather(hello×3) → ~1 с
```

### Solution 5
```python
import aiohttp

async def fetch(session, url):
    async with session.get(url) as resp:
        return await resp.text()

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, "https://example.com") for _ in range(3)]
        pages = await asyncio.gather(*tasks)
```

### Solution 6
```python
# asyncio конкурентен для I/O;
# CPU-задачи занимают GIL — используют
# multiprocessing или отдельные потоки
```

### Solution 7
```python
async def main():
    try:
        result = await asyncio.wait_for(hello(), timeout=2)
    except asyncio.TimeoutError:
        print("timeout")
```
<!--/SOLUTION-->

<!--QUIZ-->
What is asyncio?
- Async I/O library
- Threads
- Multiprocessing
- None
* Correct answer: Async I/O library
Event loop.

What is async def?
- Coroutine
- Function
- Generator
- None
* Correct answer: Coroutine
Awaitable.

What is await?
- Yields control
- Blocks
- Ends
- None
* Correct answer: Yields control
Pause.

What is gather?
- Runs together
- One by one
- Stops
- None
* Correct answer: Runs together
Concurrent.

What is run?
- Starts loop
- Stops
- Awaits
- None
* Correct answer: Starts loop
Entry.

What is an event loop?
- Scheduler
- Thread
- CPU
- None
* Correct answer: Scheduler
Turns.

What is aiohttp?
- Async HTTP
- Sync requests
- Database
- None
* Correct answer: Async HTTP
Client.

What is I/O bound?
- Waiting on I/O
- CPU heavy
- Memory
- None
* Correct answer: Waiting on I/O
Async fits.

What is CPU bound?
- Heavy compute
- I/O
- Wait
- None
* Correct answer: Heavy compute
Processes.

What is wait_for?
- Timeout
- Loop
- Gather
- None
* Correct answer: Timeout
Limit.

What is TimeoutError?
- Raised on wait
- Normal
- Warning
- None
* Correct answer: Raised on wait
Catch.

What is the benefit?
- Fewer threads
- Faster CPU
- Simpler
- None
* Correct answer: Fewer threads
Scale.
<!--/QUIZ-->
