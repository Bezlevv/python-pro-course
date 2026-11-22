---
title: Sentry: error tracking
summary: Capture exceptions, breadcrumbs.
order: 3
duration: 45 min
difficulty: intermediate
tags: sentry
---

Sentry reports production errors.

## Setup

```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://...@o0.ingest.sentry.io/0",
    traces_sample_rate=1.0,
)
```

## Capture

```python
try:
    1 / 0
except ZeroDivisionError as e:
    sentry_sdk.capture_exception(e)
```

## Breadcrumbs

```python
sentry_sdk.add_breadcrumb(message="user logged in")
```

## Lesson summary

Errors auto-collected with context.

<!--TASK-->
### Task 1 — Init
Initialize Sentry.

### Task 2 — Capture
Capture an exception.

### Task 3 — Message
Capture a message.

### Task 4 — Breadcrumb
Add a breadcrumb.

### Task 5 — User
Set user context.

### Task 6 — Release
Set release.

### Task 7 — Ignore
Ignore a known error.
<!--/TASK-->

<!--HINT-->
### Hint 1
init.

### Hint 2
capture_exception.

### Hint 3
capture_message.

### Hint 4
add_breadcrumb.

### Hint 5
set_user.

### Hint 6
release.

### Hint 7
ignore_errors.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://...@o0.ingest.sentry.io/0",
    traces_sample_rate=1.0,
)
```

### Solution 2
```python
try:
    1 / 0
except ZeroDivisionError as e:
    sentry_sdk.capture_exception(e)
```

### Solution 3
```python
sentry_sdk.capture_message("something odd happened")
```

### Solution 4
```python
sentry_sdk.add_breadcrumb(message="user logged in")
```

### Solution 5
```python
sentry_sdk.set_user({"id": "42", "email": "a@b.c"})
```

### Solution 6
```python
sentry_sdk.set_tag("release", "1.2.3")
```

### Solution 7
```python
sentry_sdk.init(
    dsn="...",
    ignore_errors=[KeyboardInterrupt],
)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is Sentry?
- Error tracking
- Metrics
- Logs
- None
* Correct answer: Error tracking
Service.

What is DSN?
- Connection string
- Error
- User
- None
* Correct answer: Connection string
Key.

What is capture_exception?
- Sends error
- Logs locally
- Fixes
- None
* Correct answer: Sends error
Exception.

What is capture_message?
- Sends message
- Error
- User
- None
* Correct answer: Sends message
Manual.

What is a breadcrumb?
- Context trail
- Error
- Release
- None
* Correct answer: Context trail
Steps.

What is set_user?
- Attaches user
- Removes
- Logs
- None
* Correct answer: Attaches user
Context.

What is set_tag?
- Adds metadata
- User
- Error
- None
* Correct answer: Adds metadata
Release.

What is a release?
- Version tag
- Error
- Log
- None
* Correct answer: Version tag
Deploy.

What is ignore_errors?
- Skips list
- Sends
- Fixes
- None
* Correct answer: Skips list
Known.

What is traces_sample_rate?
- Sampling
- Errors
- Users
- None
* Correct answer: Sampling
1.0.

What is an event?
- Reported incident
- Metric
- Panel
- None
* Correct answer: Reported incident
Error.

What is the benefit?
- Automatic reports
- Manual logs
- Required
- None
* Correct answer: Automatic reports
Context.
<!--/QUIZ-->
