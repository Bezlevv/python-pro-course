---
title: Project: Snake game
summary: Full game from scratch.
order: 4
duration: 55 min
difficulty: advanced
tags: project, game, snake
---

Build Snake with movement, food, growth.

## Core elements

- Grid movement;
- Food spawning;
- Snake growth;
- Collision end.

## Sketch

```python
import pygame
from random import randint

pygame.init()
size = width, height = 400, 400
cell = 20
screen = pygame.display.set_mode(size)

snake = [(100, 100)]
direction = (cell, 0)
food = (randint(0, 19) * cell, randint(0, 19) * cell)
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != (0, cell):
        direction = (0, -cell)
    # ... остальные направления

    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, head)
    if head == food:
        food = (randint(0, 19) * cell, randint(0, 19) * cell)
    else:
        snake.pop()

    screen.fill((0, 0, 0))
    for segment in snake:
        pygame.draw.rect(screen, (0, 255, 0),
                         (segment[0], segment[1], cell, cell))
    pygame.draw.rect(screen, (255, 0, 0),
                     (food[0], food[1], cell, cell))
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
```

## Lesson summary

Snake: state + input + drawing.

<!--TASK-->
### Task 1 — Grid
Set cell size 20.

### Task 2 — Snake
Store segments list.

### Task 3 — Direction
Change on keys.

### Task 4 — Move
Add head, remove tail.

### Task 5 — Food
Spawn randomly.

### Task 6 — Grow
Eat → keep tail.

### Task 7 — End
Stop on wall/self.
<!--/TASK-->

<!--HINT-->
### Hint 1
cell.

### Hint 2
List.

### Hint 3
Keys.

### Hint 4
insert.

### Hint 5
randint.

### Hint 6
pop.

### Hint 7
Check.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
cell = 20
```

### Solution 2
```python
snake = [(100, 100)]
```

### Solution 3
```python
if keys[pygame.K_UP] and direction != (0, cell):
    direction = (0, -cell)
if keys[pygame.K_DOWN] and direction != (0, -cell):
    direction = (0, cell)
if keys[pygame.K_LEFT] and direction != (cell, 0):
    direction = (-cell, 0)
if keys[pygame.K_RIGHT] and direction != (-cell, 0):
    direction = (cell, 0)
```

### Solution 4
```python
head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
snake.insert(0, head)
```

### Solution 5
```python
from random import randint
food = (randint(0, 19) * cell, randint(0, 19) * cell)
```

### Solution 6
```python
if head == food:
    food = (randint(0, 19) * cell, randint(0, 19) * cell)
else:
    snake.pop()
```

### Solution 7
```python
if head in snake[1:] or not (0 <= head[0] < width and 0 <= head[1] < height):
    running = False
```
<!--/SOLUTION-->

<!--QUIZ-->
What is the snake?
- Segment list
- One rect
- Food
- None
* Correct answer: Segment list
State.

What is direction?
- Movement vector
- Speed
- Score
- None
* Correct answer: Movement vector
Keys.

What is head?
- First segment
- Last
- Food
- None
* Correct answer: First segment
Front.

What is insert(0)?
- Adds front
- Adds end
- Removes
- None
* Correct answer: Adds front
Move.

What is pop?
- Removes tail
- Adds
- Clears
- None
* Correct answer: Removes tail
No growth.

What is food?
- Target
- Segment
- Wall
- None
* Correct answer: Target
Spawn.

What is randint?
- Random int
- Fixed
- User input
- None
* Correct answer: Random int
Food.

What is growth?
- Keep tail
- Remove
- Shrink
- None
* Correct answer: Keep tail
Eat.

What is the wall check?
- Bounds
- Speed
- Color
- None
* Correct answer: Bounds
End.

What is self-collision?
- Hitting snake
- Wall
- Food
- None
* Correct answer: Hitting snake
End.

What is tick(10)?
- Slow speed
- Fast
- No limit
- None
* Correct answer: Slow speed
FPS.

What is a tuple?
- (x, y)
- List
- String
- None
* Correct answer: (x, y)
Segment.
<!--/QUIZ-->
