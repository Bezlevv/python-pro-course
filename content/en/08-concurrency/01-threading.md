---
title: Threads: threading and Lock
summary: Creating threads, join, daemons, data races, Lock.
order: 1
duration: 40 min
difficulty: intermediate
tags: threads, threading, Lock
---

Threads let code run "at the same time" within one process.

## Create and start

```python
import threading
import time

def say_hello(name):
    time.sleep(0.5)
    print(f"Hello, {name}!")

threads = []
for name in ["Anna", "Boris", "Vika"]:
    t = threading.Thread(target=say_hello, args=(name,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
```

## join

`join()` waits for a thread to finish.

## Daemons

`daemon=True` — thread does not block program exit.

## Data race

```python
counter = 0
ITERATIONS = 1_000_000

def increment():
    global counter
    for _ in range(ITERATIONS):
        counter += 1
# результат часто меньше ожидаемого
```

## Lock

```python
lock = threading.Lock()

def increment_safe():
    global counter
    for _ in range(ITERATIONS):
        with lock:
            counter += 1
```

## Lesson summary

Threads give concurrency; protect shared data with Lock.

<!--TASK-->
### Task 1 — Threads
Create 5 threads that print their names.

### Task 2 — join
Ensure "All done" prints after threads finish.

### Task 3 — Data race
Run 8 threads incrementing a counter; print it.

### Task 4 — Lock
Fix with Lock and get the exact result.

### Task 5 — Daemon
Create a daemon thread; explain program exit.

### Task 6 — RLock
Use RLock in a recursive function.

### Task 7 — Event
Use threading.Event to coordinate start.
<!--/TASK-->

<!--HINT-->
### Hint 1
Thread(target=fn, args=(...)).

### Hint 2
t.join().

### Hint 3
global counter.

### Hint 4
with lock:.

### Hint 5
daemon=True.

### Hint 6
RLock.

### Hint 7
event.wait()/set().
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import threading

def worker(name):
    print(name)

threads = [threading.Thread(target=worker, args=(f"T{i}",)) for i in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

### Solution 2
```python
for t in threads:
    t.join()
print("All done")
```

### Solution 3
```python
counter = 0
ITERATIONS = 1_000_000

def increment():
    global counter
    for _ in range(ITERATIONS):
        counter += 1

threads = [threading.Thread(target=increment) for _ in range(8)]
for t in threads: t.start()
for t in threads: t.join()
print(counter)   # часто < 8_000_000
```

### Solution 4
```python
lock = threading.Lock()

def increment_safe():
    global counter
    for _ in range(ITERATIONS):
        with lock:
            counter += 1
# ровно 8_000_000
```

### Solution 5
```python
t = threading.Thread(target=worker, daemon=True)
t.start()
# программа завершится без ожидания демона
```

### Solution 6
```python
lock = threading.RLock()

def recurse(n):
    with lock:
        if n > 0:
            recurse(n - 1)
```

### Solution 7
```python
event = threading.Event()

def waiter():
    event.wait()
    print("started")

t = threading.Thread(target=waiter)
t.start()
event.set()
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a thread?
- A line of execution
- A process
- A file
- A lock
* Correct answer: A line of execution
Within a process.

What does start() do?
- Begins the thread
- Ends
- Joins
- Locks
* Correct answer: Begins the thread
Run.

What does join() do?
- Waits for the thread
- Starts
- Kills
- None
* Correct answer: Waits for the thread
Block.

What is a data race?
- Unsynchronized shared access
- Fast code
- A bug in print
- None
* Correct answer: Unsynchronized shared access
Lost updates.

What is a Lock?
- Mutual exclusion
- A thread
- A queue
- A counter
* Correct answer: Mutual exclusion
Protects.

What is `with lock:`?
- Safe acquire/release
- A loop
- A thread
- None
* Correct answer: Safe acquire/release
Context.

What is a daemon?
- Non-blocking background thread
- Main thread
- Lock
- Counter
* Correct answer: Non-blocking background thread
Exits with program.

What is RLock?
- Reentrant lock
- Regular lock
- Read lock
- None
* Correct answer: Reentrant lock
Same thread reacquire.

What is GIL?
- Global interpreter lock
- Global input list
- Guard
- None
* Correct answer: Global interpreter lock
CPython.

Do threads speed up CPU work?
- No, usually not
- Yes, always
- Only I/O
- None
* Correct answer: No, usually not
GIL.

What is a race window?
- Between read and write
- A lock
- A thread
- None
* Correct answer: Between read and write
Loss.

What is threading.Event?
- Signaling primitive
- A timer
- A lock
- A thread
* Correct answer: Signaling primitive
set/wait.
<!--/QUIZ-->
