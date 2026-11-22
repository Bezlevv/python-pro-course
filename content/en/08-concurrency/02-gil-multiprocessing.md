---
title: GIL and multiprocessing
summary: What GIL is, why threads don't accelerate CPU tasks, processes.
order: 2
duration: 45 min
difficulty: advanced
tags: gil, multiprocessing, processes
---

The GIL limits CPU parallelism of threads; processes bypass it.

## GIL

Global Interpreter Lock: only one thread executes Python bytecode at a time.

## CPU-bound

```python
def cpu_work(n=3_000_000):
    total = 0
    for i in range(n):
        total += i % 7
    return total
```

Threads won't speed this up.

## Processes

```python
from multiprocessing import Process

if __name__ == "__main__":
    processes = [Process(target=cpu_work) for _ in range(4)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
```

## Value/Queue

```python
from multiprocessing import Process, Value

def inc(counter):
    for _ in range(1_000_000):
        with counter.get_lock():
            counter.value += 1
```

## Lesson summary

Use processes for CPU-bound work; threads for I/O.

<!--TASK-->
### Task 1 — GIL explanation
Describe GIL in comments.

### Task 2 — CPU threads
Measure 4 threads vs sequential for cpu_work.

### Task 3 — Processes
Run 4 processes and compare time.

### Task 4 — Value
Share a counter with Value and lock.

### Task 5 — Queue
Send results between processes with Queue.

### Task 6 — if __name__
Explain why the guard is required.

### Task 7 — Choose
Decide: threads or processes for downloading files.
<!--/TASK-->

<!--HINT-->
### Hint 1
One bytecode at a time.

### Hint 2
time.perf_counter().

### Hint 3
Process.

### Hint 4
Value("i", 0) + get_lock.

### Hint 5
Queue.put/get.

### Hint 6
spawn.

### Hint 7
Threads (I/O).
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
# GIL позволяет выполнять байт-код только одному потоку
# → потоки не ускоряют CPU-задачи
```

### Solution 2
```python
import threading, time

start = time.perf_counter()
for _ in range(4):
    cpu_work()
sequential = time.perf_counter() - start

threads = [threading.Thread(target=cpu_work) for _ in range(4)]
start = time.perf_counter()
for t in threads: t.start()
for t in threads: t.join()
threaded = time.perf_counter() - start
print(sequential, threaded)
```

### Solution 3
```python
from multiprocessing import Process

if __name__ == "__main__":
    start = time.perf_counter()
    processes = [Process(target=cpu_work) for _ in range(4)]
    for p in processes: p.start()
    for p in processes: p.join()
    print(time.perf_counter() - start)
```

### Solution 4
```python
from multiprocessing import Process, Value

def inc(counter):
    for _ in range(1_000_000):
        with counter.get_lock():
            counter.value += 1

if __name__ == "__main__":
    counter = Value("i", 0)
    ps = [Process(target=inc, args=(counter,)) for _ in range(8)]
    for p in ps: p.start()
    for p in ps: p.join()
    print(counter.value)   # 8_000_000
```

### Solution 5
```python
from multiprocessing import Process, Queue

def square(x, q):
    q.put(x * x)

if __name__ == "__main__":
    q = Queue()
    ps = [Process(target=square, args=(i, q)) for i in range(5)]
    for p in ps: p.start()
    for p in ps: p.join()
    print(sorted([q.get() for _ in range(5)]))
```

### Solution 6
```python
# На Windows процессы создаются через spawn:
# без if __name__ код создания выполнился бы в каждом потомке
```

### Solution 7
```python
# Скачивание файлов — I/O:
# потоки подходят лучше и легче процессов
```
<!--/SOLUTION-->

<!--QUIZ-->
What is GIL?
- Global Interpreter Lock
- A library
- A process
- A queue
* Correct answer: Global Interpreter Lock
CPython.

Why don't threads help CPU tasks?
- GIL
- Memory
- Speed
- None
* Correct answer: GIL
One at a time.

What is a process?
- Independent interpreter
- A thread
- A file
- A lock
* Correct answer: Independent interpreter
Own GIL.

What is spawn?
- Process creation method
- A thread
- A lock
- None
* Correct answer: Process creation method
Windows.

What does Process.start do?
- Starts a process
- Ends
- Joins
- None
* Correct answer: Starts a process
Run.

What does join do?
- Waits for completion
- Starts
- Kills
- None
* Correct answer: Waits for completion
Block.

What is Value?
- Shared memory
- A type
- A lock
- None
* Correct answer: Shared memory
Processes.

What does get_lock do?
- Lock for Value
- Creates
- Deletes
- None
* Correct answer: Lock for Value
Protect.

What is Queue?
- Inter-process queue
- A list
- A lock
- None
* Correct answer: Inter-process queue
Send data.

What is CPU-bound?
- Computations dominate
- I/O dominates
- Memory
- Network
* Correct answer: Computations dominate
Use processes.

What is I/O-bound?
- Waiting dominates
- Computations
- Both
- None
* Correct answer: Waiting dominates
Use threads.

Why the guard?
- Avoid recursive spawn
- Speed
- Memory
- None
* Correct answer: Avoid recursive spawn
Required on Windows.
<!--/QUIZ-->
