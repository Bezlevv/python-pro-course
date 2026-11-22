---
title: NumPy vectorization
summary: Arrays, ufuncs, avoid loops.
order: 2
duration: 45 min
difficulty: intermediate
tags: numpy
---

NumPy speeds up numeric code.

## Arrays

```python
import numpy as np
a = np.array([1, 2, 3])
b = a * 2        # [2 4 6]
c = a + b        # [3 6 9]
print(a.sum(), a.mean(), a.max())
```

## Avoid loops

```python
# медленно:
total = 0
for x in a:
    total += x
# быстро:
total = a.sum()
```

## Lesson summary

Vectorized operations beat Python loops.

<!--TASK-->
### Task 1 — Array
Create an array.

### Task 2 — Ops
Multiply and add.

### Task 3 — Aggregates
Sum, mean, max.

### Task 4 — Compare
Loop vs vectorized sum.

### Task 5 — Boolean
Filter with a mask.

### Task 6 — Shape
Check shape and dtype.

### Task 7 — 2D
Matrix multiply.
<!--/TASK-->

<!--HINT-->
### Hint 1
np.array.

### Hint 2
*.

### Hint 3
sum().

### Hint 4
Vectorized.

### Hint 5
a[a > 1].

### Hint 6
shape.

### Hint 7
@.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import numpy as np
a = np.array([1, 2, 3])
```

### Solution 2
```python
b = a * 2
c = a + b
```

### Solution 3
```python
print(a.sum(), a.mean(), a.max())
```

### Solution 4
```python
# loop: for x in a: total += x
# numpy: a.sum() — на порядок быстрее
```

### Solution 5
```python
mask = a > 1
print(a[mask])   # [2 3]
```

### Solution 6
```python
print(a.shape, a.dtype)   # (3,) int64
```

### Solution 7
```python
m = np.array([[1, 2], [3, 4]])
n = np.array([[5, 6], [7, 8]])
print(m @ n)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is NumPy?
- Numerical library
- A browser
- A database
- None
* Correct answer: Numerical library
Arrays.

What is an array?
- N-dim data
- A list only
- A string
- None
* Correct answer: N-dim data
ndarray.

What is vectorization?
- Batch ops
- Loops
- One scalar
- None
* Correct answer: Batch ops
Fast.

What is a mask?
- Boolean filter
- Loop
- Sort
- None
* Correct answer: Boolean filter
a > 1.

What is shape?
- Dimensions
- Size
- Type
- None
* Correct answer: Dimensions
Tuple.

What is dtype?
- Data type
- Size
- Shape
- None
* Correct answer: Data type
int64.

What is sum?
- Total
- Mean
- Max
- None
* Correct answer: Total
Aggregate.

What is mean?
- Average
- Sum
- Max
- None
* Correct answer: Average
Mean.

What is @?
- Matrix multiply
- Multiply elementwise
- Concat
- None
* Correct answer: Matrix multiply
Operator.

What is an axis?
- Dimension
- Value
- Mask
- None
* Correct answer: Dimension
axis=0.

What is the benefit?
- Speed
- Memory only
- Style
- None
* Correct answer: Speed
C loop.

What is broadcasting?
- Shape alignment
- Loops
- Errors
- None
* Correct answer: Shape alignment
Sizes.
<!--/QUIZ-->
