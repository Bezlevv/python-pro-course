---
title: Sound, text, scoring
summary: Fonts, score, simple audio.
order: 3
duration: 45 min
difficulty: intermediate
tags: sound, text, score
---

UI text and audio polish games.

## Text

```python
font = pygame.font.Font(None, 36)
text = font.render(f"Score: {score}", True, (255, 255, 255))
screen.blit(text, (20, 20))
```

## Sound

```python
pygame.mixer.init()
sound = pygame.mixer.Sound("beep.wav")
sound.play()
```

## Lesson summary

Render text each frame; play sounds on events.

<!--TASK-->
### Task 1 — Font
Create a font.

### Task 2 — Render
Render score text.

### Task 3 — Blit
Draw it.

### Task 4 — Score
Increase on collision.

### Task 5 — Init audio
pygame.mixer.init().

### Task 6 — Play
Play a sound.

### Task 7 — Game over
Show "Game Over".
<!--/TASK-->

<!--HINT-->
### Hint 1
Font.

### Hint 2
render.

### Hint 3
blit.

### Hint 4
score +=.

### Hint 5
mixer.

### Hint 6
Sound.

### Hint 7
Center.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
font = pygame.font.Font(None, 36)
```

### Solution 2
```python
text = font.render(f"Score: {score}", True, (255, 255, 255))
```

### Solution 3
```python
screen.blit(text, (20, 20))
```

### Solution 4
```python
if hits:
    score += 1
```

### Solution 5
```python
pygame.mixer.init()
```

### Solution 6
```python
beep = pygame.mixer.Sound("beep.wav")
beep.play()
```

### Solution 7
```python
over_font = pygame.font.Font(None, 72)
over_text = over_font.render("Game Over", True, (255, 0, 0))
screen.blit(over_text, (300, 280))
```
<!--/SOLUTION-->

<!--QUIZ-->
What is font?
- Text style
- Sound
- Color
- None
* Correct answer: Text style
Render.

What is render?
- Makes image
- Plays
- Draws
- None
* Correct answer: Makes image
Text.

What is blit?
- Draws surface
- Initializes
- Plays
- None
* Correct answer: Draws surface
Copy.

What is a score?
- Number
- Image
- Sound
- None
* Correct answer: Number
Points.

What is mixer?
- Audio module
- Font
- Event
- None
* Correct answer: Audio module
Sound.

What is Sound?
- Audio file
- Text
- Surface
- None
* Correct answer: Audio file
Play.

What is play?
- Starts audio
- Stops
- Loads
- None
* Correct answer: Starts audio
Sound.

What is a wav?
- Audio format
- Image
- Font
- None
* Correct answer: Audio format
File.

What is a color?
- RGB tuple
- Size
- Font
- None
* Correct answer: RGB tuple
(255,255,255).

What is position?
- x, y
- Speed
- Score
- None
* Correct answer: x, y
Blit.

What is game over?
- End state
- Start
- Pause
- None
* Correct answer: End state
Message.

What is UI?
- Interface
- Audio
- Physics
- None
* Correct answer: Interface
Text.
<!--/QUIZ-->
