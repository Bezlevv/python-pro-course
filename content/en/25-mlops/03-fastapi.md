---
title: Serving models with FastAPI
summary: Load model, endpoint, input schema.
order: 3
duration: 50 min
difficulty: advanced
tags: fastapi, ml
---

Serve a model behind an HTTP API.

## App

```python
from fastapi import FastAPI
from pydantic import BaseModel
import pickle

app = FastAPI()
model = pickle.load(open("model.pkl", "rb"))

class Input(BaseModel):
    features: list[float]

@app.post("/predict")
def predict(data: Input):
    pred = model.predict([data.features])
    return {"prediction": pred.tolist()}
```

## Run

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Lesson summary

FastAPI + pydantic validate and serve.

<!--TASK-->
### Task 1 — Load
Load a model.

### Task 2 — Schema
Define Input.

### Task 3 — Endpoint
create /predict.

### Task 4 — Run
uvicorn.

### Task 5 — Test
Send a request.

### Task 6 — Docs
Open /docs.

### Task 7 — Concurrency
Why FastAPI is fast?
<!--/TASK-->

<!--HINT-->
### Hint 1
pickle.

### Hint 2
BaseModel.

### Hint 3
@app.post.

### Hint 4
uvicorn.

### Hint 5
curl.

### Hint 6
Swagger.

### Hint 7
Async.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import pickle
model = pickle.load(open("model.pkl", "rb"))
```

### Solution 2
```python
from pydantic import BaseModel

class Input(BaseModel):
    features: list[float]
```

### Solution 3
```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/predict")
def predict(data: Input):
    pred = model.predict([data.features])
    return {"prediction": pred.tolist()}
```

### Solution 4
```bash
pip install fastapi uvicorn
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Solution 5
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features":[1.0,2.0]}'
```

### Solution 6
```text
Открыть http://localhost:8000/docs —
интерактивная документация Swagger
```

### Solution 7
```text
FastAPI построен на asyncio и Starlette:
много одновременных запросов на одном процессе
```
<!--/SOLUTION-->

<!--QUIZ-->
What is FastAPI?
- Web framework
- A model
- A database
- None
* Correct answer: Web framework
API.

What is pydantic?
- Validation
- Model
- Framework
- None
* Correct answer: Validation
Schema.

What is BaseModel?
- Input schema
- A model
- A database
- None
* Correct answer: Input schema
Class.

What is @app.post?
- POST route
- GET
- Delete
- None
* Correct answer: POST route
Decorator.

What is uvicorn?
- ASGI server
- Framework
- Model
- None
* Correct answer: ASGI server
Run.

What is pickle?
- Serialization
- HTTP
- Validation
- None
* Correct answer: Serialization
Load.

What is /docs?
- Swagger UI
- Endpoint data
- Model
- None
* Correct answer: Swagger UI
Docs.

What is a feature?
- Input value
- Output
- Label
- None
* Correct answer: Input value
List.

What is prediction?
- Model output
- Input
- Training
- None
* Correct answer: Model output
Result.

What is asyncio?
- Async engine
- Sync
- Threads
- None
* Correct answer: Async engine
Fast.

What is curl?
- CLI request
- A browser
- A model
- None
* Correct answer: CLI request
Test.

What is the benefit?
- High throughput
- Slow
- Required
- None
* Correct answer: High throughput
Async.
<!--/QUIZ-->
