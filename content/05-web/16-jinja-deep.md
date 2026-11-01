---
title: Jinja2 глубоко: наследование, макросы, фильтры
summary: Environment и FileSystemLoader, наследование extends/block, include, макросы, кастомные фильтры, контроль пробелов, автоэкранирование и тесты на отрендеренный HTML.
order: 16
duration: 50 мин
difficulty: advanced
tags: jinja2, flask, шаблоны, тесты
---

В уроке про Flask и формы мы уже познакомились с двойными фигурными скобками `{{ }}` и тегами `{% %}`. Но Jinja2 — самостоятельная библиотека, её можно использовать и вне Flask. Сейчас мы разберём, как устроен её движок, и научимся строить крупные шаблоны: с наследованием, макросами, собственными фильтрами и защитой от XSS.

## Environment и FileSystemLoader

Центральный объект Jinja2 — `Environment` («окружение»). Он хранит настройки и знает, откуда брать шаблоны. Настроить окружение просто:

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))
```

`FileSystemLoader` указывает папку, в которой лежат шаблоны. Дальше берём шаблон по имени и рендерим его с данными:

```python
template = env.get_template("hello.html")
print(template.render(name="Аня"))
```

Аргументы `render()` становятся переменными шаблона. Рендер с контекстом: можно передать и один готовый словарь — `template.render({"name": "Аня", "items": [1, 2]})`, это удобно, когда данных много. Переменные, которые должны быть видны во всех шаблонах окружения, добавляют через `env.globals`. Если шаблон ссылается на несуществующую переменную, по умолчанию получится пустая строка — не ошибка.

## Наследование: extends и block

На реальном сайте почти все страницы делят общую «рамку»: шапку, меню, подвал. Копировать её в каждый файл нельзя — при любой правке пришлось бы править всё. Jinja2 решает это наследованием. Базовый шаблон описывает каркас и помечает изменяемые места блоками:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <title>{% block title %}Мой сайт{% endblock %}</title>
</head>
<body>
    <header>
        {% block header %}Шапка{% endblock %}
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
    <footer>© 2026, PythonПро</footer>
</body>
</html>
```

Дочерний шаблон объявляет `{% extends "base.html" %}` и переопределяет нужные блоки:

```html
{% extends "base.html" %}

{% block title %}Главная{% endblock %}

{% block content %}
    <h1>Привет, {{ name }}!</h1>
{% endblock %}
```

Блок, который дочерний шаблон не переопределил, остаётся таким, как в базе. А `{{ super() }}` внутри блока вставляет содержимое родительского блока — удобно, когда нужно дополнить, а не заменить. Порядок блоков в дочернем шаблоне не важен: Jinja2 собирает итоговую страницу по именам блоков.

## include: вставка фрагментов

Если кусок используется в нескольких шаблонах, но не является частью их «скелета», его выносят в отдельный файл и вставляют через `{% include "footer.html" %}`. Фрагмент видит текущий контекст — все переменные, доступные в момент вызова. Если файл может отсутствовать, добавь `ignore missing`: `{% include "ads.html" ignore missing %}`.

## Макросы: функции в шаблоне

Повторяющиеся куски разметки оформляют как макросы — это своего рода функции шаблона:

```jinja
{% macro card(title, text) %}
<article class="card">
    <h3>{{ title }}</h3>
    <p>{{ text }}</p>
</article>
{% endmacro %}
```

Вызов: `{{ card("Заголовок", "Текст") }}`. Макросы обычно складывают в отдельный файл и импортируют: `{% import "_cards.html" as cards %}`, тогда вызывают `{{ cards.card(...) }}`. Макрос принимает аргументы, возвращает HTML и держит весь код карточки в одном месте.

## Фильтры и кастомные фильтры

Фильтр — функция, которая принимает значение и возвращает преобразованное. Вызывается вертикальной чертой: `{{ text|upper }}`, `{{ items|length }}`, `{{ users|join(", ") }}`, `{{ comment|default("нет комментария") }}`. Цепочки допустимы: `{{ name|trim|title }}`. Встроенных фильтров десятки, а свои пишутся за минуту:

```python
def pluralize(count, singular, plural):
    return singular if count == 1 else plural

env.filters["pluralize"] = pluralize
```

Теперь `{{ tasks|length|pluralize("задача", "задачи") }}` выведет «1 задача» или «3 задачи». Во Flask фильтр регистрируют декоратором `@app.template_filter("pluralize")`.

## Управление пробелами

Теги `{% %}` сами по себе ничего не печатают, но окружающие их переводы строк и отступы попадают в вывод — это раздувает HTML. Решения два: настроить окружение (`Environment(trim_blocks=True, lstrip_blocks=True)`) либо ставить дефисы у тегов: `{%- if x -%}` убирает пробелы до и после конструкции. На больших проектах обычно выбирают настройку окружения.

## Автоэкранирование и безопасность

Самое важное. Если пользователь ввёл текст, а мы вставили его в шаблон как есть, в страницу можно внедрить код — классическая XSS-атака:

```jinja
{{ user_input }}
```

При включённом `autoescape` специальные символы (`<`, `>`, `&`, `"`) превращаются в безопасные сущности (`&lt;`, `&gt;`, …) и выводятся как обычный текст. Flask включает `autoescape` для `.html`-шаблонов автоматически. Самостоятельный `Environment` — нет: `autoescape=True` нужно включить явно. Если данные заведомо безопасны (например, HTML из твоего кода), используй `{{ value|safe }}` или `Markup(value)` — но только когда уверен.

## Итог

Мы узнали, как устроен `Environment` и как подключить `FileSystemLoader`, как строить наследование через `extends`/`block`, вставлять фрагменты через `include`, писать макросы и кастомные фильтры, контролировать пробелы и защищаться от XSS. Теперь закрепим практикой: соберём систему шаблонов и покроем её тестами.

<!--TASK-->
### Задача 1

Создай папку `templates` и в ней файл `hello.html`: заголовок `<h1>Привет, {{ name }}!</h1>`, под ним маркированный список `<ul>` с циклом `{% for city in cities %}<li>{{ city }}</li>{% endfor %}`. Напиши скрипт `render_hello.py`, который создаёт `Environment(loader=FileSystemLoader("templates"))`, берёт шаблон через `get_template("hello.html")`, рендерит его с аргументами `name="Аня"` и `cities=["Москва", "Казань", "Новосибирск"]` и печатает результат через `print`. Запусти скрипт и убедись, что в выводе есть заголовок с именем «Аня» и ровно три пункта списка.

### Задача 2

Построй наследование. Создай `base.html` с блоками: `title` (по умолчанию «Мой сайт»), `header` (по умолчанию «Шапка сайта»), `content` (пустой). В подвале вне блоков напиши строку `© 2026, PythonПро`. Затем создай `index.html` и `about.html` с `{% extends "base.html" %}`: первый переопределяет `title` на «Главная» и `content` — приветствие с именем, второй — `title` на «Обо мне» и `content` — абзац о себе. Блоки `header` не переопределяй. Напиши скрипт, который рендерит обе страницы и печатает каждую. Убедись, что в обоих выводах есть строка `© 2026, PythonПро` и разный текст внутри `<title>`.

### Задача 3

Вынеси повторяющееся в макросы и фрагменты. Создай `_cards.html` с макросом `card(title, text)`, который возвращает `<article class="card">` с `<h3>` и `<p>`. Создай `footer.html` с простым `<footer>Сделано в PythonПро</footer>`. В `index.html` подключи `{% import "_cards.html" as cards %}` и `{% include "footer.html" %}`, затем выведи три карточки с разными заголовками и текстами. Отрендери страницу и с помощью `html.count('class="card"')` проверь, что карточек ровно три, а футер присутствует. Выведи результат подсчёта на экран.

### Задача 4

Добавь кастомный фильтр и проверь автоэкранирование через pytest. Создай Flask-приложение `app.py`: фильтр `pluralize(count, singular, plural)` через `@app.template_filter("pluralize")`; маршрут `/tasks`, который передаёт в шаблон `tasks.html` список из трёх строк и `count=len(items)`; маршрут `/echo`, который передаёт в `echo.html` строку `"<script>alert('xss')</script>"`. В `tasks.html` выведи `{{ count|pluralize("задача", "задачи") }}` и список через цикл; в `echo.html` — `{{ text }}` безо всяких `|safe`. Напиши `test_filters.py` с `TestClient(app)`: тест `test_pluralize_content` проверяет `200`, наличие `3 задачи` и `<li>купить молоко</li>` в `response.text`; тест `test_autoescape` проверяет, что в ответе `/echo` нет сырого `<script>`, но есть `&lt;script&gt;`. Установи `flask` и `pytest`, если нужно, и запусти `pytest test_filters.py -v`.

### Задача 5

Добавь наследование и напиши комплексные тесты. Создай `base.html` с навигацией (ссылки на `/`, `/about`, `/tasks`), блоком `content` и подвалом `© 2026, PythonПро`. Переделай `index.html`, `about.html` и `tasks.html` так, чтобы они наследовали `base.html` и переопределяли `title` («Главная», «Обо мне», «Задачи»). Напиши `test_layout.py`: `test_index_uses_base_layout` проверяет `200`, наличие `Логотип PythonПро`, `© 2026` и `<title>Главная</title>` в ответе `/`; `test_about_uses_base_layout` — то же для `/about` с `<title>Обо мне</title>`; `test_nav_is_shared` проверяет, что обе страницы содержат одинаковые ссылки `href="/about"` и `href="/tasks"`. Запусти `pytest test_layout.py -v` и убедись, что все тесты зелёные.

<!--/TASK-->

<!--HINT-->
### Подсказка 1

`Environment(loader=FileSystemLoader("templates"))` ищет шаблоны в папке `templates` — в `get_template` указывай только имя файла без пути. Все переменные из `render(...)` доступны в шаблоне как обычные имена: `{{ name }}` и `{% for city in cities %}`. Если вывод пустой — проверь, что папка `templates` лежит рядом со скриптом.

### Подсказка 2

Первая строка дочернего шаблона — `{% extends "base.html" %}`. Каждый блок открывается `{% block имя %}` и закрывается `{% endblock %}`. Что не переопределил — остаётся из базы. Для проверки выведи `template.render(...)` обеих страниц через `print` — подвал и разные `<title>` должны быть видны глазами.

### Подсказка 3

Импорт макросов: `{% import "_cards.html" as cards %}` — дальше вызов `{{ cards.card("Заголовок", "Текст") }}`. Вставка фрагмента: `{% include "footer.html" %}`. Метод `str.count` считает непересекающиеся вхождения: `html.count('class="card"')` вернёт 3 при трёх карточках.

### Подсказка 4

Фильтр регистрируется через `@app.template_filter("pluralize")` прямо над функцией. В `TestClient(app)` ответы доступны: `response.status_code`, `response.text`. Автоэкранирование для `.html` Flask включает сам: `{{ text }}` выведет `&lt;script&gt;`, а не тег. Проверка `assert "<script>" not in r.text` ловит «сырой» тег.

### Подсказка 5

В `base.html` `<title>{% block title %}...{% endblock %}</title>` — дочерние переопределяют только текст блока. Общие части (навигация, подвал) лежат вне блоков, поэтому попадают в каждую страницу. Одна фикстура `client = TestClient(app)` на уровне модуля переиспользуется всеми тестами — создавай её один раз и запускай `pytest test_layout.py -v`.

<!--/HINT-->

<!--SOLUTION-->
### Разбор 1

`templates/hello.html`:

```html
<h1>Привет, {{ name }}!</h1>
<ul>
    {% for city in cities %}
        <li>{{ city }}</li>
    {% endfor %}
</ul>
```

`render_hello.py`:

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("hello.html")
html = template.render(
    name="Аня",
    cities=["Москва", "Казань", "Новосибирск"],
)
print(html)
```

Запуск: `python render_hello.py`. Вывод:

```
<h1>Привет, Аня!</h1>
<ul>
    <li>Москва</li>
    <li>Казань</li>
    <li>Новосибирск</li>
</ul>
```

Разбор. `Environment` — это «фабрика» шаблонов: он хранит настройки и знает, откуда их читать (`FileSystemLoader` указывает папку). `get_template("hello.html")` загружает файл и парсит его один раз; повторные вызовы `render` переиспользуют разобранный шаблон, поэтому рендер быстрый. Аргументы `render(name="Аня", cities=[...])` попадают в контекст: `{{ name }}` подставляется в текст, а `{% for city in cities %}` перебирает список и порождает по одному `<li>` на город. Итог — полноценная HTML-строка, которую можно вернуть из Flask или записать в файл.

### Разбор 2

`base.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <title>{% block title %}Мой сайт{% endblock %}</title>
</head>
<body>
    <header>{% block header %}Шапка сайта{% endblock %}</header>
    <main>{% block content %}{% endblock %}</main>
    <footer>© 2026, PythonПро</footer>
</body>
</html>
```

`index.html`:

```html
{% extends "base.html" %}

{% block title %}Главная{% endblock %}

{% block content %}
    <h1>Привет, {{ name }}!</h1>
{% endblock %}
```

`about.html`:

```html
{% extends "base.html" %}

{% block title %}Обо мне{% endblock %}

{% block content %}
    <p>Я изучаю Python и строю сайты на Flask.</p>
{% endblock %}
```

Скрипт `render_site.py`:

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))
for page in ("index", "about"):
    print(env.get_template(f"{page}.html").render(name="Аня"))
    print("---")
```

Разбор. `{% extends %}` должен стоять первой строкой дочернего шаблона — это не комментарий, а директива наследования. Итоговая страница собирается из базы: берётся каркас из `base.html`, и для каждого `block`, который ребёнок переопределил, подставляется содержимое ребёнка. Блоки `header` и `footer` не тронуты, поэтому оба вывода содержат «Шапка сайта» и `© 2026, PythonПро`. А вот `<title>` разный: «Главная» у одной страницы и «Обо мне» у другой. Это и есть главная ценность наследования: общая рамка меняется в одном месте, а уникальное содержимое — в своих шаблонах.

### Разбор 3

`templates/_cards.html`:

```jinja
{% macro card(title, text) %}
<article class="card">
    <h3>{{ title }}</h3>
    <p>{{ text }}</p>
</article>
{% endmacro %}
```

`templates/footer.html`:

```html
<footer>Сделано в PythonПро</footer>
```

`templates/index.html` (выдержка):

```jinja
{% import "_cards.html" as cards %}
{% include "footer.html" %}

{{ cards.card("Jinja2", "Наследование и макросы") }}
{{ cards.card("Flask", "Микрофреймворк") }}
{{ cards.card("CSS", "Flexbox и Grid") }}
```

Скрипт:

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))
html = env.get_template("index.html").render()
print(html.count('class="card"'))   # ожидаем 3
print("Сделано в PythonПро" in html)  # ожидаем True
```

Разбор. Макрос — это функция шаблона: он принимает аргументы и возвращает готовую разметку. Вся разметка карточки живёт в одном месте — `_cards.html`, и если захочешь поменять структуру карточки, правишь только макрос. Импорт `{% import "_cards.html" as cards %}` даёт пространство имён `cards`, чтобы имена не конфликтовали. `{% include "footer.html" %}` вставляет фрагмент прямо в текущее место — он видит контекст, но не создаёт наследования. Подсчёт `html.count('class="card"')` даёт 3: ровно столько раз вызван макрос. Футер присутствует — это подтверждает `in html`.

### Разбор 4

`app.py`:

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.template_filter("pluralize")
def pluralize(count, singular, plural):
    return singular if count == 1 else plural

@app.route("/tasks")
def tasks():
    items = ["купить молоко", "позвонить бабушке", "записаться к врачу"]
    return render_template("tasks.html", items=items, count=len(items))

@app.route("/echo")
def echo():
    return render_template("echo.html", text="<script>alert('xss')</script>")

if __name__ == "__main__":
    app.run(debug=True)
```

`templates/tasks.html`:

```html
<h1>{{ count|pluralize("задача", "задачи") }}</h1>
<ul>
    {% for item in items %}
        <li>{{ item }}</li>
    {% endfor %}
</ul>
```

`templates/echo.html`:

```html
<p>{{ text }}</p>
```

`test_filters.py`:

```python
from flask.testing import TestClient
from app import app

client = TestClient(app)

def test_pluralize_content():
    r = client.get("/tasks")
    assert r.status_code == 200
    assert "3 задачи" in r.text
    assert "<li>купить молоко</li>" in r.text

def test_autoescape():
    r = client.get("/echo")
    assert r.status_code == 200
    assert "<script>" not in r.text
    assert "&lt;script&gt;" in r.text
```

Разбор. Декоратор `@app.template_filter("pluralize")` регистрирует функцию как фильтр: в шаблоне `count|pluralize("задача", "задачи")` означает вызов `pluralize(count, "задача", "задачи")` — значение слева от вертикальной черты становится первым аргументом. Фильтр возвращает «задача» для единицы и «задачи» для остального. Тест `test_pluralize_content` проверяет отрендеренный HTML как строку: там есть «3 задачи» и пункт списка — значит, и фильтр, и цикл сработали. Тест `test_autoescape` — про безопасность: Flask для `.html` включает экранирование, поэтому `<script>alert('xss')</script>` превращается в `&lt;script&gt;alert(&#39;xss&#39;)&lt;/script&gt;`. Браузер покажет это как текст, а не выполнит. Сырой `<script>` в ответе отсутствует — проверка `assert "<script>" not in r.text` это ловит.

### Разбор 5

`templates/base.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <title>{% block title %}PythonПро{% endblock %}</title>
</head>
<body>
    <header>
        <nav>
            <a href="/">Логотип PythonПро</a>
            <a href="/">Главная</a>
            <a href="/about">Обо мне</a>
            <a href="/tasks">Задачи</a>
        </nav>
    </header>
    <main>{% block content %}{% endblock %}</main>
    <footer>© 2026, PythonПро. Все права защищены.</footer>
</body>
</html>
```

`templates/index.html`:

```html
{% extends "base.html" %}

{% block title %}Главная{% endblock %}

{% block content %}
    <h1>Привет, {{ name }}!</h1>
{% endblock %}
```

`test_layout.py`:

```python
from flask.testing import TestClient
from app import app

client = TestClient(app)

def test_index_uses_base_layout():
    r = client.get("/")
    assert r.status_code == 200
    assert "Логотип PythonПро" in r.text
    assert "© 2026" in r.text
    assert "<title>Главная</title>" in r.text

def test_about_uses_base_layout():
    r = client.get("/about")
    assert r.status_code == 200
    assert "Логотип PythonПро" in r.text
    assert "© 2026" in r.text
    assert "<title>Обо мне</title>" in r.text

def test_nav_is_shared():
    r1 = client.get("/").text
    r2 = client.get("/about").text
    for link in ('href="/about"', 'href="/tasks"'):
        assert link in r1
        assert link in r2
```

Разбор. Навигация и подвал лежат в `base.html` вне блоков — значит, они автоматически попадают в каждую страницу, которая наследует базу. Тесты это проверяют: `test_index_uses_base_layout` ищет в ответе `/` и логотип, и подвал, и переопределённый `<title>Главная</title>`. Если бы кто-то забыл `{% extends %}` или убрал блок `title`, тест упал бы — это и есть защита от регрессий при рефакторинге шаблонов. `test_nav_is_shared` сравнивает структуру двух страниц: обе должны содержать одни и те же ссылки меню. Так один набор тестов покрывает содержимое, наследование и связность страниц. Запуск `pytest test_layout.py -v` покажет три зелёных теста.

<!--/SOLUTION-->

<!--QUIZ-->
Что делает класс Environment в Jinja2?
- Хранит настройки и умеет создавать шаблоны
- Отправляет HTML в браузер
- Заменяет Flask
- Хранит только переменные
* Правильный ответ: Хранит настройки и умеет создавать шаблоны
Environment — центральный объект: он знает настройки (autoescape, trim_blocks), загрузчик и фабрику шаблонов.

Что делает FileSystemLoader?
- Ищет шаблоны в указанной папке
- Сжимает HTML
- Проверяет HTML на ошибки
- Выполняет Python-код в шаблоне
* Правильный ответ: Ищет шаблоны в указанной папке
FileSystemLoader("templates") говорит Environment, в какой папке лежат шаблоны.

Как дочерний шаблон объявляет наследование?
- {% include "base.html" %}
- {% extends "base.html" %}
- {% block "base.html" %}
- {% import "base.html" %}
* Правильный ответ: {% extends "base.html" %}
Директива extends указывает базовый шаблон и стоит первой строкой дочернего шаблона.

Что выведет {{ super() }} внутри блока?
- Содержимое родительского блока
- Пустую строку
- Имя текущего шаблона
- Ошибку рендера
* Правильный ответ: Содержимое родительского блока
super() вставляет содержимое блока из базового шаблона — удобно, чтобы дополнить его, а не заменить.

Чем include отличается от extends?
- include вставляет фрагмент в текущее место, а extends строит каркас по базе
- Это одно и то же
- include работает только с картинками
- extends запрещён в Flask
* Правильный ответ: include вставляет фрагмент в текущее место, а extends строит каркас по базе
include добавляет отдельный файл как есть; extends создаёт иерархию шаблонов с блоками.

Как объявить макрос card в шаблоне?
- {% macro card(title, text) %} ... {% endmacro %}
- {% function card(title, text) %}
- {% def card(title, text) %}
- {{ macro card(title, text) }}
* Правильный ответ: {% macro card(title, text) %} ... {% endmacro %}
Макрос — это функция шаблона: принимает аргументы и возвращает разметку.

Как зарегистрировать кастомный фильтр во Flask?
- @app.template_filter("pluralize") над функцией
- env.add_filter("pluralize")
- Регистрация не нужна
- jinja2.register_filter("pluralize")
* Правильный ответ: @app.template_filter("pluralize") над функцией
Декоратор делает функцию фильтром: в шаблоне она вызывается как value|pluralize(...).

Что делает автоэкранирование (autoescape)?
- Превращает спецсимволы в безопасные сущности
- Удаляет все теги из вывода
- Ускоряет рендер
- Отключает фильтры
* Правильный ответ: Превращает спецсимволы в безопасные сущности
<, >, &, " превращаются в &lt;, &gt; и т. д. — введённый пользователем код не выполнится.

Как вывести заведомо безопасный HTML без экранирования?
- {{ value|safe }}
- {{ value|raw }}
- {{ safe(value) }}
- {{ value }unescaped }}
* Правильный ответ: {{ value|safe }}
Фильтр safe помечает значение как безопасное. Используй его только для данных, которым доверяешь полностью.

Что делают {%- и -%} в тегах?
- Убирают пробелы и переводы строк вокруг тега
- Добавляют отступ
- Отключают экранирование
- Помечают блок
* Правильный ответ: Убирают пробелы и переводы строк вокруг тега
Дефисы контролируют пробелы: {%- срезает пробелы до тега, -%} — после.
<!--/QUIZ-->
