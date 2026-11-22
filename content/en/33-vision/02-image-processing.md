---
title: Filters, Morphology, and Contours
summary: Blurring, threshold binarization, morphological operations, and object contour detection.
order: 2
duration: 45 min
difficulty: intermediate
tags: opencv, filters, morphology, contours
---

In the last lesson we learned to read images and work with pixels. But real tasks (object search, recognition, segmentation) require preparing the image: removing noise, turning the picture into black and white, and finding object boundaries. That's what we'll do now.

## Noise and filtering

Any image from a camera contains noise — random bright or dark dots. Filters average neighboring pixels and smooth the picture.

```python
import cv2

img = cv2.imread("photo.jpg")

# Simple averaging over a 5x5 window
blurred = cv2.blur(img, (5, 5))

# Gaussian blur — weighted average, preserves edges more softly
gauss = cv2.GaussianBlur(img, (5, 5), 0)

# Median filter — great at killing "salt and pepper"
median = cv2.medianBlur(img, 5)
```

The window size is an odd number (3, 5, 7...). The larger the window, the stronger the blur.

## Threshold binarization

After blurring, it's useful to turn the image into a binary one: every pixel is either 0 (black) or 255 (white). This is done with the `cv2.threshold` function:

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
```

Here the threshold is 127: lighter pixels become white, darker ones black. The threshold is often hard to pick manually. Otsu's method helps — it finds the optimal threshold itself:

```python
_, binary_otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
```

For scenes with uneven lighting, `cv2.adaptiveThreshold` is better — it computes a threshold separately for each small region:

```python
adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 11, 2)
```

## Morphology

A binary image often contains "holes" inside objects and random noise specks. Morphological operations fix this by rolling a structuring element (usually a kernel of ones) over the image.

```python
import numpy as np

kernel = np.ones((5, 5), np.uint8)

# Erosion: shrinks white regions, removes small specks
eroded = cv2.erode(binary, kernel, iterations=1)

# Dilation: grows white regions, fills holes
dilated = cv2.dilate(binary, kernel, iterations=1)

# Opening = erosion + dilation: cleans white noise off the background
opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

# Closing = dilation + erosion: fills holes inside objects
closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
```

## Contours

Contours are the boundaries of white regions on a binary image. `cv2.findContours` returns a list of contours (and a hierarchy — in OpenCV 4 the function returns exactly two values):

```python
contours, hierarchy = cv2.findContours(closed, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
```

- `cv2.RETR_EXTERNAL` — only external contours, without nested holes;
- `cv2.CHAIN_APPROX_SIMPLE` — compresses the contour, keeping only corners.

Each contour is an array of points. Let's draw them on a copy of the original:

```python
out = img.copy()
cv2.drawContours(out, contours, -1, (0, 255, 0), 3)
```

For each contour you can get a bounding rectangle and an area:

```python
for c in contours:
    x, y, w, h = cv2.boundingRect(c)   # rectangle coordinates and size
    area = cv2.contourArea(c)          # contour area in pixels
```

This is exactly the data needed to count objects, filter out small debris by area, and draw boxes around found items.

## Summary

The image processing pipeline usually looks like this: `imread` → blur → binarization (threshold) → morphology → `findContours` → contour analysis. Let's reinforce this with tasks.

<!--TASK-->
### Task 1
Write a function `denoise(path, ksize=5)` that reads an image, applies `cv2.GaussianBlur` with a `(ksize, ksize)` window, and saves the result to the file `denoised.png`. Print the dimensions of the original and resulting images. Check: the array shape must not change after blurring, and the blurred file must appear on disk.

### Task 2
Write a function `binarize(path)` that reads an image, converts it to gray, and applies the Otsu threshold (`cv2.THRESH_BINARY + cv2.THRESH_OTSU`). Save the binary image to `binary.png`. Additionally, compute and print what percentage of pixels became white (255). Formula: `np.count_nonzero(binary) / binary.size * 100`.

### Task 3
Write a function `morph_clean(binary)` that takes a binary image, applies opening (MORPH_OPEN) and closing (MORPH_CLOSE) with the kernel `np.ones((5, 5), np.uint8)`, and returns the cleaned image. Save it to `cleaned.png`. At the end, print the number of white pixels before and after processing — it should be either smaller or roughly the same.

### Task 4
Write a function `preprocess_bin(img, kernel_size=5)` that performs full image preparation: Gaussian blur with a `(kernel_size, kernel_size)` window, conversion to gray, Otsu binarization, opening, and closing. The function returns the ready binary image. Write **pytest tests**: check that the result is two-dimensional, has dtype `uint8`, contains only the values 0 and 255, and for a fully black (or white) image returns an array of only zeros. Run the tests.

### Task 5
Write a function `largest_contour_bbox(binary)` that finds the largest contour by area on a binary image (via `cv2.findContours` and `cv2.contourArea`) and returns its bounding rectangle as a tuple `(x, y, w, h)`. If there are no contours — return `None`. Write **pytest tests**: on an image with a single white 80×80 square on the left, the rectangle must be `(10, 10, 80, 80)`; on a fully black image the function must return `None`. Run the tests.
<!--/TASK-->

<!--HINT-->
### Hint 1
Blurring does not change the shape: `img.shape == blurred.shape`. To save, use `cv2.imwrite("denoised.png", blurred)`. Print the dimensions with `print(img.shape, blurred.shape)`.

### Hint 2
First `gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)`, then `_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)`. White percentage: `np.count_nonzero(binary) / binary.size * 100`.

### Hint 3
Opening: `cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)`, closing: `cv2.morphologyEx(..., cv2.MORPH_CLOSE, kernel)`. Counting white pixels before and after — `np.count_nonzero()`.

### Hint 4
Chain the steps: `blur = cv2.GaussianBlur(img, (k, k), 0)` → `gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)` → `_, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)` → opening and closing with `np.ones((k, k), np.uint8)`. In tests, create `np.zeros((50, 50), dtype=np.uint8)`.

### Hint 5
`contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)`. If the list is empty — `return None`. Otherwise iterate over the contours, compare `cv2.contourArea(c)`, remember the maximum, then `cv2.boundingRect(best)`. For the square test, create a white rectangle on a black background via slice assignment.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
import cv2

def denoise(path, ksize=5):
    img = cv2.imread(path)
    blurred = cv2.GaussianBlur(img, (ksize, ksize), 0)
    cv2.imwrite("denoised.png", blurred)
    print(img.shape, blurred.shape)

denoise("photo.jpg")
```

Result:

```
(1080, 1920, 3) (1080, 1920, 3)
```

What's going on here? `cv2.GaussianBlur` blurs the image using a Gaussian kernel of size `(ksize, ksize)` — the third argument (standard deviation) is passed as 0, and OpenCV computes it from the window size itself. The window size must be odd, otherwise OpenCV raises an exception. The array shape does not change: the filter processes each pixel by recomputing it from its neighbors, but the geometry stays the same.

### Solution 2
Solution:

```python
import cv2
import numpy as np

def binarize(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255,
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite("binary.png", binary)
    white = np.count_nonzero(binary) / binary.size * 100
    print(f"White pixels: {white:.1f}%")

binarize("photo.jpg")
```

What's going on here? Otsu's method works like this: OpenCV tries all possible thresholds and picks the one at which the variance between the black and white classes is maximal. So we don't need the numeric threshold value (the first returned parameter) — we ignore it via `_`. The percentage of white pixels is computed with `np.count_nonzero` — it returns the number of nonzero elements (and white is 255). It's convenient to print the result with one decimal place using an f-string.

### Solution 3
Solution:

```python
import cv2
import numpy as np

def morph_clean(binary):
    kernel = np.ones((5, 5), np.uint8)
    opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    cleaned = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
    cv2.imwrite("cleaned.png", cleaned)
    before = np.count_nonzero(binary)
    after = np.count_nonzero(cleaned)
    print(f"Before: {before}, after: {after}")
    return cleaned
```

What's going on here? Opening (erosion, then dilation) erases small white specks from the background, while closing (dilation, then erosion) fills dark holes inside objects. Both operations use the same kernel. The number of white pixels usually decreases because opening removes debris; if objects contained many holes, closing may compensate for that — that's why the task says "either smaller or roughly the same". Such a cleaned binary layer is ideal for contour detection.

### Solution 4
Solution:

```python
import cv2
import numpy as np

def preprocess_bin(img, kernel_size=5):
    blur = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 0, 255,
                          cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    opened = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
    return cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
```

Tests:

```python
def test_preprocess_shape():
    img = np.zeros((60, 80, 3), dtype=np.uint8)
    out = preprocess_bin(img)
    assert len(out.shape) == 2
    assert out.shape == (60, 80)

def test_preprocess_dtype():
    img = np.zeros((60, 80, 3), dtype=np.uint8)
    out = preprocess_bin(img)
    assert out.dtype == np.uint8

def test_preprocess_binary_values():
    img = np.random.randint(0, 256, (60, 80, 3), dtype=np.uint8)
    out = preprocess_bin(img)
    assert set(np.unique(out)).issubset({0, 255})

def test_preprocess_black_image():
    img = np.zeros((60, 80, 3), dtype=np.uint8)
    out = preprocess_bin(img)
    assert not np.any(out)
```

What's going on here? The function assembles the full pipeline: blurring removes noise before binarization, the Otsu threshold finds the boundary itself, and morphology cleans the result. For a black image, Otsu sees only one brightness class, so the result is entirely black — this is what the fourth test checks. Importantly, `kernel_size` is used both for the blur window and for the kernel — this keeps the function consistent.

### Solution 5
Solution:

```python
import cv2
import numpy as np

def largest_contour_bbox(binary):
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    best = max(contours, key=cv2.contourArea)
    return cv2.boundingRect(best)
```

Tests:

```python
def test_largest_bbox_square():
    binary = np.zeros((100, 200), dtype=np.uint8)
    binary[10:90, 10:90] = 255
    assert largest_contour_bbox(binary) == (10, 10, 80, 80)

def test_largest_bbox_empty():
    binary = np.zeros((100, 200), dtype=np.uint8)
    assert largest_contour_bbox(binary) is None

def test_largest_bbox_picks_biggest():
    binary = np.zeros((100, 200), dtype=np.uint8)
    binary[10:30, 10:30] = 255     # small square
    binary[50:90, 120:180] = 255   # big square
    x, y, w, h = largest_contour_bbox(binary)
    assert (x, y, w, h) == (120, 50, 60, 40)
```

What's going on here? `cv2.findContours` in OpenCV 4 returns a tuple of two elements — contours and hierarchy — so we unpack `contours, _`. `max(contours, key=cv2.contourArea)` finds the contour with the maximum area. `cv2.boundingRect` returns a tuple `(x, y, w, h)` — the coordinates of the top-left corner and the rectangle dimensions. The third test shows that the function picks exactly the largest contour, not the first one found: the small 20×20 square on the left is ignored in favor of the big 60×40 one on the right.
<!--/SOLUTION-->

<!--QUIZ-->
Which filter best removes "salt and pepper" noise?
- Median (medianBlur)
- Gaussian (GaussianBlur)
- Average (blur)
* Correct answer: Median (medianBlur)
The median filter replaces a pixel with the window median and handles point noise excellently.

What does cv2.threshold return?
- A tuple (threshold, image)
- Only the image
- The number of white pixels
* Correct answer: A tuple (threshold, image)
The function returns two values: the applied threshold and the binary array.

What does Otsu's method do?
- Picks the optimal threshold itself
- Removes noise
- Finds contours
* Correct answer: Picks the optimal threshold itself
Otsu maximizes the separability of the two brightness classes.

How is an adaptive threshold different from a regular one?
- The threshold is computed separately for regions, not for the whole image
- It works only with color images
- It is faster than the regular one
* Correct answer: The threshold is computed separately for regions, not for the whole image
adaptiveThreshold computes the threshold locally, which helps with uneven lighting.

What does erosion do?
- Shrinks white regions, removes small noise
- Grows white regions
- Blurs the image
* Correct answer: Shrinks white regions, removes small noise
Erosion "eats away" the boundaries of white objects.

What is opening (MORPH_OPEN)?
- Erosion, then dilation
- Dilation, then erosion
- Only dilation
* Correct answer: Erosion, then dilation
Opening cleans white noise off the background.

How many values does cv2.findContours return in OpenCV 4?
- 2: contours and hierarchy
- 1: only contours
- 3: contours, hierarchy, and image
* Correct answer: 2: contours and hierarchy
In the fourth version, the image is not returned.

What does cv2.boundingRect(c) return?
- (x, y, w, h) — rectangle coordinates and size
- The contour area
- The list of contour points
* Correct answer: (x, y, w, h) — rectangle coordinates and size
boundingRect gives the minimal rectangle around the contour.

What does cv2.contourArea(c) do?
- Computes the contour area in pixels
- Finds the contour center
- Draws the contour
* Correct answer: Computes the contour area in pixels
The area helps filter out small debris.

Why is morphology needed after binarization?
- To remove noise and holes without changing object geometry
- To colorize the image
- To increase resolution
* Correct answer: To remove noise and holes without changing object geometry
Morphological operations clean the binary layer before contour detection.
<!--/QUIZ-->
