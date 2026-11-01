---
title: Django: модели, ORM, админка, формы
summary: Как описывать модели данных, работать с базой через ORM, наполнять админку и создавать формы.
order: 8
duration: 40 мин
difficulty: advanced
---

В прошлом уроке данные жили в обычных списках — так делают только для обучения. В реальном сайте данные хранятся в базе данных, а управляет ей Django с помощью ORM — слоя, который превращает Python-классы в SQL-таблицы. Сегодня научимся работать с моделями, админкой и формами.

## Модели

Модель — это класс, описывающий таблицу. Поле класса — столбец таблицы. Добавим модель книги в `books/models.py`:

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    year = models.IntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

`CharField` — строка, `IntegerField` — целое число, `DateTimeField(auto_now_add=True)` — дата создания записи. Метод `__str__` определяет, как объект выглядит в админке.

## Миграции

Чтобы изменения превратились в таблицы, выполни:

```bash
python manage.py makemigrations books
python manage.py migrate
```

Первая команда создаёт файл миграции (описание изменений), вторая — применяет его к базе. По умолчанию Django использует SQLite — файл `db.sqlite3` рядом с `manage.py`.

## ORM

Работа с данными через Python-объекты:

```python
# создание записи
Book.objects.create(title="Война и мир", author="Лев Толстой", year=1869)

# чтение: все книги
Book.objects.all()

# фильтрация: книги после 2000 года, отсортированные по году
Book.objects.filter(year__gt=2000).order_by("year")

# поиск точного совпадения
Book.objects.get(title="Мастер и Маргарита")

# подсчёт
Book.objects.count()
```

`filter` возвращает QuerySet — ленивую коллекцию: запрос к базе выполняется только когда данные действительно нужны. Двойное подчёркивание (`year__gt`) означает «год больше чем». Всё это можно пробовать в оболочке Django:

```bash
python manage.py shell
```

## Админка

Добавим модель в админку — правка `books/admin.py`:

```python
from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "year")
    search_fields = ("title", "author")
```

Создай суперпользователя и войди на `/admin/`:

```bash
python manage.py createsuperuser
```

Админка сама соберёт интерфейс для просмотра, добавления и редактирования книг.

## Формы

Форма собирает данные от пользователя и проверяет их. Для модели удобно использовать ModelForm:

```python
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "year"]
```

Представление обрабатывает два случая: GET — показать пустую форму, POST — принять данные, проверить и сохранить:

```python
from django.shortcuts import redirect, render
from .forms import BookForm

def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("books")
    else:
        form = BookForm()
    return render(request, "books/add_book.html", {"form": form})
```

## Итог урока

Мы узнали:

- как объявлять модели и какие бывают поля;
- зачем нужны миграции и как их применять;
- как работать с данными через ORM: create, filter, get, order_by;
- как зарегистрировать модель в админке;
- как создать форму на основе модели и обработать её отправку.

Теперь закрепим всё практикой.

<!--TASK-->
### Задача 1

Создай модель `Article` в `articles/models.py`. Она должна наследоваться от `models.Model` и иметь поля: `title` — `CharField(max_length=200)`, `author` — `CharField(max_length=100)`, `published_year` — `IntegerField`, `views_count` — `IntegerField(default=0)`. Добавь метод `__str__`, возвращающий `self.title`. Затем выполни `python manage.py makemigrations articles` и `python manage.py migrate` — после этого в проекте появится файл базы данных `db.sqlite3`.

### Задача 2

Поработай с ORM в оболочке. Запусти `python manage.py shell` и выполни: создай четыре статьи через `Article.objects.create(...)` — две с годом 2019 и две с годом 2023. Проверь `Article.objects.count()` (должно быть 4), `Article.objects.filter(published_year__gte=2020)` (две статьи) и `Article.objects.order_by("-views_count")`. Печатай промежуточные результаты, чтобы увидеть их в оболочке.

### Задача 3

Зарегистрируй модель в админке. В `articles/admin.py` импортируй модель и добавь класс `ArticleAdmin(admin.ModelAdmin)` с `list_display = ("title", "author", "published_year")`, зарегистрированный через декоратор `@admin.register(Article)`. Выполни `python manage.py createsuperuser` и создай аккаунт. Запусти сервер, войди в `http://127.0.0.1:8000/admin/` и добавь 3–4 статьи через интерфейс.

### Задача 4

Напиши представление с фильтрацией. В `articles/views.py` создай функцию `article_list(request)`, которая через ORM достаёт статьи из `Article.objects.filter(published_year__gte=2020).order_by("-views_count")` и передаёт их в `render` с шаблоном `articles/article_list.html`. В шаблоне выведи заголовок и список статей через цикл `{% for %}`: у каждой статьи покажи `title`, `author`, `published_year` и `views_count`.

### Задача 5

Собери всё воедино. Убедись, что модель `Article` создана, миграции применены, админка отображает колонки и наполнена статьями (включая статью 2019 года), а представление `article_list` подключено к главной странице `""` в `articles/urls.py`. Запусти сервер и проверь список: на странице должны быть ТОЛЬКО статьи с 2020 года и позже, отсортированные по убыванию просмотров. Опиши, что ты увидишь в браузере.

<!--/TASK-->

<!--HINT-->
### Подсказка 1

Модель — обычный класс с наследованием от `models.Model`. Поле — атрибут класса с типом поля: `models.CharField(max_length=200)`, `models.IntegerField(default=0)`. После описания модели обязательны `makemigrations articles` и `migrate` — иначе таблицы не создадутся.

### Подсказка 2

В оболочке `python manage.py shell` работает обычный Python. Создание: `Article.objects.create(title="...", author="...", published_year=2023, views_count=10)`. Фильтрация: `Article.objects.filter(published_year__gte=2020)` — `__gte` значит «больше или равно». Для просмотра результата печатай QuerySet или вызывай `list()`.

### Подсказка 3

Админка: создай класс `ArticleAdmin(admin.ModelAdmin)` с `list_display` и зарегистрируй его декоратором `@admin.register(Article)` над классом. Суперпользователь создаётся командой `python manage.py createsuperuser` (логин, почта, пароль). После входа на `/admin/` модель появится в списке.

### Подсказка 4

Запрос пишется цепочкой: `Article.objects.filter(published_year__gte=2020).order_by("-views_count")`. Минус перед полем — сортировка по убыванию. Передай результат в `render` под ключом `articles`. В шаблоне цикл `{% for article in articles %}` и доступ к полям через `article.title`, `article.author` и т.д.

### Подсказка 5

Проверь всю цепочку: модель + миграции + админка + URL `path("", views.article_list)` в `articles/urls.py` + `include` в проекте. Сортировка по убыванию — `order_by("-views_count")`. Статья 2019 года не должна попасть на страницу из-за фильтра `__gte=2020`.

<!--/HINT-->

<!--SOLUTION-->
### Разбор 1

`articles/models.py`:

```python
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_year = models.IntegerField()
    views_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title
```

Разбор по шагам:

- Наследование от `models.Model` сообщает Django, что этот класс — модель, и для него будет создана таблица.
- `CharField(max_length=200)` — строковое поле с ограничением длины; `IntegerField` — целое число; `default=0` задаёт значение по умолчанию для `views_count`.
- `__str__` определяет человекочитаемое представление объекта — оно используется в админке и при печати.
- `python manage.py makemigrations articles` создаёт файл миграции в папке `articles/migrations/` — это описание изменений схемы.
- `python manage.py migrate` применяет миграцию: в проекте появляется `db.sqlite3` с таблицей `articles_article`.

### Разбор 2

В оболочке (`python manage.py shell`):

```python
from articles.models import Article

Article.objects.create(title="Статья 2019-1", author="Аня", published_year=2019, views_count=5)
Article.objects.create(title="Статья 2019-2", author="Аня", published_year=2019, views_count=15)
Article.objects.create(title="Статья 2023-1", author="Петя", published_year=2023, views_count=100)
Article.objects.create(title="Статья 2023-2", author="Петя", published_year=2023, views_count=50)

Article.objects.count()                                  # 4
Article.objects.filter(published_year__gte=2020)          # статьи 2023 года
Article.objects.order_by("-views_count")                  # от самых просматриваемых
```

Разбор по шагам:

- `Article.objects.create(...)` — один вызов, который создаёт объект и сохраняет его в базе.
- `Article.objects.count()` возвращает число записей; `all()` — все записи.
- `filter(published_year__gte=2020)` — условие «год больше или равен 2020»: `__gte` расшифровывается как greater than or equal.
- `order_by("-views_count")` — сортировка по убыванию: минус перед именем поля.
- QuerySet ленив: запрос к базе выполняется только при реальном использовании — например, при печати, итерации или вызове `len()`.

### Разбор 3

`articles/admin.py`:

```python
from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_year")
```

Разбор по шагам:

- `@admin.register(Article)` — декоратор, регистрирующий модель в админке; класс `ArticleAdmin` описывает, как она там выглядит.
- `list_display` — кортеж полей, которые станут колонками в списке объектов: `title`, `author`, `published_year`.
- `python manage.py createsuperuser` — интерактивная команда: логин, почта (можно пропустить), пароль.
- После `runserver` вход на `http://127.0.0.1:8000/admin/` открывает интерфейс, где можно добавлять, редактировать и удалять статьи.
- Админка — бесплатный бонус Django: интерфейс управления данными без единой строки фронтенда.

### Разбор 4

`articles/views.py`:

```python
from django.shortcuts import render
from .models import Article

def article_list(request):
    articles = Article.objects.filter(published_year__gte=2020).order_by("-views_count")
    return render(request, "articles/article_list.html", {"articles": articles})
```

`articles/templates/articles/article_list.html`:

```html
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Статьи</title></head>
<body>
  <h1>Статьи с 2020 года</h1>
  <ul>
    {% for article in articles %}
      <li>{{ article.title }} — {{ article.author }} ({{ article.published_year }}, {{ article.views_count }} просмотров)</li>
    {% endfor %}
  </ul>
</body>
</html>
```

Разбор по шагам:

- Запрос собирается цепочкой: `filter` сначала отбирает статьи с 2020 года, `order_by("-views_count")` затем сортирует результат по убыванию просмотров.
- Фильтрация и сортировка происходят в базе данных, а не в Python, — ORM транслирует вызовы в SQL.
- QuerySet передаётся в шаблон: `{% for article in articles %}` итерируется по записям.
- Поля объекта доступны через точку: `article.title`, `article.author`, `article.published_year`, `article.views_count`.
- Страница показывает только соответствующие условию статьи, уже в нужном порядке.

### Разбор 5

Полная сборка (фрагменты):

`articles/models.py` — модель из задачи 1; `articles/admin.py` — админка из задачи 3; `articles/views.py` — `article_list` из задачи 4.

`articles/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.article_list, name="articles"),
]
```

Разбор по шагам:

- Миграции применены: таблица существует, админка наполнена (включая статью 2019 года — она нужна для проверки фильтра).
- `articles/urls.py` направляет главную страницу на `article_list`; проект подключает это через `include("articles.urls")`.
- В браузере на `http://127.0.0.1:8000/` ты увидишь заголовок «Статьи с 2020 года» и список только тех статей, у которых `published_year >= 2020`.
- Порядок — по убыванию `views_count`: статья с наибольшим числом просмотров первая. Статья 2019 года на страницу не попадёт.
- Если страница пуста — проверь, что в базе есть подходящие статьи: фильтр честно отсекает всё, что не соответствует условию.

<!--/SOLUTION-->

<!--QUIZ-->
От какого класса наследуются все модели Django?
- object
- django.db.models.Model
- BaseModel
- Table
* Правильный ответ: django.db.models.Model
Именно это превращает класс в таблицу базы данных.

Что делают команды makemigrations и migrate?
- Перезапускают сервер
- Превращают модели в таблицы базы данных
- Создают шаблоны
- Устанавливают зависимости
* Правильный ответ: Превращают модели в таблицы базы данных
Первая генерирует файл миграции, вторая применяет его к базе.

Что возвращает Book.objects.filter(year__gt=2000)?
- SQL-строку
- QuerySet — ленивую коллекцию записей
- Один объект
- Список словарей
* Правильный ответ: QuerySet — ленивую коллекцию записей
Запрос к базе выполняется только тогда, когда данные действительно нужны.

Что означает двойное подчёркивание в published_year__gte=2020?
- «больше или равно»
- «больше»
- «равно»
- «меньше»
* Правильный ответ: «больше или равно»
gte — greater than or equal: год >= 2020.

Как отсортировать записи по убыванию просмотров?
- order_by("views_count")
- order_by("-views_count")
- sort("-views_count")
- filter("-views_count")
* Правильный ответ: order_by("-views_count")
Минус перед именем поля — сортировка по убыванию.

Как создать суперпользователя для админки?
- python manage.py admin
- python manage.py createsuperuser
- python manage.py superuser
- django-admin adduser
* Правильный ответ: python manage.py createsuperuser
Он сможет войти в /admin/ и управлять данными.

Что делает auto_now_add=True в DateTimeField?
- Автоматически ставит текущую дату при создании записи
- Обновляет дату при каждом изменении
- Делает поле необязательным
- Хранит дату как строку
* Правильный ответ: Автоматически ставит текущую дату при создании записи
Заполнять это поле вручную не нужно.
<!--/QUIZ-->
