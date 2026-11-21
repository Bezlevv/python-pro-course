---
title: Decorators
summary: How decorators work, closures, functools.wraps and decorators with arguments.
order: 4
duration: 45 min
difficulty: intermediate
tags: decorators, closures, wraps, wrapper
---

A decorator is a function that takes another function and returns a new function that wraps it: add behavior without changing the original code.

## Functions are objects

```python
def greet(name):
    return f"Hello, {name}!"

def shout(func, name):
    return func(name).upper()

print(shout(greet, "Anna"))   # HELLO, ANNA!
```

## Closures

A nested function that remembers variables from the outer function:

```python
def make_multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply

double = make_multiplier(2)
print(double(5))   # 10
```

## First decorator

```python
def loud(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"Function returned: {result}")
        return result
    return wrapper

@loud
def add(a, b):
    return a + b
```

`@loud` is sugar for `add = loud(add)`.

## functools.wraps

Keep the name and docstring of the original:

```python
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ...
    return wrapper
```

## Decorators with arguments

```python
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def say_hi():
    print("Hi!")
```

## Lesson summary

Decorators wrap functions: logging, timing, caching, access checks. Remember three levels: function → wrapper → application via @.

<!--TASK-->
### Task 1 — First wrapper
Write decorator loud that prints the returned value before returning it. Apply to add(2,3).

### Task 2 — Timer
Write decorator timer that measures execution time and prints it. Test with a small loop.

### Task 3 — wraps
Write decorator with @wraps(func) and verify func.__name__ is preserved.

### Task 4 — Decorator with argument
Write repeat(times) and apply @repeat(3) to a greeting function.

### Task 5 — Log decorator
Write decorator log that prints "Calling {name} with {args}".

### Task 6 — Only positive
Write decorator check_positive that raises ValueError if any argument < 0.

### Task 7 — Stacking
Apply two decorators to one function (timer and loud) and observe the order of output.
<!--/TASK-->

<!--HINT-->
### Hint 1
Return wrapper(*args, **kwargs).

### Hint 2
Use time.perf_counter() before/after call.

### Hint 3
@wraps(func) inside wrapper definition.

### Hint 4
repeat returns decorator; decorator returns wrapper.

### Hint 5
wrapper logs func.__name__ and args.

### Hint 6
If any(arg < 0 for arg in args): raise ValueError.

### Hint 7
Order: bottom decorator applies first.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
def loud(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"Result: {result}")
        return result
    return wrapper

@loud
def add(a, b):
    return a + b

add(2, 3)   # prints Result: 5
```

### Solution 2
```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"Time: {time.perf_counter() - start:.4f}")
        return result
    return wrapper

@timer
def work():
    return sum(range(1000))

work()
```

### Solution 3
```python
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@timer
def hello():
    "Says hello"
    return "hi"

print(hello.__name__)   # hello
```

### Solution 4
```python
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def greet():
    print("Hi!")

greet()   # three times
```

### Solution 5
```python
def log(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args}")
        return func(*args, **kwargs)
    return wrapper

@log
def add(a, b):
    return a + b

add(1, 2)
```

### Solution 6
```python
def check_positive(func):
    def wrapper(*args, **kwargs):
        if any(arg < 0 for arg in args):
            raise ValueError("Negative argument")
        return func(*args, **kwargs)
    return wrapper

@check_positive
def sqrt_sum(a, b):
    return a ** 0.5 + b ** 0.5
```

### Solution 7
```python
@timer
@loud
def add(a, b):
    return a + b

add(2, 3)
# loud wraps first, then timer wraps loud
```
Bottom decorator is applied first.
<!--/SOLUTION-->

<!--QUIZ-->
What is a decorator?
- A function that wraps another function
- A class
- A module
- A loop
* Correct answer: A function that wraps another function
Returns a new function.

What is @loud equivalent to?
- add = loud(add)
- add = loud
- loud(add) directly
- add()
* Correct answer: add = loud(add)
Decorator sugar.

What is a closure?
- A nested function remembering outer variables
- A list
- A class
- An error
* Correct answer: A nested function remembering outer variables
Captures environment.

What is *args?
- Tuple of positional arguments
- Dict of keywords
- A list
- Nothing
* Correct answer: Tuple of positional arguments
Passes through.

What is **kwargs?
- Dict of keyword arguments
- Tuple
- List
- String
* Correct answer: Dict of keyword arguments
Passes through.

What does @wraps(func) do?
- Keeps name and docstring
- Removes the function
- Adds timing
- Changes args
* Correct answer: Keeps name and docstring
For introspection.

What is a decorator with arguments?
- Function returning a decorator
- A plain decorator
- A class
- A lambda
* Correct answer: Function returning a decorator
@repeat(3).

Why use decorators?
- To add behavior without changing code
- To delete functions
- To speed up
- To create classes
* Correct answer: To add behavior without changing code
Reusable wrappers.

What does wrapper return?
- The result of the original function
- None
- A tuple
- A string
* Correct answer: The result of the original function
It must return the value.

What is the order when stacking?
- Bottom decorator applies first
- Top first
- Random
- Both same
* Correct answer: Bottom decorator applies first
Closest to the function first.

Can a decorator return a class?
- Yes
- No
- Only functions
- Only lambdas
* Correct answer: Yes
Any callable.

What tool helps debug decorated functions?
- @wraps
- print
- type
- len
* Correct answer: @wraps
Keeps original metadata.
<!--/QUIZ-->
