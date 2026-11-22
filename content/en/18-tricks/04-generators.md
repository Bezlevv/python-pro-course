---
title: Generators, yield, itertools
summary: Lazy iteration, infinite sequences.
order: 4
duration: 45 min
difficulty: advanced
tags: generators, yield, itertools
---

Generators produce values on demand.

## Generator

```python
def count_up_to(n):
    x = 0
    while x < n:
        yield x
        x += 1

for value in count_up_to(3):
    print(value)   # 0 1 2
```

## Lazy benefits

Memory-friendly: one value at a time.

## itertools

```python
from itertools import islice, cycle, chain

list(islice(cycle("AB"), 4))   # ['A','B','A','B']
list(chain([1, 2], [3]))        # [1,2,3]
```

## Lesson summary

Generators are lazy iterators.

<!--TASK-->
### Task 1 — Generator
Write count_up_to.

### Task 2 — Infinite
Yield forever (take 5).

### Task 3 — islice
Limit infinite sequence.

### Task 4 — chain
Chain two iterables.

### Task 5 — Memory
Explain lazy memory saving.

### Task 6 — next
Use next() manually.

### Task 7 — Comp
Generator expression (x for x in ...).
<!--/TASK-->

<!--HINT-->
### Hint 1
yield.

### Hint 2
while True.

### Hint 3
islice.

### Hint 4
chain.

### Hint 5
One at a time.

### Hint 6
next().

### Hint 7
Genexp.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
def count_up_to(n):
    x = 0
    while x < n:
        yield x
        x += 1
```

### Solution 2
```python
def natural():
    n = 0
    while True:
        yield n
        n += 1
```

### Solution 3
```python
from itertools import islice
print(list(islice(natural(), 5)))   # [0,1,2,3,4]
```

### Solution 4
```python
from itertools import chain
print(list(chain([1, 2], [3, 4])))   # [1,2,3,4]
```

### Solution 5
```python
# Генератор хранит только текущее значение:
# огромные последовательности без нагрузки на память
```

### Solution 6
```python
gen = count_up_to(3)
print(next(gen))   # 0
print(next(gen))   # 1
```

### Solution 7
```python
squares = (x**2 for x in range(1000000))
print(next(squares))   # 0
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a generator?
- Lazy iterator
- A list
- A dict
- None
* Correct answer: Lazy iterator
yield.

What is yield?
- Produces value
- Ends
- Returns only
- None
* Correct answer: Produces value
Pause.

What is lazy?
- On demand
- All at once
- Eager
- None
* Correct answer: On demand
Memory.

What is next?
- Takes next
- Starts
- Stops
- None
* Correct answer: Takes next
Manual.

What is islice?
- Limits slice
- Sorts
- Chains
- None
* Correct answer: Limits slice
Infinite.

What is chain?
- Joins iterables
- Splits
- Repeats
- None
* Correct answer: Joins iterables
Sequence.

What is cycle?
- Repeats
- Ends
- Sorts
- None
* Correct answer: Repeats
Forever.

What is a generator expression?
- (x for x in ...)
- [x for]
- {x for}
- None
* Correct answer: (x for x in ...)
Lazy.

What is StopIteration?
- End signal
- Error
- Start
- None
* Correct answer: End signal
Raised.

What is an iterator?
- Produces values
- A list
- A set
- None
* Correct answer: Produces values
Protocol.

What is the benefit?
- Low memory
- Faster always
- Required
- None
* Correct answer: Low memory
Big data.

What does iter() do?
- Makes iterator
- Ends
- Repeats
- None
* Correct answer: Makes iterator
Object.
<!--/QUIZ-->
