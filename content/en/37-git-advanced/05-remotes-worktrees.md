---
title: Remote strategies and worktree
summary: How remote repositories work, how to push and pull correctly, why --force-with-lease, and how to work with multiple working copies via worktree.
order: 5
duration: 40 min
difficulty: advanced
tags: git, remote, fetch, pull, push, force-with-lease, worktree, GitHub flow
---

So far we have worked locally. But the point of Git is collaboration, and it starts with **remote** — remote repositories with which your local one exchanges commits. Understanding the mechanics of fetch/pull/push and the rules of working with other people's branches is what separates someone who "just knows git" from an engineer who can be trusted with a shared branch.

## What a remote is

A `remote` is simply a named reference to another repository (usually over https or ssh). By default the main one is called `origin`:

```bash
git remote -v
# origin  https://github.com/user/project.git (fetch)
# origin  https://github.com/user/project.git (push)
git remote add team https://...team.../project.git
git remote get-url origin
git remote set-url origin https://new/address.git
```

For experiments you can use a local path — Git works fine with `file://` and with directories. For example, a remote repository is made "bare" — without a working tree, only objects and references:

```bash
git init --bare project.git
```

## fetch vs pull vs push

- `git fetch` — downloads objects and branches from the remote but does **not** touch your local branches. After fetch only `origin/*` is updated.
- `git pull` = `fetch` + merging the current branch with its upstream.
- `git push` — sends local commits to the remote.

The exact picture after `git fetch`:

```bash
git fetch origin
git log --oneline origin/main   # what is on the remote
git log --oneline main          # what you have
```

## pull: three strategies

`git pull` does a merge by default. This creates "forks" in history. Strategies:

| Command | Behavior |
|---|---|
| `git pull` | fetch + merge (merge commit on divergence) |
| `git pull --rebase` | fetch + rebase of local commits on top of origin |
| `git pull --ff-only` | fast-forward only; if the branches diverged — refuse |

The modern `git pull --rebase` is the standard for daily synchronization: your local commits are neatly relocated on top of fresh foreign ones, history stays linear. You can pin the behavior:

```bash
git config pull.rebase true
```

## push: upstream and "forcefulness"

First push of a new branch:

```bash
git push -u origin feature/login
```

`-u` sets upstream — the link of the local branch with `origin/feature/login`. After that `git push` is enough.

A regular push works only on **fast-forward**: Git refuses to send if the remote has commits that are not local. This is protection against overwriting.

But sometimes you want to rewrite a branch's history (after rebase/squash). Then `--force` is needed. Bare `git push --force` is dangerous: it silently wipes other people's commits. The right variant is `--force-with-lease`:

```bash
git push --force-with-lease origin feature/login
```

It pushes forcefully but **only if** the remote branch has not changed since: if someone managed to push, the push is refused. This is protection against overwriting other people's work.

## Working process (GitHub Flow)

1. `git checkout -b feature/...` from the up-to-date `main`;
2. small commits with clear messages;
3. regularly `git pull --rebase origin main` — so as not to lag behind;
4. push the branch, open a Pull Request;
5. after review and fixes (squash/amend again) — `git push --force-with-lease`;
6. merge into `main`.

## worktree: multiple working copies

`git worktree` lets you keep several working trees from one repository. You need it when you are working on a feature and urgently need to fix a bug on `main` — without switching, without stashing unfinished work:

```bash
git worktree add ../hotfix -b hotfix/fix
```

This creates the folder `../hotfix` with a working tree on the new branch `hotfix/fix`. The main repository continues living its own life. See the list:

```bash
git worktree list
git worktree remove ../hotfix
```

One repository, many working trees — convenient for long tasks and for working on two versions of code in parallel.

<!--TASK-->
### Task 1
Create a bare remote and act out a fetch/pull/push cycle:

1. `git init --bare project.git` in a separate folder.
2. In a working folder `git init`, add the remote: `git remote add origin ../project.git`.
3. Make two commits (e.g. `v1`, `v2`) and `git push -u origin main`.
4. Add a third change and push again.
5. Run `git fetch origin`, then compare `git log --oneline origin/main` and `git log --oneline main` — they must match.

Expected result: `git push -u origin main` outputs `main -> main` and `branch 'main' set up to track 'origin/main'`, and both commit lists are identical.

### Task 2
Write a pytest test `test_pull_rebase_linear.py`: simulate two developers with a shared remote:

1. Bare repository `origin`; first working directory `alice` — commit `A`, push to `origin`.
2. Second working directory `bob` clones `origin` (`git clone origin bob`), makes commit `B` (on `main`), but does **not** push.
3. `alice` makes commit `C` and pushes.
4. `bob` runs `git pull --rebase` and then `git push`.
5. Check: in `bob` history is linear — `git log --oneline --graph main` contains no fork symbols, and it has three commits: `A`, `C`, `B` (C before B).

Run `pytest test_pull_rebase_linear.py -v`: expected result — `1 passed`.

### Task 3
Write a pytest test `test_force_with_lease.py` that proves the protection of `--force-with-lease`:

1. Bare `origin`; `alice` — commit `A`, push.
2. `bob` clones, makes a commit and pushes — now `B` is in origin.
3. `alice` (whose memory still has `origin/main` = `A`) rewrites her history (`git commit --amend`) and tries `git push --force-with-lease origin main` — the push must be **rejected**.
4. After `git fetch` (memory update) `git push --force-with-lease origin main` — must succeed.

Run `pytest test_force_with_lease.py -v`: expected result — `1 passed`.

### Task 4
Work with worktree:

1. In the repository from task 1 create branch `feature/pain` with one commit.
2. Run `git worktree add ../fix -b hotfix/fix`.
3. In the new folder `../fix` change a file, make a commit.
4. Check `git worktree list`: there should be two working trees.
5. Run `git worktree remove ../fix` and make sure the list again contains one tree.

Expected result: before removal `git worktree list` shows two paths: the main one and `../fix`; after `remove` — one.

### Task 5
Understand the pull strategy. In a repository with diverged branches (as in task 2, points 1–3):

1. Run `git pull --ff-only` — record that Git refuses (fast-forward is impossible).
2. Run `git pull` (regular) — a merge commit appears; look at `git log --oneline --graph -5`.
3. Run `git reset --hard origin/main`, then `git pull --rebase` — history should become linear.

Expected result: you can explain the difference between the three outputs and know when to choose which strategy.

<!--/TASK-->

<!--HINT-->
### Hint 1
Paths to the bare repository: `git remote add origin ../project.git` works if the folders are nearby. `git push -u origin main` — the first push configures upstream. After `git fetch origin` comparing the logs will show whether the branches are in sync.

### Hint 2
`git clone origin bob` creates the folder `bob`. For `bob` to have his own commit `B`, change a file and commit (without push). `alice` pushes `C`. Then in `bob`: `git pull --rebase` — rebase `B` on top of `origin/main`, then `git push`. Linearity check: `git log --oneline --graph main` — the first column must have no `|/` forks, message order A, C, B.

### Hint 3
`git commit --amend` changes the last commit (new hash). `--force-with-lease` compares the local "picture" of `origin/main` with the real one; while it is not updated (`git fetch`), the push is rejected. Expected codes: the first attempt — `returncode != 0`, the second (after fetch) — 0.

### Hint 4
`git worktree add ../fix -b hotfix/fix` — the relative path is counted from the current folder. Before `git worktree remove ../fix` make sure there are no uncommitted changes in that folder: otherwise Git will refuse. `git worktree list` will show lines: `<path to the main repo> <branch>`, then `../fix hotfix/fix`.

### Hint 5
On divergence `--ff-only` will refuse: fast-forward is impossible. A regular `git pull` will create a merge commit (a fork in the graph). After `git reset --hard origin/main` and `git pull --rebase` the local commits will be relocated on top of `origin/main` — the graph becomes linear. To return to the state after task 2, use `git log` to find the needed shas.

<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Commands:

```bash
git init --bare project.git

mkdir work && cd work
git init
git remote add origin ../project.git
git config user.name "Test"
git config user.email "test@example.com"

echo v1 > f.txt && git add f.txt && git commit -m "v1"
echo v2 > f.txt && git add f.txt && git commit -m "v2"
git push -u origin main

echo v3 > f.txt && git add f.txt && git commit -m "v3"
git push origin main

git fetch origin
git log --oneline origin/main
git log --oneline main
```

Analysis: `--bare` creates a repository without a working tree — it only accepts push/fetch. `git push -u origin main` sends the branch and records upstream (the link main → origin/main). `fetch` updates the copies of remote branches; after it `origin/main` and `main` match. Note: fetch does not change the local branch — if we had "ridden off" ahead, the log would show a divergence. That is why fetch is safe: you can do it at any moment.

### Solution 2
Solution:

```python
import subprocess
import tempfile
from pathlib import Path

import pytest


def git(*args, cwd, check=True):
    return subprocess.run(
        ["git", *args], cwd=cwd, check=check,
        capture_output=True, text=True,
    )


def commit_file(repo, name, content, message):
    (Path(repo) / name).write_text(content)
    git("add", name, cwd=repo)
    git("commit", "-m", message, cwd=repo)


def test_pull_rebase_keeps_history_linear():
    with tempfile.TemporaryDirectory() as tmp:
        origin = str(Path(tmp) / "origin.git")
        alice = str(Path(tmp) / "alice")
        bob = str(Path(tmp) / "bob")
        git("init", "--bare", origin)

        Path(alice).mkdir()
        git("init", cwd=alice)
        git("config", "user.name", "Alice", cwd=alice)
        git("config", "user.email", "alice@example.com", cwd=alice)
        git("remote", "add", "origin", origin, cwd=alice)
        commit_file(alice, "f.txt", "A\n", "A")
        git("push", "-u", "origin", "main", cwd=alice)

        git("clone", origin, bob)
        git("config", "user.name", "Bob", cwd=bob)
        git("config", "user.email", "bob@example.com", cwd=bob)
        commit_file(bob, "f.txt", "A\nB\n", "B")

        commit_file(alice, "f.txt", "A\nC\n", "C")
        git("push", "origin", "main", cwd=alice)

        git("pull", "--rebase", cwd=bob)
        git("push", "origin", "main", cwd=bob)

        graph = git("log", "--oneline", "--graph", "main", cwd=bob).stdout
        assert "|/" not in graph and "/" not in graph.splitlines()[1:]
        messages = git("log", "--format=%s", "main", cwd=bob).stdout
        assert messages.splitlines() == ["B", "C", "A"]
```

Analysis: both "developers" make commits on top of the same state. Without rebase, `bob` would get a merge commit and a fork after `git pull`. With `--rebase`, commit `B` is relocated on top of `origin/main` (which contains `C`), after which the push passes as fast-forward. Checks: no forks in the graph, message order from top to bottom B, C, A. This is an accurate model of the morning "pull --rebase + push" in a team. Run: `pytest test_pull_rebase_linear.py -v` → `1 passed`.

### Solution 3
Solution:

```python
import subprocess
import tempfile
from pathlib import Path

import pytest


def git(*args, cwd, check=True):
    return subprocess.run(
        ["git", *args], cwd=cwd, check=check,
        capture_output=True, text=True,
    )


def commit_file(repo, name, content, message):
    (Path(repo) / name).write_text(content)
    git("add", name, cwd=repo)
    git("commit", "-m", message, cwd=repo)


def test_force_with_lease_protects_remote():
    with tempfile.TemporaryDirectory() as tmp:
        origin = str(Path(tmp) / "origin.git")
        alice = str(Path(tmp) / "alice")
        bob = str(Path(tmp) / "bob")
        git("init", "--bare", origin)

        Path(alice).mkdir()
        git("init", cwd=alice)
        git("config", "user.name", "Alice", cwd=alice)
        git("config", "user.email", "alice@example.com", cwd=alice)
        git("remote", "add", "origin", origin, cwd=alice)
        commit_file(alice, "f.txt", "A\n", "A")
        git("push", "-u", "origin", "main", cwd=alice)

        git("clone", origin, bob)
        git("config", "user.name", "Bob", cwd=bob)
        git("config", "user.email", "bob@example.com", cwd=bob)
        commit_file(bob, "f.txt", "A\nB\n", "B")
        git("push", "origin", "main", cwd=bob)

        commit_file(alice, "f.txt", "A\nA2\n", "A2")
        git("commit", "--amend", "-m", "A2", cwd=alice)

        first = git("push", "--force-with-lease", "origin", "main",
                    cwd=alice, check=False)
        assert first.returncode != 0

        git("fetch", "origin", cwd=alice)
        second = git("push", "--force-with-lease", "origin", "main",
                     cwd=alice, check=False)
        assert second.returncode == 0
```

Analysis: `alice`'s local "picture" of `origin/main` is still `A` (she did not fetch after Bob's push). `--force-with-lease` compares this picture with the real remote and sees `B` — it refuses. After `git fetch` (buffer updated) the forced send passes. This is exactly how you rewrite the history of your own branch in a PR: first fetch, then `--force-with-lease`, and other people's work is never silently wiped. Run: `pytest test_force_with_lease.py -v` → `1 passed`.

### Solution 4
Commands:

```bash
git checkout -b feature/pain
echo pain > pain.txt && git add pain.txt && git commit -m "pain"
git worktree add ../fix -b hotfix/fix
cd ../fix
echo fix > fix.txt && git add fix.txt && git commit -m "fix"
cd ../work
git worktree list
git worktree remove ../fix
git worktree list
```

Analysis: `git worktree add` creates a new working copy (folder) and attaches it to a new branch. The main repository and `../fix` are independent working trees of one repository: commits in either are visible to both (shared history). `git worktree list` shows all trees. `remove` requires a clean working tree — if there are changes, Git will refuse (then `git worktree remove --force`). Worktree is irreplaceable when you urgently need to fix a bug on another branch without stashing the current work.

### Solution 5
Sequence (continuation of task 2):

```bash
git pull --ff-only
# fatal: Not possible to fast-forward, aborting.
git pull
# Merge made by the 'ort' strategy.
git log --oneline --graph -5
# *   Merge branch 'main' ...
# |\
# | * C
# * | B
# |/
# * A
git reset --hard origin/main
git pull --rebase
git log --oneline --graph -5
# * B
# * C
# * A
```

Analysis: `--ff-only` is conservative protection: if the branches diverged, it refuses without doing anything unexpected. A regular `pull` does a merge — a "fork" and a merge commit appear in history; that is fine for public branches but clutters personal history. `pull --rebase` relocates local commits on top of foreign ones — history is linear, and this is the best choice for feature branches. `reset --hard origin/main` is an auxiliary action to roll back the merge and start a "clean" experiment. Three strategies — three different results, and the choice depends on whose branch it is: personal → rebase, shared → merge or ff-only.

<!--/SOLUTION-->

<!--QUIZ-->
What is a remote in Git?
- A named reference to another repository
- A folder with backup copies
- A branch in the local repository
- A special type of commit
* Correct answer: A named reference to another repository
remote stores an address (usually https/ssh) and lets you exchange commits.

What does git fetch do?
- Downloads objects and branches from the remote without touching local branches
- Immediately merges the remote branch with the local one
- Sends local commits to the remote
- Deletes the remote
* Correct answer: Downloads objects and branches from the remote without touching local branches
After fetch only origin/* is updated; local branches stay as they were.

What does git pull --rebase do?
- fetch + rebase of local commits on top of origin
- fetch + merge
- Only fetch
- push + merge
* Correct answer: fetch + rebase of local commits on top of origin
Local commits are relocated on top of fresh foreign ones — history stays linear.

What does git pull --ff-only do?
- Refuses if fast-forward is impossible
- Always creates a merge commit
- Deletes local commits
- Forcibly rewrites history
* Correct answer: Refuses if fast-forward is impossible
If the branches diverged, --ff-only stops with an error without changing anything.

What does -u do in git push -u origin main?
- Sets upstream: the link of the branch with origin/main
- Sends forcibly
- Sends all branches
- Creates a remote
* Correct answer: Sets upstream: the link of the branch with origin/main
After -u further git push commands work without specifying remote and branch.

How does --force-with-lease differ from --force?
- It first checks that the remote branch has not changed since the last fetch
- It only works with bare repositories
- It does not allow rewriting history at all
- It requires explicit confirmation
* Correct answer: It first checks that the remote branch has not changed since the last fetch
If someone managed to push, --force-with-lease refuses, while bare --force wipes other people's work.

What happens on git push if the remote has commits that are not local?
- The push is refused (not fast-forward)
- The push succeeds with a merge
- The push deletes other people's commits
- The push creates a new branch
* Correct answer: The push is refused (not fast-forward)
A regular push requires fast-forward; otherwise — refusal with a hint about force.

What does git worktree add ../fix -b hotfix/fix create?
- A new working copy on a new branch
- A clone of the whole repository
- A bare repository
- A new remote
* Correct answer: A new working copy on a new branch
Worktree adds another working tree of the same repository on the given branch.

How to see all working trees?
- git worktree list
- git branch --trees
- git show --worktrees
- git trees --all
* Correct answer: git worktree list
The command prints the paths and branches of all working trees.

Which order of actions is correct before pushing a feature branch after a long work?
- git pull --rebase origin main, then push
- git push, then pull
- git commit --amend, then push --force
- Only git fetch
* Correct answer: git pull --rebase origin main, then push
First synchronize with main (rebase) so history is linear, then push.

<!--/QUIZ-->
