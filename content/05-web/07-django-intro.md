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
### Задача 1

Создай проект и приложение. Установи Django: `pip install django`. Затем выполни `django-admin startproject mysite`, перейди в папку `cd mysite` и создай приложение `python manage.py startapp articles`. Изучи структуру: файл `manage.py` — главная утилита, папка `mysite` — настройки проекта, папка `articles` — будущее приложение. Запусти сервер `python manage.py runserver` и убедись, что проект стартует без ошибок.

### Задача 2

Создай первое представление. В `articles/views.py` напиши функцию `hello(request)`, которая возвращает `HttpResponse("<h1>Привет, Django!</h1>")`. Создай файл `articles/urls.py` и подключи маршрут `path("", views.hello, name="hello")`. В `mysite/urls.py` добавь `path("", include("articles.urls"))`. Запусти сервер и проверь `http://127.0.0.1:8000/` — должен показаться заголовок «Привет, Django!».

### Задача 3

Зарегистрируй приложение. Открой `mysite/settings.py` и добавь строку `"articles"` в список `INSTALLED_APPS`. Затем переведи представление с `HttpResponse` на шаблоны: создай папку `articles/templates/articles/` и файл `hello.html` с заголовком `<h1>{{ heading }}</h1>`. Обнови функцию `hello`, чтобы она вызывала `render(request, "articles/hello.html", {"heading": "Привет, Django!"})`. Проверь в браузере.

### Задача 4

Выведи список данных. В `articles/views.py` измени функцию `hello`: создай список из трёх строк — названий статей — и передай его в `render` как `articles`. В `hello.html` под заголовком добавь `<ul>`, внутри которого цикл `{% for article in articles %}` и `<li>{{ article }}</li>`. Обнови страницу: под заголовком появится маркированный список из трёх пунктов.

### Задача 5

Собери финальное приложение. Переименуй функцию в `news` (или оставь `hello`), но сделай так: представление `news` рендерит `articles/news.html` с заголовком «Новости» и списком из трёх-четырёх статей. Шаблон должен выводить заголовок и список. Проверь, что приложение зарегистрировано в `INSTALLED_APPS`, и главная страница `""` ведёт на это представление. Запусти сервер и опиши, что именно ты увидишь в браузере.

<!--/TASK-->

<!--HINT-->
### Подсказка 1

`django-admin startproject mysite` создаёт папку проекта, `python manage.py startapp articles` — приложение внутри него. Обе команды выполняются из правильных директорий: вторая — только после `cd mysite`. Сервер запускается командой `python manage.py runserver`.

### Подсказка 2

Представление — обычная функция: `def hello(request): return HttpResponse("...")`. Для URL приложения создавай отдельный файл `urls.py` с `urlpatterns = [path("", views.hello, name="hello")]`, а в проекте подключай его через `include`. Импорт: `from django.urls import path`, `from . import views`.

### Подсказка 3

Без записи в `INSTALLED_APPS` Django не видит шаблоны приложения. Папка шаблонов — `articles/templates/articles/`, путь в `render` — `"articles/hello.html"`. Контекст передаётся словарём: `{"heading": "..."}`.

### Подсказка 4

Список передаётся в контексте: `{"heading": ..., "articles": articles}`. В шаблоне цикл `{% for article in articles %}` обязательно закрывается `{% endfor %}`. Вывод переменной — `{{ article }}`.

### Подсказка 5

Проверь цепочку: `mysite/urls.py` → `include("articles.urls")` → `articles/urls.py` → `path("", views.news)`. Имя шаблона в `render` должно совпадать с реальным файлом. В браузере на `http://127.0.0.1:8000/` должен открыться твой список новостей.

<!--/HINT-->

<!--SOLUTION-->
### Разбор 1

```bash
pip install django
django-admin startproject mysite
cd mysite
python manage.py startapp articles
python manage.py runserver
```

Разбор по шагам:

- `pip install django` ставит фреймворк; после этого в системе появляется команда `django-admin`.
- `django-admin startproject mysite` создаёт папку проекта с файлом `manage.py` и папкой `mysite` (настройки, корневой `urls.py`, `settings.py`).
- `cd mysite` — обязательный переход внутрь проекта: команды `manage.py` выполняются из его корня.
- `python manage.py startapp articles` создаёт приложение — папку с `views.py`, `models.py`, `admin.py` и другими файлами.
- `python manage.py runserver` поднимает сервер разработки на `http://127.0.0.1:8000`. Пустая страница «It worked!» означает, что проект состоялся.

### Разбор 2

`articles/views.py`:

```python
from django.http import HttpResponse

def hello(request):
    return HttpResponse("<h1>Привет, Django!</h1>")
```

`articles/urls.py` (новый файл):

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.hello, name="hello"),
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

Разбор по шагам:

- `HttpResponse` превращает строку в HTTP-ответ; кириллица допустима напрямую.
- `articles/urls.py` — таблица маршрутов приложения: `path("", views.hello, name="hello")` связывает корневой адрес приложения с представлением.
- В `mysite/urls.py` строка `path("", include("articles.urls"))` делегирует обработку корневого адреса приложению `articles`.
- Так устроена схема: проект держит общие настройки, приложение — свои URL, которые подключаются через `include`.
- При запросе `/` Django найдёт правило, вызовет `hello`, и браузер покажет заголовок.

### Разбор 3

`mysite/settings.py` (фрагмент):

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    # ... остальные встроенные ...
    "articles",
]
```

`articles/templates/articles/hello.html`:

```html
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Приветствие</title></head>
<body>
  <h1>{{ heading }}</h1>
</body>
</html>
```

`articles/views.py`:

```python
from django.shortcuts import render

def hello(request):
    return render(request, "articles/hello.html", {"heading": "Привет, Django!"})
```

Разбор по шагам:

- Запись `"articles"` в `INSTALLED_APPS` регистрирует приложение: без этого Django не найдёт ни шаблоны, ни миграции, ни админку.
- Шаблоны лежат в `articles/templates/articles/`. Вложенная папка с именем приложения избегает конфликтов имён между разными приложениями.
- `render(request, "articles/hello.html", {"heading": "Привет, Django!"})` — сборка страницы: шаблон + словарь контекста.
- В шаблоне `{{ heading }}` выводит значение из контекста. HTML переехал из Python в шаблон — разделение логики и представления.

### Разбор 4

`articles/views.py`:

```python
from django.shortcuts import render

def hello(request):
    articles = ["Как работает HTTP", "Что такое ORM", "Основы шаблонов"]
    return render(request, "articles/hello.html", {"heading": "Привет, Django!", "articles": articles})
```

`articles/templates/articles/hello.html`:

```html
<h1>{{ heading }}</h1>
<ul>
    {% for article in articles %}
        <li>{{ article }}</li>
    {% endfor %}
</ul>
```

Разбор по шагам:

- Список передаётся в контексте под ключом `articles`; в шаблоне он доступен как переменная.
- Цикл `{% for article in articles %}` перебирает элементы; для каждого выполняется тело — `<li>{{ article }}</li>`.
- Конструкция закрывается `{% endfor %}`; без этого Django вернёт ошибку рендера.
- Итог — `<ul>` с тремя пунктами. Одна и та же страница покажет любое количество статей, если список станет длиннее.
- Так связываются данные из Python и разметка: представление готовит данные, шаблон их показывает.

### Разбор 5

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

`articles/templates/articles/news.html`:

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

Разбор по шагам:

- `news` принимает запрос, строит список статей и передаёт его в шаблон через `render`. Путь `"articles/news.html"` обязан совпадать с реальным расположением файла.
- `articles/urls.py` направляет корневой адрес приложения на `views.news`; `mysite/urls.py` подключает всё через `include("articles.urls")`.
- Приложение зарегистрировано в `INSTALLED_APPS` (см. задачу 3) — без этого шаблон не найдётся.
- В браузере на `http://127.0.0.1:8000/` ты увидишь заголовок «Новости» и список из трёх пунктов с названиями статей. Это полноценная страница на Django: URL → представление → шаблон.

<!--/SOLUTION-->

<!--QUIZ-->
Какая команда создаёт новый проект Django?
- python manage.py startapp project
- django-admin startproject mysite
- django start mysite
- python -m django new mysite
* Правильный ответ: django-admin startproject mysite
Утилита django-admin устанавливается вместе с Django.

Что такое представление (view) в Django?
- HTML-шаблон
- Функция, принимающая запрос и возвращающая ответ
- Таблица в базе данных
- Конфигурационный файл
* Правильный ответ: Функция, принимающая запрос и возвращающая ответ
Представление — это Python-функция, которую вызывает Django при обращении к URL.

Куда нужно добавить приложение, чтобы Django его «увидел»?
- В urlpatterns
- В INSTALLED_APPS
- В TEMPLATES
- В DATABASES
* Правильный ответ: В INSTALLED_APPS
Без регистрации Django не найдёт шаблоны и миграции приложения.

Как вывести переменную в Django-шаблоне?
- {% variable %}
- {{ variable }}
- {{% variable %}}
- [variable]
* Правильный ответ: {{ variable }}
Двойные фигурные скобки — вывод значения, {% %} — управляющие конструкции.

Чем проект отличается от приложения?
- Это одно и то же
- Проект — весь сайт целиком, приложение — отдельный модуль внутри проекта
- Приложение больше проекта
- Проект — только фронтенд
* Правильный ответ: Проект — весь сайт целиком, приложение — отдельный модуль внутри проекта
Проект объединяет настройки и несколько приложений.

Какая команда запускает сервер разработки?
- python manage.py launch
- python manage.py runserver
- django-admin runserver
- python run.py
* Правильный ответ: python manage.py runserver
После этого сайт доступен на http://127.0.0.1:8000/.

Что делает функция include() в mysite/urls.py?
- Запускает сервер
- Подключает URL-маршруты другого модуля (например, приложения)
- Создаёт таблицу в базе данных
- Рендерит шаблон
* Правильный ответ: Подключает URL-маршруты другого модуля (например, приложения)
path("", include("articles.urls")) делегирует обработку адресов приложению articles.

В каком файле Django находится список INSTALLED_APPS?
- В manage.py
- В settings.py
- В urls.py
- В views.py
* Правильный ответ: В settings.py
settings.py хранит конфигурацию проекта, включая список установленных приложений.
<!--/QUIZ-->
