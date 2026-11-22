---
title: Context managers and with
summary: with blocks, __enter__/__exit__.
order: 3
duration: 40 min
difficulty: intermediate
tags: context manager, with
---

with manages resources safely.

## Files

```python
with open("data.txt", "w") as f:
    f.write("hello")
# файл закрыт автоматически
```

## Custom

```python
class ManagedFile:
    def __init__(self, name):
        self.name = name
    def __enter__(self):
        self.file = open(self.name, "w")
        return self.file
    def __exit__(self, exc_type, exc, tb):
        self.file.close()

with ManagedFile("data.txt") as f:
    f.write("hi")
```

## contextlib

```python
from contextlib import contextmanager

@contextmanager
def managed(name):
    f = open(name, "w")
    try:
        yield f
    finally:
        f.close()
```

## Lesson summary

with guarantees cleanup even on errors.

<!--TASK-->
### Task 1 — File
Open with and write.

### Task 2 — Custom
Implement __enter__/__exit__.

### Task 3 — contextmanager
Use @contextmanager.

### Task 4 — Why
Why not manual close?

### Task 5 — Multiple
Open two files in one with.

### Task 6 — suppress
Ignore an error with contextlib.suppress.

### Task 7 — Timing
Time a block with a manager.
<!--/TASK-->

<!--HINT-->
### Hint 1
open.

### Hint 2
__enter__.

### Hint 3
yield.

### Hint 4
Cleanup.

### Hint 5
Comma.

### Hint 6
suppress.

### Hint 7
Timer.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
with open("data.txt", "w") as f:
    f.write("hello")
```

### Solution 2
```python
class ManagedFile:
    def __init__(self, name):
        self.name = name
    def __enter__(self):
        self.file = open(self.name, "w")
        return self.file
    def __exit__(self, exc_type, exc, tb):
        self.file.close()
```

### Solution 3
```python
from contextlib import contextmanager

@contextmanager
def managed(name):
    f = open(name, "w")
    try:
        yield f
    finally:
        f.close()
```

### Solution 4
```python
# with закрывает ресурс даже при исключении —
# вручную легко забыть
```

### Solution 5
```python
with open("a.txt") as a, open("b.txt") as b:
    print(a.read(), b.read())
```

### Solution 6
```python
from contextlib import suppress
with suppress(FileNotFoundError):
    open("missing.txt").read()
# ошибка проигнорирована
```

### Solution 7
```python
import time
from contextlib import contextmanager

@contextmanager
def timer():
    start = time.perf_counter()
    try:
        yield
    finally:
        print(time.perf_counter() - start)

with timer():
    sum(range(1_000_000))
```
<!--/SOLUTION-->

<!--QUIZ-->
What is with?
- Block
- Loop
- Function
- None
* Correct answer: Block
Context.

What is __enter__?
- Sets up
- Cleans
- Runs
- None
* Correct answer: Sets up
Returns.

What is __exit__?
- Cleans up
- Sets
- Opens
- None
* Correct answer: Cleans up
Close.

What is yield?
- Pauses/passes
- Ends
- Errors
- None
* Correct answer: Pauses/passes
contextmanager.

What is finally?
- Always runs
- If error
- Never
- None
* Correct answer: Always runs
Guarantee.

What is a resource?
- File/connection
- A number
- A loop
- None
* Correct answer: File/connection
Must close.

Why with?
- Auto cleanup
- Speed
- Style
- None
* Correct answer: Auto cleanup
Safe.

What is suppress?
- Ignores errors
- Raises
- Logs
- None
* Correct answer: Ignores errors
contextlib.

What is a generator?
- yield function
- A list
- A class
- None
* Correct answer: yield function
Lazy.

What is the file mode "w"?
- Write
- Read
- Append
- None
* Correct answer: Write
Truncate.

What happens on exception?
- __exit__ runs
- Nothing
- Crash only
- None
* Correct answer: __exit__ runs
Cleanup.

What is a double with?
- Two resources
- One
- Error
- None
* Correct answer: Two resources
Comma.
<!--/QUIZ-->
