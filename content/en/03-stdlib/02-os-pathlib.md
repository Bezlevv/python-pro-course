---
title: os, pathlib, shutil
summary: Working with files and directories, paths, copying and moving.
order: 2
duration: 35 min
difficulty: intermediate
tags: os, pathlib, shutil
---

File system tasks are daily work: lists, paths, copy, move, delete.

## pathlib (recommended)

```python
from pathlib import Path

p = Path("data")
p.mkdir(exist_ok=True)
p.exists()   # True
list(p.iterdir())
```

## os

```python
import os
os.getcwd()
os.listdir(".")
os.makedirs("a/b", exist_ok=True)
```

## shutil

```python
import shutil
shutil.copy("a.txt", "b.txt")
shutil.move("b.txt", "tmp/b.txt")
shutil.rmtree("tmp")
```

## glob

```python
from pathlib import Path
list(Path(".").glob("*.py"))
list(Path(".").rglob("*.txt"))
```

## Lesson summary

pathlib is the modern API; os covers legacy; shutil handles file operations.

<!--TASK-->
### Task 1 — Create dir
Create "projects" with Path.mkdir(exist_ok=True); verify exists().

### Task 2 — List files
List all files in current directory with iterdir and print names.

### Task 3 — glob
Find all .md files with glob and rglob.

### Task 4 — Copy
Create a file, copy it with shutil.copy; verify both exist.

### Task 5 — Move
Move a file into a folder; verify the folder contains it.

### Task 6 — Remove
Delete a temporary directory with shutil.rmtree.

### Task 7 — Current dir
Print os.getcwd() and the parent of the current path.
<!--/TASK-->

<!--HINT-->
### Hint 1
Path("projects").mkdir(exist_ok=True).

### Hint 2
for p in Path(".").iterdir(): print(p).

### Hint 3
Path(".").glob("*.md"); rglob.

### Hint 4
shutil.copy("a", "b").

### Hint 5
shutil.move("a", "folder/a").

### Hint 6
shutil.rmtree("temp").

### Hint 7
Path.cwd() and .parent.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from pathlib import Path
Path("projects").mkdir(exist_ok=True)
print(Path("projects").exists())   # True
```

### Solution 2
```python
for p in Path(".").iterdir():
    print(p.name)
```

### Solution 3
```python
print(list(Path(".").glob("*.md")))
print(list(Path(".").rglob("*.txt")))
```

### Solution 4
```python
import shutil
Path("a.txt").write_text("Hello", encoding="utf-8")
shutil.copy("a.txt", "b.txt")
print(Path("b.txt").exists())   # True
```

### Solution 5
```python
Path("tmp").mkdir(exist_ok=True)
shutil.move("b.txt", "tmp/b.txt")
print((Path("tmp") / "b.txt").exists())
```

### Solution 6
```python
shutil.rmtree("tmp")
print(Path("tmp").exists())   # False
```

### Solution 7
```python
import os
print(os.getcwd())
print(Path.cwd().parent)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is pathlib?
- Modern path API
- Legacy os
- File copy
- Zip
* Correct answer: Modern path API
Path objects.

What does mkdir(exist_ok=True) do?
- Creates without error if exists
- Always fails
- Copies
- Removes
* Correct answer: Creates without error if exists
Safe creation.

What does iterdir do?
- Lists directory content
- Reads files
- Copies
- Deletes
* Correct answer: Lists directory content
Iterator.

What does glob do?
- Matches names by pattern
- Lists all
- Reads
- Deletes
* Correct answer: Matches names by pattern
*.py.

What does rglob do?
- Recursive glob
- Only current dir
- Reverse
- Copy
* Correct answer: Recursive glob
All subdirs.

What does shutil.copy do?
- Copies a file
- Moves
- Deletes
- Reads
* Correct answer: Copies a file
Creates a copy.

What does shutil.move do?
- Moves a file/dir
- Copies
- Deletes
- Renames only
* Correct answer: Moves a file/dir
Relocates.

What does shutil.rmtree do?
- Removes a directory tree
- Removes one file
- Copies
- Moves
* Correct answer: Removes a directory tree
Recursive deletion.

What is Path.cwd()?
- Current working directory
- Home
- Temp
- Root
* Correct answer: Current working directory
As a Path.

How to join paths?
- Path("a") / "b"
- "a" + "b"
- os.join("a", "b")
- Path("a+b")
* Correct answer: Path("a") / "b"
Safe join.

What is Path(".")?
- Current directory
- Parent
- Home
- File
* Correct answer: Current directory
As object.

Which is the recommended modern way?
- pathlib
- os.path
- glob module only
- shutil only
* Correct answer: pathlib
Cleaner API.
<!--/QUIZ-->
