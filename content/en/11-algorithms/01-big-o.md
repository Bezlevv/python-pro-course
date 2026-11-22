---
title: Complexity: Big O notation
summary: Growth rates, best/worst case, analysis examples.
order: 1
duration: 40 min
difficulty: intermediate
tags: big o, complexity
---

Big O describes how runtime grows with input size.

## Common classes

- O(1): constant;
- O(log n): halving (binary search);
- O(n): single loop;
- O(n log n): good sorting;
- O(n²): nested loops.

## Examples

```python
def first(xs):       # O(1)
    return xs[0]

def total(xs):        # O(n)
    s = 0
    for x in xs:
        s += x
    return s

def find(xs, t):      # O(n)
    for x in xs:
        if x == t:
            return True
    return False
```

## Dropping constants

O(2n) → O(n); O(n² + n) → O(n²).

## Lesson summary

Estimate complexity by loops and data access.

<!--TASK-->
### Task 1 — Constant
Write an O(1) operation.

### Task 2 — Linear
Write an O(n) loop.

### Task 3 — Nested
Write O(n²).

### Task 4 — Simplify
Simplify O(3n) to O(n).

### Task 5 — Log
Describe why binary search is O(log n).

### Task 6 — Sort
State complexity of sorted().

### Task 7 — Choose
Pick a dict vs list for membership.
<!--/TASK-->

<!--HINT-->
### Hint 1
xs[0].

### Hint 2
Loop.

### Hint 3
Nested.

### Hint 4
Remove constants.

### Hint 5
Halving.

### Hint 6
O(n log n).

### Hint 7
dict.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
def first(xs):
    return xs[0]
```

### Solution 2
```python
def total(xs):
    s = 0
    for x in xs:
        s += x
    return s
```

### Solution 3
```python
def pairs(xs):
    for i in xs:
        for j in xs:
            print(i, j)
```

### Solution 4
```python
# O(3n) → O(n)
# Константы не влияют на асимптотику
```

### Solution 5
```python
# Каждый шаг отбрасывает половину:
# log2(n) шагов
```

### Solution 6
```python
# sorted() — O(n log n)
```

### Solution 7
```python
# dict/set: O(1) в среднем
# list: O(n)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is Big O?
- Growth rate
- Exact time
- Memory
- None
* Correct answer: Growth rate
Asymptotic.

What is O(1)?
- Constant
- Linear
- Log
- Square
* Correct answer: Constant
Independent.

What is O(n)?
- Linear
- Constant
- Log
- None
* Correct answer: Linear
One pass.

What is O(log n)?
- Halving
- Linear
- Square
- None
* Correct answer: Halving
Search.

What is O(n log n)?
- Merge sort
- Bubble
- Linear
- None
* Correct answer: Merge sort
Efficient.

What is O(n²)?
- Nested loops
- One loop
- Constant
- None
* Correct answer: Nested loops
Square.

Can we drop constants?
- Yes
- No
- Sometimes
- Never
* Correct answer: Yes
Asymptotic.

What is worst case?
- Slowest input
- Fastest
- Average
- None
* Correct answer: Slowest input
Bound.

What is best case?
- Fastest input
- Slowest
- Average
- None
* Correct answer: Fastest input
Minimum.

What is average case?
- Typical
- Worst
- Best
- None
* Correct answer: Typical
Middle.

What is space complexity?
- Memory usage
- Time
- Input
- None
* Correct answer: Memory usage
Extra.

Which is faster: dict lookup or list scan?
- dict
- list
- Equal
- None
* Correct answer: dict
O(1).
<!--/QUIZ-->
