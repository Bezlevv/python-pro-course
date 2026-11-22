---
title: Final work: your own project
summary: Choose an idea, plan, build, test and present.
order: 7
duration: 180 min
difficulty: advanced
tags: project, final, portfolio
---

The capstone: build your own project from scratch.

## Ideas

- to-do with Flask/Django;
- weather API client;
- data dashboard;
- telegram bot;
- neural network classifier.

## Steps

1. Requirements and plan;
2. Minimal working version (MVP);
3. Tests;
4. README;
5. Push to GitHub.

## Checklist

- code organized;
- tests pass;
- README describes how to run;
- one clear feature set.

## Lesson summary

Deliver a finished, tested, documented project — your portfolio piece.

<!--TASK-->
### Task 1 — Choose
Pick an idea and write its goal.

### Task 2 — Plan
Write 3-5 user stories.

### Task 3 — MVP
Build the minimal version.

### Task 4 — Tests
Add at least 3 tests.

### Task 5 — README
Write how to install/run.

### Task 6 — Publish
Push to GitHub.

### Task 7 — Review
Evaluate your project with the checklist.
<!--/TASK-->

<!--HINT-->
### Hint 1
Simple idea first.

### Hint 2
Stories "As a user...".

### Hint 3
Core only.

### Hint 4
pytest.

### Hint 5
Install + usage.

### Hint 6
git push.

### Hint 7
Checklist.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
# Цель: консольный планировщик задач с сохранением в JSON
```

### Solution 2
```python
# - Я как пользователь могу добавить задачу
# - Я могу отметить выполненной
# - Я могу посмотреть список
# - Я могу удалить
# - Я могу сохранить и перезагрузить
```

### Solution 3
```python
# Минимальная версия: add/list/done в памяти
```

### Solution 4
```python
def test_add():
    tasks = []
    tasks.append("buy milk")
    assert tasks == ["buy milk"]
```

### Solution 5
```markdown
# Task Manager
## Install
pip install -r requirements.txt
## Run
python main.py
```

### Solution 6
```bash
git init
git add .
git commit -m "MVP"
git remote add origin <url>
git push -u origin main
```

### Solution 7
```python
# Проверить: код, тесты, README, запуск, GitHub
```
<!--/SOLUTION-->

<!--QUIZ-->
What is MVP?
- Minimal viable product
- Maximum
- Model
- None
* Correct answer: Minimal viable product
Core features.

Why plan first?
- Clarity
- Speed
- Required
- None
* Correct answer: Clarity
Direction.

What is a user story?
- Feature from user view
- A test
- A bug
- A commit
* Correct answer: Feature from user view
Requirement.

Why tests in a project?
- Protect behavior
- Style
- Speed
- None
* Correct answer: Protect behavior
Regression.

What is README for?
- How to run
- Data
- Tests
- Logs
* Correct answer: How to run
Documentation.

What is a portfolio project?
- Showable work
- Homework only
- Copy
- None
* Correct answer: Showable work
For interviews.

What does git push do?
- Uploads
- Downloads
- Deletes
- None
* Correct answer: Uploads
To remote.

What is a checklist?
- Quality criteria
- A test
- A file
- None
* Correct answer: Quality criteria
Before done.

What should README include?
- Install/run
- Only author
- Only title
- Nothing
* Correct answer: Install/run
Usage.

What is the final deliverable?
- Working project
- Code only
- Plan
- None
* Correct answer: Working project
Done.

Why publish on GitHub?
- Visible portfolio
- Backup
- Tests
- None
* Correct answer: Visible portfolio
Share.

What is self-review?
- Check yourself
- Skip
- Ask only
- None
* Correct answer: Check yourself
Final pass.
<!--/QUIZ-->
