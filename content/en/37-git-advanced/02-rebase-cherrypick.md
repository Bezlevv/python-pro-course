---
title: Rebase, cherry-pick, interactive rebase
summary: Clean history and selective commits.
order: 2
duration: 50 min
difficulty: advanced
tags: git, rebase
---

These commands rewrite history.

## Rebase

```bash
git checkout feature
git rebase main
# перекладывает коммиты feature поверх main
```

## Cherry-pick

```bash
git cherry-pick abc1234
# применить один коммит в текущую ветку
```

## Interactive

```bash
git rebase -i HEAD~3
# squash, reword, drop
```

## Lesson summary

Rebase linearizes; cherry-pick selects.

<!--TASK-->
### Task 1 — Rebase
Rebase feature onto main.

### Task 2 — Conflicts
Resolve during rebase.

### Task 3 — Cherry-pick
Apply a commit.

### Task 4 — Squash
Combine with -i.

### Task 5 — Reword
Edit a message.

### Task 6 — Drop
Remove a commit.

### Task 7 — Safety
When not to rebase?
<!--/TASK-->

<!--HINT-->
### Hint 1
git rebase main.

### Hint 2
Status.

### Hint 3
cherry-pick.

### Hint 4
squash.

### Hint 5
reword.

### Hint 6
drop.

### Hint 7
Shared.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```bash
git checkout feature
git rebase main
```

### Solution 2
```bash
git status        # конфликт
# исправить файлы
git add -A
git rebase --continue
```

### Solution 3
```bash
git cherry-pick abc1234
```

### Solution 4
```bash
git rebase -i HEAD~3
# поменять pick на squash для нужных строк
```

### Solution 5
```bash
git rebase -i HEAD~2
# pick → reword, сохранить, ввести новое сообщение
```

### Solution 6
```bash
git rebase -i HEAD~3
# pick → drop
```

### Solution 7
```text
Не переписывать коммиты, уже отправленные
в общую ветку — это сломает историю других
```
<!--/SOLUTION-->

<!--QUIZ-->
What is rebase?
- Reapplies commits
- Merges
- Copies
- None
* Correct answer: Reapplies commits
Linear.

What is cherry-pick?
- Applies one commit
- Merges all
- Deletes
- None
* Correct answer: Applies one commit
Select.

What is interactive?
- -i flag
- Automatic
- None
- Always
* Correct answer: -i flag
Editor.

What is squash?
- Combines commits
- Splits
- Deletes
- None
* Correct answer: Combines commits
One.

What is reword?
- Changes message
- Content
- Author
- None
* Correct answer: Changes message
Edit.

What is drop?
- Removes commit
- Adds
- Keeps
- None
* Correct answer: Removes commit
Skip.

What is pick?
- Keep commit
- Remove
- Combine
- None
* Correct answer: Keep commit
Default.

What is --continue?
- After conflict
- Start
- Abort
- None
* Correct answer: After conflict
Next.

What is --abort?
- Cancels
- Continues
- Starts
- None
* Correct answer: Cancels
Restore.

What is a conflict?
- Same lines
- Different files
- Error always
- None
* Correct answer: Same lines
Manual.

What is history?
- Commit chain
- Files
- Branches
- None
* Correct answer: Commit chain
Log.

When not to rebase?
- Shared commits
- Local only
- Always
- None
* Correct answer: Shared commits
Danger.
<!--/QUIZ-->
