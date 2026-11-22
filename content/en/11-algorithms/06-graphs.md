---
title: Graphs: representation, DFS, BFS
summary: Adjacency lists, depth-first and breadth-first search.
order: 6
duration: 50 min
difficulty: advanced
tags: graphs, dfs, bfs
---

Graphs model connections between objects.

## Representation

```python
graph = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["D"],
    "D": [],
}
```

## DFS (stack/recursion)

```python
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited
```

## BFS (queue)

```python
from collections import deque

def bfs(graph, start):
    visited = {start}
    q = deque([start])
    order = []
    while q:
        node = q.popleft()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                q.append(neighbor)
    return order
```

## Lesson summary

Adjacency lists + DFS/BFS solve traversal.

<!--TASK-->
### Task 1 — Graph
Build an adjacency list of 5 nodes.

### Task 2 — DFS
Implement recursive DFS and print order.

### Task 3 — BFS
Implement BFS and print order.

### Task 4 — Has path
Check if there's a path between nodes.

### Task 5 — Cycle idea
Explain how to detect a cycle.

### Task 6 — Shortest
Why BFS gives shortest path in unweighted.

### Task 7 — Memory
Compare adjacency list vs matrix.
<!--/TASK-->

<!--HINT-->
### Hint 1
dict of lists.

### Hint 2
Visited set.

### Hint 3
deque.

### Hint 4
DFS.

### Hint 5
Back edges.

### Hint 6
Layers.

### Hint 7
Size.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
graph = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["D", "E"],
    "D": [],
    "E": [],
}
```

### Solution 2
```python
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited

print(dfs(graph, "A"))
```

### Solution 3
```python
from collections import deque

def bfs(graph, start):
    visited = {start}
    q = deque([start])
    order = []
    while q:
        node = q.popleft()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                q.append(neighbor)
    return order

print(bfs(graph, "A"))
```

### Solution 4
```python
def has_path(graph, start, target):
    return target in dfs(graph, start)
```

### Solution 5
```python
# Если при DFS встречаем уже посещённую вершину
# на текущем пути — в графе есть цикл
```

### Solution 6
```python
# BFS обходит слоями: первая встреча цели — кратчайший путь
```

### Solution 7
```python
# Список смежности: O(V + E) памяти
# Матрица: O(V²)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a graph?
- Nodes and edges
- A list
- A tree only
- None
* Correct answer: Nodes and edges
Connections.

What is an adjacency list?
- dict node → neighbors
- Matrix
- Set
- None
* Correct answer: dict node → neighbors
Compact.

What is DFS?
- Depth-first
- Breadth-first
- Both
- None
* Correct answer: Depth-first
Stack/recursion.

What is BFS?
- Breadth-first
- Depth-first
- Sort
- None
* Correct answer: Breadth-first
Queue.

What is a visited set?
- Prevents repeats
- Slows
- Optional
- None
* Correct answer: Prevents repeats
Avoid cycles.

What is a cycle?
- Repeating path
- A node
- An edge
- None
* Correct answer: Repeating path
Closed.

What uses a stack?
- DFS
- BFS
- Sort
- None
* Correct answer: DFS
LIFO.

What uses a queue?
- BFS
- DFS
- Both
- None
* Correct answer: BFS
FIFO.

When is BFS shortest?
- Unweighted
- Weighted
- Always
- Never
* Correct answer: Unweighted
Layers.

What is a neighbor?
- Adjacent node
- Parent
- Child
- None
* Correct answer: Adjacent node
Edge.

What is V and E?
- Vertices and edges
- Values
- Errors
- None
* Correct answer: Vertices and edges
Complexity.

What is a tree?
- Acyclic graph
- Cyclic
- Both
- None
* Correct answer: Acyclic graph
Special.
<!--/QUIZ-->
