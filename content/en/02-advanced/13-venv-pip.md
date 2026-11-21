---
title: venv, pip, requirements.txt
summary: Virtual environments, package management, freeze and reproducible installs.
order: 13
duration: 45 min
difficulty: intermediate
tags: venv, pip, requirements, packages
---

A virtual environment isolates project dependencies.

## Creating and activating

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

## pip basics

```bash
pip install requests
pip uninstall requests
pip list
pip show requests
```

## requirements.txt

```bash
pip freeze > requirements.txt
```

Then restore:

```bash
pip install -r requirements.txt
```

## Pip best practices

- always use a venv;
- commit requirements.txt;
- pin versions or use ranges;
- upgrade carefully.

## Lesson summary

venv isolates environments; pip manages packages; requirements.txt makes installs reproducible.

<!--TASK-->
### Task 1 — Create venv
Create .venv using python -m venv; activate it; print sys.executable inside.

### Task 2 — Install
Install requests inside the venv and show its version with pip show.

### Task 3 — Freeze
Freeze the environment to requirements.txt and show its content.

### Task 4 — Restore
Create a new venv and install from requirements.txt; verify requests is importable.

### Task 5 — List
Use pip list and count installed packages.

### Task 6 — Uninstall
Uninstall requests and show that import fails afterwards.

### Task 7 — Best practices
Write a short script that prints the current env path and pip version.
<!--/TASK-->

<!--HINT-->
### Hint 1
python -m venv .venv; activate.

### Hint 2
pip install requests; pip show requests.

### Hint 3
pip freeze > requirements.txt.

### Hint 4
python -m venv .venv2; install -r.

### Hint 5
pip list | measure or print.

### Hint 6
pip uninstall -y requests.

### Hint 7
import sys; print(sys.prefix); subprocess for pip.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```bash
python -m venv .venv
.venv\Scripts\activate
```
```python
import sys
print(sys.executable)   # path inside .venv
```

### Solution 2
```bash
pip install requests
pip show requests
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
python -c "import requests; print(requests.__version__)"
```

### Solution 5
```bash
pip list
```

### Solution 6
```bash
pip uninstall -y requests
python -c "import requests"   # ModuleNotFoundError
```

### Solution 7
```python
import sys
print("Env:", sys.prefix)
import subprocess
print(subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True, text=True).stdout.strip())
```
<!--/SOLUTION-->

<!--QUIZ-->
What does venv do?
- Isolates dependencies
- Speeds up Python
- Installs packages
- Compiles
* Correct answer: Isolates dependencies
Separate site-packages.

How to create a venv?
- python -m venv .venv
- pip venv
- python venv
- create venv
* Correct answer: python -m venv .venv
Standard command.

How to activate on Windows?
- .venv\Scripts\activate
- source .venv/bin/activate
- venv start
- activate .venv
* Correct answer: .venv\Scripts\activate
Windows path.

What does pip install do?
- Installs a package
- Uninstalls
- Lists
- Upgrades pip
* Correct answer: Installs a package
From PyPI.

What does pip freeze output?
- Installed packages with versions
- Installed only names
- Python version
- Paths
* Correct answer: Installed packages with versions
For requirements.txt.

How to restore dependencies?
- pip install -r requirements.txt
- pip freeze
- pip list
- pip install .
* Correct answer: pip install -r requirements.txt
Reproducible install.

Why pin versions?
- Reproducibility
- Speed
- Memory
- Network
* Correct answer: Reproducibility
Same versions.

What does pip uninstall -y do?
- Removes without asking
- Installs
- Lists
- Fails
* Correct answer: Removes without asking
-y flag skips confirmation.

Where are packages stored in a venv?
- .venv/Lib/site-packages
- System global
- Home
- Temp
* Correct answer: .venv/Lib/site-packages
Isolated location.

Should requirements.txt be committed?
- Yes
- No
- Only some
- Never
* Correct answer: Yes
Helps teammates.

What is sys.prefix?
- Path of the current environment
- Python version
- Package list
- Home
* Correct answer: Path of the current environment
Shows the venv path.

What happens if a package is missing?
- ModuleNotFoundError
- ImportError both
- Nothing
- Warning
* Correct answer: ModuleNotFoundError
When importing.
<!--/QUIZ-->
