---
title: Famous Python projects
summary: Where Python works in the real world: YouTube, Instagram, Dropbox, Google, NASA, games, science, and AI. Inspiring stories.
order: 7
duration: 25 min
difficulty: beginner
tags: projects, companies, history, inspiration
---

## Python has already changed the world. You're next

Sometimes it seems programming is about screens and brackets. But behind every major service you use daily there is code, and in a huge number of cases that code is Python. Let's take a walk through famous projects and see where our language lives. These aren't just interesting facts — they are proof that Python is capable of great things.

## Web giants

- **Instagram.** One of the largest projects on Django — a Python framework. The Instagram team has publicly said their backend runs on Django and Python, and that this lets them ship features fast for hundreds of millions of users.
- **YouTube.** The video service started on Python: early versions used Python for key parts of the platform, and this code ran at enormous scale.
- **Dropbox.** A popular cloud storage service: the desktop client was originally written almost entirely in Python. Founder Drew Houston started with Python.
- **Google.** Python is one of Google's official languages. The search engine's early crawler (a program that visits sites) was written in Python, and Google still actively uses it in internal tools.
- **Spotify, Pinterest, Reddit.** These companies' backend services are largely built on Python.

## Science and space

- **NASA.** The space agency uses Python to process satellite images, calculate orbits, and analyze scientific data. Many mission tools are in Python.
- **CERN.** The European particle physics laboratory (Large Hadron Collider) actively uses Python to analyze experiment data.
- **Scientific computing.** NumPy, SciPy, and Matplotlib are the world standard: from bioinformatics to astrophysics.

## Games and entertainment

- **Civilization IV.** The cult turn-based strategy allowed modding the game in Python — the gaming community created thousands of mods.
- **EVE Online.** The space MMO uses Python (a Stackless Python variant) for game world logic, serving tens of thousands of concurrent players.
- **Blender.** A professional 3D editor: its scripting language is Python, and all animation and effect automation is written in it.

## Artificial intelligence

- **PyTorch.** The neural network framework created at Meta made Python the standard for AI research.
- **OpenAI and ChatGPT.** GPT models are trained and served on the Python ecosystem: PyTorch and internal Python tools.
- **All major LLMs.** Practically every large language model — Gemini, Llama, Claude — lives in the Python world in one way or another: training, data processing, APIs.

## Finance

Banks, exchanges, and fintech companies use Python for risk analysis, trading algorithms, and forecasts. Simplicity and math libraries made Python the de facto standard of quantitative finance.

## What this means for you

All these projects once started with simple scripts — the same kind you've already written in previous lessons. Nobody was "born" knowing how to write Instagram or a game: first there were hundreds of small programs, errors, curiosity. Python doesn't make you a genius automatically, but it removes the barrier between a thought and working code — and that's the most important thing.

Let's finish the lesson with a mini-demo that reminds us: even simple bricks build big systems.

```python
import random

facts = [
    "Instagram runs on Django — a Python framework.",
    "The Dropbox client is historically written in Python.",
    "Google's early crawler was written in Python.",
    "NASA uses Python to process space data.",
    "EVE Online uses Python for its game world logic.",
]
print(random.choice(facts))
```

## Lesson summary

Today we learned:

- that Python stands behind Instagram, YouTube, Dropbox, and Google;
- that NASA and CERN use it in science and space;
- that Civilization IV and EVE Online were programmed in Python;
- that PyTorch and ChatGPT live in the Python ecosystem;
- that big projects start with small simple scripts.

Now — practice that connects you to these stories.

<!--TASK-->
### Task 1
Write a program `fact_of_day.py` that stores a list of five facts about Python and its projects (take them from the lesson or invent your own) and prints one random fact on each run. Use `random.choice(facts)`. Run the program three times in a row and make sure the facts can change. Add a line `Fact of the day ready!` at the end.

### Task 2
Write a program `recommender.py` — a mini-model of a recommendation system (like Netflix). There is a purchase list: `["book", "coffee", "book", "blanket", "coffee", "book"]`. Count with `Counter` which product is bought most often and print `We recommend buying: book` (the item with the maximum frequency) and the rarest purchase. Use `most_common()`.

### Task 3
Write a program `search_engine.py` — a mini-model of a search engine. There is a list of "pages": `pages = {"python.org": "Python is a great language", "github.com": "Code hosting", "wikipedia.org": "Free encyclopedia"}`. The program takes a search query via `input()`, goes through all pages, and prints those whose text contains the query (the `in` operator). If nothing is found — print `Nothing found`.

### Task 4
Write a program `timeline.py` that stores a dictionary of famous milestones: `{"Python created": 1991, "Google started using Python": 1996, "YouTube launched": 2005, "Instagram launched": 2010, "PyTorch created": 2016, "ChatGPT launched": 2022}`. The program should print all events in order from oldest to newest (use `sorted()` by value) and separately the earliest event.

### Task 5
Write a program `python_top_letters.py`: take the word `"python"`, count each letter's frequency with `Counter` and print the letters in descending frequency order (via `most_common()`). Then print the unique letters and their count. This is a little study of the "insides" of the name of the language you're learning to program in.
<!--/TASK-->

<!--HINT-->
### Hint 1
Create a list of strings `facts = [...]`. Add `import random`. Print `print(random.choice(facts))`. Then add `print("Fact of the day ready!")`. On each run `random.choice` picks a random list element.

### Hint 2
Add `from collections import Counter`. `Counter(purchases)` counts frequencies. The most frequent: `counter.most_common(1)[0]` — a pair (product, count). The rarest: `counter.most_common()[-1]`. Print both with f-strings.

### Hint 3
Read the query: `query = input("Search: ").lower()`. Loop with `for page, text in pages.items():`. Check containment with `if query in text.lower():` — don't forget `lower()` so case doesn't interfere. Collect found pages into a list and print it or `Nothing found`.

### Hint 4
Use `sorted(events.items(), key=lambda item: item[1])` — sort by year (value). Each pair is `(event, year)`. Print them in a loop: `print(f"{year}: {event}")`. The earliest is the first element of the sorted list: `sorted_events[0]`.

### Hint 5
`Counter("python")` gives letter frequencies. `counter.most_common()` — a list of pairs in descending frequency order. Print each pair: `for letter, count in counter.most_common(): print(letter, count)`. Unique letters — `len(counter)`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
import random

facts = [
    "Instagram runs on Django — a Python framework.",
    "The Dropbox client is historically written in Python.",
    "Google's early crawler was written in Python.",
    "NASA uses Python to process space data.",
    "EVE Online uses Python for its game world logic.",
]

print(random.choice(facts))
print("Fact of the day ready!")
```

What happens here? The `facts` list contains five strings. `random.choice(facts)` picks one random string from the list — on each run the result can differ. This is how "fact of the day" widgets on sites, random wisdom in apps, and even servers that shuffle quiz dictionaries work. Randomness is an important tool: it makes programs alive and pleasantly unpredictable.

### Solution 2
Solution:

```python
from collections import Counter

purchases = ["book", "coffee", "book", "blanket", "coffee", "book"]
counter = Counter(purchases)

top_product, top_count = counter.most_common(1)[0]
rare_product, rare_count = counter.most_common()[-1]

print(f"We recommend buying: {top_product} ({top_count} purchases)")
print(f"The rarest purchase: {rare_product} ({rare_count} purchase)")
```

Result:

```
We recommend buying: book (3 purchases)
The rarest purchase: blanket (1 purchase)
```

What happens here? `Counter` counts purchase frequencies. `most_common(1)[0]` returns the first (most frequent) pair, `most_common()[-1]` — the last (rarest). We unpack the pairs into variables `top_product, top_count`. This is a prototype of recommendation systems: Netflix recommends what you watched more often, shops suggest "often bought together". All the magic is in counting frequencies — exactly what we know how to do.

### Solution 3
Solution:

```python
pages = {
    "python.org": "Python is a great language",
    "github.com": "Code hosting",
    "wikipedia.org": "Free encyclopedia",
}

query = input("Search: ").lower()
found = []

for page, text in pages.items():
    if query in text.lower():
        found.append(page)

if found:
    print("Found on pages:", found)
else:
    print("Nothing found")
```

Example run:

```
Search: language
Found on pages: ['python.org']
```

What happens here? `pages.items()` iterates "address — page text" pairs. The operator `query in text.lower()` checks whether the query occurs in the text; `lower()` makes everything lowercase so "Language" and "language" count as equal. Found pages are collected into the `found` list. This is a simplified but real text search — the same principle search engines use, only on the scale of billions of pages.

### Solution 4
Solution:

```python
events = {
    "Python created": 1991,
    "Google started using Python": 1996,
    "YouTube launched": 2005,
    "Instagram launched": 2010,
    "PyTorch created": 2016,
    "ChatGPT launched": 2022,
}

sorted_events = sorted(events.items(), key=lambda item: item[1])

for event, year in sorted_events:
    print(f"{year}: {event}")

earliest = sorted_events[0]
print("Earliest event:", earliest[0], earliest[1])
```

Result:

```
1991: Python created
1996: Google started using Python
2005: YouTube launched
2010: Instagram launched
2016: PyTorch created
2022: ChatGPT launched
Earliest event: Python created 1991
```

What happens here? `sorted(events.items(), key=lambda item: item[1])` sorts pairs by the second element (year). `lambda item: item[1]` is an anonymous function that says: "extract the element at index 1 for comparison". The result is a chronology. This is how analytics builds event timelines — from project history to sales charts. `sorted()` is one of Python's most useful tools; you'll meet it constantly.

### Solution 5
Solution:

```python
from collections import Counter

word = "python"
counter = Counter(word)

print("Letter frequencies:")
for letter, count in counter.most_common():
    print(letter, "-", count)

print("Unique letters:", len(counter))
```

Result:

```
Letter frequencies:
p - 1
y - 1
t - 1
h - 1
o - 1
n - 1
Unique letters: 6
```

What happens here? `Counter("python")` counts each character. `most_common()` returns all pairs in descending frequency order — here every letter appears once, but if you take a word with repeated letters, the order becomes visual. `len(counter)` is the number of unique letters. This is a tiny but real data study: you collected statistics on text. Such simple experiments build analytical thinking — the main skill for working with data.
<!--/SOLUTION-->

<!--QUIZ-->
Which Python framework does Instagram run on?
- Django
- Flask
- Kivy
* Correct answer: Django
Instagram is one of the largest projects on Django.

Which part of Dropbox was historically written in Python?
- The desktop client
- The web server
- The mobile app
* Correct answer: The desktop client
Dropbox's founder started with Python; the client was written almost entirely in it.

What did NASA use Python for?
- Processing space images and scientific data
- Launching rockets from a keyboard
- Creating games
* Correct answer: Processing space images and scientific data
NASA uses Python to analyze mission data.

Which game allowed writing mods in Python?
- Civilization IV
- Tetris
- Solitaire
* Correct answer: Civilization IV
The Civilization IV community created thousands of Python mods.

Which neural network framework was created at Meta?
- PyTorch
- Django
- Flask
* Correct answer: PyTorch
PyTorch is the standard of AI research, created at Meta.

In what language was Google's early crawler written (per known stories)?
- Python
- Assembly
- SQL
* Correct answer: Python
Google's early crawler was written in Python.

Which game uses Python for its game world logic?
- EVE Online
- Chess
- Minesweeper
* Correct answer: EVE Online
EVE Online uses Stackless Python to serve its game world.

What does random.choice(facts) do?
- Picks a random element from the list
- Sorts the list
- Deletes a random element
* Correct answer: Picks a random element from the list
random.choice returns one random element of a sequence.

What does sorted(events.items(), key=lambda item: item[1]) do?
- Sorts pairs by the second element (year)
- Sorts pairs alphabetically
- Deletes duplicates
* Correct answer: Sorts pairs by the second element (year)
key=lambda item: item[1] says to compare the second value of each pair.

Why are big project stories important for a beginner?
- They prove big projects start with simple code
- They replace practice
- They contain secret passwords
* Correct answer: They prove big projects start with simple code
Every giant started with small programs and gradual growth.
<!--/QUIZ-->
