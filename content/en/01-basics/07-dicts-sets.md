---
title: Dictionaries and sets
summary: Dicts: keys and values, methods, iteration; sets: unique values and operations.
order: 7
duration: 30 min
difficulty: beginner
tags: dict, set, key, unique
---

A dictionary maps keys to values; a set stores unique elements.

## Dictionaries

```python
user = {"name": "Anna", "age": 21}
print(user["name"])     # Anna
user["city"] = "Moscow" # add
user["age"] = 22        # update
```

## Dict methods

```python
user.get("email", "none")   # safe read
user.keys(), user.values(), user.items()
```

## Iterating a dict

```python
for key, value in user.items():
    print(key, value)
```

## Sets

```python
s = {1, 2, 2, 3}
print(s)          # {1, 2, 3}
s.add(4)
s.discard(1)
```

## Set operations

```python
a = {1, 2, 3}; b = {2, 3, 4}
a | b   # union
a & b   # intersection
a - b   # difference
```

## When to use

- Dict — look up by key quickly.
- Set — check membership and deduplicate.

## Lesson summary

We learned dicts and sets: creation, methods, iteration, and set algebra.

<!--TASK-->
### Task 1 — Build a dict
Create a dict with your name, age and city. Print each value by key.

### Task 2 — Update and add
From a base dict, add a key and update another; print the final dict.

### Task 3 — get() safety
Print user.get("email", "no email") when the key is absent.

### Task 4 — Loop over items
Loop over the dict and print "key: value" for each pair.

### Task 5 — Deduplicate with set
Given [1,2,2,3,3,3], build a set and print unique values sorted.

### Task 6 — Set operations
For a={1,2,3}, b={2,3,4} print union, intersection and difference.

### Task 7 — Membership
Write a program that reads a word and prints whether it is in a set of know words.
<!--/TASK-->

<!--HINT-->
### Hint 1
Access via user["name"]; keys must be unique.

### Hint 2
Assigning a new key adds; assigning existing updates.

### Hint 3
get(key, default) never raises.

### Hint 4
for k, v in d.items() gives pairs.

### Hint 5
set(lst) removes duplicates; sorted() sorts.

### Hint 6
Operators |, &, - work on sets.

### Hint 7
Use `word in words_set`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
me = {"name": "Anna", "age": 21, "city": "Moscow"}
print(me["name"], me["age"], me["city"])
```

### Solution 2
```python
d = {"a": 1, "b": 2}
d["c"] = 3
d["b"] = 20
print(d)   # {'a': 1, 'b': 20, 'c': 3}
```

### Solution 3
```python
print(me.get("email", "no email"))   # no email
```

### Solution 4
```python
for k, v in me.items():
    print(f"{k}: {v}")
```

### Solution 5
```python
lst = [1, 2, 2, 3, 3, 3]
unique = set(lst)
print(sorted(unique))   # [1, 2, 3]
```

### Solution 6
```python
a = {1, 2, 3}
b = {2, 3, 4}
print(a | b)   # {1, 2, 3, 4}
print(a & b)   # {2, 3}
print(a - b)   # {1}
```

### Solution 7
```python
known = {"python", "java", "go"}
word = input("Word: ").lower()
print(word in known)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a dict?
- Key-value pairs
- An ordered list
- A set
- A function
* Correct answer: Key-value pairs
Keys map to values.

How to read a value?
- d["key"]
- d("key")
- d.key
- d.get? both
* Correct answer: d["key"]
Bracket access by key.

What does get(key, default) do?
- Returns default if key missing
- Always raises
- Adds the key
- Deletes the key
* Correct answer: Returns default if key missing
Safe read.

How to iterate keys and values?
- for k, v in d.items()
- for k in d.values()
- for v in d.keys()
- for each in d
* Correct answer: for k, v in d.items()
items gives pairs.

What is a set?
- Unique elements
- Ordered pairs
- A dict
- A tuple
* Correct answer: Unique elements
Duplicates are removed.

What is {1,2,2,3}?
- {1, 2, 3}
- {1, 2, 2, 3}
- [1, 2, 3]
- Error
* Correct answer: {1, 2, 3}
Set deduplicates.

What is union?
- a | b
- a & b
- a - b
- a ^ b
* Correct answer: a | b
All elements of both.

What is intersection?
- a & b
- a | b
- a - b
- a + b
* Correct answer: a & b
Elements in both.

What is difference?
- a - b
- a & b
- a | b
- a ^ b
* Correct answer: a - b
In a but not in b.

How to add to a set?
- s.add(x)
- s.append(x)
- s.insert(x)
- s[x] = 1
* Correct answer: s.add(x)
add works for sets.

Which is faster for membership?
- set
- list
- tuple? same
- str
* Correct answer: set
Average O(1).

What does d.keys() return?
- Keys view
- Values
- Pairs
- A list
* Correct answer: Keys view
Iterable of keys.
<!--/QUIZ-->
