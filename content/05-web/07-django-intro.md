---
title: Django: проект и приложения
summary: Что такое Django, чем проект отличается от приложения, первые представления, маршруты и шаблоны.
order: 7
duration: 35 мин
difficulty: intermediate
---

Django — самый известный веб-фреймворк Python. Его часто называют «батарейки включены»: внутри уже есть почти всё, что нужно для сайта — ORM для работы с базой данных, админка, формы, защита от распространённых атак. В этом уроке ты сделаешь свой первый проект и поймёшь архитектуру Django.

## Проект и приложение

В Django два ключевых понятия:

- **Проект** (project) — это весь сайт целиком: настройки, список URL, общая конфигурация.
- **Приложение** (app) — отдельный функциональный модуль внутри проекта, например «блог», «магазин» или «отзывы».

Создадим проект и приложение:

```bash
django-admin startproject mysite
cd mysite
python manage.py startapp books
```

После `startproject` появляется `manage.py` — главная утилита, и папка `mysite` с настройками. Приложение `books` появляется рядом.

## Первое представление

Представление (view) — это функция, которая получает запрос и возвращает ответ. Открой `books/views.py`:

```python
from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>Библиотека</h1><p>Привет, Django!</p>")
```

Подключим URL приложения. В `mysite/urls.py`:

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("books.urls")),
]
```

А в новом файле `books/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
```

Теперь запусти сервер:

```bash
python manage.py runserver
```

Открой `http://127.0.0.1:8000/` — увидишь заголовок «Библиотека».

## Настройки и регистрация приложения

Чтобы Django знал о приложении, добавь его в `INSTALLED_APPS` в `settings.py`:

```python
INSTALLED_APPS = [
    # ... встроенные приложения ...
    "books",
]
```

Правило простое: не зарегистрировал приложение — Django его «не видит» (шаблоны, админка, миграции).

## Шаблоны

Код HTML обычно не пишут в представлениях — для этого есть шаблоны. Создай папку `books/templates/books/` и файл `index.html`:

```html
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Библиотека</title></head>
<body>
  <h1>{{ heading }}</h1>
  <ul>
    {% for book in books %}
      <li>{{ book }}</li>
    {% endfor %}
  </ul>
</body>
</html>
```

Двойные фигурные скобки `{{ }}` выводят переменные, а `{% %}` — управляющие конструкции вроде циклов. Обновим представление:

```python
from django.shortcuts import render

def index(request):
    books = ["Война и мир", "Мастер и Маргарита", "1984"]
    return render(request, "books/index.html", {"heading": "Библиотека", "books": books})
```

`render` собирает страницу из шаблона и словаря контекста.

## Как работает запрос

Когда браузер открывает страницу, Django сопоставляет URL с правилом из `urls.py`, вызывает представление, а оно возвращает ответ (часто — результат `render`). Это классический паттерн MVT: модель — представление — шаблон. Про модели мы поговорим подробнее в следующем уроке, а пока данные у нас просто в списке.

## Итог урока

Мы узнали:

- чем проект отличается от приложения и как их создать;
- как написать представление и подключить его URL;
- зачем нужна регистрация в `INSTALLED_APPS`;
- как с помощью шаблонов выводить данные на страницу;
- как запускать сервер разработки.

Теперь закрепим всё практикой.

<!--TASK-->
**Задача.** В проекте `mysite` из урока создай приложение `articles` («статьи»). Напиши представление `news`, которое через `render` показывает страницу с заголовком «Новости» и списком трёх-четырёх статей (просто массив строк в `views.py`). Подключи URL: главная страница `""` должна вести на это представление. Зарегистрируй приложение в `INSTALLED_APPS`. Запусти `python manage.py runserver` и убедись, что на `http://127.0.0.1:8000/` открывается твоя страница с заголовком и списком. Опиши, что именно ты должен увидеть в браузере.
<!--/TASK-->

<!--HINT-->
Не забудь создать файл `articles/urls.py` и добавить `path("", include("articles.urls"))` в общий `urls.py`. Шаблон лежит в `articles/templates/articles/news.html`, а имя шаблона в `render` — `"articles/news.html"`. Проверь, что `"articles"` есть в `INSTALLED_APPS`.
<!--/HINT-->

<!--SOLUTION-->
Создание приложения:

```bash
python manage.py startapp articles
```

`articles/views.py`:

```python
from django.shortcuts import render

def news(request):
    articles = [
        "Первая статья: как работает HTTP",
        "Вторая статья: что такое ORM",
        "Третья статья: основы шаблонов",
    ]
    return render(request, "articles/news.html", {"title": "Новости", "articles": articles})
```

`articles/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.news, name="news"),
]
```

`mysite/urls.py`:

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("articles.urls")),
]
```

В `settings.py` добавь строку `"articles"` в `INSTALLED_APPS`.

Шаблон `articles/templates/articles/news.html`:

```html
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>{{ title }}</title></head>
<body>
  <h1>{{ title }}</h1>
  <ul>
    {% for article in articles %}
      <li>{{ article }}</li>
    {% endfor %}
  </ul>
</body>
</html>
```

Запуск:

```bash
python manage.py runserver
```

Разбор шагов: `startapp` создаёт структуру приложения; `views.news` формирует контекст и вызывает `render`, который наполняет шаблон данными; `include("articles.urls")` делегирует обработку корневого адреса приложению; без записи в `INSTALLED_APPS` шаблоны и команды приложения могут не найтись. В браузере на `http://127.0.0.1:8000/` ты должен увидеть заголовок «Новости» и три пункта списка с названиями статей.
<!--/SOLUTION-->
