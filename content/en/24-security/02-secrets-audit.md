---
title: Secrets and Dependency Audit
summary: How to store keys and passwords safely, keep them out of code and repositories, and automatically check libraries for known vulnerabilities.
order: 2
duration: 40 min
difficulty: advanced
tags: secrets, keys, pip-audit, safety, CVE, CI
---

In this lesson we'll cover two topics that often go hand in hand: **secrets management** (passwords, tokens, API keys) and **dependency audit** (checking libraries for known vulnerabilities). Both are a mandatory part of the production culture of a Python developer.

## Why secrets must not go into code

A secret is any information that grants access: a database password, an `API_KEY` of a payment gateway, a private SSH key, Django's `SECRET_KEY`. If a secret lands in a Git repository, it stays in commit history forever: even if you delete the file, an attacker can pull it out of an old commit. So the rules are simple:

- secrets are **never stored in source code**;
- use environment variables, secret stores, and CI secrets instead.

Reading a secret from the environment:

```python
import os

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("DJANGO_SECRET_KEY is not set!")
```

Note: no default value. If a secret is not set — better to stop at once than silently work with an empty or fake key. Secrets can be kept in a `.env` file, but such a file must go into `.gitignore` so it doesn't get committed:

```gitignore
# .gitignore
.env
*.pem
config/keys/
```

For local development `python-dotenv` is handy — it loads `.env` into the environment, but in production secrets usually come from the orchestrator (Docker secrets, Kubernetes secrets, cloud managers) or secret stores like HashiCorp Vault.

## How to find leaked secrets

If you suspect a secret has already reached the repository, use scanners:

- `git-secrets` — prevents committing strings that look like secrets;
- `detect-secrets` — finds secrets in history and working files;
- `gitleaks` — a powerful scanner for repositories.

The simplest start is to run a detector over the current folder:

```bash
pip install detect-secrets
detect-secrets scan > .secrets.baseline
```

The `.secrets.baseline` file is a "snapshot" of known findings; afterwards the scanner warns only about new ones. In CI such a step is first — rewriting a commit is cheaper than revoking a compromised key.

## Dependency audit: pip-audit and safety

Even properly hidden secrets won't save you if your dependencies contain a vulnerability with a public exploit. Two main tools check packages for known CVEs:

- **pip-audit** — checks installed packages or `requirements.txt` against the OSV (Open Source Vulnerabilities) database;
- **safety** — checks dependencies against PyUp's own vulnerability database.

Installation and run:

```bash
pip install pip-audit safety
pip-audit -r requirements.txt
safety check -r requirements.txt
```

A useful output format is JSON — easy to parse in a script:

```bash
pip-audit -r requirements.txt --format json
```

And here is how to run the audit programmatically and parse the report:

```python
import json
import subprocess

result = subprocess.run(
    ["pip-audit", "-r", "requirements.txt", "--format", "json"],
    capture_output=True, text=True, check=True,
)
report = json.loads(result.stdout)
for finding in report.get("dependencies", []):
    print(finding["name"], finding["version"])
    for vuln in finding.get("vulns", []):
        print("  -", vuln["id"], vuln.get("description", "")[:60])
```

The report contains the package name, version, and a list of vulnerabilities with identifiers (CVE/OSV). In CI the audit is usually a blocking step: if there are vulnerabilities above a certain level — the pipeline fails, and updating dependencies becomes mandatory.

## What to do with the results

1. Update the package to a version where the vulnerability is fixed; if there is no fix — look for an alternative.
2. Pin versions: `requests==2.32.3`, not `requests>=2`.
3. Put the audit in CI for every PR.
4. Don't forget transitive dependencies — `pip-audit` checks them too.

```mermaid
flowchart LR
    A["Secrets"] --> B["Environment variables"]
    B --> C["Secret store"]
    D["Dependencies"] --> E["pip-audit"]
    E --> F["Vulnerabilities"]
```

## Lesson summary

Secrets — only through the environment and stores, never through code. Secret scanners — in pre-commit and CI. Dependencies — under the control of `pip-audit`/`safety` with a blocking audit. Now let's reinforce: we'll write a safe secret reader, a `requirements.txt` parser, a programmatic audit, a detector of leaked keys, and a secret redactor for text.

<!--TASK-->
### Task 1
Write a function `get_secret(name)` that returns the secret value from environment variables and **fails with an error** if it is not set. Use `os.environ.get(name)`, and if the result is `None` — raise `RuntimeError(f"Secret {name} is not set!")`. Then call `get_secret("STRIPE_API_KEY")` in a `try/except` block and print the error message via `except RuntimeError as e: print(e)`. The program must print exactly one line — the error message (assuming the variable is not set). This approach is deliberately "loud": silently working without a secret is not allowed.

### Task 2
Write a function `analyze_requirements(text)` that takes the contents of a `requirements.txt` file as a multiline string and returns a tuple of two numbers: the number of lines with a pinned version (`==`) and the number of lines without a hard version. For every non-empty line that doesn't start with `#`: if the line contains `==` — that's pinning, otherwise it's not. Call the function on the following text and print `Pinned: N, unpinned: M`:

```
django==5.0.6
requests>=2.31
flask==3.0.3
# comment
numpy
```

### Task 3
Write a script that runs `pip-audit -r requirements.txt --format json` via `subprocess.run`, parses the JSON, and for each dependency with vulnerabilities prints `Package: <name> <version>, vulnerabilities: <N>`. Be sure to pass `capture_output=True, text=True, check=True` and parse the result with `json.loads`. If the report has no dependencies with `vulns` — print `No vulnerabilities found`.

### Task 4
Write a function `scan_for_secrets(text)` that uses regular expressions to find possible leaked secrets in text: AWS keys of the form `AKIA` + 16 uppercase letters/digits and Stripe tokens of the form `sk_live_` + 24 characters. Return the list of found matches (the secret strings themselves). Use `re.findall` with the patterns `r"AKIA[0-9A-Z]{16}"` and `r"sk_live_[A-Za-z0-9]{24}"`. Test on the text `"key=AKIAIOSFODNN7EXAMPLE, stripe=sk_live_1234567890abcdefghijklmn"` and print each finding on a new line.

### Task 5
Write a class `SecretRedactor` that masks secrets in text before output. The constructor takes a list of secrets; the method `redact(text)` replaces every occurrence of a secret with `"***"` via `str.replace` and returns the result. Then create an instance with the secret `"supersecret"`, apply `redact` to the string `"Token: supersecret, all good"` and print the result. No occurrence of the real secret must appear on screen — instead, `***`. Such a redactor comes in handy before writing logs.
### Task 6 — Dependency audit
Install `pip-audit` and run `pip-audit` in the project. Expected result: a list of known vulnerabilities (or the message "No known vulnerabilities found"). Save the output to audit.txt.
### Task 7 — Checking secrets in git
Use `gitleaks detect` (or a regex script) to find possible secrets in the repository. Expected result: if there are no secrets — "no leaks found"; if there are — files are listed. Add a .gitignore for possible .env files.

<!--/TASK-->

<!--HINT-->
### Hint 1
`os.environ.get(name)` returns `None` if the variable is absent. Check specifically for `None`, not an empty string. Be sure to use `raise`, not `print`, inside the function — the error must stop the flow.
### Hint 2
Split the text with `text.splitlines()` and discard empty lines and comments (`line.strip().startswith("#")`). For the rest count `"==" in line`. Return the tuple `(pinned, unpinned)`.
### Hint 3
Pass the command as a list: `["pip-audit", "-r", "requirements.txt", "--format", "json"]`. In `subprocess.run` set `capture_output=True, text=True, check=True`. Report structure: `report["dependencies"]` — a list of dicts with keys `name`, `version`, `vulns`.
### Hint 4
`re.findall(pattern, text)` returns a list of all matches. Concatenate both lists with `+`. Make sure the AWS pattern captures exactly 16 characters after `AKIA`.
### Hint 5
In a loop over `self.secrets` do `text = text.replace(secret, "***")`. The method must return the modified text. Note: if a secret is part of another word, that word will be replaced too, so in reality masking is done on word boundaries.
### Hint 6
`pip install pip-audit && pip-audit` — by default checks the current environment.
### Hint 7
`gitleaks detect --source .` — scans for secrets; if gitleaks is missing, grep by key patterns.

<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
import os

def get_secret(name):
    value = os.environ.get(name)
    if value is None:
        raise RuntimeError(f"Secret {name} is not set!")
    return value

try:
    get_secret("STRIPE_API_KEY")
except RuntimeError as e:
    print(e)
```

Result:

```
Secret STRIPE_API_KEY is not set!
```

What's happening here? `os.environ.get` is safer than direct `os.environ[name]`: it doesn't raise `KeyError` but returns `None`. We explicitly check this case and raise a `RuntimeError` with a clear message. The application fails "loudly" rather than continuing with `None` — that's the fail-fast principle. In a real project the same function fits nicely in a configuration module: all secrets are gathered in one place, and if one is missing, the service doesn't start and CI shows the reason. Also remember: check for `None`, not for `""`, because an empty string is also a potential sign of a configuration error.

### Solution 2
Solution:

```python
def analyze_requirements(text):
    pinned = unpinned = 0
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if "==" in s:
            pinned += 1
        else:
            unpinned += 1
    return pinned, unpinned

sample = """django==5.0.6
requests>=2.31
flask==3.0.3
# comment
numpy"""

p, u = analyze_requirements(sample)
print(f"Pinned: {p}, unpinned: {u}")
```

Result:

```
Pinned: 2, unpinned: 2
```

What's happening here? `splitlines()` splits the text into lines; empty lines and comments are skipped. `django==5.0.6` and `flask==3.0.3` contain `==` — that's hard pinning, there are two. `requests>=2.31` and `numpy` have no hard version — also two. Pinning matters for build reproducibility: without it `pip install` may pull new minor versions that suddenly break production or bring a vulnerability. That's why serious projects use `==` combined with `constraints.txt` and a blocking audit.

### Solution 3
Solution:

```python
import json
import subprocess

result = subprocess.run(
    ["pip-audit", "-r", "requirements.txt", "--format", "json"],
    capture_output=True, text=True, check=True,
)
report = json.loads(result.stdout)

found = False
for dep in report.get("dependencies", []):
    vulns = dep.get("vulns", [])
    if vulns:
        found = True
        print(f"Package: {dep['name']} {dep['version']}, vulnerabilities: {len(vulns)}")
if not found:
    print("No vulnerabilities found")
```

What's happening here? `pip-audit` runs as an external process; `capture_output=True` catches the output, `text=True` turns it into a string, `check=True` raises an exception if the command exits with an error. `json.loads(result.stdout)` parses the report: a list of dicts under the key `dependencies`, each with `name`, `version`, and `vulns` (the list of vulnerabilities). If the list is non-empty — we print the name and the count. If `vulns` is nowhere — we print "not found". In CI such a script exits with a non-zero code on findings so the pipeline fails. The same approach works for `safety check --json`.

### Solution 4
Solution:

```python
import re

def scan_for_secrets(text):
    patterns = [
        r"AKIA[0-9A-Z]{16}",
        r"sk_live_[A-Za-z0-9]{24}",
    ]
    found = []
    for p in patterns:
        found.extend(re.findall(p, text))
    return found

text = "key=AKIAIOSFODNN7EXAMPLE, stripe=sk_live_1234567890abcdefghijklmn"
for secret in scan_for_secrets(text):
    print(secret)
```

Result:

```
AKIAIOSFODNN7EXAMPLE
sk_live_1234567890abcdefghijklmn
```

What's happening here? `re.findall` returns all non-overlapping matches of the pattern. The first pattern catches AWS access keys: the `AKIA` prefix plus 16 characters of `[0-9A-Z]`. The second catches Stripe test tokens with `sk_live_` and 24 characters. Both findings are printed. Of course, this is a simplified detector: real scanners (detect-secrets, gitleaks) account for entropy and context to avoid false positives. But even a simple regex detector running in CI catches the freshest leak before the commit reaches history.

### Solution 5
Solution:

```python
class SecretRedactor:
    def __init__(self, secrets):
        self.secrets = secrets

    def redact(self, text):
        for secret in self.secrets:
            text = text.replace(secret, "***")
        return text

redactor = SecretRedactor(["supersecret"])
print(redactor.redact("Token: supersecret, all good"))
```

Result:

```
Token: ***, all good
```

What's happening here? The `redact` method goes through the list of secrets and replaces every occurrence with `***`. The replacement is safe because the new value (`***`) contains no secret. An important nuance: `str.replace` also replaces substrings inside other words — if a secret is short, that yields false positives. In real code masking is done on word boundaries and combined with regexes. The key takeaway: before writing anything to logs or error reports, run the text through such a redactor — secrets must not leave the service boundaries in plain text.
### Solution 6
```bash
pip install pip-audit
pip-audit > audit.txt
type audit.txt
```
pip-audit compares package versions against vulnerability databases (OSV). This is part of regular dependency audit.
### Solution 7
```bash
gitleaks detect --source . --report-path leaks.json
```
If secrets are found — rotate them and clean the history. Running regularly (pre-commit) keeps secrets out of the repository.

<!--/SOLUTION-->

<!--QUIZ-->
Why must secrets not be committed even "temporarily"?
- They stay in Git history forever and can be extracted
- Git encrypts them automatically
- They take too much space
* Correct answer: They stay in Git history forever and can be extracted
Deleting a file from the working copy does not clean the commit history.

How to read a secret correctly in Python?
- os.environ.get(name) with a None check and an error
- Hard-code the value in code
- Store it in config.py module
* Correct answer: os.environ.get(name) with a None check and an error
The secret comes from the environment; if it's missing, the application fails with a clear error.

What does pip-audit do?
- Checks dependencies for known vulnerabilities against the OSV database
- Installs packages from requirements.txt
- Encrypts secrets in code
* Correct answer: Checks dependencies for known vulnerabilities against the OSV database
pip-audit finds CVEs in direct and transitive dependencies.

Which flag in subprocess.run makes the command considered successful only with a zero return code?
- check=True
- shell=True
- capture_output=True
* Correct answer: check=True
With a non-zero code check=True raises CalledProcessError.

What does dependency pinning mean?
- Fixing exact versions with ==
- Removing extra dependencies
- Installing packages from a local cache
* Correct answer: Fixing exact versions with ==
Pinning makes the build reproducible and protects against surprises.

Which tool finds secrets right in the repository?
- detect-secrets
- pip-audit
- safety
* Correct answer: detect-secrets
detect-secrets and gitleaks scan code and commit history for secrets.

What will os.environ.get("MISSING") return if the variable is absent?
- None
- ""
- KeyError
* Correct answer: None
.get does not throw an exception but returns None — convenient for an explicit check.

Why make dependency audit a blocking step in CI?
- So a release doesn't go to production with known vulnerabilities
- To speed up the build
- To replace tests
* Correct answer: So a release doesn't go to production with known vulnerabilities
The pipeline fails on findings — updating becomes mandatory.

What does str.replace do when masking secrets?
- Replaces all occurrences of a substring with a new string
- Removes the string from memory
- Encrypts the string
* Correct answer: Replaces all occurrences of a substring with a new string
replace replaces every occurrence, so the secret disappears from the output.

Where are secrets stored in a production environment?
- In environment variables and secret stores
- In the repository next to code
- In requirements.txt
* Correct answer: In environment variables and secret stores
Orchestrators (Kubernetes, Docker secrets, Vault) deliver secrets at runtime.
What does pip-audit do?
- Finds vulnerabilities in installed packages
- Updates pip
- Removes packages
- Lints
* Correct answer: Finds vulnerabilities in installed packages
It compares versions against vulnerability databases.

What is gitleaks?
- A secret scanner in git history
- A package manager
- A formatter
- A profiler
* Correct answer: A secret scanner in git history
It finds API keys and passwords in code.

Why is a committed secret dangerous?
- It can be read from history even after deletion
- It speeds up code
- It means nothing
- It changes types
* Correct answer: It can be read from history even after deletion
Deleting a file does not erase it from commit history.

What to do if a secret has leaked?
- Immediately revoke and replace it
- Leave it
- Hide it in a comment
- Rename the variable
* Correct answer: Immediately revoke and replace it
Rotating the secret denies the attacker access.

# 
<!--/QUIZ-->
