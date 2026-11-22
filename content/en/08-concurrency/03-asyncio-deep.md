---
title: asyncio deeper: tasks, timeouts, aiohttp
summary: create_task, gather, wait_for, semaphore, aiohttp.
order: 3
duration: 50 min
difficulty: advanced
tags: asyncio, tasks, aiohttp
---

asyncio scales I/O concurrency with tasks and timeouts.

## Tasks

```python
import asyncio

async def worker(name):
    await asyncio.sleep(1)
    return name

async def main():
    t1 = asyncio.create_task(worker("A"))
    t2 = asyncio.create_task(worker("B"))
    print(await t1, await t2)

asyncio.run(main())
```

## gather

```python
results = await asyncio.gather(worker("A"), worker("B"), worker("C"))
```

## Timeout

```python
try:
    await asyncio.wait_for(worker("x"), timeout=1)
except asyncio.TimeoutError:
    print("timeout")
```

## Semaphore

```python
sem = asyncio.Semaphore(3)

async def limited(name):
    async with sem:
        await asyncio.sleep(1)
```

## aiohttp

```python
import aiohttp

async def fetch(session, url):
    async with session.get(url) as resp:
        return resp.status

async def main():
    async with aiohttp.ClientSession() as session:
        statuses = await asyncio.gather(
            fetch(session, "https://httpbin.org/get"),
            fetch(session, "https://httpbin.org/get"),
        )
    print(statuses)
```

## Lesson summary

Tasks + gather + timeouts + semaphore + aiohttp = efficient async I/O.

<!--TASK-->
### Task 1 — Task
Create two tasks and print their results.

### Task 2 — gather
Use gather and collect an ordered list.

### Task 3 — Timeout
Wrap a slow coroutine with wait_for.

### Task 4 — Semaphore
Limit concurrency to 2 with a semaphore.

### Task 5 — Sleep compare
Compare time.sleep vs asyncio.sleep in async.

### Task 6 — aiohttp
Fetch two URLs concurrently.

### Task 7 — Cancel
Explain task cancellation with cancel().
<!--/TASK-->

<!--HINT-->
### Hint 1
create_task + await.

### Hint 2
gather(*coros).

### Hint 3
wait_for(coro, timeout=1).

### Hint 4
async with sem.

### Hint 5
perf_counter.

### Hint 6
ClientSession.

### Hint 7
task.cancel().
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import asyncio

async def worker(name):
    await asyncio.sleep(1)
    return name

async def main():
    t1 = asyncio.create_task(worker("A"))
    t2 = asyncio.create_task(worker("B"))
    print(await t1, await t2)

asyncio.run(main())
```

### Solution 2
```python
async def main():
    results = await asyncio.gather(worker("A"), worker("B"))
    print(results)
```

### Solution 3
```python
async def slow():
    await asyncio.sleep(5)

async def main():
    try:
        await asyncio.wait_for(slow(), timeout=1)
    except asyncio.TimeoutError:
        print("timeout")
```

### Solution 4
```python
sem = asyncio.Semaphore(2)

async def limited(name):
    async with sem:
        await asyncio.sleep(1)
        print(name)
```

### Solution 5
```python
import time

async def main():
    start = time.perf_counter()
    await asyncio.sleep(1)
    print(time.perf_counter() - start)
```

### Solution 6
```python
import aiohttp

async def fetch(session, url):
    async with session.get(url) as resp:
        return resp.status

async def main():
    async with aiohttp.ClientSession() as session:
        statuses = await asyncio.gather(
            fetch(session, "https://httpbin.org/get"),
            fetch(session, "https://httpbin.org/get"),
        )
    print(statuses)
```

### Solution 7
```python
task = asyncio.create_task(slow())
task.cancel()
# asyncio.CancelledError внутри задачи
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a task?
- Scheduled coroutine
- A thread
- A process
- A function
* Correct answer: Scheduled coroutine
Concurrent.

What does create_task do?
- Schedules a coroutine
- Runs sync
- Deletes
- None
* Correct answer: Schedules a coroutine
Background.

What does gather do?
- Waits for all
- One
- Stops
- None
* Correct answer: Waits for all
Results.

What is wait_for?
- Timeout wrapper
- Always waits
- Cancels never
- None
* Correct answer: Timeout wrapper
Limit.

What is a semaphore?
- Concurrency limit
- A lock
- A task
- None
* Correct answer: Concurrency limit
N slots.

What is aiohttp?
- Async HTTP client
- Sync client
- ORM
- None
* Correct answer: Async HTTP client
I/O.

What does async with do?
- Async context
- Loop
- Error
- None
* Correct answer: Async context
Resource.

What is await?
- Yields control
- Blocks
- Sleeps
- None
* Correct answer: Yields control
Event loop.

What is CancelledError?
- Raised on cancel
- Timeout
- Error
- None
* Correct answer: Raised on cancel
Internal.

What is an event loop?
- Scheduler
- A thread
- A process
- None
* Correct answer: Scheduler
Runs tasks.

Is asyncio single-threaded?
- Yes
- No
- Both
- None
* Correct answer: Yes
Cooperative.

What fits asyncio?
- I/O-bound
- CPU-bound
- Both
- Neither
* Correct answer: I/O-bound
Waiting.
<!--/QUIZ-->
