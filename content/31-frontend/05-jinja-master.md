---
title: Jinja2-мастер: наследование, макросы, фильтры
summary: Шаблонизатор Jinja2: переменные, фильтры, наследование через extends/block, include, макросы и autoescape.
order: 5
duration: 50 мин
difficulty: advanced
tags: jinja2, шаблоны, flask, макросы, фильтры
---

Ты уже писал HTML вручную. Но в настоящих веб-приложениях страницы собираются из данных: список товаров, профиль пользователя, лента новостей. Для этого нужен **шаблонизатор** — инструмент, который наполняет HTML-каркас данными. Самый популярный в Python-мире — **Jinja2**.

## Первый шаблон

Библиотека `jinja2` — это пакет Python. Минимальный пример:

```python
from jinja2 import Template

template = Template("Привет, {{ name }}!")
print(template.render(name="Аня"))  # Привет, Аня!
```

Синтаксис Jinja2:

- `{{ выражение }}` — вывод значения;
- `{% оператор %}` — логика: условия, циклы, наследование;
- `{# комментарий #}` — комментарий, не попадает в вывод.

Внутри `{{ }}` можно использовать почти любые Python-выражения: арифметику, вызовы методов, доступ к элементам списков и словарей. `{{ user.name }}` и `{{ user["name"] }}` равнозначны.

## Условия и циклы

```python
template = Template("""
{% for item in items %}
    {{ loop.index }}. {{ item }}
{% endfor %}
{% if items|length == 0 %}
    Список пуст.
{% endif %}
""")
print(template.render(items=["Python", "Jinja2"]))
```

Переменная `loop` доступна внутри цикла: `loop.index` (с 1), `loop.index0` (с 0), `loop.first`, `loop.last`.

## Фильтры

Фильтры применяются через `|` и меняют значение. Основные:

- `{{ name|upper }}` — верхний регистр, есть `lower`, `capitalize`, `title`;
- `{{ items|join(", ") }}` — склейка списка;
- `{{ items|length }}` — длина;
- `{{ value|default("нет значения") }}` — значение по умолчанию (для `False` есть `default("...", boolean=True)`);
- `{{ price|round(2) }}` — округление;
- `{{ text|truncate(50) }}` — обрезание текста;
- `{{ text|e }}` / `{{ text|safe }}` — экранирование и «сырой» вывод.

```python
from jinja2 import Template

t = Template("Итого: {{ total|round(2) }} ₽")
print(t.render(total=1234.5678))  # Итого: 1234.57 ₽
```

## autoescape: безопасность по умолчанию

По умолчанию в `jinja2.Template` **autoescape выключен** — вывод не экранируется. Это значит, что если в шаблон попадёт пользовательский текст с HTML, он «оживёт». В Flask для `.html`-шаблонов autoescape включён, но если ты создаёшь шаблоны вручную — включи его сам:

```python
from jinja2 import Environment

env = Environment(autoescape=True)
t = env.from_string("{{ user_input }}")
print(t.render(user_input="<script>alert(1)</script>"))
# &lt;script&gt;alert(1)&lt;/script&gt;
```

Правило: **никогда не помечай пользовательский ввод как `|safe`**. `|safe` нужен только для доверенного HTML (например, разметки, которую написал ты).

## Наследование: extends и block

Наследование — главная фишка Jinja2. Ты строишь базовый шаблон `base.html` с блоками, а дочерние страницы их заполняют:

```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Сайт{% endblock %}</title>
</head>
<body>
    <header>{% block header %}Шапка{% endblock %}</header>
    <main>{% block content %}{% endblock %}</main>
    <footer>{% block footer %}© 2026{% endblock %}</footer>
</body>
</html>
```

```html
<!-- page.html -->
{% extends "base.html" %}

{% block title %}Обо мне{% endblock %}

{% block content %}
    <h1>Обо мне</h1>
    <p>Привет! Меня зовут Аня.</p>
{% endblock %}
```

Если в дочернем шаблоне не переопределить блок — останется содержимое родителя. А `{{ super() }}` вставляет родительское содержимое внутрь переопределённого блока. Дочерний шаблон **обязан** начинаться с `{% extends %}`.

## include и макросы

`{% include "partials/footer.html" %}` вставляет содержимое другого шаблона — удобно для переиспользуемых кусочков (карточки, кнопки). Ещё мощнее — **макросы**: функции внутри шаблонов:

```html
{% macro card(title, text) %}
    <article class="card">
        <h3>{{ title }}</h3>
        <p>{{ text }}</p>
    </article>
{% endmacro %}
```

Использование:

```html
{{ card("Проект 1", "Описание первого проекта") }}
{{ card("Проект 2", "Описание второго проекта") }}
```

Макросы можно хранить в отдельном файле и подключать через `{% import "macros.html" as ui %}` или `{% from "macros.html" import card %}`. У макросов могут быть значения по умолчанию: `{% macro card(title, text="") %}`.

## Environment и FileSystemLoader

В реальном проекте шаблоны лежат в папке. Их загружает `Environment` с `FileSystemLoader`:

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"), autoescape=True)
template = env.get_template("page.html")
print(template.render(user="Аня"))
```

Именно так это делает Flask: он создаёт окружение Jinja2 для папки `templates/` со включённым autoescape.

## Пробел и контроль вывода

Служебные теги можно «прижимать» к тексту: `{%-` и `-%}` убирают пробелы и переносы строк вокруг себя. Это пригодится, когда нужно вывести элементы в одну строку без лишних пробелов.

Теперь соберём всё вместе: ты построишь наследование, напишешь макросы, разберёшься с экранированием и покроешь всё тестами.

<!--TASK-->
### Задача 1
Напиши скрипт `basics.py`, который создаёт `Environment(autoescape=True)` и рендерит строковый шаблон:

```
Привет, {{ name|capitalize }}! Сегодня {{ day }}.
У тебя {{ tasks|length }} задач: {{ tasks|join(", ") }}.
```

Передай `name="аня"`, `day="суббота"`, `tasks=["Python", "CSS", "Jinja2"]`. Выведи результат на экран. Ожидаемый результат:

```
Привет, Аня! Сегодня суббота.
У тебя 3 задач: Python, CSS, Jinja2.
```

### Задача 2
Создай папку `templates/` с двумя шаблонами: `base.html` и `about.html`. В `base.html` — каркас страницы с блоками `title`, `content`. В `about.html` — `{% extends "base.html" %}`, переопределение `title` на «Обо мне» и `content` на абзац о себе. Затем напиши скрипт `render_about.py`, который через `Environment(loader=FileSystemLoader("templates"), autoescape=True)` рендерит `about.html` и печатает результат. Дополнительно напиши pytest-тест `test_extends.py`: проверь через `BeautifulSoup`, что в отрендеренном HTML есть `<title>Обо мне</title>`, содержимое `content`-блока, а также каркас из `base.html` (`<main>`, `<footer>`). Ожидаемый результат: страница собрана из двух шаблонов.

### Задача 3
Создай файл `templates/macros.html` с макросом `card(title, text)` (карточка: `<article class="card">` с `<h3>` и `<p>`). Затем создай шаблон `gallery.html`, который через `{% from "macros.html" import card %}` подключает макрос, и в цикле `{% for post in posts %}` выводит `{{ card(post.title, post.text) }}`. Напиши скрипт, который рендерит `gallery.html` со списком из трёх постов и печатает HTML. Ожидаемый результат: в выводе три карточки, каждая с заголовком и текстом.

### Задача 4
Создай два скрипта, которые показывают разницу экранирования. Первый — `unsafe.py`: шаблон `{{ user_input }}` при `Environment(autoescape=False)` рендерит `<img src=x onerror=alert(1)>` — выведи результат. Второй — `safe.py`: тот же шаблон, но `Environment(autoescape=True)`; выведи результат. Затем модифицируй `safe.py`: добавь фильтр `|safe` к выводу и снова выведи. Ожидаемый результат: в первом случае — сырой HTML-тег, во втором — экранированная последовательность (`&lt;img ...&gt;`), в третьем — снова сырой тег. В комментарии в коде объясни, чем опасен вариант с `|safe` для пользовательского ввода.

### Задача 5
Напиши файл тестов `test_jinja.py` (используй pytest), который проверяет:

- **Макрос**: отрендерь шаблон с макросом `card` для списка из двух постов и проверь через `BeautifulSoup`, что в HTML ровно две `<article class="card">`, у каждой есть `<h3>` с заголовком;
- **Наследование**: отрендерь `about.html` и проверь, что `title` — «Обо мне», а в `<main>` есть `<h1>`;
- **Autoescape**: отрендерь `{{ value }}` с `Environment(autoescape=True)` и значением `<script>alert(1)</script>`, проверь, что в HTML нет тега `<script>` (нет подстроки `<script>`), а есть `&lt;script&gt;`;
- **Фильтры**: отрендерь `{{ text|truncate(10) }}` с длинным текстом и проверь, что результат короче исходного и заканчивается на `...`.

Ожидаемый результат: все тесты проходят, запуск — `python -m pytest test_jinja.py`.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
`Environment(autoescape=True)` создаёт окружение. Строковый шаблон — через `Environment.from_string("...")` или просто `Template("...")` из `jinja2`. Фильтры пишутся через `|`: `{{ name|capitalize }}`.

### Подсказка 2
Базовый шаблон с блоками: `{% block title %}...{% endblock %}`. Дочерний начинается с `{% extends "base.html" %}`. Загрузчик: `Environment(loader=FileSystemLoader("templates"), autoescape=True)`; `env.get_template("about.html").render()`.

### Подсказка 3
Макрос объявляется `{% macro card(title, text) %}...{% endmacro %}`. Подключение: `{% from "macros.html" import card %}`. В цикле `{% for post in posts %}` вызывай `{{ card(post.title, post.text) }}`. В `render()` передай `posts=[{"title": ..., "text": ...}, ...]`.

### Подсказка 4
По умолчанию `Environment(autoescape=False)`. Включение: `Environment(autoescape=True)`. Проверь вывод глазами: сырой тег против `&lt;...&gt;`. `|safe` отключает экранирование для конкретного значения.

### Подсказка 5
Для тестов переиспользуй `Environment(loader=FileSystemLoader("templates"), autoescape=True)`. Красивый приём — фикстура: `@pytest.fixture` возвращает окружение. Для проверки карточек: `soup.find_all("article", class_="card")`. Для автоэкранирования: `assert "<script>" not in html`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Файл `basics.py`:

```python
from jinja2 import Environment

env = Environment(autoescape=True)
template = env.from_string(
    "Привет, {{ name|capitalize }}! Сегодня {{ day }}.\n"
    "У тебя {{ tasks|length }} задач: {{ tasks|join(', ') }}."
)
result = template.render(
    name="аня", day="суббота", tasks=["Python", "CSS", "Jinja2"],
)
print(result)
```

Вывод:

```
Привет, Аня! Сегодня суббота.
У тебя 3 задач: Python, CSS, Jinja2.
```

Что здесь происходит? `env.from_string()` превращает строку в шаблон. `{{ name|capitalize }}` меняет первую букву на заглавную; `{{ tasks|length }}` считает элементы списка; `{{ tasks|join(', ') }}` склеивает список через запятую с пробелом. `Environment(autoescape=True)` включён с самого начала — привыкай к безопасному режиму.

### Разбор 2
`templates/base.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Сайт{% endblock %}</title>
</head>
<body>
    <header>{% block header %}Шапка{% endblock %}</header>
    <main>{% block content %}{% endblock %}</main>
    <footer>{% block footer %}© 2026{% endblock %}</footer>
</body>
</html>
```

`templates/about.html`:

```html
{% extends "base.html" %}

{% block title %}Обо мне{% endblock %}

{% block content %}
    <h1>Обо мне</h1>
    <p>Привет! Меня зовут Аня.</p>
{% endblock %}
```

`render_about.py`:

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"), autoescape=True)
print(env.get_template("about.html").render())
```

`test_extends.py`:

```python
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader


def render_about():
    env = Environment(loader=FileSystemLoader("templates"), autoescape=True)
    return env.get_template("about.html").render()


def test_title_and_content_blocks():
    html = render_about()
    soup = BeautifulSoup(html, "html.parser")
    assert soup.title.get_text() == "Обо мне"
    main = soup.find("main")
    assert main.find("h1").get_text() == "Обо мне"
    assert main.find("p") is not None


def test_base_frame_present():
    html = render_about()
    soup = BeautifulSoup(html, "html.parser")
    assert soup.find("footer") is not None
    assert soup.find("header") is not None
```

Что здесь происходит? `about.html` наследует каркас `base.html`: блоки `title` и `content` переопределены, а `header` и `footer` остались родительскими. Тесты подтверждают, что собранная страница содержит и переопределённые блоки, и каркас из базы. Так работает наследование: двойная работа исключена, каждая страница определяет только своё.

### Разбор 3
`templates/macros.html`:

```html
{% macro card(title, text) %}
    <article class="card">
        <h3>{{ title }}</h3>
        <p>{{ text }}</p>
    </article>
{% endmacro %}
```

`templates/gallery.html`:

```html
{% from "macros.html" import card %}
<div class="gallery">
    {% for post in posts %}
        {{ card(post.title, post.text) }}
    {% endfor %}
</div>
```

Скрипт:

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"), autoescape=True)
posts = [
    {"title": "Python 3.13", "text": "Новый релиз"},
    {"title": "Jinja2", "text": "Шаблонизатор"},
    {"title": "Grid", "text": "Адаптивная сетка"},
]
print(env.get_template("gallery.html").render(posts=posts))
```

Что здесь происходит? Макрос `card` — это «функция» внутри шаблона: объявлена один раз, вызывается сколько угодно раз. `{% from "macros.html" import card %}` подтягивает её из отдельного файла — макросы можно переиспользовать на всех страницах. Цикл `{% for post in posts %}` проходит по списку постов и для каждого вызывает макрос. Получается чистая, повторяемая разметка без копипаста.

### Разбор 4
`unsafe.py`:

```python
from jinja2 import Environment

env = Environment()  # autoescape выключен по умолчанию
print(env.from_string("{{ user_input }}").render(
    user_input="<img src=x onerror=alert(1)>",
))
```

Вывод: сырой тег `<img src=x onerror=alert(1)>` — браузер его выполнит.

`safe.py`:

```python
from jinja2 import Environment

env = Environment(autoescape=True)
print(env.from_string("{{ user_input }}").render(
    user_input="<img src=x onerror=alert(1)>",
))
# &lt;img src=x onerror=alert(1)&gt;

print(env.from_string("{{ user_input|safe }}").render(
    user_input="<img src=x onerror=alert(1)>",
))
# <img src=x onerror=alert(1)>
```

Что здесь происходит? При `autoescape=True` спецсимволы превращаются в безопасные сущности: `<` → `&lt;`, `>` → `&gt;` — и браузер показывает их как текст. Фильтр `|safe` отключает экранирование и возвращает сырой HTML. Если применить его к пользовательскому вводу — злоумышленник сможет внедрить свой скрипт (XSS). Вывод: `|safe` — только для доверенного HTML.

### Разбор 5
Файл `test_jinja.py`:

```python
import pytest
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader


@pytest.fixture
def env():
    return Environment(loader=FileSystemLoader("templates"), autoescape=True)


def test_macro_renders_cards(env):
    template = env.get_template("gallery.html")
    html = template.render(posts=[
        {"title": "A", "text": "1"},
        {"title": "B", "text": "2"},
    ])
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.find_all("article", class_="card")
    assert len(cards) == 2
    assert cards[0].find("h3").get_text() == "A"
    assert cards[1].find("p").get_text() == "2"


def test_inheritance(env):
    html = env.get_template("about.html").render()
    soup = BeautifulSoup(html, "html.parser")
    assert soup.title.get_text() == "Обо мне"
    assert soup.find("main").find("h1") is not None


def test_autoescape_prevents_xss(env):
    html = env.from_string("{{ value }}").render(
        value="<script>alert(1)</script>")
    assert "<script>" not in html
    assert "&lt;script&gt;" in html


def test_truncate_filter(env):
    html = env.from_string("{{ text|truncate(10) }}").render(
        text="Очень длинное предложение текста")
    result = html.strip()
    assert len(result) < len("Очень длинное предложение текста")
    assert result.endswith("...")
```

Что здесь происходит? Фикстура `env` создаёт окружение с загрузчиком и autoescape — тесты не дублируют код. Проверка макроса считает карточки и заглядывает внутрь каждой. Тест autoescape гарантирует главное: чужой скрипт не попадёт в страницу. Тест `truncate` проверяет, что длинный текст обрезан и завершён многоточием. Все четыре теста запускаются командой `python -m pytest test_jinja.py`.
<!--/SOLUTION-->

<!--QUIZ-->
Что означают двойные фигурные скобки {{ }} в Jinja2?
- Вывод значения выражения
- Комментарий
- Оператор логики
* Правильный ответ: Вывод значения выражения
{{ выражение }} выводит результат в HTML.

Как называется оператор наследования шаблона?
- {% extend %}
- {% extends %}
- {% include %}
* Правильный ответ: {% extends %}
{% extends "base.html" %} — наследование от базового шаблона, и он должен быть первой строкой.

Что делает блок {% block content %}?
- Определяет место, которое дочерний шаблон может заполнить
- Комментирует код
- Подключает файл
* Правильный ответ: Определяет место, которое дочерний шаблон может заполнить
Блоки — «дыры» в базовом шаблоне, которые переопределяются наследниками.

Какой фильтр делает первую букву заглавной?
- upper
- capitalize
- title (для каждого слова)
- Выбери все подходящие
* Правильный ответ: capitalize
capitalize — первая буква строка заглавная, title — каждого слова.

Что делает {{ super() }}?
- Вставляет содержимое родительского блока
- Вызывает функцию
- Удаляет блок
* Правильный ответ: Вставляет содержимое родительского блока
super() позволяет дополнить родительский блок, не теряя его содержимое.

Что такое макрос в Jinja2?
- Функция внутри шаблона, переиспользуемый фрагмент разметки
- Встроенный фильтр
- Тип данных
* Правильный ответ: Функция внутри шаблона, переиспользуемый фрагмент разметки
Макросы объявляются через {% macro %} и вызываются как функции.

Что делает фильтр |join(", ")?
- Склеивает элементы списка через запятую с пробелом
- Добавляет элементы в список
- Сортирует список
* Правильный ответ: Склеивает элементы списка через запятую с пробелом
join превращает список в строку с указанным разделителем.

Что делает autoescape=True?
- Включает экранирование вывода — HTML-теги в данных становятся безопасным текстом
- Отключает проверку типов
- Ускоряет рендер
* Правильный ответ: Включает экранирование вывода — HTML-теги в данных становятся безопасным текстом
autoescape превращает спецсимволы в сущности, нейтрализуя XSS.

Когда можно использовать фильтр |safe?
- Только для доверенного HTML, не для пользовательского ввода
- Для любого ввода
- Никогда
* Правильный ответ: Только для доверенного HTML, не для пользовательского ввода
|safe отключает экранирование — на пользовательском вводе это уязвимость.

Что делает {% include %}?
- Вставляет содержимое другого шаблона в текущее место
- Наследует шаблон
- Импортирует макросы
* Правильный ответ: Вставляет содержимое другого шаблона в текущее место
include подключает готовый фрагмент (например, футер) в шаблон.
<!--/QUIZ-->
