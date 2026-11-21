---
title: Loops: for and while
summary: Repeating code with for/range, iterating collections, while loops, break/continue.
order: 8
duration: 30 min
difficulty: beginner
tags: loops, for, while, break, continue, range
---

Loops repeat code. `for` is used when you know the number of iterations; `while` — when a condition controls it.

## for with range

```python
for i in range(5):      # 0,1,2,3,4
    print(i)

for i in range(2, 8, 2):  # 2,4,6
    print(i)
```

## Iterating collections

```python
for name in ["Anna", "Boris"]:
    print(name)

for key, value in {"a": 1}.items():
    print(key, value)
```

## while

```python
x = 0
while x < 3:
    print(x)
    x += 1
```

## break and continue

- `break` exits the loop immediately.
- `continue` skips to the next iteration.

```python
for i in range(10):
    if i == 5:
        break
    if i % 2 == 0:
        continue
    print(i)   # 1, 3
```

## Lesson summary

We learned for/range, iterating collections, while loops and the break/continue controls.

<!--TASK-->
### Task 1 — Print 1..10
Using range(1, 11), print the numbers 1..10.

### Task 2 — Sum 1..100
Compute the sum of numbers from 1 to 100 with a for loop; print it (expected 5050).

### Task 3 — Even numbers
Print even numbers from 0 to 20 using range with step.

### Task 4 — while countdown
Print from 5 down to 1 using while, then "Go!".

### Task 5 — Filter with continue
For x in range(10), skip numbers divisible by 3 using continue; print the others.

### Task 6 — Find with break
Loop over a list [4, 8, 15, 16, 23, 42]; break when you find 16 and print its index.

### Task 7 — Table of squares
Print "n: n^2" for n in 1..10 using f-string.
<!--/TASK-->

<!--HINT-->
### Hint 1
range(start, stop) — stop is exclusive.

### Hint 2
total = 0; for i in range(1, 101): total += i.

### Hint 3
range(0, 21, 2).

### Hint 4
Initialize x=5; while x>0: print(x); x -= 1.

### Hint 5
if i % 3 == 0: continue.

### Hint 6
enumerate(lst) gives (index, value).

### Hint 7
print(f"{n}: {n*n}").
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
for i in range(1, 11):
    print(i)
```

### Solution 2
```python
total = 0
for i in range(1, 101):
    total += i
print(total)   # 5050
```

### Solution 3
```python
for i in range(0, 21, 2):
    print(i)
```

### Solution 4
```python
x = 5
while x > 0:
    print(x)
    x -= 1
print("Go!")
```

### Solution 5
```python
for x in range(10):
    if x % 3 == 0:
        continue
    print(x)   # 1,2,4,5,7,8
```

### Solution 6
```python
lst = [4, 8, 15, 16, 23, 42]
for i, v in enumerate(lst):
    if v == 16:
        print(i)   # 3
        break
```

### Solution 7
```python
for n in range(1, 11):
    print(f"{n}: {n * n}")
```
<!--/SOLUTION-->

<!--QUIZ-->
What does range(3) produce?
- 0, 1, 2
- 1, 2, 3
- 0, 1, 2, 3
- 3
* Correct answer: 0, 1, 2
Stop is exclusive.

What is range(1, 5)?
- 1, 2, 3, 4
- 1..5
- 0..4
- 5
* Correct answer: 1, 2, 3, 4
From 1 to 4.

What does range(0, 10, 2) produce?
- 0, 2, 4, 6, 8
- 1, 3, 5, 7, 9
- 0..10
- 2, 4, 6, 8
* Correct answer: 0, 2, 4, 6, 8
Step 2.

Which loop runs while a condition is true?
- while
- for
- if
- range
* Correct answer: while
while condition: block.

What does break do?
- Exits the loop
- Skips one iteration
- Restarts
- Ends the program
* Correct answer: Exits the loop
Immediate exit.

What does continue do?
- Skips to the next iteration
- Exits
- Restarts
- Prints
* Correct answer: Skips to the next iteration
The rest of the body is skipped.

What is the sum 1..100?
- 5050
- 5000
- 100
- 10100
* Correct answer: 5050
Gauss formula.

How to get index in a loop?
- enumerate(lst)
- len(lst)
- for i in lst
- lst.enumerate
* Correct answer: enumerate(lst)
Yields (index, value).

What is while True?
- Infinite loop (usually with break)
- Error
- Runs once
- Nothing
* Correct answer: Infinite loop (usually with break)
Break inside stops it.

How to print 1..10?
- range(1, 11)
- range(1, 10)
- range(10)
- range(11)
* Correct answer: range(1, 11)
Stop exclusive → 11.

What will `for i in range(5): print(i)` print?
- 0 1 2 3 4
- 1 2 3 4 5
- 0..5
- 5
* Correct answer: 0 1 2 3 4
Starts at 0.

What is wrong with `while x < 3:` without x change?
- Infinite loop
- Error
- Nothing
- Prints once
* Correct answer: Infinite loop
x never changes.
<!--/QUIZ-->
