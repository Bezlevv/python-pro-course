---
title: Search: linear and binary
summary: Linear scan, binary search, complexity, boundaries.
order: 3
duration: 40 min
difficulty: intermediate
tags: search, binary search
---

Searching finds an element in a collection.

## Linear search

```python
def linear_search(arr, target):
    for i, x in enumerate(arr):
        if x == target:
            return i
    return -1
```

O(n) — works on any list.

## Binary search

```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

O(log n) — requires sorted data.

## Lesson summary

Linear is simple; binary is fast on sorted data.

<!--TASK-->
### Task 1 — Linear
Implement linear search.

### Task 2 — Binary
Implement binary search.

### Task 3 — Test
Test both on [1,3,5,7].

### Task 4 — Not found
Return -1 for missing.

### Task 5 — Compare
Time both on 1M items.

### Task 6 — Requirement
Explain why binary needs sorted.

### Task 7 — Bisect
Use bisect module.
<!--/TASK-->

<!--HINT-->
### Hint 1
enumerate.

### Hint 2
Halving.

### Hint 3
5 → index 2.

### Hint 4
-1.

### Hint 5
perf_counter.

### Hint 6
Order.

### Hint 7
bisect_left.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
def linear_search(arr, target):
    for i, x in enumerate(arr):
        if x == target:
            return i
    return -1
```

### Solution 2
```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

### Solution 3
```python
arr = [1, 3, 5, 7]
print(linear_search(arr, 5))   # 2
print(binary_search(arr, 5))   # 2
```

### Solution 4
```python
print(binary_search(arr, 4))   # -1
```

### Solution 5
```python
import time
data = list(range(1_000_000))
start = time.perf_counter(); linear_search(data, 999_999); print(time.perf_counter() - start)
start = time.perf_counter(); binary_search(data, 999_999); print(time.perf_counter() - start)
```

### Solution 6
```python
# Бинарный поиск сравнивает середину и отбрасывает половину
# — требует отсортированного массива
```

### Solution 7
```python
import bisect
print(bisect.bisect_left(arr, 5))
```
<!--/SOLUTION-->

<!--QUIZ-->
What is linear search?
- Scan all
- Halve
- Skip
- None
* Correct answer: Scan all
O(n).

What is binary search?
- Halving
- Scan
- Random
- None
* Correct answer: Halving
O(log n).

What does binary require?
- Sorted data
- Unique
- Big
- None
* Correct answer: Sorted data
Order.

What is mid?
- Middle index
- Target
- Start
- None
* Correct answer: Middle index
(lo+hi)//2.

What to return if missing?
- -1
- 0
- None
- Error
* Correct answer: -1
Convention.

What is O(log n)?
- Fast growth
- Slow
- Constant
- None
* Correct answer: Fast growth
Low.

When use linear?
- Unsorted
- Sorted
- Never
- Always
* Correct answer: Unsorted
Simple.

What is enumerate?
- Index + value
- Values
- Indexes
- None
* Correct answer: Index + value
Pairs.

What is bisect?
- Built-in binary search
- Linear
- Sort
- None
* Correct answer: Built-in binary search
Module.

What is the loop condition?
- lo <= hi
- lo < hi
- lo == hi
- None
* Correct answer: lo <= hi
Correct.

What happens at mid == target?
- Return mid
- Continue
- Stop
- None
* Correct answer: Return mid
Found.

Is binary good for sorted huge data?
- Yes
- No
- Same
- None
* Correct answer: Yes
Fast.
<!--/QUIZ-->
