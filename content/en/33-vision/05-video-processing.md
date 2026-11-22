---
title: Video Processing
summary: Reading video with VideoCapture, frame processing, writing results with VideoWriter, stream metrics.
order: 5
duration: 45 min
difficulty: advanced
tags: opencv, video, videocapture, videowriter
---

An image is a single frame, and a video is a sequence of frames that we process in a loop. OpenCV can read video both from files and from a webcam, and can write the processing result into a new video file.

## Reading video

`cv2.VideoCapture` opens a video file or a camera (a device ordinal number, e.g. `0`):

```python
import cv2

cap = cv2.VideoCapture("input.mp4")
if not cap.isOpened():
    print("Could not open video")
    exit()
```

Stream properties are obtained via `cap.get()` with constants:

```python
fps = cap.get(cv2.CAP_PROP_FPS)        # frames per second
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frames_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # total frames
print(fps, width, height, frames_count)
```

## Reading frames

Frames are read in a loop with the `cap.read()` method, which returns a tuple: the success flag `ret` and the frame itself (a BGR numpy array):

```python
while True:
    ret, frame = cap.read()
    if not ret:
        break  # video ended (or an error)
    # ... process the frame ...
```

The flag `ret` becomes `False` when the video ends. That's the loop exit condition.

## Writing video

For writing you need `cv2.VideoWriter` with a codec, frame rate, and size:

```python
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # MPEG-4 codec
writer = cv2.VideoWriter("output.mp4", fourcc, fps, (width, height))
```

The codec is chosen by a four-character string: `"mp4v"` for MP4, `"XVID"` for AVI. The `write()` method adds a frame to the file, and `release()` closes the stream:

```python
writer.write(frame)   # inside the loop
writer.release()      # after the loop
```

## Processing frames

Inside the loop, we can do everything we already know with each frame: convert to gray, blur, find contours, detect objects. For example, a grayscale version of a video:

```python
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)  # VideoWriter expects 3 channels
    writer.write(gray_bgr)
```

Note: `VideoWriter` expects frames of the same width, height, and number of channels as specified at creation. That's why a gray frame is converted back to three channels before writing.

## Counting frames

A counter of processed frames is an ordinary variable:

```python
count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    count += 1
print(f"Frames processed: {count}")
```

## Reading from a camera

For a webcam, open `cv2.VideoCapture(0)`. Frames are read the same way, but the loop won't end by itself — an explicit exit is needed (for example, on pressing the `q` key):

```python
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    # show the frame in a window
    cv2.imshow("camera", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
```

## Summary

Video processing is a cyclic repetition of image processing: open a stream → read a frame → process it → write it → read the next one. Don't forget to close both streams with `release()`. Now for practice.

<!--TASK-->
### Task 1
Write a function `video_info(path)` that opens a video via `cv2.VideoCapture` and prints: FPS, width, height, and the total number of frames (properties `CAP_PROP_FPS`, `CAP_PROP_FRAME_WIDTH`, `CAP_PROP_FRAME_HEIGHT`, `CAP_PROP_FRAME_COUNT`). If the video could not be opened — print `Could not open video`. Test on any of your video files or generate a test one via VideoWriter.

### Task 2
Write a function `save_first_frame(path, out_path)` that reads exactly the first frame from a video and saves it as an image to `out_path`. Use `cap.read()` and `cv2.imwrite`. Check that the file was created and that it is indeed an image (its shape is a three-dimensional array).

### Task 3
Write a function `convert_to_gray_video(src, dst)` that reads the video `src`, converts each frame to gray (then back to BGR for writing), and saves the result to `dst` with the same FPS and frame size. Print how many frames were processed. Run it on a short test video.

### Task 4
Write a function `process_frame(frame, mode)` that processes one frame: with `mode="gray"` it returns a gray frame converted back to 3 channels; with `mode="blur"` — the result of `cv2.GaussianBlur(frame, (5, 5), 0)`; with any other value — the original frame. Write **pytest tests**: check that the frame shape is preserved in all modes, that the gray result has exactly 3 channels, and that an unknown mode returns the same object. Run the tests.

### Task 5
Write a function `count_frames(path)` that counts the number of frames in a video by reading them in a loop (without `CAP_PROP_FRAME_COUNT`). Write **pytest tests**: create a test video with a known number of frames (e.g., 10) via `cv2.VideoWriter`, then check that `count_frames` returns exactly that number. Run the tests.
<!--/TASK-->

<!--HINT-->
### Hint 1
Properties: `cap.get(cv2.CAP_PROP_FPS)` etc. Wrap width and height in `int()`. Opening check — `cap.isOpened()`. Don't forget `cap.release()`.

### Hint 2
`ret, frame = cap.read()` — the first call returns the first frame. Check `ret`, then `cv2.imwrite(out_path, frame)`. Frame shape — `frame.shape`.

### Hint 3
In the loop: `gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)`, then `gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)`. VideoWriter: `cv2.VideoWriter(dst, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))`. Increment the frame counter by 1 inside the loop.

### Hint 4
For gray: `gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)`, then `cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)`. For blur — `cv2.GaussianBlur(frame, (5, 5), 0)`. In tests, create a frame via `np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)`.

### Hint 5
For the test you need to create a video file: `writer = cv2.VideoWriter("test.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 30.0, (320, 240))` and write 10 frames of `np.zeros((240, 320, 3), dtype=np.uint8)` via `writer.write()`. Then call `count_frames("test.mp4")`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
import cv2

def video_info(path):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print("Could not open video")
        return
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print(f"FPS: {fps}, size: {width}x{height}, frames: {total}")
    cap.release()

video_info("input.mp4")
```

Result (example):

```
FPS: 30.0, size: 1920x1080, frames: 300
```

What's going on here? `CAP_PROP_FRAME_WIDTH` and `CAP_PROP_FRAME_HEIGHT` return floating-point numbers, so they are converted to `int`. `CAP_PROP_FRAME_COUNT` is the total number of frames (may be unavailable for some codecs). `release()` frees the stream resources — this matters so the file doesn't stay locked.

### Solution 2
Solution:

```python
import cv2

def save_first_frame(path, out_path):
    cap = cv2.VideoCapture(path)
    ret, frame = cap.read()
    if not ret:
        print("Could not read frame")
        return
    cv2.imwrite(out_path, frame)
    print(f"Frame saved: {frame.shape}")
    cap.release()

save_first_frame("input.mp4", "first_frame.png")
```

Result:

```
Frame saved: (1080, 1920, 3)
```

What's going on here? The first `cap.read()` call returns the first frame of the video. The `ret` check protects against empty videos. `cv2.imwrite` saves the frame as an ordinary image. This is how video previews are made — a single frame that's convenient to show a user without rewinding the whole file.

### Solution 3
Solution:

```python
import cv2

def convert_to_gray_video(src, dst):
    cap = cv2.VideoCapture(src)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(dst, fourcc, fps, (width, height))
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        writer.write(gray_bgr)
        count += 1
    cap.release()
    writer.release()
    print(f"Frames processed: {count}")

convert_to_gray_video("input.mp4", "gray.mp4")
```

What's going on here? The loop reads frames until `ret` becomes `False`. Each frame is converted to gray and then back to BGR — otherwise `VideoWriter`, created for three-channel frames, would not accept a two-dimensional array. The writer's parameters are the same as the source video: FPS and frame size. The counter lets you confirm that no frame was lost.

### Solution 4
Solution:

```python
import cv2

def process_frame(frame, mode):
    if mode == "gray":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    if mode == "blur":
        return cv2.GaussianBlur(frame, (5, 5), 0)
    return frame
```

Tests:

```python
import numpy as np

def test_process_gray_shape():
    frame = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    out = process_frame(frame, "gray")
    assert out.shape == (100, 100, 3)

def test_process_gray_channels():
    frame = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    out = process_frame(frame, "gray")
    assert out.shape[2] == 3

def test_process_blur_shape():
    frame = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    out = process_frame(frame, "blur")
    assert out.shape == frame.shape

def test_process_unknown_mode():
    frame = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    assert process_frame(frame, "unknown") is frame
```

What's going on here? The gray frame is converted back to three channels before returning, so `shape` is preserved in all modes — this is a key requirement for `VideoWriter`. The `test_process_unknown_mode` test checks that an unknown mode doesn't cause an error but returns the original object: `is` compares object identity, not values.

### Solution 5
Solution:

```python
import cv2

def count_frames(path):
    cap = cv2.VideoCapture(path)
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        count += 1
    cap.release()
    return count
```

Tests:

```python
import numpy as np

def make_test_video(path, frames=10):
    writer = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*"mp4v"),
                              30.0, (320, 240))
    blank = np.zeros((240, 320, 3), dtype=np.uint8)
    for _ in range(frames):
        writer.write(blank)
    writer.release()

def test_count_frames():
    make_test_video("test.mp4", 10)
    assert count_frames("test.mp4") == 10
```

What's going on here? The test generates its own video: 10 identical black frames. `count_frames` counts them by reading the stream to the end. This approach tests the real loop behavior, not just reading metadata. Note: `VideoWriter` must be closed via `release()` before another stream can open this file — otherwise the file may be incomplete.
<!--/SOLUTION-->

<!--QUIZ-->
What does cap.read() return?
- A tuple (ret, frame) — success flag and frame
- Only the frame
- The number of frames
* Correct answer: A tuple (ret, frame) — success flag and frame
ret == False means the end of the video or a read error.

How do you check that a video was opened?
- cap.isOpened()
- cap.open()
- cap.valid()
* Correct answer: cap.isOpened()
isOpened returns True if the stream is ready for reading.

How do you get a video's FPS?
- cap.get(cv2.CAP_PROP_FPS)
- cap.fps()
- cv2.fps(cap)
* Correct answer: cap.get(cv2.CAP_PROP_FPS)
Stream properties are read via cap.get with a constant.

What does ret == False mean in a read loop?
- The video ended or an error occurred
- The frame is processed
- The camera is off
* Correct answer: The video ended or an error occurred
This condition is the basis for exiting the loop.

What does cv2.VideoWriter_fourcc(*"mp4v") do?
- Creates the MPEG-4 codec for writing
- Opens a video for reading
- Changes the FPS
* Correct answer: Creates the MPEG-4 codec for writing
fourcc is a four-character codec identifier.

Why is a gray frame converted back to BGR before writing?
- VideoWriter expects frames of the same shape and number of channels
- To speed up writing
- It's an FPS requirement
* Correct answer: VideoWriter expects frames of the same shape and number of channels
The writer is configured for a specific resolution and number of channels.

What does writer.write(frame) do?
- Adds a frame to the video file
- Reads a frame
- Closes the stream
* Correct answer: Adds a frame to the video file
write adds one frame to the output file.

What must be done after the writing loop?
- writer.release() and cap.release()
- Nothing
- Restart the script
* Correct answer: writer.release() and cap.release()
Closing the streams guarantees the files are finalized correctly.

How do you open a webcam?
- cv2.VideoCapture(0)
- cv2.VideoCapture("webcam")
- cv2.openCamera(0)
* Correct answer: cv2.VideoCapture(0)
Number 0 is the device's first camera.

How many channels does a gray frame have?
- 1
- 3
- 4
* Correct answer: 1
A gray image is two-dimensional, but before writing it is returned to 3 channels.
<!--/QUIZ-->
