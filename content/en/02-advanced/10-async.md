---
title: Async: asyncio, async/await
summary: Event loop, coroutines, tasks, gather, async generators and asyncio.sleep.
order: 10
duration: 50 min
difficulty: intermediate
tags: asyncio, async, await, coroutine, task
---

asyncio runs concurrent code with a single thread using cooperative multitasking.

## Coroutines

```python
import asyncio

async def main():
    print("Start")
    await asyncio.sleep(1)
    print("End")

asyncio.run(main())
```

## Tasks

```python
async def main():
    task = asyncio.create_task(worker())
    await task
```

Create tasks to run coroutines concurrently.

## gather

```python
await asyncio.gather(worker(1), worker(2), worker(3))
```

gather waits for all and returns results.

## async generators

```python
async def gen():
    for i in range(3):
        await asyncio.sleep(0.1)
        yield i
```

## Lesson summary

Async code uses an event loop, coroutines (async def), await, and tools like tasks and gather.

<!--TASK-->
### Task 1 — First coroutine
Write async def hello() that prints "Hello", sleeps 0.5s, prints "World"; run with asyncio.run.

### Task 2 — Two coroutines
Write two coroutines and run them sequentially with two awaits; measure time.

### Task 3 — Tasks
Create two tasks and run them concurrently; show the total time.

### Task 4 — gather
Use asyncio.gather on three coroutines and collect return values.

### Task 5 — Asyncio sleep
Compare time.sleep vs asyncio.sleep in async code; use perf_counter.

### Task 6 — Async generator
Write an async generator yielding 1..3 with small delays; collect with async for.

### Task 7 — Timeout
Use asyncio.wait_for with timeout=1 on a 3-second sleep and catch TimeoutError.
<!--/TASK-->

<!--HINT-->
### Hint 1
asyncio.run(main()).

### Hint 2
await first(); await second() — sequential.

### Hint 3
task = asyncio.create_task(coro()); await task.

### Hint 4
results = await asyncio.gather(a(), b(), c()).

### Hint 5
time.sleep blocks; asyncio.sleep frees the loop.

### Hint 6
async for x in gen(): print(x).

### Hint 7
try: await asyncio.wait_for(long(), timeout=1) except asyncio.TimeoutError.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import asyncio

async def hello():
    print("Hello")
    await asyncio.sleep(0.5)
    print("World")

asyncio.run(hello())
```

### Solution 2
```python
async def job(name):
    await asyncio.sleep(1)
    return name

async def main():
    r1 = await job("A")
    r2 = await job("B")
    print(r1, r2)   # ~2s

asyncio.run(main())
```

### Solution 3
```python
async def main():
    t1 = asyncio.create_task(job("A"))
    t2 = asyncio.create_task(job("B"))
    await t1
    await t2
    # ~1s total
```

### Solution 4
```python
async def main():
    results = await asyncio.gather(job("A"), job("B"), job("C"))
    print(results)

asyncio.run(main())
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
async def gen():
    for i in range(1, 4):
        await asyncio.sleep(0.1)
        yield i

async def main():
    async for x in gen():
        print(x)

asyncio.run(main())
```

### Solution 7
```python
async def long():
    await asyncio.sleep(3)

async def main():
    try:
        await asyncio.wait_for(long(), timeout=1)
    except asyncio.TimeoutError:
        print("Timeout")

asyncio.run(main())
```
<!--/SOLUTION-->

<!--QUIZ-->
What is asyncio.run()?
- Runs a coroutine in an event loop
- Runs threads
- Imports
- Prints
* Correct answer: Runs a coroutine in an event loop
Entry point.

What is a coroutine?
- A function defined with async def
- A thread
- A process
- A generator only
* Correct answer: A function defined with async def
Can await.

What does await do?
- Yields control to the event loop
- Sleeps forever
- Returns
- Errors
* Correct answer: Yields control to the event loop
Pauses until result ready.

What is a task?
- A scheduled coroutine
- A thread
- A process
- A function
* Correct answer: A scheduled coroutine
Runs concurrently.

What does gather do?
- Waits for multiple coroutines
- Runs sequentially
- Stops
- Sorts
* Correct answer: Waits for multiple coroutines
Returns results.

Does asyncio.sleep block the loop?
- No
- Yes
- Sometimes
- Only with tasks
* Correct answer: No
Other coroutines run.

Why use tasks?
- Concurrency
- Simplicity
- Type safety
- Memory
* Correct answer: Concurrency
Multiple coroutines interleave.

What is asyncio.wait_for?
- Limits waiting time
- Waits forever
- Runs in threads
- Sleeps
* Correct answer: Limits waiting time
Timeout raises TimeoutError.

Can async loops use async for?
- Yes
- No
- Only in threads
- Only with gather
* Correct answer: Yes
For async generators.

What happens on timeout?
- TimeoutError is raised
- Program exits
- Nothing
- Retry
* Correct answer: TimeoutError is raised
Catch it.

Is async faster than threads for I/O?
- Usually, with lighter overhead
- Always faster CPU
- Never
- Equal
* Correct answer: Usually, with lighter overhead
For many concurrent I/O operations.

Which is blocking?
- time.sleep
- asyncio.sleep
- await gather
- create_task
* Correct answer: time.sleep
Blocks the whole thread.
<!--/QUIZ-->
