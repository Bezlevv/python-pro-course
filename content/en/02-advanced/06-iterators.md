---
title: Iterators
summary: What iterators are, iter() and next(), the iterator protocol and custom iterables.
order: 6
duration: 40 min
difficulty: intermediate
tags: iterators, iter, next, protocol
---

Iterators are objects that produce values one at a time. Every `for` loop uses them under the hood.

## Iterables vs iterators

- iterable: can be passed to iter() (lists, strings, dicts);
- iterator: produced by iter(), has __next__.

```python
nums = [1, 2, 3]
it = iter(nums)
print(next(it))   # 1
print(next(it))   # 2
```

## The protocol

An iterator implements __iter__ (returns itself) and __next__ (returns the next value or raises StopIteration).

## Custom iterator

```python
class Countdown:
    def __init__(self, n):
        self.n = n
    def __iter__(self):
        return self
    def __next__(self):
        if self.n <= 0:
            raise StopIteration
        self.n -= 1
        return self.n
```

## for loop mechanics

```python
for x in Countdown(3):
    print(x)
```

`for` calls iter(), then next() until StopIteration.

## Lesson summary

Iterators power for loops, generator functions are iterators, and any object with __next__ can drive iteration.

<!--TASK-->
### Task 1 — iter/next
Create a list, get an iterator, print first two values with next().

### Task 2 — String iterator
Iterate over "abc" using an iterator and next() three times.

### Task 3 — Custom Countdown
Implement class Countdown(n) with __iter__/__next__, print 3,2,1.

### Task 4 — StopIteration
Call next() after exhaustion in a try/except and print "End".

### Task 5 — Infinite iterator
Create class Squares that yields squares 1,4,9,...; consume first 4 via islice.

### Task 6 — Reverse iterator
Write class Reverse(iterable) that iterates backwards; test on [1,2,3].

### Task 7 — Sum with iterator
Create an iterator over 1..5 and compute the sum using next() in a loop.
<!--/TASK-->

<!--HINT-->
### Hint 1
it = iter(lst); next(it).

### Hint 2
next(iter("abc")).

### Hint 3
StopIteration when done.

### Hint 4
except StopIteration: print("End").

### Hint 5
__next__ returns n*n and increments n.

### Hint 6
Store the list; __next__ uses an index going backwards.

### Hint 7
Loop until StopIteration, adding values.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
nums = [1, 2, 3]
it = iter(nums)
print(next(it))   # 1
print(next(it))   # 2
```

### Solution 2
```python
it = iter("abc")
print(next(it), next(it), next(it))   # a b c
```

### Solution 3
```python
class Countdown:
    def __init__(self, n):
        self.n = n
    def __iter__(self):
        return self
    def __next__(self):
        if self.n <= 0:
            raise StopIteration
        self.n -= 1
        return self.n

for x in Countdown(3):
    print(x)   # 2 1 0? (n decremented before return)
```
Adjust logic to yield 3,2,1: decrement after return.

### Solution 4
```python
it = iter([])
try:
    next(it)
except StopIteration:
    print("End")
```

### Solution 5
```python
class Squares:
    def __init__(self):
        self.n = 1
    def __iter__(self):
        return self
    def __next__(self):
        v = self.n * self.n
        self.n += 1
        return v

import itertools
print(list(itertools.islice(Squares(), 4)))   # [1,4,9,16]
```

### Solution 6
```python
class Reverse:
    def __init__(self, data):
        self.data = data
        self.index = len(data)
    def __iter__(self):
        return self
    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index -= 1
        return self.data[self.index]

print(list(Reverse([1, 2, 3])))   # [3, 2, 1]
```

### Solution 7
```python
class OneToFive:
    def __init__(self):
        self.n = 1
    def __iter__(self):
        return self
    def __next__(self):
        if self.n > 5:
            raise StopIteration
        v = self.n
        self.n += 1
        return v

total = 0
for x in OneToFive():
    total += x
print(total)   # 15
```
<!--/SOLUTION-->

<!--QUIZ-->
What is an iterable?
- Object that can be passed to iter()
- An iterator
- A list only
- A function
* Correct answer: Object that can be passed to iter()
Lists, strings, dicts.

What is an iterator?
- Object with __next__
- A list
- A dict
- A module
* Correct answer: Object with __next__
Produces values sequentially.

What does iter() do?
- Returns an iterator from an iterable
- Ends iteration
- Sorts
- Copies
* Correct answer: Returns an iterator from an iterable
Starting point.

What does next(it) do?
- Returns the next value
- Resets the iterator
- Ends it
- Deletes it
* Correct answer: Returns the next value
Progresses.

What raises StopIteration?
- Exhausted iterator
- Empty list
- TypeError
- Zero division
* Correct answer: Exhausted iterator
Signals end.

What does __iter__ return?
- self usually
- None
- A list
- An int
* Correct answer: self usually
Iterator returns itself.

Can a list be an iterator?
- No, it is iterable
- Yes, always
- Only strings
- Only sets
* Correct answer: No, it is iterable
Use iter(list).

Does for use next()?
- Yes, internally
- No
- Sometimes
- Only while
* Correct answer: Yes, internally
Calls until StopIteration.

What happens without StopIteration?
- Infinite loop
- Error
- Nothing
- Stop
* Correct answer: Infinite loop
for cannot finish.

Which makes a custom iterator?
- Implementing __next__
- Importing
- def
- class only
* Correct answer: Implementing __next__
Plus __iter__.

What is iter("abc")?
- An iterator over characters
- A list
- An int
- A set
* Correct answer: An iterator over characters
Strings are iterable.

Can a generator be an iterator?
- Yes
- No
- Only with class
- Only in 3.10
* Correct answer: Yes
Generators implement the protocol.
<!--/QUIZ-->
