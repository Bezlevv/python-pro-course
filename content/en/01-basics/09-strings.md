---
title: Strings in depth
summary: Methods, slicing, formatting, f-strings and common string operations.
order: 9
duration: 35 min
difficulty: beginner
tags: strings, methods, format, f-string
---

Strings are everywhere. Python gives you rich methods to work with them.

## Creating and basics

```python
s = "Hello, Python"
print(len(s))        # 13
print(s[0], s[-1])   # H n
```

## Methods

```python
s.upper()       # HELLO, PYTHON
s.lower()       # hello, python
s.strip()       # removes outer spaces
s.split(",")    # ['Hello', ' Python']
", ".join(["a", "b"])   # "a, b"
s.replace("Python", "World")
s.startswith("Hello")   # True
s.find("Python")        # index or -1
```

## Slicing

```python
s[0:5]   # Hello
s[-6:]   # Python
s[::2]   # every second char
```

## f-strings

```python
name = "Anna"
age = 21
print(f"{name} is {age} years old")
```

## Membership

```python
"Python" in s   # True
```

## Lesson summary

We learned string methods, slicing, membership and f-string formatting.

<!--TASK-->
### Task 1 — Basics
Create s=" Hello, Python ". Print its length, s[0] and s[-1].

### Task 2 — Case methods
Print s.upper(), s.lower(), s.title() and s.capitalize().

### Task 3 — Split and join
Split "apple,banana,cherry" by comma into a list; then join the list with " | ".

### Task 4 — Replace and strip
From "  Hello World  " strip spaces, replace "World" with "Python", print result.

### Task 5 — Slices
For "Python Programming" print first 6 chars, last 11 chars, and every second char.

### Task 6 — Check methods
Test startswith("Py"), endswith("ing"), isdigit() on "123", isalpha() on "abc".

### Task 7 — f-string table
For names ["Anna", "Boris"] and ages [21, 30], print rows like "Anna: 21".
<!--/TASK-->

<!--HINT-->
### Hint 1
Index 0 is first, -1 is last.

### Hint 2
title() capitalizes each word; capitalize() only the first.

### Hint 3
split returns a list; join concatenates.

### Hint 4
strip() removes spaces at both ends.

### Hint 5
Slices use [start:stop:step].

### Hint 6
Check methods return booleans.

### Hint 7
Loop with zip(names, ages) and f-string.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
s = " Hello, Python "
print(len(s))    # 15
print(s[0])      # ' '
print(s[-1])     # ' '
```

### Solution 2
```python
print(s.upper())       #  HELLO, PYTHON 
print(s.lower())       #  hello, python 
print("hello world".title())       # Hello World
print("hello".capitalize())        # Hello
```

### Solution 3
```python
fruits = "apple,banana,cherry".split(",")
print(fruits)                 # ['apple', 'banana', 'cherry']
print(" | ".join(fruits))     # apple | banana | cherry
```

### Solution 4
```python
t = "  Hello World  "
print(t.strip().replace("World", "Python"))   # Hello Python
```

### Solution 5
```python
s = "Python Programming"
print(s[:6])     # Python
print(s[-11:])   # Programming
print(s[::2])    # Pto rgamn
```

### Solution 6
```python
print("Python".startswith("Py"))   # True
print("Programming".endswith("ing"))  # True
print("123".isdigit())            # True
print("abc".isalpha())            # True
```

### Solution 7
```python
for name, age in zip(["Anna", "Boris"], [21, 30]):
    print(f"{name}: {age}")
```
<!--/SOLUTION-->

<!--QUIZ-->
What is len("Python")?
- 6
- 5
- 7
- 0
* Correct answer: 6
Number of characters.

What does s.upper() return?
- Uppercase copy
- Lowercase
- Same string
- Title case
* Correct answer: Uppercase copy
Methods return new strings.

What does "a,b".split(",") return?
- ['a', 'b']
- 'a b'
- 'a,b'
- ('a', 'b')
* Correct answer: ['a', 'b']
Separates by delimiter.

What does " ".join(["x","y"]) return?
- "x y"
- ['x','y']
- "xy"
- "x,y"
* Correct answer: "x y"
Join concatenates with separator.

What does "  hi  ".strip() return?
- "hi"
- "  hi"
- "hi  "
- " h i "
* Correct answer: "hi"
Removes outer whitespace.

What does "abc".replace("b", "X") return?
- "aXc"
- "abc"
- "Xbc"
- "abX"
* Correct answer: "aXc"
Replaces all occurrences.

What is "Hello"[-1]?
- "o"
- "H"
- "e"
- "l"
* Correct answer: "o"
Last character.

What is "Python"[0:3]?
- "Pyt"
- "Pyth"
- "yth"
- "P"
* Correct answer: "Pyt"
Slice from 0 to 2.

What does "Py".startswith("P") return?
- True
- False
- Error
- None
* Correct answer: True
Checks prefix.

What does "123".isdigit() return?
- True
- False
- "123" with- None
* Correct answer: True
All chars are digits.

What is f"{x}!" for x=5?
- "5!"
- "x!"
- 5
- Error
* Correct answer: "5!"
f-string inserts value.

What is "Python" % "th"?
- 2
- 5
- 1
- -1
* Correct answer: 2
First occurrence index.
<!--/QUIZ-->
