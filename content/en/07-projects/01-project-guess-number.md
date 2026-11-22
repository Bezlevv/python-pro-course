---
title: Project: the game "Guess the number"
summary: Build a console game with random numbers, loops and input.
order: 1
duration: 45 min
difficulty: beginner
tags: project, game, random
---

Let's build a complete small game.

## Goal

The program chooses a number from 1 to 100; the player guesses.

## Plan

1. random.randint(1, 100);
2. loop: read guess, compare, tell "higher"/"lower";
3. count attempts; congratulate.

## Skeleton

```python
import random

secret = random.randint(1, 100)
attempts = 0

while True:
    guess = int(input("Your guess: "))
    attempts += 1
    if guess < secret:
        print("Higher")
    elif guess > secret:
        print("Lower")
    else:
        print(f"Great! {attempts} attempts")
        break
```

## Lesson summary

A loop + conditions + input make a real game.

<!--TASK-->
### Task 1 — Random
Generate a random number 1..100.

### Task 2 — Input
Read a guess and convert to int.

### Task 3 — Compare
Print Higher/Lower.

### Task 4 — Loop
Loop until correct.

### Task 5 — Attempts
Count and show attempts.

### Task 6 — Error handling
Handle non-integer input.

### Task 7 — Play again
Ask whether to play again.
<!--/TASK-->

<!--HINT-->
### Hint 1
random.randint(1, 100).

### Hint 2
int(input(...)).

### Hint 3
if/elif.

### Hint 4
while True + break.

### Hint 5
attempts += 1.

### Hint 6
try/except ValueError.

### Hint 7
input("again? y/n").
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import random
secret = random.randint(1, 100)
```

### Solution 2
```python
guess = int(input("Your guess: "))
```

### Solution 3
```python
if guess < secret:
    print("Higher")
elif guess > secret:
    print("Lower")
else:
    print("Correct!")
```

### Solution 4
```python
while True:
    ...
    if guess == secret:
        break
```

### Solution 5
```python
attempts = 0
# в цикле: attempts += 1
print(f"Attempts: {attempts}")
```

### Solution 6
```python
try:
    guess = int(input("Your guess: "))
except ValueError:
    print("Enter a number")
    continue
```

### Solution 7
```python
if input("Play again? (y/n): ").lower() == "y":
    # перезапуск
```
<!--/SOLUTION-->

<!--QUIZ-->
What does random.randint do?
- Random integer in range
- Random float
- Seed
- Choose
* Correct answer: Random integer in range
Inclusive.

What is input()?
- Reads a line
- Prints
- Returns int
- Errors
* Correct answer: Reads a line
String.

Why convert to int?
- Comparison needs numbers
- Style
- Required
- None
* Correct answer: Comparison needs numbers
Input string.

What is while True?
- Infinite loop
- One pass
- Error
- None
* Correct answer: Infinite loop
With break.

What does break do?
- Exits the loop
- Continues
- Restarts
- Prints
* Correct answer: Exits the loop
End.

What is an attempt counter?
- attempts += 1
- len
- sum
- None
* Correct answer: attempts += 1
Increment.

How to handle bad input?
- try/except
- if/else only
- print
- pass
* Correct answer: try/except
ValueError.

What is "Higher"?
- Hint
- Error
- Win
- None
* Correct answer: Hint
Guidance.

What is secret?
- Hidden number
- Guess
- Attempts
- Input
* Correct answer: Hidden number
Target.

What is the win condition?
- guess == secret
- guess < secret
- attempts
- None
* Correct answer: guess == secret
Equal.

Why loop until break?
- Unknown attempts
- One try
- Fixed
- None
* Correct answer: Unknown attempts
Repeat.

What is a game loop?
- Main repeat
- A screen
- A save
- None
* Correct answer: Main repeat
Core.
<!--/QUIZ-->
