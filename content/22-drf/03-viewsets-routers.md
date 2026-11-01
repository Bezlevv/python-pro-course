---
title: ViewSet и Router
summary: Готовые вьюхи для CRUD: generics, ModelViewSet, Router и кастомные действия через @action.
order: 3
duration: 35 мин
difficulty: advanced
tags: drf, viewsets, routers, generics, crud
---

В прошлом уроке мы писали вьюхи на `APIView` вручную: для каждого метода — своя ветка кода. Но DRF умеет генерировать стандартные операции CRUD (Create, Read, Update, Delete) автоматически. В этом уроке разберёмся с `generics`, `ViewSet` и `Router` — инструментами, которые сокращают количество кода в разы.

## Проблема повторяющегося кода

Посмотри на типовую вьюху для списка и создания объектов. Она почти всегда выглядит одинаково: получить все объекты, сериализовать, вернуть; или принять данные, проверить, сохранить. Для каждой модели приходится писать одно и то же. DRF решает это через **generic-вьюхи** (обобщённые) и **viewsets** (наборы вьюх).

## Generic-вьюхи: generics

Классы из `rest_framework.generics` закрывают типовые сценарии. Самые популярные:

- `ListCreateAPIView` — `GET` (список) + `POST` (создание);
- `RetrieveUpdateDestroyAPIView` — `GET` (одна запись) + `PUT`/`PATCH` + `DELETE`;
- `RetrieveAPIView` — только чтение одной записи;
- `ListAPIView` — только список.

Вот как выглядит полный CRUD для книги на `generics`:

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

Два класса вместо десятков строк кода! DRF сам:

- делает выборку через `queryset`;
- сериализует через `serializer_class`;
- обрабатывает `404`, если объекта нет;
- проверяет данные и возвращает `400` при ошибках;
- возвращает `201` при создании.

В `urls.py` подключаем маршруты:

```python
from django.urls import path
from books.views import BookListCreateView, BookDetailView

urlpatterns = [
    path("api/books/", BookListCreateView.as_view()),
    path("api/books/<int:pk>/", BookDetailView.as_view()),
]
```

## ViewSet: всё в одном классе

`generics` — это уже хорошо, но для одного ресурса нам всё ещё нужны два класса. **`ViewSet`** собирает все операции в один класс:

```python
# books/views.py
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

`ModelViewSet` предоставляет методы: `list` (GET списка), `retrieve` (GET одной), `create` (POST), `update` (PUT), `partial_update` (PATCH), `destroy` (DELETE). При желании можно унаследоваться от `ReadOnlyModelViewSet`, чтобы получить только `list` и `retrieve`, — отлично для «только чтение» API.

## Router: маршруты автоматически

Так `ViewSet` объединяет операции, `Router` автоматически генерирует все маршруты для него:

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

Теперь автоматически доступны маршруты:

- `GET /api/books/` — список;
- `POST /api/books/` — создание;
- `GET /api/books/<pk>/` — одна книга;
- `PUT /api/books/<pk>/` — полное обновление;
- `PATCH /api/books/<pk>/` — частичное обновление;
- `DELETE /api/books/<pk>/` — удаление.

`basename` нужен, чтобы Router мог строить имена URL для `reverse()`. Если его не указать, DRF выведет предупреждение, но попытается вывести имя из модели.

## Кастомные действия: @action

Иногда нужны нестандартные операции. Для этого есть декоратор **`@action`**:

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

С `detail=False` действие доступно по адресу `/api/books/recent/` (без id), а с `detail=True` — `/api/books/<pk>/publish/`. Параметр `methods` задаёт HTTP-методы.

## Итог

`generics` убирают шаблонный код для типовых операций, `ViewSet` объединяет их в один класс, а `Router` строит маршруты автоматически. Кастомные действия через `@action` добавляют свои адреса. В следующем уроке мы добавим к этому аутентификацию и права доступа.

<!--TASK-->
### Задача 1
Для модели `Book` напиши две generic-вьюхи: `BookListCreateView` (`ListCreateAPIView`) и `BookDetailView` (`RetrieveUpdateDestroyAPIView`). Пропиши маршруты `/api/books/` и `/api/books/<int:pk>/`. Проверь все методы: GET списка, POST создание, GET одной книги, PUT обновление, DELETE удаление.

### Задача 2
Перепиши те же два класса в один `BookViewSet` на базе `ModelViewSet`. Подключи его через `DefaultRouter` с префиксом `books`. Проверь, что все маршруты CRUD работают: список, создание, получение одной книги, обновление и удаление.

### Задача 3
Добавь в `BookViewSet` действие `recent` с `@action(detail=False, methods=["get"])`, которое возвращает три последние книги (сортировка по `-id`, срез `[:3]`). Проверь, что оно доступно по адресу `/api/books/recent/`.

### Задача 4
Добавь в `BookViewSet` действие `publish` с `@action(detail=True, methods=["post"])`, которое ставит книге `published = 2026` (или текущий год) и возвращает `{"status": "published"}`. Проверь через POST на `/api/books/<pk>/publish/`.

### Задача 5
Создай `BookViewSet` на базе `ReadOnlyModelViewSet` для модели `Author` (поле `name`). Убедись, что доступны только GET-методы (список и одна запись), а POST возвращает `405 Method Not Allowed`. Для проверки используй curl.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
У generic-вьюх два атрибута: `queryset` и `serializer_class`. `ListCreateAPIView` даёт GET списка и POST, `RetrieveUpdateDestroyAPIView` — GET/PUT/PATCH/DELETE одной записи. Маршруты: `path("api/books/", BookListCreateView.as_view())` и `path("api/books/<int:pk>/", BookDetailView.as_view())`.

### Подсказка 2
`viewsets.ModelViewSet` содержит все шесть методов CRUD. Router: `router = DefaultRouter(); router.register("books", BookViewSet, basename="book")`, затем `path("api/", include(router.urls))`.

### Подсказка 3
Импортируй `from rest_framework.decorators import action` и `from rest_framework.response import Response`. Внутри действия используй `self.get_queryset().order_by("-id")[:3]` и `self.get_serializer(books, many=True)`. С `detail=False` адрес будет `/api/books/recent/`.

### Подсказка 4
С `detail=True` действие получает `pk` в аргументах. Для получения объекта используй `self.get_object()`. Метод `post` в `@action` задаётся через `methods=["post"]`. Адрес: `/api/books/<pk>/publish/`.

### Подсказка 5
`ReadOnlyModelViewSet` наследуется от `generics.ListAPIView` и `generics.RetrieveAPIView` — у него есть только `list` и `retrieve`. Создание вернёт `405`, потому что маршрут для POST просто не будет зарегистрирован.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

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

Что здесь происходит? `ListCreateAPIView` сам реализует логику списка и создания: `GET` возвращает все книги, `POST` валидирует данные и возвращает `201`. `RetrieveUpdateDestroyAPIView` обрабатывает одну запись: `GET` — чтение, `PUT` — обновление, `DELETE` — удаление, причём автоматически возвращает `404` для несуществующего id.

### Разбор 2
Решение:

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

Что здесь происходит? `ModelViewSet` объединяет методы для всех операций CRUD. Router регистрирует эти методы на маршрутах: список и создание — `/api/books/`, работа с одной записью — `/api/books/<pk>/`. Вручную писать маршруты не нужно — Router делает это сам.

### Разбор 3
Решение:

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

Что здесь происходит? `@action(detail=False, ...)` создаёт новый маршрут без id: `/api/books/recent/`. `self.get_queryset()` возвращает базовую выборку, `order_by("-id")` сортирует от новых к старым, а `[:3]` берет три последние. `self.get_serializer(books, many=True)` создаёт сериализатор с правильными настройками из класса.

### Разбор 4
Решение:

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

Что здесь происходит? `detail=True` означает, что действие относится к конкретному объекту, поэтому адрес выглядит как `/api/books/<pk>/publish/`. `self.get_object()` получает объект по id из URL и сам возвращает `404`, если его нет. Мы меняем год публикации, сохраняем и возвращаем ответ.

### Разбор 5
Решение:

```python
# books/views.py
from rest_framework import viewsets
from .models import Author
from .serializers import AuthorSerializer


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
```

Что здесь происходит? `ReadOnlyModelViewSet` унаследован от `ListAPIView` и `RetrieveAPIView`, поэтому он знает только методы `list` и `retrieve` — GET списка и GET одной записи. Router не создаёт маршрутов для POST/PUT/DELETE, поэтому такие запросы вернут `405 Method Not Allowed`. Это удобный способ ограничить API режимом «только чтение».
<!--/SOLUTION-->

<!--QUIZ-->
Какой класс объединяет все операции CRUD в один?
- ModelViewSet
- APIView
- ListAPIView
* Правильный ответ: ModelViewSet
ModelViewSet содержит list, retrieve, create, update, partial_update, destroy.

Что делает DefaultRouter?
- Генерирует маршруты для ViewSet автоматически
- Создаёт таблицы в базе данных
- Проверяет авторизацию
* Правильный ответ: Генерирует маршруты для ViewSet автоматически
Router.register("books", BookViewSet) создаёт все стандартные маршруты CRUD.

Какой класс даёт только GET списка и POST создания?
- ListCreateAPIView
- RetrieveUpdateDestroyAPIView
- APIView
* Правильный ответ: ListCreateAPIView
ListCreateAPIView предназначен для списка и создания объектов.

Что вернёт POST на ReadOnlyModelViewSet?
- 405 Method Not Allowed
- 200 OK
- 404 Not Found
* Правильный ответ: 405 Method Not Allowed
ReadOnlyModelViewSet не имеет create, поэтому маршрут для POST отсутствует.

Для чего нужен basename в router.register?
- Для построения имён URL при вызове reverse()
- Для названия базы данных
- Для имени папки приложения
* Правильный ответ: Для построения имён URL при вызове reverse()
basename используется в reverse("book-list") и reverse("book-detail").

Что делает @action(detail=False)?
- Добавляет маршрут без id, например /api/books/recent/
- Добавляет только метод GET
- Создаёт новую модель
* Правильный ответ: Добавляет маршрут без id, например /api/books/recent/
При detail=False действие доступно на уровне коллекции, без pk в URL.

Как получить объект по id внутри действия с detail=True?
- self.get_object()
- self.get_pk()
- self.fetch()
* Правильный ответ: self.get_object()
get_object() сам достаёт объект и возвращает 404, если его нет.

Какой метод использует ViewSet для получения базовой выборки?
- get_queryset()
- get_model()
- fetch_all()
* Правильный ответ: get_queryset()
get_queryset() возвращает queryset, заданный в атрибуте класса.

Что вернёт RetrieveUpdateDestroyAPIView при отсутствии объекта?
- 404 Not Found
- 200 OK
- 500 Internal Server Error
* Правильный ответ: 404 Not Found
Generic-вьюхи автоматически возвращают 404 для несуществующего id.

Как ограничить ViewSet только чтением?
- Наследоваться от ReadOnlyModelViewSet
- Убрать метод get
- Добавить свойство only_read = True
* Правильный ответ: Наследоваться от ReadOnlyModelViewSet
ReadOnlyModelViewSet оставляет только list и retrieve.
<!--/QUIZ-->
