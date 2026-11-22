---
title: Testing Django apps
summary: TestCase, client, factories.
order: 4
duration: 50 min
difficulty: advanced
tags: django, testing
---

Django provides a test framework.

## TestCase

```python
from django.test import TestCase
from django.urls import reverse
from .models import User

class UserTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="alice")

    def test_page(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "alice")
```

## Run

```bash
python manage.py test
```

## Lesson summary

TestCase + client simulate requests.

<!--TASK-->
### Task 1 — Model test
Create a model and test it.

### Task 2 — setUp
Create data in setUp.

### Task 3 — Client
GET a page.

### Task 4 — Status
Assert 200.

### Task 5 — Contains
Assert content.

### Task 6 — POST
Submit a form.

### Task 7 — Run
Run the test suite.
<!--/TASK-->

<!--HINT-->
### Hint 1
TestCase.

### Hint 2
setUp.

### Hint 3
client.get.

### Hint 4
assertEqual.

### Hint 5
assertContains.

### Hint 6
client.post.

### Hint 7
manage.py test.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from django.test import TestCase
from .models import User

class UserModelTests(TestCase):
    def test_str(self):
        user = User.objects.create(username="alice")
        self.assertEqual(str(user), "alice")
```

### Solution 2
```python
class PageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="alice")
```

### Solution 3
```python
response = self.client.get("/profile/")
```

### Solution 4
```python
self.assertEqual(response.status_code, 200)
```

### Solution 5
```python
self.assertContains(response, "alice")
```

### Solution 6
```python
response = self.client.post("/login/",
                           {"username": "a", "password": "x"})
self.assertEqual(response.status_code, 200)
```

### Solution 7
```bash
python manage.py test
```
<!--/SOLUTION-->

<!--QUIZ-->
What is TestCase?
- Django test base
- A decorator
- A client
- None
* Correct answer: Django test base
Class.

What is setUp?
- Pre-test setup
- Post-test
- Assert
- None
* Correct answer: Pre-test setup
Data.

What is self.client?
- Test client
- Real browser
- Model
- None
* Correct answer: Test client
Requests.

What is get?
- GET request
- POST
- Put
- None
* Correct answer: GET request
Read.

What is post?
- POST request
- GET
- Delete
- None
* Correct answer: POST request
Submit.

What is assertEqual?
- Compares
- Contains
- Raises
- None
* Correct answer: Compares
==.

What is assertContains?
- Checks content
- Status
- Type
- None
* Correct answer: Checks content
Text.

What is reverse?
- URL by name
- Hardcode
- Redirect
- None
* Correct answer: URL by name
Helper.

What is response?
- Result object
- Request
- Model
- None
* Correct answer: Result object
Status.

What is status_code?
- HTTP code
- Body
- Header
- None
* Correct answer: HTTP code
200.

What is a test database?
- Created/isolated
- Real
- Shared
- None
* Correct answer: Created/isolated
Clean.

What is manage.py test?
- Test runner
- Server
- Migrate
- None
* Correct answer: Test runner
Command.
<!--/QUIZ-->
