---
title: Jinja2 и формы во Flask
summary: Шаблоны Jinja2, передача данных в HTML, циклы и условия в шаблонах, обработка форм.
order: 5
duration: 45 мин
difficulty: intermediate
---

В предыдущем уроке Flask возвращал обычные строки. Для настоящего сайта этого мало: нужны HTML-страницы, причём с динамическим содержимым. Ручное склеивание строк в Python быстро становится нечитаемым. Flask решает проблему системой шаблонов Jinja2.

## Зачем шаблоны

Шаблон — это HTML-файл с местами для данных. Логика живёт в Python, а представление — в шаблоне. Такое разделение упрощает поддержку проекта: дизайнер правит шаблоны, программист — логику, и они не мешают друг другу.

## Подготовка

Создай папку `templates` рядом с приложением — Flask ищет шаблоны именно там. Передай шаблон через `render_template`:

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", name="Аня", age=25)
```

Данные передаются в шаблон вторым аргументом — парами имя/значение.

## Синтаксис Jinja2

- `{{ выражение }}` — вывести значение;
- `{% if ... %}` / `{% endif %}` — условие;
- `{% for ... %}` / `{% endfor %}` — цикл;
- фильтры: `{{ name|upper }}` — верхний регистр, `{{ items|length }}` — длина списка.

Пример шаблона:

```html
<h1>Привет, {{ name }}!</h1>

{% if age >= 18 %}
    <p>Ты взрослый.</p>
{% else %}
    <p>Ты несовершеннолетний.</p>
{% endif %}

<ul>
{% for city in cities %}
    <li>{{ city }}</li>
{% endfor %}
</ul>
```

## Формы

Форма — способ собрать данные от пользователя. HTML-форма отправляет данные на сервер:

```html
<form method="post" action="/hello">
    <input name="name" placeholder="Твоё имя">
    <button type="submit">Поздороваться</button>
</form>
```

Атрибут `name` у поля — ключ, по которому сервер достанет значение.

## Обработка формы во Flask

Данные формы доступны в `request.form`:

```python
from flask import request

@app.route("/hello", methods=["POST"])
def hello():
    name = request.form.get("name", "гость")
    return render_template("hello.html", name=name)
```

`request.form` ведёт себя как словарь, а `.get(key, default)` позволяет указать значение по умолчанию на случай пустой формы.

## Полный пример

`app.py`:

```python
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello", methods=["POST"])
def hello():
    name = request.form.get("name", "гость")
    return render_template("hello.html", name=name)

if __name__ == "__main__":
    app.run(debug=True)
```

`templates/index.html` — форма из примера выше, а `templates/hello.html`:

```html
<h1>Привет, {{ name }}!</h1>
<a href="/">Назад</a>
```

## Итог

Мы связали две стороны: HTML-формы собирают данные, Jinja2 наполняет страницы результатами. Это база любого сайта на Flask.

<!--TASK-->
### Задача 1

Создай приложение `template_app.py` и папку `templates`. В `templates` создай файл `hello.html` с заголовком `<h1>Привет, {{ name }}!</h1>`. В `template_app.py` определи маршрут `/`, который вызывает `render_template("hello.html", name="Аня")`. Запусти приложение и открой `http://127.0.0.1:5000/`: на странице должно появиться «Привет, Аня!». Это докажет, что переменная из Python передалась в шаблон.

### Задача 2

Научись выводить списки. В `template_app.py` добавь в маршрут `/` передачу списка городов: `cities=["Москва", "Казань", "Новосибирск"]`. В `hello.html` под заголовком добавь маркированный список `<ul>`, внутри которого цикл `{% for city in cities %}` выводит `<li>{{ city }}</li>`. Обнови страницу: под приветствием должен появиться список из трёх городов — по одному пункту на город.

### Задача 3

Добавь условие. В маршрут `/` передай ещё переменную `age=25`. В `hello.html` добавь блок `{% if age >= 18 %}`: если условие истинно, выводи `<p>Ты взрослый.</p>`, иначе — `<p>Ты несовершеннолетний.</p>`. Не забудь закрыть конструкцию тегом `{% endif %}`. Проверь оба случая: поменяй `age` на `15` — текст должен смениться на «Ты несовершеннолетний».

### Задача 4

Создай форму. В `templates` создай `index.html` с формой: `<form method="post" action="/hello">`, поле `<input name="name" placeholder="Твоё имя">` и кнопку `<button type="submit">Поздороваться</button>`. В `template_app.py` добавь маршрут `/hello` с `methods=["POST"]`, который читает имя через `request.form.get("name", "гость")` и рендерит `hello.html` с этим именем. Заполни форму и отправь: должна появиться страница с приветствием именно по введённому имени.

### Задача 5

Собери финальное приложение `friends_app.py`. Оно должно: на `/` показывать форму из двух полей — `name` и `city` — с кнопкой отправки; форма отправляет POST на `/greet`; `/greet` читает оба поля, формирует список городов `[city, "Москва", "Казань", "Новосибирск"]` и рендерит `greet.html`. В `greet.html` приветствуй пользователя по имени (если имя пустое — «Привет, гость!») и выведи список из четырёх городов. Проверь отправку с заполненными и пустыми полями.

<!--/TASK-->

<!--HINT-->
### Подсказка 1

Flask ищет шаблоны в папке `templates` рядом с приложением. Вывод переменной в Jinja2 — двойные фигурные скобки: `{{ name }}`. Имя переменной в шаблоне должно совпадать с именем аргумента в `render_template`.

### Подсказка 2

Цикл в шаблоне: `{% for city in cities %} ... {% endfor %}`. Внутри — `{{ city }}`. Список передаётся так же, как обычная переменная: `render_template("hello.html", cities=cities)`. Каждый элемент списка станет отдельным `<li>`.

### Подсказка 3

Условие в Jinja2: `{% if age >= 18 %} ... {% else %} ... {% endif %}`. Сравнение пишется обычным Python-синтаксисом. Проверь оба значения `age` — велика вероятность опечатки в имени переменной или в отсутствии `{% endif %}`.

### Подсказка 4

Форма отправляет данные на адрес из атрибута `action` методом из `method`. Сервер читает их через `request.form.get("name", "гость")` — второй аргумент это значение по умолчанию. Не забудь указать `methods=["POST"]` в декораторе маршрута.

### Подсказка 5

Передай в `render_template` и `name`, и `city`, и весь список: `cities=[city, "Москва", "Казань", "Новосибирск"]`. Условие `{% if name %}` покроет случай пустого имени. Достаточно двух шаблонов: `index.html` с формой и `greet.html` с результатом.

<!--/HINT-->

<!--SOLUTION-->
### Разбор 1

`template_app.py`:

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("hello.html", name="Аня")

if __name__ == "__main__":
    app.run(debug=True)
```

`templates/hello.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head><meta charset="utf-8"><title>Приветствие</title></head>
<body>
    <h1>Привет, {{ name }}!</h1>
</body>
</html>
```

Разбор по шагам:

- Папка `templates` должна лежать рядом с `template_app.py` — там Flask ищет шаблоны по умолчанию.
- `render_template("hello.html", name="Аня")` — первая строка: имя файла шаблона, дальше — пары «имя переменной → значение».
- В шаблоне переменные выводятся двойными фигурными скобками: `{{ name }}`. В момент рендера Jinja2 подставит на это место значение «Аня».
- Flask соберёт готовый HTML и вернёт его как ответ. Браузер покажет «Привет, Аня!».
- Если вместо имени появится пустое место — значит, имена в `render_template` и в шаблоне не совпали.

### Разбор 2

`template_app.py`:

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template(
        "hello.html",
        name="Аня",
        cities=["Москва", "Казань", "Новосибирск"],
    )

if __name__ == "__main__":
    app.run(debug=True)
```

`templates/hello.html`:

```html
<h1>Привет, {{ name }}!</h1>
<ul>
    {% for city in cities %}
        <li>{{ city }}</li>
    {% endfor %}
</ul>
```

Разбор по шагам:

- Список передаётся в шаблон как обычная переменная: `cities=[...]`.
- Цикл `{% for city in cities %}` перебирает элементы списка. Для каждого элемента выполняется тело цикла — строка с `{{ city }}`.
- Конструкция обязательно закрывается тегом `{% endfor %}` — иначе Jinja2 выдаст ошибку рендера.
- Результат — HTML с тремя пунктами `<li>`: по одному на город. Порядок элементов сохраняется: цикл идёт слева направо по списку.
- Так выводятся любые коллекции: задачи, статьи, товары. Одна страница обслуживает список любой длины.

### Разбор 3

`template_app.py` передаёт `age=25`; `templates/hello.html`:

```html
<h1>Привет, {{ name }}!</h1>
<ul>
    {% for city in cities %}
        <li>{{ city }}</li>
    {% endfor %}
</ul>

{% if age >= 18 %}
    <p>Ты взрослый.</p>
{% else %}
    <p>Ты несовершеннолетний.</p>
{% endif %}
```

Разбор по шагам:

- Условие `{% if age >= 18 %}` пишется почти как в Python; работает и `==`, и `<`, и `and`/`or`.
- Ветка `{% else %}` необязательна, но здесь она нужна для второго варианта текста.
- Конструкция закрывается `{% endif %}`. Забытый `{% endif %}` — самая частая причина ошибок в шаблонах.
- При `age=25` условие истинно — выведется «Ты взрослый». При `age=15` сработает `else`.
- В шаблоне не должно быть сложной логики: максимум — условие или цикл. Бизнес-логика остаётся в Python.

### Разбор 4

`templates/index.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head><meta charset="utf-8"><title>Форма</title></head>
<body>
    <form method="post" action="/hello">
        <input name="name" placeholder="Твоё имя">
        <button type="submit">Поздороваться</button>
    </form>
</body>
</html>
```

`template_app.py`:

```python
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello", methods=["POST"])
def hello():
    name = request.form.get("name", "гость")
    return render_template("hello.html", name=name)

if __name__ == "__main__":
    app.run(debug=True)
```

Разбор по шагам:

- Атрибут `method="post"` у формы говорит браузеру, каким методом отправлять данные; `action="/hello"` — на какой адрес.
- Поле `<input name="name">` — ключ `name` попадает в данные формы. Без атрибута `name` поле проигнорируется.
- В обработчике `request.form` ведёт себя как словарь: `request.form.get("name", "гость")` вернёт введённое имя или «гость», если поле пустое.
- Без `methods=["POST"]` маршрут принимал бы только GET, а форма шлёт POST — вернулась бы ошибка 405.
- После чтения данных происходит рендер `hello.html` уже с реальным именем пользователя.

### Разбор 5

`friends_app.py`:

```python
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/greet", methods=["POST"])
def greet():
    name = request.form.get("name", "").strip()
    city = request.form.get("city", "").strip()
    cities = [city, "Москва", "Казань", "Новосибирск"]
    return render_template("greet.html", name=name, cities=cities)

if __name__ == "__main__":
    app.run(debug=True)
```

`templates/index.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head><meta charset="utf-8"><title>Друзья</title></head>
<body>
    <form method="post" action="/greet">
        <p>Имя: <input name="name"></p>
        <p>Город: <input name="city"></p>
        <button type="submit">Отправить</button>
    </form>
</body>
</html>
```

`templates/greet.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head><meta charset="utf-8"><title>Приветствие</title></head>
<body>
    {% if name %}
        <h1>Привет, {{ name }}!</h1>
    {% else %}
        <h1>Привет, гость!</h1>
    {% endif %}
    <ul>
        {% for city in cities %}
            <li>{{ city }}</li>
        {% endfor %}
    </ul>
    <a href="/">Назад</a>
</body>
</html>
```

Разбор по шагам:

- Форма с двумя полями и методом POST отправляет данные на `/greet`.
- `request.form.get("name", "").strip()` — чтение поля с запасным значением (пустая строка) и очисткой от пробелов. `strip()` убирает случайные пробелы, введённые пользователем.
- `cities = [city, "Москва", "Казань", "Новосибирск"]` — город пользователя становится первым элементом списка.
- В `greet.html` условие `{% if name %}` проверяет непустое имя: пустая строка — это ложь в Python, поэтому она уйдёт в ветку `else` и выведется «Привет, гость!».
- Цикл `{% for city in cities %}` выводит четыре пункта списка. Один и тот же шаблон обслуживает и заполненную, и пустую форму.

<!--/SOLUTION-->

<!--QUIZ-->
Как вывести переменную в шаблоне Jinja2?
- {{ name }}
- {% name %}
- [[ name ]]
- $name$
* Правильный ответ: {{ name }}
Двойные фигурные скобки выводят значение выражения.

Чем заканчивается цикл {% for %} в шаблоне?
- {% break %}
- {% endfor %}
- {% stop %}
- {% done %}
* Правильный ответ: {% endfor %}
Конструкции Jinja2 закрываются парными тегами: endfor, endif, endblock.

Где Flask по умолчанию ищет шаблоны?
- В папке static
- В папке templates
- В корне проекта
- В папке pages
* Правильный ответ: В папке templates
Создай папку templates рядом с приложением.

В каком объекте лежат данные отправленной POST-формы?
- request.args
- request.form
- request.cookies
- request.data
* Правильный ответ: request.form
По атрибуту name поля можно достать значение методом get.

Что вернёт request.form.get("name", "гость"), если поля name в форме нет?
- Ошибку
- Пустую строку
- "гость"
- None
* Правильный ответ: "гость"
Второй аргумент — значение по умолчанию, если ключ отсутствует.

Какой фильтр Jinja2 переводит строку в верхний регистр?
- big
- uppercase
- upper
- caps
* Правильный ответ: upper
{{ name|upper }} — один из самых простых фильтров.
<!--/QUIZ-->
