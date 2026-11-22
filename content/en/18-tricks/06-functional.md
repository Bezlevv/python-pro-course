---
title: Functional style: map, filter, reduce
summary: Higher-order functions and immutable data.
order: 6
duration: 40 min
difficulty: intermediate
tags: functional, map, reduce
---

Functional style works with functions, not loops.

## map

```python
nums = [1, 2, 3]
squares = list(map(lambda x: x**2, nums))
```

## filter

```python
even = list(filter(lambda x: x % 2 == 0, nums))
```

## reduce

```python
from functools import reduce
total = reduce(lambda a, b: a + b, nums, 0)
```

## Lesson summary

map/filter/reduce replace simple loops.

<!--TASK-->
### Task 1 — Map
Double all values.

### Task 2 — Filter
Keep positives.

### Task 3 — Reduce
Sum with reduce.

### Task 4 — Lambda
Write a lambda.

### Task 5 — Compose
map + filter together.

### Task 6 — Immutable
Why not mutate?

### Task 7 — Choice
When use comprehensions instead?
<!--/TASK-->

<!--HINT-->
### Hint 1
map.

### Hint 2
filter.

### Hint 3
reduce.

### Hint 4
lambda x:.

### Hint 5
Chain.

### Hint 6
Predictable.

### Hint 7
Readability.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
nums = [1, 2, 3, 4]
doubled = list(map(lambda x: x * 2, nums))
# [2, 4, 6, 8]
```

### Solution 2
```python
positives = list(filter(lambda x: x > 0, [-1, 2, -3, 4]))
# [2, 4]
```

### Solution 3
```python
from functools import reduce
total = reduce(lambda a, b: a + b, nums, 0)
# 10
```

### Solution 4
```python
square = lambda x: x ** 2
print(square(4))   # 16
```

### Solution 5
```python
result = list(map(lambda x: x ** 2,
                  filter(lambda x: x % 2 == 0, nums)))
# [4, 16]
```

### Solution 6
```python
# Функциональный стиль не меняет исходные данные:
# меньше побочных эффектов, проще предсказать
```

### Solution 7
```python
# Для простых случаев понятнее comprehension:
# [x**2 for x in nums if x % 2 == 0]
```
<!--/SOLUTION-->

<!--QUIZ-->
What is map?
- Applies function
- Filters
- Sums
- None
* Correct answer: Applies function
Transforms.

What is filter?
- Keeps matches
- Transforms
- Reduces
- None
* Correct answer: Keeps matches
Predicate.

What is reduce?
- Combines
- Filters
- Maps
- None
* Correct answer: Combines
Fold.

What is lambda?
- Anonymous function
- A class
- A loop
- None
* Correct answer: Anonymous function
Inline.

What is a higher-order function?
- Takes/returns functions
- A class
- A loop
- None
* Correct answer: Takes/returns functions
map.

What is immutability?
- No changes
- Mutation
- Loops
- None
* Correct answer: No changes
Safe.

What is a side effect?
- External change
- Pure result
- Return
- None
* Correct answer: External change
Avoid.

What is compose?
- Combining functions
- Naming
- Looping
- None
* Correct answer: Combining functions
Chain.

What is a predicate?
- Boolean function
- Transform
- Sum
- None
* Correct answer: Boolean function
Filter.

What is pure?
- Same input → same output
- Random
- Mutating
- None
* Correct answer: Same input → same output
Deterministic.

What is lazy?
- On demand
- Immediate
- Full
- None
* Correct answer: On demand
map object.

What is the Pythonic way?
- Comprehension
- map always
- Loops only
- None
* Correct answer: Comprehension
Readable.
<!--/QUIZ-->
