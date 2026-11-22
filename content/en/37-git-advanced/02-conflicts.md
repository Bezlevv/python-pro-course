---
title: Resolving conflicts
summary: Why conflicts arise, how to read the markers <<<<<<<, =======, >>>>>>>, how to resolve them manually, with commands, and automatically via rerere.
order: 2
duration: 40 min
difficulty: advanced
tags: git, conflicts, merge, rebase, rerere, mergetool
---

A conflict is not a Git error but a normal event: two branches changed **the same place** of the same file, and Git cannot decide on its own which variant is correct. It honestly stops and asks you to choose. The ability to resolve conflicts quickly and calmly is the main practical skill of any developer working in a team.

## What a conflict looks like

Scenario: both `main` and `feature` changed the `VERSION` line in `app.py`. On `git merge feature` or `git rebase main`, Git will report:

```bash
CONFLICT (content): Merge conflict in app.py
Automatic merge failed; fix conflicts and then commit the result.
```

And markers appear in the file itself:

```
<<<<<<< HEAD
VERSION = "1.1"
=======
VERSION = "1.2"
>>>>>>> feature
```

- `<<<<<<< HEAD` — start of the conflicting block, followed by **your** version (in rebase, `HEAD` is the branch being rebased, i.e. our feature);
- `=======` — separator between versions;
- `>>>>>>> feature` — end of the block, followed by the version from the other branch.

The task: keep the needed variant (or combine both), **delete all three markers** and save the file.

## How to determine the scale

First, look at which files are affected:

```bash
git status          # Unmerged paths section
git diff            # changes relative to the index
```

`git status` will mark conflicting files with status `UU` (both modified). Then open each file and look for markers. If there are many conflicts, it is convenient to search for them manually or via `git grep`:

```bash
git grep -n '^<<<<<<<'
```

## Ways to resolve

**1. Manually.** Open the file in an editor, keep what you need, remove the markers, then:

```bash
git add app.py
git commit          # for merge — completes the merge
# or for rebase:
git rebase --continue
```

**2. Choose one of the versions entirely.** If you already know which version you need, you do not have to edit the file:

```bash
git checkout --ours app.py     # take our version
git checkout --theirs app.py   # take their version
```

Attention: with `merge` and `rebase` the meaning of `ours`/`theirs` is **opposite**:

| Operation | --ours | --theirs |
|---|---|---|
| git merge | the branch you are on (current) | the branch being merged in |
| git rebase | the branch being rebased (the result) | the base (main/upstream) |

Confusion here is the source of half of the ruined decisions. The rule: "ours is the branch into which changes are currently being merged, i.e. the current one; theirs is the one whose changes are being merged in".

**3. Visual tool.** `git mergetool` opens the configured tool (e.g. `meld`, `kdiff3`, `vimdiff`). Setup:

```bash
git config merge.tool vimdiff
git mergetool
```

After using the tool, do not forget `git add` and to finish the operation.

**4. Auto-remembering with rerere.** Rerere ("reuse recorded resolution") remembers how you resolved a conflict and automatically applies the solution the next time the **exact same** conflict occurs. Enable globally:

```bash
git config --global rerere.enabled true
```

During a conflict Git writes `Recorded preimage for 'app.py'` — that means the solution was remembered. Useful when rebasing the same branch often and the conflicts repeat.

## Conflicts during rebase

During rebase, conflicts usually arise per commit: Git applies commits one by one and may stop after each. Resolved — `git rebase --continue`; want to try again from scratch — `git rebase --abort`; skip a commit — `git rebase --skip`. Important: `git commit` during rebase does **not** finish it — only `--continue` does.

## How to prevent conflicts

- Synchronize more often: `git pull --rebase` before starting work and before a PR.
- Make small commits and short feature branches — less chance of touching the same lines.
- Do not mix a file rename and content edits in one commit.
- Agree on file formats (line ordering, style) — then "formatting conflicts" will not multiply.

<!--TASK-->
### Task 1
Create a temporary repository and reproduce a conflict manually:

1. `git init`; set name and email.
2. Create `config.py` with the line `PORT = 8000`, commit.
3. Create branch `feature`; in it change to `PORT = 9000`, commit.
4. Return to `main`; change to `PORT = 8080`, commit.
5. Run `git merge feature` — a conflict should arise.
6. Open `config.py`, find the markers, keep `PORT = 8080`, delete the markers, run `git add config.py` and `git commit`.

Expected result: `git status` shows a clean tree, `config.py` has no `<<<<<<<` marker, and `git log --oneline` contains a merge commit.

### Task 2
Write a pytest test `test_conflict_merge.py` that checks the "anatomy" of a conflict:

1. Temporary repository: base commit, branch `feature` changes a line, `main` changes the same line.
2. `git merge feature` must finish with a non-zero return code — check via `subprocess.run` without `check=True`.
3. Check that the file has all three markers `<<<<<<<`, `=======`, `>>>>>>>`.
4. Resolve the conflict: write the value from `main` into the file, delete the markers, `git add`, `git commit`.
5. Check that `git status` is clean and there are no markers left in the file.

Run `pytest test_conflict_merge.py -v`: expected result — `1 passed`.

### Task 3
Write a pytest test `test_conflict_rebase_ours.py` about the semantics of `--ours`/`--theirs` during rebase:

1. Scenario: `main` = `A`; branch `feature` from `A` with commit `B` (changes `VERSION = "1.1"`); then commit `D` on `main` (changes the same line to `VERSION = "1.2"`).
2. `git rebase main` (on `feature`) — conflict.
3. Run `git checkout --ours config.py`, then `git add config.py`, `git rebase --continue`.
4. Check that the final `config.py` has `VERSION = "1.1"` (the OURS variant, of the feature branch), not `"1.2"`.

Run `pytest test_conflict_rebase_ours.py -v`: expected result — `1 passed`.

### Task 4
Resolve a conflict "like a pro": in the repository from task 1 repeat steps 1–5, but instead of manual editing use:

```bash
git checkout --theirs config.py
git add config.py
git commit
```

Then do the same but with `--ours`, and compare the file contents. In your answer write a short conclusion: which value ended up in the file with `--ours` and which with `--theirs` in the context of **merge** (not rebase). Expected result: you can explain why in merge `--ours` is the variant of the current branch (main) and `--theirs` is the variant of the merged-in branch (feature).

### Task 5
Enable rerere and verify that a repeated conflict resolves itself:

1. `git config --global rerere.enabled true`.
2. Repeat the task 1 scenario (conflict on `PORT`), resolve it **manually** (keep `PORT = 8080`), finish the merge.
3. Change `PORT` in both branches again and try merging once more. Pay attention to the message `Resolved 'config.py' using previous resolution`.

Expected result: on the second merge Git does not stop, or stops but immediately applies the remembered solution; in any case `config.py` contains `PORT = 8080` without manual intervention. Verify that `git config rerere.enabled` returns `true`.

<!--/TASK-->

<!--HINT-->
### Hint 1
The markers go strictly in order: `<<<<<<< HEAD`, then `=======`, then `>>>>>>> feature`. Keep one line between the markers and delete all three marker lines entirely, including `<<<<<<<`, `=======` and `>>>>>>>`. After `git add` and `git commit` check `git grep -n '^<<<<<<<'` — the output should be empty.

### Hint 2
Without `check=True` `subprocess.run` returns an object with a `returncode` field — for a conflicting merge it will be `1`. Check markers by reading the file: `"<<<<<<< HEAD" in content`. To simulate "both branches change one line", write different values to the same line of the file in each commit.

### Hint 3
During rebase `--ours` is the branch being rebased (feature), `--theirs` is the base (main). So to keep the feature variant you need exactly `--ours`. After `git checkout --ours config.py` be sure to do `git add config.py` and `git rebase --continue`, otherwise Git will not understand that the conflict is resolved.

### Hint 4
Read the table in the theory: in `merge` `--ours` is the current branch (main), `--theirs` is the merged-in branch (feature). Do not confuse with rebase — there the roles swap. Run both variants in **different** clones or cancel the first merge with `git merge --abort` before the second experiment.

### Hint 5
After the first manual resolution, rerere saves the "image" of the conflict and the solution. For the second experiment, make the conflict **exactly the same** (same lines, same values). If the second merge finished without stopping — rerere worked. Check the setting: `git config rerere.enabled`.

<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Commands:

```bash
git init
git config user.name "Test"
git config user.email "test@example.com"

echo 'PORT = 8000' > config.py
git add config.py && git commit -m "base: config"

git checkout -b feature
sed -i 's/PORT = 8000/PORT = 9000/' config.py
git add config.py && git commit -m "feat: change port"

git checkout main
sed -i 's/PORT = 8000/PORT = 8080/' config.py
git add config.py && git commit -m "fix: port"

git merge feature
```

Git will report a conflict. Open `config.py`:

```
<<<<<<< HEAD
PORT = 8080
=======
PORT = 9000
>>>>>>> feature
```

Keep `PORT = 8080` (the main variant), delete the three marker lines:

```bash
git add config.py
git commit -m "merge: resolve port conflict"
```

Why this works: Git cannot decide on its own whose port is correct — both changes lie on the same line. After editing, the file is "clean" again, `git add` marks the conflict as resolved, and the final `git commit` creates a merge commit. Check: `git grep -n '^<<<<<<<'` prints nothing, `git status` shows a clean working tree.

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


def test_merge_conflict_anatomy():
    with tempfile.TemporaryDirectory() as repo:
        git("init", cwd=repo)
        git("config", "user.name", "Test", cwd=repo)
        git("config", "user.email", "test@example.com", cwd=repo)

        commit_file(repo, "config.py", "PORT = 8000\n", "base")

        git("checkout", "-b", "feature", cwd=repo)
        commit_file(repo, "config.py", "PORT = 9000\n", "feat: port")

        git("checkout", "main", cwd=repo)
        commit_file(repo, "config.py", "PORT = 8080\n", "fix: port")

        result = git("merge", "feature", cwd=repo, check=False)
        assert result.returncode != 0

        content = (Path(repo) / "config.py").read_text()
        assert "<<<<<<< HEAD" in content
        assert "=======" in content
        assert ">>>>>>> feature" in content

        (Path(repo) / "config.py").write_text("PORT = 8080\n")
        git("add", "config.py", cwd=repo)
        git("commit", "-m", "merge: resolve conflict", cwd=repo)

        status = git("status", "--porcelain", cwd=repo).stdout
        assert status == ""
        content = (Path(repo) / "config.py").read_text()
        assert "<<<<<<<" not in content
```

Key point: `merge` is called with `check=False` so it does not fail on a non-zero code — a conflict is exactly a non-zero `returncode`. Markers are checked as plain text. Resolving the conflict is writing one of the variants over the whole file, then `add` and `commit`. Final checks: `git status --porcelain` is empty (clean tree) and there are no markers. Run: `pytest test_conflict_merge.py -v` → `1 passed`.

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


def test_rebase_conflict_ours_is_feature():
    with tempfile.TemporaryDirectory() as repo:
        git("init", cwd=repo)
        git("config", "user.name", "Test", cwd=repo)
        git("config", "user.email", "test@example.com", cwd=repo)

        commit_file(repo, "config.py", 'VERSION = "1.0"\n', "base")

        git("checkout", "-b", "feature", cwd=repo)
        commit_file(repo, "config.py", 'VERSION = "1.1"\n', "feat: 1.1")

        git("checkout", "main", cwd=repo)
        commit_file(repo, "config.py", 'VERSION = "1.2"\n', "feat: 1.2")

        git("checkout", "feature", cwd=repo)
        result = git("rebase", "main", cwd=repo, check=False)
        assert result.returncode != 0

        git("checkout", "--ours", "config.py", cwd=repo)
        git("add", "config.py", cwd=repo)
        git("rebase", "--continue", cwd=repo)

        content = (Path(repo) / "config.py").read_text()
        assert 'VERSION = "1.1"' in content
```

Analysis of the key point: during rebase Git lays the `feature` commits on top of `main`. At the moment of conflict, `HEAD` is the "rebased" branch (`feature`, our variant), and `theirs` is the base (`main`). So `--ours` keeps `"1.1"` from the feature. This is where people get confused most often: with merge it would be the other way around. The check asserts `"1.1"` — which proves the test understands the semantics. Run: `pytest test_conflict_rebase_ours.py -v` → `1 passed`.

### Solution 4
For merge the table is correct: `--ours` is the current branch (main), `--theirs` is the merged-in branch (feature). After `git checkout --theirs config.py` the file will have `PORT = 9000` (from `feature`), after `git checkout --ours config.py` — `PORT = 8080` (from `main`). Final comment: "in merge --ours takes the variant of the current branch (main), and --theirs the variant of the merged-in branch (feature); in rebase the roles swap: --ours is the rebased branch, --theirs is the base". This asymmetry is a consequence of merge and rebase having different "current" branches in Git's interpretation. Once you remember it, you will stop making mistakes in the choice.

### Solution 5
After enabling `rerere.enabled` and manually resolving the first conflict, Git saved the "image" of the conflict and the solution. Git recognizes a repeated identical conflict and applies the saved solution, writing `Resolved 'config.py' using previous resolution`. The second merge may not stop at all — Git immediately substitutes `PORT = 8080`. This is very convenient for long-lived branches where the same conflicts arise on every rebase. Check: `git config rerere.enabled` → `true`. Caveat: rerere remembers the solution by the content of the conflicting **hunks**, so small edits in neighboring lines can prevent "recognition" — that is normal.

<!--/SOLUTION-->

<!--QUIZ-->
What do the markers <<<<<<< HEAD ... >>>>>>> feature mean in a file?
- Places where Git could not merge the variants from two branches
- Developer comments
- Formatting settings
- Syntax errors in code
* Correct answer: Places where Git could not merge the variants from two branches
Git marks the conflicting sections: on top — your variant, below — the variant of the other branch.

What should you do with the markers when resolving a conflict?
- Leave them in the file
- Delete all three markers and keep the needed variant
- Turn them into comments
- Move them to the end of the file
* Correct answer: Delete all three markers and keep the needed variant
The markers are auxiliary markup: after choosing a variant they must be deleted.

Which command finishes a merge after resolving a conflict?
- git rebase --continue
- git commit (after git add)
- git merge --commit
- git checkout --commit
* Correct answer: git commit (after git add)
After `git add` of the resolved files, a regular git commit creates the merge commit. (For rebase — only git rebase --continue.)

What does --ours mean in git merge?
- The variant of the current branch into which changes are being merged
- The variant of the branch being merged in
- The variant from the index
- The variant from the stash
* Correct answer: The variant of the current branch into which changes are being merged
In merge, --ours is the current branch (e.g. main), --theirs is the merged-in branch (feature). In rebase the roles swap.

What does --theirs mean in git rebase?
- The variant of the rebased branch (feature)
- The variant of the base onto which the rebase happens (main)
- The variant from the reflog
- The variant from the last commit
* Correct answer: The variant of the base onto which the rebase happens (main)
In rebase ours is the branch being rebased, theirs is the base. This is the opposite of merge.

What does rerere do?
- Remembers conflict resolutions and applies them on repeat
- Deletes all conflicts automatically
- Disables merges
- Creates backup copies of files
* Correct answer: Remembers conflict resolutions and applies them on repeat
reuse recorded resolution: a repeated identical conflict is resolved automatically with the saved solution.

What happens after git rebase --abort?
- The rebase is cancelled, the branch returns to its original state
- The conflict is resolved automatically
- A merge commit is created
- The rebase continues skipping the conflict
* Correct answer: The rebase is cancelled, the branch returns to its original state
--abort rolls back the rebase entirely, returning the branch to its state before it started.

How to check that no conflict markers are left in the repository?
- git grep -n '^<<<<<<<'
- git log --markers
- git diff --checkmarkers
- git status --markers
* Correct answer: git grep -n '^<<<<<<<'
The command searches all tree files for lines starting with the marker.

Which command opens an external comparison tool?
- git mergetool
- git conflict --tool
- git diff --manual
- git merge --visual
* Correct answer: git mergetool
git mergetool launches the configured tool (meld, vimdiff, etc.) for each conflicting file.

Which of the following reduces the likelihood of conflicts?
- Frequent git pull --rebase and small commits
- Working in one branch without pull
- Renaming files together with editing content
- Big commits once a month
* Correct answer: Frequent git pull --rebase and small commits
Small commits and constant synchronization reduce overlapping changes in the same lines.

<!--/QUIZ-->
