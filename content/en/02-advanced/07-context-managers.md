---
title: Context managers (with)
summary: The with statement, __enter__/__exit__, contextlib.contextmanager and nested managers.
order: 7
duration: 40 min
difficulty: intermediate
tags: with, context manager, __enter__, __exit__, contextlib
---

A context manager automates setup and cleanup: open a resource, use it, always close it — even on errors.

## with

```python
with open("file.txt", encoding="utf-8") as f:
    print(f.read())
# the file is closed automatically
```

## Custom context manager

```python
class ManagedFile:
    def __init__(self, path):
        self.path = path
    def __enter__(self):
        self.f = open(self.path, "w", encoding="utf-8")
        return self.f
    def __exit__(self, exc_type, exc_val, tb):
        self.f.close()
        return False   # do not suppress exceptions
```

## contextlib.contextmanager

```python
from contextlib import contextmanager

@contextmanager
def managed_file(path):
    f = open(path, "w", encoding="utf-8")
    try:
        yield f
    finally:
        f.close()
```

## Nested and chained

Multiple `with` statements can be combined:

```python
with open("a.txt") as a, open("b.txt") as b:
    ...
```

## Lesson summary

Context managers guarantee cleanup. Implement via __enter__/__exit__ or @contextmanager.

<!--TASK-->
### Task 1 — File with with
Write and read a file using with; confirm it can be read after the block.

### Task 2 — Custom ManagedFile
Implement class ManagedFile with __enter__/__exit__ and test writing.

### Task 3 — __exit__ signature
Implement __exit__ that prints the exception type on error, then returns False.

### Task 4 — contextmanager
Rewrite ManagedFile using @contextmanager and yield.

### Task 5 — Timer manager
Create Timer that prints elapsed time in __exit__.

### Task 6 — Suppress
Write a context manager Suppress(Exc) that swallows a given exception and prints a message.

### Task 7 — Nested with
Open two files with one with statement and write lines from one into another.
<!--/TASK-->

<!--HINT-->
### Hint 1
with open(...) as f: f.write(...).

### Hint 2
__enter__ returns the resource; __exit__ cleans up.

### Hint 3
__exit__(self, exc_type, exc_val, tb).

### Hint 4
@contextmanager: yield inside try/finally.

### Hint 5
Record time in __enter__, print in __exit__.

### Hint 6
If exc_type is a subclass of Exc, print and return True.

### Hint 7
with open("a") as a, open("b", "w") as b:
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
with open("hello.txt", "w", encoding="utf-8") as f:
    f.write("Hello!")

with open("hello.txt", encoding="utf-8") as f:
    print(f.read())
```

### Solution 2
```python
class ManagedFile:
    def __init__(self, path):
        self.path = path
    def __enter__(self):
        self.f = open(self.path, "w", encoding="utf-8")
        return self.f
    def __exit__(self, exc_type, exc_val, tb):
        self.f.close()
        return False

with ManagedFile("data.txt") as f:
    f.write("123")
```

### Solution 3
```python
class ManagedFile:
    def __exit__(self, exc_type, exc_val, tb):
        if exc_type is not None:
            print("Error:", exc_type.__name__)
        self.f.close()
        return False
```

### Solution 4
```python
from contextlib import contextmanager

@contextmanager
def managed_file(path):
    f = open(path, "w", encoding="utf-8")
    try:
        yield f
    finally:
        f.close()

with managed_file("data.txt") as f:
    f.write("abc")
```

### Solution 5
```python
import time

class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self
    def __exit__(self, *args):
        print(f"Elapsed: {time.perf_counter() - self.start:.4f}")

with Timer():
    sum(range(100000))
```

### Solution 6
```python
class Suppress:
    def __init__(self, exc):
        self.exc = exc
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, tb):
        if exc_type and issubclass(exc_type, self.exc):
            print("Suppressed:", exc_val)
            return True
        return False

with Suppress(ZeroDivisionError):
    x = 1 / 0
print("No crash")
```

### Solution 7
```python
with open("a.txt", encoding="utf-8") as a, \
     open("b.txt", "w", encoding="utf-8") as b:
    b.write(a.read())
```
<!--/SOLUTION-->

<!--QUIZ-->
What does with guarantee?
- Cleanup of the resource
- Speed
- Sorting
- Nothing
* Correct answer: Cleanup of the resource
Even on errors.

Which method is called on enter?
- __enter__
- __init__
- __exit__
- __del__
* Correct answer: __enter__
Returns the resource.

Which method is called on exit?
- __exit__
- __enter__
- __close__
- __del__
* Correct answer: __exit__
Cleanup.

What should __exit__ return?
- False to propagate exceptions
- True always
- None
- The resource
* Correct answer: False to propagate exceptions
True suppresses.

What does @contextmanager turn into?
- A generator into a context manager
- A class
- A list
- A decorator only
* Correct answer: A generator into a context manager
Code before yield = enter.

What does yield do inside @contextmanager?
- Provides the resource
- Ends
- Returns
- Errors
* Correct answer: Provides the resource
with ... as f gives yielded object.

Can with combine two files?
- Yes, with open(...) as a, open(...) as b
- No
- Only one
- With loop
* Correct answer: Yes, with open(...) as a, open(...) as b
Multiple contexts.

What happens if an exception occurs in with?
- __exit__ still runs
- Nothing
- File stays open
- Program freezes
* Correct answer: __exit__ still runs
Cleanup guaranteed.

What does return True in __exit__ do?
- Suppresses the exception
- Re-raises it
- Logs it
- Stops
* Correct answer: Suppresses the exception
Continues after block.

Which is a built-in context manager?
- open() with with
- list
- dict
- print
* Correct answer: open() with with
File objects.

What is timer context manager useful for?
- Measuring elapsed time
- Writing files
- Reading
- Deleting
* Correct answer: Measuring elapsed time
Auto cleanup around timing.

Where to close a resource manually?
- In __exit__
- In __init__
- In __enter__
- Never
* Correct answer: In __exit__
Guaranteed execution.
<!--/QUIZ-->
