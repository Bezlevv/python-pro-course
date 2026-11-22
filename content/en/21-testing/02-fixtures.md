---
title: Fixtures and parametrization
summary: Setup/shared data, multiple cases.
order: 2
duration: 40 min
difficulty: intermediate
tags: pytest, fixtures
---

Fixtures and parametrization keep tests clean.

## Fixture

```python
import pytest

@pytest.fixture
def data():
    return {"x": 1, "y": 2}

def test_uses_fixture(data):
    assert data["x"] + data["y"] == 3
```

## Parametrize

```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

## Lesson summary

Fixtures share setup; parametrize broadens cases.

<!--TASK-->
### Task 1 — Fixture
Create a simple fixture.

### Task 2 — Use
Use it in a test.

### Task 3 — Parametrize
Three cases for add.

### Task 4 — Scope
Explain scope="module".

### Task 5 — Temp
Use tmp_path fixture.

### Task 6 — Cleanup
yield after setup.

### Task 7 — Combine
Parametrize + fixture together.
<!--/TASK-->

<!--HINT-->
### Hint 1
@pytest.fixture.

### Hint 2
Argument.

### Hint 3
parametrize.

### Hint 4
Once per module.

### Hint 5
tmp_path.

### Hint 6
yield.

### Hint 7
Both.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import pytest

@pytest.fixture
def data():
    return {"x": 1, "y": 2}
```

### Solution 2
```python
def test_fixture(data):
    assert data["x"] == 1
```

### Solution 3
```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

### Solution 4
```python
# scope="module" — фикстура создаётся один раз
# на весь модуль, а не на каждый тест
```

### Solution 5
```python
def test_write(tmp_path):
    f = tmp_path / "data.txt"
    f.write_text("hi")
    assert f.read_text() == "hi"
```

### Solution 6
```python
@pytest.fixture
def resource():
    res = open_resource()
    yield res
    res.close()   # cleanup после теста
```

### Solution 7
```python
@pytest.mark.parametrize("key", ["x", "y"])
def test_data_keys(data, key):
    assert key in data
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a fixture?
- Shared setup
- A test
- An assert
- None
* Correct answer: Shared setup
Data.

What is the decorator?
- @pytest.fixture
- def
- import
- None
* Correct answer: @pytest.fixture
Mark.

What is parametrize?
- Multiple cases
- One case
- Setup
- None
* Correct answer: Multiple cases
Loop.

What is scope?
- Lifetime
- Name
- Type
- None
* Correct answer: Lifetime
Module/function.

What is tmp_path?
- Temp dir
- A file
- A fixture name
- None
* Correct answer: Temp dir
Path.

What is yield?
- Cleanup point
- End
- Error
- None
* Correct answer: Cleanup point
After.

What is a parameter?
- Case input
- Assert
- Fixture
- None
* Correct answer: Case input
a, b.

What is expected?
- Desired output
- Input
- Error
- None
* Correct answer: Desired output
Compare.

Why fixture?
- DRY
- Speed
- Style
- None
* Correct answer: DRY
Shared.

What is module scope?
- Once per file
- Per test
- Session
- None
* Correct answer: Once per file
Wide.

What is cleanup?
- After-work
- Setup
- Test
- None
* Correct answer: After-work
Close.

What is a table?
- Case list
- One case
- Fixture
- None
* Correct answer: Case list
Parametrize.
<!--/QUIZ-->
