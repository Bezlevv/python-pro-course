---
title: Практикум: верстаем сайт полностью
summary: Собираем всё вместе: семантический HTML, современный CSS, Jinja2-шаблоны и Flask-приложение в одном проекте.
order: 6
duration: 90 мин
difficulty: advanced
tags: проект, html, css, jinja2, flask
---

Финальный урок модуля. Мы соберём **полноценный сайт**: с семантической разметкой, современным CSS на переменных и Flexbox/Grid, Jinja2-шаблонами с наследованием и макросами, Flask-маршрутами и тестами. Это уменьшенная, но настоящая веб-разработка: такой стек ты встретишь в любом проекте на Python.

## План проекта

Делаем мини-блог «Мои заметки»:

- две страницы: главная со списком постов и страница поста;
- форма обратной связи с валидацией;
- адаптивная вёрстка: на широких экранах — контент + боковая панель, на узких — одна колонка;
- тесты на структуру, стили и поведение.

Структура папок:

```
blog/
├── app.py              # Flask-приложение
├── templates/
│   ├── base.html       # каркас с блоками
│   ├── index.html      # главная
│   ├── post.html       # страница поста
│   ├── contact.html    # форма обратной связи
│   ├── macros.html     # макросы (карточка поста)
│   └── partials/
│       └── sidebar.html  # боковая панель
├── static/
│   └── style.css       # все стили
└── tests/
    ├── test_validation.py
    └── test_site.py
```

## Данные

Посты можно хранить просто в списке словарей — для учебного проекта база данных не нужна:

```python
POSTS = [
    {"id": 1, "title": "Почему HTML — это важно",
     "date": "2026-10-15", "text": "..."},
    {"id": 2, "title": "Flexbox против Grid",
     "date": "2026-10-20", "text": "..."},
]

def get_post(post_id):
    return next((p for p in POSTS if p["id"] == post_id), None)
```

## Сборка страницы

Главная страница использует базовый шаблон и макрос карточки:

```html
{% extends "base.html" %}
{% from "macros.html" import post_card %}

{% block title %}Главная{% endblock %}

{% block content %}
    <h1>Мои заметки</h1>
    <div class="cards">
        {% for post in posts %}
            {{ post_card(post) }}
        {% endfor %}
    </div>
{% endblock %}
```

Flask-маршруты:

```python
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", posts=POSTS)

@app.route("/post/<int:post_id>")
def post(post_id):
    item = get_post(post_id)
    if item is None:
        return "Пост не найден", 404
    return render_template("post.html", post=item)
```

## Стили

В `static/style.css` — всё, что мы выучили: переменные в `:root`, карточки на Grid (`repeat(auto-fit, minmax(...))`), каркас на `grid-template-areas`, переходы, медиазапросы для мобильных и тёмной темы.

## Стили: переменные и раскладка

В `static/style.css` соберём всё, что мы выучили, в единый файл. Начни с дизайн-токенов — переменных в `:root`: цвета текста, фона, фирменный акцент, радиусы скругления, отступы. Дальше — базовые стили элементов: типографика, ссылки, кнопки. Затем компоненты: карточки (`.card`), навигация (`.nav`), форма (`.form` и поля), панель (`.sidebar`). Для раскладки карточек на главной используй Grid: `grid-template-columns: repeat(auto-fit, minmax(220px, 1fr))` — сетка сама подстроится под ширину экрана. Для страницы в целом — каркас на `grid-template-areas`: области `header`, `nav`, `main`, `aside`, `footer`, а на мобильных медиазапрос перестраивает его в одну колонку. Не забудь переходы на кнопках и ссылках, `:focus-visible` для клавиатурной навигации и `prefers-reduced-motion`, чтобы уважать пользователей, отключивших анимации в системе. Такой файл — отражение всего модуля: семантика в HTML, стили в CSS, сборка страниц в Jinja2.

## Тестирование

Мы напишем два файла тестов: тест валидации формы (логика + шаблон) и интеграционный тест всего сайта через jinja2 и BeautifulSoup. Такой подход — стандарт в веб-разработке: рендер страниц проверяется автоматически, и любой сломанный тег будет пойман до деплоя.

Приступай. Сайт ждёт!

<!--TASK-->
### Задача 1
Создай структуру проекта из плана (папки `blog/`, `templates/`, `static/`, `tests/`, `templates/partials/`). Напиши `templates/base.html`:

- `<html lang="ru">`, `<meta charset="UTF-8">`, `<meta name="viewport" ...>`;
- `<title>` внутри блока `{% block title %}`;
- `<link rel="stylesheet" href="/static/style.css">`;
- `<header>` с `<nav>` и двумя ссылками: «Главная» (`/`) и «Контакты» (`/contact`);
- `<main>` с блоком `{% block content %}`;
- `<footer>` с копирайтом;
- блок `{% block sidebar %}` в `<aside>`.

Ожидаемый результат: каркас готов, страницы будут наследовать его.

### Задача 2
Создай `templates/macros.html` с макросом `post_card(post)` — карточка поста (класс `card`): внутри — `<article>`, `<h3>` с заголовком, `<time datetime="{{ post.date }}">`, `<p>` с обрезанным текстом (`{{ post.text|truncate(80) }}`), ссылка «Читать» на `/post/{{ post.id }}`. Затем создай `templates/index.html`: `extends base.html`, блок `title` — «Главная», блок `content` — заголовок `<h1>` и цикл по `posts` с `{{ post_card(post) }}`. Напиши скрипт `render_index.py`, который рендерит `index.html` со списком из двух постов и печатает результат. Ожидаемый результат: в HTML две карточки с заголовками и ссылками.

### Задача 3
Создай `templates/post.html` (страница поста): `extends base.html`, блок `title` — `{{ post.title }}`, блок `content` — `<article>` с `<h1>` (заголовок), `<time>`, абзацами текста. Создай `templates/partials/sidebar.html` (блок «Свежие заметки» со списком из трёх ссылок) и подключи его в `base.html` через `{% include "partials/sidebar.html" %}` внутри блока `sidebar`. Затем создай `app.py` с маршрутами `/` и `/post/<int:post_id>` (для неизвестного id — «Пост не найден», статус 404) и списком `POSTS` из трёх постов. Запусти `flask --app app run` и проверь: главная показывает карточки, `/post/1` — пост, `/post/999` — 404.

### Задача 4
Создай `templates/contact.html` — форма обратной связи: поля «Имя» (`text`, `required`, `minlength="2"`), «Email» (`email`, `required`), «Сообщение» (`textarea`, `required`, `minlength="10"`), кнопка отправки. Форма: `action="/contact"`, `method="post"`. В `app.py` добавь маршрут `/contact` (GET — форма, POST — валидация), функцию `validate_contact(data)` (возвращает словарь ошибок: имя < 2 символов, email без `@`, сообщение < 10 символов). При ошибках — рендери `contact.html` с `errors` и сохранёнными `data`; при успехе — «Сообщение отправлено!». Затем напиши `tests/test_validation.py`:

- параметризованный тест `validate_contact` (пустые данные, короткое имя, плохой email, короткое сообщение, валидные данные);
- тест рендера `contact.html` с ошибками через jinja2 + `BeautifulSoup`: в HTML есть `<p class="error">` с текстом ошибки.

Ожидаемый результат: все тесты проходят, форма работает через браузер.

### Задача 5
Напиши интеграционный тест `tests/test_site.py`, который рендерит все страницы сайта через jinja2 и проверяет:

- `index.html`: есть `<header>`, `<nav>`, `<main>`, `<footer>`; в `<nav>` две ссылки; ровно три `<article class="card">`; у каждой карточки есть `<time>` и ссылка «Читать»;
- `post.html`: внутри `<main>` есть `<article>` с `<h1>`;
- `base.html`/все страницы: подключён стиль `<link rel="stylesheet" href="/static/style.css">`, есть `<meta name="viewport" ...>`;
- форма `contact.html`: `method="post"`, `action="/contact"`, у полей «Имя», «Email», «Сообщение» есть `label` с `for`, совпадающим с `id`, и `required`;
- `static/style.css`: есть `:root` с минимум тремя переменными `--color-`, `display: grid` и `display: flex`, `@media`.

Ожидаемый результат: все тесты проходят одной командой `python -m pytest tests/`.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Блоки в `base.html`: `{% block title %}{% endblock %}`, `{% block content %}{% endblock %}`, `{% block sidebar %}{% endblock %}`. Навигация — `<nav><ul><li><a href="/">Главная</a></li>...`. Помни: `{% block %}` без содержимого даст пустое место, которое заполнят наследники.

### Подсказка 2
Макрос получает словарь поста: `{% macro post_card(post) %}` и использует `post.title`, `post.date`, `post.text`, `post.id`. Подключение в `index.html`: `{% from "macros.html" import post_card %}`.

### Подсказка 3
В `post.html` сначала `{% extends "base.html" %}`. В `base.html` внутри `<aside>` поставь `{% include "partials/sidebar.html" %}`. Для 404: `if item is None: return "Пост не найден", 404`.

### Подсказка 4
`validate_contact` возвращает словарь `{"name": "...", "email": "...", "message": "..."}` только для полей с ошибками. При успехе — `if not errors:` возврати «Сообщение отправлено!». В шаблоне: `{% for field, msg in errors.items() %}<p class="error">{{ field }}: {{ msg }}</p>{% endfor %}`.

### Подсказка 5
Для тестов задай фикстуру: `env = Environment(loader=FileSystemLoader("templates"), autoescape=True)`. Для проверки «три карточки»: `len(soup.find_all("article", class_="card")) == 3`. Для стилей читай `static/style.css` и используй `assert` с подстроками.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
`templates/base.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Мои заметки{% endblock %}</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <header>
        <nav aria-label="Главное меню">
            <ul>
                <li><a href="/">Главная</a></li>
                <li><a href="/contact">Контакты</a></li>
            </ul>
        </nav>
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <aside>
        {% block sidebar %}{% endblock %}
    </aside>

    <footer>
        <p>© 2026, Мои заметки</p>
    </footer>
</body>
</html>
```

Что здесь происходит? Это каркас всего сайта: шапка с навигацией, основная область с блоком `content`, боковая панель с блоком `sidebar` и подвал. Дочерние шаблоны заполняют только блоки, а оформление и навигация переиспользуются автоматически. `meta viewport` и подключение стилей в одном месте — не нужно повторять их на каждой странице.

### Разбор 2
`templates/macros.html`:

```html
{% macro post_card(post) %}
    <article class="card">
        <h3>{{ post.title }}</h3>
        <time datetime="{{ post.date }}">{{ post.date }}</time>
        <p>{{ post.text|truncate(80) }}</p>
        <a href="/post/{{ post.id }}">Читать</a>
    </article>
{% endmacro %}
```

`templates/index.html`:

```html
{% extends "base.html" %}
{% from "macros.html" import post_card %}

{% block title %}Главная{% endblock %}

{% block content %}
    <h1>Мои заметки</h1>
    <div class="cards">
        {% for post in posts %}
            {{ post_card(post) }}
        {% endfor %}
    </div>
{% endblock %}
```

`render_index.py`:

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"), autoescape=True)
posts = [
    {"id": 1, "title": "Почему HTML — это важно",
     "date": "2026-10-15", "text": "Семантика — основа."},
    {"id": 2, "title": "Flexbox против Grid",
     "date": "2026-10-20", "text": "Выбираем инструмент."},
]
print(env.get_template("index.html").render(posts=posts))
```

Что здесь происходит? Макрос инкапсулирует разметку карточки. `|truncate(80)` обрезает длинный текст поста. В `index.html` цикл проходит по `posts` и вызывает макрос — два поста дают две карточки. Смена оформления карточки происходит в одном месте — в макросе.

### Разбор 3
`templates/post.html`:

```html
{% extends "base.html" %}

{% block title %}{{ post.title }}{% endblock %}

{% block content %}
    <article>
        <h1>{{ post.title }}</h1>
        <time datetime="{{ post.date }}">{{ post.date }}</time>
        <p>{{ post.text }}</p>
    </article>
{% endblock %}
```

`templates/partials/sidebar.html`:

```html
<h2>Свежие заметки</h2>
<ul>
    <li><a href="/post/1">Почему HTML — это важно</a></li>
    <li><a href="/post/2">Flexbox против Grid</a></li>
    <li><a href="/post/3">Jinja2-макросы</a></li>
</ul>
```

В `base.html` внутри `<aside>`: `{% include "partials/sidebar.html" %}`.

`app.py`:

```python
from flask import Flask, render_template

app = Flask(__name__)

POSTS = [
    {"id": 1, "title": "Почему HTML — это важно",
     "date": "2026-10-15", "text": "Семантика — основа."},
    {"id": 2, "title": "Flexbox против Grid",
     "date": "2026-10-20", "text": "Выбираем инструмент."},
    {"id": 3, "title": "Jinja2-макросы",
     "date": "2026-10-25", "text": "Переиспользование разметки."},
]

def get_post(post_id):
    return next((p for p in POSTS if p["id"] == post_id), None)

@app.route("/")
def index():
    return render_template("index.html", posts=POSTS)

@app.route("/post/<int:post_id>")
def post(post_id):
    item = get_post(post_id)
    if item is None:
        return "Пост не найден", 404
    return render_template("post.html", post=item)
```

Что здесь происходит? `include` вставляет боковую панель во все страницы. Маршрут `/post/<int:post_id>` принимает число из адреса; `get_post` ищет пост, а если его нет — возвращается 404. Так работает простейшая «база данных» на списке словарей.

### Разбор 4
`templates/contact.html` (фрагмент):

```html
{% extends "base.html" %}

{% block title %}Контакты{% endblock %}

{% block content %}
    <h1>Обратная связь</h1>
    {% for field, msg in errors.items() %}
        <p class="error">{{ field }}: {{ msg }}</p>
    {% endfor %}
    <form action="/contact" method="post">
        <label for="name">Имя</label>
        <input id="name" name="name" type="text" required minlength="2"
               value="{{ data.get('name', '') }}">
        <label for="email">Email</label>
        <input id="email" name="email" type="email" required
               value="{{ data.get('email', '') }}">
        <label for="message">Сообщение</label>
        <textarea id="message" name="message" required minlength="10">{{ data.get('message', '') }}</textarea>
        <button type="submit">Отправить</button>
    </form>
{% endblock %}
```

`app.py` дополняется:

```python
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        errors = validate_contact(request.form)
        if not errors:
            return "Сообщение отправлено!"
        return render_template("contact.html", errors=errors,
                               data=request.form)
    return render_template("contact.html", errors={}, data={})

def validate_contact(data):
    errors = {}
    if len(data.get("name", "").strip()) < 2:
        errors["name"] = "Имя должно содержать минимум 2 символа."
    if "@" not in data.get("email", ""):
        errors["email"] = "Введите корректный email."
    if len(data.get("message", "").strip()) < 10:
        errors["message"] = "Сообщение должно быть не короче 10 символов."
    return errors
```

`tests/test_validation.py`:

```python
import pytest
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

from app import validate_contact

@pytest.mark.parametrize("data, expected", [
    ({}, {"name", "email", "message"}),
    ({"name": "А", "email": "a@b.ru", "message": "x" * 10}, {"name"}),
    ({"name": "Аня", "email": "нет", "message": "x" * 10}, {"email"}),
    ({"name": "Аня", "email": "a@b.ru", "message": "короткое"},
     {"message"}),
    ({"name": "Аня", "email": "a@b.ru", "message": "x" * 20}, set()),
])
def test_validate_contact(data, expected):
    assert set(validate_contact(data)) == expected


def test_contact_template_renders_errors():
    env = Environment(loader=FileSystemLoader("templates"), autoescape=True)
    html = env.get_template("contact.html").render(
        errors={"email": "Введите корректный email."}, data={})
    soup = BeautifulSoup(html, "html.parser")
    error = soup.find("p", class_="error")
    assert error is not None
    assert "Введите корректный email." in error.get_text()
```

Что здесь происходит? Валидация проверяет три поля и возвращает словарь ошибок. Параметризованный тест проверяет пять сценариев. Тест рендера убеждается, что ошибка выводится в `<p class="error">`. Данные из `data` подставляются обратно в поля — пользователь не теряет ввод.

### Разбор 5
`tests/test_site.py`:

```python
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader


def make_env():
    return Environment(loader=FileSystemLoader("templates"), autoescape=True)


def render(template_name, env=None, **context):
    env = env or make_env()
    return env.get_template(template_name).render(**context)


POSTS = [
    {"id": 1, "title": "A", "date": "2026-10-15", "text": "x" * 10},
    {"id": 2, "title": "B", "date": "2026-10-20", "text": "x" * 10},
    {"id": 3, "title": "C", "date": "2026-10-25", "text": "x" * 10},
]


def test_index_structure():
    soup = BeautifulSoup(render("index.html", posts=POSTS), "html.parser")
    assert soup.find("header") and soup.find("nav")
    assert soup.find("main") and soup.find("footer")
    assert len(soup.find("nav").find_all("a")) == 2
    cards = soup.find_all("article", class_="card")
    assert len(cards) == 3
    for card in cards:
        assert card.find("time") is not None
        link = card.find("a", string="Читать")
        assert link is not None and link["href"].startswith("/post/")


def test_post_page():
    soup = BeautifulSoup(render("post.html", post=POSTS[0]), "html.parser")
    main = soup.find("main")
    assert main.find("article") is not None
    assert main.find("h1").get_text() == "A"


def test_head_meta_and_styles():
    soup = BeautifulSoup(render("index.html", posts=POSTS), "html.parser")
    assert soup.find("link", rel="stylesheet", href="/static/style.css")
    viewport = soup.find("meta", attrs={"name": "viewport"})
    assert viewport is not None


def test_contact_form():
    soup = BeautifulSoup(render("contact.html", errors={}, data={}),
                         "html.parser")
    form = soup.find("form")
    assert form["method"] == "post" and form["action"] == "/contact"
    for name in ("name", "email", "message"):
        field = soup.find(attrs={"name": name})
        assert field.get("required") is not None
        label = soup.find("label", attrs={"for": field["id"]})
        assert label is not None


def test_css_has_modern_features():
    with open("static/style.css", encoding="utf-8") as f:
        css = f.read()
    assert ":root" in css and "--color-" in css
    assert "display: grid" in css and "display: flex" in css
    assert "@media" in css
```

Что здесь происходит? Интеграционный тест рендерит реальные шаблоны и проверяет всё сразу: каркас присутствует, навигация содержит две ссылки, карточек ровно три и каждая ведёт на свою страницу, пост рендерится с заголовком, стили подключены, форма устроена правильно, а CSS использует современные возможности. Запуск: `python -m pytest tests/`. Зелёный результат означает, что сайт собран правильно — от разметки до стилей.
<!--/SOLUTION-->

<!--QUIZ-->
Какой блок в base.html заполняет страница поста?
- content
- footer
- title
- content и title
* Правильный ответ: content и title
Пост определяет и заголовок вкладки (title), и содержимое (content).

Что делает {% include "partials/sidebar.html" %}?
- Вставляет панель во все страницы, наследующие base.html
- Создаёт новый файл
- Переопределяет блок
* Правильный ответ: Вставляет панель во все страницы, наследующие base.html
include вставляет фрагмент шаблона в место вызова.

Что возвращает маршрут /post/999, если поста с id 999 нет?
- «Пост не найден» со статусом 404
- Пустую страницу
- Главную страницу
* Правильный ответ: «Пост не найден» со статусом 404
Правильный ответ на отсутствие ресурса — 404.

Для чего нужен макрос post_card?
- Чтобы переиспользовать разметку карточки поста
- Чтобы хранить данные постов
- Чтобы подключать CSS
* Правильный ответ: Чтобы переиспользовать разметку карточки поста
Макрос описывает карточку один раз, а вызывается для каждого поста.

Что произойдёт, если отправить форму с пустым сообщением?
- Сервер вернёт ошибку валидации и покажет форму заново
- Данные сохранятся
- Страница обновится
* Правильный ответ: Сервер вернёт ошибку валидации и покажет форму заново
Серверная валидация поймает пустое сообщение и покажет ошибку.

Какой файл содержит все стили проекта?
- static/style.css
- templates/style.css
- style.html
* Правильный ответ: static/style.css
Статические файлы (стили, скрипты) лежат в папке static.

Что проверяет интеграционный тест?
- Что все страницы рендерятся корректно: каркас, карточки, форма, стили
- Только Python-код
- Только CSS
* Правильный ответ: Что все страницы рендерятся корректно: каркас, карточки, форма, стили
Интеграционный тест проверяет собранный сайт целиком.

Зачем в проекте используется Jinja2, а не ручной HTML?
- Чтобы страницы собирались из данных и общего каркаса
- Чтобы ускорить браузер
- Чтобы писать меньше CSS
* Правильный ответ: Чтобы страницы собирались из данных и общего каркаса
Шаблонизатор избавляет от дублирования и наполняет страницы данными.

Что произойдёт, если убрать block content из base.html?
- Дочерние страницы не смогут вставить своё содержимое
- Ничего не изменится
- Сайт перестанет грузиться
* Правильный ответ: Дочерние страницы не смогут вставить своё содержимое
Без блока наследники не смогут заполнить основную область.

Что такое «статические файлы»?
- CSS и JS, которые отдаются браузеру как есть
- Шаблоны Jinja2
- Python-модули
* Правильный ответ: CSS и JS, которые отдаются браузеру как есть
Статика не обрабатывается сервером и раздаётся напрямую.
<!--/QUIZ-->
