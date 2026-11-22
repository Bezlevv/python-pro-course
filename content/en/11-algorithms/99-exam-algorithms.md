---
title: Exam: Algorithms and Data Structures
summary: A check of knowledge on complexity, sorting, searching, data structures, graphs, and dynamic programming.
order: 99
duration: 30 min
difficulty: advanced
tags: exam, algorithms
exam: true
---

<!--QUIZ-->
What does the notation O(n log n) mean?
- The algorithm performs exactly n log n operations
- Growth time is bounded above by the function n log n
- The algorithm always requires n log n memory
- n log n is the number of lines in the code
* Correct answer: Growth time is bounded above by the function n log n
Big-O describes the upper bound of time/memory growth, not the exact number of operations.

What is the complexity of binary search in a sorted array?
- O(1)
- O(n)
- O(log n)
- O(n log n)
* Correct answer: O(log n)
Each comparison discards half of the elements, so the number of steps is ~log2(n).

What does heapq.heappop(heap) do?
- Returns the maximum element
- Removes and returns the heap's minimum element
- Sorts the heap
- Adds an element to the heap
* Correct answer: Removes and returns the heap's minimum element
heapq implements a min-heap: heappop extracts the smallest element.

Which data structure is used to implement DFS?
- Queue
- Stack
- Heap
- Dictionary
* Correct answer: Stack
DFS goes deep — this matches the stack's LIFO order (in recursion the stack is implicit).

What is memoization?
- Storing results of subproblems for reuse
- Writing an algorithm in one line
- Input/output optimization
- A way to traverse a graph
* Correct answer: Storing results of subproblems for reuse
This is a key dynamic programming technique: don't recompute the same thing.

What is the average-case complexity of quicksort?
- O(n)
- O(log n)
- O(n log n)
- O(n²)
* Correct answer: O(n log n)
On average, quicksort splits the array in half and sorts recursively — O(n log n); in the worst case O(n²).

Which sorting algorithm is stable and runs in O(n log n) in the worst case?
- Bubble sort
- Merge sort
- Quicksort
- Shaker sort
* Correct answer: Merge sort
Merge sort guarantees O(n log n) and does not change the order of equal elements.

What is a sliding window?
- A technique that processes a fixed-length subarray in a single pass
- A window in a graphical interface
- A way to visualize a heap
- A special type of queue
* Correct answer: A technique that processes a fixed-length subarray in a single pass
The window slides across the array, reducing the complexity of enumerating subarrays.

What is the deque object from collections used for?
- For fast additions/removals from both ends
- Only as a FIFO queue
- Only as a stack
- For storing unique values
* Correct answer: For fast additions/removals from both ends
deque is a double-ended queue with O(1) at both ends.

In a graph of 100 vertices represented by adjacency lists, how much memory is needed in the worst case?
- O(100)
- O(100²)
- O(100 × average degree)
- O(1)
* Correct answer: O(100 × average degree)
Adjacency lists store edges — memory is proportional to the number of edges, not the square of the vertices.
<!--/QUIZ-->
