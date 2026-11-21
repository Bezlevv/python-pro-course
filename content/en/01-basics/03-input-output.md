---
title: Input, Output and f-strings
summary: input(), print(), f-strings, formatting numbers and building readable messages.
order: 3
duration: 25 min
difficulty: beginner
tags: input, print, f-strings, formatting
---

A program is a dialogue with the user: you ask, read input, process, and show the result.

## Reading input

```python
name = input("What is your name? ")
print("Hello,", name)
```

`input()` always returns a string. To get a number, convert it:

```python
age = int(input("How old are you? "))
```

## f-strings

f-strings allow inserting values right into a string:

```python
name = "Anna"
age = 21
print(f"Hello, {name}! You are {age}.")
```

You can put expressions inside braces:

```python
print(f"In 5 years you will be {age + 5}.")
```

## Formatting numbers

```python
price = 19.99
print(f"Price: {price:.2f}")   # 19.99
print(f"Percent: {0.25:.0%}")  # 25%
```

## Lesson summary

We learned to read user input with `input()`, convert it, build strings with f-strings, and format numbers nicely.

<!--TASK-->
### Task 1 — Greeting
Ask for the user's name and print `Hello, <name>!`.

### Task 2 — Age
Ask for age, convert to int, and print `Next year you will be <age+1>.`

### Task 3 — Sum of two numbers
Read two numbers (int), print their sum and product.

### Task 4 — f-string with expression
Given `a = 7`, print `f"Square of {a} is {a*a}"` — result: Square of 7 is 49.

### Task 5 — Curiosity
Read a number, print `f"You entered {n}; double is {n*2}"`.

### Task 6 — Formatting
Print the number 1234.5678 with `:.2f`, `:,.0f`, and `:.1e`. Explain each result.

### Task 7 — Full dialogue
Ask for name, city, and birth year; print a single f-string with all the data.
<!--/TASK-->

<!--HINT-->
### Hint 1
`input("...")` shows the prompt and waits for a line.

### Hint 2
Wrap `input()` with `int(...)` to get a number.

### Hint 3
Separate the two numbers with spaces or read them in separate calls.

### Hint 4
Expressions inside `{}` are evaluated.

### Hint 5
Store the number, then use it in the f-string.

### Hint 6
`:,.0f` adds thousands separators; `:.1e` uses scientific notation.

### Hint 7
Combine everything into one f-string.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
name = input("What is your name? ")
print(f"Hello, {name}!")
```

### Solution 2
```python
age = int(input("How old are you? "))
print(f"Next year you will be {age + 1}.")
```

### Solution 3
```python
a = int(input("First number: "))
b = int(input("Second number: "))
print(f"Sum: {a + b}, product: {a * b}")
```

### Solution 4
```python
a = 7
print(f"Square of {a} is {a * a}")
```
Output: Square of 7 is 49.

### Solution 5
```python
n = int(input("Enter a number: "))
print(f"You entered {n}; double is {n * 2}")
```

### Solution 6
```python
x = 1234.5678
print(f"{x:.2f}")   # 1234.57
print(f"{x:,.0f}")  # 1,235
print(f"{x:.1e}")   # 1.2e+03
```
Formats: two decimals, thousands separator, scientific notation.

### Solution 7
```python
name = input("Name: ")
city = input("City: ")
year = int(input("Birth year: "))
print(f"{name} from {city}, born in {year}.")
```
One f-string shows all the data.
<!--/SOLUTION-->

<!--QUIZ-->
What does input() do?
- Reads a line from the user
- Prints to screen
- Opens a file
- Returns a number always
* Correct answer: Reads a line from the user
It returns a string.

What type does input() return?
- str
- int
- float
- list
* Correct answer: str
Convert it if you need a number.

How to read an integer?
- int(input("..."))
- input(int("..."))
- str(input())
- number(input())
* Correct answer: int(input("..."))
Wraps the string with int().

What is an f-string?
- A string with inserted values: f"Hello, {name}"
- A formatted file
- A function
- A number
* Correct answer: A string with inserted values
Braces evaluate expressions.

What prints f"Square of {a} is {a*a}" for a=7?
- Square of 7 is 49
- Square of a is 49
- 7 is 49
- Error
* Correct answer: Square of 7 is 49
Both {a} and {a*a} are evaluated.

What does :.2f do?
- Formats with 2 decimal places
- Rounds to integer
- Converts to string
- Adds percent
* Correct answer: Formats with 2 decimal places
Example: 19.999 → 20.00.

Which format adds thousands separators?
- :,.0f
- :.2f
- :e
- :d
* Correct answer: :,.0f
Example: 1234567 → 1,234,567.

Can you put expressions inside f-string braces?
- Yes
- No
- Only variables
- Only numbers
* Correct answer: Yes
Any Python expression works.

What happens if you input "abc" and convert with int()?
- ValueError
- 0
- Nothing
- "abc"
* Correct answer: ValueError
The string is not a number.

How to print a greeting with a variable name?
- print(f"Hello, {name}!")
- print("Hello, {name}!")
- print(f"Hello, name!")
- print("Hello", {name})
* Correct answer: print(f"Hello, {name}!")
f-strings insert the variable.

Which is correct to read a float?
- float(input("..."))
- int(input("..."))
- str(input("..."))
- input(float("..."))
* Correct answer: float(input("..."))
Converts to a floating-point number.

What does f"{"x":.1e}" produce for x=1234.5?
- 1.2e+03
- 1234.5
- 1.2
- Error
* Correct answer: 1.2e+03
Scientific notation with one decimal.
<!--/QUIZ-->
