---
title: Automation: bots and scripts
summary: How Python removes routine: file work, renaming, schedules, terminal bots, automation safety rules.
order: 2
duration: 30 min
difficulty: beginner
tags: automation, scripts, bots, files, pathlib
---

## Routine can be delegated

Remember how many times you did the same thing by hand: renaming a hundred files, sorting photos into folders, filling in spreadsheets, answering identical messages. That is routine — the most boring part of any job. And here is the main news of this lesson: **Python is great at doing it for you**.

Automation is turning repetitive actions into a program that will do them itself, fast and without mistakes. Developers call such programs scripts. They are "little robots": you launch them, and they do their job.

## Script: a robot-program

A script is a regular `.py` file, but focused on one concrete task: process files, gather data, send emails, watch the system. They are surprisingly quick to write.

Let's start with file work. Python has an excellent tool — the `pathlib` module, which makes working with folders and files as simple as in a file manager:

```python
from pathlib import Path

# Create a folder and a file inside it
folder = Path("my_project")
folder.mkdir(exist_ok=True)

# Write text to a file
(folder / "hello.txt").write_text("Hello from a script!", encoding="utf-8")

# Read it back
text = (folder / "hello.txt").read_text(encoding="utf-8")
print(text)
```

Notice: `Path("my_project")` is a "path" to the folder. `mkdir(exist_ok=True)` creates the folder if it does not exist. The `/` operator joins a path with a file name. `write_text()` and `read_text()` write and read text. Just five lines — and you already have a file utility.

## Demo: bulk renaming

Imagine you have a folder of files whose names need a date added. Doing that by hand is tedious; a script handles it in a second:

```python
from pathlib import Path
from datetime import datetime

folder = Path("photos")
folder.mkdir(exist_ok=True)

# Create a couple of example files
for i in range(1, 4):
    (folder / f"image{i}.jpg").write_text("data", encoding="utf-8")

date = datetime.now().strftime("%Y-%m-%d")
for file in folder.iterdir():
    new_name = folder / f"{date}_{file.name}"
    file.rename(new_name)
    print("Renamed:", file.name, "->", new_name.name)
```

Here we met the `for ... in ...` loop, which iterates over items, and f-strings — strings where you can insert values inside curly braces: `f"image{i}.jpg"`. `iterdir()` lists all files in the folder, and `rename()` renames them. Run it — you'll see three files get a new prefix.

## Bots: a program that talks

A bot is a program that waits for messages and reacts to them. The simplest bot lives right in the terminal: it asks, listens, and answers. Any bot is based on a "listen → answer" loop:

```python
print("Hi! I'm an echo bot. Write something.")
while True:
    message = input("You: ")
    if message.lower() == "bye":
        print("Bot: Bye-bye! Come back soon.")
        break
    print("Bot: You wrote:", message)
```

`input()` waits until the user types something, and `while True` is an infinite loop — the bot will listen until it hears "bye" (`break` exits the loop). Real Telegram and messenger bots work exactly this way, only they listen to network messages instead of the terminal.

## Schedules and timers

Sometimes a script should run on a schedule — for example, once an hour. The simplest way is to make the program wait:

```python
import time

for i in range(3):
    print("Tick", i + 1)
    time.sleep(2)  # pause 2 seconds
```

`time.sleep(2)` pauses the program for 2 seconds. For real schedules there are libraries like `schedule`, and for running scripts on time — operating system tools (Task Scheduler on Windows or cron on Linux).

## Automation safety rules

Automation is power, but it must be handled carefully:

- **Never delete files blindly.** A program that deletes things should first show the list of what it will delete and ask for confirmation.
- **Check first, then change.** Rename files only after you are sure the name list is correct.
- **Work on a copy.** For experiments, create separate folders so you don't accidentally ruin real data.

## Lesson summary

Today we learned:

- what automation and scripts are;
- how to create folders and files with `pathlib`;
- how to rename files in a loop;
- how bots work: the "listen → answer" loop;
- how to add pauses and schedules;
- how to automate correctly and safely.

Now — practice. Build your first "robot".

<!--TASK-->
### Task 1
Write a script `file_maker.py` that creates a folder `demo_auto` and a file `hello.txt` inside it with the text `Hello from my first script!`, then reads the file and prints its contents. Run the script twice and make sure the second run does not raise an error (hint: the `exist_ok=True` parameter in `mkdir`). The phrase from the file should appear in the console.

### Task 2
Write a script `count_files.py` that counts and prints: how many files in total are in the current folder and how many of them have the `.py` extension. Use `Path(".").iterdir()` to list files and the `.suffix` method to detect the extension (e.g., `file.suffix == ".py"`). Print two numbers with labels: `Total files: N` and `.py files: M`.

### Task 3
Write a script `backup_renamer.py` that renames all files with the `.txt` extension in the folder `demo_auto`, adding the prefix `backup_` (e.g., `hello.txt` becomes `backup_hello.txt`). First create two `.txt` files in the folder, then rename them and print the new names. At the end print the full list of folder files to confirm the renaming worked.

### Task 4
Write a script `organizer.py` that creates folders `txt_files` and `md_files`, then creates three files in `demo_auto`: two with `.txt` and one with `.md`, and sorts them into the matching folders (`.txt` → `txt_files`, `.md` → `md_files`). Use `Path.rename()` or `shutil.move()`. At the end print the file lists of both folders.

### Task 5
Write a terminal bot `echo_bot.py` based on the lesson example. The bot should: greet, ask for the name, greet by name, then act as an echo (repeat messages) until it hears `bye`. For example: the bot asks `What is your name?`, the user types `Anna`, the bot answers `Nice to meet you, Anna!`, then repeats every message. Test the bot by entering several messages and `bye`.
<!--/TASK-->

<!--HINT-->
### Hint 1
Use `Path("demo_auto").mkdir(exist_ok=True)` — with this parameter a second run will not raise an error. For writing text use `write_text("...", encoding="utf-8")`, for reading — `read_text(encoding="utf-8")`. Print the read text with `print()`.

### Hint 2
Loop over `Path(".").iterdir()`: `for file in Path(".").iterdir():`. Note: `iterdir()` lists folders too, so check `file.is_file()`. The file extension is available in `file.suffix` — for `.py` it equals `".py"`. Use counters and add one in the right places.

### Hint 3
First create files with `write_text()`. Then in a second loop go over `iterdir()`, check `file.suffix == ".txt"` and run `file.rename(Path(str(file).replace(file.name, "backup_" + file.name)))`. Simpler: use `file.parent / f"backup_{file.name}"` as the new path. At the end print `[p.name for p in Path("demo_auto").iterdir()]` to see all files.

### Hint 4
Create folders `txt_files` and `md_files` with `mkdir(exist_ok=True)`. Create files in `demo_auto`. Then for each file check the extension and call `file.rename(Path("txt_files") / file.name)` for `.txt` and similarly for `.md`. The new names are just `file.name` (the file name), but in the new folder.

### Hint 5
Use `input()` for the name at the start: `name = input("What is your name? ")`, then `print("Nice to meet you,", name, "!")`. After that start a `while True` loop: inside it read `input("You: ")`, compare `message.lower() == "bye"` and `break` in that case, otherwise print `"Bot: You wrote:", message`. Don't forget `break` — without it the bot will run forever.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
from pathlib import Path

folder = Path("demo_auto")
folder.mkdir(exist_ok=True)

file = folder / "hello.txt"
file.write_text("Hello from my first script!", encoding="utf-8")

print(file.read_text(encoding="utf-8"))
```

Result:

```
Hello from my first script!
```

What happens here? `Path("demo_auto")` is the path to the folder. `mkdir(exist_ok=True)` creates it if it does not exist, so a second run does not crash. `folder / "hello.txt"` is the path to the file inside the folder. `write_text()` writes text, `read_text()` reads it. This is a minimal "robot" that creates and reads a file — the foundation of any automation.

### Solution 2
Solution:

```python
from pathlib import Path

total = 0
py_files = 0

for file in Path(".").iterdir():
    if file.is_file():
        total += 1
        if file.suffix == ".py":
            py_files += 1

print("Total files:", total)
print(".py files:", py_files)
```

Result depends on the folder contents, e.g.:

```
Total files: 5
.py files: 2
```

What happens here? `Path(".")` is the path to the current folder (the dot means "here"). `iterdir()` lists everything in it: both files and folders. We check `file.is_file()` to count only files, and `file.suffix` gives the extension, e.g. `.py`. The counters `total` and `py_files` increase by one when the condition holds. This is a mini-analyst that knows the folder's composition — the kind of script used to audit projects: how many files, of what type, how much junk.

### Solution 3
Solution:

```python
from pathlib import Path

folder = Path("demo_auto")
folder.mkdir(exist_ok=True)

(folder / "hello.txt").write_text("Hello", encoding="utf-8")
(folder / "notes.txt").write_text("Notes", encoding="utf-8")

for file in folder.iterdir():
    if file.suffix == ".txt":
        new_path = folder / f"backup_{file.name}"
        file.rename(new_path)
        print("Renamed:", file.name, "->", new_path.name)

print("Files in folder:", [p.name for p in folder.iterdir()])
```

Result:

```
Renamed: hello.txt -> backup_hello.txt
Renamed: notes.txt -> backup_notes.txt
Files in folder: ['backup_hello.txt', 'backup_notes.txt']
```

What happens here? First two text files are created. Then the loop goes over all folder items, and for each `.txt` we build a new path: `folder / f"backup_{file.name}"` — an f-string that inserts the file name into the string. `file.rename(new_path)` renames the file. The final list `[p.name for p in folder.iterdir()]` is a list comprehension, a short way to collect all file names. This is how photo and document "renamers" are written.

### Solution 4
Solution:

```python
from pathlib import Path

base = Path("demo_auto")
base.mkdir(exist_ok=True)

(base / "a.txt").write_text("text", encoding="utf-8")
(base / "b.txt").write_text("text", encoding="utf-8")
(base / "readme.md").write_text("# Heading", encoding="utf-8")

Path("txt_files").mkdir(exist_ok=True)
Path("md_files").mkdir(exist_ok=True)

for file in base.iterdir():
    if file.suffix == ".txt":
        file.rename(Path("txt_files") / file.name)
    elif file.suffix == ".md":
        file.rename(Path("md_files") / file.name)

print("txt_files:", [p.name for p in Path("txt_files").iterdir()])
print("md_files:", [p.name for p in Path("md_files").iterdir()])
```

Result:

```
txt_files: ['a.txt', 'b.txt']
md_files: ['readme.md']
```

What happens here? We create files of different types, then two destination folders. The loop checks each file's extension and "moves" it into the right folder via `rename()`. Note: `file.rename(Path("txt_files") / file.name)` does not change the file name, only the folder. Such "organizers" are really used to sort downloads: music into one folder, pictures into another, documents into a third.

### Solution 5
Solution:

```python
print("Hi! I'm an echo bot.")
name = input("What is your name? ")
print("Nice to meet you,", name, "!")

while True:
    message = input("You: ")
    if message.lower() == "bye":
        print("Bot: Bye-bye! Come back soon.")
        break
    print("Bot: You wrote:", message)
```

Example dialog:

```
Hi! I'm an echo bot.
What is your name? Anna
Nice to meet you, Anna !
You: Hello
Bot: You wrote: Hello
You: bye
Bot: Bye-bye! Come back soon.
```

What happens here? `input()` stops the program and waits for the user's input, then returns the typed string. `message.lower()` converts the text to lowercase so "Bye" and "bye" count as equal. The comparison `== "bye"` decides whether to say goodbye (`break` — exit the loop) or repeat the message. This exact pattern — "listen, decide, answer" — underlies every bot in the world, from simple scripts to virtual assistants.
<!--/SOLUTION-->

<!--QUIZ-->
What is automation in programming?
- A program does repetitive work for a person
- A program writes other programs by itself
- Speeding up the computer
* Correct answer: A program does repetitive work for a person
Automation is handing routine actions over to programs.

Which Python module is convenient for working with files and folders?
- pathlib
- random
- datetime
* Correct answer: pathlib
pathlib represents file paths as objects with methods like mkdir, rename, iterdir.

What does Path("fd").mkdir(exist_ok=True) do?
- Creates the folder without raising an error if it already exists
- Deletes the folder
- Renames the folder
* Correct answer: Creates the folder without raising an error if it already exists
exist_ok=True allows the "failure" of creation when the folder already exists.

Which method reads text from a file in pathlib?
- read_text(encoding="utf-8")
- open()
- get_text()
* Correct answer: read_text(encoding="utf-8")
The read_text() method returns the file contents as a string.

What does the while True loop do?
- Runs the loop body forever until break fires
- Runs the loop body exactly once
- Runs the loop body 10 times
* Correct answer: Runs the loop body forever until break fires
while True creates an infinite loop; you exit it with break.

Which function waits for keyboard input from the user?
- input()
- read()
- ask()
* Correct answer: input()
input() stops the program, waits for a line from the keyboard, and returns it.

What is an f-string like f"image{i}.jpg" for?
- To insert a variable's value into a string
- To join two strings
- To check a string's length
* Correct answer: To insert a variable's value into a string
Inside the curly braces of an f-string Python inserts the expression's value.

Why does deleting files with a script require caution?
- Because deletion is irreversible and can erase needed data
- Because Python cannot delete files
- Because deletion slows the computer
* Correct answer: Because deletion is irreversible and can erase needed data
A program can delete the wrong files, so first show the list and ask for confirmation.

What does time.sleep(3) do?
- Pauses the program for 3 seconds
- Speeds the program up 3 times
- Prints the time every 3 seconds
* Correct answer: Pauses the program for 3 seconds
time.sleep(3) suspends the program for 3 seconds.

What does [p.name for p in Path(".").iterdir()] return?
- A list of names of all files and folders in the current folder
- The number of files in the current folder
- The path to the current folder
* Correct answer: A list of names of all files and folders in the current folder
This is a list comprehension: it collects the names of all folder items into a list.
<!--/QUIZ-->
