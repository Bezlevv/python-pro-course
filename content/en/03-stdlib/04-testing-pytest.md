---
title: Testing with pytest
summary: Writing tests, assertions, fixtures, parametrize and running pytest.
order: 4
duration: 40 min
difficulty: intermediate
tags: pytest, tests, fixtures, parametrize
---

pytest is a popular testing framework with simple syntax and rich plugins.

## First test

```python
# test_math.py
def test_add():
    assert 2 + 2 == 4
```

Run: `pytest` in the terminal.

## Assertions

Plain `assert` statements: pytest explains failures well.

## Fixtures

```python
import pytest

@pytest.fixture
def sample_list():
    return [1, 2, 3]

def test_len(sample_list):
    assert len(sample_list) == 3
```

## Parametrize

```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add(a, b, expected):
    assert a + b == expected
```

## Running

```bash
pytest
pytest -v
pytest test_math.py
```

## Lesson summary

pytest uses functions, assert, fixtures, parametrize; `pytest -v` shows results.

<!--TASK-->
### Task 1 — Simple test
Write test_add asserting 1+1 == 2; run pytest.

### Task 2 — Fixture
Create fixture data() returning [1,2,3]; test its length.

### Task 3 — Parametrize
Parametrize test_multiply for (2,3,6), (0,5,0), (-1,4,-4).

### Task 4 — Failure read
Write a deliberately failing test; run pytest and read the failure line.

### Task 5 — Exception test
Write a test expecting ValueError using pytest.raises.

### Task 6 — tmp_path fixture
Write a test that writes to tmp_path and asserts file content.

### Task 7 — Fixture scope
Create a session-scoped fixture and test that it runs once.
<!--/TASK-->

<!--HINT-->
### Hint 1
def test_add(): assert 1+1 == 2.

### Hint 2
@pytest.fixture; function takes it.

### Hint 3
@pytest.mark.parametrize("a,b,expected", [...]).

### Hint 4
Assert wrong value; observe report.

### Hint 5
with pytest.raises(ValueError): ...

### Hint 6
tmp_path / "f.txt".

### Hint 7
@pytest.fixture(scope="session").
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
def test_add():
    assert 1 + 1 == 2
```

### Solution 2
```python
import pytest

@pytest.fixture
def data():
    return [1, 2, 3]

def test_len(data):
    assert len(data) == 3
```

### Solution 3
```python
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 6),
    (0, 5, 0),
    (-1, 4, -4),
])
def test_multiply(a, b, expected):
    assert a * b == expected
```

### Solution 4
```python
def test_fail():
    assert 1 == 2   # intentionally failing
```

### Solution 5
```python
import pytest

def test_raises():
    with pytest.raises(ValueError):
        int("abc")
```

### Solution 6
```python
def test_tmp(tmp_path):
    f = tmp_path / "data.txt"
    f.write_text("hi", encoding="utf-8")
    assert f.read_text(encoding="utf-8") == "hi"
```

### Solution 7
```python
@pytest.fixture(scope="session")
def once():
    return "session"
```
<!--/SOLUTION-->

<!--QUIZ-->
What does pytest discover?
- Functions named test_*
- Classes named Test
- Any function
- Only classes
* Correct answer: Functions named test_*
Convention.

What is an assertion?
- assert condition
- if condition
- return
- print
* Correct answer: assert condition
Checks truthiness.

What is a fixture?
- Prepared test input
- A test
- A module
- A plug
* Correct answer: Prepared test input
@pytest.fixture.

What does parametrize do?
- Runs test with multiple inputs
- Skips tests
- Marks slow
- Selects
* Correct answer: Runs test with multiple inputs
Matrix.

What is pytest.raises for?
- Checking an exception
- Catching silently
- Logging
- Skipping
* Correct answer: Checking an exception
Context manager.

What is tmp_path?
- Temporary directory per test
- Project dir
- Home
- /tmp global
* Correct answer: Temporary directory per test
Unique.

How to run with verbose?
- pytest -v
- pytest -q
- pytest --verbose? both
- pytest run
* Correct answer: pytest -v
Detailed output.

What does -v add?
- Test names/status
- Speed
- Coverage
- Nothing
* Correct answer: Test names/status
Verbose.

What is scope="session"?
- Fixture runs once per session
- Per test
- Per module
- Never
* Correct answer: Fixture runs once per session
Shared.

Where to place tests?
- test_*.py files
- Anywhere
- main.py
- config
* Correct answer: test_*.py files
Discovered by pytest.

Does pytest need classes?
- No, functions are enough
- Yes, always
- Only unittest
- Never
* Correct answer: No, functions are enough
Function style.

What happens on assertion failure?
- Test fails with report
- Program stops
- Nothing
- Retry
* Correct answer: Test fails with report
pytest continues others.
<!--/QUIZ-->
