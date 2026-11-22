---
title: Pygame: first game loop
summary: Init, screen, events, draw.
order: 1
duration: 45 min
difficulty: intermediate
tags: pygame, games
---

Pygame builds 2D games.

## Loop

```python
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

## Lesson summary

Init → loop → events → draw.

<!--TASK-->
### Task 1 — Init
Initialize pygame.

### Task 2 — Screen
Create 800×600.

### Task 3 — Loop
Main loop with QUIT.

### Task 4 — Fill
Fill black.

### Task 5 — Flip
Update display.

### Task 6 — Clock
Limit 60 FPS.

### Task 7 — Quit
Clean exit.
<!--/TASK-->

<!--HINT-->
### Hint 1
pygame.init().

### Hint 2
set_mode.

### Hint 3
while.

### Hint 4
fill.

### Hint 5
flip.

### Hint 6
tick.

### Hint 7
quit().
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import pygame
pygame.init()
```

### Solution 2
```python
screen = pygame.display.set_mode((800, 600))
```

### Solution 3
```python
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
```

### Solution 4
```python
screen.fill((0, 0, 0))
```

### Solution 5
```python
pygame.display.flip()
```

### Solution 6
```python
clock = pygame.time.Clock()
clock.tick(60)
```

### Solution 7
```python
pygame.quit()
```
<!--/SOLUTION-->

<!--QUIZ-->
What is Pygame?
- Game library
- GUI toolkit
- Web
- None
* Correct answer: Game library
2D.

What is init?
- Starts modules
- Ends
- Draws
- None
* Correct answer: Starts modules
Setup.

What is set_mode?
- Window size
- Draws
- Closes
- None
* Correct answer: Window size
Surface.

What is an event?
- Input/action
- Pixel
- Shape
- None
* Correct answer: Input/action
QUIT.

What is QUIT?
- Close event
- Draw
- Move
- None
* Correct answer: Close event
X.

What is fill?
- Background color
- Draws sprite
- Flips
- None
* Correct answer: Background color
Clear.

What is flip?
- Shows frame
- Hides
- Fills
- None
* Correct answer: Shows frame
Update.

What is tick(60)?
- 60 FPS
- 60 frames only
- Speed
- None
* Correct answer: 60 FPS
Limit.

What is a clock?
- FPS control
- Time display
- Event
- None
* Correct answer: FPS control
Stable.

What is the surface?
- Draw area
- Event
- Clock
- None
* Correct answer: Draw area
Screen.

What is RGB?
- Color tuple
- Size
- Event
- None
* Correct answer: Color tuple
(0,0,0).

What is the game loop?
- Frame cycle
- One frame
- End
- None
* Correct answer: Frame cycle
Heart.
<!--/QUIZ-->
