---
title: REST API basics
summary: Resources, methods, status codes.
order: 1
duration: 40 min
difficulty: intermediate
tags: rest, api
---

REST structures APIs around resources.

## Methods

- GET — read;
- POST — create;
- PUT/PATCH — update;
- DELETE — remove.

## Examples

```text
GET    /items          → list
GET    /items/1        → one
POST   /items          → create
PUT    /items/1        → update
DELETE /items/1        → delete
```

## Status

200 OK, 201 created, 404 not found, 400 bad request.

## Lesson summary

REST = resources + verbs + codes.

<!--TASK-->
### Task 1 — Verbs
List four methods and roles.

### Task 2 — URL
Design URLs for a /books resource.

### Task 3 — 201
When is 201 used?

### Task 4 — 404
When is 404 used?

### Task 5 — JSON
Sketch a JSON item.

### Task 6 — Idempotent
Which methods are idempotent?

### Task 7 — Stateless
Explain statelessness.
<!--/TASK-->

<!--HINT-->
### Hint 1
CRUD.

### Hint 2
/books.

### Hint 3
Created.

### Hint 4
Missing.

### Hint 5
Keys.

### Hint 6
GET/PUT/DELETE.

### Hint 7
No session.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```text
GET — чтение
POST — создание
PUT — полное обновление
PATCH — частичное обновление
DELETE — удаление
```

### Solution 2
```text
GET /books
GET /books/5
POST /books
PUT /books/5
DELETE /books/5
```

### Solution 3
```text
201 Created — после успешного POST
```

### Solution 4
```text
404 Not Found — ресурс не существует
```

### Solution 5
```json
{"id": 1, "title": "Python", "price": 19.9}
```

### Solution 6
```text
GET, PUT, DELETE — идемпотентны;
POST — нет (создаёт каждый раз)
```

### Solution 7
```text
Каждый запрос самодостаточен:
сервер не хранит состояние клиента
```
<!--/SOLUTION-->

<!--QUIZ-->
What is REST?
- Architectural style
- A framework
- A database
- None
* Correct answer: Architectural style
Resources.

What is GET?
- Read
- Create
- Delete
- None
* Correct answer: Read
Query.

What is POST?
- Create
- Read
- Delete
- None
* Correct answer: Create
Submit.

What is PUT?
- Full update
- Partial
- Read
- None
* Correct answer: Full update
Replace.

What is PATCH?
- Partial update
- Full
- Delete
- None
* Correct answer: Partial update
Fields.

What is DELETE?
- Remove
- Read
- Create
- None
* Correct answer: Remove
Gone.

What is 201?
- Created
- OK
- Not found
- None
* Correct answer: Created
POST.

What is 404?
- Not found
- Created
- OK
- None
* Correct answer: Not found
Missing.

What is a resource?
- Entity
- Method
- Status
- None
* Correct answer: Entity
Item.

What is JSON?
- Data format
- HTML
- CSS
- None
* Correct answer: Data format
Keys.

What is idempotent?
- Same result
- Changes each time
- Error
- None
* Correct answer: Same result
Repeat.

What is stateless?
- No stored state
- Sessions
- Cookies only
- None
* Correct answer: No stored state
Independent.
<!--/QUIZ-->
