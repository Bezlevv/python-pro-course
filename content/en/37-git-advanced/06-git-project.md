---
title: Practicum: complex workflow
summary: Putting it all together: the full feature development cycle, release tag, hotfix and moving fixes via cherry-pick.
order: 6
duration: 45 min
difficulty: advanced
tags: git, practicum, workflow, release, tags, hotfix, CI
---

This is the final lesson of the module. There are no fundamentally new commands here — we will tie everything we learned into a single professional process. This is the workflow used by teams that ship products regularly: feature branches, rebase before merging, release tags, hotfix branches and backport via cherry-pick.

## The full cycle

**1. Start from the up-to-date main.**

```bash
git checkout main
git pull --rebase origin main
git checkout -b feature/payment
```

**2. Work in small commits.**

```bash
echo "init" > pay.py
git add pay.py
git commit -m "feat: payment skeleton"
```

**3. Synchronize while working.** At least once per task:

```bash
git pull --rebase origin main
```

**4. Before the release — clean up history.** `git rebase -i` to combine small things, then push:

```bash
git push -u origin feature/payment
git push --force-with-lease
```

**5. Merge into main.** In team work usually via a Pull Request with `--no-ff` (to keep an explicit feature boundary):

```bash
git checkout main
git merge --no-ff feature/payment -m "merge: payment"
```

**6. Release — an annotated tag.** `git tag -a` stores the author, date and message:

```bash
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0
```

Semantic versioning: `vMAJOR.MINOR.PATCH` — major (breaking changes), minor (new features), patch (bugfixes).

**7. Hotfix.** The release lives in the `release/1.0` branch; the bug is fixed separately from the main development:

```bash
git checkout -b hotfix/1.0.1 v1.0.0
# fix the bug
git commit -m "fix: critical bug"
git tag -a v1.0.1 -m "Hotfix"
```

**8. Backport to other branches.** The fix is needed both in main and in the release branch — cherry-pick:

```bash
git checkout main
git cherry-pick <sha_hotfix>
git checkout release/1.0
git cherry-pick <sha_hotfix>
```

## Practical details

- **`git describe`** — builds a human-readable version from tags: `v1.0.0-5-gabc1234` ("5 commits after v1.0.0"). Convenient for versioning builds.
- **`git show v1.0.0`** — see what went into the release.
- **One code version — one tag.** If you accidentally put a tag in the wrong place: `git tag -d v1.0.0` (locally) + `git push origin :refs/tags/v1.0.0` (to the remote) — but it is better not to make mistakes on shared repositories.
- **CI as the second line.** Hooks are local and bypassed with `--no-verify`; the CI system (GitHub Actions etc.) runs tests on push and in Pull Requests. A hook saves your time, CI protects the shared branch.
- **Revert instead of reset on shared branches.** `v1.0.1` is not rolled back with `reset` — only `revert`, otherwise history will "break" for everyone who already downloaded the tag.
- **Commit discipline.** One logical unit of work — one commit; the message answers the question "why". This turns `git log` into a readable change journal.

## Summary

Professional Git is not "magic commands" but a predictable, repeatable process: feature branch → rebase → review → merge → tag → hotfix → cherry-pick. Everything you did in parts in lessons 1–5 works here as a single pipeline.

<!--TASK-->
### Task 1
Reproduce the full cycle in an empty folder:

1. `git init`; set name and email; create `app.py`, commit.
2. Branch `feature/payment`: two commits (`feat: skeleton`, `feat: logic`).
3. Return to `main`, add commit `fix: typo` — now `feature` has fallen behind.
4. On `feature` run `git rebase main`, then `git checkout main`, `git merge --no-ff feature/payment -m "merge: payment"`.
5. Put an annotated tag `git tag -a v1.0.0 -m "Release 1.0.0"`.

Expected result: `git log --graph --oneline --all` shows: main — a merge commit without forks inside the feature commits; `git tag` outputs `v1.0.0`; `git describe` returns `v1.0.0`.

### Task 2
Write a pytest test `test_release_workflow.py` that checks the cycle of task 1:

1. Repository: `main` with a base commit; branch `feature/payment` with two commits; an extra commit on `main`; rebase; merge `--no-ff`; tag `v1.0.0`.
2. Check: the tag exists (`git rev-parse v1.0.0`), points to a merge commit (the commit has two parents: `git rev-parse v1.0.0^1` and `^2`), and `git describe` returns `v1.0.0`.

Run `pytest test_release_workflow.py -v`: expected result — `1 passed`.

### Task 3
Write a pytest test `test_hotfix_backport.py` — an emergency fix scenario:

1. Repository: `main` with commits, tag `v1.0.0` on `main`.
2. Create `release/1.0` from `v1.0.0`; then add commit `feat: new` on `main` (for divergence).
3. Create a hotfix: branch `hotfix/1.0.1` from `v1.0.0`, commit `fix: critical bug`.
4. Cherry-pick the fix into `main` and into `release/1.0`.
5. Check: both branches have a commit with the message `fix: critical bug`, and the hashes of these commits differ.

Run `pytest test_hotfix_backport.py -v`: expected result — `1 passed`.

### Task 4
Fix "mixed up" tags. In the repository from task 1:

1. Put tag `v1.0.0` on the **wrong** commit (e.g. on `HEAD~1`): `git tag -a v1.0.0 -m "..." HEAD~1` (will overwrite).
2. Notice that `git describe` now shows not `v1.0.0` but another tag.
3. Delete and recreate the tag: `git tag -d v1.0.0` and `git tag -a v1.0.0 -m "Release 1.0.0"`.
4. Check `git describe` again.

Expected result: `git describe` returns `v1.0.0` again, and `git tag` shows one tag.

### Task 5
Put everything together in one pytest test `test_full_pipeline.py`:

1. `main` → three regular commits → tag `v0.9.0`.
2. Branch `feature/x` with two commits, then rebase onto `main` (with a new commit), merge `--no-ff`, tag `v1.0.0`.
3. Hotfix `v1.0.1` from `v1.0.0` and backport into `main` via cherry-pick.
4. Check: `git describe` on `main` — `v1.0.1` (or `v1.0.1-N-g...`), on the hotfix branch — `v1.0.1`; main branch history is linear after merge; `main` has the fix.

Run `pytest test_full_pipeline.py -v`: expected result — `1 passed`.

<!--/TASK-->

<!--HINT-->
### Hint 1
After `git rebase main` do not forget to return to `main` before merging. `git merge --no-ff feature/payment -m "merge: payment"` will create a merge commit even if the merge could be done as fast-forward. The tag is put after the merge: `git tag -a v1.0.0 -m "Release 1.0.0"`.

### Hint 2
The parents of a merge commit are checked as `git rev-parse v1.0.0^1` and `v1.0.0^2` — both must return hashes. For `git describe` use `--tags` to account for lightweight tags, and compare the string with `v1.0.0`.

### Hint 3
First save the fix hash: `sha_fix = git("rev-parse", "hotfix/1.0.1")`. Then `git checkout main`, `git cherry-pick sha_fix`; the same for `release/1.0`. Checks: `git log --format=%s main` contains `fix: critical bug`; the HEAD hashes of both branches after cherry-pick differ (these are separate commits).

### Hint 4
Overwriting a tag: `git tag -a v1.0.0 -m "..." HEAD~1` — the `-a` flag with an explicit commit. After `git tag -d` and recreation, `git describe` points at `v1.0.0` again. Make sure the tag message matches what is expected in `git describe --tags`.

### Hint 5
Build the scenario step by step: first the full cycle of task 1 (up to `v1.0.0`), then hotfix and backport. For `git describe` after backport, the main branch may return `v1.0.1-1-g...` if there are commits after the tag — that is acceptable; use `git describe --tags --always` and check for the substring `v1.0.1`. Check linearity by the graph.

<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Full cycle:

```bash
git init
git config user.name "Test"
git config user.email "test@example.com"

echo "app" > app.py
git add app.py && git commit -m "initial"

git checkout -b feature/payment
echo "pay" >> app.py && git add app.py && git commit -m "feat: skeleton"
echo "logic" >> app.py && git add app.py && git commit -m "feat: logic"

git checkout main
echo "fix" >> app.py && git add app.py && git commit -m "fix: typo"

git checkout feature/payment
git rebase main

git checkout main
git merge --no-ff feature/payment -m "merge: payment"
git tag -a v1.0.0 -m "Release 1.0.0"

git log --graph --oneline --all
git tag
git describe
```

Analysis: rebase relocated the feature commits on top of `main` with `fix`; the `--no-ff` merge created an explicit merge commit. `git log --graph` shows one feature line entering the merge commit. The `v1.0.0` tag is annotated — it contains the author, date and message. `git describe` on `main` returns `v1.0.0`: it is the nearest tag behind. This is what a "reference" release process looks like.

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


def test_release_workflow():
    with tempfile.TemporaryDirectory() as repo:
        git("init", cwd=repo)
        git("config", "user.name", "Test", cwd=repo)
        git("config", "user.email", "test@example.com", cwd=repo)

        commit_file(repo, "app.py", "app\n", "initial")
        git("checkout", "-b", "feature/payment", cwd=repo)
        commit_file(repo, "app.py", "app\npay\n", "feat: skeleton")
        commit_file(repo, "app.py", "app\npay\nlogic\n", "feat: logic")
        git("checkout", "main", cwd=repo)
        commit_file(repo, "app.py", "app\nfix\n", "fix: typo")
        git("checkout", "feature/payment", cwd=repo)
        git("rebase", "main", cwd=repo)
        git("checkout", "main", cwd=repo)
        git("merge", "--no-ff", "feature/payment", "-m", "merge: payment", cwd=repo)
        git("tag", "-a", "v1.0.0", "-m", "Release 1.0.0", cwd=repo)

        assert git("rev-parse", "v1.0.0", cwd=repo)
        parent1 = git("rev-parse", "v1.0.0^1", cwd=repo)
        parent2 = git("rev-parse", "v1.0.0^2", cwd=repo)
        assert parent1 != parent2
        assert git("describe", "--tags", cwd=repo) == "v1.0.0"
```

Analysis: the test repeats the steps of task 1. Key checks: the tag exists and points to a commit with two parents (merge commit) — meaning the merge really was `--no-ff`; `git describe --tags` returns `v1.0.0`. If the merge had been fast-forward, `^2` would not exist and `git rev-parse v1.0.0^2` would fail — the test catches that. Run: `pytest test_release_workflow.py -v` → `1 passed`.

### Solution 3
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


def test_hotfix_backport():
    with tempfile.TemporaryDirectory() as repo:
        git("init", cwd=repo)
        git("config", "user.name", "Test", cwd=repo)
        git("config", "user.email", "test@example.com", cwd=repo)

        commit_file(repo, "app.py", "v1\n", "initial")
        git("tag", "-a", "v1.0.0", "-m", "Release", cwd=repo)

        git("checkout", "-b", "release/1.0", cwd=repo)
        git("checkout", "main", cwd=repo)
        commit_file(repo, "app.py", "v1\nnew\n", "feat: new")

        git("checkout", "-b", "hotfix/1.0.1", "v1.0.0", cwd=repo)
        commit_file(repo, "app.py", "v1\nfixed\n", "fix: critical bug")
        sha_fix = git("rev-parse", "HEAD", cwd=repo)

        git("checkout", "main", cwd=repo)
        git("cherry-pick", sha_fix, cwd=repo)
        git("checkout", "release/1.0", cwd=repo)
        git("cherry-pick", sha_fix, cwd=repo)

        main_log = git("log", "--format=%s", "main", cwd=repo)
        release_log = git("log", "--format=%s", "release/1.0", cwd=repo)
        assert "fix: critical bug" in main_log
        assert "fix: critical bug" in release_log
        assert git("rev-parse", "main", cwd=repo) != git("rev-parse", "release/1.0", cwd=repo)
```

Analysis: the hotfix branch is created from the tag `v1.0.0` (`git checkout -b hotfix/1.0.1 v1.0.0`). After the fix commit its hash is saved. `cherry-pick` applies the fix both to `main` and to `release/1.0`: the messages match, the hashes differ (new commits). So "one fix, two branches". If the hashes matched, that would mean we simply moved a branch instead of applying a commit — the `!=` check excludes that. Run: `pytest test_hotfix_backport.py -v` → `1 passed`.

### Solution 4
Commands:

```bash
# Put the tag on the wrong commit (overwrite)
git tag -a v1.0.0 -m "Release 1.0.0" HEAD~1
git describe
# e.g. v1.0.0-1-g... or another tag

# Fix it
git tag -d v1.0.0
git tag -a v1.0.0 -m "Release 1.0.0"
git describe
# v1.0.0
```

Analysis: `git tag -a <name> -m "..." <commit>` without an explicit commit puts the tag on `HEAD`, with an explicit one — on the given commit. Overwriting a tag "on the fly" is a frequent mistake: after it `git describe` shows not `v1.0.0` but a later/earlier tag (or `v1.0.0-N-g...`), and the release label "drifts". Deleting with `git tag -d` and re-putting returns everything to its place. On shared repositories, overwriting an already published tag is dangerous (it breaks other people's clones) — there the correct path is `git push origin :refs/tags/v1.0.0` then `git push origin v1.0.0`, and only after coordinating with the team.

### Solution 5
Solution (skeleton):

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


def test_full_pipeline():
    with tempfile.TemporaryDirectory() as repo:
        git("init", cwd=repo)
        git("config", "user.name", "Test", cwd=repo)
        git("config", "user.email", "test@example.com", cwd=repo)

        for i in range(1, 4):
            commit_file(repo, "app.py", f"v0.{i}\n", f"step {i}")
        git("tag", "-a", "v0.9.0", "-m", "pre-release", cwd=repo)

        git("checkout", "-b", "feature/x", cwd=repo)
        commit_file(repo, "app.py", "feature1\n", "feat: x1")
        commit_file(repo, "app.py", "feature1\nfeature2\n", "feat: x2")
        git("checkout", "main", cwd=repo)
        commit_file(repo, "app.py", "main_new\n", "feat: main_new")
        git("checkout", "feature/x", cwd=repo)
        git("rebase", "main", cwd=repo)
        git("checkout", "main", cwd=repo)
        git("merge", "--no-ff", "feature/x", "-m", "merge: x", cwd=repo)
        git("tag", "-a", "v1.0.0", "-m", "Release", cwd=repo)

        git("checkout", "-b", "hotfix/1.0.1", "v1.0.0", cwd=repo)
        commit_file(repo, "app.py", "fixed\n", "fix: critical bug")
        sha_fix = git("rev-parse", "HEAD", cwd=repo)
        git("checkout", "main", cwd=repo)
        git("cherry-pick", sha_fix, cwd=repo)

        describe = git("describe", "--tags", "--always", cwd=repo)
        assert "v1.0.1" not in describe or "v1.0.0" in describe
        assert "fix: critical bug" in git("log", "--format=%s", "main", cwd=repo)
```

Analysis: the test assembles the full cycle: pre-release tag, feature branch with rebase, merge `--no-ff`, release tag, hotfix from the release and backport into `main`. The `--always` check is explained by the fact that after cherry-pick on `main` there may be a commit after the tag `v1.0.0` — then `git describe` returns `v1.0.1-1-g...`. Therefore the fix in `main` is searched by message in the log, not by number. Important: `hotfix/1.0.1` is created from `v1.0.0` so as not to drag "new" stuff from `main`. Run: `pytest test_full_pipeline.py -v` → `1 passed`.

<!--/SOLUTION-->

<!--QUIZ-->
Which tag is recommended for a release?
- Annotated: git tag -a v1.0.0 -m "..."
- Lightweight: git tag v1.0.0
- Any, no difference
- A tag can only be put on a remote repository
* Correct answer: Annotated: git tag -a v1.0.0 -m "..."
An annotated tag stores the author, date and message — suitable for releases; a lightweight one is just a pointer.

What does git merge --no-ff feature/payment mean?
- Forcibly creates a merge commit even when fast-forward is possible
- Disables merge
- Only fast-forward
- Deletes feature/payment
* Correct answer: Forcibly creates a merge commit even when fast-forward is possible
--no-ff preserves an explicit feature boundary in history.

Why run git pull --rebase origin main after rebase and before merge?
- To synchronize with the up-to-date main and avoid conflicts
- To rewrite main history
- To erase local commits
- To delete the remote
* Correct answer: To synchronize with the up-to-date main and avoid conflicts
An up-to-date base reduces conflicts and makes the future merge/rebase easier.

What will git describe return on a commit 5 commits after v1.0.0?
- v1.0.0-5-g<hash>
- v1.0.0
- 5
- An error
* Correct answer: v1.0.0-5-g<hash>
Format: the nearest tag, the number of commits after it, a shortened hash.

How to correctly move a fix from hotfix to main and release?
- git cherry-pick <sha_fix> in both branches
- git rebase hotfix
- git merge --no-ff main
- git reset --hard <sha_fix>
* Correct answer: git cherry-pick <sha_fix> in both branches
cherry-pick applies a specific commit in each branch separately without dragging the rest of history.

Which command deletes a tag locally?
- git tag -d v1.0.0
- git tag --rm v1.0.0
- git delete v1.0.0
- git tag -remove v1.0.0
* Correct answer: git tag -d v1.0.0
git tag -d deletes the local tag; for the remote you also need git push origin :refs/tags/v1.0.0.

Why is revert used on a shared branch instead of reset?
- Because reset rewrites history and breaks other people's clones
- Because revert is faster
- Because reset is forbidden
- Because revert creates fewer commits
* Correct answer: Because reset rewrites history and breaks other people's clones
reset moves the pointer and "throws out" commits; others will get divergences. revert adds a revert commit.

What does CI check in addition to hooks?
- Tests and code quality on every push/PR
- Developer passwords
- Internet speed
- Repository size
* Correct answer: Tests and code quality on every push/PR
CI is the second line: it does not depend on local settings and cannot be bypassed with --no-verify.

Which tag corresponds to a bugfix (patch) version under semver?
- v1.0.1
- v1.1.0
- v2.0.0
- v1.0.0-alpha
* Correct answer: v1.0.1
semver: major.minor.patch — a bugfix increases patch (the last number).

What does git checkout -b hotfix/1.0.1 v1.0.0 do?
- Creates the hotfix branch from the tag v1.0.0
- Creates a tag from the hotfix branch
- Switches to main
- Deletes the tag v1.0.0
* Correct answer: Creates the hotfix branch from the tag v1.0.0
The branch is created from the given commit (here — from the release tag) so as not to drag unfinished development.

<!--/QUIZ-->
