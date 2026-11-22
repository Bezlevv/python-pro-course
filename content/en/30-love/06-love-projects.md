---
title: Projects for the Soul: Ideas and Scaffolds
summary: Seven ideas and five scaffolds for first projects: a to-do list, a quest, a habit tracker, a motivator, and a poem analyzer.
order: 6
duration: 40 min
difficulty: intermediate
tags: projects, scaffolds, ideas, practice
---

You now know enough to start creating your own things. Projects for the soul aren't an obligation — they're what makes a skill come alive: you choose a topic that warms you and turn it into code. Today I'll show five scaffolds — reliable starting points — and then it's your imagination's flight.

## Why this matters

Textbook exercises teach syntax; projects teach you to create: to design, to break things into functions, to finish what you started. What's more, a finished project is the best portfolio: it says more about you than any certificate.

## Idea 1: CLI to-do list

Managing tasks from the terminal. The scaffold: a dictionary `{name: status}` plus `add`, `list_tasks`, `done` functions:

```python
tasks = {}

def add(name):
    tasks[name] = False

def list_tasks():
    for name, completed in tasks.items():
        mark = "✓" if completed else "○"
        print(f"{mark} {name}")

add("Do homework")
list_tasks()
```

## Idea 2: Text game

A room-by-room walker: a room is a dictionary with a description and exits:

```python
rooms = {
    "kitchen": {"description": "Smells like pies.", "exits": {"north": "living room"}},
    "living room": {"description": "A big sofa.", "exits": {"south": "kitchen"}},
}
```

## Idea 3: Habit tracker

Mark the days you kept a habit and count the continuous streak:

```python
week = [False, True, True, True]

def streak(days):
    count = 0
    for day in reversed(days):
        if not day:
            break
        count += 1
    return count

print(streak(week))  # 3: the last three days in a row are True
```

## Idea 4: Motivation generator

Inspiring phrases + randomness + a personal name:

```python
import random

phrases = ["You've got this!", "Every day is a step forward!"]
print(random.choice(phrases))
```

## Idea 5: Text analyzer

Count words, find frequent ones, find palindromes:

```python
from collections import Counter

text = "python snake python"
words = text.split()
print(Counter(words))  # Counter({'python': 2, 'snake': 1})
```

`collections.Counter` is a ready-made counter, a small but mighty feature.

## The main rule of a project

Break the project into functions, each small and clear. Start with the simplest working version, then complicate it. No great project was written in one evening — but every one began with a first working version. "Now is better than never" — remember?

Let's turn the five scaffolds from these ideas into tasks. Each is doable in one evening — and ready to grow.

<!--TASK-->
### Task 1
Assemble the CLI to-do list scaffold. Write the functions: `add(task)` — adds a task to the dictionary `tasks` with status `False` (not done); `list_tasks()` — prints each task with a `✓` mark (done) or `○` (not); `mark_done(task)` — changes the status to `True`. Demonstrate: add three tasks, mark one as done, print the list. Expected result: three lines like `✓ task` and `○ task`.

### Task 2
Assemble the text game scaffold. Create a dictionary `rooms` with at least three rooms: `"kitchen"`, `"living room"`, `"garden"`. Each room has a `"description"` key and `"exits"` (a dictionary: direction → room name). Write a function `go(room, direction)` that returns the new room or the string `You can't go there!` if the direction doesn't exist. Test the transitions across all three rooms and print the descriptions of the rooms you can reach from each.

### Task 3
Write a function `streak(days)` that takes a list of booleans (True — the habit was kept) and returns the length of the continuous streak at the **end** of the list: how many recent days in a row were True. If the last day is False — return 0. Test on three examples: `[True, True, False, True, True]` → `2`, `[True, True, True]` → `3`, `[False, True, False]` → `0`. Expected output: three numbers — `2`, `3`, `0`.

### Task 4
Write a "Personal motivator" program. Create a list of five inspiring phrases. Ask the user for their name with `input()`. Then pick a random phrase with `random.choice` and print `Name, phrase` — for example: `Anna, every day is a step forward!`. Run the program twice and make sure the phrases can differ. Expected result: one line with the user's name and a random phrase.

### Task 5
Write a "Poem analyzer" program. It takes a text (a string), splits it into words with `split()`, counts each word's frequency with `collections.Counter`, and prints the three most frequent words with their counts. Use the `most_common(3)` method. Test on the text: `"sun shines brightly sun warms earth"`. Expected result: three lines like `sun: 2`, `shines: 1`, `brightly: 1` (ordered by decreasing frequency).

<!--/TASK-->

<!--HINT-->
### Hint 1
The dictionary key is the task name, the value is the status `True`/`False`. `mark_done` can simply assign `tasks[task] = True`. In `list_tasks()` iterate with `for task, done in tasks.items():` and choose the symbol with a ternary expression: `"✓" if done else "○"`.

### Hint 2
Access a room as a dictionary: `rooms[room]["exits"]` — the dictionary of directions. Check: `if direction in rooms[room]["exits"]:` — in that case return `rooms[room]["exits"][direction]`. For the demo, print the descriptions of neighboring rooms via `rooms[new_room]["description"]`.

### Hint 3
Walk the list from the end: `for day in reversed(days):`. If `day` is False, exit the loop with `break`. Increment the counter while walking through True values. Remember: after exiting, return the counter.

### Hint 4
Store the list of phrases in a variable `phrases`. `name = input("What's your name? ")` gets the name. `random.choice(phrases)` picks a phrase. Print with an f-string: `f"{name}, {phrase}"`. You may need to add `import random` at the top of the file.

### Hint 5
`from collections import Counter`. After `words = text.split()` you get a list of words. `Counter(words).most_common(3)` returns a list of `(word, count)` pairs. In a loop, unpack the pairs and print `f"{word}: {count}"`.

<!--/HINT-->

<!--SOLUTION-->
### Walkthrough 1
Solution:

```python
tasks = {}

def add(task):
    tasks[task] = False

def list_tasks():
    for task, done in tasks.items():
        mark = "✓" if done else "○"
        print(f"{mark} {task}")

def mark_done(task):
    tasks[task] = True

add("Learn the lesson")
add("Read a chapter")
add("Do exercises")
mark_done("Learn the lesson")

list_tasks()
```

Result:

```
✓ Learn the lesson
○ Read a chapter
○ Do exercises
```

What's happening here? The dictionary `tasks` stores the tasks: the key is the name, the value is the status. The `add` function adds a task marked "not done" (`False`). `list_tasks` walks all tasks and chooses the symbol with the ternary expression `"✓" if done else "○"`. `mark_done` changes the status. The program is a complete mini-project: it's easy to extend (deletion, saving to a file, priorities), but even as is, it already works.

### Walkthrough 2
Solution:

```python
rooms = {
    "kitchen": {"description": "Smells like pies.", "exits": {"north": "living room"}},
    "living room": {"description": "A big sofa.", "exits": {"south": "kitchen", "east": "garden"}},
    "garden": {"description": "Roses are blooming.", "exits": {"west": "living room"}},
}

def go(room, direction):
    if direction in rooms[room]["exits"]:
        return rooms[room]["exits"][direction]
    return "You can't go there!"

next_room = go("kitchen", "north")
print(next_room, "—", rooms[next_room]["description"])
next_room = go("living room", "east")
print(next_room, "—", rooms[next_room]["description"])
next_room = go("garden", "west")
print(next_room, "—", rooms[next_room]["description"])
print(go("kitchen", "south"))
```

Result:

```
living room — A big sofa.
garden — Roses are blooming.
living room — A big sofa.
You can't go there!
```

What's happening here? Each room is a dictionary with a description and exits. The `go` function checks whether the direction exists in the exits dictionary: if yes — it returns the new room's name; if no — the message "You can't go there!" This is the core of any text game. From here the game is easy to grow: add items, inventory, win conditions — the data structure is ready.

### Walkthrough 3
Solution:

```python
def streak(days):
    count = 0
    for day in reversed(days):
        if not day:
            break
        count += 1
    return count

print(streak([True, True, False, True, True]))
print(streak([True, True, True]))
print(streak([False, True, False]))
```

Result:

```
2
3
0
```

What's happening here? `reversed(days)` walks the list from the end — from the last day to the first. While the day is `True`, we increment the counter. As soon as `False` appears, the loop breaks with `break`. In the first example the last two days are True, so the streak is 2. In the second, all three days are True — streak 3. In the third, the last day is False, so the counter stays 0. This is how the "streak" mechanic works in habit trackers — the very mechanism that keeps people engaged in daily routines.

### Walkthrough 4
Solution:

```python
import random

phrases = [
    "every day is a step forward!",
    "you can handle any task!",
    "code doesn't bite, try it!",
    "today is the best day for something new!",
    "your Python is waiting for new ideas!",
]

name = input("What's your name? ")
phrase = random.choice(phrases)
print(f"{name}, {phrase}")
```

Result (example):

```
What's your name? Anna
Anna, every day is a step forward!
```

What's happening here? `input` asks for the name, `random.choice` picks a random phrase from the list, and the f-string assembles the final greeting. Each run may produce a different phrase — that makes the program "alive." Such a motivation generator is a great gift for a friend or just a fun desktop script. The project is easy to extend: add the time of day, a list of achievements, random emoji.

### Walkthrough 5
Solution:

```python
from collections import Counter

text = "sun shines brightly sun warms earth"
words = text.split()
counts = Counter(words)

for word, count in counts.most_common(3):
    print(f"{word}: {count}")
```

Result:

```
sun: 2
shines: 1
brightly: 1
```

What's happening here? `text.split()` splits the string into words by spaces. `Counter(words)` counts how many times each word occurs — returning a dictionary of counts. `most_common(3)` gives the three most frequent `(word, count)` pairs in descending frequency order. The loop unpacks the pairs and prints them. This is the foundation for text analysis: from poems to news. You can replace the text with your own — and see which words you use most often. Such analyzers are a great way to "see" your text in a new light.

<!--/SOLUTION-->

<!--QUIZ-->
Why are soul projects needed?
- They turn a skill into living creativity and a portfolio
- They replace the textbook
- They're only needed for grades
* Correct answer: They turn a skill into living creativity and a portfolio
Projects teach you to design and finish things, and the result can be shown to others.

Which data structure suits a CLI to-do list?
- A dictionary: task → status
- A list of strings
- A number
* Correct answer: A dictionary: task → status
The key is the task name, the value is whether it's done.

How do you represent a room in a text game?
- As a dictionary with a description and exits
- As a number
- As a function without data
* Correct answer: As a dictionary with a description and exits
A room is a dictionary: "description" and "exits", where exits are also a dictionary of directions.

What does streak([True, True, False, True, True]) return?
- 2
- 5
- 3
* Correct answer: 2
The streak is counted from the end: the last two days are True, and before them False — the streak breaks.

What does random.choice(list) do?
- Returns a random element of the list
- Sorts the list
- Removes a random element
* Correct answer: Returns a random element of the list
random.choice selects one element from a sequence.

What does Counter(words).most_common(3) return?
- The three most frequent (word, count) pairs
- Three random words
- All words in alphabetical order
* Correct answer: The three most frequent (word, count) pairs
most_common sorts by frequency and returns the requested number of leaders.

Which method splits a string into words?
- split()
- strip()
- join()
* Correct answer: split()
split breaks a string by spaces into a list of substrings.

What does reversed(days) do in a loop?
- Walks the list from end to start
- Reverses the list permanently
- Sorts the list
* Correct answer: Walks the list from end to start
reversed creates an iterator going from the last element to the first.

What will streak([False, True, False]) return?
- 0
- 1
- 3
* Correct answer: 0
The last day is False — the streak breaks immediately, and the counter stays at zero.

Which symbol is convenient for a completed task in a to-do list?
- ✓ (checkmark)
- ? (question mark)
- * (asterisk)
* Correct answer: ✓ (checkmark)
A checkmark is intuitively understood as a mark of completion.
<!--/QUIZ-->
