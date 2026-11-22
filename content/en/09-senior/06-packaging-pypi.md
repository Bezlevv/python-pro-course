---
title: Packaging and publishing on PyPI
summary: pyproject.toml, build, twine, versioning.
order: 6
duration: 45 min
difficulty: advanced
tags: packaging, pypi, twine
---

Package your code so others can pip install it.

## pyproject.toml

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "mypkg"
version = "0.1.0"
description = "Example package"
requires-python = ">=3.10"
dependencies = ["requests"]
```

## Build

```bash
pip install build twine
python -m build
```

## Check and publish

```bash
twine check dist/*
twine upload dist/*
```

## Versioning

Semantic versioning: MAJOR.MINOR.PATCH.

## Lesson summary

pyproject + build + twine publish a package.

<!--TASK-->
### Task 1 — pyproject
Create a minimal pyproject.toml.

### Task 2 — Package dir
Create mypkg/ with __init__.py and a function.

### Task 3 — Build
Run python -m build and list dist/.

### Task 4 — Twine check
Run twine check.

### Task 5 — Version
Explain MAJOR.MINOR.PATCH.

### Task 6 — Local install
pip install -e . and import.

### Task 7 — License
Add license metadata.
<!--/TASK-->

<!--HINT-->
### Hint 1
[project] fields.

### Hint 2
__init__.py.

### Hint 3
python -m build.

### Hint 4
twine check.

### Hint 5
Breaking/feature/fix.

### Hint 6
pip install -e .

### Hint 7
license = {text = "MIT"}.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "mypkg"
version = "0.1.0"
description = "Example package"
requires-python = ">=3.10"
dependencies = ["requests"]
```

### Solution 2
```python
# mypkg/__init__.py
def hello() -> str:
    return "Hello from mypkg"
```

### Solution 3
```bash
pip install build twine
python -m build
ls dist/
```

### Solution 4
```bash
twine check dist/*
```

### Solution 5
```python
# MAJOR: несовместимые изменения
# MINOR: новая функциональность
# PATCH: исправления
```

### Solution 6
```bash
pip install -e .
python -c "import mypkg; print(mypkg.hello())"
```

### Solution 7
```toml
[project]
license = { text = "MIT" }
```
<!--/SOLUTION-->

<!--QUIZ-->
What is pyproject.toml?
- Build metadata
- A test file
- A lock
- None
* Correct answer: Build metadata
PEP 621.

What is build-backend?
- Tool that builds
- A package
- A test
- None
* Correct answer: Tool that builds
Setuptools.

What does python -m build do?
- Creates dist/
- Installs
- Tests
- None
* Correct answer: Creates dist/
sdist + wheel.

What is twine?
- Upload/check tool
- A builder
- A linter
- None
* Correct answer: Upload/check tool
PyPI.

What is a wheel?
- Built package
- Source
- A test
- None
* Correct answer: Built package
Installable.

What is MAJOR?
- Breaking changes
- Tiny
- Fix
- None
* Correct answer: Breaking changes
Version.

What is MINOR?
- New features
- Breaking
- Fix
- None
* Correct answer: New features
Backward compatible.

What is PATCH?
- Bug fixes
- Features
- Breaking
- None
* Correct answer: Bug fixes
Small.

What does pip install -e do?
- Editable install
- Normal
- Uninstall
- None
* Correct answer: Editable install
Dev.

What is dist/?
- Build output
- Source
- Tests
- None
* Correct answer: Build output
Artifacts.

Why publish on PyPI?
- Easy installing
- Speed
- Style
- None
* Correct answer: Easy installing
pip install.

What is requires-python?
- Minimum Python
- A dependency
- A version
- None
* Correct answer: Minimum Python
Constraint.
<!--/QUIZ-->
