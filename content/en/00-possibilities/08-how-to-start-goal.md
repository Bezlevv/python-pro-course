---
title: How to set a goal and start
summary: SMART goals, the map of 30 course modules, a first-30-days plan, and progress-tracking tools. Your start in Python.
order: 8
duration: 30 min
difficulty: beginner
tags: goal, plan, motivation, course map, 30 days
---

## Knowing why you learn is half the success

You've completed seven lessons of this module and now know what Python can do: automation, web, data, AI, games, DevOps, robots. It's a huge arsenal. But the most important question remains: **what exactly do you want to do?**

Without an answer, energy runs out fast: mornings don't start with code, lessons get postponed, the course stays on the shelf. With a goal everything is different: you know where you're going, and every small step makes sense. This lesson is about setting the right goal and not losing momentum in the first 30 days.

## Goals vary: the SMART recipe

A bad goal: "I want to learn Python." A good goal: "In 6 weeks I'll write a program that renames my photos by date and show it to my friends." Feel the difference? SMART helps formulate a goal:

- **S — Specific.** Not "learn Python" but "write a script to rename photos".
- **M — Measurable.** "I'll run it on 100 files and it will work without errors".
- **A — Achievable.** A realistic scale: not "make a new Instagram" but "make my first site".
- **R — Relevant.** The goal must matter to you, not just "because everyone learns it".
- **T — Time-bound.** "By December 1" — a deadline that mobilizes you.

## Course map: your route of 30 modules

The "PythonPro" course consists of 30 modules. Here is the whole map — from first steps to a professional level:

| # | Module | About |
|---|---|---|
| 0 | What you can do with Python | You are here: overview of superpowers and the goal |
| 1 | Python basics | Variables, types, conditions, loops, functions |
| 2 | Advanced Python | Iterators, generators, decorators, closures |
| 3 | Standard library | Files, collections, dates, utilities |
| 4 | Data and analytics | Pandas, NumPy, visualization |
| 5 | Web development | Django, Flask, FastAPI, HTML/CSS |
| 6 | Neural networks | PyTorch: training models |
| 7 | Practical projects | Building real projects |
| 8 | Asynchronicity | asyncio, multithreading, parallelism |
| 9 | Senior level | Advanced patterns and design thinking |
| 10 | Deploy and production | Deployment, CI/CD, monitoring |
| 11 | Algorithms | Data structures, complexity, olympiad problems |
| 12 | DevOps | Docker, infrastructure automation |
| 13 | Databases | SQL, SQLite, PostgreSQL, ORM |
| 14 | Software architecture | Clean architecture, design patterns |
| 15 | Career | Resume, interviews, freelance |
| 16 | AI applications | Working with LLMs: prompts, engineering, agents |
| 17 | Scraping | BeautifulSoup, Scrapy, scraping ethics |
| 18 | Tricks and optimizations | Performance secrets and goodies |
| 19 | MicroPython | Python on microcontrollers, IoT |
| 20 | Practical works | Portfolio and own projects |
| 21 | Testing | unittest, pytest, TDD |
| 22 | Django REST Framework | Django APIs for serious projects |
| 23 | Performance | Profiling and optimization |
| 24 | Cybersecurity | App protection, ethical hacking |
| 25 | MLOps | Industrial model deployment |
| 26 | Games in Python | pygame, game loop, physics |
| 27 | PyQt | Professional desktop applications |
| 28 | Libraries | How popular packages work |
| 29 | Office automation | Excel, Word, PDF, reports |
| 30 | Python and life | Final project and plans for the future |

You don't need to complete everything at once. Right now your goal is to finish the first two or three modules and build your first own project to feel how your motive works.

## First 30 days plan

The first thirty days decide whether a hobby becomes a skill. Here is a proven plan.

- **Days 1–3. Launch.** Install Python, set up an editor (VS Code), run first programs, complete module 1 "Basics".
- **Days 4–7. Daily minimum.** At least 20 minutes of code every day: variables, conditions, loops, functions. Don't set the bar at "two hours" — regularity matters more.
- **Days 8–10. Collections and strings.** Lists, dictionaries, strings, file work — finish module 1.
- **Days 11–13. Mini-automation.** Write a script that does something useful for you: sorts files, renames photos, counts something. This is your first "real" project.
- **Days 14–16. Web and data (first acquaintance).** Module 4 or 5: try an API request or a simple data analysis script.
- **Days 17–19. First big mini-project.** Pick one task (TODO list, calculator, echo bot, price parser) and take it to the end.
- **Days 20–22. Polishing.** Add error handling, split code into functions, add comments. Show the project to a friend.
- **Days 23–27. Deepening.** Complete module 2 "Advanced Python" or 3 "Standard library", keep improving the project.
- **Days 28–30. Publishing.** Create a GitHub account, upload your project's code, write a README. This is your business card.

## Habit beats talent

The secret of progress is not motivation but a system. Three rules:

1. **Minimum, but every day.** 20 minutes daily beats 4 hours once a week.
2. **Code is written by hand.** Don't read about Python — type it. Finish every lesson with tasks.
3. **Track progress.** Write down what you did. A simple table of days and checkmarks works wonders.

Here is a demo habit tracker — a program that calculates the percentage of successful days:

```python
habits = [True, True, False, True, True, True, False]
days = len(habits)
success = sum(habits) / days * 100
print(f"Weekly progress: {success:.0f}%")
print(f"Successful days: {sum(habits)} of {days}")
```

`sum(habits)` counts `True` values (in Python `True` = 1), then we divide by the number of days and get a percentage. Keep such a tracker in real life — and in a month you'll be surprised by the result.

## Lesson summary

Today we learned:

- how to set SMART goals: specific, measurable, achievable, relevant, time-bound;
- the full map of the 30-module course;
- a first-30-days plan: from installation to publishing a project on GitHub;
- why regularity matters more than volume;
- how to calculate your progress percentage.

The course doesn't start with the first lesson — it starts with the decision. You've already made it. Go!

<!--TASK-->
### Task 1
Write a program `todo_day.py` — a daily checklist. Create a task list: `["Learn the lesson", "Run code example", "Solve tasks"]`. Print the list with numbers (`1. Learn the lesson` and so on), then ask the user to enter the number of the completed task (via `int(input())`), remove it from the list with `.pop(index)` and print the remaining tasks. If the list becomes empty — print `All tasks done! Great day!`.

### Task 2
Write a program `smart_goal.py` that helps formulate a SMART goal. The program asks four things via `input()`: what you want to do, by when, what result will be a sign of success, and why it matters. Then it prints the assembled goal as nice formatted text: `My goal: ...`, `Deadline: ...`, `Sign of success: ...`, `Why it matters: ...`. Fill it with your real goal.

### Task 3
Write a program `progress_tracker.py` — a habit tracker. There is a list of 7 boolean values (e.g., `[True, True, False, True, True, False, True]`), where `True` is a day you practiced. Count and print: the number of successful days, the number of misses, and the success percentage (rounded to a whole number). If the percentage >= 70, print `Great pace!`, otherwise — `Add a daily minimum`.

### Task 4
Write a program `course_map.py` that prints the course map: the first 10 modules from the lesson table (numbers 0 to 9 with names). Use a list of pairs `[(0, "What you can do with Python"), (1, "Python basics"), ...]` and a loop `for number, name in modules:` printing `0. What you can do with Python`. At the end print `Total in the map: N modules` — with the list length.

### Task 5
Write a program `learning_diary.py` — a learning diary. The program asks via `input()` for a note about what you learned today and saves it to a file `diary.txt` (appending to the end, not overwriting), adding the date. Use `open("diary.txt", "a", encoding="utf-8")` — mode `a` (append) adds to the end. Then read the file and print all saved notes. Keep such a diary for all 30 days.
<!--/TASK-->

<!--HINT-->
### Hint 1
Number with `enumerate(tasks, 1)`: `for i, task in enumerate(tasks, 1): print(i, task)`. Choice: `choice = int(input("Which task is done? "))`. Removal — `tasks.pop(choice - 1)` (minus 1 because numbers start at 1 but indexes at 0). If `len(tasks) == 0` — print congratulations.

### Hint 2
Create four variables via `input()`: `goal = input("What do you want to do? ")`, `deadline = input("By when? ")`, `success = input("What will be the sign of success? ")`, `why = input("Why does it matter? ")`. Then print four lines with f-strings: `f"My goal: {goal}"` and so on.

### Hint 3
Successful days — `sum(days)` (True counts as 1). Misses — `len(days) - sum(days)`. Percentage — `round(sum(days) / len(days) * 100)`. Compare `if percent >= 70:` — remember the percentage is already a number, not a string.

### Hint 4
Create a list of tuples: `modules = [(0, "What you can do with Python"), (1, "Python basics"), ...]` (10 items). Loop: `for number, name in modules: print(f"{number}. {name}")`. Count — `len(modules)`. Print the final line.

### Hint 5
Get the date: `from datetime import datetime` and `today = datetime.now().strftime("%d.%m.%Y")`. Open the file in append mode: `with open("diary.txt", "a", encoding="utf-8") as f: f.write(f"{today}: {entry}\n")`. Then read: `print(open("diary.txt", encoding="utf-8").read())`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
tasks = ["Learn the lesson", "Run code example", "Solve tasks"]

print("Today's tasks:")
for i, task in enumerate(tasks, 1):
    print(i, task)

choice = int(input("Which task is done? "))
tasks.pop(choice - 1)

if tasks:
    print("Remaining:", tasks)
else:
    print("All tasks done! Great day!")
```

Example run:

```
Today's tasks:
1 Learn the lesson
2 Run code example
3 Solve tasks
Which task is done? 2
Remaining: ['Learn the lesson', 'Solve tasks']
```

What happens here? `enumerate(tasks, 1)` gives "number, task" pairs starting at 1. `int(input())` reads input as a number. `tasks.pop(choice - 1)` removes the element at the given index (hence we subtract 1: the user sees numbers from 1, but indexes start at 0). The final condition checks whether tasks remain. This is a simple but real planner program — millions of people use such ones daily.

### Solution 2
Solution:

```python
goal = input("What do you want to do? ")
deadline = input("By when? ")
success = input("What will be the sign of success? ")
why = input("Why does it matter? ")

print()
print("My goal:", goal)
print("Deadline:", deadline)
print("Sign of success:", success)
print("Why it matters:", why)
```

Example run:

```
What do you want to do? Write a file-sorting script
By when? 2 weeks
What will be the sign of success? It sorts 100 files without errors
Why does it matter? I'm tired of doing it by hand
My goal: Write a file-sorting script
Deadline: 2 weeks
Sign of success: It sorts 100 files without errors
Why it matters: I'm tired of doing it by hand
```

What happens here? Four `input()` calls gather four components of the statement. Then we print them as a neat formatted block. `print()` without arguments prints an empty line for tidiness. This is an "honest" SMART goal: specific (what exactly), measurable (sign of success), achievable (2 weeks), relevant (why it matters), time-bound (deadline). Keep this statement somewhere visible.

### Solution 3
Solution:

```python
days = [True, True, False, True, True, False, True]

success_days = sum(days)
missed = len(days) - success_days
percent = round(success_days / len(days) * 100)

print("Successful days:", success_days)
print("Misses:", missed)
print("Success percentage:", percent, "%")

if percent >= 70:
    print("Great pace!")
else:
    print("Add a daily minimum")
```

Result:

```
Successful days: 5
Misses: 2
Success percentage: 71 %
Great pace!
```

What happens here? In Python `True` is 1 and `False` is 0, so `sum(days)` counts successful days. Misses are the difference from the total days. The percentage is the share of successful days times 100, rounded. Such a tracker is an exact copy of tools used by athletes and entrepreneurs: measure, and progress becomes visible. The "minimum, but daily" rule comes straight from here: regularity gives a high percentage.

### Solution 4
Solution:

```python
modules = [
    (0, "What you can do with Python"),
    (1, "Python basics"),
    (2, "Advanced Python"),
    (3, "Standard library"),
    (4, "Data and analytics"),
    (5, "Web development"),
    (6, "Neural networks"),
    (7, "Practical projects"),
    (8, "Asynchronicity"),
    (9, "Senior level"),
]

for number, name in modules:
    print(f"{number}. {name}")

print("Total in the map:", len(modules), "modules")
```

Result:

```
0. What you can do with Python
1. Python basics
...
9. Senior level
Total in the map: 10 modules
```

What happens here? A list of tuples `(number, name)` is a compact way to store a table. The loop `for number, name in modules:` unpacks each tuple into two variables; the f-string prints number and name. `len(modules)` counts the entries. This is how any reference book is built in code: from a course map to a product catalog. You saw the full 30-module map in the theory — now you know how to print it programmatically.

### Solution 5
Solution:

```python
from datetime import datetime

entry = input("What did you learn today? ")
today = datetime.now().strftime("%d.%m.%Y")

with open("diary.txt", "a", encoding="utf-8") as f:
    f.write(f"{today}: {entry}\n")

print("— Diary entries —")
print(open("diary.txt", encoding="utf-8").read())
```

Example run (on repeated launches):

```
— Diary entries —
01.11.2026: Learned to work with loops
02.11.2026: Figured out functions
```

What happens here? Mode `"a"` (append) opens the file for appending to the end — each run adds a new line without deleting old ones. `datetime.now().strftime("%d.%m.%Y")` puts the date. The f-string assembles the entry: date, text, newline. At the end we read the whole file and print the entire diary. Keep this diary for 30 days — in a month it will be your first "learning story", pleasant to reread and show.
<!--/SOLUTION-->

<!--QUIZ-->
What does the letter S in SMART mean?
- Specific — a specific goal
- Speed
- Simple
* Correct answer: Specific — a specific goal
A goal should answer "what exactly will I do", not "I want to learn Python".

What is the "measurability" of a goal?
- A feature that makes it clear whether the goal is achieved
- The speed of achieving the goal
- The size of the goal
* Correct answer: A feature that makes it clear whether the goal is achieved
A measurable goal has a clear success criterion, e.g., "sorts 100 files".

Why is regularity more important than the volume of study?
- Short daily sessions build a habit better than rare marathons
- Because long sessions are harmful
- Regularity makes no difference
* Correct answer: Short daily sessions build a habit better than rare marathons
20 minutes every day works better than 4 hours once a week.

What does sum([True, True, False]) return?
- 2
- 3
- False
* Correct answer: 2
In Python True = 1 and False = 0, so the sum is 1 + 1 + 0 = 2.

Which file-opening mode appends to the end without overwriting?
- "a" (append)
- "w" (write)
- "r" (read)
* Correct answer: "a" (append)
Mode "a" adds data to the end of the file, keeping existing content.

What does enumerate(tasks, 1) do?
- Returns (number, element) pairs starting at 1
- Sorts the list
- Deletes the first element
* Correct answer: Returns (number, element) pairs starting at 1
enumerate adds ordinal numbers to list elements.

How many modules are in the "PythonPro" course?
- 30
- 10
- 5
* Correct answer: 30
The course consists of 30 modules — from basics to professional topics.

What does Time-bound mean in SMART?
- The goal is limited in time; it has a deadline
- The goal must be fast
- The goal shouldn't take time
* Correct answer: The goal is limited in time; it has a deadline
Having a deadline mobilizes you and helps evaluate progress.

What is a learning diary useful for?
- It shows progress and history, helps stay on track
- It replaces practice
- It teaches Python automatically
* Correct answer: It shows progress and history, helps stay on track
Notes make progress visible and motivate you to continue.

What should you do if the tracker's success percentage is below 70?
- Reduce the daily minimum and don't skip days
- Quit learning
- Raise the plan to 5 hours
* Correct answer: Reduce the daily minimum and don't skip days
It's easier to take a small step every day than a big one rarely.
<!--/QUIZ-->
