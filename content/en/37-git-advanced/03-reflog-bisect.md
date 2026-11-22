---
title: reflog, bisect and recovery
summary: How Git keeps a "safety net" of all HEAD movements, how to restore deleted commits and branches, how to find the first commit that broke the code with binary search.
order: 3
duration: 40 min
difficulty: advanced
tags: git, reflog, bisect, recovery, revert, reset, fsck
---

Git almost never destroys commits instantly. It has a "safety net": `reflog` (the log of `HEAD` movements), dangling objects and `fsck`. And `git bisect` helps find the commit that broke the behavior — with binary search. These three tools turn a "catastrophe" (deleted a branch, rolled back the wrong thing) into a routine five-minute operation.

## reflog: the log of HEAD movements

`reflog` is a local log in which Git records **every** change of the `HEAD` pointer: commits, checkout, reset, merge, rebase, cherry-pick. The records live for about 90 days (configurable via `gc.reflogExpire`).

```bash
git reflog
```

Example output:

```
a1b2c3d HEAD@{0}: commit: feat: add login
e4f5a6b HEAD@{1}: rebase (finish): returning to refs/heads/feature
e4f5a6b HEAD@{2}: rebase (start): checkout main
...
```

The right column is the actions, the left is where `HEAD` pointed, and `HEAD@{1}` means "the state of HEAD one step back". This notation works in any command that expects a commit:

```bash
git reset --hard HEAD@{1}    # go back one step
git checkout HEAD@{2}        # look at the state two steps back
git cherry-pick HEAD@{3}     # apply a commit from the past
```

## Restoring a deleted branch

Deleted the branch with `git branch -D feature`? Do not panic: it is still in the reflog.

```bash
git reflog | grep feature
# b2c3d4e5 HEAD@{4}: checkout: moving from feature to main
git checkout -b feature b2c3d4e5
```

We recreated the branch from the commit it pointed to. A "lost" rebase is restored similarly: after `git rebase -i` the old version of the branch remains in the reflog as `HEAD@{n}` before the rebase.

## reset, revert and restoring files

- `git reset --hard <sha>` — hard rollback: both the index and the working tree become as in commit `<sha>`. Dangerous if there are unsaved edits in the working tree — they will be lost. But the commit itself stays in the reflog.
- `git reset --soft <sha>` — moves only `HEAD`; changes stay in the index.
- `git reset --mixed <sha>` (default) — moves `HEAD` and the index but does not touch the working tree.
- `git revert <sha>` — creates a **new** commit that undoes the changes of `<sha>`. Safe for public history: nobody rewrites anything.

The selection rule: public history — only `revert`; personal unpublished history — `reset` is fine. Restore a single file to a commit's state:

```bash
git restore --source=HEAD~1 app.py
```

## fsck and dangling objects

Commits nothing references (no branch, no reflog) are called dangling. If the reflog has already been cleaned, they can be found like this:

```bash
git fsck --lost-found
# dangling commit a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8
```

`git fsck --lost-found` also puts lost objects into `.git/lost-found/`, from where you can retrieve them with `git show`.

## bisect: binary search for the culprit

`git bisect` is an automated game of "cold-hot". You say "this commit is good, and that one is bad", and Git uses bisection to find the first commit after which the behavior broke.

```bash
git bisect start
git bisect bad HEAD          # the current state is bad
git bisect good v1.0.0       # a known good commit
```

Git will switch `HEAD` to the middle commit. On it you check the behavior (e.g. run a test) and say:

```bash
git bisect good   # on this commit it is still good
git bisect bad    # on this commit it is already bad
```

This way, logarithmically, in ~10 steps out of 1000 commits the first bad one is found. Automatically — with a script:

```bash
git bisect run pytest test_regression.py
```

The script must return 0 (good) or a non-zero code (bad). At the end — `git bisect reset` to return to the original branch.

<!--TASK-->
### Task 1
Create a temporary repository with five commits and "accidentally lose" a branch, then restore it via reflog:

1. `git init`; set name and email; create a file with five changes, one commit each (e.g. `v1`…`v5`).
2. On `v5` create branch `experiment`, add two more commits (`v6`, `v7`).
3. Return to `main` and delete the branch with `git branch -D experiment`.
4. Find its commit in `git reflog` and restore the branch with `git checkout -b experiment <sha>`.

Expected result: `git log --oneline experiment` shows commits `v7`, `v6`, `v5` from top to bottom, and `git branch` shows `experiment` again.

### Task 2
Write a pytest test `test_reflog_restore.py`:

1. Temporary repository: commit `A`, then branch `feature` with commits `B`, `C`.
2. Switch to `main`, delete the branch with `git branch -D feature`.
3. Read `git reflog`, find the line with `feature` and take the hash (the last element of the line).
4. Recreate the branch and check: `git log --oneline feature` contains `C` and `B`.

Run `pytest test_reflog_restore.py -v`: expected result — `1 passed`.

### Task 3
Write a pytest test `test_bisect_finds_bad.py`: simulate a regression and find it with bisect:

1. Repository: 6 commits in a row, in each the file `calc.py` contains a line like `RESULT = 1`, `RESULT = 2`, … `RESULT = 6` (one commit per value, the file is fully rewritten).
2. Write a script `check.sh` that returns 0 if the file has `RESULT < 5`, otherwise 1.
3. Run `git bisect start`, `git bisect bad HEAD`, `git bisect good HEAD~5`, then `git bisect run ./check.sh`.
4. After completion check that `git show HEAD` contains `RESULT = 5` (the first "bad" commit). Then run `git bisect reset`.

Run `pytest test_bisect_finds_bad.py -v`: expected result — `1 passed`.

### Task 4
Compare `revert` and `reset` on public history. In the repository from task 1:

1. Run `git revert` on the last commit of `main` and look at `git log --oneline -3`: a new revert commit should appear.
2. Then go back one position via `git reset --hard HEAD~1` and look at the log again.

Expected result: you can explain the difference: `revert` adds a commit and does not touch history, while `reset` moves the branch, "throwing out" the commit from history. Write the output of both logs in a notebook — it will be useful for the exam.

### Task 5
Restore a commit "lost" after `reset --hard`. Scenario:

1. Make three commits. Run `git reset --hard HEAD~2` — the branch moves, two commits "disappear".
2. Find them in `git reflog` (records `HEAD@{1}`, `HEAD@{2}`).
3. Return the branch to its place with `git reset --hard HEAD@{1}`.

Expected result: `git log --oneline` shows all three commits again, and `git status` shows a clean tree.

<!--/TASK-->

<!--HINT-->
### Hint 1
In `git reflog` find the line with `checkout: moving from experiment to main` — the hash at its start is the last commit of the branch. The command `git checkout -b experiment <sha>` recreates the branch from that point.

### Hint 2
Reflog is text: `git reflog` in the helper returns stdout. Look for the line containing the substring `feature`, split it by spaces — the first element is the hash. Restore: `git checkout -b feature <sha>`; then `git log --format=%s feature`.

### Hint 3
Make the `check.sh` file executable: `os.chmod(path, 0o755)`. Inside — `#!/bin/sh` and `grep -q 'RESULT = 5' calc.py && exit 1 || exit 0` (or a check via python). `git bisect run` requires the script to run in the repository's `cwd`. After run, `git bisect reset` is mandatory, otherwise the test leaves the repository in bisect state.

### Hint 4
`git revert HEAD` creates a commit with the message `Revert "..."` — history grows. `git reset --hard HEAD~1` at the same point deletes the revert commit (but not the original commit — it remains lower in history). Compare the lengths of the logs and the number of commits.

### Hint 5
Immediately after `git reset --hard HEAD~2` run `git reflog`: there will be `HEAD@{0}` (current state) and `HEAD@{1}` (previous, with the lost commits). `git reset --hard HEAD@{1}` returns the branch to its place. If much time has passed and the record has been washed out — use `git fsck --lost-found`.

<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Steps:

```bash
git init
git config user.name "Test"
git config user.email "test@example.com"

for i in 1 2 3 4 5; do echo "v$i" > file.txt; git add file.txt; git commit -m "v$i"; done

git checkout -b experiment
echo v6 > file.txt && git add file.txt && git commit -m "v6"
echo v7 > file.txt && git add file.txt && git commit -m "v7"

git checkout main
git branch -D experiment

git reflog | grep experiment
# b2c3d4e5 HEAD@{4}: checkout: moving from experiment to main
git checkout -b experiment b2c3d4e5
git log --oneline experiment
```

The line `checkout: moving from experiment to main` — the moment we left the branch; its hash is the tip of `experiment`. Recreating the branch from that commit returns its whole history: `v7`, `v6`, `v5`. Why this works: a branch is just a pointer to a commit; while the commit is alive (in the reflog or as dangling), the branch can be recreated. `git branch -D` deletes only the pointer, not the data. The same techniques work for rebase and merge: the state before the operation is always in the reflog.

### Solution 2
Solution:

```python
import subprocess
import tempfile
from pathlib import Path

import pytest


def git(*args, cwd):
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True,
        capture_output=True, text=True,
    ).stdout.strip()


def commit_file(repo, name, content, message):
    (Path(repo) / name).write_text(content)
    git("add", name, cwd=repo)
    git("commit", "-m", message, cwd=repo)


def test_reflog_restores_deleted_branch():
    with tempfile.TemporaryDirectory() as repo:
        git("init", cwd=repo)
        git("config", "user.name", "Test", cwd=repo)
        git("config", "user.email", "test@example.com", cwd=repo)

        commit_file(repo, "f.txt", "A\n", "A")
        git("checkout", "-b", "feature", cwd=repo)
        commit_file(repo, "f.txt", "A\nB\n", "B")
        commit_file(repo, "f.txt", "A\nB\nC\n", "C")

        git("checkout", "main", cwd=repo)
        git("branch", "-D", "feature", cwd=repo)

        reflog = git("reflog", cwd=repo)
        line = next(l for l in reflog.splitlines() if "feature" in l)
        sha = line.split()[0]

        git("checkout", "-b", "feature", sha, cwd=repo)
        messages = git("log", "--format=%s", "feature", cwd=repo)
        assert "C" in messages and "B" in messages
```

Analysis: `git branch -D feature` deletes only the pointer. The reflog keeps the record of the `moving from feature to main` switch; its hash is the branch tip. `git checkout -b feature <sha>` recreates the pointer, and history `B`, `C` is available again. Possible mistakes: not finding the line (if there was another action before checkout — search for `checkout: moving from feature`), or taking the wrong hash (the first element of the line). Run: `pytest test_reflog_restore.py -v` → `1 passed`.

### Solution 3
Solution:

```python
import os
import subprocess
import tempfile
from pathlib import Path

import pytest


def git(*args, cwd):
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True,
        capture_output=True, text=True,
    ).stdout.strip()


def commit_file(repo, name, content, message):
    (Path(repo) / name).write_text(content)
    git("add", name, cwd=repo)
    git("commit", "-m", message, cwd=repo)


def test_bisect_finds_bad_commit():
    with tempfile.TemporaryDirectory() as repo:
        git("init", cwd=repo)
        git("config", "user.name", "Test", cwd=repo)
        git("config", "user.email", "test@example.com", cwd=repo)

        for i in range(1, 7):
            commit_file(repo, "calc.py", f"RESULT = {i}\n", f"step {i}")

        script = Path(repo) / "check.sh"
        script.write_text("#!/bin/sh\ngrep -q 'RESULT = 5' calc.py && exit 1 || exit 0\n")
        os.chmod(script, 0o755)

        git("bisect", "start", cwd=repo)
        git("bisect", "bad", "HEAD", cwd=repo)
        git("bisect", "good", "HEAD~5", cwd=repo)
        git("bisect", "run", "./check.sh", cwd=repo)

        head = git("show", "HEAD", "--format=%s", "--no-patch", cwd=repo)
        assert head == "step 5"

        git("bisect", "reset", cwd=repo)
```

Analysis: the script returns 1 (bad) when `RESULT = 5` and 0 (good) for smaller values. `git bisect run` checks the middle commits in turn: first `step 3` (good), then `step 5` (bad), then `step 4`, and localizes the first bad one — `step 5`. Important: `git bisect reset` at the end is mandatory — without it the test would leave the repository in bisect state and subsequent commands would fail. The check via `git show HEAD --format=%s` shows the name of the commit where bisect stopped. Run: `pytest test_bisect_finds_bad.py -v` → `1 passed`.

### Solution 4
Before the operations the log: `v7`, `v6`, …, `v1`. After `git revert HEAD`:

```
Revert "v7"
v7
v6
...
```

A new "antipode" commit appeared, history was not rewritten. After `git reset --hard HEAD~1` this revert commit disappeared — the branch points at `v7` again, but `v7` and `v6` are in place: `reset` moved the pointer, and the commits stayed in the reflog. Summary: `revert` is safe for public history (everyone sees what was undone), `reset` is only suitable for personal unpublished history. In practice: accidentally merged a feature into `main` — `git revert` (do not rewrite shared history); messed up your own branch — `git reset --hard`.

### Solution 5
Commands:

```bash
echo 1 > f.txt && git add f.txt && git commit -m "one"
echo 2 > f.txt && git add f.txt && git commit -m "two"
echo 3 > f.txt && git add f.txt && git commit -m "three"

git reset --hard HEAD~2   # now the log shows only "one"
git reflog
# HEAD@{0}: reset: moving to HEAD~2
# HEAD@{1}: commit: three
# HEAD@{2}: commit: two
git reset --hard HEAD@{1}
git log --oneline
# three, two, one
```

Analysis: `git reset --hard HEAD~2` moved the branch two commits back — `two` and `three` got detached but did not disappear: they are in the reflog. `HEAD@{1}` is the state before reset, i.e. the tip with `three`. `git reset --hard HEAD@{1}` restores everything. The moral: even after a hard reset commits stay alive for ~90 days, and almost any "lost" commit can be brought back. Reminder: when working with other people's repositories, `reset --hard` will not fix someone else's history — there only `revert` works.

<!--/SOLUTION-->

<!--QUIZ-->
What does git reflog store?
- Only deleted branches
- The history of all HEAD movements: commits, checkout, reset, merge, rebase
- The content of all files
- Passwords and access keys
* Correct answer: The history of all HEAD movements: commits, checkout, reset, merge, rebase
Every change of the HEAD pointer is recorded in the reflog with a timestamp and a description of the action.

How many days do reflog records live by default?
- 7 days
- 90 days
- 365 days
- Forever
* Correct answer: 90 days
By default reflog records expire after ~90 days (setting gc.reflogExpire).

How is the HEAD state "one step back" denoted?
- HEAD~1
- HEAD@{1}
- HEAD-1
- HEAD^1
* Correct answer: HEAD@{1}
The notation HEAD@{n} is the n-th step back in the reflog. HEAD~1 is the first parent in commit history.

Which command deletes a branch but leaves its commits in the reflog?
- git branch -d feature
- git branch -D feature
- git branch --delete-all feature
- git diff --delete feature
* Correct answer: git branch -D feature
-D deletes the branch forcibly; the commits remain reachable via the reflog and can be restored.

Which command returns a branch to an earlier state by creating a new commit?
- git reset --hard
- git revert
- git checkout
- git rebase
* Correct answer: git revert
revert creates a new commit that undoes the changes of the given one, without rewriting history.

What does git reset --hard <sha> do?
- Moves HEAD and the index but does not touch the working tree
- Moves HEAD, the index and the working tree to <sha>
- Copies <sha> into a new branch
- Creates a revert commit
* Correct answer: Moves HEAD, the index and the working tree to <sha>
--hard forcibly synchronizes all three areas with the commit; unsaved edits will be lost.

What does git fsck --lost-found return?
- A list of dangling objects nobody references
- A list of all repository branches
- A list of configured remotes
- A list of conflicting files
* Correct answer: A list of dangling objects nobody references
Commits without references are found via fsck; they can be restored by hash.

What does git bisect run ./check.sh do?
- Automatically runs the script on middle commits until it finds the first "bad" one
- Runs the script once on the current commit
- Searches for scripts in the repository
- Compares two commits
* Correct answer: Automatically runs the script on middle commits until it finds the first "bad" one
The script must return 0 for "good" commits and a non-zero code for "bad" ones.

Which command must be run after bisect finishes?
- git bisect reset
- git bisect end
- git bisect finish
- git bisect stop
* Correct answer: git bisect reset
reset returns HEAD to the original branch and exits bisect mode.

Which command returns a single file to the state from a commit?
- git restore --source=HEAD~1 app.py
- git checkout --all
- git reset --soft file
- git revert --file app.py
* Correct answer: git restore --source=HEAD~1 app.py
git restore with --source takes the file content from the given commit.

<!--/QUIZ-->
