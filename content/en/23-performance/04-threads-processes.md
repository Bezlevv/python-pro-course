---
title: Threads and multiprocessing
summary: When each fits, GIL.
order: 4
duration: 45 min
difficulty: advanced
tags: threads, multiprocessing
---

Parallelism has two main tools.

## Threads (I/O)

```python
import threading

def work(name):
    print("worker", name)

threads = [threading.Thread(target=work, args=(i,)) for i in range(3)]
for t in threads: t.start()
for t in threads: t.join()
```

## Processes (CPU)

```python
from multiprocessing import Pool

def square(x):
    return x * x

with Pool(4) as pool:
    print(pool.map(square, range(10)))
```

## GIL

Threads share GIL → CPU-bound is serialized; processes bypass it.

## Lesson summary

Threads for I/O, processes for CPU.

<!--TASK-->
### Task 1 — Thread
Start 3 threads.

### Task 2 — Join
Wait for them.

### Task 3 — Process
Use Pool.map.

### Task 4 — Compare
Thread vs process for CPU.

### Task 5 — Lock
Protect a shared counter.

### Task 6 — Queue
Pass results via Queue.

### Task 7 — Choose
Which for I/O?
<!--/TASK-->

<!--HINT-->
### Hint 1
Thread.

### Hint 2
join.

### Hint 3
Pool.

### Hint 4
GIL.

### Hint 5
Lock.

### Hint 6
Queue.

### Hint 7
Threads.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import threading

def work(name):
    print("worker", name)

threads = [threading.Thread(target=work, args=(i,)) for i in range(3)]
for t in threads:
    t.start()
```

### Solution 2
```python
for t in threads:
    t.join()
```

### Solution 3
```python
from multiprocessing import Pool

def square(x):
    return x * x

with Pool(4) as pool:
    print(pool.map(square, range(10)))
```

### Solution 4
```python
# CPU-задача: процессы ускоряют (нет GIL)
# потоки — почти нет
```

### Solution 5
```python
lock = threading.Lock()
counter = 0

def increment():
    global counter
    for _ in range(1000):
        with lock:
            counter += 1
```

### Solution 6
```python
from multiprocessing import Queue
q = Queue()
q.put("result")
print(q.get())
```

### Solution 7
```python
# I/O-задачи (сеть, файлы): потоки или asyncio
# CPU-задачи: multiprocessing
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a thread?
- Lightweight task
- Process
- CPU
- None
* Correct answer: Lightweight task
Shared memory.

What is multiprocessing?
- Separate processes
- Threads
- Async
- None
* Correct answer: Separate processes
Own interpreter.

What is the GIL?
- Global interpreter lock
- A process
- A thread
- None
* Correct answer: Global interpreter lock
One thread.

What is join?
- Waits
- Starts
- Kills
- None
* Correct answer: Waits
Finish.

What is start?
- Begins
- Waits
- Ends
- None
* Correct answer: Begins
Thread.

What is Pool?
- Worker processes
- Threads
- Lock
- None
* Correct answer: Worker processes
Map.

What is map?
- Distributes work
- Serial
- Waits
- None
* Correct answer: Distributes work
Result.

What is a Lock?
- Mutual exclusion
- Queue
- Process
- None
* Correct answer: Mutual exclusion
Race.

What is a race?
- Concurrent conflict
- Fine
- Solved
- None
* Correct answer: Concurrent conflict
Lock.

What is a Queue?
- Safe passing
- Lock
- Pool
- None
* Correct answer: Safe passing
Between.

What is CPU-bound?
- Compute heavy
- I/O
- Memory
- None
* Correct answer: Compute heavy
Processes.

What is I/O-bound?
- Waiting
- Compute
- Loop
- None
* Correct answer: Waiting
Threads/async.
<!--/QUIZ-->
