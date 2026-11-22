---
title: Final Project: Recognition
summary: End-to-end pipeline: reading, preprocessing, detection, post-processing, report; unit and integration tests.
order: 6
duration: 60 min
difficulty: advanced
tags: project, pipeline, recognition, tests
---

In this module we studied all the building blocks of computer vision: working with images, filters and contours, descriptors, YOLO detection, and video processing. Now let's assemble them into a real application — a recognition module that finds objects in an image and produces a report.

## Pipeline architecture

Any real computer vision system is built on the same principle — like a conveyor belt:

1. **Reading** — load the image (`cv2.imread`).
2. **Preprocessing** — prepare the frame (convert to the needed space, resize).
3. **Detection** — find objects (YOLO, cascades, contours — depending on the task).
4. **Post-processing** — filter by confidence, draw boxes, count.
5. **Output** — return a report and save the result.

Each stage is a separate function. This lets you test steps individually and swap the detector without touching the rest of the code.

## Designing the interface

Let's build a `Pipeline` class with methods for each stage and a `run` method that executes the whole pipeline:

```python
from dataclasses import dataclass, field

@dataclass
class Detection:
    label: str
    confidence: float
    box: tuple  # (x1, y1, x2, y2)

@dataclass
class Pipeline:
    model_path: str
    conf_threshold: float = 0.5
    _model: object = field(default=None, repr=False)

    def _load_model(self):
        from ultralytics import YOLO
        if self._model is None:
            self._model = YOLO(self.model_path)
        return self._model

    def detect(self, image):
        model = self._load_model()
        results = model.predict(source=image, conf=self.conf_threshold)
        detections = []
        result = results[0]
        for box, conf, cls in zip(result.boxes.xyxy,
                                   result.boxes.conf,
                                   result.boxes.cls):
            detections.append(Detection(
                label=result.names[int(cls)],
                confidence=float(conf),
                box=tuple(map(int, box.tolist())),
            ))
        return detections
```

Advantages: `Detection` is a simple data structure (a dataclass), detection results are easy to filter and test, and the model is loaded lazily — once.

## Post-processing and report

Let's add filtering and a text report:

```python
def filter_by_label(self, detections, label):
    return [d for d in detections if d.label == label]

def report(self, detections):
    lines = []
    for d in detections:
        lines.append(f"{d.label}: {d.confidence:.2f} {d.box}")
    return "\n".join(lines) if lines else "No objects found"
```

## Testing the pipeline

We can't run the neural network in every test, so the detector is replaced with a fake one. This is called mocking:

```python
class FakeModel:
    def predict(self, source, conf=0.5):
        return [FakeResults()]

class FakeResults:
    def __init__(self):
        self.boxes = FakeBoxes()
        self.names = {0: "person", 1: "car"}

class FakeBoxes:
    def __init__(self):
        self.xyxy = torch.tensor([[10, 20, 30, 40]])
        self.conf = torch.tensor([0.9])
        self.cls = torch.tensor([0])
```

By injecting such an object into the pipeline, we can verify the logic without downloading weights or using a GPU. This is a standard industry technique: unit tests on logic, integration tests on the real model.

## Performance

If the typical task is known, the image is resized down before detection — this speeds up the neural network several times. For example:

```python
def resize_for_inference(self, image, max_side=1280):
    h, w = image.shape[:2]
    scale = min(1.0, max_side / max(h, w))
    if scale < 1.0:
        image = cv2.resize(image, None, fx=scale, fy=scale)
    return image
```

## Summary

The project combines everything we've learned: image processing, detection, and good tested code. Splitting into stages and using dataclasses make the system maintainable, and mocking lets you check the logic quickly. Ahead of you are the final tasks of the module.

<!--TASK-->
### Task 1
Assemble the pipeline skeleton: create a `Pipeline` class with a `detect(image)` method that takes an image (a numpy array) and returns a list of `Detection` objects. Detection is via `YOLO` from `ultralytics`, the confidence threshold comes from the `conf_threshold` field. If the image is not a numpy array — raise `TypeError`. Test on a real model: print the report for any image.

### Task 2
Add a `report(detections)` method to `Pipeline` that returns a report string: one line per object in the form `label: confidence box`. If there are no detections — return the string `No objects found`. Extend the `Detection` class with the fields `label`, `confidence`, `box`. Make sure the report for an empty list prints the correct message.

### Task 3
Add a `filter_by_label(detections, label)` method that returns only detections with the given class, and a `count_by_label(detections, label)` method that returns their count. Check on the results of task 1: the number of people must not exceed the total number of objects.

### Task 4
Write **pytest tests** for the pipeline logic with a fake model. Implement the fake classes `FakeModel`, `FakeResults`, `FakeBoxes` (as in the theory) that return two objects: `person` with confidence 0.9 and `car` with confidence 0.4. Inject the fake model into `Pipeline` (via the `_model` field) and check: `detect` returns 2 objects, `filter_by_label(_, "person")` returns 1 object, `count_by_label(_, "car")` returns 1, `report` contains both lines. Run the tests.

### Task 5
Write an integration test `test_pipeline_end_to_end`: create a synthetic image with two white rectangles on a black background, inject a fake model that returns one `box` object with `(10, 10, 50, 50)`. Check that `Pipeline.run` (invent this method: reading → detection → report) returns a non-empty report and that it contains the word `box`. Also check that with `_model=None` the model is loaded (replace `YOLO` with a fake via `monkeypatch` mocking). Run the tests.
<!--/TASK-->

<!--HINT-->
### Hint 1
`Detection` is a dataclass with fields `label`, `confidence`, `box`. In `detect`, call `self._load_model()` and then `model.predict(source=image, conf=self.conf_threshold)`. Type check: `if not isinstance(image, np.ndarray): raise TypeError(...)`.

### Hint 2
In `report`, use f-strings: `f"{d.label}: {d.confidence:.2f} {d.box}"`. For an empty list — `if not detections: return "No objects found"`.

### Hint 3
`filter_by_label` — a list comprehension: `[d for d in detections if d.label == label]`. `count_by_label` — `len(self.filter_by_label(detections, label))`.

### Hint 4
Fake model: `self._model = FakeModel()` in `Pipeline` before calling `detect`. In `FakeBoxes`, provide `torch.tensor([[10, 20, 30, 40], [50, 60, 70, 80]])`, `torch.tensor([0.9, 0.4])`, `torch.tensor([0, 1])`. Names: `{0: "person", 1: "car"}`.

### Hint 5
The `run` method — `def run(self, image_path): img = cv2.imread(image_path); detections = self.detect(img); return self.report(detections)`. For mocking `YOLO`, use `monkeypatch.setattr("ultralytics.YOLO", FakeModel)`. The integration test should check the path from file to report.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
from dataclasses import dataclass, field
import numpy as np

@dataclass
class Detection:
    label: str
    confidence: float
    box: tuple

@dataclass
class Pipeline:
    model_path: str
    conf_threshold: float = 0.5
    _model: object = field(default=None, repr=False)

    def _load_model(self):
        from ultralytics import YOLO
        if self._model is None:
            self._model = YOLO(self.model_path)
        return self._model

    def detect(self, image):
        if not isinstance(image, np.ndarray):
            raise TypeError("image must be a numpy array")
        model = self._load_model()
        results = model.predict(source=image, conf=self.conf_threshold)
        detections = []
        result = results[0]
        for box, conf, cls in zip(result.boxes.xyxy,
                                   result.boxes.conf,
                                   result.boxes.cls):
            detections.append(Detection(
                label=result.names[int(cls)],
                confidence=float(conf),
                box=tuple(map(int, box.tolist())),
            ))
        return detections
```

What's going on here? The `Detection` dataclass is a simple data structure without methods. `Pipeline` stores the model path and the confidence threshold, and the `_model` field is a cache of the loaded model (`field(default=None, repr=False)` hides it from `repr`). Lazy loading in `_load_model` means the model is downloaded only on the first `detect` call. The `isinstance` type check guards against usage errors.

### Solution 2
Solution:

```python
def report(self, detections):
    if not detections:
        return "No objects found"
    lines = [f"{d.label}: {d.confidence:.2f} {d.box}"
             for d in detections]
    return "\n".join(lines)

def filter_by_label(self, detections, label):
    return [d for d in detections if d.label == label]

def count_by_label(self, detections, label):
    return len(self.filter_by_label(detections, label))
```

What's going on here? `report` turns a list of detections into a human-readable string: each detection is a separate line, confidence is rounded to two decimals (`:02f`). An empty list is handled separately — this is better than returning an empty string. `filter_by_label` and `count_by_label` are a filter/counter pair; the second uses the first, which avoids duplicated logic.

### Solution 3
Solution — this is an addition to the class from solution 2:

```python
pipeline = Pipeline("yolov8n.pt", conf_threshold=0.5)
image = cv2.imread("photo.jpg")
detections = pipeline.detect(image)
print(pipeline.report(detections))
print("People:", pipeline.count_by_label(detections, "person"))
```

What's going on here? The functions from task 3 are already added to the class in solution 2. Here we show the usage: detect objects, print the full report and, separately, the number of people. The check "people are not more than the total" holds automatically: `count_by_label` is a subset of all detections, so its count physically cannot exceed the total. If you want a formal check, you can pin it down with a test.

### Solution 4
Solution:

```python
import torch

class FakeBoxes:
    def __init__(self):
        self.xyxy = torch.tensor([[10, 20, 30, 40],
                                  [50, 60, 70, 80]])
        self.conf = torch.tensor([0.9, 0.4])
        self.cls = torch.tensor([0, 1])

class FakeResults:
    def __init__(self):
        self.boxes = FakeBoxes()
        self.names = {0: "person", 1: "car"}

class FakeModel:
    def predict(self, source, conf=0.5):
        return [FakeResults()]

def make_pipeline_with_fake():
    p = Pipeline("fake.pt")
    p._model = FakeModel()
    return p

def test_detect_returns_two():
    p = make_pipeline_with_fake()
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    detections = p.detect(image)
    assert len(detections) == 2

def test_filter_by_label_person():
    p = make_pipeline_with_fake()
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    detections = p.detect(image)
    persons = p.filter_by_label(detections, "person")
    assert len(persons) == 1
    assert persons[0].label == "person"

def test_count_by_label_car():
    p = make_pipeline_with_fake()
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    detections = p.detect(image)
    assert p.count_by_label(detections, "car") == 1

def test_report_contains_lines():
    p = make_pipeline_with_fake()
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    detections = p.detect(image)
    report = p.report(detections)
    assert "person" in report and "car" in report
```

What's going on here? The fake model returns exactly the data we specify: two objects — `person` with confidence 0.9 and `car` with 0.4. By setting `_model = FakeModel()`, we completely bypass the real neural network. The tests verify the pipeline logic: the number of detections, filtering, the counter, and the report contents. These are fast tests without the internet or weights — they can be run after every code change.

### Solution 5
Solution:

```python
class Pipeline:
    # ... (previous methods) ...

    def run(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"File not found: {image_path}")
        detections = self.detect(image)
        return self.report(detections)

def test_pipeline_end_to_end(monkeypatch):
    monkeypatch.setattr("ultralytics.YOLO", FakeModel)
    # create an image with two white rectangles
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    image[20:60, 20:60] = 255
    image[120:160, 120:160] = 255
    cv2.imwrite("tmp_pipeline.png", image)

    p = Pipeline("fake.pt")
    report = p.run("tmp_pipeline.png")
    assert "box" in report

def test_run_raises_on_missing_file():
    p = Pipeline("fake.pt")
    p._model = FakeModel()
    try:
        p.run("no_such_file.png")
    except FileNotFoundError:
        pass
    else:
        assert False, "A FileNotFoundError should have been raised"
```

What's going on here? `monkeypatch.setattr("ultralytics.YOLO", FakeModel)` replaces the `YOLO` class in the `ultralytics` module with a fake one — now `_load_model` returns `FakeModel()`. The `run` method chains the stages: reading the file, detection, report. The second test checks error handling: if the file is missing, `cv2.imread` returns `None`, and `run` must raise `FileNotFoundError`. This is what a real integration test looks like: the path from file to user report, but without a real neural network.
<!--/SOLUTION-->

<!--QUIZ-->
What is the Detection dataclass for in the pipeline?
- To structure detection data
- To load the model
- To read files
* Correct answer: To structure detection data
The dataclass describes a single object: class, confidence, and box.

What is lazy model loading?
- The model is loaded only on first use
- The model is never loaded
- The model is loaded at import
* Correct answer: The model is loaded only on first use
This saves time at program startup.

Why are fake models needed in tests?
- To verify logic without a real neural network
- To speed up the real model
- To train the model
* Correct answer: To verify logic without a real neural network
Mocking replaces a heavy dependency with a fake object.

What does monkeypatch.setattr do?
- Replaces an attribute or class for the duration of a test
- Saves the test to a file
- Cleans up temporary files
* Correct answer: Replaces an attribute or class for the duration of a test
This is pytest's standard mechanism for mocking.

Which method in Pipeline runs the whole pipeline?
- run
- detect
- report
* Correct answer: run
run chains reading, detection, and report into a pipeline.

What will cv2.imread return if the file is missing?
- None
- An empty array
- An exception
* Correct answer: None
That's why run checks image is None and raises FileNotFoundError.

Why resize an image before detection?
- For speed: fewer pixels — faster neural network
- To improve accuracy
- It's required for YOLO
* Correct answer: For speed: fewer pixels — faster neural network
Reducing the resolution speeds up inference several times.

What does filter_by_label return?
- A list of detections with only the given class
- The number of all objects
- A report string
* Correct answer: A list of detections with only the given class
Filtering by class is an ordinary list comprehension.

Why is the report for an empty list handled separately?
- To return a clear "No objects found" message
- To print nothing
- Because report would return None
* Correct answer: To return a clear "No objects found" message
An empty string is harder for the user to read.

What technique allows testing run without files on disk?
- Create a file in the test and delete it after
- Use random paths
- It cannot be tested
* Correct answer: Create a file in the test and delete it after
Tests create temporary images via cv2.imwrite.
<!--/QUIZ-->
