---
title: OpenAPI, SDK generation and mock servers
summary: Schemas, FastAPI docs, client generation, mocks, contract tests.
order: 22
duration: 55 min
difficulty: advanced
tags: openapi, swagger, sdk, mocks
---

OpenAPI describes APIs; tools derive docs, clients and mocks.

## Schema

```yaml
openapi: 3.0.0
info:
  title: Books
  version: 1.0.0
paths:
  /books:
    get:
      responses:
        '200':
          description: List of books
```

## FastAPI auto-docs

/apiopenapi.json and /docs come free.

## SDK generation

Tools: openapi-generator, datamodel-code-generator → models.

## Mock servers

`prism mock schema.yaml` serves example responses.

## Contract tests

Validate responses against the schema.

## Lesson summary

OpenAPI is a single source of truth for docs, SDKs, mocks.

<!--TASK-->
### Task 1 — Minimal schema
Write an OpenAPI YAML with /ping.

### Task 2 — CRUD schema
Describe /books with GET/POST.

### Task 3 — FastAPI docs
Implement FastAPI and note /docs.

### Task 4 — Generate models
Generate Pydantic models from a schema.

### Task 5 — Mock
Run a mock server and test a GET.

### Task 6 — SDK call
Call the mock with requests.

### Task 7 — Validate
Validate a response against the schema.
<!--/TASK-->

<!--HINT-->
### Hint 1
openapi: 3.0.0.

### Hint 2
paths: /books.

### Hint 3
FastAPI auto.

### Hint 4
datamodel-code-generator.

### Hint 5
prism mock.

### Hint 6
requests to mock URL.

### Hint 7
openapi-spec-validator.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```yaml
openapi: 3.0.0
info:
  title: Ping
  version: 1.0.0
paths:
  /ping:
    get:
      responses:
        '200':
          description: OK
```

### Solution 2
```yaml
paths:
  /books:
    get:
      responses:
        '200':
          description: List
    post:
      requestBody:
        content:
          application/json:
            schema:
              type: object
      responses:
        '201':
          description: Created
```

### Solution 3
```python
from fastapi import FastAPI
app = FastAPI()
# /docs — Swagger UI, /openapi.json — схема
```

### Solution 4
```bash
datamodel-code-generator --input schema.yaml --output models.py
```

### Solution 5
```bash
prism mock schema.yaml
# GET http://127.0.0.1:4010/books
```

### Solution 6
```python
import requests
r = requests.get("http://127.0.0.1:4010/books", timeout=10)
print(r.status_code, r.json())
```

### Solution 7
```python
from openapi_spec_validator import validate_spec
import yaml

def = yaml.safe_load(open("schema.yaml"))
validate_spec(spec)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is OpenAPI?
- API description standard
- A database
- A template
- A server
* Correct answer: API description standard
Schema.

What does FastAPI generate?
- openapi.json + docs
- Only routes
- Login
- Static
* Correct answer: openapi.json + docs
Automatic.

What is a mock server?
- Serves example responses
- Real backend
- Cache
- Queue
* Correct answer: Serves example responses
From schema.

What is an SDK?
- Generated client
- Schema
- Test
- Mock
* Correct answer: Generated client
From schema.

What is a contract test?
- Validates against schema
- Performance
- Security
- Load
* Correct answer: Validates against schema
Conformance.

Which generator makes models?
- datamodel-code-generator
- pytest
- black
- gunicorn
* Correct answer: datamodel-code-generator
Pydantic.

What is prism?
- Mock server tool
- A library
- A DB
- A model
* Correct answer: Mock server tool
For schemas.

What is YAML?
- Data format
- Language
- DB
- Server
* Correct answer: Data format
For schemas.

What are paths?
- Endpoints
- Methods
- Schemas
- Types
* Correct answer: Endpoints
/books.

What does validate_spec do?
- Checks schema validity
- Runs tests
- Starts server
- None
* Correct answer: Checks schema validity
Syntax.

What is components in schema?
- Reusable definitions
- Paths
- Servers
- Tags
* Correct answer: Reusable definitions
Models.

Why single source of truth?
- Docs/SDK/mocks consistent
- Faster
- Smaller
- None
* Correct answer: Docs/SDK/mocks consistent
One place.
<!--/QUIZ-->
