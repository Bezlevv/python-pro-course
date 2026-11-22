---
title: Algorithms and complexity
summary: Big O, common complexities, sorting/searching basics.
order: 5
duration: 45 min
difficulty: advanced
tags: algorithms, big o, complexity
---

Understanding complexity picks the right approach.

## Big O

Describes growth: O(1), O(log n), O(n), O(n log n), O(n²).

## Examples

```python
# O(1)
def first(lst):
    return lst[0]

# O(n)
def total(lst):
    return sum(lst)

# O(n²)
def pairs(lst):
    for i in lst:
        for j in lst:
            print(i, j)
```

## Binary search: O(log n)

```python
def binary_search(lst, target):
    lo, hi = 0, len(lst) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if lst[mid] == target:
            return mid
        if lst[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

## Lesson summary

Estimate growth to choose algorithms and data structures.

<!--TASK-->
### Task 1 — O(1)
Write an O(1) function.

### Task 2 — O(n)
Write an O(n) loop.

### Task 3 — O(n²)
Write a nested loop.

### Task 4 — log n
Implement binary search.

### Task 5 — Compare
Compare linear and binary search on sorted data.

### Task 6 — Sort complexity
State the complexity of sorted().

### Task 7 — Choose
Which data structure for fast lookup?
<!--/TASK-->

<!--HINT-->
### Hint 1
return lst[0].

### Hint 2
sum or loop.

### Hint 3
Nested.

### Hint 4
Halving.

### Hint 5
Timing.

### Hint 6
O(n log n).

### Hint 7
dict/set.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
def first(lst):
    return lst[0]
# O(1)
```

### Solution 2
```python
def total(lst):
    s = 0
    for x in lst:
        s += x
    return s
# O(n)
```

### Solution 3
```python
def pairs(lst):
    for i in lst:
        for j in lst:
            print(i, j)
# O(n²)
```

### Solution 4
```python
def binary_search(lst, target):
    lo, hi = 0, len(lst) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if lst[mid] == target:
            return mid
        if lst[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

### Solution 5
```python
import time
data = list(range(10_000_000))
start = time.perf_counter()
# линейный поиск: target in data
# бинарный: binary_search(data, target)
print(time.perf_counter() - start)
```

### Solution 6
```python
# sorted() — O(n log n)
```

### Solution 7
```python
# dict/set: O(1) в среднем
# список: O(n)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is Big O?
- Growth rate
- Speed
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

What is O(n²)?
- Nested loops
- One loop
- Constant
- None
* Correct answer: Nested loops
Square.

What is O(log n)?
- Halving
- Linear
- Constant
- None
* Correct answer: Halving
Binary search.

What is sorted() complexity?
- O(n log n)
- O(n)
- O(n²)
- O(1)
* Correct answer: O(n log n)
Good.

Which is fastest for lookup?
- dict
- list
- tuple
- str
* Correct answer: dict
O(1).

What is binary search prerequisite?
- Sorted data
- Any
- Unique
- None
* Correct answer: Sorted data
Order.

Why complexity matters?
- Scale
- Style
- Name
- None
* Correct answer: Scale
Performance.

What is an algorithm?
- Steps to solve
- A library
- A class
- None
* Correct answer: Steps to solve
Procedure.

What is worst case?
- Max time
- Min
- Average
- None
* Correct answer: Max time
Bound.

What is amortized?
- Average over ops
- Worst
- Best
- None
* Correct answer: Average over ops
e.g., list.append.
<!--/QUIZ-->
