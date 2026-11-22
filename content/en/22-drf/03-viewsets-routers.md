---
title: ViewSet and Router
summary: Ready-made views for CRUD: generics, ModelViewSet, Router and custom actions via @action.
order: 3
duration: 35 min
difficulty: advanced
tags: drf, viewsets, routers, generics, crud
---

In the last lesson we wrote views on `APIView` manually: for each method — its own branch of code. But DRF can generate standard CRUD operations (Create, Read, Update, Delete) automatically. In this lesson we will look at `generics`, `ViewSet` and `Router` — tools that cut the amount of code many times over.

## The problem of repetitive code

Look at a typical view for listing and creating objects. It almost always looks the same: get all objects, serialize, return; or accept data, validate, save. For every model you have to write the same thing. DRF solves this with **generic views** and **viewsets** (sets of views).

## Generic views: generics

Classes from `rest_framework.generics` cover typical scenarios. The most popular:

- `ListCreateAPIView` — `GET` (list) + `POST` (creation);
- `RetrieveUpdateDestroyAPIView` — `GET` (single record) + `PUT`/`PATCH` + `DELETE`;
- `RetrieveAPIView` — read-only single record;
- `ListAPIView` — list only.

Here is what full CRUD for a book looks like with `generics`:

```python
# books/views.py
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

Two classes instead of dozens of lines of code! DRF itself:

- queries through `queryset`;
- serializes through `serializer_class`;
- handles `404` if the object does not exist;
- validates data and returns `400` on errors;
- returns `201` on creation.

In `urls.py` we wire up the routes:

```python
from django.urls import path
from books.views import BookListCreateView, BookDetailView

urlpatterns = [
    path("api/books/", BookListCreateView.as_view()),
    path("api/books/<int:pk>/", BookDetailView.as_view()),
]
```

## ViewSet: everything in one class

`generics` is already good, but for one resource we still need two classes. **`ViewSet`** collects all operations into one class:

```python
# books/views.py
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

`ModelViewSet` provides methods: `list` (GET list), `retrieve` (GET one), `create` (POST), `update` (PUT), `partial_update` (PATCH), `destroy` (DELETE). If desired, you can inherit from `ReadOnlyModelViewSet` to get only `list` and `retrieve` — great for read-only APIs.

## Router: routes automatically

Just as `ViewSet` combines operations, `Router` automatically generates all routes for it:

```python
# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books.views import BookViewSet

router = DefaultRouter()
router.register("books", BookViewSet, basename="book")

urlpatterns = [
    path("api/", include(router.urls)),
]
```

Now the routes are available automatically:

- `GET /api/books/` — list;
- `POST /api/books/` — creation;
- `GET /api/books/<pk>/` — one book;
- `PUT /api/books/<pk>/` — full update;
- `PATCH /api/books/<pk>/` — partial update;
- `DELETE /api/books/<pk>/` — deletion.

`basename` is needed for the Router to build URL names for `reverse()`. If you do not specify it, DRF will print a warning, but will try to derive the name from the model.

## Custom actions: @action

Sometimes non-standard operations are needed. That is what the **`@action`** decorator is for:

```python
from rest_framework.decorators import action
from rest_framework.response import Response


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=False, methods=["get"])
    def recent(self, request):
        recent_books = self.get_queryset().order_by("-id")[:5]
        serializer = self.get_serializer(recent_books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None):
        book = self.get_object()
        book.published = 2026
        book.save()
        return Response({"status": "published"})
```

With `detail=False` the action is available at `/api/books/recent/` (no id), and with `detail=True` — at `/api/books/<pk>/publish/`. The `methods` parameter sets the HTTP methods.

```mermaid
flowchart LR
    A["ViewSet"] --> B["Router"]
    B --> C["Route names"]
    C --> D["@action"]
    D --> E["Custom actions"]
```

## Summary

`generics` remove boilerplate code for typical operations, `ViewSet` combines them into one class, and `Router` builds routes automatically. Custom actions via `@action` add their own URLs. In the next lesson we will add authentication and permissions to this.

<!--TASK-->
### Task 1
For the `Book` model write two generic views: `BookListCreateView` (`ListCreateAPIView`) and `BookDetailView` (`RetrieveUpdateDestroyAPIView`). Define the routes `/api/books/` and `/api/books/<int:pk>/`. Test all methods: GET list, POST creation, GET one book, PUT update, DELETE deletion.

### Task 2
Rewrite the same two classes into one `BookViewSet` based on `ModelViewSet`. Connect it via `DefaultRouter` with the `books` prefix. Verify that all CRUD routes work: list, creation, getting one book, update and deletion.

### Task 3
Add a `recent` action to `BookViewSet` with `@action(detail=False, methods=["get"])` that returns the three latest books (sorted by `-id`, slice `[:3]`). Verify that it is available at `/api/books/recent/`.

### Task 4
Add a `publish` action to `BookViewSet` with `@action(detail=True, methods=["post"])` that sets the book's `published = 2026` (or the current year) and returns `{"status": "published"}`. Test via POST to `/api/books/<pk>/publish/`.

### Task 5
Create a `BookViewSet` based on `ReadOnlyModelViewSet` for the `Author` model (field `name`). Make sure only GET methods are available (list and single record), and POST returns `405 Method Not Allowed`. Use curl to test.
### Task 6 — Custom action via @action
Add an action `@action(detail=True, methods=["post"]) def mark_sold(self, request, pk=None)` to `BookViewSet` that sets `book.sold = True`. Check the URL: `books/{pk}/mark_sold/`.
### Task 7 — Using mixins
Write `BookListCreateView` based on `ListModelMixin` + `CreateModelMixin` + `GenericAPIView` with `get_queryset` and `get_serializer_class`.

<!--/TASK-->

<!--HINT-->
### Hint 1
Generic views have two attributes: `queryset` and `serializer_class`. `ListCreateAPIView` provides GET list and POST, `RetrieveUpdateDestroyAPIView` — GET/PUT/PATCH/DELETE for a single record. Routes: `path("api/books/", BookListCreateView.as_view())` and `path("api/books/<int:pk>/", BookDetailView.as_view())`.

### Hint 2
`viewsets.ModelViewSet` contains all six CRUD methods. Router: `router = DefaultRouter(); router.register("books", BookViewSet, basename="book")`, then `path("api/", include(router.urls))`.

### Hint 3
Import `from rest_framework.decorators import action` and `from rest_framework.response import Response`. Inside the action use `self.get_queryset().order_by("-id")[:3]` and `self.get_serializer(books, many=True)`. With `detail=False` the URL will be `/api/books/recent/`.

### Hint 4
With `detail=True` the action receives `pk` in the arguments. Use `self.get_object()` to get the object. The `post` method in `@action` is set via `methods=["post"]`. URL: `/api/books/<pk>/publish/`.

### Hint 5
`ReadOnlyModelViewSet` inherits from `generics.ListAPIView` and `generics.RetrieveAPIView` — it only has `list` and `retrieve`. Creation will return `405`, because the route for POST simply will not be registered.
### Hint 6
@action ends up in router URLs: `books/{pk}/mark_sold/`; the detail=True attribute means a concrete object.
### Hint 7
Mixin classes add the list() and create() methods; it is enough to override queryset and serializer_class.

<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
# books/views.py
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

```python
# urls.py
from django.urls import path
from books.views import BookListCreateView, BookDetailView

urlpatterns = [
    path("api/books/", BookListCreateView.as_view()),
    path("api/books/<int:pk>/", BookDetailView.as_view()),
]
```

What is going on here? `ListCreateAPIView` implements list and creation logic itself: `GET` returns all books, `POST` validates data and returns `201`. `RetrieveUpdateDestroyAPIView` handles a single record: `GET` — read, `PUT` — update, `DELETE` — deletion, and automatically returns `404` for a non-existent id.

### Solution 2
Solution:

```python
# books/views.py
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

```python
# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books.views import BookViewSet

router = DefaultRouter()
router.register("books", BookViewSet, basename="book")

urlpatterns = [
    path("api/", include(router.urls)),
]
```

What is going on here? `ModelViewSet` combines methods for all CRUD operations. The Router registers these methods on routes: list and creation — `/api/books/`, working with a single record — `/api/books/<pk>/`. There is no need to write routes manually — the Router does it itself.

### Solution 3
Solution:

```python
from rest_framework.decorators import action
from rest_framework.response import Response


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=False, methods=["get"])
    def recent(self, request):
        books = self.get_queryset().order_by("-id")[:3]
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
```

What is going on here? `@action(detail=False, ...)` creates a new route without id: `/api/books/recent/`. `self.get_queryset()` returns the base queryset, `order_by("-id")` sorts from newest to oldest, and `[:3]` takes the three latest. `self.get_serializer(books, many=True)` creates a serializer with the correct settings from the class.

### Solution 4
Solution:

```python
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None):
        book = self.get_object()
        book.published = datetime.now().year
        book.save()
        return Response({"status": "published", "id": book.id})
```

What is going on here? `detail=True` means the action refers to a specific object, so the URL looks like `/api/books/<pk>/publish/`. `self.get_object()` gets the object by id from the URL and itself returns `404` if it does not exist. We change the publication year, save and return the response.

### Solution 5
Solution:

```python
# books/views.py
from rest_framework import viewsets
from .models import Author
from .serializers import AuthorSerializer


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
```

What is going on here? `ReadOnlyModelViewSet` inherits from `ListAPIView` and `RetrieveAPIView`, so it only knows the `list` and `retrieve` methods — GET list and GET single record. The Router does not create routes for POST/PUT/DELETE, so such requests will return `405 Method Not Allowed`. This is a convenient way to restrict an API to read-only mode.
### Solution 6
```python
from rest_framework.decorators import action
from rest_framework.response import Response

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=True, methods=["post"])
    def mark_sold(self, request, pk=None):
        book = self.get_object()
        book.sold = True
        book.save()
        return Response({"status": "sold"})
```
@action adds a custom action without manual URL routing.
### Solution 7
```python
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import GenericAPIView

class BookListCreateView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```
Mixins carry ready-made list/create logic; the pattern manually replicates ModelViewSet.

<!--/SOLUTION-->

<!--QUIZ-->
Which class combines all CRUD operations into one?
- ModelViewSet
- APIView
- ListAPIView
* Correct answer: ModelViewSet
ModelViewSet contains list, retrieve, create, update, partial_update, destroy.

What does DefaultRouter do?
- Generates routes for ViewSet automatically
- Creates tables in the database
- Checks authorization
* Correct answer: Generates routes for ViewSet automatically
Router.register("books", BookViewSet) creates all standard CRUD routes.

Which class gives only GET list and POST creation?
- ListCreateAPIView
- RetrieveUpdateDestroyAPIView
- APIView
* Correct answer: ListCreateAPIView
ListCreateAPIView is for listing and creating objects.

What will POST return on ReadOnlyModelViewSet?
- 405 Method Not Allowed
- 200 OK
- 404 Not Found
* Correct answer: 405 Method Not Allowed
ReadOnlyModelViewSet has no create, so the route for POST is absent.

What is basename in router.register for?
- Building URL names when calling reverse()
- Naming the database
- The app folder name
* Correct answer: Building URL names when calling reverse()
basename is used in reverse("book-list") and reverse("book-detail").

What does @action(detail=False) do?
- Adds a route without id, e.g. /api/books/recent/
- Adds only the GET method
- Creates a new model
* Correct answer: Adds a route without id, e.g. /api/books/recent/
With detail=False the action is available at the collection level, without pk in the URL.

How to get an object by id inside an action with detail=True?
- self.get_object()
- self.get_pk()
- self.fetch()
* Correct answer: self.get_object()
get_object() fetches the object itself and returns 404 if it does not exist.

Which method does a ViewSet use to get the base queryset?
- get_queryset()
- get_model()
- fetch_all()
* Correct answer: get_queryset()
get_queryset() returns the queryset set in the class attribute.

What will RetrieveUpdateDestroyAPIView return when an object is missing?
- 404 Not Found
- 200 OK
- 500 Internal Server Error
* Correct answer: 404 Not Found
Generic views automatically return 404 for a non-existent id.

How to restrict a ViewSet to read-only?
- Inherit from ReadOnlyModelViewSet
- Remove the get method
- Add a property only_read = True
* Correct answer: Inherit from ReadOnlyModelViewSet
ReadOnlyModelViewSet leaves only list and retrieve.
What does @action do in a ViewSet?
- Adds a custom action that is routed automatically
- Creates a new model
- Replaces list
- Deletes routes
* Correct answer: Adds a custom action that is routed automatically
Router will build the URL for the action itself.

What does detail=True mean in @action?
- The action applies to a concrete object (pk)
- To the list
- To the serializer
- To the route
* Correct answer: The action applies to a concrete object (pk)
It requires pk in the URL.

What do Mixin classes provide?
- Ready-made list/create/update/retrieve/destroy methods
- Nothing
- Only import
- Models
* Correct answer: Ready-made list/create/update/retrieve/destroy methods
Mixins are combined with GenericAPIView.

Which class combines everything — list, create, retrieve, update, delete?
- ModelViewSet
- APIView
- View
- SimpleView
* Correct answer: ModelViewSet
ModelViewSet inherits all Mixins and gives full CRUD.

# 
<!--/QUIZ-->
