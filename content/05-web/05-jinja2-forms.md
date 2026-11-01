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
**Задача.** Создай приложение `friends_app.py` и папку `templates`. Приложение должно:

1. На `/` показывать форму из двух полей: `name` (имя) и `city` (город), с кнопкой отправки;
2. Форма отправляет POST на `/greet`;
3. `/greet` читает оба поля и рендерит шаблон `greet.html`, который:
   - приветствует пользователя по имени (`Привет, Аня!`);
   - выводит список городов: первый — тот, что ввёл пользователь, плюс `Москва`, `Казань`, `Новосибирск`;
   - если имя пустое, выводит `Привет, гость!`.

Ожидаемый результат: после отправки формы — страница с приветствием и списком из четырёх городов.
<!--/TASK-->

<!--HINT-->
Передай в `render_template` и `name`, и `city`, и весь список городов: `cities=[city, "Москва", ...]`. В шаблоне условие `{% if name %}` покроет случай пустого имени, а цикл `{% for %}` выведет города.
<!--/HINT-->

<!--SOLUTION-->
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

- Маршрут `/` просто отдаёт форму: статичный шаблон `index.html`. Метод формы `post`, адрес `action="/greet"` — туда уйдут данные.
- Поля формы имеют атрибуты `name="name"` и `name="city"` — по ним Flask найдёт значения в `request.form`.
- В `greet()` мы читаем данные: `request.form.get("name", "")` возвращает значение поля или пустую строку, если оно отсутствует. Метод `.strip()` убирает лишние пробелы — классическая подготовка пользовательского ввода.
- `cities = [city, "Москва", "Казань", "Новосибирск"]` — список городов, первый элемент — город пользователя. При пустом поле в списке будет пустая строка, поэтому лучше не отправлять форму без города.
- `render_template("greet.html", name=name, cities=cities)` передаёт в шаблон обе переменные.
- В `greet.html` условие `{% if name %}` проверяет, непустое ли имя: в Python истина — непустая строка, поэтому `""` попадёт в ветку `else` и выведется «гость».
- Цикл `{% for city in cities %}` перебирает список — пункты `<li>` появятся для каждого города.
- Ссылка на `/` возвращает к форме.

Запусти `python friends_app.py`, отправь форму — и увидишь приветствие со списком городов.
<!--/SOLUTION-->
