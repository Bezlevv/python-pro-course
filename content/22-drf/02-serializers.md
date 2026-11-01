---
title: Сериализаторы: валидация и ModelSerializer
summary: Как превращать объекты моделей в JSON и обратно: Serializer, ModelSerializer, валидация полей и объектов.
order: 2
duration: 35 мин
difficulty: advanced
tags: drf, serializers, modelserializer, валидация
---

Сериализаторы — это сердце Django REST Framework. Именно они превращают сложные объекты (модели, queryset-ы) в JSON для ответа и, наоборот, принимают JSON от клиента и превращают его в объекты. В этом уроке мы научимся писать сериализаторы двумя способами: базовый `Serializer` и быстрый `ModelSerializer`, — а также разберёмся с валидацией.

## Зачем нужны сериализаторы

Представь: у тебя есть модель `Book`. Нужно отдать клиенту список книг в JSON. Вручную пришлось бы писать:

```python
books = Book.objects.all()
data = [{"id": b.id, "title": b.title, "author": b.author} for b in books]
```

А если полей двадцать, а ещё есть связанные модели? Вручную это превращается в ад. Сериализатор решает задачу одной строкой:

```python
def book_list(request):
    serializer = BookSerializer(Book.objects.all(), many=True)
    return Response(serializer.data)
```


Дополнительный бонус: сериализаторы умеют **валидировать** входящие данные и создавать/обновлять объекты.

## Serializer: базовый класс

Начнём с базового класса `Serializer`. Он объявляет поля и правила валидации:

```python
# books/serializers.py
from rest_framework import serializers


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    author = serializers.CharField(max_length=100)
    published = serializers.IntegerField(min_value=1500, max_value=2100)
```

Поля работают как формы в Django: `CharField` проверяет длину строки, `IntegerField` — что это число и что оно в заданных пределах. Свойство `read_only=True` означает, что поле нельзя отправить на сервер, но можно вернуть в ответе — удобно для `id`, который присваивает БД.

Используем сериализатор во вьюхе:

```python
# books/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer


class BookListCreateView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            # create() мы напишем ниже
            book = serializer.save()
            return Response(BookSerializer(book).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
```

## Методы create и update

Сам по себе базовый `Serializer` не знает, как сохранять данные. Мы должны написать методы `create()` и `update()`:

```python
class BookSerializer(serializers.Serializer):
    # ... поля ...

    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.author = validated_data.get("author", instance.author)
        instance.published = validated_data.get("published", instance.published)
        instance.save()
        return instance
```

`validated_data` — это словарь с чистыми (проверенными) данными. Метод `save()` во вьюхе вызывает `create()`, если объекта ещё нет, и `update()` — если он есть.

## ModelSerializer: меньше кода

В 90% случаев поля сериализатора совпадают с полями модели. Для этого есть **`ModelSerializer`** — он сам генерирует поля из модели:

```python
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "published"]
```

Можно использовать `fields = "__all__"`, чтобы включить все поля модели, или `exclude = ["id"]`, чтобы исключить ненужные. `ModelSerializer` сам создаёт `create()` и `update()` — писать их вручную не нужно.

Почему `ModelSerializer` лучше базового? Он:

- берёт типы полей из модели (например, `CharField(max_length=200)` автоматически);
- подхватывает ограничения модели (`unique=True`, `blank=True`);
- сам пишет `create()` и `update()`;
- реже содержит ошибки, потому что не расходится с моделью.

## Валидация: три уровня

**1. Валидация поля.** Метод с именем `validate_<поле>`:

```python
def validate_published(self, value):
    if value > 2026:
        raise serializers.ValidationError("Год не может быть в будущем")
    return value
```

**2. Валидация объекта.** Метод `validate` получает весь словарь данных и проверяет поля вместе:

```python
def validate(self, attrs):
    if attrs.get("author") == attrs.get("title"):
        raise serializers.ValidationError("Автор не может совпадать с названием")
    return attrs
```

Любая ошибка из этих методов попадает в `serializer.errors` и вернётся клиенту в ответе с кодом `400`.

**3. Валидаторы на уровне поля.** Список `validators`:

```python
def no_profanity(value):
    if "запретное" in value.lower():
        raise serializers.ValidationError("Некорректное слово")

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "published"]
        extra_kwargs = {
            "title": {"validators": [no_profanity]},
        }
```

## Итог

Сериализаторы превращают модели в JSON и обратно. Базовый `Serializer` даёт полный контроль, а `ModelSerializer` экономит время и уменьшает вероятность ошибок. Валидация бывает на уровне поля, объекта и через отдельные функции-валидаторы. В следующем уроке мы посмотрим, как писать готовые вьюхи для работы с моделями без ручного кода.

<!--TASK-->
### Задача 1
Для модели `Book` (поля `title`, `author`, `published`) создай сериализатор на базе `ModelSerializer` с полями `["id", "title", "author", "published"]`. Напиши вьюху на базе `APIView`, которая на `GET` возвращает список всех книг (с `many=True`), а на `POST` — создаёт книгу из `request.data` и возвращает `201`. Проверь оба метода.

### Задача 2
Создай сериализатор на базе класса `Serializer` для модели `Book` (без `ModelSerializer`). Реализуй методы `create()` и `update()` вручную. Напиши вьюху, которая поддерживает `GET` (список), `POST` (создание) и `PUT` (обновление книги по id из `kwargs`). Убедись, что PUT-запрос обновляет существующую запись.

### Задача 3
Добавь в сериализатор `BookSerializer` на базе `ModelSerializer` метод `validate_published`, который запрещает год больше текущего (используй `datetime.now().year`). Убедись, что при попытке создать книгу с годом 2100 сериализатор возвращает ошибку, а вьюха — `400 Bad Request`.

### Задача 4
Добавь в `BookSerializer` метод `validate`, который запрещает создавать книгу, где `author` совпадает с `title` (ироничный случай). Проверь: при отправке таких данных `serializer.errors` должен содержать ошибку, и вьюха должна вернуть `400`.

### Задача 5
Используй `extra_kwargs` в `ModelSerializer`, чтобы сделать поле `published` необязательным (с дефолтом 2000) и добавить валидатор, запрещающий пустой заголовок `title`. Подсказка: для дефолта нужен `"default": 2000` в `extra_kwargs` для поля `published`. Проверь, что книга без `published` создаётся с годом 2000.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
`ModelSerializer` объявляется так: `class BookSerializer(serializers.ModelSerializer):` с вложенным `class Meta:`. Во вьюхе для списка передай `many=True`: `BookSerializer(Book.objects.all(), many=True)`. Для создания — `BookSerializer(data=request.data)`, затем `is_valid()` и `save()`.

### Подсказка 2
Базовый `Serializer` не умеет сохранять — напиши `create(self, validated_data)` и `update(self, instance, validated_data)`. Во вьюхе для PUT используй `kwargs.get("pk")` и `Book.objects.get(pk=pk)`; для `update` передай объект в сериализатор: `BookSerializer(book, data=request.data, partial=False)`.

### Подсказка 3
Метод валидации поля: `def validate_published(self, value):`. Если `value > datetime.now().year` — подними `serializers.ValidationError("...")`. Ошибку нужно вернуть через `raise`, а не через `return`.

### Подсказка 4
Метод `validate(self, attrs)` получает словарь данных. Сравни `attrs.get("author")` и `attrs.get("title")`. Если они равны — `raise serializers.ValidationError("...")`. Ошибка появится в `serializer.errors` под ключом `non_field_errors`.

### Подсказка 5
В `class Meta` добавь `extra_kwargs = {"published": {"default": 2000}}`. Для валидатора заголовка создай функцию-валидатор и укажи её в `extra_kwargs` для `title`: `{"validators": [validate_title]}`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
# books/serializers.py
from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "published"]
```

```python
# books/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer


class BookListCreateView(APIView):
    def get(self, request):
        serializer = BookSerializer(Book.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
```

Что здесь происходит? `ModelSerializer` сам описывает поля из модели, а также умеет создавать и обновлять объекты. Во вьюхе мы используем `many=True` для списка, а для создания — проверяем `is_valid()` и вызываем `save()`. `serializer.data` содержит данные в формате, готовом для JSON.

### Разбор 2
Решение:

```python
# books/serializers.py
from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    author = serializers.CharField(max_length=100)
    published = serializers.IntegerField()

    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.author = validated_data.get("author", instance.author)
        instance.published = validated_data.get("published", instance.published)
        instance.save()
        return instance
```

Что здесь происходит? Базовый `Serializer` только описывает формат данных. Метод `create` создаёт новый объект модели, `update` обновляет существующий: `validated_data.get("title", instance.title)` берёт новое значение, а если его не прислали — оставляет старое. Во вьюхе мы передаём объект в сериализатор при обновлении: `BookSerializer(book, data=request.data)`.

### Разбор 3
Решение:

```python
from datetime import datetime
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "published"]

    def validate_published(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError(
                "Год не может быть в будущем")
        return value
```

Что здесь происходит? DRF вызывает метод `validate_published` после базовой проверки поля. Если `raise serializers.ValidationError(...)` — сериализатор заносит текст ошибки в `errors` и `is_valid()` возвращает `False`. Вьюха возвращает `400 Bad Request` с этим списком ошибок.

### Разбор 4
Решение:

```python
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "published"]

    def validate(self, attrs):
        if attrs.get("author") == attrs.get("title"):
            raise serializers.ValidationError(
                "Автор не может совпадать с названием")
        return attrs
```

Что здесь происходит? Метод `validate` вызывается после проверки всех полей по отдельности. Он получает весь словарь `attrs`. Ошибка, поднятая здесь, попадает в `errors["non_field_errors"]`, потому что она относится ко всему объекту, а не к конкретному полю. Такая валидация нужна, когда поля зависят друг от друга.

### Разбор 5
Решение:

```python
def validate_title(value):
    if not value.strip():
        raise serializers.ValidationError("Заголовок не может быть пустым")


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "published"]
        extra_kwargs = {
            "title": {"validators": [validate_title]},
            "published": {"default": 2000},
        }
```

Что здесь происходит? `extra_kwargs` позволяет переопределить настройки полей без ручного описания. `default` подставляет значение, если клиент не прислал поле. `validators` добавляет функцию-валидатор, которая вызывается при проверке данных. Теперь книга без `published` создастся с годом 2000, а пустой заголовок будет отклонён.
<!--/SOLUTION-->

<!--QUIZ-->
Что делает ModelSerializer?
- Генерирует поля из модели автоматически
- Только проверяет данные на корректность
- Заменяет собой базу данных
* Правильный ответ: Генерирует поля из модели автоматически
ModelSerializer сам создаёт поля, create() и update() на основе модели.

Какой метод нужно реализовать в базовом Serializer, чтобы сохранять новый объект?
- create()
- save_all()
- commit()
* Правильный ответ: create()
Метод create(validated_data) вызывается при save(), когда объекта ещё нет.

Что означает read_only=True у поля?
- Поле нельзя отправить на сервер, но можно вернуть в ответе
- Поле нельзя вывести в ответе
- Поле можно только читать с диска
* Правильный ответ: Поле нельзя отправить на сервер, но можно вернуть в ответе
read_only-поля игнорируются при валидации входящих данных, но попадают в ответ.

Где окажется ошибка из метода validate()?
- В errors["non_field_errors"]
- В errors["title"]
- В отдельном файле лога
* Правильный ответ: В errors["non_field_errors"]
Ошибки уровня объекта попадают в ключ non_field_errors.

Какой код возвращает вьюха при невалидных данных сериализатора?
- 200 OK
- 400 Bad Request
- 500 Internal Server Error
* Правильный ответ: 400 Bad Request
Невалидные данные — ошибка клиента, ей соответствует 400.

Что вернёт serializer.errors после неудачной валидации?
- Список ошибок по полям
- Пустую строку
- Сам объект модели
* Правильный ответ: Список ошибок по полям
errors — это словарь, где ключ — имя поля, значение — список ошибок.

Для чего нужен параметр many=True?
- Чтобы сериализовать сразу несколько объектов (список)
- Чтобы разрешить только метод GET
- Чтобы включить отладку
* Правильный ответ: Чтобы сериализовать сразу несколько объектов (список)
С many=True сериализатор работает с queryset-ом, а не с одним объектом.

Как превратить список полей модели в "__all__"?
- fields = "__all__"
- all = True
- include = "*"
* Правильный ответ: fields = "__all__"
Значение "__all__" включает в сериализатор все поля модели.

Что делает метод save() у сериализатора?
- Вызывает create() или update() в зависимости от наличия объекта
- Сохраняет данные в файл
- Проверяет пароль
* Правильный ответ: Вызывает create() или update() в зависимости от наличия объекта
Если объект передан — update(), если нет — create().

Как называется метод валидации конкретного поля title?
- validate_title
- check_title
- field_title
* Правильный ответ: validate_title
DRF ищет метод validate_<имя_поля> и вызывает его после базовой проверки.
<!--/QUIZ-->
