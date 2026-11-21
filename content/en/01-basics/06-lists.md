---
title: Lists and slices
summary: Creating lists, indexing, methods, iteration, slicing and copies.
order: 6
duration: 30 min
difficulty: beginner
tags: lists, slicing, methods, index
---

A list is an ordered mutable collection: you can add, remove and change elements.

## Creating lists

```python
nums = [1, 2, 3]
mixed = [1, "two", 3.0, True]
empty = []
```

## Indexing

Indexes start at 0; negative indexes count from the end:

```python
print(nums[0])    # 1
print(nums[-1])   # 3
```

## Useful methods

```python
nums.append(4)      # add to the end
nums.insert(0, 0)   # insert at position
nums.remove(2)      # remove by value
nums.pop()          # remove the last
nums.sort()         # sort in place
len(nums)
```

## Slices

```python
print(nums[1:3])   # from index 1 to 2
print(nums[:2])    # first two
print(nums[::2])   # every second
```

## Iteration

```python
for x in nums:
    print(x)
```

## Copying

`b = a` does not copy; both names refer to the same list. Use `a.copy()` or `a[:]`.

## Lesson summary

We learned to create lists, access by index, use methods, slice, and copy correctly.

<!--TASK-->
### Task 1 — Build a list
Create a list of the first five even numbers. Print it and its length.

### Task 2 — Indexing
For the list [10, 20, 30, 40], print index 0, index -1, index 2.

### Task 3 — Append and insert
Start with [1, 2, 3]. Append 4, insert 0 at the start. Print the result.

### Task 4 — Remove and pop
From [5, 10, 15, 10], remove value 10 once, then pop the last. Print the result.

### Task 5 — Slices
For [0,1,2,3,4,5,6,7,8,9] print: first 3, elements 3..5, every second element, the reversed list.

### Task 6 — Sum via loop
Given [3, 7, 2, 9], compute the sum with a loop and print it (also compare with sum()).

### Task 7 — Copy safety
Create a = [1,2,3]; b = a; b.append(4). Print a — explain why a changed. Then use copy() and show it is independent.
<!--/TASK-->

<!--HINT-->
### Hint 1
Evens: [2,4,6,8,10]; len() gives the count.

### Hint 2
Use positive and negative indexes.

### Hint 3
append adds; insert(pos, value) places at index.

### Hint 4
remove deletes the first occurrence; pop removes the last (or by index).

### Hint 5
Slices: [start:stop:step]; [::-1] reverses.

### Hint 6
total = 0; for x in lst: total += x.

### Hint 7
b = a shares the object; a.copy() creates a new list.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
evens = [2, 4, 6, 8, 10]
print(evens)          # [2, 4, 6, 8, 10]
print(len(evens))     # 5
```

### Solution 2
```python
lst = [10, 20, 30, 40]
print(lst[0])   # 10
print(lst[-1])  # 40
print(lst[2])   # 30
```

### Solution 3
```python
lst = [1, 2, 3]
lst.append(4)
lst.insert(0, 0)
print(lst)   # [0, 1, 2, 3, 4]
```

### Solution 4
```python
lst = [5, 10, 15, 10]
lst.remove(10)   # removes first 10
lst.pop()        # removes last
print(lst)       # [5, 15]
```

### Solution 5
```python
lst = list(range(10))
print(lst[:3])      # [0, 1, 2]
print(lst[3:6])     # [3, 4, 5]
print(lst[::2])     # [0, 2, 4, 6, 8]
print(lst[::-1])    # [9, 8, ..., 0]
```

### Solution 6
```python
lst = [3, 7, 2, 9]
total = 0
for x in lst:
    total += x
print(total)          # 21
print(sum(lst))       # 21
```

### Solution 7
```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)   # [1, 2, 3, 4] — same object!
c = a.copy()
c.append(5)
print(a)   # [1, 2, 3, 4]
print(c)   # [1, 2, 3, 4, 5]
```
b is a reference; copy() makes an independent list.
<!--/SOLUTION-->

<!--QUIZ-->
What is the first index?
- 0
- 1
- -1
- len
* Correct answer: 0
Indexes start at zero.

What is lst[-1]?
- The last element
- The first
- Error
- The second last
* Correct answer: The last element
Negative indexes go from the end.

What does append do?
- Adds to the end
- Inserts at index
- Removes
- Sorts
* Correct answer: Adds to the end
append(x) grows the list.

What does pop() do?
- Removes the last element and returns it
- Clears the list
- Adds an element
- Sorts
* Correct answer: Removes the last element and returns it
pop(index) removes that index.

What does [1:3] select?
- Elements at indexes 1 and 2
- Elements 1..3
- First three
- Last three
* Correct answer: Elements at indexes 1 and 2
End index is exclusive.

How to reverse a list?
- lst[::-1]
- lst.reverse? both
- lst[::1]
- lst[-1]
* Correct answer: lst[::-1]
Step -1 goes backwards.

What does b = a do?
- Makes b refer to the same list
- Copies the list
- Creates a tuple
- Error
* Correct answer: Makes b refer to the same list
No copy is made.

How to copy a list?
- a.copy()
- a = b
- list append
- cannot
* Correct answer: a.copy()
Creates a new list.

What is len([1,2,3])?
- 3
- 2
- 4
- 0
* Correct answer: 3
Length of the list.

What does lst.insert(1, 99) do?
- Puts 99 at index 1
- Replaces index 1
- Deletes 99
- Appends 99
* Correct answer: Puts 99 at index 1
Elements shift right.

Which loop prints all elements?
- for x in lst: print(x)
- for i in lst: print(i)? both
- print(lst)
- while lst: print(lst)
* Correct answer: for x in lst: print(x)
Iteration over the list.

What is sum([1,2,3])?
- 6
- 3
- 7
- 0
* Correct answer: 6
Built-in sum.
<!--/QUIZ-->
