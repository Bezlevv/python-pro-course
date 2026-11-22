---
title: Amazing Language Features
summary: Decorators, functools.cache caching, contextlib, itertools, and dataclasses — tools that make code shorter and stronger.
order: 4
duration: 35 min
difficulty: intermediate
tags: decorators, functools, contextlib, itertools, dataclasses
---

It's time for the features that make Python worth loving: small but powerful tools from the standard library. They turn tedious code into short, expressive code.

## Decorators: functions that adorn functions

A decorator is a function that takes a function and returns a new, extended version. The classic is timing:

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.6f} sec")
        return result
    return wrapper

@timer
def slow_square(x):
    time.sleep(0.1)
    return x * x

print(slow_square(5))  # prints the time and 25
```

The `@timer` notation is just sugar for `slow_square = timer(slow_square)`. The `wrapper` function accepts any arguments (`*args, **kwargs`) and passes them through — so the decorator fits any function.

## functools.cache: instant caching

The `@functools.cache` decorator remembers call results. Returning Fibonacci without exponential complexity — one line:

```python
from functools import cache

@cache
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(50))  # 12586269025, instantly
```

Without `@cache`, such a call would take billions of years. Cache is precisely "remembering the past."

## contextlib: context managers without classes

The `with` statement guarantees that a resource will be closed even if an error occurs:

```python
with open("notes.txt", "w") as f:
    f.write("Hello!")
```

And `@contextlib.contextmanager` lets you make your own context manager with a simple function:

```python
from contextlib import contextmanager

@contextmanager
def temporary_message():
    print("Entering the block")
    yield
    print("Leaving the block")

with temporary_message():
    print("Inside the block")
```

## itertools: a factory of iterators

The `itertools` module is a treasure trove of small generators:

```python
from itertools import count, cycle, chain

# infinite counter
evens = count(0, 2)          # 0, 2, 4, ...
print(next(evens), next(evens))  # 0 2

# cycle over a list
turns = cycle(["rock", "scissors", "paper"])
print(next(turns), next(turns), next(turns))  # rock scissors paper

# chaining sequences
combined = chain([1, 2], [3, 4])
print(list(combined))  # [1, 2, 3, 4]
```

## dataclasses: data classes without boilerplate

An ordinary "data bag" class requires writing `__init__`, `__repr__`, comparisons... `@dataclass` does it automatically:

```python
from dataclasses import dataclass

@dataclass
class Book:
    title: str
    author: str
    pages: int

book = Book("War and Peace", "Tolstoy", 1274)
print(book)          # Book(title='War and Peace', author='Tolstoy', pages=1274)
print(book.pages)    # 1274
```

One decorator line — and the class got a constructor, a beautiful representation, and comparison between instances.

## Why does all this matter?

These tools don't just shorten code — they eliminate whole classes of errors: decorators spare you from copying timers, cache — from manual cache dictionaries, context managers — from forgotten file closes, dataclasses — from typos in `__init__`. These are features that make the programmer faster and the code more reliable. Let's try them out.

<!--TASK-->
### Task 1
Write a decorator `logger` that prints the line `Calling <function name>` before calling the function, and `Done!` after. Apply it to a function `add(a, b)` that returns the sum. Call `add(3, 4)` and make sure both service lines and the result `7` appear on the screen. Use `*args` and `**kwargs` inside the wrapper so the decorator works with any function.

### Task 2
Use `@functools.cache` to speed up a recursive Fibonacci function. Write a function `fib(n)` that returns the nth Fibonacci number (0, 1, 1, 2, ...). Add a recursion call counter: a global variable `calls` that the function increments on every call. Print `fib(30)` and the value of `calls` after computing. Then comment out (or remove) `@cache`, print `fib(30)` and `calls` again — and compare how many times more calls happened without the cache. Expected result: with cache, calls is noticeably smaller (dozens); without cache — millions.

### Task 3
Using `@contextlib.contextmanager`, write a context manager `indent` that prints `>>>` before each line inside the block. To do this, it should return a printing function via `yield`, and after `yield` print `<<<`. Inside `with indent() as print_indented:`, call `print_indented("line 1")` and `print_indented("line 2")`. Expected output:

```text
>>> line 1
>>> line 2
<<<
```

### Task 4
Using `itertools.count` and `itertools.cycle`, write a program that: 1) prints the first 5 even numbers from the infinite counter `count(0, 2)`; 2) prints the first 6 values of the cycle `cycle(["🐍", "❤️"])` (emoji or the words "python", "love"). Use `islice` from `itertools` to limit the number of values. Expected output: `0 2 4 6 8` and `🐍 ❤️ 🐍 ❤️ 🐍 ❤️`.

### Task 5
Create a class `Student` with `@dataclass` with fields: `name` (string), `group` (string, default `"PY-31"`), `scores` (list of grades, default `field(default_factory=list)`). Add a method `average()` that returns the average grade (if there are no grades — `0.0`). Create two students: one with grades, one without. Print both with `print()` and the averages. Expected result: a clean object representation and the numbers `4.5` and `0.0`.

<!--/TASK-->

<!--HINT-->
### Hint 1
A decorator is a function that takes a function and returns a wrapper: `def logger(func):` inside define `def wrapper(*args, **kwargs):` and return `wrapper`. Inside `wrapper`, first print, then call `func(*args, **kwargs)` and save the result, then print and return the result. Apply it with `@logger` above the function.

### Hint 2
`from functools import cache`, then `@cache` above `def fib(n):`. Increment the counter `calls` as the first line of the function body: `global calls; calls += 1`. Make sure `calls` is declared at module level. For comparison, remove the decorator and run again — but be careful: without the cache, `fib(30)` makes about 2.7 million calls, which is fine time-wise.

### Hint 3
Under `@contextmanager`, you don't need to print `>>>` outside — instead, inside `yield` return a local function: `def print_line(line): print(">>>", line)`. Everything after `yield` runs when exiting the block: `print("<<<")`.

### Hint 4
`islice(iterable, n)` takes the first n elements: `list(islice(count(0, 2), 5))`. For the cycle: `list(islice(cycle(["🐍", "❤️"]), 6))`. Print the lists with `print()` — or space-separated if it looks nicer.

### Hint 5
`from dataclasses import dataclass, field`. For a mutable default value (a list) use `field(default_factory=list)` — otherwise Python will raise an error about a mutable object. The `average` method: `return sum(self.scores) / len(self.scores) if self.scores else 0.0`.

<!--/HINT-->

<!--SOLUTION-->
### Walkthrough 1
Solution:

```python
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print("Done!")
        return result
    return wrapper

@logger
def add(a, b):
    return a + b

print(add(3, 4))
```

Result:

```
Calling add
Done!
7
```

What's happening here? The decorator `logger` is a function that takes `func` and returns `wrapper`. When we write `@logger` above `add`, Python does `add = logger(add)`, and now `add` is `wrapper`. When `add(3, 4)` is called, `wrapper` runs: it prints the function name, calls the real `add` with the same arguments (`*args, **kwargs` pass them unchanged), prints "Done!" and returns the result. Thanks to `*args, **kwargs`, the decorator can be attached to any function.

### Walkthrough 2
Solution:

```python
from functools import cache

calls = 0

@cache
def fib(n):
    global calls
    calls += 1
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(30))
print("Calls with cache:", calls)
```

Result:

```
832040
Calls with cache: 31
```

What's happening here? `@cache` remembers the result for each argument. So every `n` from 0 to 30 is computed exactly once: 31 calls in total instead of millions. Without the decorator, `fib(30)` would recursively call itself about 2.7 million times — and the numbers would grow exponentially. Cache is an elegant solution to a classic problem: we add one decorator and get a speedup of hundreds of thousands of times. Meanwhile the code stays clean and readable.

### Walkthrough 3
Solution:

```python
from contextlib import contextmanager

@contextmanager
def indent():
    def print_line(line):
        print(">>>", line)
    yield print_line
    print("<<<")

with indent() as print_indented:
    print_indented("line 1")
    print_indented("line 2")
```

Result:

```
>>> line 1
>>> line 2
<<<
```

What's happening here? The code before `yield` runs when entering the `with` — here we create the function `print_line` and hand it out via `yield`. The variable `print_indented` in `with` receives exactly that. Inside the block we call `print_indented`, and it prints lines with the `>>>` prefix. When the block ends, the code after `yield` runs — `print("<<<")`. This construct is a compact way to make a context manager without a class with `__enter__` and `__exit__` methods.

### Walkthrough 4
Solution:

```python
from itertools import count, cycle, islice

print(list(islice(count(0, 2), 5)))
print(list(islice(cycle(["🐍", "❤️"]), 6)))
```

Result:

```
[0, 2, 4, 6, 8]
['🐍', '❤️', '🐍', '❤️', '🐍', '❤️']
```

What's happening here? `count(0, 2)` is an infinite counter of even numbers. By itself it's infinite, so we limit it with `islice(..., 5)`, which takes the first 5 elements. `cycle(["🐍", "❤️"])` repeats the list forever, and `islice` takes the first 6 elements. Notice: the whole `itertools` module is built on lazy generators — infinite sequences don't occupy memory; they're computed on demand.

### Walkthrough 5
Solution:

```python
from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    group: str = "PY-31"
    scores: list = field(default_factory=list)

    def average(self):
        if self.scores:
            return sum(self.scores) / len(self.scores)
        return 0.0

anna = Student("Anna", scores=[5, 4, 5, 4])
borya = Student("Borya")

print(anna)
print(anna.average())
print(borya)
print(borya.average())
```

Result:

```
Student(name='Anna', group='PY-31', scores=[5, 4, 5, 4])
4.5
Student(name='Borya', group='PY-31', scores=[])
0.0
```

What's happening here? `@dataclass` automatically generates the constructor, `__repr__` (the clean representation for `print`), and object comparison. `field(default_factory=list)` is a must for mutable default values: without it, all students would share one common list. The `average()` method uses a ternary expression: if there are grades — it computes the average; otherwise — `0.0`. The class came out short but complete — without the boilerplate of a manual `__init__`.

<!--/SOLUTION-->

<!--QUIZ-->
What does a decorator do in Python?
- Takes a function and returns its extended version
- Deletes the function
- Renames the function
* Correct answer: Takes a function and returns its extended version
A decorator wraps a function, adding behavior without changing the original code.

What does the @timer annotation above a function mean?
- func = timer(func)
- timer = func(timer)
- func = timer()
* Correct answer: func = timer(func)
@timer is syntactic sugar for assigning the wrapper to the original function.

What does @functools.cache do?
- Remembers the results of function calls
- Speeds up the disk
- Cleans memory
* Correct answer: Remembers the results of function calls
cache caches the result for each argument and reuses it.

Why does fib(30) make about 2.7 million calls without cache but only 31 with @cache?
- The cache remembers every computed result and doesn't recompute it
- The cache executes calls faster
- The cache removes the recursion
* Correct answer: The cache remembers every computed result and doesn't recompute it
Each argument is computed once; the remaining accesses take the result from memory.

Which operator guarantees the file is closed even on error?
- with open(...) as f:
- f.close()
- open(...)
* Correct answer: with open(...) as f:
The with operator automatically closes the file when leaving the block.

What does @contextlib.contextmanager do?
- Lets you create a context manager from a function with yield
- Creates a class
- Stops the program
* Correct answer: Lets you create a context manager from a function with yield
The code before yield runs on entry, after — on exit from the with block.

What does itertools.count(0, 2) do?
- Infinitely generates the numbers 0, 2, 4, ...
- Returns a list of five numbers
- Counts up to 2
* Correct answer: Infinitely generates the numbers 0, 2, 4, ...
count is a lazy infinite counter that you limit with islice or a loop.

What does itertools.cycle(["a", "b"]) do?
- Infinitely repeats the elements of the list
- Returns a list of two elements
- Shuffles the list
* Correct answer: Infinitely repeats the elements of the list
cycle loops the sequence: a, b, a, b, ...

Why is field(default_factory=list) needed in a dataclass?
- So each instance gets its own separate list
- So the list is shared by all instances
- So the field becomes required
* Correct answer: So each instance gets its own separate list
default_factory creates a new list for each object, avoiding a shared mutable value.

What does @dataclass automatically create?
- The constructor, __repr__, and comparison
- Only the __init__ method
- Nothing, only annotations
* Correct answer: The constructor, __repr__, and comparison
dataclass generates the routine methods from the field annotations.
<!--/QUIZ-->
