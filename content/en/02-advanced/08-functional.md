---
title: Functional style: lambda, map, filter, sorted
summary: Anonymous functions and functional tools for concise transformation of collections.
order: 8
duration: 40 min
difficulty: intermediate
tags: lambda, map, filter, sorted, functional
---

Functional style focuses on transforming data with small, testable functions.

## lambda

```python
square = lambda x: x * x
print(square(5))   # 25
```

Lambda is an anonymous function for simple expressions.

## map

```python
nums = [1, 2, 3]
print(list(map(lambda x: x * 2, nums)))   # [2, 4, 6]
```

## filter

```python
print(list(filter(lambda x: x > 1, nums)))   # [2, 3]
```

## sorted with key

```python
people = [("Anna", 21), ("Boris", 30)]
print(sorted(people, key=lambda p: p[1]))
```

## functools.reduce

```python
from functools import reduce
print(reduce(lambda a, b: a + b, nums))   # 6
```

## Lesson summary

lambda, map, filter, sorted and reduce let you express transformations concisely.

<!--TASK-->
### Task 1 — lambda basics
Define square = lambda x: x * x; print square(6).

### Task 2 — map
Double every number in [1,2,3,4] with map; print list.

### Task 3 — filter
Keep numbers > 2 from [1,2,3,4,5] with filter.

### Task 4 — sorted by key
Sort strings by their length using key=len.

### Task 5 — sorted by second element
Sort list of tuples by age (second element) ascending.

### Task 6 — reduce
Compute product of [1,2,3,4] with reduce.

### Task 7 — combine map+filter
From 1..10 take squares, then keep even ones using map/filter; print result.
<!--/TASK-->

<!--HINT-->
### Hint 1
square = lambda x: x * x.

### Hint 2
list(map(func, iterable)).

### Hint 3
list(filter(predicate, iterable)).

### Hint 4
sorted(words, key=len).

### Hint 5
sorted(data, key=lambda t: t[1]).

### Hint 6
reduce(lambda a,b: a*b, nums).

### Hint 7
filter(lambda x: x % 2 == 0, map(lambda x: x*x, range(1,11))).
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
square = lambda x: x * x
print(square(6))   # 36
```

### Solution 2
```python
nums = [1, 2, 3, 4]
print(list(map(lambda x: x * 2, nums)))   # [2,4,6,8]
```

### Solution 3
```python
nums = [1, 2, 3, 4, 5]
print(list(filter(lambda x: x > 2, nums)))   # [3,4,5]
```

### Solution 4
```python
words = ["Python", "Go", "Java", "C"]
print(sorted(words, key=len))   # ['C','Go','Java','Python']
```

### Solution 5
```python
people = [("Anna", 21), ("Boris", 30), ("Vika", 19)]
print(sorted(people, key=lambda p: p[1]))
```

### Solution 6
```python
from functools import reduce
print(reduce(lambda a, b: a * b, [1, 2, 3, 4]))   # 24
```

### Solution 7
```python
squares = map(lambda x: x * x, range(1, 11))
evens = filter(lambda x: x % 2 == 0, squares)
print(list(evens))   # [4,16,36,64,100]
```
<!--/SOLUTION-->

<!--QUIZ-->
What is lambda?
- Anonymous function
- A module
- A list
- A class
* Correct answer: Anonymous function
For simple expressions.

What does map do?
- Applies a function to each element
- Filters elements
- Sorts
- Sums
* Correct answer: Applies a function to each element
Returns map object.

What does filter do?
- Keeps elements passing the predicate
- Transforms each
- Sorts
- Splits
* Correct answer: Keeps elements passing the predicate
Boolean condition.

What does sorted(key=...) do?
- Sorts by a key function
- Filters
- Maps
- Reduces
* Correct answer: Sorts by a key function
key=len etc.

What is the result of map(lambda x: x+1, [1,2])?
- [2, 3]
- [1, 2]
- (2,3)
- map object
* Correct answer: map object (lazy); list() to show
Output: [2,3] after list.

How to materialize map?
- list(map(...))
- map(...)
- sum(map(...))
- map actually returns list
* Correct answer: list(map(...))
Convert to list.

What does reduce do?
- Combines elements into one value
- Filters
- Sorts
- Maps
* Correct answer: Combines elements into one value
Left-to-right.

Which import is needed for reduce?
- from functools import reduce
- import math
- from itertools import reduce
- reduce built-in
* Correct answer: from functools import reduce
functools.

What is sorted(people, key=lambda p: p[1])?
- Sort by second element
- Sort by first
- Reverse sort
- Filter
* Correct answer: Sort by second element
Age in tuples.

Can lambda have multiple statements?
- No, only expressions
- Yes
- With pass
- Only one line + return
* Correct answer: No, only expressions
Single expression body.

What does filter(lambda x: x % 2 == 0, range(5)) give?
- [0, 2, 4]
- [1, 3]
- [0..4]
- Odd
* Correct answer: [0, 2, 4]
Even numbers.

Is functional style always faster?
- Not necessarily; readability is the point
- Always
- Never
- Only in loops
* Correct answer: Not necessarily; readability is the point
Prefer clarity.
<!--/QUIZ-->
