---
title: Stacks, queues, deque, hash tables
summary: LIFO, FIFO, deque, dicts and sets.
order: 4
duration: 45 min
difficulty: intermediate
tags: stack, queue, deque, hash
---

Data structures organize access patterns.

## Stack (LIFO)

```python
stack = []
stack.append(1)
stack.append(2)
top = stack.pop()   # 2
```

## Queue (FIFO)

```python
from collections import deque
q = deque()
q.append(1)
q.append(2)
first = q.popleft()   # 1
```

## deque

Fast operations at both ends.

## Hash table (dict/set)

```python
d = {"a": 1}
d["b"] = 2
s = {1, 2, 3}
```

## Lesson summary

Pick structure by access pattern: stack, queue, or hash.

<!--TASK-->
### Task 1 — Stack
Implement push/pop with a list.

### Task 2 — Queue
Use deque for FIFO.

### Task 3 — Parentheses
Check balanced brackets with a stack.

### Task 4 — Dict
Count characters with a dict.

### Task 5 — Set
Remove duplicates with a set.

### Task 6 — deque
Append both sides.

### Task 7 — Choose
Choose a structure for history (undo).
<!--/TASK-->

<!--HINT-->
### Hint 1
append/pop.

### Hint 2
append/popleft.

### Hint 3
Pairs.

### Hint 4
d[c] = d.get(c, 0) + 1.

### Hint 5
set(xs).

### Hint 6
appendleft.

### Hint 7
Stack.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
stack = [1, 2, 3]
stack.append(4)
print(stack.pop())   # 4
```

### Solution 2
```python
from collections import deque
q = deque([1, 2, 3])
q.append(4)
print(q.popleft())   # 1
```

### Solution 3
```python
PAIRS = {")": "(", "]": "[", "}": "{"}

def balanced(s):
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in PAIRS:
            if not stack or stack.pop() != PAIRS[ch]:
                return False
    return not stack

print(balanced("([])"))   # True
print(balanced("([)]"))   # False
```

### Solution 4
```python
text = "abracadabra"
counts = {}
for ch in text:
    counts[ch] = counts.get(ch, 0) + 1
print(counts)
```

### Solution 5
```python
xs = [1, 2, 2, 3, 3, 3]
print(set(xs))
```

### Solution 6
```python
dq = deque([1, 2])
dq.appendleft(0)
dq.append(3)
print(list(dq))   # [0, 1, 2, 3]
```

### Solution 7
```python
# История отмен (undo) — LIFO → стек
```
<!--/SOLUTION-->

<!--QUIZ-->
What is LIFO?
- Last in, first out
- First in
- Random
- None
* Correct answer: Last in, first out
Stack.

What is FIFO?
- First in, first out
- Last in
- Random
- None
* Correct answer: First in, first out
Queue.

What is pop?
- Removes last
- Removes first
- Adds
- None
* Correct answer: Removes last
Stack.

What is popleft?
- Removes first
- Removes last
- Adds
- None
* Correct answer: Removes first
Queue.

What is deque?
- Double-ended queue
- List only
- Set
- None
* Correct answer: Double-ended queue
Fast both.

What is a hash table?
- Key → value
- Ordered list
- Stack
- None
* Correct answer: Key → value
dict.

What is a set?
- Unique items
- Ordered
- Duplicates
- None
* Correct answer: Unique items
No repeats.

What is O(1) access?
- dict/set
- list scan
- stack
- None
* Correct answer: dict/set
Average.

What is append?
- Add to end
- Add to start
- Remove
- None
* Correct answer: Add to end
Both.

What is the undo structure?
- Stack
- Queue
- Set
- None
* Correct answer: Stack
LIFO.

What is balanced brackets?
- Matching pairs
- Sorted
- Counted
- None
* Correct answer: Matching pairs
Stack.

What is d.get(c, 0)?
- Safe read
- Error
- Delete
- None
* Correct answer: Safe read
Default.
<!--/QUIZ-->
