---
title: Operators: arithmetic, comparison, logic
summary: Arithmetic operators, comparisons, logical operators and precedence.
order: 4
duration: 25 min
difficulty: beginner
tags: operators, arithmetic, comparison, boolean
---

Operators are the "verbs" of programming: they combine values and produce new ones.

## Arithmetic operators

```python
print(2 + 3)    # 5 addition
print(7 - 2)    # 5 subtraction
print(4 * 3)    # 12 multiplication
print(8 / 2)    # 4.0 division (always float)
print(8 // 3)   # 2 integer division
print(8 % 3)    # 2 remainder
print(2 ** 3)   # 8 exponent
```

## Comparison operators

`==`, `!=`, `<`, `>`, `<=`, `>=` return booleans:

```python
print(3 > 2)   # True
print(3 == 4)  # False
```

## Logical operators

`and`, `or`, `not` work with booleans:

```python
print(True and False)  # False
print(True or False)   # True
print(not True)        # False
```

## Precedence

Order (from high to low): `**`, `* / // %`, `+ -`, comparisons, `not`, `and`, `or`. Parentheses override it.

## Lesson summary

We learned the arithmetic, comparison and logical operators, and the rules of precedence.

<!--TASK-->
### Task 1 — Arithmetic
Compute and print: 17+4, 17-4, 17*4, 17/4, 17//4, 17%4, 2**10.

### Task 2 — Integer division and remainder
For a=17, b=5 print the quotient and the remainder. Show that a == (a//b)*b + a%b.

### Task 3 — Comparisons
Print the results of 10 > 5, 10 == 10, 10 != 9, 10 <= 10.

### Task 4 — Combining booleans
For x=7 print: x > 3 and x < 10; x == 5 or x == 7; not (x == 5).

### Task 5 — Precedence check
Predict then print: 2 + 3 * 4 (14), (2 + 3) * 4 (20), 2 ** 3 ** 2 (512).

### Task 6 — Reading numbers and comparing
Read two numbers from the user, print which is greater and whether they are equal.

### Task 7 — Divisibility
Read n; print whether n is divisible by 3 (n % 3 == 0).
<!--/TASK-->

<!--HINT-->
### Hint 1
Use one print per operation or several values in one print.

### Hint 2
Integer division discards the remainder; % gives the remainder.

### Hint 3
Comparisons always return True/False.

### Hint 4
and is true only if both are true; or — if at least one.

### Hint 5
Exponentiation is right-associative: 2 ** 3 ** 2 = 2 ** (3 ** 2).

### Hint 6
input() returns a string — convert with int().

### Hint 7
n % 3 == 0 checks divisibility by 3.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
print(17 + 4)  # 21
print(17 - 4)  # 13
print(17 * 4)  # 68
print(17 / 4)  # 4.25
print(17 // 4) # 4
print(17 % 4)  # 1
print(2 ** 10) # 1024
```

### Solution 2
```python
a, b = 17, 5
q, r = a // b, a % b
print(q, r)                # 3 2
print(a == q * b + r)      # True
```

### Solution 3
```python
print(10 > 5)    # True
print(10 == 10)  # True
print(10 != 9)   # True
print(10 <= 10)  # True
```

### Solution 4
```python
x = 7
print(x > 3 and x < 10)  # True
print(x == 5 or x == 7)  # True
print(not (x == 5))      # True
```

### Solution 5
```python
print(2 + 3 * 4)    # 14
print((2 + 3) * 4)  # 20
print(2 ** 3 ** 2)  # 512
```
Precedence: * binds stronger than +; ** is right-associative.

### Solution 6
```python
a = int(input("First: "))
b = int(input("Second: "))
print(a > b, a < b, a == b)
```

### Solution 7
```python
n = int(input("n: "))
print(n % 3 == 0)
```
True if n is divisible by 3.
<!--/SOLUTION-->

<!--QUIZ-->
What is 8 / 2?
- 4.0
- 4
- 2
- 16
* Correct answer: 4.0
Division always returns a float.

What is 8 // 3?
- 2
- 2.66
- 3
- 24
* Correct answer: 2
Integer division truncates.

What is 8 % 3?
- 2
- 3
- 5
- 1
* Correct answer: 2
Remainder of 8 / 3.

What is 2 ** 5?
- 32
- 25
- 10
- 7
* Correct answer: 32
Exponentiation.

Which operator checks equality?
- ==
- =
- !=
- is
* Correct answer: ==
== compares values.

What does 10 > 5 return?
- True
- False
- 1
- 10
* Correct answer: True
Comparison returns a boolean.

What is True and False?
- False
- True
- 0
- Error
* Correct answer: False
and is true only if both are true.

What is True or False?
- True
- False
- 1
- Error
* Correct answer: True
or is true if at least one is true.

What does not True return?
- False
- True
- 0
- None
* Correct answer: False
not negates the boolean.

What is 2 + 3 * 4?
- 14
- 20
- 9
- 24
* Correct answer: 14
* has higher precedence than +.

What is (2 + 3) * 4?
- 20
- 14
- 9
- 24
* Correct answer: 20
Parentheses override precedence.

How to check divisibility by 3?
- n % 3 == 0
- n / 3
- n // 3
- n * 3
* Correct answer: n % 3 == 0
No remainder means divisible.
<!--/QUIZ-->
