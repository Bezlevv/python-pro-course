---
title: Git hooks and pre-commit
summary: Hooks, pre-commit config.
order: 3
duration: 45 min
difficulty: advanced
tags: git hooks
---

Hooks run commands at git events.

## Hook example

`.git/hooks/pre-commit`:

```bash
#!/bin/sh
python -m pytest -q || exit 1
```

## pre-commit

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.10.0
    hooks:
      - id: black
```

```bash
pip install pre-commit
pre-commit install
```

## Lesson summary

Hooks enforce quality before commits.

<!--TASK-->
### Task 1 — Hook
Write a pre-commit hook.

### Task 2 — Permissions
chmod +x.

### Task 3 — Config
Add black.

### Task 4 — Install
pre-commit install.

### Task 5 — Run
Run on all files.

### Task 6 — Skip
Skip hooks.

### Task 7 — Ideas
What else to run?
<!--/TASK-->

<!--HINT-->
### Hint 1
.sh.

### Hint 2
+x.

### Hint 3
yaml.

### Hint 4
install.

### Hint 5
run --all-files.

### Hint 6
--no-verify.

### Hint 7
Lint.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```bash
#!/bin/sh
python -m pytest -q || exit 1
```

### Solution 2
```bash
chmod +x .git/hooks/pre-commit
```

### Solution 3
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.10.0
    hooks:
      - id: black
```

### Solution 4
```bash
pip install pre-commit
pre-commit install
```

### Solution 5
```bash
pre-commit run --all-files
```

### Solution 6
```bash
git commit --no-verify -m "urgent"
```

### Solution 7
```text
ruff, mypy, pytest, проверка секретов (gitleaks)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a hook?
- Git event script
- A file
- A branch
- None
* Correct answer: Git event script
pre-commit.

What is pre-commit?
- Before commit
- After
- Before push
- None
* Correct answer: Before commit
Event.

What is post-commit?
- After commit
- Before
- Push
- None
* Correct answer: After commit
Cleanup.

What is black?
- Formatter
- Linter
- Tester
- None
* Correct answer: Formatter
Style.

What is ruff?
- Linter
- Formatter only
- Test
- None
* Correct answer: Linter
Fast.

What is the config?
- .pre-commit-config.yaml
- .gitignore
- README
- None
* Correct answer: .pre-commit-config.yaml
Repos.

What is install?
- Registers hooks
- Runs
- Removes
- None
* Correct answer: Registers hooks
Setup.

What is run --all-files?
- Checks everything
- Staged only
- Nothing
- None
* Correct answer: Checks everything
Bulk.

What is --no-verify?
- Skips hooks
- Runs
- Errors
- None
* Correct answer: Skips hooks
Emergency.

What is exit 1?
- Fail signal
- Success
- Ignore
- None
* Correct answer: Fail signal
Block.

What is a repo?
- Hook source
- File
- Branch
- None
* Correct answer: Hook source
GitHub.

What is the benefit?
- Quality gates
- Slower only
- Required
- None
* Correct answer: Quality gates
Automatic.
<!--/QUIZ-->
