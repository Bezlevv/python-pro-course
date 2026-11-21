---
title: GitHub collaboration, PR and code review
summary: Forks, branches, pull requests, reviews and issues.
order: 8
duration: 45 min
difficulty: intermediate
tags: github, pull request, review, fork
---

Teamwork on GitHub: propose changes via pull requests and review code.

## Fork and clone

- Fork a repository to your account;
- `git clone <your-fork>`.

## Branch and commit

```bash
git switch -c feature
# make changes
git add . && git commit -m "Message"
git push -u origin feature
```

## Pull request

Open a PR from your branch into the upstream main on GitHub.

## Review

Reviewers comment, approve or request changes; the author updates the branch.

## Issues

Issues track bugs and tasks; reference them from commits/PRs.

## Lesson summary

Forks → branches → PRs → reviews enable collaborative development.

<!--TASK-->
### Task 1 — Fork concept
Describe in a comment the steps to fork and clone a repo.

### Task 2 — Branch workflow
Write the commands to create a branch, commit and push.

### Task 3 — PR title
Write a good PR title and description for "add feature".

### Task 4 — Review types
List the possible review outcomes (approve, request changes, comment).

### Task 5 — Update after review
List the commands to add a new commit to the PR branch.

### Task 6 — Issue template
Write a short issue template with title, description, steps.

### Task 7 — Checklist for PR
Write a PR checklist (tests, docs, formatting).
<!--/TASK-->

<!--HINT-->
### Hint 1
Fork via web; clone URL.

### Hint 2
git switch -c feature; commit; push -u.

### Hint 3
Title short; body details.

### Hint 4
Approve / request changes / comment.

### Hint 5
add, commit, push to same branch.

### Hint 6
Title, description, steps, expected.

### Hint 7
Tests, docs, style, self-review.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```bash
# 1. Fork on GitHub
# 2. git clone https://github.com/you/repo.git
# 3. cd repo
```

### Solution 2
```bash
git switch -c feature
git add .
git commit -m "Add feature"
git push -u origin feature
```

### Solution 3
```
Title: Add search feature
Body: Implements full-text search; adds tests and docs.
```

### Solution 4
- Approve;
- Request changes;
- Comment (without blocking);
- Dismiss review.

### Solution 5
```bash
git add .
git commit -m "Address review comments"
git push
```

### Solution 6
```
Title: [Bug] Login fails with empty password
Description: ...
Steps: 1) ... 2) ...
Expected: ...
Actual: ...
```

### Solution 7
- Tests pass;
- docs updated;
- code formatted;
- self-review done.
<!--/SOLUTION-->

<!--QUIZ-->
What is a fork?
- A copy in your account
- A branch
- A clone on disk
- A PR
* Correct answer: A copy in your account
For contributions.

What is a pull request?
- A proposal to merge changes
- A command
- A clone
- An issue
* Correct answer: A proposal to merge changes
Between branches.

What is code review?
- Checking changes by others
- Running tests
- Merging
- Closing
* Correct answer: Checking changes by others
Quality gate.

What does approve mean?
- Reviewer accepts changes
- Rejects
- Asks edits
- Comments
* Correct answer: Reviewer accepts changes
Can merge.

What is an issue?
- A task/bug tracker item
- A branch
- A commit
- A file
* Correct answer: A task/bug tracker item
Discussion.

What is a good PR title?
- Short and descriptive
- Long essay
- Issue number only
- Random
* Correct answer: Short and descriptive
Clear.

Where does a PR branch come from?
- A feature branch
- Main
- A fork only
- HEAD
* Correct answer: A feature branch
Changes.

What does git push -u do?
- Sets upstream
- Deletes
- Reverts
- Tags
* Correct answer: Sets upstream
First push link.

How to update a PR after review?
- Push new commits
- Recreate PR
- Close
- Squash instantly
* Correct answer: Push new commits
Same branch.

What does "request changes" mean?
- Reviewer wants edits
- Merge OK
- No comments
- Approved
* Correct answer: Reviewer wants edits
Blocking.

Which is essential in PR?
- Tests
- Haiku
- Screenshots always
- Jokes
* Correct answer: Tests
Quality assurance.

What does upstream mean?
- The original repository
- Your fork
- Local branch
- Cache
* Correct answer: The original repository
Source of truth.
<!--/QUIZ-->
