---
title: Exam: Python Basics
summary: Test your knowledge of Python basics: variables, data types, operators, conditions, loops, collections, functions, errors, files and modules.
order: 99
duration: 30 min
difficulty: advanced
tags: exam
exam: true
---

<!--QUIZ-->
What type does the expression 3.14 have?
- int
- float
- complex
- Decimal
* Correct answer: float
Any number with a decimal point in Python has type float.

What does print(7 // 2) output?
- 3.5
- 3
- 4
- Error
* Correct answer: 3
The // operator performs integer division and discards the fractional part.

How do you check that two variables a and b are equal?
- a = b
- a == b
- a is equal b
- a.equals(b)
* Correct answer: a == b
The == operator compares values, while = assigns a value to a variable.

How do you turn the string "42" into the number 42?
- number("42")
- int("42")
- str(42)
- cast("42")
* Correct answer: int("42")
The int() function converts a string into an integer.

What does print(len([10, 20, 30])) output?
- 3
- 10
- 30
- Error
* Correct answer: 3
The len() function returns the number of items in a collection.

Which loop prints the numbers 0, 1, 2?
- for i in range(3): print(i)
- for i in range(1, 3): print(i)
- for i in [3]: print(i)
- for i in range(4): print(i)
* Correct answer: for i in range(3): print(i)
range(3) generates the numbers 0, 1, 2 — the third element of range is not included.

How do you add an item to the end of a list?
- list.push(item)
- list.append(item)
- list.add(item)
- list.insert_end(item)
* Correct answer: list.append(item)
The append() method adds an item to the end of a list.

How do you declare a function that takes an argument x?
- function f(x): ...
- def f(x): ...
- define f(x): ...
- fn f(x): ...
* Correct answer: def f(x): ...
Functions are declared with the keyword def, followed by the name and parameters in parentheses.

Which block catches errors when code runs?
- catch / except
- try / except
- throw / catch
- handle / error
* Correct answer: try / except
Code inside try is executed, and if an exception occurs, control passes to the except block.

Which way of opening a file guarantees it gets closed?
- f = open("data.txt"); ...
- with open("data.txt") as f: ...
- open("data.txt", "auto"); ...
- file = read("data.txt"); ...
* Correct answer: with open("data.txt") as f: ...
The with context manager closes the file itself after the block runs, even if an error occurs.
<!--/QUIZ-->
