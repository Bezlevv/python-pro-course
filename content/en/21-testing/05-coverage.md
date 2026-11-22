---
title: Coverage and continuous testing
summary: pytest-cov, coverage reports, CI.
order: 5
duration: 40 min
difficulty: advanced
tags: coverage, ci
---

Coverage measures how much code tests exercise.

## Run coverage

```bash
pip install pytest-cov
pytest --cov=myapp
pytest --cov=myapp --cov-report=html
```

## Read

Percentages per file; focus on core modules.

## CI

Run tests on every push via GitHub Actions.

## Lesson summary

Coverage guides effort; CI enforces tests.

<!--TASK-->
### Task 1 — Install
Install pytest-cov.

### Task 2 — Run
Run with --cov.

### Task 3 — Report
Generate HTML report.

### Task 4 — Analyze
Which file needs tests?

### Task 5 — Target
Set a 80% goal.

### Task 6 — CI
Add a test job.

### Task 7 — Badge
Add a coverage badge.
<!--/TASK-->

<!--HINT-->
### Hint 1
pip install.

### Hint 2
--cov.

### Hint 3
--cov-report=html.

### Hint 4
Low%.

### Hint 5
Threshold.

### Hint 6
Actions.

### Hint 7
Badge.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```bash
pip install pytest-cov
```

### Solution 2
```bash
pytest --cov=myapp
```

### Solution 3
```bash
pytest --cov=myapp --cov-report=html
# открыть htmlcov/index.html
```

### Solution 4
```text
Смотреть на файлы с наименьшим процентом —
там функции не покрыты тестами
```

### Solution 5
```text
Цель: не менее 80% ключевых модулей;
можно добавить fail_under=80 в конфиг
```

### Solution 6
```yaml
- name: Run tests
  run: |
    pip install -r requirements.txt pytest-cov
    pytest --cov=myapp --cov-fail-under=80
```

### Solution 7
```text
Провайдеры (Coveralls/Codecov) дают badge —
картинку со статусом для README
```
<!--/SOLUTION-->

<!--QUIZ-->
What is coverage?
- Tested lines %
- A test
- A bug
- None
* Correct answer: Tested lines %
Metric.

What is pytest-cov?
- Plugin
- A test
- A runner
- None
* Correct answer: Plugin
Coverage.

What is --cov=myapp?
- Measures module
- Tests only
- Skips
- None
* Correct answer: Measures module
Target.

What is HTML report?
- Visual coverage
- Text
- PDF
- None
* Correct answer: Visual coverage
htmlcov.

What is fail_under?
- Minimum gate
- Maximum
- None
- Always
* Correct answer: Minimum gate
80.

What is CI?
- Automated runs
- Manual
- Debug
- None
* Correct answer: Automated runs
Push.

What is a badge?
- Status image
- Code
- Test
- None
* Correct answer: Status image
README.

What is a core module?
- Important code
- Unused
- Tests
- None
* Correct answer: Important code
Prioritize.

What is 100%?
- Full coverage
- Impossible
- Required
- None
* Correct answer: Full coverage
Goal.

What is a miss?
- Untested line
- Error
- Pass
- None
* Correct answer: Untested line
Red.

What is a measurement?
- Percent
- Guess
- Style
- None
* Correct answer: Percent
Data.

What is the workflow?
- Test → measure → improve
- Write only
- Skip
- None
* Correct answer: Test → measure → improve
Loop.
<!--/QUIZ-->
