---
title: Typical Python Questions
summary: We break down the questions most often asked in interviews: mutable types, decorators, generators, GIL, closures, and context managers.
order: 2
duration: 50 min
difficulty: advanced
tags: python, interview, decorators, generators, gil, closures
---

A technical Python interview usually has two parts: language questions and coding tasks. In this lesson we'll go through the most common topics and learn to answer in a way that shows the interviewer real understanding, not memorized phrases.

## Mutable and immutable objects

Python has mutable (`list`, `dict`, `set`) and immutable (`int`, `str`, `tuple`, `frozenset`) objects. An immutable object can't be changed "in place": any operation creates a new object. This matters for data safety and for passing arguments to functions.

```python
s = "abc"
# s[0] = "x"  # TypeError: 'str' object does not support item assignment
```

Beginners often confuse `==` and `is`: `==` compares values, while `is` checks whether it's the very same object (the same memory address). For `int` and `str`, Python sometimes reuses objects (interning), so `x is y` may return `True` for `256` but `False` for `257`. Never rely on `is` to compare values.

## The dangerous mutable default argument

```python
def add(item, result=[]):
    result.append(item)
    return result
```

The default list is created once when the function is defined and lives between calls. A classic interview item is to explain the bug and fix it with `None`:

```python
def add(item, result=None):
    if result is None:
        result = []
    result.append(item)
    return result
```

## Decorators

A decorator is a function that takes a function and returns a new one. Most often, to add a wrapper: logging, timing, permission checks.

```python
import functools

def logged(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

`functools.wraps` preserves the name and docstring of the original function — this is often asked about.

## Generators and iterators

An iterator is an object with a `__next__` method. A generator is a function with `yield`: it pauses and yields one value at a time, so it doesn't hold everything in memory.

```python
def squares(n):
    for i in range(n):
        yield i * i
```

The generator body runs lazily, during iteration. If asked "what does print(gen) output?" — the correct answer is: the generator object, not numbers.

## GIL

The GIL (Global Interpreter Lock) is a global interpreter lock: only one thread of Python code runs at any moment. That's why threads don't speed up CPU-bound tasks; for those you use `multiprocessing`, and `asyncio` for I/O. The point is to understand the consequences, not just name the term.

## Closures and nonlocal

A closure is a function that remembers variables from the enclosing scope even after that scope has finished:

```python
def make_counter():
    count = 0
    def inc():
        nonlocal count
        count += 1
        return count
    return inc
```

Without `nonlocal`, the assignment `count += 1` would create a new local variable inside `inc`.

## *args and **kwargs

`*args` collects extra positional arguments into a tuple; `**kwargs` collects named ones into a dict. They are also used to forward parameters to another function.

## Context managers

`with` opens a resource and guarantees it gets closed even on error. You can write your own manager with a class implementing `__enter__`/`__exit__`, or with `contextlib.contextmanager`.

## How to answer

Think out loud. If you don't know the answer, say so — but show your line of reasoning. Write code carefully and watch out for edge cases: empty input, `None`, large sizes. The interviewer evaluates not only correctness but how you think.

## Summary

Learn the core concepts: mutable types, `==` vs `is`, the mutable default argument bug, decorators, generators, GIL, closures, context managers. Be able to explain every example from this lesson fluently — that's enough for most interviews.

<!--TASK-->
### Task 1
Write a decorator `timer` that measures a function's execution time in seconds and prints a line like `Function name took 0.12 sec`. The decorator should accept any function with any arguments and return its result unchanged. Use `time.perf_counter()` for measuring. Test the decorator on a function that sums the numbers from 1 to 1,000,000, and make sure the time message appears in the console.

### Task 2
Write a generator `fibonacci(n)` that yields the first `n` Fibonacci numbers (starting with 0 and 1). Make sure `for x in fibonacci(10): print(x)` works and prints 10 numbers, and that `print(fibonacci(5))` shows a generator object, not a list of numbers. Compare it with a version that builds the whole list: explain why the generator saves memory.

### Task 3
The code below contains the classic mutable default argument bug:

```python
def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags
```

Write a fixed version that does not accumulate tags between calls. Verify: after `add_tag("python")` and `add_tag("sql")` calls, tags should accumulate independently, and calling again without the second argument should not contain tags from previous calls.

### Task 4
Write a function `make_counter()` that returns a counter function: each call returns a number one greater than the previous one (1, 2, 3...). Use a closure and `nonlocal`. Verify that two independent counters created via `make_counter()` don't affect each other.

### Task 5
Use `contextlib.contextmanager` to write a context manager `time_block()` that prints the execution time of the `with` block in seconds. Inside `with time_block():`, run `time.sleep(0.5)` and make sure a line with a time around 0.5 seconds appears on screen.

<!--/TASK-->

<!--HINT-->
### Hint 1
A decorator is a function that returns a wrapper `wrapper(*args, **kwargs)`. Inside the wrapper, measure the time before calling the function (`start = time.perf_counter()`), call it, measure the time after, and print the difference. Don't forget to return the function's result. For polish, add `functools.wraps`.

### Hint 2
A generator is written like a normal function but uses `yield` instead of `return`. Keep two variables `a` and `b`; in a `for _ in range(n)` loop yield `a`, then update the pair: `a, b = b, a + b`. Laziness means values are created one at a time, not all at once.

### Hint 3
The correct pattern: default value `None`, and inside the function create a new list if the argument wasn't passed. Compare the old and new behavior: in the old version, after the first call the tags stay in a shared list; in the new one, they don't.

### Hint 4
The outer function should have a variable `count = 0`, and the inner one should increment it via `nonlocal count`. Remember that without `nonlocal` Python will create a new local variable and the counter won't work. Return the inner function, not the result of calling it.

### Hint 5
The syntax: `@contextmanager` above a generator function, where `yield` separates "before the block" from "after the block". Everything before `yield` runs on entering `with`; everything after runs on exit. Measure the time around `yield` and print the difference.

<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"Function {func.__name__} took {elapsed:.2f} sec")
        return result
    return wrapper

@timer
def big_sum():
    return sum(range(1, 1_000_001))

print(big_sum())
```

Run it:

```bash
python timer_demo.py
```

Example output:

```
Function big_sum took 0.04 sec
500000500000
```

What's going on here? `wrapper` accepts any arguments via `*args, **kwargs` and passes them to the original function. We record the time before the call and compute the difference after. `functools.wraps` preserves the function's metadata (name, docstring) so the decorator is "transparent". The decorator returns the function's result unchanged, so `print(big_sum())` prints the sum, not `None`.

### Solution 2
Solution:

```python
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for x in fibonacci(10):
    print(x)

print(fibonacci(5))
```

The first lines of output:

```
0
1
1
2
3
...
```

What's going on here? The keyword `yield` turns the function into a generator. At each `next()` or loop step, execution pauses at `yield` and hands out the current value; on the next call it resumes from that point. So `fibonacci(5)` is a generator object (output like `<generator object fibonacci at 0x...>`), not a list. If we built the whole list, memory would grow linearly with `n`, while a generator stores only two variables — a win for large `n`.

### Solution 3
The fixed version:

```python
def add_tag(tag, tags=None):
    if tags is None:
        tags = []
    tags.append(tag)
    return tags

print(add_tag("python"))   # ['python']
print(add_tag("sql"))      # ['sql']
print(add_tag("flask"))    # ['flask']
```

What's going on here? In the original code, the list `tags=[]` was created once when the function was defined and lived between calls: a second call would add a tag to the same list as the first. This is the classic mutable default argument trap. In the fixed version the default is immutable `None`, and a new list is created on each call where the argument isn't passed. Result: every call is independent. This question is asked very often in interviews — be ready to explain both behaviors.

### Solution 4
Solution:

```python
def make_counter():
    count = 0
    def inc():
        nonlocal count
        count += 1
        return count
    return inc

c1 = make_counter()
c2 = make_counter()
print(c1())  # 1
print(c1())  # 2
print(c2())  # 1
```

What's going on here? The inner function `inc` "closes over" the variable `count` from the enclosing scope. Without `nonlocal`, the statement `count += 1` would create a new local variable inside `inc`, and the counter would always return 1. With `nonlocal`, we tell Python: modify the variable from the outer function. Each `make_counter()` call creates its own closure with its own `count`, so `c1` and `c2` are independent. Such counter factories are a common question about closures.

### Solution 5
Solution:

```python
from contextlib import contextmanager
import time

@contextmanager
def time_block():
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"Elapsed time: {elapsed:.2f} sec")

with time_block():
    time.sleep(0.5)
```

Run it:

```bash
python time_block_demo.py
```

Output:

```
Elapsed time: 0.50 sec
```

What's going on here? `@contextmanager` is a decorator from the `contextlib` module that turns a generator into a context manager. The code before `yield` runs when entering `with` (entering the block); the code after runs on exit. `try`/`finally` guarantees the timing happens even if an exception occurs inside the block. Such a manager is handy in tests and when profiling code — and it's a good answer to "how do I write my own context manager".

<!--/SOLUTION-->

<!--QUIZ-->
What does this code print: a = [1]; b = a; b.append(2); print(a)?
- [1]
- [1, 2]
- [2]
- Error
* Correct answer: [1, 2]
b is a reference to the same object as a, so changes through b are visible in a too.

Why is it dangerous to use [] as a default argument value?
- The list is created once and shared across all calls
- Python forbids lists in arguments
- Such code doesn't compile
- A list cannot be passed to a function
* Correct answer: The list is created once and shared across all calls
The default object is created when the function is defined and accumulates changes between calls.

What does the keyword yield do in a function?
- Turns the function into a generator
- Terminates the program
- Returns a value and ends the function
- Declares a variable
* Correct answer: Turns the function into a generator
yield pauses execution and yields a value, letting it resume from that point later.

How do == and is differ?
- == compares values, is compares references to the same object
- == compares references, is compares values
- They are the same
- is only works with strings
* Correct answer: == compares values, is compares references to the same object
is checks object identity, while == checks value equality.

What is the GIL?
- A global interpreter lock that limits thread parallelism
- A library for working with graphics
- A floating-point number format
- The Java virtual machine
* Correct answer: A global interpreter lock that limits thread parallelism
The GIL allows only one thread of Python code to run at a time, so processes are used for CPU-bound tasks.

Why is nonlocal needed inside a nested function?
- To change a variable from the enclosing function
- To declare a global variable
- To create a constant
- To make a function asynchronous
* Correct answer: To change a variable from the enclosing function
Without nonlocal, the assignment would create a new local variable in the nested function.

How is a generator different from a list?
- A generator yields items one at a time and doesn't store the whole set in memory
- A generator stores all items in memory
- They are the same
- A generator cannot be iterated
* Correct answer: A generator yields items one at a time and doesn't store the whole set in memory
Generators' laziness saves memory on large data sets.

What is a decorator?
- A function that takes a function and returns a new function with extended behavior
- A special class from the standard library
- A data type
- A language operator
* Correct answer: A function that takes a function and returns a new function with extended behavior
A decorator wraps a function without changing its source code.

<!--/QUIZ-->
