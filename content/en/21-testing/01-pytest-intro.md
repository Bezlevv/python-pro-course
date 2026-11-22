---
title: Why tests and pytest basics
summary: Test structure, assert, running.
order: 1
duration: 40 min
difficulty: intermediate
tags: testing, pytest
---

Tests prove code works and keep it working.

## pytest

```python
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
```

## Run

```bash
pytest
pytest test_file.py -v
```

## Lesson summary

Small test functions with assert.

<!--TASK-->
### Task 1 — Function
Write add().

### Task 2 — Test
Write test_add.

### Task 3 — Fail
Write a deliberately failing test and see it fail.

### Task 4 — Run
Run pytest.

### Task 5 — Verbose
Use -v.

### Task 6 — Edge
Test edge cases (negative, zero).

### Task 7 — Naming
Explain test_ conventions.
<!--/TASK-->

<!--HINT-->
### Hint 1
def add.

### Hint 2
assert.

### Hint 3
Fails.

### Hint 4
pytest.

### Hint 5
-v.

### Hint 6
Extremes.

### Hint 7
Prefix.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
def add(a, b):
    return a + b
```

### Solution 2
```python
def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
```

### Solution 3
```python
def test_fail():
    assert add(2, 2) == 5   # упадёт
```

### Solution 4
```bash
pytest
```

### Solution 5
```bash
pytest -v
```

### Solution 6
```python
def test_edges():
    assert add(0, 0) == 0
    assert add(-5, 5) == 0
```

### Solution 7
```python
# Функции тестов начинаются с test_,
# файлы — test_*.py, классы — Test*
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a test?
- Verification
- A feature
- A bug
- None
* Correct answer: Verification
Check.

What is assert?
- Condition check
- Loop
- Import
- None
* Correct answer: Condition check
Equality.

What is pytest?
- Test framework
- A linter
- A debugger
- None
* Correct answer: Test framework
Runner.

What is a passing test?
- Green
- Red
- Skip
- None
* Correct answer: Green
OK.

What is a failing test?
- Red
- Green
- Skip
- None
* Correct answer: Red
Problem.

What is -v?
- Verbose
- Version
- Validate
- None
* Correct answer: Verbose
Details.

What is an edge case?
- Extreme input
- Normal
- Empty only
- None
* Correct answer: Extreme input
Zero/negative.

What is a suite?
- Test collection
- One test
- A file
- None
* Correct answer: Test collection
Run.

What is discovery?
- Finds tests
- Runs one
- Installs
- None
* Correct answer: Finds tests
test_.

What is a report?
- Results
- Code
- Assert
- None
* Correct answer: Results
Passed.

What is regression?
- Breakage
- Improvement
- New feature
- None
* Correct answer: Breakage
Protect.

Why test?
- Confidence
- Speed
- Style
- None
* Correct answer: Confidence
Safety.
<!--/QUIZ-->
