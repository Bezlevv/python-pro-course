---
title: Mocks and monkeypatching
summary: Replace slow/external parts.
order: 3
duration: 45 min
difficulty: advanced
tags: mock, monkeypatch
---

Mocks substitute external dependencies.

## Simple

```python
def fetch(url):
    return requests.get(url).json()

def test_fetch(monkeypatch):
    class FakeResponse:
        def json(self):
            return {"ok": True}
    monkeypatch.setattr("module.requests.get",
                        lambda url: FakeResponse())
    assert fetch("http://x")["ok"] is True
```

## unittest.mock

```python
from unittest.mock import patch

with patch("module.requests.get") as mock_get:
    mock_get.return_value.json.return_value = {"ok": True}
    result = fetch("http://x")
```

## Lesson summary

Mocks isolate code from the outside world.

<!--TASK-->
### Task 1 — Why
Why mock?

### Task 2 — monkeypatch
Replace a function.

### Task 3 — Fake
Return a fake response.

### Task 4 — patch
Use unittest.mock.patch.

### Task 5 — Rvalue
Set return_value.

### Task 6 — Assert called
Check the call count.

### Task 7 — Error
Simulate failure.
<!--/TASK-->

<!--HINT-->
### Hint 1
External.

### Hint 2
setattr.

### Hint 3
Class.

### Hint 4
patch.

### Hint 5
return_value.

### Hint 6
assert_called_once.

### Hint 7
side_effect.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
# Внешние вызовы (сеть, БД, время)
# медленные и нестабильные — в тестах их подменяют
```

### Solution 2
```python
def test_fetch(monkeypatch):
    monkeypatch.setattr("module.requests.get",
                        lambda url: FakeResponse())
```

### Solution 3
```python
class FakeResponse:
    def json(self):
        return {"ok": True}
```

### Solution 4
```python
from unittest.mock import patch

with patch("module.requests.get") as mock_get:
    ...
```

### Solution 5
```python
mock_get.return_value.json.return_value = {"ok": True}
```

### Solution 6
```python
mock_get.assert_called_once()
mock_get.assert_called_with("http://x")
```

### Solution 7
```python
import requests
mock_get.side_effect = requests.ConnectionError("no net")
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a mock?
- Fake object
- Real call
- A test
- None
* Correct answer: Fake object
Substitute.

Why mock?
- Isolation
- Speed
- Style
- None
* Correct answer: Isolation
External.

What is monkeypatch?
- Replaces attribute
- Deletes
- Adds file
- None
* Correct answer: Replaces attribute
Fixture.

What is setattr?
- Sets attribute
- Gets
- Deletes
- None
* Correct answer: Sets attribute
Patch.

What is patch?
- Context manager
- A test
- A mock only
- None
* Correct answer: Context manager
unittest.

What is return_value?
- Mock result
- Input
- Error
- None
* Correct answer: Mock result
Fake.

What is side_effect?
- Raised/sequence
- Return
- Call
- None
* Correct answer: Raised/sequence
Error.

What is assert_called_once?
- One call check
- Zero
- Many
- None
* Correct answer: One call check
Verify.

What is a mock object?
- Replaceable double
- Real
- A class
- None
* Correct answer: Replaceable double
Magic.

What is a spy?
- Records calls
- Replaces
- Deletes
- None
* Correct answer: Records calls
Observe.

What is a stub?
- Fixed data
- Dynamic
- Error
- None
* Correct answer: Fixed data
Simple.

What is the risk?
- Over-mocking
- Under-testing
- Speed
- None
* Correct answer: Over-mocking
False confidence.
<!--/QUIZ-->
