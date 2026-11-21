---
title: Testing web applications
summary: Testing Flask/FastAPI/Django endpoints with pytest and test clients.
order: 13
duration: 45 min
difficulty: advanced
tags: testing, pytest, web
---

Web tests verify endpoints without a real browser.

## Flask test client

```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

def test_index(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"Hello" in r.data
```

## FastAPI TestClient

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_index():
    r = client.get("/")
    assert r.status_code == 200
```

## Django test client

```python
from django.test import TestCase

class IndexTest(TestCase):
    def test_index(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
```

## Lesson summary

Test clients exercise routes; assert status and content.

<!--TASK-->
### Task 1 — Flask client
Create a fixture returning the app test client.

### Task 2 — Status
Test that "/" returns 200.

### Task 3 — Content
Assert "Hello" appears in the response.

### Task 4 — 404
Test that an unknown route returns 404.

### Task 5 — POST
Test a POST endpoint and its response.

### Task 6 — FastAPI
Use TestClient to test an endpoint.

### Task 7 — Django
Write a simple Django TestCase.
<!--/TASK-->

<!--HINT-->
### Hint 1
app.test_client().

### Hint 2
assert r.status_code == 200.

### Hint 3
b"Hello" in r.data.

### Hint 4
assert r.status_code == 404.

### Hint 5
client.post("/submit", data={...}).

### Hint 6
TestClient(app).

### Hint 7
TestCase; self.client.get.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()
```

### Solution 2
```python
def test_index(client):
    r = client.get("/")
    assert r.status_code == 200
```

### Solution 3
```python
def test_content(client):
    r = client.get("/")
    assert b"Hello" in r.data
```

### Solution 4
```python
def test_404(client):
    r = client.get("/missing")
    assert r.status_code == 404
```

### Solution 5
```python
def test_post(client):
    r = client.post("/submit", data={"name": "Anna"})
    assert r.status_code == 200
    assert b"Anna" in r.data
```

### Solution 6
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_index():
    r = client.get("/")
    assert r.status_code == 200
```

### Solution 7
```python
from django.test import TestCase

class IndexTest(TestCase):
    def test_index(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a test client?
- Client that simulates requests
- A browser
- A server
- A DB
* Correct answer: Client that simulates requests
In-process.

What is client.get?
- GET request
- POST
- DELETE
- Open
* Correct answer: GET request
Simulated.

What is r.status_code?
- HTTP status
- Body
- Headers
- URL
* Correct answer: HTTP status
Assert.

What is r.data?
- Response body (bytes)
- Status
- JSON
- Headers
* Correct answer: Response body (bytes)
Content.

How to test 404?
- Get unknown path
- Assert 200
- Post
- Nothing
* Correct answer: Get unknown path
Assert 404.

What does TESTING=True do?
- Enables test mode
- Starts browser
- Disables
- Logs
* Correct answer: Enables test mode
Propagates errors.

What is FastAPI TestClient?
- Client for FastAPI
- Plugin
- DB
- Model
* Correct answer: Client for FastAPI
Uses httpx.

What does client.post do?
- POST request
- GET
- PUT
- HEAD
* Correct answer: POST request
With data.

What is Django TestCase?
- Base test class
- Fixture
- Middleware
- Admin
* Correct answer: Base test class
Self.client.

What does self.client.get do?
- Simulates GET
- Real network
- DB
- None
* Correct answer: Simulates GET
Django test.

What is b"Hello"?
- Bytes literal
- String
- List
- None
* Correct answer: Bytes literal
Compare with r.data.

Why test endpoints?
- Regression safety
- Speed
- Design
- SEO
* Correct answer: Regression safety
Confidence.
<!--/QUIZ-->
