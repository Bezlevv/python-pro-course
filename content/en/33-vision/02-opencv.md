---
title: OpenCV: filters and contours
summary: Blur, edges, contours.
order: 2
duration: 50 min
difficulty: intermediate
tags: opencv
---

OpenCV processes images.

## Blur

```python
import cv2
img = cv2.imread("photo.jpg")
blurred = cv2.GaussianBlur(img, (5, 5), 0)
```

## Edges

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 100, 200)
```

## Contours

```python
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(len(contours))
```

## Lesson summary

Filters smooth; Canny finds edges; contours outline objects.

<!--TASK-->
### Task 1 — Gray
Convert to grayscale.

### Task 2 — Blur
Gaussian blur.

### Task 3 — Canny
Detect edges.

### Task 4 — Contours
Find contours.

### Task 5 — Draw
Draw contours.

### Task 6 — Resize
Resize an image.

### Task 7 — Save
Save processed image.
<!--/TASK-->

<!--HINT-->
### Hint 1
cvtColor.

### Hint 2
GaussianBlur.

### Hint 3
Canny.

### Hint 4
findContours.

### Hint 5
drawContours.

### Hint 6
resize.

### Hint 7
imwrite.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```

### Solution 2
```python
blurred = cv2.GaussianBlur(img, (5, 5), 0)
```

### Solution 3
```python
edges = cv2.Canny(gray, 100, 200)
```

### Solution 4
```python
contours, _ = cv2.findContours(
    edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```

### Solution 5
```python
cv2.drawContours(img, contours, -1, (0, 255, 0), 2)
```

### Solution 6
```python
small = cv2.resize(img, (400, 300))
```

### Solution 7
```python
cv2.imwrite("out.jpg", img)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a filter?
- Image operation
- A file
- A model
- None
* Correct answer: Image operation
Blur.

What is blur?
- Smoothing
- Sharpening
- Cropping
- None
* Correct answer: Smoothing
Gaussian.

What is Canny?
- Edge detector
- Blur
- Threshold
- None
* Correct answer: Edge detector
Algorithm.

What is a contour?
- Boundary
- Color
- Pixel
- None
* Correct answer: Boundary
Outline.

What is findContours?
- Finds outlines
- Draws
- Blurs
- None
* Correct answer: Finds outlines
Edges.

What is drawContours?
- Highlights
- Finds
- Smooths
- None
* Correct answer: Highlights
Green.

What is cvtColor?
- Converts color
- Resizes
- Saves
- None
* Correct answer: Converts color
BGR→gray.

What is resize?
- Changes size
- Color
- Filters
- None
* Correct answer: Changes size
Dimensions.

What is imwrite?
- Saves image
- Loads
- Shows
- None
* Correct answer: Saves image
File.

What is a kernel?
- Filter window
- Image
- Edge
- None
* Correct answer: Filter window
5×5.

What is threshold?
- Cutoff
- Blur
- Resize
- None
* Correct answer: Cutoff
Gradient.

What is RETR_EXTERNAL?
- Outer only
- All
- None
- Tree
* Correct answer: Outer only
Mode.
<!--/QUIZ-->
