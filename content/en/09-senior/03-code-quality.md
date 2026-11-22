---
title: Code quality: ruff, black, mypy, pre-commit
summary: Linters, formatters, type checkers and git hooks.
order: 3
duration: 45 min
difficulty: intermediate
tags: ruff, black, mypy, pre-commit
---

Quality tools catch issues before review.

## ruff

```bash
pip install ruff
ruff check .
ruff format .
```

## black

```bash
pip install black
black .
```

## mypy

```bash
pip install mypy
mypy --strict file.py
```

```python
def greet(name: str) -> str:
    return "Hello, " + name
```

## pre-commit

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
```

```bash
pip install pre-commit
pre-commit install
```

## Lesson summary

ruff/black/mypy + pre-commit automate quality.

<!--TASK-->
### Task 1 — ruff
Run ruff check on a file with an unused import.

### Task 2 — format
Run ruff format and show changes.

### Task 3 — mypy
Add annotations and run mypy.

### Task 4 — mypy error
Call greet(42) and see the error.

### Task 5 — pre-commit config
Write a minimal config.

### Task 6 — install
Run pre-commit install.

### Task 7 — chain
Describe what runs before each commit.
<!--/TASK-->

<!--HINT-->
### Hint 1
ruff check.

### Hint 2
ruff format.

### Hint 3
mypy.

### Hint 4
Type error.

### Hint 5
YAML.

### Hint 6
pre-commit install.

### Hint 7
Lint + format + types.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```bash
pip install ruff
ruff check .
```
F401: unused import.

### Solution 2
```bash
ruff format .
```

### Solution 3
```python
def greet(name: str) -> str:
    return "Hello, " + name
```
```bash
mypy file.py
```

### Solution 4
```python
print(greet(42))
```
```bash
mypy --strict file.py
# error: Argument 1 has incompatible type "int"; expected "str"
```

### Solution 5
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
```

### Solution 6
```bash
pip install pre-commit
pre-commit install
```

### Solution 7
```python
# Перед коммитом: линт, форматирование, типы, тесты
```
<!--/SOLUTION-->

<!--QUIZ-->
What does ruff do?
- Lints and formats
- Types
- Tests
- None
* Correct answer: Lints and formats
Fast.

What is F401?
- Unused import
- Syntax
- Type
- None
* Correct answer: Unused import
Rule.

What does black do?
- Formats code
- Lints
- Types
- None
* Correct answer: Formats code
Style.

What does mypy do?
- Checks types
- Lints
- Formats
- None
* Correct answer: Checks types
Static.

What is an annotation?
- name: str
- A comment
- A docstring
- None
* Correct answer: name: str
Hint.

What is --strict?
- Strict mypy
- Fast
- Quiet
- None
* Correct answer: Strict mypy
All checks.

What is pre-commit?
- Git hooks
- A linter
- A formatter
- None
* Correct answer: Git hooks
Automation.

What is a hook?
- Runs before commit
- A test
- A file
- None
* Correct answer: Runs before commit
Gate.

What does pre-commit install do?
- Installs hooks
- Runs tests
- Deletes
- None
* Correct answer: Installs hooks
Setup.

What is a repo in config?
- Hook source
- A git repo
- A file
- None
* Correct answer: Hook source
Download.

Why automate quality?
- Consistency
- Speed
- Style
- None
* Correct answer: Consistency
Team.

What runs first usually?
- ruff
- pytest? after
- mypy? after
- All
* Correct answer: ruff
Lint.
<!--/QUIZ-->
