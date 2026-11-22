---
title: Project: API service with FastAPI
summary: Build a books API with validation, CRUD and docs.
order: 3
duration: 90 min
difficulty: advanced
tags: project, fastapi, api
---

Build a clean API service.

## Plan

1. Models via Pydantic;
2. In-memory storage;
3. Endpoints: list, get, create, update, delete;
4. Test with TestClient.

## Skeleton

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
    title: str
    author: str
    year: int

books = []

@app.get("/books")
def list_books():
    return books
```

## Lesson summary

A typed API with validation and automatic docs.

<!--TASK-->
### Task 1 — Model
Create Book with title, author, year.

### Task 2 — List
GET /books returns the list.

### Task 3 — Create
POST /books appends and returns 201.

### Task 4 — Get one
GET /books/{id} returns or 404.

### Task 5 — Update
PUT /books/{id} updates.

### Task 6 — Delete
DELETE /books/{id} removes.

### Task 7 — Test
Write TestClient tests.
<!--/TASK-->

<!--HINT-->
### Hint 1
BaseModel.

### Hint 2
list.

### Hint 3
status_code=201.

### Hint 4
HTTPException(404).

### Hint 5
PUT.

### Hint 6
DELETE.

### Hint 7
TestClient.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from pydantic import BaseModel

class Book(BaseModel):
    title: str
    author: str
    year: int
```

### Solution 2
```python
books = []

@app.get("/books")
def list_books():
    return books
```

### Solution 3
```python
@app.post("/books", status_code=201)
def create_book(book: Book):
    books.append(book)
    return book
```

### Solution 4
```python
@app.get("/books/{book_id}")
def get_book(book_id: int):
    if book_id >= len(books):
        raise HTTPException(status_code=404, detail="Not found")
    return books[book_id]
```

### Solution 5
```python
@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    if book_id >= len(books):
        raise HTTPException(status_code=404)
    books[book_id] = book
    return book
```

### Solution 6
```python
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    if book_id >= len(books):
        raise HTTPException(status_code=404)
    return books.pop(book_id)
```

### Solution 7
```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_create():
    r = client.post("/books", json={"title": "Py", "author": "A", "year": 2020})
    assert r.status_code == 201
```
<!--/SOLUTION-->

<!--QUIZ-->
What is Pydantic for?
- Validation
- ORM
- Templates
- Tests
* Correct answer: Validation
Models.

What is BaseModel?
- Data model base
- Table
- Route
- None
* Correct answer: Data model base
Define.

What status is created?
- 201
- 200
- 404
- 500
* Correct answer: 201
Created.

What is HTTPException?
- Error response
- Success
- Model
- Test
* Correct answer: Error response
Raise.

What is 404?
- Not found
- OK
- Created
- Error
* Correct answer: Not found
Missing.

What does PUT do?
- Full update
- Create
- Delete
- Read
* Correct answer: Full update
Replace.

What does DELETE do?
- Removes
- Creates
- Updates
- Reads
* Correct answer: Removes
Delete.

What is in-memory storage?
- A list
- SQLite
- PostgreSQL
- File
* Correct answer: A list
Temporary.

What is TestClient?
- Client for tests
- A server
- A model
- A DB
* Correct answer: Client for tests
Requests.

What is json= in tests?
- Request body
- Headers
- Query
- None
* Correct answer: Request body
JSON.

What is /docs?
- Swagger UI
- Schema file
- Admin
- Logs
* Correct answer: Swagger UI
Interactive.

Why 404 on missing index?
- Out of range
- Empty
- Wrong
- None
* Correct answer: Out of range
Validation.
<!--/QUIZ-->
