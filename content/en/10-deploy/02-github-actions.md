---
title: CI/CD: GitHub Actions
summary: Workflows, jobs, steps, matrix, secrets.
order: 2
duration: 45 min
difficulty: advanced
tags: ci, cd, github actions
---

GitHub Actions runs checks on every push.

## Workflow

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: pip install -r requirements.txt
      - run: pytest
```

## Matrix

```yaml
strategy:
  matrix:
    python-version: ["3.12", "3.13"]
```

## Secrets

```yaml
- run: echo ${{ secrets.TOKEN }}
```

## Lesson summary

Workflows automate tests and deployment on push.

<!--TASK-->
### Task 1 — Trigger
Write on: [push].

### Task 2 — Job
Add a test job on ubuntu.

### Task 3 — Steps
Checkout + setup-python.

### Task 4 — Run tests
pip install + pytest.

### Task 5 — Matrix
Add two Python versions.

### Task 6 — Cache
Cache pip.

### Task 7 — Secrets
Use a secret in a step.
<!--/TASK-->

<!--HINT-->
### Hint 1
on: push.

### Hint 2
jobs.test.

### Hint 3
actions/checkout.

### Hint 4
pytest.

### Hint 5
matrix.

### Hint 6
actions/cache.

### Hint 7
secrets.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```yaml
name: CI
on: [push, pull_request]
```

### Solution 2
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: echo "hello"
```

### Solution 3
```yaml
steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-python@v5
    with:
      python-version: "3.13"
```

### Solution 4
```yaml
- run: pip install -r requirements.txt
- run: pytest
```

### Solution 5
```yaml
strategy:
  matrix:
    python-version: ["3.12", "3.13"]
```

### Solution 6
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

### Solution 7
```yaml
- run: echo "Token length: ${#TOKEN}"
  env:
    TOKEN: ${{ secrets.TOKEN }}
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a workflow?
- Automated pipeline
- A file only
- A test
- None
* Correct answer: Automated pipeline
YAML.

What is on?
- Trigger events
- A job
- A step
- None
* Correct answer: Trigger events
push.

What is a job?
- Group of steps
- A trigger
- A platform
- None
* Correct answer: Group of steps
Runs on.

What is a step?
- One action
- A job
- A trigger
- None
* Correct answer: One action
run/uses.

What is checkout?
- Gets the code
- Tests
- Deploys
- None
* Correct answer: Gets the code
action.

What is setup-python?
- Installs Python
- Tests
- Deploys
- None
* Correct answer: Installs Python
Action.

What is a matrix?
- Combinations
- One job
- Secrets
- None
* Correct answer: Combinations
Versions.

What is a secret?
- Hidden value
- A file
- A job
- None
* Correct answer: Hidden value
${{ secrets }}.

What is runs-on?
- OS for job
- A step
- A trigger
- None
* Correct answer: OS for job
ubuntu.

What is cache?
- Reuses dependencies
- Runs tests
- Deploys
- None
* Correct answer: Reuses dependencies
Speed.

What is CI?
- Continuous integration
- Deployment
- Test only
- None
* Correct answer: Continuous integration
Checks.

What is CD?
- Continuous deployment
- Integration
- Test
- None
* Correct answer: Continuous deployment
Release.
<!--/QUIZ-->
