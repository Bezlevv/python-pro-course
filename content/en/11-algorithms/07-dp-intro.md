---
title: Dynamic programming: Fibonacci, stairs, knapsack
summary: Memoization, bottom-up tables, classic problems.
order: 7
duration: 50 min
difficulty: advanced
tags: dp, memoization, knapsack
---

Dynamic programming solves problems by combining subproblems.

## Fibonacci

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

## Stairs

```python
def climb(n):
    a, b = 1, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

## Knapsack

```python
def knapsack(capacity, weights, values):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w],
                               dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]
    return dp[n][capacity]
```

## Lesson summary

Memoization or tables avoid repeated work.

<!--TASK-->
### Task 1 — Fibonacci
Implement memoized fib.

### Task 2 — Table
Implement fib bottom-up.

### Task 3 — Stairs
Count ways for n=10.

### Task 4 — Knapsack
Solve capacity 50 with 3 items.

### Task 5 — Memoization
Explain caching.

### Task 6 — Overlap
Explain overlapping subproblems.

### Task 7 — Choose
When to use DP?
<!--/TASK-->

<!--HINT-->
### Hint 1
lru_cache.

### Hint 2
Loop.

### Hint 3
Climb.

### Hint 4
Table.

### Hint 5
Cache.

### Hint 6
Repeat.

### Hint 7
Optimal substructure.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(30))
```

### Solution 2
```python
def fib_table(n):
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]

print(fib_table(30))
```

### Solution 3
```python
def climb(n):
    a, b = 1, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

print(climb(10))   # 89
```

### Solution 4
```python
print(knapsack(50, [10, 20, 30], [60, 100, 120]))   # 220
```

### Solution 5
```python
# Мемоизация сохраняет результаты подзадач,
# чтобы не пересчитывать их повторно
```

### Solution 6
```python
# fib(n-1) и fib(n-2) перекрываются — это overlap
```

### Solution 7
```python
# Когда оптимальное решение строится из оптимальных подзадач
# и подзадачи повторяются
```
<!--/SOLUTION-->

<!--QUIZ-->
What is DP?
- Dynamic programming
- Deep print
- Data
- None
* Correct answer: Dynamic programming
Method.

What is memoization?
- Caching results
- Sorting
- Looping
- None
* Correct answer: Caching results
Top-down.

What is overlap?
- Repeated subproblems
- Unique
- Errors
- None
* Correct answer: Repeated subproblems
DP fits.

What is fib(30)?
- 832040
- 30
- 300
- None
* Correct answer: 832040
Value.

What is bottom-up?
- Iterative table
- Recursion
- Cache
- None
* Correct answer: Iterative table
Tabulation.

What is dp[i][w]?
- Best value with i items, w capacity
- Weight
- Count
- None
* Correct answer: Best value with i items, w capacity
Knapsack.

What is subproblem?
- Smaller piece
- Full problem
- Answer
- None
* Correct answer: Smaller piece
Part.

What is optimal substructure?
- Best from best
- Random
- Fixed
- None
* Correct answer: Best from best
Property.

What is the stairs recurrence?
- f(n)=f(n-1)+f(n-2)
- f(n)=n
- f(n)=2n
- None
* Correct answer: f(n)=f(n-1)+f(n-2)
Two options.

What is the base case?
- fib(0)=0, fib(1)=1
- Error
- End
- None
* Correct answer: fib(0)=0, fib(1)=1
Stop.

What is lru_cache?
- Caching decorator
- A loop
- A table
- None
* Correct answer: Caching decorator
Memo.

When use DP?
- Overlap + substructure
- Always
- Never
- Random
* Correct answer: Overlap + substructure
Criteria.
<!--/QUIZ-->
