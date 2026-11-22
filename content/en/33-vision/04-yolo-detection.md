---
title: Object Detection: YOLO
summary: Object detection neural networks, Ultralytics YOLO, predictions, confidence filtering, annotations.
order: 4
duration: 50 min
difficulty: advanced
tags: yolo, ultralytics, detection, neural networks
---

Classical methods like Haar cascades can only find one type of object (faces) and require separate training for each task. Modern object detection works differently: a single neural network finds all objects in an image in one pass, draws boxes around them, and reports the class and confidence of each object. The most famous representative of this approach is YOLO (You Only Look Once).

## What is YOLO

YOLO divides the image into a grid and immediately predicts for each cell: which objects are in it, where their bounding boxes are, and how confident the model is in each prediction. Hence the name — "you only look once". This makes YOLO very fast: it processes dozens of frames per second and can run on real-time video.

## Ultralytics YOLO

In Python, the most convenient ready-made YOLO models come from the Ultralytics library:

```bash
pip install ultralytics
```

The model is loaded with a single line — there's no need to program the neural network architecture:

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")   # pretrained neural network (n — nano, the lightest)
```

On the first call, Ultralytics downloads the model weights from the internet (about 6 MB). Now let's predict objects in an image:

```python
results = model.predict(source="photo.jpg", conf=0.5)
```

`conf=0.5` — the confidence threshold: predictions weaker than 50% are discarded.

## Result structure

`model.predict` returns a list `results` — one item per image (you can pass a folder with several at once). For a single image, take `results[0]`.

```python
result = results[0]

# Boxes: tensor (N, 4) — coordinates x1, y1, x2, y2
boxes = result.boxes.xyxy
# Confidence: tensor (N,)
confs = result.boxes.conf
# Classes: tensor (N,)
classes = result.boxes.cls
# Class names
names = result.names
```

Let's break down one object:

```python
for box, conf, cls in zip(boxes, confs, classes):
    x1, y1, x2, y2 = map(int, box.tolist())
    label = names[int(cls)]
    print(f"{label}: {conf:.2f} [{x1}, {y1}, {x2}, {y2}]")
```

The output will look roughly like this:

```
person: 0.92 [112, 48, 340, 512]
car: 0.87 [540, 260, 800, 420]
```

## Annotating the result

Ultralytics can draw boxes and labels itself — the `plot()` method returns a BGR image ready to save:

```python
annotated = result.plot()          # BGR array with boxes
cv2.imwrite("annotated.jpg", annotated)
```

## Processing the object list

Often you don't just need to see the boxes, but to count objects or filter them. For example, how many people are in a frame:

```python
people = sum(1 for cls in classes if names[int(cls)] == "person")
```

## Where to go next

Ultralytics has pretrained models of different sizes: `yolov8n.pt` (nano), `yolov8s.pt` (small), `yolov8m.pt` (medium). The larger the model, the higher the accuracy, but the lower the speed. Also, these models can be fine-tuned on your own data — that's a topic for a separate course. We'll focus on using a ready-made model.

## Summary

Detection with YOLO is three steps: load the model (`YOLO("yolov8n.pt")`), call `predict`, and parse `result.boxes`. The box data lives in PyTorch tensors, so for convenience they are converted to Python lists via `tolist()`. Let's reinforce this with practice.

<!--TASK-->
### Task 1
Write a function `load_and_predict(model_path, image_path)` that loads a YOLO model and calls `predict` with the threshold `conf=0.5`. For each found object, print a line of the form `class: confidence [x1, y1, x2, y2]`. To convert coordinates to int, use `map(int, box.tolist())`. If the result is empty, print `No objects found`.

### Task 2
Write a function `annotate_image(model_path, image_path, out_path)` that makes a prediction, gets the annotated image via `result.plot()`, saves it to the given path, and returns `None`. Check that the file appeared on disk and its size is greater than zero. Use `os.path.getsize` for the check.

### Task 3
Write a function `count_detections(results)` that takes a list of results and returns the total number of objects across all images (the sum of `boxes` lengths over all results). As dummy data, you can pass an empty list — the function should return 0. Check on a real prediction: the number of objects must match the number of printed lines from task 1.

### Task 4
Write a function `parse_boxes(result, conf_thr=0.5)` that returns a list of dictionaries of the form `{"class": class_name, "conf": float, "box": (x1, y1, x2, y2)}` for all objects with confidence at least `conf_thr`. Write **pytest tests**: create a fake result object with known fields (via a simple class with `boxes`, `names` attributes and `torch.tensor` tensors) and check that threshold filtering works and that coordinates are converted to an int tuple. Run the tests.

### Task 5
Write a function `most_frequent_class(result)` that returns the string name of the class that occurs most often (on a tie — any). Write **pytest tests**: create a fake result with classes `[0, 1, 0, 2, 0]` and names `{0: "person", 1: "car", 2: "dog"}` — the function must return `"person"`. Also check behavior on an empty result: the function must return `None`. Run the tests.
<!--/TASK-->

<!--HINT-->
### Hint 1
Model: `model = YOLO(model_path)`. Prediction: `results = model.predict(source=image_path, conf=0.5)`. Data: `boxes = results[0].boxes.xyxy`, `confs = results[0].boxes.conf`, `classes = results[0].boxes.cls`, `names = results[0].names`.

### Hint 2
Annotation: `annotated = results[0].plot()` — a BGR array. Save via `cv2.imwrite(out_path, annotated)`. File size: `os.path.getsize(out_path) > 0`.

### Hint 3
Total objects: `sum(len(r.boxes) for r in results)`. For an empty list the sum is 0.

### Hint 4
Create the class `class FakeBoxes: pass` with attributes `xyxy = torch.tensor([[10, 20, 30, 40]])`, `conf = torch.tensor([0.7])`, `cls = torch.tensor([0])`, and `class FakeResult` with `boxes = FakeBoxes()` and `names = {0: "person"}`. Compare the result with the expected list of dictionaries.

### Hint 5
Count frequencies with a plain dict or `collections.Counter`. For an empty result return `None`. Note: classes are indices, and you must return the name from `names`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
from ultralytics import YOLO

def load_and_predict(model_path, image_path):
    model = YOLO(model_path)
    results = model.predict(source=image_path, conf=0.5)
    result = results[0]
    boxes = result.boxes.xyxy
    confs = result.boxes.conf
    classes = result.boxes.cls
    names = result.names
    if len(boxes) == 0:
        print("No objects found")
        return
    for box, conf, cls in zip(boxes, confs, classes):
        x1, y1, x2, y2 = map(int, box.tolist())
        label = names[int(cls)]
        print(f"{label}: {conf:.2f} [{x1}, {y1}, {x2}, {y2}]")

load_and_predict("yolov8n.pt", "photo.jpg")
```

Result (example):

```
person: 0.92 [112, 48, 340, 512]
car: 0.87 [540, 260, 800, 420]
```

What's going on here? `model.predict` returns a list of results — one per image. `result.boxes.xyxy` is a tensor of box coordinates in the `(x1, y1, x2, y2)` format (top-left and bottom-right corners). `map(int, box.tolist())` turns the tensor numbers into plain integers. The class is an index, and the name comes from the `result.names` dictionary.

### Solution 2
Solution:

```python
import os
import cv2
from ultralytics import YOLO

def annotate_image(model_path, image_path, out_path):
    model = YOLO(model_path)
    results = model.predict(source=image_path, conf=0.5)
    annotated = results[0].plot()
    cv2.imwrite(out_path, annotated)
    print(f"Saved to {out_path}, size {os.path.getsize(out_path)} bytes")

annotate_image("yolov8n.pt", "photo.jpg", "annotated.jpg")
```

What's going on here? `result.plot()` draws boxes, class labels, and confidence percentages right on a copy of the image and returns a BGR array. Then everything is as usual: `cv2.imwrite`. `os.path.getsize` verifies the file was really created. The same approach is used to show detection on video — each frame is processed and annotated.

### Solution 3
Solution:

```python
def count_detections(results):
    return sum(len(r.boxes) for r in results)
```

What's going on here? Each item of `results` has a `boxes` attribute, and it has `.xyxy` with one row per object, so `len(r.boxes)` is the number of objects in one image. We sum over all results. For an empty list the generator yields nothing and the sum is 0. This function is handy together with task 1 — the number of lines on screen should match its return value.

### Solution 4
Solution:

```python
import torch

def parse_boxes(result, conf_thr=0.5):
    parsed = []
    boxes = result.boxes.xyxy
    confs = result.boxes.conf
    classes = result.boxes.cls
    for box, conf, cls in zip(boxes, confs, classes):
        if conf.item() < conf_thr:
            continue
        x1, y1, x2, y2 = map(int, box.tolist())
        parsed.append({
            "class": result.names[int(cls)],
            "conf": conf.item(),
            "box": (x1, y1, x2, y2),
        })
    return parsed
```

Tests:

```python
class FakeBoxes:
    def __init__(self):
        self.xyxy = torch.tensor([
            [10, 20, 30, 40],
            [50, 60, 70, 80],
        ])
        self.conf = torch.tensor([0.9, 0.3])
        self.cls = torch.tensor([0, 1])

class FakeResult:
    def __init__(self):
        self.boxes = FakeBoxes()
        self.names = {0: "person", 1: "car"}

def test_parse_boxes_filter():
    res = parse_boxes(FakeResult(), conf_thr=0.5)
    assert len(res) == 1
    assert res[0]["class"] == "person"
    assert res[0]["conf"] == 0.9
    assert res[0]["box"] == (10, 20, 30, 40)

def test_parse_boxes_all():
    res = parse_boxes(FakeResult(), conf_thr=0.0)
    assert len(res) == 2
    assert res[1]["class"] == "car"
```

What's going on here? We can't run the neural network in tests — it's slow and requires downloading weights. So we create a fake class with the same attributes as a real result. The key point: values from PyTorch tensors are extracted with `.item()` and `.tolist()`. Threshold filtering drops the object with confidence 0.3 — it's absent from the first test but appears at threshold 0.0 in the second.

### Solution 5
Solution:

```python
from collections import Counter

def most_frequent_class(result):
    classes = result.boxes.cls
    if len(classes) == 0:
        return None
    counter = Counter(int(cls) for cls in classes)
    top_index = counter.most_common(1)[0][0]
    return result.names[top_index]
```

Tests:

```python
import torch

class FakeBoxes:
    def __init__(self):
        self.cls = torch.tensor([0, 1, 0, 2, 0])

class FakeResult:
    def __init__(self):
        self.boxes = FakeBoxes()
        self.names = {0: "person", 1: "car", 2: "dog"}

def test_most_frequent_person():
    assert most_frequent_class(FakeResult()) == "person"

class FakeEmptyBoxes:
    def __init__(self):
        self.cls = torch.tensor([])

class FakeEmptyResult:
    def __init__(self):
        self.boxes = FakeEmptyBoxes()
        self.names = {}

def test_most_frequent_empty():
    assert most_frequent_class(FakeEmptyResult()) is None
```

What's going on here? `collections.Counter` counts the occurrences of each class. `most_common(1)` returns a list with one element — the pair `(class, count)` — from which we take the index. Then we get the name from `result.names` by index. In the fake data, class 0 (`person`) occurs three times, so the answer is `"person"`. An empty result is handled separately: if there are no objects, we return `None` instead of crashing with an indexing error.
<!--/SOLUTION-->

<!--QUIZ-->
What does the acronym YOLO stand for?
- You Only Look Once — "look once"
- Your Own Local Objects
- Yielding Object Learning Output
* Correct answer: You Only Look Once — "look once"
The network scans the image in a single pass.

Which library provides ready-made YOLO models in Python?
- ultralytics
- scikit-learn
- pygame
* Correct answer: ultralytics
Ultralytics supports YOLOv8 models and newer.

What does YOLO("yolov8n.pt") do?
- Loads a pretrained YOLOv8 nano model
- Starts training
- Installs CUDA
* Correct answer: Loads a pretrained YOLOv8 nano model
The letter n means nano, the lightest version.

What is the coordinate format of boxes in result.boxes.xyxy?
- (x1, y1, x2, y2) — two opposite corners
- (x, y, w, h) — corner and size
- (cx, cy, w, h) — center and size
* Correct answer: (x1, y1, x2, y2) — two opposite corners
xyxy stores the top-left and bottom-right corners.

What does the conf parameter in predict mean?
- Confidence threshold: weaker predictions are discarded
- The number of objects
- The box size
* Correct answer: Confidence threshold: weaker predictions are discarded
With conf=0.5, only predictions with confidence from 50% remain.

How do you get a class name by its index?
- result.names[int(cls)]
- result.labels[cls]
- result.classes[cls]
* Correct answer: result.names[int(cls)]
names is a dictionary where the index maps to the class name.

What does result.plot() return?
- An annotated image in BGR
- A list of boxes
- A report text
* Correct answer: An annotated image in BGR
plot draws boxes and labels and returns a numpy array.

What role do PyTorch tensors play in the Ultralytics API?
- They store coordinates, confidences, and classes
- They manage GPU memory manually
- They fully replace numpy
* Correct answer: They store coordinates, confidences, and classes
boxes, conf, cls are tensors; values are read via .tolist() and .item().

Which model is more accurate — yolov8n or yolov8m?
- yolov8m (medium)
- yolov8n (nano)
- They are the same
* Correct answer: yolov8m (medium)
A larger model means higher accuracy but lower speed.

What will predict return for an empty image?
- Empty tensors of boxes, confidences, and classes
- None
- An error
* Correct answer: Empty tensors of boxes, confidences, and classes
The list of objects will simply be empty.
<!--/QUIZ-->
