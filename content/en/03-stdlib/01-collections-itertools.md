---
title: collections, itertools, functools
summary: Useful standard helpers: Counter, defaultdict, deque, chain, product, lru_cache.
order: 1
duration: 40 min
difficulty: intermediate
tags: collections, itertools, functools
---

The standard library contains powerful data and function tools.

## collections

```python
from collections import Counter, defaultdict, deque, namedtuple

Counter("abracadabra")      # counts
defaultdict(list)           # default factory
deque([1,2,3])              # fast ends
Point = namedtuple("Point", "x y")
```

## itertools

```python
from itertools import chain, product, islice, groupby

list(chain([1,2],[3,4]))    # [1,2,3,4]
list(product("ab", [1,2]))  # all pairs
list(islice(range(100), 3))
```

## functools

```python
from functools import lru_cache, partial, reduce

@lru_cache(maxsize=None)
def fib(n): ...
```

## Lesson summary

collections/itertools/functools make code shorter and faster.

<!--TASK-->
### Task 1 — Counter
Count characters in "mississippi"; show most common 2.

### Task 2 — defaultdict
Group words by first letter using defaultdict(list).

### Task 3 — deque
Use deque to appendleft and popleft; show behavior.

### Task 4 — namedtuple
Create Point(x, y); access by name.

### Task 5 — itertools.product
Generate all combos of [1,2] x ["a","b"].

### Task 6 — islice
Take the first 5 even numbers from a generator.

### Task 7 — lru_cache
Speed up a recursive fib; show caching benefit.
<!--/TASK-->

<!--HINT-->
### Hint 1
Counter(text).most_common(2).

### Hint 2
d[word[0]].append(word).

### Hint 3
dq.appendleft(x); dq.popleft().

### Hint 4
Point(1, 2); p.x.

### Hint 5
product([1,2], ["a","b"]).

### Hint 6
islice(evens(), 5).

### Hint 7
@lru_cache(maxsize=None) on fib.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from collections import Counter
c = Counter("mississippi")
print(c.most_common(2))   # [('s', 4), ('i', 4)]
```

### Solution 2
```python
words = ["apple", "apricot", "banana"]
d = defaultdict(list)
for w in words:
    d[w[0]].append(w)
print(dict(d))
```

### Solution 3
```python
from collections import deque
dq = deque([1, 2, 3])
dq.appendleft(0)
dq.popleft()
print(list(dq))   # [1, 2, 3]
```

### Solution 4
```python
from collections import namedtuple
Point = namedtuple("Point", "x y")
p = Point(1, 2)
print(p.x, p.y)   # 1 2
```

### Solution 5
```python
from itertools import product
print(list(product([1, 2], ["a", "b"])))
```

### Solution 6
```python
from itertools import islice

def evens():
    n = 0
    while True:
        yield n
        n += 2

print(list(islice(evens(), 5)))   # [0, 2, 4, 6, 8]
```

### Solution 7
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(30))   # fast
```
<!--/SOLUTION-->

<!--QUIZ-->
What does Counter do?
- Counts hashable items
- Sorts
- Groups
- Joins
* Correct answer: Counts hashable items
Returns counts.

What is defaultdict(list)?
- Auto-creates list for missing keys
- Normal dict
- Set
- Counter
* Correct answer: Auto-creates list for missing keys
No KeyError.

What is deque good for?
- Fast operations on both ends
- Sorting
- Hashing
- Counting
* Correct answer: Fast operations on both ends
O(1) ends.

What is namedtuple?
- Tuple with named fields
- Dict
- Class
- List
* Correct answer: Tuple with named fields
p.x.

What does itertools.product do?
- Cartesian product
- Sums
- Filters
- Sorts
* Correct answer: Cartesian product
All combos.

What does islice do?
- Slices an iterator
- Sums
- Sorts
- Maps
* Correct answer: Slices an iterator
Take limited items.

What does lru_cache do?
- Caches results
- Limits memory
- Counts
- Formats
* Correct answer: Caches results
Memoization.

What does partial do?
- Fixes arguments
- Reverses
- Copies
- Times
* Correct answer: Fixes arguments
partial(add, 1).

What does reduce do?
- Combines iterable to one value
- Splits
- Sorts
- Maps
* Correct answer: Combines iterable to one value
functools.

Which import for Counter?
- from collections import Counter
- import itertools
- from functools import counter
- counter
* Correct answer: from collections import Counter
In collections.

What does chain do?
- Concatenates iterables
- Repeats
- Counts
- Zips
* Correct answer: Concatenates iterables
Seamless iteration.

What does groupby do?
- Groups adjacent equal items
- Sorts
- Filters
- Reverses
* Correct answer: Groups adjacent equal items
Use with sorted data.
<!--/QUIZ-->
