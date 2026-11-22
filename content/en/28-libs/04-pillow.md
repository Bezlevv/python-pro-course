---
title: Pillow: image processing
summary: Open, resize, save, filters.
order: 4
duration: 45 min
difficulty: intermediate
tags: pillow, images
---

Pillow edits images in Python.

## Open and info

```python
from PIL import Image

img = Image.open("photo.jpg")
print(img.size, img.mode)
```

## Resize and rotate

```python
img = img.resize((400, 300))
img = img.rotate(90)
```

## Filters

```python
from PIL import ImageFilter

blurred = img.filter(ImageFilter.GaussianBlur(radius=2))
```

## Save

```python
img.save("out.png")
```

## Lesson summary

Open → transform → save.

<!--TASK-->
### Task 1 — Open
Open an image and print size.

### Task 2 — Resize
Resize.

### Task 3 — Rotate
Rotate 90°.

### Task 4 — Crop
Crop a region.

### Task 5 — Blur
Gaussian blur.

### Task 6 — Grayscale
Convert mode.

### Task 7 — Save
Save as PNG.
<!--/TASK-->

<!--HINT-->
### Hint 1
Image.open.

### Hint 2
resize.

### Hint 3
rotate.

### Hint 4
crop.

### Hint 5
GaussianBlur.

### Hint 6
convert.

### Hint 7
save.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from PIL import Image
img = Image.open("photo.jpg")
print(img.size, img.mode)
```

### Solution 2
```python
img = img.resize((400, 300))
```

### Solution 3
```python
img = img.rotate(90)
```

### Solution 4
```python
box = (100, 100, 300, 300)
cropped = img.crop(box)
```

### Solution 5
```python
from PIL import ImageFilter
blurred = img.filter(ImageFilter.GaussianBlur(radius=2))
```

### Solution 6
```python
gray = img.convert("L")
```

### Solution 7
```python
img.save("out.png")
```
<!--/SOLUTION-->

<!--QUIZ-->
What is Pillow?
- Image library
- Video
- Audio
- None
* Correct answer: Image library
PIL.

What is open?
- Loads file
- Creates
- Saves
- None
* Correct answer: Loads file
Image.

What is size?
- Width/height
- Color
- Mode
- None
* Correct answer: Width/height
Tuple.

What is mode?
- Color type
- Size
- Format
- None
* Correct answer: Color type
RGB/L.

What is resize?
- Scales
- Rotates
- Crops
- None
* Correct answer: Scales
New size.

What is rotate?
- Turns
- Scales
- Filters
- None
* Correct answer: Turns
Degrees.

What is crop?
- Cuts region
- Resizes
- Rotates
- None
* Correct answer: Cuts region
Box.

What is a box?
- (left, top, right, bottom)
- Size
- Color
- None
* Correct answer: (left, top, right, bottom)
Crop.

What is filter?
- Effect
- Save
- Resize
- None
* Correct answer: Effect
Blur.

What is GaussianBlur?
- Soft blur
- Sharpen
- Grayscale
- None
* Correct answer: Soft blur
Filter.

What is convert?
- Changes mode
- Resizes
- Crops
- None
* Correct answer: Changes mode
"L".

What is save?
- Writes file
- Opens
- Closes
- None
* Correct answer: Writes file
Format.
<!--/QUIZ-->
