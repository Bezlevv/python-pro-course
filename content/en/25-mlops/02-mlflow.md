---
title: Experiments with MLflow
summary: Track runs, parameters, metrics.
order: 2
duration: 45 min
difficulty: advanced
tags: mlflow
---

MLflow tracks experiments.

## Track

```python
import mlflow

with mlflow.start_run():
    mlflow.log_param("lr", 0.01)
    mlflow.log_metric("accuracy", 0.93)
    mlflow.log_artifact("model.pkl")
```

## UI

```bash
mlflow ui
# http://localhost:5000
```

## Lesson summary

Log params/metrics; compare runs.

<!--TASK-->
### Task 1 — Start
Start a run.

### Task 2 — Params
Log two parameters.

### Task 3 — Metrics
Log a metric.

### Task 4 — Artifact
Save a model file.

### Task 5 — Compare
Open the UI.

### Task 6 — Nested
Use a child run.

### Task 7 — Load
Use mlflow.pyfunc.load_model.
<!--/TASK-->

<!--HINT-->
### Hint 1
start_run.

### Hint 2
log_param.

### Hint 3
log_metric.

### Hint 4
log_artifact.

### Hint 5
mlflow ui.

### Hint 6
Run.

### Hint 7
Load.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import mlflow
with mlflow.start_run():
    ...
```

### Solution 2
```python
mlflow.log_param("lr", 0.01)
mlflow.log_param("epochs", 10)
```

### Solution 3
```python
mlflow.log_metric("accuracy", 0.93)
```

### Solution 4
```python
import pickle
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
mlflow.log_artifact("model.pkl")
```

### Solution 5
```bash
mlflow ui
# открыть http://localhost:5000 — таблица запусков
```

### Solution 6
```python
with mlflow.start_run() as parent:
    mlflow.log_metric("m", 1)
    with mlflow.start_run(nested=True) as child:
        mlflow.log_metric("m", 2)
```

### Solution 7
```python
loaded = mlflow.pyfunc.load_model("runs:/<id>/model")
```
<!--/SOLUTION-->

<!--QUIZ-->
What is MLflow?
- Experiment tracking
- A model
- A database
- None
* Correct answer: Experiment tracking
Tool.

What is a run?
- One experiment
- A model
- A metric
- None
* Correct answer: One experiment
Instance.

What is log_param?
- Logs config
- Logs metric
- Saves model
- None
* Correct answer: Logs config
Hyper.

What is log_metric?
- Logs number
- Logs param
- Artifact
- None
* Correct answer: Logs number
Accuracy.

What is an artifact?
- Saved file
- Metric
- Param
- None
* Correct answer: Saved file
Model.

What is the UI?
- Comparison view
- Terminal
- API
- None
* Correct answer: Comparison view
Localhost.

What is nested?
- Child run
- Sibling
- End
- None
* Correct answer: Child run
Parent.

What is pyfunc?
- Generic loader
- A model
- A param
- None
* Correct answer: Generic loader
Predict.

What is a run id?
- Identifier
- Metric
- File
- None
* Correct answer: Identifier
Path.

What is comparison?
- Runs side-by-side
- Training
- Deploy
- None
* Correct answer: Runs side-by-side
Choose.

What is tracking?
- Recording
- Predicting
- Training
- None
* Correct answer: Recording
Logs.

What is the benefit?
- Organized experiments
- Manual
- Required
- None
* Correct answer: Organized experiments
Compare.
<!--/QUIZ-->
