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
**Задача.** Продолжи проект из предыдущего урока. Создай модель `Article` («статья») с полями `title`, `author`, `published_year` (целое) и `views_count` (целое, по умолчанию 0). Выполни миграции. Зарегистрируй модель в админке с выводом колонок `title`, `author`, `published_year`. Создай суперпользователя, войди в `/admin/` и добавь 3–4 статьи. Затем напиши представление `article_list`, которое через ORM достаёт статьи, опубликованные в 2020 году или позже, отсортированные по убыванию просмотров, и выводит их на страницу через шаблон. Запусти сервер и убедись, что страница показывает именно те статьи, которые ты добавил(а) в админке. Опиши ожидаемый результат в браузере.
<!--/TASK-->

<!--HINT-->
Для условия «больше или равно» используй `published_year__gte=2020`, для сортировки по убыванию — `.order_by("-views_count")`. Не забудь про `makemigrations` и `migrate` после создания модели. В шаблоне перебирай статьи циклом `{% for %}`.
<!--/HINT-->

<!--SOLUTION-->
Модель в `articles/models.py`:

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

Команды:

```bash
python manage.py makemigrations articles
python manage.py migrate
python manage.py createsuperuser
```

Админка в `articles/admin.py`:

```python
from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_year")
```

Представление в `articles/views.py`:

```python
from django.shortcuts import render
from .models import Article

def article_list(request):
    articles = Article.objects.filter(published_year__gte=2020).order_by("-views_count")
    return render(request, "articles/article_list.html", {"articles": articles})
```

URL в `articles/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.article_list, name="articles"),
]
```

Шаблон `articles/templates/articles/article_list.html`:

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

Разбор: миграции превращают модель в таблицу в SQLite; `filter(published_year__gte=2020)` оставляет статьи с 2020 года и позже; `order_by("-views_count")` сортирует по убыванию просмотров. Список `articles` попадает в шаблон через контекст, а цикл `{% for %}` выводит каждую статью. Итог: страница показывает только те статьи, которые ты добавил(а) в админке и которые соответствуют условию.
<!--/SOLUTION-->
