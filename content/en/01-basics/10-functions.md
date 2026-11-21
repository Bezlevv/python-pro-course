---
title: Functions: def, parameters, return
summary: Defining functions, arguments, return values, default parameters and scope.
order: 10
duration: 30 min
difficulty: beginner
tags: functions, def, return, parameters
---

Functions package reusable logic: define once, call many times.

## Define and call

```python
def greet(name):
    return f"Hello, {name}!"

print(greet("Anna"))
```

## Parameters

```python
def add(a, b):
    return a + b

def greet_full(name, greeting="Hi"):
    return f"{greeting}, {name}!"
```

- positional arguments: add(1, 2);
- keyword arguments: add(b=2, a=1);
- default parameters: greeting="Hi".

## return

`return` sends a value back; `return` without value returns None.

## Scope

Variables inside a function are local; to use a global, declare `global`.

## Lesson summary

We learned def, parameters, arguments, return and basics of scope.

<!--TASK-->
### Task 1 — Greet
Write a function greet(name) returning f"Hello, {name}!". Call it for "Anna".

### Task 2 — Add
Write add(a, b) returning the sum. Test with positions и keywords.

### Task 3 — Default parameter
Write repeat(text, times=2) returning text multiplied. Call with and without the second argument.

### Task 4 — Is even
Write is_even(n) returning True for even numbers. Print results for 4 and 7.

### Task 5 — Max of three
Write max3(a, b, c) returning the largest without built-in max.

### Task 6 — Convert
Write to_celsius(f) returning (f - 32) * 5 / 9. Test with 32 and 212.

### Task 7 — Counter
Write a function that prints its call number using a mutable default (call_count=[0]) and returns it.
<!--/TASK-->

<!--HINT-->
### Hint 1
def greet(name): return f"Hello, {name}!"

### Hint 2
Arguments can be passed by position or by name.

### Hint 3
Default values are used when not passed.

### Hint 4
Return n % 2 == 0.

### Hint 5
Compare with if/elif.

### Hint 6
Formula: (f - 32) * 5 / 9.

### Hint 7
def counter(state=[0]): state[0] += 1; return state[0].
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
def greet(name):
    return f"Hello, {name}!"

print(greet("Anna"))   # Hello, Anna!
```

### Solution 2
```python
def add(a, b):
    return a + b

print(add(1, 2))        # 3
print(add(b=2, a=1))    # 3
```

### Solution 3
```python
def repeat(text, times=2):
    return text * times

print(repeat("ab"))        # abab
print(repeat("ab", 3))     # ababab
```

### Solution 4
```python
def is_even(n):
    return n % 2 == 0

print(is_even(4))   # True
print(is_even(7))   # False
```

### Solution 5
```python
def max3(a, b, c):
    if a >= b and a >= c:
        return a
    if b >= c:
        return b
    return c

print(max3(3, 7, 5))   # 7
```

### Solution 6
```python
def to_celsius(f):
    return (f - 32) * 5 / 9

print(to_celsius(32))    # 0.0
print(to_celsius(212))   # 100.0
```

### Solution 7
```python
def counter(state=[0]):
    state[0] += 1
    return state[0]

print(counter())   # 1
print(counter())   # 2
```
Mutable default persists between calls.
<!--/SOLUTION-->

<!--QUIZ-->
What keyword defines a function?
- def
- func
- function
- lambda
* Correct answer: def
Followed by name and parentheses.

What does return do?
- Sends a value back
- Prints it
- Stops the program
- Saves it
* Correct answer: Sends a value back
The caller receives the value.

What if a function has no return?
- It returns None
- Error
- Returns 0
- Returns ""
* Correct answer: It returns None
Default return value.

How to call add(1, 2)?
- add(1, 2)
- add 1 2
- add(1)(2)
- add[1,2]
* Correct answer: add(1, 2)
Arguments in parentheses.

What is a default parameter?
- A value used when not passed
- A required argument
- A keyword
- A type
* Correct answer: A value used when not passed
greeting="Hi".

Which call is keyword-style?
- add(b=2, a=1)
- add(1, 2)
- add((1,2))
- add(1)
* Correct answer: add(b=2, a=1)
Names are given.

What is local scope?
- Variables visible only inside the function
- Global variables
- Module scope
- None
* Correct answer: Variables visible only inside the function
Local by default.

How to read a global variable?
- Declare global or just read it
- Impossible
- Use global in name
- import
* Correct answer: Declare global or just read it
Reading is safe; assignment needs global.

What is f"{name}!" for name="A"?
- "A!"
- 'name!'
- A
- Error
* Correct answer: "A!"
f-string substitution.

What does repeat("x", 3) return if defined as text*times?
- "xxx"
- "x3"
- 3
- "x x x"
* Correct answer: "xxx"
Multiplication repeats the string.

Can a function call another function?
- Yes
- No
- Only builtins
- Only in class
* Correct answer: Yes
Functions are values.

What is the result of max3(1,2,3)?
- 3
- 1
- 2
- None
* Correct answer: 3
The largest argument.
<!--/QUIZ-->
