---
title: Thread/process pools and Queue
summary: ThreadPoolExecutor, ProcessPoolExecutor, queue.Queue.
order: 4
duration: 40 min
difficulty: advanced
tags: pools, queue, futures
---

Pools manage worker threads/processes; Queue coordinates producers-consumers.

## ThreadPoolExecutor

```python
from concurrent.futures import ThreadPoolExecutor

def work(x):
    return x * x

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(work, range(10)))
print(results)
```

## ProcessPoolExecutor

```python
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(work, range(10)))
```

## queue.Queue

```python
import queue
q = queue.Queue()
q.put(1)
q.get()
```

## Lesson summary

Pools simplify parallelism; Queue is thread-safe.

<!--TASK-->
### Task 1 — Thread pool
Map a function over 10 inputs with ThreadPoolExecutor.

### Task 2 — Process pool
Do it with ProcessPoolExecutor.

### Task 3 — Number of workers
Set max_workers=3 and explain.

### Task 4 — Queue basics
Put/get values in queue.Queue.

### Task 5 — Producer/consumer
Two threads produce; one consumes.

### Task 6 — Futures
Use pool.submit and result().

### Task 7 — Choose
Decide thread vs process pool for images resize.
<!--/TASK-->

<!--HINT-->
### Hint 1
pool.map.

### Hint 2
ProcessPoolExecutor.

### Hint 3
max_workers.

### Hint 4
put/get.

### Hint 5
Threads + queue.

### Hint 6
future.result().

### Hint 7
Threads (I/O).
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from concurrent.futures import ThreadPoolExecutor

def work(x):
    return x * x

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(work, range(10)))
print(results)
```

### Solution 2
```python
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(work, range(10)))
print(results)
```

### Solution 3
```python
# max_workers ограничивает число одновременно работающих воркеров
```

### Solution 4
```python
import queue
q = queue.Queue()
q.put(1)
q.put(2)
print(q.get(), q.get())
```

### Solution 5
```python
import threading
import queue

q = queue.Queue()

def producer(start):
    for i in range(start, start + 5):
        q.put(i)

def consumer():
    while not q.empty():
        print(q.get())

t1 = threading.Thread(target=producer, args=(0,))
t2 = threading.Thread(target=producer, args=(10,))
c = threading.Thread(target=consumer)
t1.start(); t2.start(); c.start()
t1.join(); t2.join(); c.join()
```

### Solution 6
```python
with ThreadPoolExecutor(max_workers=2) as pool:
    f1 = pool.submit(work, 5)
    f2 = pool.submit(work, 7)
    print(f1.result(), f2.result())
```

### Solution 7
```python
# Ресайз изображений — CPU-задача: процессы
# Скачивание — I/O: потоки
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a pool?
- Managed workers
- A queue
- A lock
- None
* Correct answer: Managed workers
Reuse.

What is map in pool?
- Applies function to inputs
- A dict
- A queue
- None
* Correct answer: Applies function to inputs
Ordered.

What is max_workers?
- Worker count
- Inputs
- Outputs
- None
* Correct answer: Worker count
Concurrency.

What is submit?
- Schedules one call
- Maps
- Deletes
- None
* Correct answer: Schedules one call
Future.

What is Future?
- Result placeholder
- A thread
- A queue
- None
* Correct answer: Result placeholder
.result().

What is queue.Queue?
- Thread-safe queue
- Thread
- Lock
- None
* Correct answer: Thread-safe queue
Exchange.

What is put?
- Adds an item
- Gets
- Deletes
- None
* Correct answer: Adds an item
Producer.

What is get?
- Takes an item
- Adds
- Prints
- None
* Correct answer: Takes an item
Consumer.

Is Queue safe across threads?
- Yes
- No
- Sometimes
- Never
* Correct answer: Yes
Built-in locks.

When use process pool?
- CPU-bound
- I/O-bound
- Both
- Neither
* Correct answer: CPU-bound
Bypass GIL.

When use thread pool?
- I/O-bound
- CPU-bound
- Both
- Neither
* Correct answer: I/O-bound
Light.

What does with pool do?
- Closes after block
- Starts
- Pauses
- None
* Correct answer: Closes after block
Cleanup.
<!--/QUIZ-->
