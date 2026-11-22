---
title: Idioms: comprehensions, slicing, unpacking
summary: Pythonic one-liners.
order: 1
duration: 40 min
difficulty: intermediate
tags: idioms, comprehension
---

Python idioms are concise and readable.

## Comprehensions

```python
squares = [x**2 for x in range(10)]
even = [x for x in range(10) if x % 2 == 0]
d = {x: x**2 for x in range(5)}
```

## Slicing

```python
nums = [0, 1, 2, 3, 4]
nums[1:4]   # [1, 2, 3]
nums[::-1]  # reversed
```

## Unpacking

```python
a, b, *rest = [1, 2, 3, 4]
first, *_, last = nums
```

## Lesson summary

Comprehensions, slices, unpacking shorten code.

<!--TASK-->
### Task 1 — List comp
Squares of 1–10.

### Task 2 — Filter
Even numbers.

### Task 3 — Dict comp
char: count from a string.

### Task 4 — Slice
Middle three elements.

### Task 5 — Reverse
Reverse a list.

### Task 6 — Unpack
Head and tail.

### Task 7 — Zip
Pair two lists.
<!--/TASK-->

<!--HINT-->
### Hint 1
[x**2 for x in ...].

### Hint 2
if x % 2 == 0.

### Hint 3
{c: s.count(c)}.

### Hint 4
[1:4].

### Hint 5
[::-1].

### Hint 6
*rest.

### Hint 7
zip().
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
squares = [x**2 for x in range(1, 11)]
```

### Solution 2
```python
even = [x for x in range(10) if x % 2 == 0]
```

### Solution 3
```python
s = "abracadabra"
counts = {c: s.count(c) for c in set(s)}
```

### Solution 4
```python
nums = [0, 1, 2, 3, 4]
print(nums[1:4])   # [1, 2, 3]
```

### Solution 5
```python
print(nums[::-1])   # [4, 3, 2, 1, 0]
```

### Solution 6
```python
head, *tail = nums
print(head, tail)   # 0 [1, 2, 3, 4]
```

### Solution 7
```python
names = ["a", "b"]
values = [1, 2]
for name, value in zip(names, values):
    print(name, value)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a comprehension?
- Inline loop
- A function
- A class
- None
* Correct answer: Inline loop
Build.

What is a filter?
- if clause
- for
- Map
- None
* Correct answer: if clause
Condition.

What is slicing?
- Range access
- Loop
- Sort
- None
* Correct answer: Range access
[1:4].

What is [::-1]?
- Reverse
- Copy
- Sort
- None
* Correct answer: Reverse
Step -1.

What is unpacking?
- Assigning parts
- Packing
- Sorting
- None
* Correct answer: Assigning parts
*a.

What is *rest?
- Collects rest
- Error
- First
- None
* Correct answer: Collects rest
List.

What is zip?
- Pairs iterables
- Splits
- Sorts
- None
* Correct answer: Pairs iterables
Tuples.

What is enumerate?
- Index + value
- Values
- Indexes
- None
* Correct answer: Index + value
Pairs.

What is a dict comprehension?
- {k: v for}
- List
- Set
- None
* Correct answer: {k: v for}
Map.

What is a set comprehension?
- {x for}
- List
- Dict
- None
* Correct answer: {x for}
Unique.

What is the walrus?
- := assignment
- ==
- =
- None
* Correct answer: := assignment
Inline.

What is the benefit?
- Readable
- Faster always
- Required
- None
* Correct answer: Readable
Pythonic.
<!--/QUIZ-->
