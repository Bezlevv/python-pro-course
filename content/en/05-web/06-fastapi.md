---
title: FastAPI: endpoints and Pydantic
summary: Creating APIs, path/query params, request bodies, validation.
order: 6
duration: 45 min
difficulty: intermediate
tags: fastapi, pydantic, endpoints
---

FastAPI builds modern async APIs with automatic validation and docs.

## Minimal

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello"}
```

Run: `uvicorn main:app --reload`.

## Parameters

```python
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

## Pydantic

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

@app.post("/items")
def create_item(item: Item):
    return {"name": item.name, "price": item.price}
```

## Docs

FastAPI auto-generates /docs (Swagger).

## Lesson summary

FastAPI: types validate input; models define bodies; docs are automatic.

<!--TASK-->
### Task 1 — Hello
Create the minimal app with GET /.

### Task 2 — Type param
Add GET /items/{id} with int id.

### Task 3 — Query param
Add optional q parameter with default None.

### Task 4 — Body model
Create Item model and POST /items.

### Task 5 — Validation
Try sending a wrong type; note the 422 error.

### Task 6 — Status codes
Return 201 on creation with status_code=201.

### Task 7 — Docs
Explain how to open /docs and /openapi.json.
<!--/TASK-->

<!--HINT-->
### Hint 1
FastAPI(); @app.get("/").

### Hint 2
path param with type.

### Hint 3
q: str | None = None.

### Hint 4
BaseModel fields.

### Hint 5
Automatic 422.

### Hint 6
status_code=201.

### Hint 7
/docs, /openapi.json.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello"}
```

### Solution 2
```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

### Solution 3
```python
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

### Solution 4
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

@app.post("/items")
def create_item(item: Item):
    return {"name": item.name, "price": item.price}
```

### Solution 5
```python
# POST {"name": 123} → 422 Unprocessable Entity
```

### Solution 6
```python
@app.post("/items", status_code=201)
def create_item(item: Item):
    return item
```

### Solution 7
```python
# http://127.0.0.1:8000/docs — Swagger UI
# http://127.0.0.1:8000/openapi.json — schema
```
<!--/SOLUTION-->

<!--QUIZ-->
What is FastAPI built on?
- Starlette + Pydantic
- Django
- Flask
- Tornado
* Correct answer: Starlette + Pydantic
Modern stack.

What does @app.get do?
- Adds GET endpoint
- Starts server
- Imports
- Validates
* Correct answer: Adds GET endpoint
Route.

What is a path parameter?
- /items/{id}
- ?q=1
- header
- body
* Correct answer: /items/{id}
In URL.

What is a query parameter?
- ?q=...
- /path
- body
- header
* Correct answer: ?q=...
Optional.

What is Pydantic?
- Data validation library
- ORM
- Template
- Test
* Correct answer: Data validation library
Models.

What is BaseModel?
- Pydantic base class
- Django model
- Flask class
- None
* Correct answer: Pydantic base class
Define fields.

What happens on wrong type input?
- 422
- 200
- 404
- 500
* Correct answer: 422
Validation error.

What does status_code=201 do?
- Sets response status
- Sets body
- Redirects
- Logs
* Correct answer: Sets response status
Created.

How to run FastAPI?
- uvicorn main:app --reload
- python app.py
- flask run
- manage.py
* Correct answer: uvicorn main:app --reload
ASGI.

What is /docs?
- Swagger UI
- JSON schema
- Test page
- Admin
* Correct answer: Swagger UI
Interactive.

What is /openapi.json?
- OpenAPI schema
- HTML
- PDF
- Logs
* Correct answer: OpenAPI schema
Machine-readable.

Are endpoints async-capable?
- Yes
- No
- Only GET
- Only POST
* Correct answer: Yes
async def supported.
<!--/QUIZ-->
