---
title: Самостоятельная работа: сайт-визитка на Flask + Jinja2 + CSS
summary: Собери личный сайт-визитку: Flask + Jinja2 (наследование, include, фильтры), CSS Flexbox/Grid с адаптивностью, pytest-тесты страниц и шаблонов.
order: 9
duration: 240 мин
difficulty: intermediate
tags: flask, jinja2, html, css, тесты
---

Это самостоятельная работа, в которой ты соберёшь настоящее веб-приложение — личный сайт-визитку. Здесь соединяются все изученные темы: Flask и маршруты, шаблоны Jinja2 с наследованием, CSS-вёрстка на Flexbox и Grid, адаптивность и автотесты на pytest. Работа рассчитана на несколько заходов: не торопись, проходи этапы по порядку и запускай программу после каждого.

## Постановка задачи

Нужно создать сайт-визитку: персональную страницу с рассказом о себе, навыками, проектами и контактами. Сайт состоит из нескольких страниц, собранных из общих шаблонов: единая шапка с навигацией и подвал есть на каждой странице, а содержимое меняется. Данные о навыках и проектах живут в Python-коде, а шаблоны выводят их циклами и фильтрами. Готовый проект покрывается pytest-тестами.

Чему ты научишься: проектировать каркас приложения, наследовать шаблоны, выносить повторяющиеся фрагменты через include, писать кастомные фильтры, стилизовать страницы через переменные, flex и grid с медиазапросами и проверять результат тестами.

## Требования

- Приложение `app.py` на Flask; маршруты `/` и `/about` (можно добавлять свои); все страницы рендерятся через `render_template`.
- Общий каркас `templates/base.html`: `<head>` с `meta charset`, `meta viewport`, блоком `title`, подключением стилей через `url_for("static", filename="style.css")`; в `<body>` — шапка `<header>` с навигацией `<nav>` (логотип и ссылки), `<main>` с блоком `content`, подвал `<footer>`.
- Дочерние страницы наследуют `base.html` через `{% extends %}` и переопределяют только блоки `title` и `content`. Общие части (шапка, подвал) в страницах не дублируются.
- Главная страница содержит секции: hero (имя, роль, фото), about (пара абзацев о себе), skills (список навыков с уровнями), projects (сетка карточек проектов), contacts (ссылки на Telegram/почту и форма-заглушка).
- Данные (навыки, проекты) — списки словарей в `app.py`; шаблоны выводят их циклами `{% for %}`.
- Минимум один кастомный фильтр через `@app.template_filter` (например, `level_label` или `truncate_words`) и использование встроенных: `length`, `default`, `upper`.
- Стили в `static/style.css`: CSS-переменные `:root`, сброс `box-sizing: border-box`, навигация на flex, сетка проектов на grid, медиазапрос `@media (max-width: 768px)`.
- Тесты в `test_app.py` через `TestClient`: минимум 8 ассертов — статусы 200, ключевые тексты страниц, наследование (общие шапка/подвал везде, разные `<title>`), работа фильтров.
- Код читаемый, с комментариями; приложение запускается `python app.py` и открывается на `http://127.0.0.1:5000/`.

## Критерии оценки (10 баллов)

| Критерий | Баллы |
|---|---|
| Каркас Flask + наследование шаблона (base.html, блоки, маршруты) | 2 |
| Секции и контент главной страницы (hero, about, skills, projects, contacts) | 2 |
| Стили: переменные, flex-навигация, grid-сетка, адаптивность | 2 |
| Динамические данные и кастомный фильтр | 2 |
| Тесты pytest проходят, код читаемый | 2 |

Зачтено — от 7 баллов.

## Что сдать

- Файл `app.py` (полная рабочая версия после 5-го этапа).
- Шаблоны из `templates/`: `base.html`, `index.html`, `about.html`, фрагменты (например, `contacts.html`).
- Файл `static/style.css`.
- Файл `test_app.py` — все тесты зелёные (`pytest test_app.py -v`).
- Скриншоты десктопной и мобильной версий главной страницы (или краткое текстовое описание).
- Комментарий в начале `app.py`: как запустить, какие файлы за что отвечают, что бы ты улучшил.
- Викторина по уроку на платформе (8 вопросов).

<!--TASK-->
### Задача 1

Каркас приложения и наследование шаблона. Создай `app.py`: приложение Flask с маршрутами `/` и `/about`, каждый возвращает `render_template` для `index.html` и `about.html`. Создай `templates/base.html`: `<!DOCTYPE html>`, `<head>` с `meta charset`, `meta name="viewport"`, блоком `<title>{% block title %}...{% endblock %}</title>` и подключением стилей `<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">`; в `<body>` — `<header>` с `<nav>` (логотип «PythonПро» и ссылки «Главная», «Обо мне»), `<main>` с блоком `{% block content %}{% endblock %}`, подвал `<footer>© 2026, PythonПро</footer>`. Создай `templates/index.html` и `templates/about.html` с `{% extends "base.html" %}`: переопредели `title` («Главная» и «Обо мне») и `content` (приветствие и абзац о себе). Запусти `python app.py` и проверь обе страницы в браузере: шапка, подвал и навигация должны быть на обеих, а заголовок вкладки — разный.

### Задача 2

Секции сайта. На главной `index.html` внутри блока `content` добавь секции: `hero` — `<h1>` с твоим именем, `<p>` с ролью (например, «Python-разработчик»), `<img>` с фото; `about` — два-три абзаца о себе; `skills` — маркированный список `<ul>` из четырёх-пяти навыков; `projects` — `<section class="projects">` с тремя `<article class="card">` (название и описание); `contacts` — ссылки на Telegram и почту. Описания проектов пока можно написать текстом прямо в шаблоне. В `about.html` добавь блок `content` с двумя абзацами и списком увлечений. Обнови страницы в браузере и проверь, что все секции отображаются.

### Задача 3

Стилизация: переменные, flex, grid, адаптивность. Создай `static/style.css`: `:root` с переменными `--accent`, `--bg`, `--card-gap`; универсальный сброс `* { box-sizing: border-box; }`; стили для `body` (фон `var(--bg)`, шрифт), навигации (`display: flex`, `justify-content`, `gap`, `list-style: none`), секций, `.card` (border, padding, border-radius) и `.projects` (`display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: var(--card-gap);`). Добавь медиазапрос `@media (max-width: 768px)`: навигация становится `flex-direction: column`, `.projects` — `grid-template-columns: 1fr`. Подключи стили в `base.html` через `url_for`. Проверь: сужай окно браузера — колонки проектов должны превращаться в одну, навигация — в столбик.

### Задача 4

Динамические данные и фильтры. В `app.py` определи списки словарей: `SKILLS = [{"name": "Python", "level": 5}, ...]` (4–5 навыков) и `PROJECTS = [{"title": ..., "description": ..., "year": ...}, ...]` (3–4 проекта). Передай их в `render_template` для `/`. В шаблонах выведи навыки циклом (например, `{{ skill.name }}`), проекты — карточками из словарей. Добавь кастомный фильтр через `@app.template_filter("level_label")`: он превращает число уровня 1–5 в слово («новичок», «базовый», «средний», «уверенный», «эксперт»). Используй его в шаблоне: `{{ skill.level|level_label }}`. Также примени встроенные фильтры: `{{ projects|length }}` (число проектов), `{{ skill.name|upper }}` хотя бы в одном месте, `{{ project.description|default("нет описания") }}`. Проверь страницы в браузере.

### Задача 5

Тесты pytest страниц и шаблонов. Создай `test_app.py`: импортируй `app` из `app.py`, `TestClient` из `flask.testing`, заведи `client = TestClient(app)`. Напиши тесты: `test_index_status` — `/` возвращает 200; `test_index_content` — в тексте ответа есть твоё имя, слово «Проекты» и число из фильтра `length` (например, «3 проекта» или аналогичное); `test_about_status` — `/about` возвращает 200 и содержит `<title>Обо мне</title>`; `test_inheritance` — и `/`, и `/about` содержат «PythonПро» (логотип/подвал) и ссылку `href="/about"`; `test_level_label_filter` — в ответе `/` есть слово «эксперт» (для навыка с уровнем 5). Запусти `pytest test_app.py -v` и добейся, чтобы все тесты были зелёными.

<!--/TASK-->

<!--HINT-->
### Подсказка 1

Структура: `app.py` лежит рядом с папками `templates` и `static`. В `base.html` все общие части — шапка, навигация, подвал — располагаются вне блоков; блоки `title` и `content` — единственное, что переопределяют дочерние шаблоны. Первая строка `index.html` — `{% extends "base.html" %}`. Не забудь `app.run(debug=True)` под `if __name__ == "__main__":`.

### Подсказка 2

Каждая секция — `<section>` с классом для будущих стилей: `class="hero"`, `class="about"`, `class="skills"`, `class="projects"`, `class="contacts"`. Внутри секций используй семантичные теги: `h1`/`h2`, `p`, `ul`/`li`, `img`, `a`. Изображение можно подключить с внешнего ресурса (например, `https://picsum.photos/200`) — это не нарушает требований.

### Подсказка 3

Переменные используются через `var(--имя)`. Для навигации достаточно `display: flex; justify-content: center; gap: 24px; list-style: none;` на `ul` (или его классе). Для grid-сетки используй `repeat(auto-fit, minmax(240px, 1fr))` — колонки будут автоматически переноситься, не задавая жёсткое число. Медиазапрос пишется в конце файла.

### Подсказка 4

Фильтр: `@app.template_filter("level_label")` над функцией `def level_label(level): ...`, которая возвращает слово из списка `["новичок", "базовый", "средний", "уверенный", "эксперт"]` по индексу `level - 1` (с проверкой границ). В шаблоне: `{{ skill.level|level_label }}`. Обрати внимание: `{{ projects|length }}` — это число, обёрнутое в текст: «У меня {{ projects|length }} проекта» — но для числа 1 и 5 нужно аккуратно подобрать форму слова или использовать более простое предложение.

### Подсказка 5

`TestClient(app)` вызывает приложение в памяти без сервера. `response.text` — тело ответа как строка, в ней ищем подстроки: `assert "PythonПро" in response.text`. Для проверки разных заголовков вкладки ищи `<title>Главная</title>` и `<title>Обо мне</title>` по отдельности. Запускай `pytest test_app.py -v` из папки проекта — тесты должны обнаружиться автоматически.

<!--/HINT-->

<!--SOLUTION-->
### Разбор 1

`app.py`:

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
```

`templates/base.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}PythonПро{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <header>
        <nav>
            <a href="/" class="logo">PythonПро</a>
            <a href="/">Главная</a>
            <a href="/about">Обо мне</a>
        </nav>
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
    <footer>© 2026, PythonПро</footer>
</body>
</html>
```

`templates/index.html`:

```html
{% extends "base.html" %}

{% block title %}Главная{% endblock %}

{% block content %}
    <h1>Привет, я Аня!</h1>
    <p>Это мой сайт-визитка.</p>
{% endblock %}
```

`templates/about.html` — аналогично, но `title` = «Обо мне» и другой текст в `content`. Разбор. Flask автоматически ищет шаблоны в `templates`, а статику — в `static`; `url_for("static", filename="style.css")` генерирует правильный путь. В `base.html` блоки `title` и `content` — «дыры» каркаса, которые заполняют дочерние шаблоны. Навигация и подвал вне блоков — поэтому они одинаковы на всех страницах. Проверка в браузере: две страницы с разными заголовками вкладки, но общей шапкой и подвалом. Если шапка пропала — проверь, что `{% extends %}` стоит первой строкой.

### Разбор 2

Фрагмент `index.html` (внутри `content`):

```html
<section class="hero">
    <h1>Аня Иванова</h1>
    <p>Python-разработчик</p>
    <img src="https://picsum.photos/200" alt="Фото">
</section>

<section class="about">
    <h2>Обо мне</h2>
    <p>Изучаю Python и веб-разработку уже год. Делаю проекты на Flask.</p>
</section>

<section class="skills">
    <h2>Навыки</h2>
    <ul>
        <li>Python</li>
        <li>Flask</li>
        <li>HTML/CSS</li>
        <li>SQL</li>
    </ul>
</section>

<section class="projects">
    <h2>Проекты</h2>
    <article class="card"><h3>Визитка</h3><p>Этот сайт</p></article>
    <article class="card"><h3>Заметки</h3><p>Консольное приложение на Python</p></article>
    <article class="card"><h3>Бот</h3><p>Telegram-бот на Flask</p></article>
</section>

<section class="contacts">
    <h2>Контакты</h2>
    <a href="https://t.me/username">Telegram</a>
    <a href="mailto:me@example.com">Почта</a>
</section>
```

Разбор. Каждая секция — `<section>` с классом: это даёт точку опоры для CSS на следующем этапе. Внутри — только семантичные теги: заголовки, абзацы, списки, ссылки. Список навыков — `<ul>` с `<li>`, проекты — `<article class="card">`, потому что карточка — самостоятельный независимый блок. Ссылки на контакты: `https://t.me/username` для Telegram и `mailto:...` для почты. Внутри секций нет вложенных `##`-заголовков Markdown — только HTML, это важно для чистоты шаблона.

### Разбор 3

`static/style.css` (ключевые части):

```css
:root {
    --accent: #2563eb;
    --bg: #f5f7fa;
    --card-gap: 16px;
}

* { box-sizing: border-box; }

body {
    margin: 0;
    font-family: sans-serif;
    background: var(--bg);
}

nav {
    display: flex;
    justify-content: center;
    gap: 24px;
    padding: 16px;
    background: white;
}

nav a {
    color: var(--accent);
    text-decoration: none;
}

.card {
    border: 1px solid #ddd;
    padding: 16px;
    border-radius: 8px;
    background: white;
}

.projects {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: var(--card-gap);
}

@media (max-width: 768px) {
    nav { flex-direction: column; align-items: center; }
    .projects { grid-template-columns: 1fr; }
}
```

Разбор. `:root` хранит переменные: цвет акцента, фон, отступ. `var(--bg)` подставляет значение — поменять палитру можно в одном месте. `* { box-sizing: border-box; }` не даёт карточкам «расползаться» из-за padding. Навигация — flex: ссылки в ряд по центру с `gap`. `.projects` — grid с `repeat(auto-fit, minmax(240px, 1fr))`: колонки автоматически создаются по мере места (на широком экране — три, на среднем — две). Медиазапрос на 768px разворачивает навигацию в столбик и делает проекты одноколоночными. Проверка в браузере с сужением окна покажет адаптивность.

### Разбор 4

`app.py` (дополнения):

```python
SKILLS = [
    {"name": "Python", "level": 5},
    {"name": "Flask", "level": 4},
    {"name": "HTML/CSS", "level": 3},
    {"name": "SQL", "level": 2},
]

PROJECTS = [
    {"title": "Визитка", "description": "Этот сайт", "year": 2026},
    {"title": "Заметки", "description": "Консольный менеджер заметок", "year": 2025},
    {"title": "Трекер привычек", "description": "Приложение с напоминаниями", "year": 2025},
]

@app.template_filter("level_label")
def level_label(level):
    words = ["новичок", "базовый", "средний", "уверенный", "эксперт"]
    if 1 <= level <= len(words):
        return words[level - 1]
    return "неизвестно"

@app.route("/")
def index():
    return render_template("index.html", skills=SKILLS, projects=PROJECTS)
```

В шаблоне:

```jinja
<ul>
    {% for skill in skills %}
        <li>{{ skill.name }} — {{ skill.level|level_label }}</li>
    {% endfor %}
</ul>
<p>Всего проектов: {{ projects|length }}</p>
```

Разбор. Данные вынесены из шаблона в Python — шаблон стал чистым представлением, а данные можно менять, не трогая HTML. Цикл `{% for skill in skills %}` перебирает словари, доступ к полям — через точку: `{{ skill.name }}`. Кастомный фильтр `level_label` принимает число и возвращает слово: `{{ skill.level|level_label }}`. Фильтр с проверкой границ безопасен для любых значений. Встроенный `{{ projects|length }}` выводит число проектов. Если список пуст, `{% for %}` просто ничего не выведет — рендер не упадёт.

### Разбор 5

`test_app.py`:

```python
from flask.testing import TestClient
from app import app, PROJECTS

client = TestClient(app)

def test_index_status():
    assert client.get("/").status_code == 200

def test_index_content():
    r = client.get("/")
    assert "Аня" in r.text
    assert "Проекты" in r.text
    assert f"{len(PROJECTS)}" in r.text

def test_about_status():
    r = client.get("/about")
    assert r.status_code == 200
    assert "<title>Обо мне</title>" in r.text

def test_inheritance():
    for path in ("/", "/about"):
        r = client.get(path)
        assert "PythonПро" in r.text
        assert 'href="/about"' in r.text

def test_level_label_filter():
    r = client.get("/")
    assert "эксперт" in r.text
```

Разбор. `TestClient(app)` вызывает приложение без запуска сервера — тесты быстрые и изолированные. `test_index_status` и `test_about_status` проверяют, что страницы отвечают 200. `test_index_content` ищет в HTML имя, заголовок секции и число проектов из данных (сравнение с `len(PROJECTS)` защищает от рассинхронизации). `test_inheritance` — суть наследования: общие «PythonПро» (логотип и подвал) и навигация присутствуют на обеих страницах. `test_level_label_filter` проверяет кастомный фильтр: навык с уровнем 5 даёт «эксперт» в отрендеренном HTML. Запуск `pytest test_app.py -v` — пять зелёных тестов. Если тест упал, читай вывод pytest: он показывает, в какой строке и какая подстрока не нашлась.

<!--/SOLUTION-->

<!--QUIZ-->
Где Flask по умолчанию ищет шаблоны?
- В папке templates
- В папке static
- В корне проекта
- В папке pages
* Правильный ответ: В папке templates
Папка templates лежит рядом с app.py; имена файлов указываются в render_template без пути.

Как правильно подключить CSS-файл в шаблоне?
- <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
- <link rel="stylesheet" href="style.css">
- <style src="style.css">
- {% css "style.css" %}
* Правильный ответ: <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
url_for генерирует путь к статике независимо от структуры проекта.

Что делает {% block content %} в базовом шаблоне?
- Описывает место, которое дочерние шаблоны могут заполнить
- Вставляет файл
- Объявляет переменную
- Импортирует макрос
* Правильный ответ: Описывает место, которое дочерние шаблоны могут заполнить
Блок — это «дыра» каркаса; дочерний шаблон переопределяет её содержимое.

Что обязательно стоит первой строкой дочернего шаблона?
- {% extends "base.html" %}
- {% block %}
- {% include %}
- {% macro %}
* Правильный ответ: {% extends "base.html" %}
Директива extends объявляет наследование и должна идти до остального содержимого.

Зачем нужны кастомные фильтры?
- Чтобы преобразовывать данные при выводе в шаблоне
- Чтобы ускорить Flask
- Чтобы заменить циклы
- Чтобы отправлять формы
* Правильный ответ: Чтобы преобразовывать данные при выводе в шаблоне
Например, level_label превращает число уровня в человекочитаемое слово: {{ skill.level|level_label }}.

Что делает TestClient в тестах?
- Вызывает приложение в памяти без реального сервера
- Открывает браузер
- Отправляет письма
- Тестирует CSS
* Правильный ответ: Вызывает приложение в памяти без реального сервера
TestClient имитирует HTTP-запросы, поэтому тесты не требуют запущенного сервера.

Как проверить содержимое страницы в тесте?
- assert "текст" in response.text
- assert response.html == "текст"
- assert response.body.has("текст")
- print(response.text)
* Правильный ответ: assert "текст" in response.text
response.text — тело ответа как строка; подстрока ищется оператором in.

Что делает repeat(auto-fit, minmax(240px, 1fr)) в grid?
- Автоматически создаёт колонки шириной от 240px по свободному месту
- Всегда создаёт ровно 3 колонки
- Делает сетку фиксированной
- Отключает grid
* Правильный ответ: Автоматически создаёт колонки шириной от 240px по свободному месту
Колонки переносятся в зависимости от ширины окна — вёрстка адаптивная без отдельных media-правил на каждую ширину.

Что произойдёт с навигацией при max-width: 768px?
- Применятся стили из медиазапросa, например flex-direction: column
- Ничего не изменится
- Навигация удалится
- Страница станет пустой
* Правильный ответ: Применятся стили из медиазапросa, например flex-direction: column
Медиазапрос переопределяет свойства при ширине окна ≤ 768px.

Что проверяет тест наследования (inheritance)?
- Что общие элементы шапки и подвала есть на всех страницах
- Что все страницы одинаковые
- Что CSS подключён
- Что фильтры работают
* Правильный ответ: Что общие элементы шапки и подвала есть на всех страницах
Тест ищет в ответе нескольких страниц одни и те же подстроки — логотип, ссылки навигации, текст подвала.
<!--/QUIZ-->
