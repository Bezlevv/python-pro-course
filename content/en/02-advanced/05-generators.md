---
title: Generators and yield
summary: Generator functions, yield, lazy evaluation, generator expressions and itertools.
order: 5
duration: 40 min
difficulty: intermediate
tags: generators, yield, lazy, iterator
---

Generators produce values one at a time instead of building whole lists in memory.

## Yield

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

for x in countdown(3):
    print(x)
```

## Lazy evaluation

Values are produced on demand: good for large sequences.

## Generator expressions

```python
squares = (x * x for x in range(10))
print(sum(squares))   # 285
```

## Pausing

`yield` pauses the function; the generator resumes on the next request.

## Use cases

- processing files line by line;
- infinite sequences;
- pipelines.

## Lesson summary

Generators are memory-efficient iterators created with yield or generator expressions.

<!--TASK-->
### Task 1 — Simple generator
Write counter(n) yielding 1..n; iterate and print.

### Task 2 — Even generator
Write evens(limit) yielding even numbers up to limit.

### Task 3 — Generator expression
Create (x**2 for x in range(5)); print list() of it.

### Task 4 — Infinite sequence
Write naturals() yielding 1,2,3,...; take first 5 using itertools.islice.

### Task 5 — File lines
Write read_lines(path) yielding stripped lines from a file; test with a temp file.

### Task 6 — Pipeline
Chain two generators (squares then filter odd) and collect results.

### Task 7 — Fibonacci
Write fib() generator yielding Fibonacci numbers; print first 8.
<!--/TASK-->

<!--HINT-->
### Hint 1
def counter(n): i=1; while i<=n: yield i; i+=1.

### Hint 2
yield only when i % 2 == 0.

### Hint 3
list(gen) materializes.

### Hint 4
itertools.islice(naturals(), 5).

### Hint 5
Use open() with with and yield line.strip().

### Hint 6
Square then filter with (x for x in gen if x % 2).

### Hint 7
a,b = 0,1; while True: yield a; a,b = b, a+b.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
def counter(n):
    i = 1
    while i <= n:
        yield i
        i += 1

for x in counter(3):
    print(x)   # 1 2 3
```

### Solution 2
```python
def evens(limit):
    for i in range(limit + 1):
        if i % 2 == 0:
            yield i

print(list(evens(6)))   # [0, 2, 4, 6]
```

### Solution 3
```python
squares = (x ** 2 for x in range(5))
print(list(squares))   # [0, 1, 4, 9, 16]
```

### Solution 4
```python
import itertools

def naturals():
    n = 1
    while True:
        yield n
        n += 1

print(list(itertools.islice(naturals(), 5)))   # [1,2,3,4,5]
```

### Solution 5
```python
def read_lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.strip()
```

### Solution 6
```python
squares = (x * x for x in range(10))
odds = (x for x in squares if x % 2)
print(list(odds))   # [1, 9, 25, 49, 81]
```

### Solution 7
```python
def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

import itertools
print(list(itertools.islice(fib(), 8)))   # [0,1,1,2,3,5,8,13]
```
<!--/SOLUTION-->

<!--QUIZ-->
What does yield do?
- Pauses and returns a value
- Stops the function
- Creates a list
- Ends the loop
* Correct answer: Pauses and returns a value
The generator resumes later.

Are generators lazy?
- Yes, values on demand
- No
- Sometimes
- Only in classes
* Correct answer: Yes, values on demand
Memory efficient.

What is a generator expression?
- (x for x in ...)
- [x for x in ...]
- {x for x in ...}
- generator()
* Correct answer: (x for x in ...)
Parentheses — lazy.

How to materialize a generator?
- list(gen)
- gen()
- len(gen)
- sum(gen) only
* Correct answer: list(gen)
Convert to list.

Can a generator be infinite?
- Yes
- No
- Only with stop
- Impossible
* Correct answer: Yes
Yield forever; consume partially.

What does itertools.islice do?
- Slices an iterator
- Sums it
- Sorts it
- Reverses it
* Correct answer: Slices an iterator
Take a limited number.

Is a generator an iterator?
- Yes
- No
- Only a function
- Only a class
* Correct answer: Yes
It has __next__.

What happens after the last yield?
- StopIteration
- Return None
- Loop
- Error
* Correct answer: StopIteration
Signals the end.

What is the benefit over a list?
- Lower memory
- Faster always
- Simpler
- Debugging
* Correct answer: Lower memory
One value at a time.

Can you reuse a generator?
- No, it is exhausted
- Yes, infinitely
- Only once more
- After copy
* Correct answer: No, it is exhausted
Create a new one.

What does sum((x for x in range(5))) return?
- 10
- 15
- 5
- 0
* Correct answer: 10
0+1+2+3+4.

Which is a generator function?
- def f(): yield 1
- def f(): return 1
- def f(): print(1)
- lambda
* Correct answer: def f(): yield 1
Contains yield.
<!--/QUIZ-->
