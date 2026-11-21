---
title: NumPy: arrays and operations
summary: Creating arrays, shapes, vectorized math, indexing and broadcasting.
order: 1
duration: 40 min
difficulty: intermediate
tags: numpy, arrays, vectorization
---

NumPy adds fast multi-dimensional arrays and vectorized math.

## Creating arrays

```python
import numpy as np

a = np.array([1, 2, 3])
b = np.zeros((2, 3))
c = np.ones((2, 2))
d = np.arange(5)
e = np.linspace(0, 1, 5)
```

## Shape and dtype

```python
a.shape, a.dtype, a.ndim
```

## Vectorized operations

```python
a + 10
a * a
a.sum(), a.mean(), a.max()
```

## Indexing

```python
a[0]
a[-1]
a[1:3]
```

## Broadcasting

```python
m = np.ones((3, 1))
v = np.array([1, 2, 3])
print(m + v)   # broadcasts
```

## Lesson summary

NumPy arrays are fast; vectorization replaces loops.

<!--TASK-->
### Task 1 — Create arrays
Create ones(3), zeros((2,2)), arange(10), linspace(0,1,4); print shapes.

### Task 2 — Operations
For a = [1,2,3,4] compute a+5, a*2, a**2.

### Task 3 — Reductions
Compute sum, mean, min, max, std of a.

### Task 4 — Indexing
From [10,20,30,40,50] get first, last, and slice 1:4.

### Task 5 — 2D
Create a 2x3 array; access element [1][2]; sum over axis 0.

### Task 6 — Broadcasting
Add a column vector to a row vector (3x1 + 1x3).

### Task 7 — Comparison
Create boolean mask a > 2 and count True elements.
<!--/TASK-->

<!--HINT-->
### Hint 1
np.ones, np.zeros, np.arange, np.linspace.

### Hint 2
Vectorized expressions.

### Hint 3
a.sum(), a.mean(), a.std().

### Hint 4
a[0], a[-1], a[1:4].

### Hint 5
arr[1, 2]; arr.sum(axis=0).

### Hint 6
m + v broadcasts.

### Hint 7
(a > 2).sum().
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import numpy as np
print(np.ones(3).shape)
print(np.zeros((2, 2)).shape)
print(np.arange(10).shape)
print(np.linspace(0, 1, 4))
```

### Solution 2
```python
a = np.array([1, 2, 3, 4])
print(a + 5)
print(a * 2)
print(a ** 2)
```

### Solution 3
```python
print(a.sum(), a.mean(), a.min(), a.max(), a.std())
```

### Solution 4
```python
x = np.array([10, 20, 30, 40, 50])
print(x[0], x[-1], x[1:4])
```

### Solution 5
```python
m = np.array([[1, 2, 3], [4, 5, 6]])
print(m[1, 2])          # 6
print(m.sum(axis=0))    # [5 7 9]
```

### Solution 6
```python
col = np.ones((3, 1))
row = np.array([1, 2, 3])
print(col + row)
```

### Solution 7
```python
a = np.array([1, 5, 2, 7])
print((a > 2).sum())   # 3
```
<!--/SOLUTION-->

<!--QUIZ-->
What does np.array([1,2,3]) create?
- A 1D array
- A list
- A tuple
- A string
* Correct answer: A 1D array
NumPy array.

What is vectorization?
- Operations on whole arrays
- Loops
- Functions
- Import
* Correct answer: Operations on whole arrays
Fast.

What does a.shape return?
- Dimensions
- Values
- Type
- Size
* Correct answer: Dimensions
Tuple.

What does a.sum() do?
- Sums elements
- Sorts
- Reshapes
- Copies
* Correct answer: Sums elements
Reduction.

What is broadcasting?
- Expanding shapes for ops
- Printing
- Casting
- Slicing
* Correct answer: Expanding shapes for ops
Shape alignment.

How to index a 2D array?
- a[i, j]
- a[i][j] both
- a(i, j)
- aij
* Correct answer: a[i, j]
Comma indexing.

What does axis=0 mean?
- Down rows
- Across columns
- Both
- None
* Correct answer: Down rows
First axis.

What does np.arange(10) produce?
- 0..9
- 1..10
- 0..10
- 10 numbers? yes
* Correct answer: 0..9
Stop exclusive.

What is np.linspace(0,1,5)?
- 5 evenly spaced numbers
- 5 random
- 0..1 step
- Boolean
* Correct answer: 5 evenly spaced numbers
Inclusive endpoints.

What does a > 2 return?
- Boolean array
- Numbers
- None
- String
* Correct answer: Boolean array
Mask.

Why use NumPy?
- Speed and convenience
- GUI
- Printing
- Types
* Correct answer: Speed and convenience
C-backed.

What does a.mean() do?
- Average
- Sum
- Max
- Sort
* Correct answer: Average
Mean.
<!--/QUIZ-->
