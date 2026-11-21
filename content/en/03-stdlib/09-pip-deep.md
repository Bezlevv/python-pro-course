---
title: pip in depth
summary: Installing, upgrading, requirements variants, wheels, pipx and checks.
order: 9
duration: 40 min
difficulty: intermediate
tags: pip, requirements, wheel, pipx
---

pip is the classic Python installer; understanding it helps debug environments.

## Basics

```bash
pip install requests
pip install "requests==2.31.0"
pip install "requests>=2.0,<3.0"
pip uninstall requests
```

## requirements.txt

```bash
pip freeze > requirements.txt
pip install -r requirements.txt
```

## Wheel and download

```bash
pip download requests -d wheels
pip install --no-index --find-links wheels requests
```

## pipx

Run CLI tools in isolated environments:

```bash
pipx install ruff
```

## Checks

```bash
pip check
pip list --outdated
```

## Lesson summary

pip installs packages; freeze produces requirements; pipx isolates apps.

<!--TASK-->
### Task 1 — Install
Install requests and show pip show requests.

### Task 2 — Version spec
Install a pinned version like requests==2.31.0.

### Task 3 — Freeze
Freeze to requirements.txt and view content.

### Task 4 — Install from file
Create a new env and install -r requirements.txt.

### Task 5 — Download wheels
Download wheels of a package into a folder.

### Task 6 — Offline install
Install from the local wheels folder with --no-index.

### Task 7 — pipx
Install ruff via pipx and run it.
<!--/TASK-->

<!--HINT-->
### Hint 1
pip install requests; pip show requests.

### Hint 2
pip install "requests==2.31.0".

### Hint 3
pip freeze > requirements.txt; type.

### Hint 4
pip install -r requirements.txt.

### Hint 5
pip download -d wheels requests.

### Hint 6
pip install --no-index --find-links wheels requests.

### Hint 7
pipx install ruff; ruff --version.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```bash
pip install requests
pip show requests
```

### Solution 2
```bash
pip install "requests==2.31.0"
```

### Solution 3
```bash
pip freeze > requirements.txt
type requirements.txt
```

### Solution 4
```bash
python -m venv .venv2
.venv2\Scripts\activate
pip install -r requirements.txt
```

### Solution 5
```bash
pip download requests -d wheels
ls wheels
```

### Solution 6
```bash
pip install --no-index --find-links wheels requests
```

### Solution 7
```bash
pipx install ruff
ruff --version
```
<!--/SOLUTION-->

<!--QUIZ-->
What does pip install do?
- Installs packages
- Uninstalls
- Lists
- Freezes
* Correct answer: Installs packages
From PyPI.

What is a version spec?
- "requests==2.31.0"
- requests
- pip
- list
* Correct answer: "requests==2.31.0"
Pinned.

What does pip freeze do?
- Prints installed with versions
- Installs
- Downloads
- Checks
* Correct answer: Prints installed with versions
For requirements.

What does pip install -r do?
- Installs from requirements.txt
- Removes
- Freezes
- Shows
* Correct answer: Installs from requirements.txt
Batch.

What is a wheel?
- Built package format
- Installer
- Repo
- Env
* Correct answer: Built package format
.whl.

What does pip download do?
- Saves packages without installing
- Installs
- Removes
- Checks
* Correct answer: Saves packages without installing
For offline.

What does --no-index do?
- Blocks PyPI
- Enables
- Uses wheels
- Nothing
* Correct answer: Blocks PyPI
Local only.

What does --find-links do?
- Uses a local folder
- Ignores
- Deletes
- Uploads
* Correct answer: Uses a local folder
Source.

What is pipx?
- Runs tools in isolated envs
- Installs libraries
- A pip fork
- A lock
* Correct answer: Runs tools in isolated envs
For CLI apps.

What does pip check do?
- Verifies dependencies
- Updates
- Removes
- Installs
* Correct answer: Verifies dependencies
Finds conflicts.

What does pip list --outdated show?
- Outdated packages
- All installed
- Removed
- None
* Correct answer: Outdated packages
Update candidates.

Why pin versions?
- Reproducibility
- Speed
- Size
- Style
* Correct answer: Reproducibility
Stable builds.
<!--/QUIZ-->
