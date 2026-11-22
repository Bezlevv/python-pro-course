---
title: Hosting, .env and secrets
summary: Deployment platforms, environment variables, secret management.
order: 4
duration: 40 min
difficulty: intermediate
tags: hosting, env, secrets
---

Deploy to a real host; keep config out of code.

## Environment variables

```python
import os

SECRET = os.environ.get("SECRET_KEY", "dev")
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
```

## .env

```bash
SECRET_KEY=change-me
DEBUG=false
```

## Hosting options

- Render, Fly.io, Railway — easy PaaS;
- VPS + Docker + Nginx — full control.

## Secrets

Never commit .env; use the platform's secret store.

## Lesson summary

env vars separate config from code; PaaS simplifies deployment.

<!--TASK-->
### Task 1 — Read env
Read SECRET_KEY via os.environ.

### Task 2 — Default
Provide a fallback default.

### Task 3 — .env
Create a .env file and list vars.

### Task 4 — Ignore
Gitignore .env.

### Task 5 — Host choice
Compare PaaS vs VPS in comments.

### Task 6 — Set env
Show the command to set an env var.

### Task 7 — Platform secrets
Describe storing secrets on Render/Fly.
<!--/TASK-->

<!--HINT-->
### Hint 1
os.environ.get.

### Hint 2
default.

### Hint 3
.env.

### Hint 4
.gitignore.

### Hint 5
PaaS vs VPS.

### Hint 6
export or set.

### Hint 7
Dashboard.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import os
secret = os.environ.get("SECRET_KEY")
```

### Solution 2
```python
secret = os.environ.get("SECRET_KEY", "dev-default")
```

### Solution 3
```bash
SECRET_KEY=change-me
DEBUG=false
ALLOWED_HOSTS=example.com
```

### Solution 4
```
# .gitignore
.env
```

### Solution 5
```python
# PaaS: быстро, меньше контроля
# VPS: полный контроль, больше работы
```

### Solution 6
```bash
# Linux/macOS
export SECRET_KEY=value
# Windows PowerShell
$env:SECRET_KEY="value"
```

### Solution 7
```python
# Render: Dashboard → Environment
# Fly.io: fly secrets set NAME=value
```
<!--/SOLUTION-->

<!--QUIZ-->
What are env vars?
- Config outside code
- Files
- Secrets only
- None
* Correct answer: Config outside code
Environment.

What does os.environ.get do?
- Reads a variable
- Sets
- Deletes
- None
* Correct answer: Reads a variable
With default.

What is .env?
- Local env file
- A secret store
- A config path
- None
* Correct answer: Local env file
Not committed.

Why default?
- Safe fallback
- Required
- Faster
- None
* Correct answer: Safe fallback
Dev.

What is PaaS?
- Platform as a Service
- A VPS
- Docker only
- None
* Correct answer: Platform as a Service
Render.

What is a VPS?
- Virtual private server
- PaaS
- A DB
- None
* Correct answer: Virtual private server
Full control.

What is the danger of committing .env?
- Leaks
- Speed
- Size
- None
* Correct answer: Leaks
Secrets.

Where to keep real secrets?
- Platform secret store
- Code
- README
- Logs
* Correct answer: Platform secret store
Safe.

What is DEBUG=false in prod?
- Safer
- Faster
- Required
- None
* Correct answer: Safer
No debug info.

What is ALLOWED_HOSTS?
- Accepted hosts
- Blocked
- DNS
- None
* Correct answer: Accepted hosts
Django.

How to set locally for a session?
- export / $env:
- Change file
- pip
- None
* Correct answer: export / $env:
Per session.

What does .gitignore protect?
- .env
- Code
- Tests
- None
* Correct answer: .env
Not committed.
<!--/QUIZ-->
