---
title: DRF: serializers and viewsets
summary: ModelSerializer, ViewSet, router.
order: 2
duration: 50 min
difficulty: advanced
tags: drf, serializer
---

DRF builds REST APIs quickly.

## Serializer

```python
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "price"]
```

## ViewSet

```python
from rest_framework import viewsets

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

## Router

```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("books", BookViewSet)
# urlpatterns += router.urls
```

## Lesson summary

Serializer + ViewSet + router = full CRUD API.

<!--TASK-->
### Task 1 — Serializer
Create BookSerializer.

### Task 2 — ViewSet
Create BookViewSet.

### Task 3 — Router
Register in a router.

### Task 4 — Fields
Limit serializer fields.

### Task 5 — Validation
Add a custom validate.

### Task 6 — Permission
Add permissions.

### Task 7 — Test
Test with APIRequestFactory.
<!--/TASK-->

<!--HINT-->
### Hint 1
ModelSerializer.

### Hint 2
ModelViewSet.

### Hint 3
DefaultRouter.

### Hint 4
fields.

### Hint 5
validate_title.

### Hint 6
IsAuthenticated.

### Hint 7
APIClient.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "price"]
```

### Solution 2
```python
from rest_framework import viewsets

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

### Solution 3
```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("books", BookViewSet)
urlpatterns = router.urls
```

### Solution 4
```python
class Meta:
    model = Book
    fields = ["id", "title"]
```

### Solution 5
```python
def validate_title(self, value):
    if len(value) < 3:
        raise serializers.ValidationError("too short")
    return value
```

### Solution 6
```python
from rest_framework.permissions import IsAuthenticated

class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
```

### Solution 7
```python
from rest_framework.test import APIClient
client = APIClient()
response = client.get("/books/")
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a serializer?
- Model ↔ JSON
- A view
- A router
- None
* Correct answer: Model ↔ JSON
Conversion.

What is ModelSerializer?
- Auto fields
- Manual
- View
- None
* Correct answer: Auto fields
Meta.

What is a ViewSet?
- CRUD group
- One view
- Router
- None
* Correct answer: CRUD group
ModelViewSet.

What is queryset?
- Data source
- Serializer
- Permission
- None
* Correct answer: Data source
All.

What is a router?
- URL generation
- View
- Serializer
- None
* Correct answer: URL generation
Register.

What is fields?
- Included fields
- Excluded
- Methods
- None
* Correct answer: Included fields
Whitelist.

What is validation?
- Data checks
- Rendering
- Routing
- None
* Correct answer: Data checks
validate_.

What is a permission?
- Access rule
- URL
- Data
- None
* Correct answer: Access rule
Authenticated.

What is APIClient?
- Test client
- Browser
- Router
- None
* Correct answer: Test client
Requests.

What is IsAuthenticated?
- Login required
- Public
- Admin
- None
* Correct answer: Login required
Permission.

What is status 400?
- Bad request
- OK
- Created
- None
* Correct answer: Bad request
Validation.

What is the DRF benefit?
- Fast CRUD
- Slow
- Manual
- None
* Correct answer: Fast CRUD
DRY.
<!--/QUIZ-->
