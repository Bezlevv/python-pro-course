---
title: Фильтрация, поиск и пагинация
summary: django-filter, SearchFilter, OrderingFilter, классы пагинации — как отдавать клиенту только нужные данные.
order: 5
duration: 30 мин
difficulty: advanced
tags: drf, фильтрация, поиск, пагинация, django-filter
---

Крупное API не может отдавать клиенту все записи подряд: их могут быть тысячи, и это медленно. DRF решает это тремя механизмами: **фильтрация** (выборка по точным значениям), **поиск** (подстрока в текстовых полях), **пагинация** (разбиение ответа на страницы). Разберём каждый.

## Фильтрация через django-filter

Точная фильтрация по значениям полей делается пакетом **`django-filter`**:

```bash
pip install django-filter
```

```python
# settings.py
INSTALLED_APPS = [
    ...
    "django_filters",
]

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
}
```

Теперь у вьюхи появится параметр `filterset_fields`:

```python
from django_filters.rest_framework import DjangoFilterBackend


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["author", "published"]
```

Клиент может запросить:

```
GET /api/books/?author=Толстой
GET /api/books/?published=2020&author=Толстой
```

В ответе — только книги, где `author="Толстой"` и `published=2020`. Если нужны более сложные условия (например, «год больше 2000»), создают класс фильтра:

```python
import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):
    published_min = django_filters.NumberFilter(
        field_name="published", lookup_expr="gte")
    published_max = django_filters.NumberFilter(
        field_name="published", lookup_expr="lte")

    class Meta:
        model = Book
        fields = ["author", "published_min", "published_max"]
```

Во вьюхе указываем `filterset_class = BookFilter`, и клиент может писать `?published_min=2000&published_max=2020`.

## Поиск и сортировка

**`SearchFilter`** ищет подстроку в текстовых полях:

```python
from rest_framework.filters import SearchFilter, OrderingFilter


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "author"]
    ordering_fields = ["published", "title"]
```

Запрос `GET /api/books/?search=война` вернёт книги, в названии или авторе которых встречается слово «война». `search_fields` поддерживает нотацию:

- `"title"` — точное совпадение с подстрокой;
- `"^title"` — начало строки;
- `"=title"` — точное совпадение всего значения.

**`OrderingFilter`** сортирует по полям из `ordering_fields`:

```
GET /api/books/?ordering=published
GET /api/books/?ordering=-published
GET /api/books/?ordering=-published,title
```

Знак минус — обратный порядок, запятая — несколько уровней сортировки.

## Пагинация

**Пагинация** делит ответ на страницы. Базовая настройка:

```python
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}
```

Теперь `GET /api/books/` вернёт:

```json
{
  "count": 57,
  "next": "http://.../api/books/?page=2",
  "previous": null,
  "results": [ ... 10 объектов ... ]
}
```

Клиент может ходить по страницам через `?page=2`, `?page=3` и т.д. `count` — общее количество записей, `next`/`previous` — ссылки на соседние страницы.

Иногда нужна нестандартная пагинация. Например, чтобы клиент сам выбирал размер страницы:

```python
from rest_framework.pagination import PageNumberPagination


class BookPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
```

Подключение во вьюхе:

```python
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination
```

Теперь `GET /api/books/?page_size=25` вернёт до 25 записей на странице.

## Курсорная пагинация

Альтернатива `PageNumberPagination` — **`CursorPagination`**. Она использует курсор (зашифрованную позицию) вместо номера страницы и гарантирует стабильность при добавлении новых записей:

```python
from rest_framework.pagination import CursorPagination


class BookCursorPagination(CursorPagination):
    page_size = 10
    ordering = "-id"
```

## Итог

Фильтрация (`django-filter`) убирает лишние записи по точным значениям, поиск (`SearchFilter`) ищет подстроки, сортировка (`OrderingFilter`) расставляет порядок, а пагинация делит ответ на страницы. Вместе они делают API быстрым и удобным для клиентов. В заключительном уроке мы напишем тесты на всё это.

<!--TASK-->
### Задача 1
Установи `django-filter`, добавь `django_filters` в `INSTALLED_APPS` и подключи `DjangoFilterBackend` в `REST_FRAMEWORK`. Для `BookViewSet` добавь `filter_backends = [DjangoFilterBackend]` и `filterset_fields = ["author", "published"]`. Проверь через curl: `GET /api/books/?author=Толстой` должен вернуть только книги этого автора.

### Задача 2
Добавь в `BookViewSet` `SearchFilter` и `OrderingFilter`. Задай `search_fields = ["title", "author"]` и `ordering_fields = ["published", "title"]`. Проверь: `?search=война` находит книги с этим словом, а `?ordering=-published` сортирует по убыванию года.

### Задача 3
Создай класс `BookFilter(django_filters.FilterSet)` с полями `published_min` и `published_max` (lookup_expr: gte/lte) и подключи его через `filterset_class` в вьюхе. Проверь запрос `?published_min=2000&published_max=2010`.

### Задача 4
Включи пагинацию: `DEFAULT_PAGINATION_CLASS = PageNumberPagination` и `PAGE_SIZE = 5`. Создай не меньше 12 книг (циклом или командой в shell) и проверь, что ответ содержит `count`, `next`, `previous`, `results`, а `?page=2` показывает вторую страницу.

### Задача 5
Создай класс `BookPagination(PageNumberPagination)` с `page_size = 10`, `page_size_query_param = "page_size"` и `max_page_size = 50`. Подключи его в `BookViewSet` через `pagination_class`. Проверь: `?page_size=25` возвращает до 25 записей, а `?page_size=999` — не больше 50.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
После `pip install django-filter` добавь `django_filters` в `INSTALLED_APPS`, а `DjangoFilterBackend` — в `DEFAULT_FILTER_BACKENDS`. В классе вьюхи укажи `filter_backends = [DjangoFilterBackend]` и `filterset_fields`.

### Подсказка 2
`SearchFilter` и `OrderingFilter` импортируются из `rest_framework.filters`. В `search_fields` указываются поля, по которым ищется подстрока, в `ordering_fields` — поля для сортировки.

### Подсказка 3
Класс фильтра объявляется так: `class BookFilter(django_filters.FilterSet):` с полями `published_min = django_filters.NumberFilter(field_name="published", lookup_expr="gte")`. Внутри `class Meta` укажи `model = Book` и перечисли доступные поля. Во вьюхе — `filterset_class = BookFilter`.

### Подсказка 4
Настройки добавляются в `REST_FRAMEWORK`: `"DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination"`, `"PAGE_SIZE": 5`. Для массового создания книг используй `Book.objects.bulk_create([...])` в shell.

### Подсказка 5
Класс наследуется от `PageNumberPagination`, атрибуты: `page_size`, `page_size_query_param`, `max_page_size`. Подключение — `pagination_class = BookPagination` внутри вьюхи.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```bash
pip install django-filter
```

```python
# settings.py
INSTALLED_APPS = [
    ...
    "django_filters",
]

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
}
```

```python
# books/views.py
from django_filters.rest_framework import DjangoFilterBackend


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["author", "published"]
```

Что здесь происходит? `DjangoFilterBackend` анализирует query-параметры и превращает их в SQL-условия. `filterset_fields` указывает, какие поля можно использовать для фильтрации. Запрос `?author=Толстой` выполнит выборку с условием `author='Толстой'`. Поля вне списка просто игнорируются.

### Разбор 2
Решение:

```python
from rest_framework.filters import SearchFilter, OrderingFilter


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "author"]
    ordering_fields = ["published", "title"]
```

Что здесь происходит? `SearchFilter` берёт параметр `search` и ищет его как подстроку в полях из `search_fields`, используя регистронезависимый поиск. `OrderingFilter` читает параметр `ordering`: `-published` означает сортировку по убыванию, а список через запятую — несколько критериев.

### Разбор 3
Решение:

```python
# books/filters.py
import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):
    published_min = django_filters.NumberFilter(
        field_name="published", lookup_expr="gte")
    published_max = django_filters.NumberFilter(
        field_name="published", lookup_expr="lte")

    class Meta:
        model = Book
        fields = ["author", "published_min", "published_max"]
```

```python
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter
```

Что здесь происходит? `NumberFilter` с `lookup_expr="gte"` означает «больше или равно», `lte` — «меньше или равно». Запрос `?published_min=2000&published_max=2010` превращается в условие `published >= 2000 AND published <= 2010`. Это намного гибче простого `filterset_fields`.

### Разбор 4
Решение:

```python
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.PageNumberPagination"
    ),
    "PAGE_SIZE": 5,
}
```

Этот подход задаёт пагинацию глобально. Ответ на `GET /api/books/`:

```json
{
  "count": 12,
  "next": "http://127.0.0.1:8000/api/books/?page=2",
  "previous": null,
  "results": [ ... ]
}
```

Что здесь происходит? `PageNumberPagination` делит выборку на страницы по 5 записей. `count` — общее количество, `next`/`previous` — ссылки. Запрос `?page=2` вернёт записи с 6-й по 10-ю.

### Разбор 5
Решение:

```python
from rest_framework.pagination import PageNumberPagination


class BookPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50
```

```python
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination
```

Что здесь происходит? `page_size_query_param` даёт клиенту возможность самому задавать размер страницы. `max_page_size` ограничивает этот размер, чтобы слишком большое значение не нагружало сервер. Теперь `?page_size=25` вернёт по 25 записей, а `?page_size=999` — не больше 50.
<!--/SOLUTION-->

<!--QUIZ-->
Какой пакет отвечает за точную фильтрацию в DRF?
- django-filter
- pandas
- django-jwt
* Правильный ответ: django-filter
DjangoFilterBackend из пакета django-filter фильтрует по значениям полей.

Как включить фильтрацию по полям author и published?
- filterset_fields = ["author", "published"]
- search_fields = ["author", "published"]
- ordering_fields = ["author", "published"]
* Правильный ответ: filterset_fields = ["author", "published"]
filterset_fields указывает поля, по которым возможна фильтрация.

Какой параметр использует SearchFilter?
- ?search=...
- ?q=...
- ?find=...
* Правильный ответ: ?search=...
SearchFilter читает параметр search и ищет подстроку.

Как отсортировать по убыванию года?
- ?ordering=-published
- ?ordering=published
- ?sort=published-desc
* Правильный ответ: ?ordering=-published
Знак минус перед полем означает обратный порядок.

Какой атрибут задаёт поля для сортировки?
- ordering_fields
- sort_fields
- order_by
* Правильный ответ: ordering_fields
OrderingFilter разрешает сортировку только по полям из ordering_fields.

Что содержит ключ count в ответе с пагинацией?
- Общее количество записей
- Номер текущей страницы
- Размер страницы
* Правильный ответ: Общее количество записей
count — суммарное число записей во всей выборке.

Как называется параметр для запроса конкретной страницы?
- page
- offset
- start
* Правильный ответ: page
PageNumberPagination использует ?page=N.

Какой класс пагинации использует зашифрованную позицию?
- CursorPagination
- OffsetPagination
- SlicePagination
* Правильный ответ: CursorPagination
CursorPagination работает с курсорами, а не с номерами страниц.

Что делает page_size_query_param?
- Разрешает клиенту задавать размер страницы
- Ограничивает число страниц
- Скрывает поле page
* Правильный ответ: Разрешает клиенту задавать размер страницы
Например, ?page_size=25 вернёт по 25 записей.

Что ограничивает max_page_size?
- Максимальный размер страницы
- Суммарное число записей
- Максимальное число страниц
* Правильный ответ: Максимальный размер страницы
Даже если клиент запросит 999, больше max_page_size не отдастся.
<!--/QUIZ-->
