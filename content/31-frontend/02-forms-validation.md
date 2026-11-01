---
title: Формы: валидация на клиенте и сервере
summary: Все типы полей ввода, связка label/input, клиентская валидация браузером и серверная — на Python.
order: 2
duration: 45 мин
difficulty: intermediate
tags: html, формы, валидация, flask, pytest
---

В этом уроке ты научишься создавать формы — от простого поля ввода до полноценной валидации, которая не даст сохранить мусорные данные. Запомни главное правило сразу: **валидация на клиенте — это удобство пользователя, а на сервере — безопасность данных**. Браузерную проверку можно обойти за секунду, поэтому сервер обязан проверять всё заново.

## Анатомия формы

Форма — это `<form>`. У неё два ключевых атрибута:

- `action` — куда отправлять данные (URL обработчика);
- `method` — способ отправки: `get` (параметры в адресе) или `post` (данные в теле запроса). Для форм с личными данными почти всегда `post`.

Каждое поле должно иметь подпись `<label>`, связанную с полем через атрибуты `for` и `id`. Это требование доступности: клик по подписи фокусирует поле, а скринридер зачитывает подпись перед полем.

```html
<form action="/register" method="post">
    <label for="name">Имя</label>
    <input id="name" name="name" type="text" required>

    <label for="email">Email</label>
    <input id="email" name="email" type="email" required>

    <button type="submit">Зарегистрироваться</button>
</form>
```

## Типы полей ввода

Атрибут `type` не просто меняет вид поля — браузер подключает проверку формата и правильную клавиатуру на телефонах:

| Тип | Что даёт |
|---|---|
| `text` | обычная строка |
| `email` | проверка, что введено похожее на email |
| `password` | скрывает символы |
| `number` | цифры, кнопки «вверх/вниз» |
| `tel` | телефонная клавиатура |
| `url` | проверка, что это ссылка |
| `date` | выбор даты из календаря |
| `search` | поле поиска с крестиком |
| `checkbox` | галочка |
| `radio` | выбор одного из группы |
| `range` | ползунок |
| `file` | выбор файла |
| `color` | выбор цвета |

Для выбора из списка есть `<select>` с `<option>`, для многострочного текста — `<textarea>`:

```html
<label for="city">Город</label>
<select id="city" name="city">
    <option value="msk">Москва</option>
    <option value="spb">Санкт-Петербург</option>
</select>

<label for="comment">Комментарий</label>
<textarea id="comment" name="comment" rows="4"></textarea>
```

## Клиентская валидация

Браузер умеет проверять данные до отправки. Основные атрибуты:

- `required` — поле обязательно;
- `minlength` / `maxlength` — длина строки;
- `min` / `max` — диапазон числа;
- `step` — шаг числа;
- `pattern` — регулярное выражение, которому должна соответствовать строка;
- `autocomplete` — подсказки браузера (`name`, `email`, `current-password` и другие).

```html
<label for="phone">Телефон</label>
<input id="phone" name="phone" type="tel"
       placeholder="+7 XXX XXX-XX-XX"
       pattern="\+7\s[0-9]{3}\s[0-9]{3}-[0-9]{2}-[0-9]{2}"
       required>
```

Невалидные поля браузер подсвечивает и блокирует отправку. Можно стилизовать состояния через псевдоклассы `:invalid` и `:valid`, а также отключить встроенную проверку атрибутом `novalidate` — например, если форму проверяет твой скрипт.

## Серверная валидация

Клиентская проверка — только первый рубеж. Представь, что кто-то отправил запрос напрямую, минуя браузер. Поэтому сервер обязан проверять всё. Вот минимальный обработчик на Flask, который возвращает ошибки в шаблон:

```python
from flask import Flask, render_template, request

app = Flask(__name__)

def validate_registration(data):
    errors = {}
    if not data.get("name") or len(data["name"].strip()) < 2:
        errors["name"] = "Имя должно содержать минимум 2 символа."
    if not data.get("email") or "@" not in data["email"]:
        errors["email"] = "Введите корректный email."
    return errors

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        errors = validate_registration(request.form)
        if not errors:
            return "Спасибо за регистрацию!", 200
        return render_template("register.html", errors=errors,
                               data=request.form)
    return render_template("register.html", errors={}, data={})
```

А в шаблоне ошибки выводятся рядом с полями. Кстати, именно здесь вступает в силу Jinja2 — с ним ты подробно познакомишься в пятом уроке, но базовый вывод уже сможешь использовать:

```html
{% for field, message in errors.items() %}
    <p class="error">{{ field }}: {{ message }}</p>
{% endfor %}
```

Обрати внимание: мы сохраняем введённые пользователем значения (`data`) и подставляем их обратно в поля — так человек не теряет данные из-за одной ошибки. Никогда не выводи ошибки и данные без экранирования: шаблонизатор должен быть настроен на `autoescape`, иначе пользовательский текст (например, `<script>`) выполнится на твоей странице — это XSS-уязвимость.

## Чек-лист формы

- У каждого поля есть `<label>` с `for` = `id` поля.
- Метод `post` для данных, меняющих состояние.
- `required`, `type`, `pattern`, `minlength` — на нужных полях.
- Сервер заново проверяет все данные.
- Ошибки выводятся понятным языком, значения не теряются.
- Никакой вывод без экранирования.

Теперь применим всё на практике: создадим форму регистрации, добавим проверки и напишем тесты и для разметки, и для серверной логики.

<!--TASK-->
### Задача 1
Создай файл `registration.html` с формой регистрации. Форма должна содержать:

- `<form>` с `action="/register"` и `method="post"`;
- поле «Имя» — `type="text"`;
- поле «Email» — `type="email"`;
- поле «Пароль» — `type="password"`;
- поле «Дата рождения» — `type="date"`;
- `<select>` «Город» с тремя вариантами (например, Москва, Санкт-Петербург, Казань);
- группу радио-кнопок «Пол» (мужской/женский/другое) в `<fieldset>` с `<legend>`;
- чекбокс «Согласен с условиями» (как в деревянных сайтах: согласие обязательно);
- `<textarea>` «Комментарий»;
- кнопку отправки.

У каждого поля должна быть подпись `<label>`, связанная через `for`/`id`. Сохрани и открой в браузере — убедись, что все типы полей отображаются корректно.

### Задача 2
Добавь в форму из задачи 1 клиентскую валидацию:

- имя: `required`, `minlength="2"`, `autocomplete="name"`;
- email: `required`, `type="email"`, `autocomplete="email"`;
- пароль: `required`, `minlength="8"`, `autocomplete="new-password"`;
- телефон-поле (добавь новое поле `type="tel"`): `pattern="\+7\s[0-9]{3}\s[0-9]{3}-[0-9]{2}-[0-9]{2}"` и `placeholder="+7 900 123-45-67"`;
- чекбокс согласия: `required`;
- дату рождения ограничь `max="2010-12-31"` (старше 15 лет).

Проверь в браузере: попробуй отправить пустую форму, неправильный email и телефон — браузер должен показать подсказки и не отправить форму.

### Задача 3
Напиши pytest-тест `test_form_structure.py`, который проверяет разметку формы из задачи 2. Тест должен покрыть:

- у формы `method="post"` и `action="/register"`;
- для каждого поля `<input>` существует связанный `<label>` (для совпадает с id);
- у поля email тип `email` и есть `required`;
- у пароля есть `minlength`;
- чекбокс согласия имеет `required`;
- поле телефон имеет атрибут `pattern`.

Используй `BeautifulSoup`. Ожидаемый результат: все проверки проходят, тест запускается через `python -m pytest test_form_structure.py`.

### Задача 4
Напиши на Python функцию `validate_registration(data)` (реализация может быть из теории) и маленькое Flask-приложение `app.py` с маршрутом `/register`, которое: при `GET` показывает форму; при `POST` вызывает валидацию; если ошибок нет — возвращает «Спасибо за регистрацию!»; если есть — рендерит шаблон `register.html` с ошибками и сохранёнными значениями.

Создай шаблон `register.html` (в папке `templates/`), который выводит форму и блок ошибок: `<p class="error">` для каждого поля с ошибкой. Проверь руками: запусти `flask --app app run`, зайди на `http://127.0.0.1:5000/register`, отправь пустую форму — увидишь ошибки; отправь валидные данные — увидишь благодарность.

### Задача 5
Напиши pytest-тесты для серверной части из задачи 4. Создай файл `test_server.py`:

- параметризованный тест для `validate_registration`: пустой словарь, имя короче 2 символов, email без `@`, валидные данные — проверь, какие ошибки возвращаются;
- тест рендера: отрендерь шаблон `register.html` через jinja2 с ошибками `{"email": "Введите корректный email."}` и проверь через `BeautifulSoup`, что в HTML есть `<p class="error">` с этим текстом;
- тест безопасного вывода: передай в шаблон значение поля с HTML-тегом (например, `<script>alert(1)</script>`) и проверь, что отрендеренный текст не содержит живого тега `<script>` (то есть он экранирован).

Ожидаемый результат: все тесты проходят.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Каждое поле начинается с `<label for="уникальный-id">`, а у `<input>` должен быть такой же `id`. Для радио-группы оберни кнопки в `<fieldset><legend>Пол</legend>...</fieldset>`. Для всех радио-кнопок используй одно имя `name="gender"` — так браузер знает, что это одна группа.

### Подсказка 2
Не забудь, что `pattern` задаётся как **регулярное выражение**, и в нём пробелы имеют значение. В HTML-атрибуте обратный слеш пишется как есть: `pattern="\+7\s[0-9]{3}\s..."`. Для проверки ограничения даты используй `max` в формате ГГГГ-ММ-ДД.

### Подсказка 3
Пройдись по всем инпутам циклом: `for field in soup.find_all("input"):`. Для каждого найди `label` через `soup.find("label", attrs={"for": field.get("id")})`. Особый случай — поле `type="checkbox"` с `name="agree"`. Используй `field.get("required") is not None` и `field.get("minlength")`.

### Подсказка 4
Функция валидации возвращает словарь ошибок: ключ — имя поля, значение — текст ошибки. Учти, что `request.form` — это словарь «имя поля → значение». В шаблоне ошибки перебирай циклом `{% for field, message in errors.items() %}`. Возврат рендера: `render_template("register.html", errors=errors, data=request.form)`.

### Подсказка 5
Для рендера без запуска сервера используй jinja2 напрямую: `from jinja2 import Environment, FileSystemLoader; env = Environment(loader=FileSystemLoader("templates"), autoescape=True)`. Проверка экранирования: `assert "<script>" not in html` — но с учётом того, что jinja2 при autoescape выведет `&lt;script&gt;`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Пример формы: 

```html
<form action="/register" method="post">
    <label for="name">Имя</label>
    <input id="name" name="name" type="text">

    <label for="email">Email</label>
    <input id="email" name="email" type="email">

    <label for="password">Пароль</label>
    <input id="password" name="password" type="password">

    <label for="birth">Дата рождения</label>
    <input id="birth" name="birth" type="date">

    <label for="city">Город</label>
    <select id="city" name="city">
        <option value="msk">Москва</option>
        <option value="spb">Санкт-Петербург</option>
        <option value="kzn">Казань</option>
    </select>

    <fieldset>
        <legend>Пол</legend>
        <label><input type="radio" name="gender" value="male"> Мужской</label>
        <label><input type="radio" name="gender" value="female"> Женский</label>
        <label><input type="radio" name="gender" value="other"> Другое</label>
    </fieldset>

    <label><input type="checkbox" name="agree"> Согласен с условиями</label>

    <label for="comment">Комментарий</label>
    <textarea id="comment" name="comment" rows="4"></textarea>

    <button type="submit">Отправить</button>
</form>
```

Что здесь происходит? Подписи связаны с полями через `for`/`id` — благодаря этому клик по тексту подписи ставит курсор в поле. Радио-кнопки имеют одно имя `name="gender"`, поэтому браузер считает их одной группой: выбрать можно только одну. `<fieldset>` и `<legend>` группируют их визуально и семантически. Отправка происходит методом `post` на адрес `/register` — для регистрационных данных это правильный выбор.

### Разбор 2
Добавляем атрибуты валидации:

```html
<input id="name" name="name" type="text" required
       minlength="2" autocomplete="name">
<input id="email" name="email" type="email" required autocomplete="email">
<input id="password" name="password" type="password" required
       minlength="8" autocomplete="new-password">
<input id="phone" name="phone" type="tel" required
       pattern="\+7\s[0-9]{3}\s[0-9]{3}-[0-9]{2}-[0-9]{2}"
       placeholder="+7 900 123-45-67">
<input id="birth" name="birth" type="date" required max="2010-12-31">
<input type="checkbox" name="agree" required>
```

Что здесь происходит? `required` запрещает отправку пустого поля; `minlength` проверяет длину строки; `type="email"` включает проверку формата; `pattern` требует, чтобы телефон совпадал с регулярным выражением `\+7\s[0-9]{3}\s[0-9]{3}-[0-9]{2}-[0-9]{2}` — это формат `+7 900 123-45-67`; `max="2010-12-31"` не даёт выбрать дату рождения «моложе» 15 лет; `autocomplete` включает браузерные подсказки.

### Разбор 3
Тест `test_form_structure.py`:

```python
from bs4 import BeautifulSoup


def load_form():
    with open("registration.html", encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")


def test_form_method_and_action():
    soup = load_form()
    form = soup.find("form")
    assert form.get("method") == "post"
    assert form.get("action") == "/register"


def test_every_input_has_label():
    soup = load_form()
    for field in soup.find_all("input"):
        if field.get("type") == "radio":
            continue  # радио-кнопки обёрнуты в label
        label = soup.find("label", attrs={"for": field.get("id")})
        assert label is not None, f"Нет label для поля {field.get('name')}"


def test_email_type_and_required():
    soup = load_form()
    email = soup.find("input", attrs={"name": "email"})
    assert email.get("type") == "email"
    assert email.get("required") is not None


def test_password_minlength():
    soup = load_form()
    password = soup.find("input", attrs={"name": "password"})
    assert password.get("minlength") == "8"


def test_agree_required():
    soup = load_form()
    agree = soup.find("input", attrs={"name": "agree"})
    assert agree.get("required") is not None


def test_phone_pattern():
    soup = load_form()
    phone = soup.find("input", attrs={"name": "phone"})
    assert "pattern" in phone.attrs
```

Что здесь происходит? Мы загружаем HTML в BeautifulSoup и проверяем атрибуты. Для радио-кнопок мы их пропускаем намеренно — они обёрнуты в `<label>` целиком, и отдельная подпись им не нужна. Остальным полям подпись обязательна: если `label` с совпадающим `for` не найдётся, `assert` упадёт с понятным сообщением, в котором указано имя проблемного поля.

### Разбор 4
Файл `app.py`:

```python
from flask import Flask, render_template, request

app = Flask(__name__)


def validate_registration(data):
    errors = {}
    name = data.get("name", "").strip()
    if len(name) < 2:
        errors["name"] = "Имя должно содержать минимум 2 символа."
    email = data.get("email", "").strip()
    if "@" not in email or "." not in email:
        errors["email"] = "Введите корректный email."
    if len(data.get("password", "")) < 8:
        errors["password"] = "Пароль должен быть не короче 8 символов."
    return errors


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        errors = validate_registration(request.form)
        if not errors:
            return "Спасибо за регистрацию!", 200
        return render_template("register.html", errors=errors,
                               data=request.form)
    return render_template("register.html", errors={}, data={})
```

Шаблон `templates/register.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head><meta charset="UTF-8"><title>Регистрация</title></head>
<body>
    <h1>Регистрация</h1>
    {% for field, message in errors.items() %}
        <p class="error">{{ field }}: {{ message }}</p>
    {% endfor %}
    <form action="/register" method="post">
        <label for="name">Имя</label>
        <input id="name" name="name" type="text"
               value="{{ data.get('name', '') }}">
        <label for="email">Email</label>
        <input id="email" name="email" type="email"
               value="{{ data.get('email', '') }}">
        <label for="password">Пароль</label>
        <input id="password" name="password" type="password">
        <button type="submit">Отправить</button>
    </form>
</body>
</html>
```

Что здесь происходит? `validate_registration` возвращает словарь ошибок: ключ — имя поля, значение — текст. В обработчике при `GET` мы показываем пустую форму, при `POST` — валидируем и либо возвращаем благодарность, либо рендерим шаблон с ошибками. В шаблоне ошибки выводятся циклом, а значения `data` подставляются обратно в `value` полей — пользователь не теряет данные.

### Разбор 5
Файл `test_server.py`:

```python
import pytest
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

from app import validate_registration


@pytest.mark.parametrize("data, expected", [
    ({}, {"name", "email", "password"}),
    ({"name": "А", "email": "a@b.ru", "password": "12345678"},
     {"name"}),
    ({"name": "Аня", "email": "непочта", "password": "12345678"},
     {"email"}),
    ({"name": "Аня", "email": "a@b.ru", "password": "12345678"},
     set()),
])
def test_validate_registration(data, expected):
    assert set(validate_registration(data)) == expected


def test_register_template_renders_errors():
    env = Environment(loader=FileSystemLoader("templates"),
                      autoescape=True)
    template = env.get_template("register.html")
    html = template.render(errors={"email": "Введите корректный email."},
                           data={})
    soup = BeautifulSoup(html, "html.parser")
    error = soup.find("p", class_="error")
    assert error is not None
    assert "Введите корректный email." in error.get_text()


def test_template_escapes_user_input():
    env = Environment(loader=FileSystemLoader("templates"),
                      autoescape=True)
    template = env.get_template("register.html")
    html = template.render(errors={}, data={"name": "<script>alert(1)</script>"})
    assert "<script>" not in html
    assert "&lt;script&gt;" in html
```

Что здесь происходит? Параметризованный тест покрывает четыре сценария: полностью пустые данные (ошибки по всем трём полям), слишком короткое имя, неверный email и валидные данные (без ошибок). Тест рендера создаёт окружение jinja2 с `autoescape=True` и проверяет, что ошибка попадает в `<p class="error">`. Последний тест доказывает безопасность: значение с HTML-тегом экранируется в `&lt;script&gt;`, и живого тега в выводе нет.
<!--/SOLUTION-->

<!--QUIZ-->
Какой метод HTTP обычно используется для отправки регистрационной формы?
- get
- post
- put
* Правильный ответ: post
Данные формы, меняющие состояние, отправляют методом post.

Как связано поле input с его подписью label?
- Через атрибуты for и id
- Они просто должны стоять рядом
- Через атрибут name
* Правильный ответ: Через атрибуты for и id
for у label должен совпадать с id поля — так оформляется связь.

Какой тип поля включает проверку формата адреса электронной почты?
- text
- email
- password
* Правильный ответ: email
type="email" заставляет браузер проверять, что введено похожее на email значение.

Что делает атрибут pattern?
- Указывает образец пароля
- Задаёт регулярное выражение для проверки значения
- Включает подсказки браузера
* Правильный ответ: Задаёт регулярное выражение для проверки значения
pattern проверяет строку на соответствие регулярному выражению.

Зачем нужна серверная валидация, если есть клиентская?
- Чтобы ускорить работу браузера
- Потому что клиентскую проверку можно обойти — сервер обязан проверять заново
- Она не нужна
* Правильный ответ: Потому что клиентскую проверку можно обойти — сервер обязан проверять заново
Браузерную проверку легко обойти, поэтому без серверной не обойтись.

Какой атрибут запрещает отправку пустого поля?
- placeholder
- required
- readonly
* Правильный ответ: required
required делает поле обязательным для заполнения.

Что такое XSS-уязвимость?
- Уязвимость, связанная с подстановкой пользовательского текста в HTML без экранирования
- Ошибка в CSS-стилях
- Медленная загрузка страницы
* Правильный ответ: Уязвимость, связанная с подстановкой пользовательского текста в HTML без экранирования
Если не экранировать ввод, пользователь может внедрить чужой скрипт.

Какой тег объединяет группу радио-кнопок с заголовком?
- div
- fieldset + legend
- group
* Правильный ответ: fieldset + legend
fieldset группирует поля, а legend даёт им заголовок.

Что делает type="date"?
- Показывает календарь для выбора даты
- Превращает поле в текст
- Ничего не меняет
* Правильный ответ: Показывает календарь для выбора даты
Поле даты открывает календарь и возвращает значение в формате ГГГГ-ММ-ДД.

Что делает атрибут autocomplete="email"?
- Заполняет поле прошлым введённым email
- Проверяет формат email
- Скрывает поле
* Правильный ответ: Заполняет поле прошлым введённым email
autocomplete включает браузерные подсказки и авто-заполнение.
<!--/QUIZ-->
