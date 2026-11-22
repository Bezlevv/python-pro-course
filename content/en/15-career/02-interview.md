---
title: Interviews: algorithms and questions
summary: What is asked, how to prepare.
order: 2
duration: 50 min
difficulty: intermediate
tags: interview, algorithms
---

Interviews check problem solving and communication.

## Typical tasks

- Reversing strings/lists;
- Two-sum, sorting;
- OOP design;
- Databases and SQL.

## Approach

1. Clarify;
2. Discuss approach and complexity;
3. Code;
4. Test mentally.

## Questions

Explain Python, GIL, OOP, HTTP, SQL.

## Lesson summary

Think aloud, plan, then code.

<!--TASK-->
### Task 1 — Reverse
Reverse a string.

### Task 2 — Two-sum
Solve two-sum.

### Task 3 — Duplicates
Find duplicates.

### Task 4 — Explain
Explain your approach in 3 steps.

### Task 5 — Complexity
State complexity.

### Task 6 — Question
Answer: what is the GIL?

### Task 7 — Mock
Describe a mock interview plan.
<!--/TASK-->

<!--HINT-->
### Hint 1
s[::-1].

### Hint 2
Dict.

### Hint 3
set.

### Hint 4
Clarify.

### Hint 5
Big O.

### Hint 6
Global interpreter lock.

### Hint 7
Practice.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
def reverse_string(s):
    return s[::-1]
```

### Solution 2
```python
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []
```

### Solution 3
```python
def find_duplicates(nums):
    seen = set()
    result = []
    for x in nums:
        if x in seen:
            result.append(x)
        else:
            seen.add(x)
    return result
```

### Solution 4
```python
# 1. Уточняю формат ввода/вывода
# 2. Предлагаю решение и сложность
# 3. Пишу код и проверяю на примере
```

### Solution 5
```python
# two_sum со словарём: O(n) времени, O(n) памяти
```

### Solution 6
```python
# GIL — глобальная блокировка интерпретатора:
# один поток Python выполняется за раз;
# для CPU-задач используют multiprocessing
```

### Solution 7
```python
# Ежедневно 1 задача + разбор,
# неделя — OOP/БД/сеть, финальные мок-интервью
```
<!--/SOLUTION-->

<!--QUIZ-->
What is two-sum?
- Find pair summing to target
- Sort
- Reverse
- None
* Correct answer: Find pair summing to target
Classic.

What is the dict trick?
- O(n) lookup
- O(n²)
- Sorting
- None
* Correct answer: O(n) lookup
Hash.

What is a set for?
- Duplicates
- Sorting
- Length
- None
* Correct answer: Duplicates
Unique.

What is the GIL?
- Global interpreter lock
- Garbage
- A package
- None
* Correct answer: Global interpreter lock
Threads.

What is multiprocessing?
- Separate processes
- Threads
- Async
- None
* Correct answer: Separate processes
CPU.

What is a complexity?
- Growth rate
- Length
- Speed
- None
* Correct answer: Growth rate
Big O.

What is clarify?
- Ask questions
- Guess
- Code
- None
* Correct answer: Ask questions
First.

What is think aloud?
- Explain reasoning
- Stay silent
- Skip
- None
* Correct answer: Explain reasoning
Interview.

What is an edge case?
- Empty/one item
- Normal
- Large
- None
* Correct answer: Empty/one item
Check.

What is a mock?
- Practice interview
- Real job
- A test
- None
* Correct answer: Practice interview
Prepare.

What is OOP?
- Object-oriented programming
- Algorithm
- SQL
- None
* Correct answer: Object-oriented programming
Design.

What is the best approach?
- Clarify → plan → code → test
- Code fast
- Skip
- None
* Correct answer: Clarify → plan → code → test
Structured.
<!--/QUIZ-->
