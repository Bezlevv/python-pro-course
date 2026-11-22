---
title: Sorting algorithms
summary: Bubble, insertion, merge, quick sort.
order: 2
duration: 50 min
difficulty: intermediate
tags: sorting, merge sort, quicksort
---

Sorting puts elements in order; understanding algorithms helps choose.

## Bubble sort

```python
def bubble_sort(arr):
    a = arr[:]
    n = len(a)
    for i in range(n):
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a
```

## Insertion sort

```python
def insertion_sort(arr):
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a
```

## Merge sort

Divide, sort halves, merge.

## Quick sort

Pick pivot, partition, recurse.

## Lesson summary

O(n²) simple sorts vs O(n log n) advanced.

<!--TASK-->
### Task 1 — Bubble
Implement bubble sort and test.

### Task 2 — Insertion
Implement insertion sort.

### Task 3 — Merge
Implement merge sort (recursive).

### Task 4 — Quick
Implement a simple quicksort.

### Task 5 — Compare
Time bubble vs merge on 1000 items.

### Task 6 — Stable
Explain what stable means.

### Task 7 — Built-in
Use sorted() and compare.
<!--/TASK-->

<!--HINT-->
### Hint 1
Swaps.

### Hint 2
Insert.

### Hint 3
Recursion.

### Hint 4
Pivot.

### Hint 5
perf_counter.

### Hint 6
Order preserved.

### Hint 7
sorted().
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
def bubble_sort(arr):
    a = arr[:]
    n = len(a)
    for i in range(n):
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a
```

### Solution 2
```python
def insertion_sort(arr):
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a
```

### Solution 3
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:]); result.extend(right[j:])
    return result
```

### Solution 4
```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)
```

### Solution 5
```python
import random, time
data = [random.randint(0, 1000) for _ in range(1000)]
start = time.perf_counter(); bubble_sort(data); print("bubble", time.perf_counter() - start)
start = time.perf_counter(); merge_sort(data); print("merge", time.perf_counter() - start)
```

### Solution 6
```python
# Стабильная сортировка сохраняет порядок равных элементов
# (merge стабильна, quick — часто нет)
```

### Solution 7
```python
print(sorted(data))
```
<!--/SOLUTION-->

<!--QUIZ-->
What is bubble sort?
- Adjacent swaps
- Insert
- Merge
- None
* Correct answer: Adjacent swaps
O(n²).

What is insertion sort?
- Inserts into sorted part
- Swaps
- Divides
- None
* Correct answer: Inserts into sorted part
Good on small.

What is merge sort?
- Divide and merge
- Swaps
- Pivot
- None
* Correct answer: Divide and merge
O(n log n).

What is quicksort?
- Pivot partition
- Merge
- Insert
- None
* Correct answer: Pivot partition
Average O(n log n).

What is stable?
- Equal order kept
- Faster
- Memory
- None
* Correct answer: Equal order kept
Property.

Which is O(n log n)?
- Merge sort
- Bubble
- Insertion
- All
* Correct answer: Merge sort
Advanced.

Which is O(n²)?
- Bubble
- Merge
- Quick average
- None
* Correct answer: Bubble
Simple.

Why use built-in sorted()?
- Optimized
- Required
- Slower
- None
* Correct answer: Optimized
Timsort.

What is a pivot?
- Partition element
- A swap
- A sort
- None
* Correct answer: Partition element
Quick.

What is recursion?
- Function calls itself
- A loop
- An error
- None
* Correct answer: Function calls itself
Merge.

What is a base case?
- Stop condition
- Loop
- Error
- None
* Correct answer: Stop condition
len <= 1.

Which is best for huge sorted data?
- Timsort (sorted)
- Bubble
- Slow merge
- None
* Correct answer: Timsort (sorted)
Adaptive.
<!--/QUIZ-->
