---
title: Descriptors, Matching, and Faces
summary: Keypoints of images (ORB, SIFT), template matching with matchTemplate, face detection with Haar cascades.
order: 3
duration: 50 min
difficulty: advanced
tags: opencv, orb, sift, faces, templates
---

We have learned to prepare images and find contours. But how do we find a **specific object** — for example, a logo in a photo or a person's face? For that we need descriptors — numeric "fingerprints" of characteristic image points.

## Keypoints and descriptors

A keypoint is a pixel that stands out from its neighbors: a corner, a bright spot, an edge intersection. Good keypoints should be stable under changes of scale, rotation, and lighting. For each point, the algorithm computes a **descriptor** — a vector of numbers describing its neighborhood. If the descriptors of two images match, these are most likely the same scene point.

### ORB

ORB is a fast, free algorithm. It is created via `cv2.ORB_create()`:

```python
import cv2

orb = cv2.ORB_create(nfeatures=500)
keypoints, descriptors = orb.detectAndCompute(img, None)
```

`detectAndCompute` returns a list of keypoints and an array of descriptors. Each ORB descriptor is a vector of 32 bytes. Let's draw the points:

```python
vis = cv2.drawKeypoints(img, keypoints, None, color=(0, 255, 0))
cv2.imwrite("orb.png", vis)
```

### SIFT

SIFT is a more accurate but heavier algorithm. It used to be patented, but the patent expired, and now `cv2.SIFT_create()` works without issues:

```python
sift = cv2.SIFT_create()
keypoints, descriptors = sift.detectAndCompute(img, None)
```

For SIFT, a descriptor is a vector of 128 `float32` numbers.

## Matching descriptors

To find the same object in two images, we match their descriptors. The best tool for this is `cv2.BFMatcher` (brute force: compares every descriptor with every other):

```python
bf = cv2.BFMatcher(cv2.NORM_HAMMING)  # for ORB — Hamming distance
matches = bf.knnMatch(des1, des2, k=2)
```

To filter out bad matches, Lowe's rule is used: take the two best candidates for each point and keep only those where the best is noticeably better than the second:

```python
good = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good.append(m)
```

## Template matching with matchTemplate

Sometimes the object is known in advance — for example, there is a small template image. Then, instead of keypoints, `cv2.matchTemplate` is used, which "rolls" the template over the whole image and looks for the place of maximum similarity:

```python
result = cv2.matchTemplate(scene, template, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
top_left = max_loc
```

`TM_CCOEFF_NORMED` gives values from −1 to 1, where 1 is a perfect match. The location of the maximum is the top-left corner of the found template.

## Face detection: Haar cascades

To find faces, computer vision uses trained classifiers. OpenCV ships ready-made cascades in the `cv2.data` folder:

```python
cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
```

`detectMultiScale` returns a list of rectangles `(x, y, w, h)`. `scaleFactor` — how much the window scale changes at each step (smaller is more accurate but slower); `minNeighbors` — how many neighboring detections are needed to confirm a face (more means fewer false positives). Cascades work faster on black-and-white images:

```python
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
```

## Summary

Descriptors (ORB/SIFT) answer the question "which points are characteristic of an image and what they look like", `matchTemplate` finds a known template, and Haar cascades are trained detectors for specific objects such as faces. Now for practice.

<!--TASK-->
### Task 1
Write a function `orb_keypoints(path)` that reads an image, finds keypoints with the ORB algorithm (`cv2.ORB_create(nfeatures=300)`), and saves the image with the drawn points to the file `orb.png`. Print the number of found points. Check that the function works without errors for any color image.

### Task 2
Write a function `sift_keypoints(path)` that does the same, but via `cv2.SIFT_create()`, and saves the result to `sift.png`. Print the number of points and the descriptor array shape. Make sure the descriptors have shape `(N, 128)` and type `float32`.

### Task 3
Write a function `match_template(scene_path, template_path)` that finds a template on a scene via `cv2.matchTemplate` with `cv2.TM_CCOEFF_NORMED`, finds the maximum point via `cv2.minMaxLoc`, and returns a tuple `(x, y, w, h)` — the coordinates of the top-left corner and the template dimensions. Additionally, save the scene with the drawn rectangle to `matched.png`. If the maximum similarity is below 0.5 — return `None`.

### Task 4
Write a function `extract_descriptors(path, algorithm="orb")` that returns a tuple `(keypoints, descriptors)` for ORB or SIFT depending on the argument. Write **pytest tests**: check that for ORB the descriptor type is `uint8`, for SIFT it is `float32`, that the number of keypoints equals the number of descriptor rows, and that for a 10×10 image at least one descriptor is found. Run the tests.

### Task 5
Write a function `detect_faces(path)` that uses `cv2.CascadeClassifier` with `haarcascade_frontalface_default.xml`, detects faces on a gray image, and returns a list of rectangles `(x, y, w, h)`. Write **pytest tests**: check that on an image without faces (for example, fully white) the result is an empty list, and on an image with a drawn "face" (a white ellipse on a black background) at least one rectangle is returned, with all its dimensions positive. Run the tests.
<!--/TASK-->

<!--HINT-->
### Hint 1
Create the detector: `orb = cv2.ORB_create(nfeatures=300)`, then `keypoints, descriptors = orb.detectAndCompute(img, None)`. Drawing: `vis = cv2.drawKeypoints(img, keypoints, None, color=(0, 255, 0))`. Count: `len(keypoints)`.

### Hint 2
SIFT: `sift = cv2.SIFT_create()`, then proceed as with ORB. Descriptor shape — `descriptors.shape`, type — `descriptors.dtype`. Compare with the expected `(N, 128)` and `float32`.

### Hint 3
`result = cv2.matchTemplate(scene, template, cv2.TM_CCOEFF_NORMED)`, then `min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)`. If `max_val < 0.5` — return `None`. Otherwise the rectangle: `(max_loc[0], max_loc[1], template.shape[1], template.shape[0])`.

### Hint 4
If `algorithm == "orb"` — `cv2.ORB_create()`, otherwise `cv2.SIFT_create()`. In tests, create a synthetic image with contrast corners, e.g. `np.random.randint(0, 256, (100, 100), dtype=np.uint8)`. The length of `keypoints` must equal `descriptors.shape[0]`.

### Hint 5
Cascade: `cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")`. For the "face", draw a white ellipse on a black image: `cv2.ellipse(img, center, axes, 0, 0, 360, 255, -1)`. `detectMultiScale` parameters: `scaleFactor=1.1, minNeighbors=3`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
import cv2

def orb_keypoints(path):
    img = cv2.imread(path)
    orb = cv2.ORB_create(nfeatures=300)
    keypoints, _ = orb.detectAndCompute(img, None)
    vis = cv2.drawKeypoints(img, keypoints, None, color=(0, 255, 0))
    cv2.imwrite("orb.png", vis)
    print(f"ORB points: {len(keypoints)}")

orb_keypoints("photo.jpg")
```

Result:

```
ORB points: 300
```

What's going on here? `cv2.ORB_create(nfeatures=300)` creates a detector limited to 300 points. `detectAndCompute` finds points and computes their descriptors in a single call. `cv2.drawKeypoints` draws green circles at the found locations. ORB is a fast algorithm, so it suits real-time video.

### Solution 2
Solution:

```python
import cv2

def sift_keypoints(path):
    img = cv2.imread(path)
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(img, None)
    vis = cv2.drawKeypoints(img, keypoints, None, color=(0, 0, 255))
    cv2.imwrite("sift.png", vis)
    print(f"SIFT points: {len(keypoints)}")
    print(f"Descriptor shape: {descriptors.shape}, dtype: {descriptors.dtype}")

sift_keypoints("photo.jpg")
```

Result:

```
SIFT points: 1287
Descriptor shape: (1287, 128), dtype: float32
```

What's going on here? SIFT describes each point with a vector of 128 floating-point numbers — so comparing such descriptors takes more memory but gives high accuracy. Shape `(N, 128)` means: N rows — one per point, 128 columns — descriptor components. We'll verify this shape in the tests of the next task.

### Solution 3
Solution:

```python
import cv2

def match_template(scene_path, template_path):
    scene = cv2.imread(scene_path)
    template = cv2.imread(template_path)
    result = cv2.matchTemplate(scene, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if max_val < 0.5:
        return None
    x, y = max_loc
    w, h = template.shape[1], template.shape[0]
    cv2.rectangle(scene, (x, y), (x + w, y + h), (0, 255, 0), 3)
    cv2.imwrite("matched.png", scene)
    return (x, y, w, h)
```

What's going on here? `cv2.matchTemplate` slides the template over the scene and computes a correlation coefficient for each position. `cv2.minMaxLoc` returns the minimum and maximum with their coordinates. `TM_CCOEFF_NORMED` normalizes the result to the range [−1, 1], so the 0.5 threshold is a reasonable boundary for "similar enough". The coordinates of `max_loc` are the top-left corner of the found fragment, and the width and height come from the template.

### Solution 4
Solution:

```python
import cv2

def extract_descriptors(path, algorithm="orb"):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if algorithm == "orb":
        detector = cv2.ORB_create()
    else:
        detector = cv2.SIFT_create()
    return detector.detectAndCompute(img, None)
```

Tests:

```python
import numpy as np

def test_orb_dtype():
    img = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
    cv2.imwrite("tmp.png", img)
    kps, des = extract_descriptors("tmp.png", "orb")
    assert des.dtype == np.uint8

def test_sift_dtype():
    img = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
    cv2.imwrite("tmp.png", img)
    kps, des = extract_descriptors("tmp.png", "sift")
    assert des.dtype == np.float32
    assert des.shape[1] == 128

def test_keypoints_match_rows():
    img = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
    cv2.imwrite("tmp.png", img)
    kps, des = extract_descriptors("tmp.png", "orb")
    assert len(kps) == des.shape[0]

def test_finds_keypoints():
    img = np.zeros((100, 100), dtype=np.uint8)
    img[10:40, 10:40] = 255
    img[60:90, 60:90] = 128
    cv2.imwrite("tmp.png", img)
    kps, des = extract_descriptors("tmp.png", "orb")
    assert len(kps) >= 1
```

What's going on here? We read the image directly in gray (`cv2.IMREAD_GRAYSCALE`) because descriptors don't need color. The tests check the main contracts: the descriptor data type differs between ORB (`uint8`) and SIFT (`float32`), the number of descriptor rows matches the number of points, and at least one point is found on an image with sharp contrast blocks. A random image (`np.random.randint`) guarantees many keypoints: noise is nothing but contrast transitions.

### Solution 5
Solution:

```python
import cv2

def detect_faces(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)
    return [tuple(f) for f in faces]
```

Tests:

```python
def test_no_faces():
    img = np.full((100, 100, 3), 255, dtype=np.uint8)
    cv2.imwrite("tmp_blank.png", img)
    assert detect_faces("tmp_blank.png") == []

def test_fake_face():
    img = np.zeros((200, 200, 3), dtype=np.uint8)
    cv2.ellipse(img, (100, 100), (40, 50), 0, 0, 360, (255, 255, 255), -1)
    cv2.imwrite("tmp_face.png", img)
    faces = detect_faces("tmp_face.png")
    assert len(faces) >= 1
    x, y, w, h = faces[0]
    assert x >= 0 and y >= 0 and w > 0 and h > 0
```

What's going on here? A Haar cascade is a trained classifier that checks many rectangular features at different scales. `scaleFactor=1.1` means the window grows by 10% at each step; `minNeighbors=3` means a face counts only if at least three neighboring windows confirm it. A white ellipse on a black background imitates a face: dark background, a light oval region with soft boundaries. The cascade was trained on real faces, so the result for an ellipse can be non-deterministic — but the "at least one rectangle" requirement usually holds thanks to the shape.
<!--/SOLUTION-->

<!--QUIZ-->
What is a descriptor?
- A vector of numbers describing the neighborhood of a keypoint
- A point coordinate
- The image itself
* Correct answer: A vector of numbers describing the neighborhood of a keypoint
A descriptor is a numeric "fingerprint" of a point, used to compare it across different images.

What is the data type of ORB descriptors?
- uint8
- float32
- int64
* Correct answer: uint8
ORB uses compact binary descriptors of 32 bytes.

What is the data type of SIFT descriptors?
- float32
- uint8
- bool
* Correct answer: float32
SIFT produces a vector of 128 floating-point numbers.

Which algorithm is faster — ORB or SIFT?
- ORB
- SIFT
- The same
* Correct answer: ORB
ORB is optimized for speed; SIFT is heavier but more accurate.

What metric should be used to compare ORB descriptors?
- Hamming distance
- Euclidean distance
- Cosine similarity
* Correct answer: Hamming distance
Since ORB descriptors are binary vectors, they are compared with NORM_HAMMING.

Which function searches for a template in an image?
- cv2.matchTemplate
- cv2.findContours
- cv2.matchFeatures
* Correct answer: cv2.matchTemplate
matchTemplate slides the template and returns a similarity map.

What does cv2.minMaxLoc return?
- Minimum, maximum, and their coordinates
- Only the maximum
- A list of points
* Correct answer: Minimum, maximum, and their coordinates
minMaxLoc gives 4 values: min_val, max_val, min_loc, max_loc.

What does detectMultiScale do in Haar cascades?
- Returns a list of rectangles with faces
- Blurs the image
- Finds contours
* Correct answer: Returns a list of rectangles with faces
detectMultiScale scans the image at different scales.

What does the minNeighbors parameter mean?
- How many neighboring windows must confirm the object
- The minimum face size
- The number of objects
* Correct answer: How many neighboring windows must confirm the object
More minNeighbors means fewer false positives.

What will matchTemplate with TM_CCOEFF_NORMED return on a perfect match?
- 1.0
- 0.0
- 255
* Correct answer: 1.0
Normalized correlation reaches 1 on a complete match.
<!--/QUIZ-->
