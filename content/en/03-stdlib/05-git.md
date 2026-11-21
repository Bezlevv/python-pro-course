---
title: Git and GitHub for Pythonists
summary: Repositories, commits, branches, merging and publishing on GitHub.
order: 5
duration: 45 min
difficulty: intermediate
tags: git, github, commit, branch
---

Git tracks the history of your code; GitHub hosts repositories.

## Initialize

```bash
git init
git add .
git commit -m "First commit"
```

## Status and log

```bash
git status
git log --oneline
```

## Branches

```bash
git switch -c feature
git switch main
git merge feature
```

## Publishing

```bash
git remote add origin https://github.com/user/repo.git
git push -u origin main
```

## Clone and pull

```bash
git clone https://github.com/user/repo.git
git pull
```

## Lesson summary

Git tracks versions; common cycle: add → commit → push; branches organize work.

<!--TASK-->
### Task 1 — Init and commit
Create a directory, git init, create README.md, add and commit.

### Task 2 — Status
Modify a file and run git status; list changed files.

### Task 3 — Log
Make two commits; show git log --oneline.

### Task 4 — Branch
Create branch feature, switch, commit, switch back.

### Task 5 — Merge
Merge feature into main; show log graph.

### Task 6 — Ignore
Create .gitignore for __pycache__ and verify it is ignored.

### Task 7 — Remote
Add a remote origin and show git remote -v.
<!--/TASK-->

<!--HINT-->
### Hint 1
git init; git add .; git commit.

### Hint 2
git status --short.

### Hint 3
git log --oneline.

### Hint 4
git switch -c feature.

### Hint 5
git merge feature.

### Hint 6
Write __pycache__/ into .gitignore.

### Hint 7
git remote add origin URL.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```bash
git init
echo "# My project" > README.md
git add .
git commit -m "Initial commit"
```

### Solution 2
```bash
echo "change" >> README.md
git status --short
```

### Solution 3
```bash
git log --oneline
```

### Solution 4
```bash
git switch -c feature
# make changes, commit
git switch main
```

### Solution 5
```bash
git merge feature
git log --oneline --graph
```

### Solution 6
```bash
echo "__pycache__/" >> .gitignore
git status   # ignored files absent
```

### Solution 7
```bash
git remote add origin https://github.com/user/repo.git
git remote -v
```
<!--/SOLUTION-->

<!--QUIZ-->
What does git init do?
- Creates a repository
- Clones
- Commits
- Pushes
* Correct answer: Creates a repository
Starts tracking.

What does git add do?
- Stages changes
- Commits
- Removes
- Shows
* Correct answer: Stages changes
Prepares for commit.

What does git commit do?
- Saves a snapshot
- Stages
- Pushes
- Pulls
* Correct answer: Saves a snapshot
With a message.

What is a branch?
- Independent line of work
- A copy of git
- A commit
- A tag
* Correct answer: Independent line of work
Isolated changes.

How to create a branch and switch?
- git switch -c name
- git branch -c
- git commit -c
- git clone
* Correct answer: git switch -c name
Create + switch.

What does git merge do?
- Joins branches
- Deletes
- Reverts
- Tags
* Correct answer: Joins branches
Combines history.

What does git status show?
- Current state
- Remote branches
- Logs
- Config
* Correct answer: Current state
Uncommitted changes.

What does git log show?
- History
- Files
- Status
- Remotes
* Correct answer: History
Commits.

What does git push do?
- Uploads commits to remote
- Downloads
- Starts server
- Removes
* Correct answer: Uploads commits to remote
Origin.

What does git pull do?
- Fetches and merges
- Pushes
- Stashes
- Clones
* Correct answer: Fetches and merges
Updates local.

What is .gitignore?
- Files to ignore
- Git config
- History
- Remote
* Correct answer: Files to ignore
Patterns.

What does git clone do?
- Copies a repository
- Creates a branch
- Commits
- Tags
* Correct answer: Copies a repository
Full copy.
<!--/QUIZ-->
