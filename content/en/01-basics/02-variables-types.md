---
title: Variables and Data Types
summary: What a variable is, numbers, strings, booleans, type() and naming rules.
order: 2
duration: 25 min
difficulty: beginner
tags: variables, types, int, float, str, bool
---

Variables are "boxes" with names in which you store values. Python does not require declaring a type — the type is determined by the value.

## What is a variable

```python
name = "Anna"
age = 21
height = 1.68
is_student = True
```

Rules for names: letters, digits, underscores; cannot start with a digit; cannot contain spaces or hyphens.

## Basic types

- `int` — integers: `42`, `-7`;
- `float` — floating-point numbers: `3.14`, `0.5`;
- `str` — strings: `"hello"`, `'world'`;
- `bool` — booleans: `True`, `False`.

```python
print(type(42))        # <class 'int'>
print(type(3.14))      # <class 'float'>
print(type("hi"))      # <class 'str'>
print(type(True))      # <class 'bool'>
```

## Dynamic typing

You can assign a value of another type to the same variable later:

```python
x = 10
x = "now a string"
```

Python allows it, but it is good practice to keep one type per variable.

## Type conversion

```python
int("42")       # 42
float("3.5")    # 3.5
str(42)         # "42"
bool("")        # False — empty string
```

## Lesson summary

We learned what variables are, naming rules, main types (`int`, `float`, `str`, `bool`), how to check a type with `type()`, and how to convert values.

<!--TASK-->
### Task 1 — Create variables
Create variables: `city = "Moscow"`, `population = 12_000_000`, `area = 2511.0`, `is_capital = True`. Print each with `print()`.

### Task 2 — Types
Print the type of each variable from Task 1 using `type()`. Expected: str, int, float, bool.

### Task 3 — Arithmetic
Given `a = 10` and `b = 3`, print `a + b`, `a - b`, `a * b`, `a / b`, `a // b`, `a % b`, `a ** b`.

### Task 4 — String operations
Create `s = "Python"`. Print `len(s)`, `s.upper()`, `s.lower()`, `s[0]`, `s[-1]`.

### Task 5 — Conversion
Convert: `int("15") + 5`, `float("2.5") * 2`, `str(100) + "!"`. Print the results and their types.

### Task 6 — Boolean logic
For `age = 18`, print whether `age >= 18` and `age < 65`. Explain what bool values are returned.

### Task 7 — Swap
Given `x = 1`, `y = 2`, swap their values and print them (x=2, y=1).
<!--/TASK-->

<!--HINT-->
### Hint 1
Use underscores in large numbers: `12_000_000` is readable and equals 12000000.

### Hint 2
Call `type(variable)` inside `print()`.

### Hint 3
`//` is integer division, `%` is remainder, `**` is power.

### Hint 4
`len()` returns length, `str[index]` accesses characters.

### Hint 5
`int("15")` converts the string to the number 15.

### Hint 6
Comparisons return booleans.

### Hint 7
Use a temporary variable: `tmp = x; x = y; y = tmp`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
city = "Moscow"
population = 12_000_000
area = 2511.0
is_capital = True
print(city, population, area, is_capital)
```

### Solution 2
```python
print(type(city), type(population), type(area), type(is_capital))
```
Output: `<class 'str'> <class 'int'> <class 'float'> <class 'bool'>`.

### Solution 3
```python
a, b = 10, 3
print(a + b)   # 13
print(a - b)   # 7
print(a * b)   # 30
print(a / b)   # 3.333...
print(a // b)  # 3
print(a % b)   # 1
print(a ** b)  # 1000
```

### Solution 4
```python
s = "Python"
print(len(s))     # 6
print(s.upper())  # PYTHON
print(s.lower())  # python
print(s[0])       # P
print(s[-1])      # n
```

### Solution 5
```python
print(int("15") + 5)          # 20
print(float("2.5") * 2)       # 5.0
print(str(100) + "!")         # 100!
```

### Solution 6
```python
age = 18
print(age >= 18)   # True
print(age < 65)    # True
```
Comparison operators return booleans.

### Solution 7
```python
x, y = 1, 2
tmp = x
x = y
y = tmp
print(x, y)  # 2 1
```
A temporary variable swaps the values.
<!--/SOLUTION-->

<!--QUIZ-->
What is a variable?
- A named container for a value
- A file
- A comment
- A function
* Correct answer: A named container for a value
You can store data in it.

Which name is valid in Python?
- my_name
- 2name
- my-name
- my name
* Correct answer: my_name
Names cannot start with a digit or contain a hyphen/space.

What is the type of 3.14?
- float
- int
- str
- bool
* Correct answer: float
A number with a decimal point.

What does type(True) return?
- <class 'bool'>
- True
- <class 'int'>
- boolean
* Correct answer: <class 'bool'>
True is a boolean value.

What is the result of int("42")?
- 42
- "42"
- Error
- 42.0
* Correct answer: 42
Converts the string to an integer.

What does len("Python") return?
- 6
- 5
- P
- Error
* Correct answer: 6
The string has 6 characters.

What does s.upper() do?
- Returns the string in uppercase
- Makes it lowercase
- Deletes it
- Sorts it
* Correct answer: Returns the string in uppercase
Method of str.

What is the result of 7 // 2?
- 3
- 3.5
- 1
- 4
* Correct answer: 3
Integer division discards the fractional part.

What is 7 % 2?
- 1
- 3
- 0.5
- 2
* Correct answer: 1
The remainder of division.

Which value converts to False with bool()?
- ""
- "0"
- 1
- "False"
* Correct answer: ""
Empty strings are falsy.

How to swap two variables?
- Use a temporary variable
- Swap names
- Delete both
- Not possible
* Correct answer: Use a temporary variable
tmp = x; x = y; y = tmp.

Can a variable change its type?
- Yes, Python is dynamically typed
- No, never
- Only in classes
- Only for numbers
* Correct answer: Yes, Python is dynamically typed
The type follows the assigned value.
<!--/QUIZ-->
