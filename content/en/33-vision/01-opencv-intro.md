---
title: OpenCV: Basic Image Operations
summary: Reading and writing images, BGR/RGB color spaces, pixel access, resizing, cropping.
order: 1
duration: 40 min
difficulty: intermediate
tags: opencv, numpy, images, pixels
---

Computer vision is a field of artificial intelligence that teaches programs to "see": find objects and faces in images, read text, and estimate scene parameters. One of the key libraries here is OpenCV (Open Source Computer Vision), created at Intel and supporting hundreds of algorithms. In Python it is installed as the `opencv-python` package and imported as `cv2`.

## Installation and import

Install the library together with numpy and matplotlib:

```bash
pip install opencv-python numpy matplotlib
```

Import and check the version:

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

print(cv2.__version__)
```

If you saw a version number, OpenCV is ready to work.

## How OpenCV stores images

The `cv2.imread(path)` function reads a file and returns a **numpy array**. A color image is a three-dimensional array: `(height, width, channels)`. Each pixel stores three numbers from 0 to 255 (type `uint8`).

```python
img = cv2.imread("photo.jpg")
print(img.shape)      # (1080, 1920, 3) — height, width, channels
print(img.dtype)      # uint8
print(img[0, 0])      # BGR values of the top-left pixel
```

A critical detail: **OpenCV stores color in BGR order** (blue, green, red), not RGB. Most other tools — matplotlib, PIL — expect RGB. If you pass an OpenCV array straight to `plt.imshow()`, the red and blue channels swap places and the image looks "wrong". Let's see this in action:

```python
# Create a "red" 100x100 image
red_bgr = np.zeros((100, 100, 3), dtype=np.uint8)
red_bgr[:] = (0, 0, 255)   # BGR: blue=0, green=0, red=255

plt.subplot(1, 2, 1)
plt.imshow(red_bgr)              # matplotlib thinks it's RGB — it will be blue!
plt.title("Without conversion")
plt.axis("off")

# Correct: first convert BGR to RGB
red_rgb = cv2.cvtColor(red_bgr, cv2.COLOR_BGR2RGB)
plt.subplot(1, 2, 2)
plt.imshow(red_rgb)              # now a true red
plt.title("After cvtColor")
plt.axis("off")
plt.show()
```

Remember the rule: `cv2.imread` → BGR, `plt.imshow` → RGB. Between them, always do `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)`.

## Pixel access and slicing

Since an image is a numpy array, the usual indexing mechanisms work with it. Note: the first coordinate is the row (y), the second is the column (x).

```python
pixel = img[100, 200]          # pixel at row 100, column 200
img[100, 200] = (255, 0, 0)    # repaint it blue (BGR!)
channel_blue = img[:, :, 0]    # a single channel
region = img[50:150, 200:400]  # rectangular region (slice)
```

A slice is not a copy, but a "window" onto the same data. If you modify `region`, the original changes too. To get an independent copy, use `.copy()`.

## Resizing and cropping

`cv2.resize` changes the size. The size is set either explicitly or by scale factors:

```python
small = cv2.resize(img, (640, 360))            # exact width and height
half = cv2.resize(img, None, fx=0.5, fy=0.5)  # shrink by half
```

Cropping is just a slice:

```python
crop = img[100:400, 200:600]
```

## Writing and displaying

Writing to disk is `cv2.imwrite`; it returns `True` on success:

```python
ok = cv2.imwrite("out.png", crop)
print(ok)  # True
```

For display on screen in a learning environment, it's better not to use `cv2.imshow` (it needs a GUI), but to save files and open them via matplotlib:

```python
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(rgb)
plt.axis("off")
plt.show()
```

## Creating images from scratch

It is often convenient to generate test images programmatically:

```python
blank = np.zeros((300, 400, 3), dtype=np.uint8)   # black
blank[:] = (255, 255, 255)                        # fill with white
blank[50:150, 100:250] = (0, 0, 255)              # red rectangle
```

## Summary

An image in OpenCV is a numpy array in BGR format; `imread` reads, `imwrite` saves; pixels are accessed via slices `img[y1:y2, x1:x2]`; color is converted with `cvtColor`. Now let's solidify these skills with tasks.

<!--TASK-->
### Task 1
Write a function `inspect_image(path)` that reads the image from the given path, prints its shape and data type (dtype), and then saves a copy to the file `copy.png`. Don't forget to check that `cv2.imread` did not return `None` (this means the file was not found), and if the file is missing — print the message `File not found` and exit the function. Run the function on any image on your computer and make sure the copy appears next to the script.

### Task 2
Write a function `generate_grid()` that creates a synthetic 800×400 image divided into four vertical stripes of equal width: blue, green, red, and white (in BGR colors). Save the result to the file `grid.png`. Hint: create `np.zeros((400, 800, 3), dtype=np.uint8)` and fill width-wise slices. After running, open `grid.png` — there should be exactly four stripes in the specified order.

### Task 3
Write a function `flip_horizontal(img)` that mirrors the image horizontally (flips it left-to-right) **without** `cv2.flip` — only with numpy and slices. Check the result: save both versions (original and flipped) to files `original.png` and `flipped.png`. In the function, be sure to use `[:: -1]` along the needed axis. Make sure the flipped picture looks like a mirror reflection of the original.

### Task 4
Write a function `crop_center(img, width, height)` that returns the central part of the image of the given size. If the requested size is larger than the original — return the original unchanged. Also write **pytest tests**: check that the result shape equals `(height, width, 3)` for even and odd sizes, that the result for too large a size equals the original, and that the slice is indeed taken from the center. Run `pytest` and make sure all tests pass.

### Task 5
Write a function `to_gray_and_resize(img, scale)` that converts a color image to grayscale via `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)`, then shrinks it `scale` times via `cv2.resize` with scale factors `fx=scale, fy=scale`. The function returns the resulting grayscale array. Write **pytest tests**: check that the result is two-dimensional (height, width), that its dtype is `uint8`, and that the result height is approximately `round(original_height * scale)`. Run the tests and prove everything works.
<!--/TASK-->

<!--HINT-->
### Hint 1
Read the image like this: `img = cv2.imread(path)`, then `if img is None: print("File not found"); return`. For the copy, simply call `cv2.imwrite("copy.png", img)`. The shape is printed as `print(img.shape)`, the type as `print(img.dtype)`.

### Hint 2
Create the array `grid = np.zeros((400, 800, 3), dtype=np.uint8)`. Half the width is 400 pixels. Fill the slices: `grid[:, 0:200] = (255, 0, 0)` — blue, `grid[:, 200:400] = (0, 255, 0)` — green, `grid[:, 400:600] = (0, 0, 255)` — red, `grid[:, 600:800] = (255, 255, 255)` — white. Save with `cv2.imwrite`.

### Hint 3
Horizontal mirroring means reversing the slices along the width axis: `img[:, ::-1]`. Return the new array `img[:, ::-1]` — numpy creates a copy of the data with such a slice. Save both images with separate `cv2.imwrite` calls.

### Hint 4
Compute the center: `h, w = img.shape[:2]`, then `x1 = (w - width) // 2`, `y1 = (h - height) // 2`, and return `img[y1:y1+height, x1:x1+width]`. If `width > w` or `height > h` — return `img`. For tests, create small arrays via `np.zeros((100, 200, 3), dtype=np.uint8)`.

### Hint 5
Inside the function: `gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)`, then `resized = cv2.resize(gray, None, fx=scale, fy=scale)`. In tests, compare the height with `round(img.shape[0] * scale)`. Remember: `np.uint8` is the dtype of the result, `len(resized.shape) == 2` is the two-dimensionality check.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
import cv2

def inspect_image(path):
    img = cv2.imread(path)
    if img is None:
        print("File not found")
        return
    print(img.shape)
    print(img.dtype)
    cv2.imwrite("copy.png", img)

inspect_image("photo.jpg")
```

Result:

```
(1080, 1920, 3)
uint8
```

What's going on here? `cv2.imread` returns `None` if the file is missing or corrupted — the `img is None` check protects us from errors below. `shape` describes the array dimensions, `dtype` the data type. The line `cv2.imwrite("copy.png", img)` writes a copy and returns `True` on success. Note: `imwrite` determines the format by the file extension, so `.png` in the name gives a PNG file.

### Solution 2
Solution:

```python
import cv2
import numpy as np

def generate_grid():
    grid = np.zeros((400, 800, 3), dtype=np.uint8)
    grid[:, 0:200] = (255, 0, 0)    # blue
    grid[:, 200:400] = (0, 255, 0)  # green
    grid[:, 400:600] = (0, 0, 255)  # red
    grid[:, 600:800] = (255, 255, 255)  # white
    cv2.imwrite("grid.png", grid)

generate_grid()
```

What's going on here? `np.zeros((400, 800, 3), dtype=np.uint8)` creates a black 400×800 image with three channels. Each slice `grid[:, a:b]` captures all rows and the columns from `a` to `b` — the range of one stripe. Assigning the tuple `(B, G, R)` paints the whole region with a single color. The stripes run left to right because columns grow left to right.

### Solution 3
Solution:

```python
import cv2

def flip_horizontal(img):
    return img[:, ::-1]

img = cv2.imread("photo.jpg")
cv2.imwrite("original.png", img)
cv2.imwrite("flipped.png", flip_horizontal(img))
```

What's going on here? The slice `img[:, ::-1]` takes all rows (first axis) and all columns in reverse order (second axis with step −1). Numpy returns a new view of the data for such a slice, so the original does not change — we get exactly the mirrored image. This is pure numpy without `cv2.flip`: the function returns an array of the same shape but with mirror-placed pixels. You can compare file sizes: `flipped.png` has the same geometry, but the picture inside is mirrored.

### Solution 4
Solution:

```python
import cv2
import numpy as np

def crop_center(img, width, height):
    h, w = img.shape[:2]
    if width > w or height > h:
        return img
    x1 = (w - width) // 2
    y1 = (h - height) // 2
    return img[y1:y1 + height, x1:x1 + width]
```

Tests:

```python
def test_crop_center_shape():
    img = np.zeros((100, 200, 3), dtype=np.uint8)
    out = crop_center(img, 50, 40)
    assert out.shape == (40, 50, 3)

def test_crop_center_odd():
    img = np.zeros((101, 201, 3), dtype=np.uint8)
    out = crop_center(img, 51, 41)
    assert out.shape == (41, 51, 3)

def test_crop_center_too_large():
    img = np.zeros((10, 10, 3), dtype=np.uint8)
    out = crop_center(img, 50, 50)
    assert out.shape == (10, 10, 3)

def test_crop_center_center_pixel():
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    img[50, 50] = (255, 0, 0)
    out = crop_center(img, 10, 10)
    assert out[5, 5].tolist() == [255, 0, 0]
```

What's going on here? The function computes the coordinates of the top-left corner of the central rectangle as `(w - width) // 2` and `(h - height) // 2` — integer division guarantees we don't go out of bounds for odd sizes. The check `width > w or height > h` guards against slices larger than the original image. The fourth test confirms the slice is taken from the center: pixel `(50, 50)` is the center of a 100×100 image, and in a 10×10 result it must land at `(5, 5)`.

### Solution 5
Solution:

```python
import cv2

def to_gray_and_resize(img, scale):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.resize(gray, None, fx=scale, fy=scale)
```

Tests:

```python
import numpy as np

def test_gray_is_2d():
    img = np.random.randint(0, 256, (80, 120, 3), dtype=np.uint8)
    out = to_gray_and_resize(img, 0.5)
    assert len(out.shape) == 2

def test_gray_dtype():
    img = np.random.randint(0, 256, (80, 120, 3), dtype=np.uint8)
    out = to_gray_and_resize(img, 0.5)
    assert out.dtype == np.uint8

def test_gray_resize_shape():
    img = np.random.randint(0, 256, (80, 120, 3), dtype=np.uint8)
    out = to_gray_and_resize(img, 0.5)
    assert out.shape == (40, 60)

def test_gray_resize_custom_scale():
    img = np.random.randint(0, 256, (100, 200, 3), dtype=np.uint8)
    out = to_gray_and_resize(img, 0.25)
    assert out.shape == (25, 50)
```

What's going on here? `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)` turns a three-channel array into a two-dimensional one — each pixel becomes a single brightness value. `cv2.resize(gray, None, fx=scale, fy=scale)` shrinks the image `scale` times along both axes: with `scale=0.5`, a height of 80 becomes 40. `np.random.randint` in the tests generates a random image so we don't depend on a specific file. The tests check the function's main contracts: two-dimensionality, type, and exact result geometry.
<!--/SOLUTION-->

<!--QUIZ-->
What color order does OpenCV use by default?
- RGB
- BGR
- GRB
* Correct answer: BGR
OpenCV reads and stores images in BGR order — a common cause of "weird" colors in matplotlib.

What will cv2.imread return if the file is not found?
- None
- An empty array
- It will raise an exception
* Correct answer: None
imread returns None — check the result before using it.

What data type does an image array have?
- uint8
- float32
- int64
* Correct answer: uint8
Brightness values 0–255 are stored as 8-bit unsigned integers.

What does cv2.cvtColor(img, cv2.COLOR_BGR2RGB) do?
- Swaps the channels from BGR to RGB
- Blurs the image
- Changes the size
* Correct answer: Swaps the channels from BGR to RGB
cvtColor converts between color spaces.

How do you write an image to a file?
- cv2.imwrite("out.png", img)
- cv2.save("out.png", img)
- img.write("out.png")
* Correct answer: cv2.imwrite("out.png", img)
imwrite takes a path and an array and returns True on success.

What index does the first coordinate have in img[y, x]?
- y is the row, x is the column
- x is the row, y is the column
- The order does not matter
* Correct answer: y is the row, x is the column
In numpy arrays, the first axis is rows (height), the second is columns (width).

What does the slice img[50:150, 200:400] give?
- A rectangular region of the image
- Every 50th pixel
- A mirror of the image
* Correct answer: A rectangular region of the image
The slice selects the region from rows 50–150 and columns 200–400.

What does the expression img[:, ::-1] do?
- Mirrors the image horizontally
- Mirrors it vertically
- Rotates it by 90°
* Correct answer: Mirrors the image horizontally
Reversing the columns in reverse order flips it left-to-right.

What array does np.zeros((300, 400, 3), dtype=np.uint8) create?
- A black 300×400 image
- A white 300×400 image
- A red 400×300 image
* Correct answer: A black 300×400 image
All pixels equal zero — that is black.

Why is BGR→RGB conversion needed before plt.imshow?
- So colors display correctly
- To speed up output
- Conversion is not needed
* Correct answer: So colors display correctly
plt.imshow expects RGB, so the BGR array must be rearranged.
<!--/QUIZ-->
