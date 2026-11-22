---
title: Desktop, games, mobile apps
summary: Graphic windows with Tkinter and PyQt, games with pygame and turtle, mobile apps with Kivy. We create our first window and first game.
order: 5
duration: 30 min
difficulty: beginner
tags: desktop, games, mobile, tkinter, pygame, kivy
---

## Programs you can touch

So far our programs lived in the terminal — printed text and waited for input. But Python can also create things you see on screen and interact with using the mouse: app windows, games, interfaces. This is a special kind of magic — when your code turns into buttons, fields, and animations.

Today we'll take first steps in three directions at once: desktop apps, games, and mobile development.

## Desktop: Tkinter and PyQt

Desktop applications are programs that run on a computer in their own window: editors, players, calendars, utilities.

- **Tkinter** — Python's built-in GUI library. You don't need to install it: it already comes with Python. Great for starting out: windows, buttons, input fields, lists.
- **PyQt / PySide** — more powerful frameworks based on Qt. A professional tool for serious applications with a modern design.

Here is a minimal Tkinter program — a window with a label:

```python
import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("My first window")
window.geometry("300x200")

# Add a label
label = tk.Label(window, text="Hello, world!", font=("Arial", 16))
label.pack()

# Start the event loop — the window stays open
window.mainloop()
```

Run it — a real window with text appears. `tk.Tk()` creates the window, `tk.Label()` creates the label, `pack()` places it, and `mainloop()` starts the "event loop": the program waits for user actions (clicks, key presses) and reacts to them.

## Games: pygame and turtle

Python is often underestimated as a game language, and unfairly. Of course, AAA games use C++ and specialized engines, but for indie games, prototypes, and learning, Python is an excellent choice.

- **pygame** — a library for creating games: sprites, sound, key handling, game loop. Thousands of educational games — from "Snake" to platformers — are written in pygame.
- **turtle** — a built-in learning module where a "turtle" draws lines and shapes by your commands. It's the perfect way to understand graphics without complex theory.

A "Snake" example in pygame takes about a hundred lines — a realistic amount for a beginner. A quick start looks like this:

```python
import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("My game")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((30, 30, 60))   # dark blue background
    pygame.display.flip()

pygame.quit()
```

Here you see the structure of any game: a `while` loop, event handling (closing the window), frame rendering. Add sprites and logic — and you get a game.

## Mobile apps: Kivy

Want your program to run on a phone? Python helps here too:

- **Kivy** — a framework for multitouch applications: the same code runs on Android, iOS, Windows, and macOS.
- **BeeWare** — lets you build apps with native interfaces and publish them in stores.

Mobile development in Python is a smaller niche than JS/Flutter, but it exists and grows, especially for internal tools, prototypes, and learning apps.

## Building our first window and first game

We already saw a Tkinter window. Let's add a button that changes the text — so you feel the program listening to you:

```python
import tkinter as tk

def change_text():
    label.config(text="You clicked the button!")

window = tk.Tk()
label = tk.Label(window, text="Hello!")
label.pack()
button = tk.Button(window, text="Click me", command=change_text)
button.pack()
window.mainloop()
```

The function `change_text` is called on every button click (that's the "event"). `label.config(text=...)` changes the label text. This is how almost any interface works: button → event → function.

## Lesson summary

Today we learned:

- that Tkinter is a built-in tool for windowed applications;
- how to create a window with a label and a button;
- that pygame is a game library, and turtle is built-in educational graphics;
- that Kivy and BeeWare let you make mobile apps in Python;
- how the event loop and click handling work.

Now let's create our first visible programs.

<!--TASK-->
### Task 1
Write a program `my_window.py` that opens a Tkinter window of 400×300 with the title `My app` and two labels: `Hello, world!` (font size 18) and `Python opens windows` (font size 12). Use `tk.Label()` and `pack()` for both labels. Run the program — a window with two lines of text should appear. Close the window with the X.

### Task 2
Write a program `click_me.py` — a window with the label `I'm not clicked yet` and a button `Click me`. On every click the label should change color (e.g., cycling: black → blue → red → black). Use a handler function with `label.config(fg="...")`. Hint: store the current color index in a variable inside the function (e.g., global or in a list).

### Task 3
Write a program `greeter.py` with an input field (`tk.Entry`) and a button. When the user enters a name and clicks the button, the label below the field should change to `Hello, name!`. Use `.get()` to read the text from the input field. If the field is empty — show `Enter a name!`.

### Task 4
Write a program `turtle_square.py` that draws a square with side 100 pixels using the `turtle` module: the turtle should go forward, turn 90 degrees — and so on four times. Use `turtle.forward(100)` and `turtle.left(90)`. At the end add `turtle.done()` so the drawing window doesn't close itself.

### Task 5
Write a "Guess the number" game in the terminal: the program picks a number from 1 to 10 (`random.randint(1, 10)`), and the player tries to guess it. On each attempt the program answers `Bigger!` or `Smaller!`, and on success — `Correct! Number: N` and the number of attempts. Use a `while True` loop and `break` when guessed. Try playing a few times.
<!--/TASK-->

<!--HINT-->
### Hint 1
Create the window: `window = tk.Tk()`, set the size `window.geometry("400x300")` and title `window.title("My app")`. Create two labels: `tk.Label(window, text="...", font=("Arial", 18))` and a second one with size 12. Place each with `pack()`. At the end — `window.mainloop()`.

### Hint 2
Create a variable `index = 0` and a color list `colors = ["black", "blue", "red"]`. Inside the `change()` function change the color: `label.config(fg=colors[index])`, then `index = (index + 1) % len(colors)` — this cycles the iteration. To change `index` inside the function, declare it global: `global index` as the first line of the function.

### Hint 3
Create `entry = tk.Entry(window)` and `entry.pack()`. In the handler function read `name = entry.get()`. If `name == ""` — show `Enter a name!`, otherwise — `Hello, name!` via `label.config(text=f"Hello, {name}!")`.

### Hint 4
Add `import turtle`. Create a turtle: `t = turtle.Turtle()`. Repeat four times: `t.forward(100)` and `t.left(90)`. You can use a loop `for i in range(4):`. At the end `turtle.done()` — the window stays open.

### Hint 5
Pick a number: `secret = random.randint(1, 10)`. Set `attempts = 0`. In a `while True:` loop read `guess = int(input("Your number: "))`, increase `attempts`, compare with `secret` and print a hint. On a match print the result and `break`. Don't forget `import random`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
import tkinter as tk

window = tk.Tk()
window.title("My app")
window.geometry("400x300")

label1 = tk.Label(window, text="Hello, world!", font=("Arial", 18))
label1.pack()

label2 = tk.Label(window, text="Python opens windows", font=("Arial", 12))
label2.pack()

window.mainloop()
```

What happens here? `tk.Tk()` creates the main window. `geometry("400x300")` sets the size, `title()` the title. `tk.Label()` creates a label: the first argument is the parent window, then the text and font. `pack()` places the label in the window and manages the layout. `mainloop()` starts the event loop: the window lives until closed. This is the minimal "program with a face" — a GUI you can show your friends.

### Solution 2
Solution:

```python
import tkinter as tk

colors = ["black", "blue", "red"]
index = 0

def change():
    global index
    label.config(fg=colors[index])
    index = (index + 1) % len(colors)

window = tk.Tk()
label = tk.Label(window, text="I'm not clicked yet")
label.pack()
button = tk.Button(window, text="Click me", command=change)
button.pack()
window.mainloop()
```

What happens here? `command=change` means: "on click, call the function change". Inside, `global index` allows changing the global variable. `label.config(fg=colors[index])` changes the text color (fg — foreground, text color). The expression `(index + 1) % len(colors)` returns the division remainder: 0 → 1 → 2 → 0 → … — so colors cycle. This is the classic interface pattern: state (current color) + event (click) → reaction.

### Solution 3
Solution:

```python
import tkinter as tk

def greet():
    name = entry.get()
    if name == "":
        label.config(text="Enter a name!")
    else:
        label.config(text=f"Hello, {name}!")

window = tk.Tk()
entry = tk.Entry(window)
entry.pack()
button = tk.Button(window, text="Greet", command=greet)
button.pack()
label = tk.Label(window, text="")
label.pack()
window.mainloop()
```

What happens here? `tk.Entry` is an input field where the user types text. `entry.get()` returns the typed string. If it's empty, we ask for a name; otherwise we insert it into the f-string `f"Hello, {name}!"` and update the label. This is already a full interactive program: input → processing → output. This is how forms, search bars, and chats work. Add this pattern to your toolbox — you'll need it in a hundred projects.

### Solution 4
Solution:

```python
import turtle

t = turtle.Turtle()
for i in range(4):
    t.forward(100)
    t.left(90)

turtle.done()
```

What happens here? `turtle.Turtle()` creates a "turtle" — a cursor that leaves a trail. `t.forward(100)` moves it forward 100 pixels, `t.left(90)` turns it 90 degrees left. Four loop repetitions give a closed square. `turtle.done()` keeps the window open so you can admire the drawing. Turtle is the gateway to computer graphics: the same "move and draw" idea underlies vector graphics and game engines.

### Solution 5
Solution:

```python
import random

secret = random.randint(1, 10)
attempts = 0
print("I've picked a number from 1 to 10.")

while True:
    guess = int(input("Your number: "))
    attempts += 1
    if guess < secret:
        print("Bigger!")
    elif guess > secret:
        print("Smaller!")
    else:
        print("Correct! Number:", secret)
        print("Attempts:", attempts)
        break
```

Example game:

```
I've picked a number from 1 to 10.
Your number: 5
Bigger!
Your number: 8
Smaller!
Your number: 7
Correct! Number: 7
Attempts: 3
```

What happens here? `random.randint(1, 10)` picks a random number. The `while True` loop gives the player infinite attempts, `int(input(...))` reads and converts input into a number. The "smaller/bigger" conditions give feedback — it's a "smart" game that helps the player. On a guess, `break` ends the loop. The "pick → compare → give a hint" mechanic is the skeleton of almost any game, from Battleship to quests.
<!--/SOLUTION-->

<!--QUIZ-->
What does tk.Tk() do?
- Creates the main application window
- Creates a button
- Closes the application
* Correct answer: Creates the main application window
tk.Tk() is the entry point of any Tkinter application.

What does window.mainloop() do?
- Starts the event loop that keeps the window open
- Closes the window
- Creates a new window
* Correct answer: Starts the event loop that keeps the window open
mainloop() begins processing events: clicks, keys, window redraws.

What is tk.Label?
- A label (text UI element)
- An input field
- A log file
* Correct answer: A label (text UI element)
Label displays text in the window.

Which button parameter sets the click handler function?
- command=function_name
- text=function_name
- click=function_name
* Correct answer: command=function_name
On click, Tkinter calls the function passed in the command parameter.

What does entry.get() return?
- The text typed into the input field
- The window size
- The number of clicks
* Correct answer: The text typed into the input field
get() reads the current contents of an Entry field.

Which library is used to create games in Python?
- pygame
- csv
- statistics
* Correct answer: pygame
pygame provides a window, graphics, sound, and event handling for games.

What does turtle.forward(100) do?
- Moves the turtle forward 100 pixels
- Turns the turtle 100 degrees
- Draws a circle of radius 100
* Correct answer: Moves the turtle forward 100 pixels
forward() goes forward, leaving a trail.

Which library lets you make mobile apps in Python?
- Kivy
- tkinter
- urllib
* Correct answer: Kivy
Kivy lets the same code run on Android, iOS, and desktop.

What does random.randint(1, 10) do?
- Returns a random integer from 1 to 10 inclusive
- Returns a random fractional number
- Prints a random number
* Correct answer: Returns a random integer from 1 to 10 inclusive
randint(a, b) returns a random integer in the range [a, b].

What happens without mainloop() in Tkinter?
- The window may not appear or closes immediately
- The window becomes bigger
- Buttons become invisible
* Correct answer: The window may not appear or closes immediately
Without the event loop the program finishes right after creating the window.
<!--/QUIZ-->
