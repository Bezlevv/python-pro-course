---
title: Git hooks and automation
summary: How Git invokes hooks at key moments, how to write pre-commit, commit-msg and pre-push hooks, how to store them in the repository.
order: 4
duration: 40 min
difficulty: advanced
tags: git, hooks, pre-commit, commit-msg, pre-push, automation
---

Git hooks are scripts that Git runs automatically at key moments: before committing, before push, after merge, and so on. They turn Git from "just a version store" into a tool of discipline: you cannot commit code with forbidden secrets, cannot push bad messages, cannot bypass tests. This is the most practical way to automate quality control at the repository level.

## Where hooks live

Hooks live in `$GIT_DIR/hooks/` (by default `.git/hooks/`):

```bash
ls .git/hooks/
# applypatch-msg.sample  commit-msg.sample  post-commit.sample
# pre-commit.sample  pre-push.sample  ...
```

Everything in `.git/hooks/` is part of the local repository, not the code, so it does **not** get into git. To share hooks with the team, store them in the repository (e.g. in `scripts/hooks/`) and tell Git where to look for them:

```bash
mkdir -p scripts/hooks
git config core.hooksPath scripts/hooks
```

Now Git runs `scripts/hooks/pre-commit` instead of `.git/hooks/pre-commit`. The file must be executable (`chmod +x`).

## How a hook works

A hook is an executable script (bash, Python, anything). The exit code decides everything:

- **0** — the action is allowed, Git continues;
- **non-zero** — Git **stops** the operation with a message from stderr.

Example of the simplest `pre-commit` in bash:

```bash
#!/bin/sh
echo "Committing!"
exit 0
```

## Important hooks

**pre-commit** — before creating a commit. The classic: run a linter/tests, check that there are no conflict markers or secrets:

```bash
#!/bin/sh
if git grep -n '<<<<<<<' -- ':!*.md'; then
  echo "Conflict markers found"; exit 1
fi
```

**commit-msg** — after entering the message, before creating the commit. It receives the path to the file with the message. Ideal for checking the format:

```bash
#!/bin/sh
grep -qE '^(feat|fix|docs|refactor|test|chore):' "$1" \
  || { echo "The message must start with feat:/fix:/..."; exit 1; }
```

**pre-push** — before pushing to the remote. It receives the remote name and URL. Standard protection: do not push to `main` directly, run tests:

```bash
#!/bin/sh
pytest -q || exit 1
```

**Others:** `pre-rebase` (forbid rebasing published branches), `post-commit` (notifications, metric generation), `post-merge`, `post-checkout`, `prepare-commit-msg` (auto-insert the task number).

## A hook in Python

A hook does not have to be in bash. For example, `pre-commit` in Python:

```python
#!/usr/bin/env python3
import subprocess, sys

out = subprocess.run(["git", "diff", "--cached", "--name-only"],
                     capture_output=True, text=True).stdout
if any("secret" in name.lower() for name in out.splitlines()):
    print("Do not commit files with the word secret in the name!")
    sys.exit(1)
```

## Best practices

- Locally for a quick start: `git config core.hooksPath scripts/hooks` + scripts in `scripts/hooks/`.
- In a team: agree on a set of hooks, put them in the repository, and the enabling instructions in the README. For automatic installation, tools like pre-commit (Python) or husky (JavaScript) are used — they install hooks themselves.
- Do not make hooks too slow: if `pre-commit` runs the whole test suite for 5 minutes, colleagues will start bypassing it (`git commit --no-verify`). Check only what concerns the index.
- Remember: a hook is not protection but a reminder: `--no-verify` bypasses any hook, so critical checks should also live in CI.

<!--TASK-->
### Task 1
Create a repository and the first hook:

1. `git init`; set name and email; create `app.py` and make a base commit.
2. Create `.git/hooks/pre-commit` — a bash script that searches for conflict markers in the index via `git grep -n '<<<<<<<'` and exits with code 1 if found.
3. Make it executable.
4. Add the marker `<<<<<<< HEAD` to `app.py` and try to commit — the commit must be blocked.
5. Remove the marker and commit again — it should pass.

Expected result: the first commit attempt fails with an error and the hook's message; the second passes, `git log --oneline` shows two commits.

### Task 2
Write a pytest test `test_commit_msg_hook.py`: a temporary repository, in `.git/hooks/commit-msg` — a script that only allows messages like `feat: ...` or `fix: ...` (regex `^(feat|fix):`). Then:

1. An attempt of `git commit -m "bad message"` must end with a non-zero code and not create a commit.
2. `git commit -m "feat: added check"` — successfully.
3. Check that `git log --oneline` contains exactly one commit (base + feat).

Run `pytest test_commit_msg_hook.py -v`: expected result — `1 passed`.

### Task 3
Write a pytest test `test_pre_push_hook.py`: a temporary repository with a remote repository (bare, `git init --bare`), in `.git/hooks/pre-push` — a script that always exits with code 1 and the message `push forbidden`. Then:

1. `git push origin main` must end with a non-zero code.
2. Check that the remote repository has no commits (`git log` there fails or is empty).

Run `pytest test_pre_push_hook.py -v`: expected result — `1 passed`.

### Task 4
Move hooks into the repository. In the repository from task 1:

1. Create the folder `scripts/hooks` and move your `pre-commit` there.
2. Run `git config core.hooksPath scripts/hooks`.
3. Commit the changes (the hook script itself should also get into history).
4. Check that the hook still works: add the marker again, try to commit — the block should fire.

Expected result: `git config core.hooksPath` returns `scripts/hooks`, and the hook blocks a commit with a marker even after you delete `.git/hooks/pre-commit`.

### Task 5
Write a `pre-commit` hook in Python that runs pytest on changed files:

1. Script: runs `pytest -q` (via `subprocess.run`), on failure prints `Tests failed!` and exits with code 1.
2. Add a test `test_math.py` with a deliberately failing test to the repository — try to commit: the commit must be blocked.
3. Fix the test, commit again.

Expected result: the first commit is blocked with the message `Tests failed!`, the second passes.

<!--/TASK-->

<!--HINT-->
### Hint 1
Inside the hook there are no `$1` arguments — we work with the staged changes. `git grep -n '<<<<<<<'` searches the whole tree, including working files; to limit to the index, you can use `git diff --cached` and `grep`, or simplified — `git grep` over files and a check via `if ...; then echo "..."; exit 1; fi`. Be sure to `chmod +x .git/hooks/pre-commit`.

### Hint 2
The hook script receives the path to the file with the message as `$1`. Check: `grep -qE '^(feat|fix):' "$1"`. In the test call `git commit` with `check=False` and check `returncode != 0`, then `git log --format=%s` — the message `bad message` must be absent there.

### Hint 3
For push you need a remote: create a bare repository with `git init --bare remote.git` in a temporary folder, add it with `git remote add origin <path>`. The `pre-push` hook fires before sending, so a non-zero code means an empty remote. Check emptiness: `git log` in the bare repository returns the error `does not have any commits` (non-zero code), or check via `git rev-parse --verify HEAD` with `check=False`.

### Hint 4
`git config core.hooksPath scripts/hooks` is a local repository setting, stored in `.git/config`, not in the code. After moving the script make sure it remained executable. `git add scripts/hooks/pre-commit` commits the hook itself — the team will see it in history.

### Hint 5
Python hook: `#!/usr/bin/env python3`, `subprocess.run(["pytest", "-q"])`, `sys.exit(1)` when `returncode != 0`. Remember: the hook runs from the repository root, so the path to the test is relative to it. Check that the file is executable and starts with a shebang.

<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Hook:

```bash
#!/bin/sh
if git grep -q -n '<<<<<<<' -- '*.py'; then
  echo "Error: conflict markers found" >&2
  exit 1
fi
```

Save to `.git/hooks/pre-commit`, make executable:

```bash
chmod +x .git/hooks/pre-commit
```

Now add the line `<<<<<<< HEAD` to `app.py` and try to commit:

```bash
echo '<<<<<<< HEAD' >> app.py
git add app.py
git commit -m "bad commit"
# Error: conflict markers found
# Commit not created
```

Remove the marker:

```bash
sed -i '/<<<<<<< HEAD/d' app.py
git add app.py
git commit -m "good commit"
```

Analysis: Git runs `pre-commit` when `git commit` is called. The script searches for markers with `git grep -q`, and if it finds them, prints a message to stderr and returns 1. Git sees the non-zero code and cancels the commit. This is the most reliable way not to "push" a conflict by accident: markers often remain after manual resolution, and the hook catches them before they get into history.

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


def test_commit_msg_hook_blocks_bad_format():
    with tempfile.TemporaryDirectory() as repo:
        git("init", cwd=repo)
        git("config", "user.name", "Test", cwd=repo)
        git("config", "user.email", "test@example.com", cwd=repo)

        (Path(repo) / "app.py").write_text("print('hi')\n")
        git("add", "app.py", cwd=repo)
        git("commit", "-m", "base", cwd=repo)

        hook = Path(repo) / ".git/hooks/commit-msg"
        hook.write_text("#!/bin/sh\ngrep -qE '^(feat|fix):' \"$1\" || { echo 'bad format'; exit 1; }\n")
        hook.chmod(0o755)

        bad = git("commit", "--allow-empty", "-m", "bad message",
                  cwd=repo, check=False)
        assert bad.returncode != 0

        good = git("commit", "--allow-empty", "-m", "feat: added check",
                   cwd=repo, check=False)
        assert good.returncode == 0

        log = git("log", "--format=%s", cwd=repo).stdout
        assert "bad message" not in log
        assert "feat: added check" in log
```

Analysis: the `commit-msg` hook receives the path to the temporary file with the message as `$1`. `grep -qE '^(feat|fix):'` checks the format; on failure — 1, and Git rejects the commit. In the test the first commit (`bad message`) is rejected, the second (`feat: ...`) is accepted; the log checks confirm the bad message did not get into history. `--allow-empty` is needed to not depend on file content. Run: `pytest test_commit_msg_hook.py -v` → `1 passed`.

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


def test_pre_push_hook_blocks_push():
    with tempfile.TemporaryDirectory() as tmp:
        repo = str(Path(tmp) / "repo")
        remote = str(Path(tmp) / "remote.git")
        Path(repo).mkdir()
        git("init", "--bare", remote)
        git("init", cwd=repo)
        git("config", "user.name", "Test", cwd=repo)
        git("config", "user.email", "test@example.com", cwd=repo)

        (Path(repo) / "app.py").write_text("x = 1\n")
        git("add", "app.py", cwd=repo)
        git("commit", "-m", "base", cwd=repo)
        git("remote", "add", "origin", remote, cwd=repo)

        hook = Path(repo) / ".git/hooks/pre-push"
        hook.write_text("#!/bin/sh\necho 'push forbidden' >&2; exit 1\n")
        hook.chmod(0o755)

        result = git("push", "origin", "main", cwd=repo, check=False)
        assert result.returncode != 0
        assert "push forbidden" in result.stderr

        head = git("rev-parse", "--verify", "HEAD", cwd=remote, check=False)
        assert head.returncode != 0
```

Analysis: `pre-push` fires before objects are sent. The script always returns 1 — the push is rejected. Checks: `returncode != 0` of push and the absence of HEAD in the bare repository (`rev-parse --verify HEAD` returns a non-zero code because the remote has no commits). This is an accurate model of the "hook does not let into prod" situation: for example, when you forgot to run tests or the branch did not pass review. Run: `pytest test_pre_push_hook.py -v` → `1 passed`.

### Solution 4
Steps:

```bash
mkdir -p scripts/hooks
git mv .git/hooks/pre-commit scripts/hooks/pre-commit   # or just cp
git config core.hooksPath scripts/hooks
git add scripts/hooks/pre-commit
git commit -m "chore: add pre-commit hook to the repository"
rm .git/hooks/pre-commit   # no longer needed — Git looks in scripts/hooks
```

Check:

```bash
git config core.hooksPath        # scripts/hooks
echo '<<<<<<< HEAD' >> app.py
git add app.py
git commit -m "test"            # blocked by the hook
```

Analysis: `core.hooksPath` redirects the hook lookup from `.git/hooks/` to `scripts/hooks/`. Now the hook is part of the code: it is visible in review, it will not be lost on clone, it can be versioned. The only nuance — `core.hooksPath` does not propagate automatically to others (it is a local setting), so new developers must run the same command once. Tools like pre-commit/husky exist precisely to automate this step: they generate config and install hooks themselves.

### Solution 5
Hook:

```python
#!/usr/bin/env python3
import subprocess
import sys

result = subprocess.run(["pytest", "-q", "test_math.py"])
if result.returncode != 0:
    print("Tests failed!", file=sys.stderr)
    sys.exit(1)
```

Save to `.git/hooks/pre-commit`, `chmod +x`. Test:

```python
def test_add():
    assert 1 + 1 == 3  # deliberately failing
```

Commit attempt:

```bash
git add test_math.py pre_commit.py
git commit -m "feat: add test"
# Tests failed!
# Commit cancelled
```

Fix `assert 1 + 1 == 2`, commit — it passes. Analysis: a Python hook is more convenient than bash for complex logic. The key point: `pytest` runs from the repository root, so paths are relative. Interception via `subprocess` gives full control: you can output not only the return code but also a fragment of the output, the list of failed tests, the branch, the username. Such a `pre-commit` is the first line of defense: it catches failing tests before they get into history, and CI remains the second line.

<!--/SOLUTION-->

<!--QUIZ-->
Where does Git look for hooks by default?
- In the .git/hooks/ folder
- In the repository root
- In the scripts/ folder
- In the .github/hooks/ folder
* Correct answer: In the .git/hooks/ folder
By default hooks live in .git/hooks/ (.sample files are examples).

Which return code allows an operation for a hook?
- 0
- 1
- 255
- 400
* Correct answer: 0
A zero code means success; any non-zero code stops the operation.

What does the pre-commit hook do?
- Runs before a commit is created and can block it
- Runs after push
- Checks the commit message
- Creates branches
* Correct answer: Runs before a commit is created and can block it
pre-commit runs before the commit is written; a non-zero code cancels the commit.

Which hook checks the format of the commit message?
- commit-msg
- pre-commit
- post-commit
- pre-push
* Correct answer: commit-msg
commit-msg receives the path to the file with the message and can reject the commit because of a bad format.

What does commit-msg receive as an argument?
- The path to the file with the commit message
- The commit hash
- The branch name
- The author name
* Correct answer: The path to the file with the commit message
$1 holds the path to the temporary file where Git stores the message text.

How to forbid a push to the remote with a hook?
- The pre-push script must return a non-zero code
- The post-push script must return 0
- Delete the remote
- Disable pre-commit
* Correct answer: The pre-push script must return a non-zero code
pre-push runs before sending; a non-zero code cancels the push.

How to make Git take hooks from scripts/hooks?
- git config core.hooksPath scripts/hooks
- git hooks --path scripts/hooks
- git config hooks.dir scripts/hooks
- Rename the folder to .git/hooks
* Correct answer: git config core.hooksPath scripts/hooks
The core.hooksPath setting points to the hooks directory instead of .git/hooks.

Which command bypasses hooks?
- git commit --no-verify
- git commit --force
- git commit --direct
- git commit --skip-hooks
* Correct answer: git commit --no-verify
--no-verify skips hooks, so critical checks should be duplicated in CI.

What language can be used for hooks?
- Any executable one: bash, Python, etc.
- Only bash
- Only C
- Only JavaScript
* Correct answer: Any executable one: bash, Python, etc.
A hook is any executable file with a shebang; Git does not restrict the language.

Why store hooks in the repository and not only in .git/hooks?
- To share them with the team and version them
- So they work faster
- So they cannot be bypassed
- So Git enables them automatically
* Correct answer: To share them with the team and version them
Hooks in scripts/hooks get into history and are visible to everyone; enabling is one core.hooksPath command.

<!--/QUIZ-->
