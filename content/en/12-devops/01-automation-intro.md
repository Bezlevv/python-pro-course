---
title: Automation of routine tasks
summary: Scripting, file operations, subprocess, scheduling.
order: 1
duration: 40 min
difficulty: intermediate
tags: automation, scripts, subprocess
---

Python automates routine work.

## Files

```python
from pathlib import Path
p = Path("data.txt")
p.write_text("hello", encoding="utf-8")
print(p.read_text(encoding="utf-8"))
```

## subprocess

```python
import subprocess
result = subprocess.run(["python", "--version"], capture_output=True, text=True)
print(result.stdout)
```

## Loop over files

```python
for f in Path(".").glob("*.log"):
    print(f.name, f.stat().st_size)
```

## Lesson summary

Scripts + pathlib + subprocess automate daily tasks.

<!--TASK-->
### Task 1 — Write/read
Create a file and read it back.

### Task 2 — Glob
List all .py files.

### Task 3 — Rename
Rename files in a folder.

### Task 4 — subprocess
Run a command and capture output.

### Task 5 — Check returncode
Handle failure.

### Task 6 — Batch
Process all .txt files (uppercase).

### Task 7 — Backup idea
Copy files to a backup folder.
<!--/TASK-->

<!--HINT-->
### Hint 1
pathlib.

### Hint 2
glob.

### Hint 3
Path.rename.

### Hint 4
subprocess.run.

### Hint 5
returncode.

### Hint 6
Loop + read/write.

### Hint 7
shutil.copy.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from pathlib import Path
p = Path("data.txt")
p.write_text("hello", encoding="utf-8")
print(p.read_text(encoding="utf-8"))
```

### Solution 2
```python
for f in Path(".").glob("*.py"):
    print(f.name)
```

### Solution 3
```python
for f in Path(".").glob("*.tmp"):
    f.rename(f.with_suffix(".bak"))
```

### Solution 4
```python
import subprocess
result = subprocess.run(["python", "--version"], capture_output=True, text=True)
print(result.stdout)
```

### Solution 5
```python
result = subprocess.run(["false"], capture_output=True, text=True)
if result.returncode != 0:
    print("failed", result.stderr)
```

### Solution 6
```python
for f in Path(".").glob("*.txt"):
    text = f.read_text(encoding="utf-8").upper()
    f.write_text(text, encoding="utf-8")
```

### Solution 7
```python
import shutil
Path("backup").mkdir(exist_ok=True)
for f in Path(".").glob("*.txt"):
    shutil.copy(f, "backup" / f.name)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is pathlib?
- Path API
- subprocess
- shutil
- None
* Correct answer: Path API
Modern.

What is Path(".").glob?
- Lists matches
- Reads
- Deletes
- None
* Correct answer: Lists matches
Pattern.

What is subprocess.run?
- Runs a command
- Opens file
- Imports
- None
* Correct answer: Runs a command
Process.

What is capture_output?
- Captures stdout/err
- Hides
- Prints
- None
* Correct answer: Captures stdout/err
Text.

What is returncode?
- Exit code
- Output
- PID
- None
* Correct answer: Exit code
0 = ok.

What is stderr?
- Error output
- Standard output
- Input
- None
* Correct answer: Error output
Messages.

What is stdout?
- Standard output
- Errors
- Input
- None
* Correct answer: Standard output
Result.

What is rename?
- Changes name
- Copies
- Deletes
- None
* Correct answer: Changes name
with_suffix.

What is shutil.copy?
- Copies file
- Moves
- Deletes
- None
* Correct answer: Copies file
Duplicate.

What is a cron-like loop?
- Scheduled script
- A thread
- A file
- None
* Correct answer: Scheduled script
Automation.

What is automation value?
- Saves time
- Complexity
- Bugs
- None
* Correct answer: Saves time
Productivity.

What is mkdir(exist_ok=True)?
- Safe create
- Error
- Deletes
- None
* Correct answer: Safe create
If missing.
<!--/QUIZ-->
