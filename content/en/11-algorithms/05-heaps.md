---
title: Heaps and priority queues
summary: heapq, heappush, heappop, nlargest.
order: 5
duration: 45 min
difficulty: advanced
tags: heap, heapq, priority queue
---

A heap keeps the smallest element quickly accessible.

## Basic heap

```python
import heapq

heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 1)
heapq.heappush(heap, 3)
print(heapq.heappop(heap))   # 1
```

## From a list

```python
data = [5, 1, 3]
heapq.heapify(data)
print(heapq.heappop(data))   # 1
```

## nlargest

```python
print(heapq.nlargest(2, [5, 1, 3]))
```

## Priority queue

Tuples (priority, item) work naturally.

## Lesson summary

Heaps give O(log n) push/pop and the min at top.

<!--TASK-->
### Task 1 — Push/pop
Push three values and pop the min.

### Task 2 — Heapify
Turn a list into a heap.

### Task 3 — nsmallest
Get the 2 smallest.

### Task 4 — Priority
Use (priority, task) tuples.

### Task 5 — Merge
Merge two sorted lists with heapq.merge.

### Task 6 — Max
Simulate max-heap with negatives.

### Task 7 — Median idea
Explain two heaps for median.
<!--/TASK-->

<!--HINT-->
### Hint 1
heappush/heappop.

### Hint 2
heapify.

### Hint 3
nsmallest.

### Hint 4
Tuples.

### Hint 5
merge().

### Hint 6
Negatives.

### Hint 7
Min+max.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import heapq
heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 1)
heapq.heappush(heap, 3)
print(heapq.heappop(heap))   # 1
```

### Solution 2
```python
data = [5, 1, 3]
heapq.heapify(data)
print(heapq.heappop(data))   # 1
```

### Solution 3
```python
print(heapq.nsmallest(2, [5, 1, 3]))   # [1, 3]
```

### Solution 4
```python
import heapq
q = []
heapq.heappush(q, (2, "task2"))
heapq.heappush(q, (1, "task1"))
heapq.heappush(q, (3, "task3"))
print(heapq.heappop(q))   # (1, 'task1')
```

### Solution 5
```python
a = [1, 3, 5]
b = [2, 4]
print(list(heapq.merge(a, b)))   # [1,2,3,4,5]
```

### Solution 6
```python
# Max-куча: кладём -x, возвращаем -heappop()
```

### Solution 7
```python
# Две кучи: max для меньшей половины, min для большей
# медиана — вершины куч
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a heap?
- Tree structure
- List only
- Queue only
- None
* Correct answer: Tree structure
Min at top.

What does heappush do?
- Adds an element
- Removes
- Sorts
- None
* Correct answer: Adds an element
O(log n).

What does heappop do?
- Removes min
- Removes max
- Adds
- None
* Correct answer: Removes min
Top.

What does heapify do?
- Turns list into heap
- Sorts fully
- Clears
- None
* Correct answer: Turns list into heap
In place.

What is nsmallest(k)?
- k smallest
- k largest
- Sorted all
- None
* Correct answer: k smallest
Heap.

What is a priority queue?
- Heap-based
- FIFO
- LIFO
- None
* Correct answer: Heap-based
Priorities.

What is a tuple in heap?
- (priority, item)
- Only ints
- Strings
- None
* Correct answer: (priority, item)
Order.

What is the top of a min-heap?
- Smallest
- Largest
- Random
- None
* Correct answer: Smallest
heap[0].

How to make a max-heap?
- Negate values
- Reverse
- Sort
- None
* Correct answer: Negate values
Trick.

What is merge()?
- Merges sorted iterables
- Sorts
- Splits
- None
* Correct answer: Merges sorted iterables
Efficient.

What is O(log n) for?
- heap operations
- Access
- Loop
- None
* Correct answer: heap operations
push/pop.

What is the median idea?
- Two heaps
- One heap
- Sort
- None
* Correct answer: Two heaps
Balanced.
<!--/QUIZ-->
