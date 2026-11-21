---
title: Conditional statements: if/elif/else
summary: Making decisions in code, elif chains, nesting and bool conversions.
order: 5
duration: 30 min
difficulty: beginner
tags: if, elif, else, conditions
---

Programs make decisions all the time. The `if` statement executes a block only when a condition is true.

## Basic if

```python
age = 18
if age >= 18:
    print("You are an adult")
```

## if/else

```python
if age >= 18:
    print("Adult")
else:
    print("Minor")
```

## elif chain

```python
score = 75
if score >= 90:
    print("A")
elif score >= 75:
    print("B")
elif score >= 60:
    print("C")
else:
    print("F")
```

## Indentation matters

The block must be indented (4 spaces by convention). Python reads indentation as structure.

## Truthiness

Many values are truthy/falsy: 0, "", [], None are falsy; everything else is truthy.

## Lesson summary

We learned if/elif/else, how indentation defines blocks, and truthiness.

<!--TASK-->
### Task 1 — Adult check
Read age; print "Adult" if age >= 18, otherwise "Minor".

### Task 2 — Even/odd
Read n; print "even" if n % 2 == 0 else "odd".

### Task 3 — Grade
Given score, print A/B/C/F using elif chain (90/75/60 thresholds).

### Task 4 — Max of two
Read a and b; print the maximum without using max().

### Task 5 — Falsy check
Print what is truthy among: 0, 1, "", "a", [], [1], None.

### Task 6 — Nested conditions
Read x and y; print which quadrant (x>0,y>0 → 1; x<0,y>0 → 2; x<0,y<0 → 3; x>0,y<0 → 4; axes → "axis").

### Task 7 — Leap year
Read year; print "leap" if divisible by 4 but not by 100, or divisible by 400.
<!--/TASK-->

<!--HINT-->
### Hint 1
Compare with >=; else covers the rest.

### Hint 2
n % 2 == 0 checks parity.

### Hint 3
Check from the highest threshold down.

### Hint 4
Use if a > b: print(a) else print(b).

### Hint 5
Use bool(value) to see truthiness.

### Hint 6
Check signs with and; handle zero separately.

### Hint 7
Leap rule: (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0).
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
age = int(input("Age: "))
if age >= 18:
    print("Adult")
else:
    print("Minor")
```

### Solution 2
```python
n = int(input("n: "))
if n % 2 == 0:
    print("even")
else:
    print("odd")
```

### Solution 3
```python
score = int(input("Score: "))
if score >= 90:
    print("A")
elif score >= 75:
    print("B")
elif score >= 60:
    print("C")
else:
    print("F")
```

### Solution 4
```python
a = int(input("a: "))
b = int(input("b: "))
if a > b:
    print(a)
else:
    print(b)
```

### Solution 5
```python
for v in [0, 1, "", "a", [], [1], None]:
    print(repr(v), bool(v))
```
Only 0, "", [], None are False.

### Solution 6
```python
x = float(input("x: "))
y = float(input("y: "))
if x > 0 and y > 0:
    print(1)
elif x < 0 and y > 0:
    print(2)
elif x < 0 and y < 0:
    print(3)
elif x > 0 and y < 0:
    print(4)
else:
    print("axis")
```

### Solution 7
```python
y = int(input("Year: "))
if (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0):
    print("leap")
else:
    print("not leap")
```
<!--/SOLUTION-->

<!--QUIZ-->
What executes when if is False?
- The else block (if present)
- Nothing ever
- The next module
- The if block anyway
* Correct answer: The else block (if present)
else is the fallback.

Which keyword adds another condition?
- elif
- elseif
- else if
- when
* Correct answer: elif
elif chains multiple conditions.

How to check even number?
- n % 2 == 0
- n / 2
- n * 2
- n == 2
* Correct answer: n % 2 == 0
Remainder zero.

What is falsy?
- 0
- 1
- "0"
- [1]
* Correct answer: 0
Zero is falsy.

Is "" truthy?
- No
- Yes
- Depends
- Error
* Correct answer: No
Empty string is falsy.

What does indentation do?
- Defines the block
- Nothing
- Slows code
- Renames variables
* Correct answer: Defines the block
Python uses indentation as structure.

What is printed for score=80 in A/B/C/F chain?
- B
- A
- C
- F
* Correct answer: B
80 >= 75 → B.

Nested if means:
- An if inside an if
- An if without else
- Two independent ifs
- An elif
* Correct answer: An if inside an if
Conditions inside conditions.

Leap year 2024?
- Yes
- No
- Error
- Unknown
* Correct answer: Yes
Divisible by 4 and not by 100.

When to use elif instead of several ifs?
- When conditions are exclusive
- Always
- Never
- Only for numbers
* Correct answer: When conditions are exclusive
elif stops after first True.
<!--/QUIZ-->
