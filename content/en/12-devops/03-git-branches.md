---
title: Git: branches, merges, resolving conflicts
summary: Branching workflows, merge/rebase, conflicts.
order: 3
duration: 45 min
difficulty: intermediate
tags: git, branches, merge
---

Git tracks versions and enables teamwork.

## Branch

```bash
git checkout -b feature
git add -A && git commit -m "feature"
git checkout main
```

## Merge

```bash
git merge feature
```

## Conflict

When both branches changed the same line.

```bash
git status            # both modified
# edit, then:
git add -A
git commit -m "merge"
```

## Lesson summary

Branches isolate work; merges integrate it.

<!--TASK-->
### Task 1 — Branch
Create and switch to a branch.

### Task 2 — Commit
Commit on the branch.

### Task 3 — Merge
Merge back to main.

### Task 4 — Conflict
Simulate a conflict and resolve it.

### Task 5 — Log
Show a graph log.

### Task 6 — Stash
Stash and restore changes.

### Task 7 — Rebase idea
Explain rebase vs merge.
<!--/TASK-->

<!--HINT-->
### Hint 1
git checkout -b.

### Hint 2
git commit.

### Hint 3
git merge.

### Hint 4
Git status.

### Hint 5
git log --graph.

### Hint 6
git stash.

### Hint 7
Linearity.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```bash
git checkout -b feature
```

### Solution 2
```bash
git add -A
git commit -m "feature work"
```

### Solution 3
```bash
git checkout main
git merge feature
```

### Solution 4
```bash
# обе ветки изменили одну строку
git status
# отредактировать файл, убрать <<<<<<< / ======= / >>>>>>>
git add -A
git commit -m "resolve conflict"
```

### Solution 5
```bash
git log --oneline --graph --all
```

### Solution 6
```bash
git stash
# ... работа ...
git stash pop
```

### Solution 7
```python
# merge: создаёт merge-коммит, сохраняет историю
# rebase: перекладывает коммиты, линейная история
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a branch?
- Independent line of work
- A file
- A log
- None
* Correct answer: Independent line of work
Isolation.

What is git checkout -b?
- Creates + switches
- Deletes
- Renames
- None
* Correct answer: Creates + switches
Branch.

What is a merge?
- Combines branches
- Deletes
- Copies
- None
* Correct answer: Combines branches
Integration.

What is a conflict?
- Same line changed
- Different files
- Error always
- None
* Correct answer: Same line changed
Manual.

What are <<<<<<< markers?
- Conflict markers
- Comments
- Errors
- None
* Correct answer: Conflict markers
Sections.

What is git status?
- Shows state
- Commits
- Pushes
- None
* Correct answer: Shows state
Files.

What is git log --graph?
- Visual history
- Files
- Config
- None
* Correct answer: Visual history
Graph.

What is git stash?
- Temporarily saves
- Deletes forever
- Merges
- None
* Correct answer: Temporarily saves
Restore.

What is rebase?
- Reapplies commits
- Merges
- Deletes
- None
* Correct answer: Reapplies commits
Linear.

What is HEAD?
- Current commit
- A branch name
- A file
- None
* Correct answer: Current commit
Pointer.

What is origin?
- Remote
- Local
- A branch
- None
* Correct answer: Remote
GitHub.

What is push?
- Uploads commits
- Downloads
- Merges
- None
* Correct answer: Uploads commits
Remote.
<!--/QUIZ-->
