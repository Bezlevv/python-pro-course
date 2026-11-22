---
title: Working with tasks and code review
summary: Issues, PRs, review etiquette.
order: 3
duration: 40 min
difficulty: intermediate
tags: tasks, code review, pr
---

Professional work flows through tasks and reviews.

## Issue

A task with description, steps to reproduce, acceptance criteria.

## PR

A proposed change with tests and description.

## Review

Check logic, tests, style; comment politely.

## Etiquette

Small PRs, clear titles, respond to comments.

## Lesson summary

Issues and PRs organize work in teams.

<!--TASK-->
### Task 1 — Issue
Write a good issue.

### Task 2 — Branch
Create a branch for the task.

### Task 3 — PR
Write a PR description.

### Task 4 — Review
Comment on a fake diff.

### Task 5 — Fix
Address review comments.

### Task 6 — Tests
Why tests in PR?

### Task 7 — Merge
Describe the merge checklist.
<!--/TASK-->

<!--HINT-->
### Hint 1
Title + steps.

### Hint 2
Feature branch.

### Hint 3
What and why.

### Hint 4
Kind.

### Hint 5
Commit.

### Hint 6
Safe.

### Hint 7
Green CI.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```text
Заголовок: Ошибка при регистрации
Шаги: 1) открыть форму 2) отправить пустую
Ожидание: сообщение об ошибке
Факт: серверная ошибка 500
```

### Solution 2
```bash
git checkout -b fix/registration-error
```

### Solution 3
```text
Что: исправил валидацию формы регистрации
Почему: пустая форма давала 500
Как проверить: pytest + вручную
```

### Solution 4
```text
«Здесь лучше использовать .get() вместо []
— чтобы не падать на отсутствующем ключе»
```

### Solution 5
```bash
git add -A && git commit -m "fix: use .get() in validation"
git push origin fix/registration-error
```

### Solution 6
```text
Тесты доказывают, что фикс работает
и не ломает остальное
```

### Solution 7
```text
CI зелёный → ревью одобрено → merge
→ удалить ветку
```
<!--/SOLUTION-->

<!--QUIZ-->
What is an issue?
- Task description
- Code
- A branch
- None
* Correct answer: Task description
Tracking.

What is a PR?
- Proposed change
- Final code
- A bug
- None
* Correct answer: Proposed change
Review.

What is a branch?
- Isolated work
- Deleted
- A file
- None
* Correct answer: Isolated work
Feature.

What is review?
- Checking changes
- Writing
- Deploying
- None
* Correct answer: Checking changes
Quality.

What is etiquette?
- Respectful comments
- Harsh
- Ignoring
- None
* Correct answer: Respectful comments
Culture.

Why small PRs?
- Easier review
- Bigger
- Faster always
- None
* Correct answer: Easier review
Focus.

What are tests?
- Verification
- Style
- Docs
- None
* Correct answer: Verification
Proof.

What is CI?
- Automated checks
- Manual
- Deploy
- None
* Correct answer: Automated checks
Gate.

What is a merge?
- Combine branch
- Delete repo
- Push
- None
* Correct answer: Combine branch
Integrate.

What is the base branch?
- main
- Feature
- Any
- None
* Correct answer: main
Target.

What is a commit message?
- Describes change
- Random
- Author
- None
* Correct answer: Describes change
git.

What is a review comment?
- Feedback
- Code
- Test
- None
* Correct answer: Feedback
Improve.
<!--/QUIZ-->
