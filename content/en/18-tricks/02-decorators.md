---
title: Decorators and callable patterns
summary: Functions as objects, decorator basics.
order: 2
duration: 45 min
difficulty: advanced
tags: decorators
---

Functions are objects: pass them around.

## Functions as values

```python
def shout(text):
    return text.upper()

def apply(func, value):
    return func(value)

print(apply(shout, "hi"))   # HI
```

## Decorator

```python
def logged(func):
    def wrapper(*args, **kwargs):
        print("call", func.__name__)
        return func(*args, **kwargs)
    return wrapper

@logged
def add(a, b):
    return a + b
```

## Lesson summary

Decorators wrap behavior around functions.

<!--TASK-->
### Task 1 — Pass function
Write apply(func, value).

### Task 2 — Simple decorator
Log calls.

### Task 3 — Preserve name
Use functools.wraps.

### Task 4 — With args
Decorator taking a parameter.

### Task 5 — Timer
Time a function.

### Task 6 — Multiple
Stack two decorators.

### Task 7 — Use
Decorate with @logged.
<!--/TASK-->

<!--HINT-->
### Hint 1
func(value).

### Hint 2
Wrapper.

### Hint 3
wraps.

### Hint 4
Outer arg.

### Hint 5
time.

### Hint 6
Order.

### Hint 7
@.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
def apply(func, value):
    return func(value)
```

### Solution 2
```python
def logged(func):
    def wrapper(*args, **kwargs):
        print("call", func.__name__)
        return func(*args, **kwargs)
    return wrapper
```

### Solution 3
```python
from functools import wraps

def logged(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### Solution 4
```python
def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def hello():
    print("hi")
```

### Solution 5
```python
import time

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(func.__name__, time.perf_counter() - start)
        return result
    return wrapper
```

### Solution 6
```python
@timer
@logged
def work():
    return 42
# применяется снизу вверх: logged, затем timer
```

### Solution 7
```python
@logged
def add(a, b):
    return a + b
add(1, 2)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a decorator?
- Wraps functions
- A loop
- A class
- None
* Correct answer: Wraps functions
@.

What is wrapper?
- Inner function
- Outer
- Data
- None
* Correct answer: Inner function
Runs.

What is *args?
- Positional args
- Keyword
- Errors
- None
* Correct answer: Positional args
Tuple.

What is **kwargs?
- Keyword args
- Positional
- Names
- None
* Correct answer: Keyword args
Dict.

What is wraps?
- Preserves metadata
- Deletes
- Renames
- None
* Correct answer: Preserves metadata
Name.

What is a closure?
- Captures context
- Global
- Error
- None
* Correct answer: Captures context
Outer.

What is first-class function?
- Passable value
- Restricted
- Special
- None
* Correct answer: Passable value
Object.

What is @?
- Decorator syntax
- At sign only
- Operator
- None
* Correct answer: Decorator syntax
Apply.

What is stacking?
- Multiple decorators
- One
- None
- Error
* Correct answer: Multiple decorators
Order.

What is a timer decorator?
- Measures time
- Logs
- Caches
- None
* Correct answer: Measures time
perf_counter.

What is a parameterized decorator?
- Takes arguments
- Simple
- Error
- None
* Correct answer: Takes arguments
@repeat(3).

What is the benefit?
- Reusable behavior
- Speed
- Style
- None
* Correct answer: Reusable behavior
DRY.
<!--/QUIZ-->
