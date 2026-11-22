---
title: File Automation: Downloads Organizer
summary: Let's tidy up the Downloads folder: get to grips with pathlib and shutil and write a script that sorts files into folders by extension.
order: 1
duration: 25 min
difficulty: intermediate
tags: pathlib, shutil, files, automation
---

Your Downloads folder is probably a mess: PDFs here, pictures there, installers somewhere else. Sorting through them by hand is boring and slow. The good news: Python does it in a couple of seconds, and in this single lesson we'll write our own file organizer.

## Getting to Know pathlib

In modern Python, a file path is not just a string — it's a `Path` object from the `pathlib` module. It has plenty of handy methods. To get a path object for a folder, write:

```python
from pathlib import Path

downloads = Path.home() / "Downloads"
print(downloads)
```

The `/` operator joins path parts — it reads much better than `os.path.join()`. Here's what `Path` can do:

- `p.mkdir(parents=True, exist_ok=True)` — create a folder together with all parents, without raising an error if it already exists;
- `p.exists()` — check whether the path exists;
- `p.is_file()` and `p.is_dir()` — whether it's a file or a folder;
- `p.name` — the file name with extension;
- `p.suffix` — the extension, e.g. `".pdf"`;
- `p.stem` — the name without the extension.

For example, print all files in a folder with their extensions:

```python
for f in downloads.iterdir():
    if f.is_file():
        print(f.name, "→", f.suffix)
```

The `iterdir()` method lists everything in the folder, and we filter with `is_file()` so as not to touch subfolders.

## Moving Files: shutil

The standard library provides `shutil.move(source, destination)` for moving files:

```python
import shutil

source = downloads / "photo.jpg"
target_folder = downloads / "images"
target_folder.mkdir(parents=True, exist_ok=True)
shutil.move(str(source), str(target_folder))
```

`shutil.move` can move both files and folders. If the second argument is an existing folder, the file ends up inside it with its original name.

## The Idea Behind the Organizer

We want an "extension → category" dictionary:

```python
CATEGORIES = {
    ".jpg": "images", ".png": "images", ".gif": "images",
    ".pdf": "documents", ".docx": "documents", ".txt": "documents",
    ".mp3": "audio", ".mp4": "video",
}
```

Then, for each file: determine the extension, find the category, create the folder (if needed), and move the file. If the extension is unfamiliar — put it in `"others"`. This is your future mini-project; the tasks below walk you through it step by step.

A couple more nuances. First, don't move blindly: if a file with the same name already exists in the target folder, `shutil.move` will simply replace it. For an organizer that's dangerous — you could lose data — so in the tasks we'll add a check and a "smart" numbered name. Second, for your first try, create a test folder with copies of files rather than running the script on your real Downloads folder.

All the organizer's logic fits into a short chain:

```mermaid
flowchart LR
    A["Downloads folder"] --> B["iterdir and is_file"]
    B --> C["suffix → category"]
    C --> D["mkdir for category"]
    D --> E["safe_move without overwrite"]
    E --> F["Counter and report"]
```

<!--TASK-->
### Task 1
Create a `test_data` folder next to the script and put several files of different types in it: `photo.jpg`, `report.pdf`, `notes.txt`, `music.mp3`, and one file without an extension — `README`. Write a program that lists all files in this folder and prints a line of the form `name → extension` for each. Use only `pathlib`: `Path`, `iterdir()`, `is_file()`, `name`, `suffix`. Expected result — a list of lines, one per file: `photo.jpg → .jpg`, `README → (no extension)`.

### Task 2
Fill in the `CATEGORIES` dictionary from the theory and teach the program to move files into categories. For each file, determine the category by extension, create the needed subfolder inside `test_data` (via `mkdir(parents=True, exist_ok=True)`), and move the file there with `shutil.move`. Expected result: after running, `test_data` gains `images`, `documents`, `audio` subfolders, and the files move into them. At the end, the program prints `Done!`.

### Task 3
Teach the organizer to handle edge cases. First, subfolders (e.g., an existing `images`) must not be moved — skip them with an `is_file()` check. Second, files with unknown extensions and files without an extension must land in the `others` folder. Use `CATEGORIES.get(ext, "others")`. Expected result: subfolders stay in place, `README` ends up in `others`, and the program runs without errors when re-run.

### Task 4
Add overwrite protection. Before moving, check whether a file with the same name exists in the target folder. If it does — pick a new numbered name: `photo_1.jpg`, `photo_2.jpg`, and so on until the name is free. Expected result: on re-running the program nothing is lost or replaced, and duplicates get `_1`, `_2` suffixes.

### Task 5
Gather all the logic into a function `organize(folder)` that returns a "category → number of moved files" dictionary (a `Counter` from `collections` or a plain dict will do). At the end of the program, print a report: lines like `images: 4`, `documents: 2`, `others: 1` — for every category that received at least one file. Expected result: after running, the report appears on screen and `test_data` is fully tidy.

### Task 6
Find duplicates by content. Walk `test_data` recursively (`rglob("*")`), compute SHA-256 for each file via `hashlib` — read the file in 64 KB chunks, not all at once. Build a "hash → list of paths" dictionary and print only those groups with more than one file. Expected result: lines like `Duplicates (2): images/photo.jpg, images/photo_1.jpg` and a summary `Groups found: 1`. Don't move or delete files — this is only a report showing what takes up space.

### Task 7
Add a "dry run" mode and an operation log to the organizer. The function `organize(folder, dry_run=False)` with `dry_run=True` must not move anything — only print a plan like `photo.jpg → images/photo.jpg`. Regardless of the mode, every planned or executed operation is written to `log.csv` as a line `file;category;new_name`. Expected result: with `dry_run=True` nothing changes in the folder, while `log.csv` contains the plan lines; with `dry_run=False` files move and the log matches the actual outcome.
<!--/TASK-->

<!--HINT-->
### Hint 1
Iterating over contents: `for f in folder.iterdir()`. Check `f.is_file()` to filter out subfolders. The extension comes from `f.suffix`, but for a file without an extension it returns an empty string — in that case substitute the text `(no extension)`. For printing, an f-string is convenient: `f"{f.name} → {ext}"`.

### Hint 2
Take the category from the dictionary: `cat = CATEGORIES.get(f.suffix.lower())`. Create the target folder with `(folder / cat).mkdir(parents=True, exist_ok=True)`, then move: `shutil.move(str(f), str(folder / cat))`. Don't forget to filter out non-files, otherwise `shutil.move` will try to move a folder with all its contents.

### Hint 3
Folders are already filtered by the `f.is_file()` check — keep it first. For unknown extensions use `.get(ext, "others")`: the second argument becomes the default value, and a file without an extension (empty string) also goes into `others`.

### Hint 4
Before moving, check `(folder / cat / f.name).exists()`. If it's true — pick a name in a loop: while `dest.exists()`, increase the counter and build `f"{f.stem}_{n}{f.suffix}"`. When the name is free, move to exactly that name.

### Hint 5
Inside the function, set up a counter: `from collections import Counter; moved = Counter()`. After a successful move do `moved[cat] += 1`. At the end return `moved`, and in the main part print the report with a loop `for cat, count in sorted(report.items())`. Don't forget to call `organize("test_data")`.

### Hint 6
For a recursive walk use `folder.rglob("*")` — it enters all subfolders. Compute the hash with a function: `h = hashlib.sha256()`, then in a loop `for chunk in iter(lambda: f.read(65536), b""): h.update(chunk)`, result — `h.hexdigest()`. Accumulate paths in a `defaultdict(list)` keyed by hash and print only lists longer than one.

### Hint 7
Separate "deciding" from "acting": first collect a list of tuples `(file, category, new_name)`, then either print it or execute `shutil.move`. Writing the log is easiest with `csv.writer` using `delimiter=";"` and `newline=""` inside `open(...)`. Create the folder only in the real-move mode, otherwise a dry run leaves empty directories behind.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
from pathlib import Path

folder = Path("test_data")

for f in folder.iterdir():
    if f.is_file():
        ext = f.suffix or "(no extension)"
        print(f"{f.name} → {ext}")
```

Result:

```
photo.jpg → .jpg
report.pdf → .pdf
notes.txt → .txt
music.mp3 → .mp3
README → (no extension)
```

What's going on here? `iterdir()` returns an iterator over all the folder's items: files and subfolders. The `f.is_file()` check keeps only files. Then `f.suffix` gives the extension with the dot, and the expression `f.suffix or "(no extension)"` is a classic trick: an empty string (a file without an extension) is falsy, so the explanatory text is substituted. Finally, the f-string conveniently assembles the output. Note that the order of lines in the report is determined by the order of items in the folder — that's normal.

### Solution 2
Solution:

```python
import shutil
from pathlib import Path

CATEGORIES = {
    ".jpg": "images", ".png": "images", ".gif": "images",
    ".pdf": "documents", ".docx": "documents", ".txt": "documents",
    ".mp3": "audio", ".mp4": "video",
}

folder = Path("test_data")

for f in folder.iterdir():
    if not f.is_file():
        continue
    cat = CATEGORIES.get(f.suffix.lower(), "others")
    target = folder / cat
    target.mkdir(parents=True, exist_ok=True)
    shutil.move(str(f), str(target))

print("Done!")
```

What's going on here? `continue` skips subfolders without touching them. `CATEGORIES.get(f.suffix.lower(), "others")` looks up the category by extension; lowering the case protects against files like `PHOTO.JPG`. `target.mkdir(parents=True, exist_ok=True)` creates the folder once and doesn't crash on repeated runs. `shutil.move(str(f), str(target))` moves the file into the category folder. Note: `shutil.move` accepts strings or `Path` objects, so `str()` is optional but makes the behavior explicit.

### Solution 3
Solution:

```python
import shutil
from pathlib import Path

CATEGORIES = {
    ".jpg": "images", ".png": "images", ".gif": "images",
    ".pdf": "documents", ".docx": "documents", ".txt": "documents",
    ".mp3": "audio", ".mp4": "video",
}

folder = Path("test_data")

for f in folder.iterdir():
    if not f.is_file():
        continue
    cat = CATEGORIES.get(f.suffix.lower(), "others")
    target = folder / cat
    target.mkdir(parents=True, exist_ok=True)
    shutil.move(str(f), str(target))

print("Done!")
```

This is almost the same code as in task 2, but now it correctly handles edge cases. Folders are skipped upfront, so `shutil.move` never receives a folder as a source. `CATEGORIES.get(ext, "others")` returns `"others"` when the extension is not in the dictionary, including for an empty extension (the `README` file). The result: `images`, `documents`, and other categories remain folders, while unrecognized files accumulate in `others`. Check that re-running the program produces no errors — that's exactly what `exist_ok=True` is for.

### Solution 4
Solution:

```python
import shutil
from pathlib import Path

def safe_move(f: Path, target: Path) -> None:
    dest = target / f.name
    if not dest.exists():
        shutil.move(str(f), str(dest))
        return
    n = 1
    while True:
        dest = target / f"{f.stem}_{n}{f.suffix}"
        if not dest.exists():
            shutil.move(str(f), str(dest))
            return
        n += 1
```

What's going on here? First we check the simplest case: if no file with that name exists in the target folder, we move as usual. If it exists — we start a loop: try `photo_1.jpg`, then `photo_2.jpg`, and so on until a free name is found. `f.stem` gives the name without the extension, `f.suffix` gives the extension, so joining them with `f"{f.stem}_{n}{f.suffix}"` is always correct even for files with several dots, e.g. `archive.backup.zip`. This approach rules out data loss on repeated runs: files aren't replaced, they get unique names.

### Solution 5
Solution:

```python
import shutil
from collections import Counter
from pathlib import Path

CATEGORIES = {
    ".jpg": "images", ".png": "images", ".gif": "images",
    ".pdf": "documents", ".docx": "documents", ".txt": "documents",
    ".mp3": "audio", ".mp4": "video",
}

def safe_move(f: Path, target: Path) -> None:
    dest = target / f.name
    if not dest.exists():
        shutil.move(str(f), str(dest))
        return
    n = 1
    while True:
        dest = target / f"{f.stem}_{n}{f.suffix}"
        if not dest.exists():
            shutil.move(str(f), str(dest))
            return
        n += 1

def organize(folder: str) -> Counter:
    folder = Path(folder)
    moved = Counter()
    for f in folder.iterdir():
        if not f.is_file():
            continue
        cat = CATEGORIES.get(f.suffix.lower(), "others")
        target = folder / cat
        target.mkdir(parents=True, exist_ok=True)
        safe_move(f, target)
        moved[cat] += 1
    return moved

report = organize("test_data")
for cat, count in sorted(report.items()):
    print(f"{cat}: {count}")
```

Result (example):

```
audio: 1
documents: 2
images: 1
others: 1
```

What's going on here? The `organize` function accepts a path as a string, turns it into a `Path`, creates a `Counter`, runs the move loop, and returns the statistics. At the end of the program, `sorted(report.items())` sorts categories alphabetically, and the report prints neatly. Such a function is easy to reuse: call `organize(str(Path.home() / "Downloads"))` — and your real Downloads folder gets tidied up. Congratulations, this is your first full-fledged automation tool!

### Solution 6
Solution:

```python
import hashlib
from collections import defaultdict
from pathlib import Path

def file_hash(path: Path, chunk: int = 65536) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()

folder = Path("test_data")
by_hash = defaultdict(list)
for f in folder.rglob("*"):
    if f.is_file():
        by_hash[file_hash(f)].append(f)

groups = {h: paths for h, paths in by_hash.items() if len(paths) > 1}
for h, paths in groups.items():
    names = ", ".join(str(p) for p in paths)
    print(f"Duplicates ({len(paths)}): {names}")
print("Groups found:", len(groups))
```

Result (example):

```
Duplicates (2): test_data/images/photo.jpg, test_data/images/photo_1.jpg
Groups found: 1
```

What's going on here? `rglob("*")` walks the folder recursively, so duplicates are found in category subfolders too. The `file_hash` function reads the file in blocks: `iter(lambda: f.read(chunk), b"")` keeps calling read until it returns an empty `b""` — that's the iterator's stop signal. This approach doesn't load a whole movie or ISO image into memory, which is nice on a regular computer and essential on a weak one. `hexdigest()` produces a 64-character string, and identical content always yields the same string, so there's no need to compare files pairwise. `defaultdict(list)` removes the "does this key already exist" check. Finally, the `len(paths) > 1` filter keeps only real duplicate groups.

### Solution 7
Solution:

```python
import csv
import shutil
from pathlib import Path

CATEGORIES = {
    ".jpg": "images", ".png": "images", ".gif": "images",
    ".pdf": "documents", ".docx": "documents", ".txt": "documents",
    ".mp3": "audio", ".mp4": "video",
}

def unique_name(target: Path, name: str) -> Path:
    dest = target / name
    if not dest.exists():
        return dest
    stem, suffix = Path(name).stem, Path(name).suffix
    n = 1
    while (target / f"{stem}_{n}{suffix}").exists():
        n += 1
    return target / f"{stem}_{n}{suffix}"

def organize(folder, dry_run=False):
    folder = Path(folder)
    plan = []
    for f in folder.iterdir():
        if not f.is_file():
            continue
        cat = CATEGORIES.get(f.suffix.lower(), "others")
        dest = unique_name(folder / cat, f.name)
        plan.append((f, cat, dest))

    for f, cat, dest in plan:
        if dry_run:
            print(f"{f.name} → {cat}/{dest.name}")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(f), str(dest))

    with open("log.csv", "w", newline="", encoding="utf-8") as fp:
        writer = csv.writer(fp, delimiter=";")
        writer.writerow(["file", "category", "new_name"])
        for f, cat, dest in plan:
            writer.writerow([f.name, cat, dest.name])

    return plan

plan = organize("test_data", dry_run=True)
print("Operations in plan:", len(plan))
```

Result (example):

```
photo.jpg → images/photo.jpg
report.pdf → documents/report.pdf
README → others/README
Operations in plan: 3
```

What's going on here? The main idea is to split the work into two passes. The first pass only reads the folder and builds the plan: a list of "from, category, to" tuples. The second pass either prints the plan or performs the moves. Thanks to this, `dry_run` isn't a separate logic branch — it's simply the absence of actions, and the risk that a "trial" mode breaks something disappears. The `unique_name` function picks a free name in advance, so the log contains exactly the name that will appear on disk, not the original one. `mkdir` is only called in the real-move mode: a dry run must not leave empty folders behind. The log is written once at the end, in UTF-8 and with `newline=""` — otherwise `csv` adds extra blank lines on Windows. The `log.csv` file opens in Excel with a semicolon delimiter and serves as proof of exactly what the program did.
<!--/SOLUTION-->

<!--QUIZ-->
Which class from the standard library is used to work with file paths?
- os.path.Path
- pathlib.Path
- Path.os
- sys.Path
* Correct answer: pathlib.Path
pathlib is the modern standard module where a path is a Path object with convenient methods.

What does p.suffix return for the file "photo.png"?
- "photo"
- ".png"
- "png"
- "photo.png"
* Correct answer: .png
suffix returns the extension together with the dot.

What does p.mkdir(parents=True, exist_ok=True) do?
- Creates a file
- Creates a folder together with all parents and doesn't fail if it already exists
- Deletes a folder
- Moves a folder
* Correct answer: Creates a folder together with all parents and doesn't fail if it already exists
parents creates any missing parent folders, and exist_ok=True avoids an error when it exists.

Which function moves a file to another folder?
- shutil.copy
- shutil.move
- shutil.delete
- shutil.transfer
* Correct answer: shutil.move
shutil.move moves a file or folder to a new location, keeping its name.

How is is_file() different from is_dir()?
- It isn't
- is_file() checks that the object is a file, and is_dir() that it's a folder
- is_file() creates a file
- is_dir() deletes a folder
* Correct answer: is_file() checks that the object is a file, and is_dir() that it's a folder
These are two sides of one check: an item is either a file or a folder.

What does iterdir() do?
- Returns an iterator over the folder's contents
- Deletes the folder's contents
- Creates a folder
- Returns the path of the parent folder
* Correct answer: Returns an iterator over the folder's contents
iterdir() lets you walk through every item inside the folder.

What does Path("photo.jpg").stem return?
- "photo"
- ".jpg"
- "photo.jpg"
- "photo_jpg"
* Correct answer: "photo"
stem is the file name without the extension, while suffix is the extension together with the dot.

Why check whether a name already exists in the target folder before moving a file?
- To avoid data loss: shutil.move silently replaces an existing file
- To speed up the program
- To avoid creating extra folders
- It's a requirement of the mkdir method
* Correct answer: To avoid data loss: shutil.move silently replaces an existing file
The protection is the dest.exists() check plus picking a new numbered name: photo_1.jpg, photo_2.jpg.

What does `Path("archive.tar.gz").suffix` return?
- ".tar.gz"
- ".gz"
- "archive"
- "tar.gz"
* Correct answer: .gz
suffix is only the last dot: for archive.tar.gz it's ".gz", while the full set of extensions is given by the suffixes property.

What does the `/` operator do for a Path object?
- Divides a number by a number
- Joins path parts
- Splits a string into parts
- Returns the parent folder
* Correct answer: Joins path parts
Path("a") / "b" gives Path("a/b") — noticeably easier to read than os.path.join().

Why does `f.suffix or "(no extension)"` substitute text for a file without an extension?
- Because suffix returns None
- Because an empty string is falsy and `or` takes the second operand
- Because or replaces empty files
- Because suffix raises an exception
* Correct answer: Because an empty string is falsy and `or` takes the second operand
For a file without an extension, suffix is "", and an empty string is falsy in a condition — so the right side of the expression is returned.

Why compare file hashes when looking for duplicates instead of the files themselves?
- A hash is shorter than a file name
- Identical content produces an identical hash, so there's no need to read and compare files pairwise
- A hash shows the file size
- This way files move faster
* Correct answer: Identical content produces an identical hash, so there's no need to read and compare files pairwise
Comparing 64-character strings replaces pairwise byte-by-byte comparison of all files.
<!--/QUIZ-->
