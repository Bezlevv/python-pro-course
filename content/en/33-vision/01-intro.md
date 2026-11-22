---
title: Computer vision basics
summary: Pixels, images, tasks.
order: 1
duration: 40 min
difficulty: intermediate
tags: vision
---

Computer vision understands images.

## Tasks

- Classification: what's in the image;
- Detection: where objects are;
- Segmentation: pixel-level masks.

## Pixels

Images are grids of numbers.

## Python tools

OpenCV, Pillow, PyTorch.

## Lesson summary

Vision = pixels + models.

<!--TASK-->
### Task 1 — Pixel
Describe a grayscale pixel.

### Task 2 — RGB
Describe an RGB pixel.

### Task 3 — Tasks
List three vision tasks.

### Task 4 — Tools
Name two libraries.

### Task 5 — Load
Load an image with OpenCV.

### Task 6 — Shape
Print height/width/channels.

### Task 7 — Threshold
Binary threshold.
<!--/TASK-->

<!--HINT-->
### Hint 1
Number.

### Hint 2
Triple.

### Hint 3
Classify.

### Hint 4
OpenCV.

### Hint 5
cv2.imread.

### Hint 6
shape.

### Hint 7
threshold.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```text
Серый пиксель — одно число яркости (0–255)
```

### Solution 2
```text
RGB-пиксель — три числа: красный, зелёный, синий
```

### Solution 3
```text
Классификация, детекция объектов, сегментация
```

### Solution 4
```text
OpenCV, Pillow, scikit-image, PyTorch
```

### Solution 5
```python
import cv2
img = cv2.imread("photo.jpg")
```

### Solution 6
```python
h, w, ch = img.shape
print(h, w, ch)
```

### Solution 7
```python
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a pixel?
- Image dot
- A file
- A model
- None
* Correct answer: Image dot
Number.

What is RGB?
- Three channels
- One
- Four
- None
* Correct answer: Three channels
Color.

What is grayscale?
- One channel
- Three
- Zero
- None
* Correct answer: One channel
Brightness.

What is classification?
- Category
- Location
- Mask
- None
* Correct answer: Category
What.

What is detection?
- Location
- Category only
- Mask
- None
* Correct answer: Location
Boxes.

What is segmentation?
- Pixel masks
- Boxes
- Category
- None
* Correct answer: Pixel masks
Level.

What is OpenCV?
- Vision library
- Database
- Browser
- None
* Correct answer: Vision library
cv2.

What is imread?
- Loads image
- Saves
- Shows
- None
* Correct answer: Loads image
File.

What is shape?
- Dimensions
- Color
- Size only
- None
* Correct answer: Dimensions
HWC.

What is threshold?
- Binary split
- Blur
- Resize
- None
* Correct answer: Binary split
127.

What is a channel?
- Color component
- Pixel
- Row
- None
* Correct answer: Color component
R/G/B.

What is BGR?
- OpenCV order
- RGB
- Gray
- None
* Correct answer: OpenCV order
Blue first.
<!--/QUIZ-->
