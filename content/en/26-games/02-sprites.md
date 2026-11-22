---
title: Sprites, movement, collisions
summary: Sprite class, keys, rect collisions.
order: 2
duration: 50 min
difficulty: intermediate
tags: sprites, collisions
---

Sprites bring objects to life.

## Sprite

```python
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
```

## Collision

```python
if pygame.sprite.spritecollide(player, enemies, False):
    print("hit!")
```

## Lesson summary

update() + rect collisions power gameplay.

<!--TASK-->
### Task 1 — Sprite
Make a Player class.

### Task 2 — Keys
Move with arrows.

### Task 3 — Group
Create a group.

### Task 4 — Draw
Draw the group.

### Task 5 — Collide
Detect collision.

### Task 6 — Wall
Stop at edges.

### Task 7 — Speed
Add a speed variable.
<!--/TASK-->

<!--HINT-->
### Hint 1
Sprite.

### Hint 2
get_pressed.

### Hint 3
Group.

### Hint 4
draw.

### Hint 5
spritecollide.

### Hint 6
Bounds.

### Hint 7
self.speed.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
```

### Solution 2
```python
def update(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        self.rect.x -= 5
    if keys[pygame.K_RIGHT]:
        self.rect.x += 5
```

### Solution 3
```python
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
```

### Solution 4
```python
all_sprites.draw(screen)
```

### Solution 5
```python
hits = pygame.sprite.spritecollide(player, enemies, False)
if hits:
    print("hit!")
```

### Solution 6
```python
if self.rect.left < 0:
    self.rect.left = 0
if self.rect.right > 800:
    self.rect.right = 800
```

### Solution 7
```python
self.speed = 5
# использовать self.rect.x += self.speed
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a sprite?
- Game object
- An event
- A color
- None
* Correct answer: Game object
Drawable.

What is rect?
- Position/size
- Image
- Event
- None
* Correct answer: Position/size
Collision.

What is update?
- Frame logic
- Draws
- Ends
- None
* Correct answer: Frame logic
Move.

What is a group?
- Sprite collection
- One sprite
- Event
- None
* Correct answer: Sprite collection
Draw.

What is get_pressed?
- Key states
- Events
- Pixels
- None
* Correct answer: Key states
List.

What is K_LEFT?
- Left arrow
- Right
- Space
- None
* Correct answer: Left arrow
Key.

What is spritecollide?
- Collision check
- Drawing
- Moving
- None
* Correct answer: Collision check
Hits.

What is a hit?
- Overlap
- Miss
- Draw
- None
* Correct answer: Overlap
Collision.

What is a boundary?
- Edge limit
- Center
- Speed
- None
* Correct answer: Edge limit
Wall.

What is x?
- Horizontal pos
- Vertical
- Speed
- None
* Correct answer: Horizontal pos
rect.

What is a surface?
- Canvas per sprite
- Event
- Clock
- None
* Correct answer: Canvas per sprite
image.

What is FPS?
- Frames per second
- Size
- Color
- None
* Correct answer: Frames per second
Smooth.
<!--/QUIZ-->
