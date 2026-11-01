---
title: Проект: ToDo-менеджер на Flask
summary: Создаём веб-приложение для управления задачами: список дел, добавление, выполнение, удаление, хранение в SQLite.
order: 2
duration: 90 мин
difficulty: intermediate
---

Привет! Этот проект — твой первый настоящий веб-сайт. Мы напишем простой ToDo-менеджер: страницу со списком задач, форму добавления, кнопки «Выполнено» и «Удалить». Все данные будут храниться в базе SQLite.

## О проекте

Стек проекта: Flask (веб-фреймворк), Jinja2 (шаблоны — идут вместе с Flask) и SQLite (база данных, встроена в Python). Приложение работает так:

- на главной странице виден список задач;
- через форму добавляется новая задача;
- кнопка «✓» помечает задачу выполненной;
- кнопка «✕» удаляет задачу;
- все изменения сохраняются в файле базы данных.

## План сборки

1. Подготовить окружение и установить Flask.
2. Создать каркас приложения с главной страницей.
3. Подключить SQLite и таблицу задач.
4. Научиться показывать список задач через шаблон.
5. Добавить форму и маршрут для новых задач.
6. Добавить пометку «выполнено» и удаление.
7. Запустить и протестировать.

## Шаг 1. Окружение и установка

Создай папку `todo_app`, внутри неё виртуальное окружение и установи Flask:

```bash
mkdir todo_app
cd todo_app
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
pip install flask
```

Виртуальное окружение изолирует зависимости проекта от остальной системы.

## Шаг 2. Каркас приложения

Создай файл `app.py`:

```python
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", tasks=[])
```

`@app.route("/")` связывает адрес `/` с функцией `index()`. `render_template` подставляет данные в шаблон.

## Шаг 3. База данных

SQLite — это один файл. Работать с ним можно через встроенный модуль `sqlite3`. Создадим вспомогательные функции для работы с таблицей задач:

```python
import sqlite3

DB = "tasks.db"


def init_db():
    con = sqlite3.connect(DB)
    con.execute(
        "CREATE TABLE IF NOT EXISTS tasks ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "title TEXT NOT NULL,"
        "done INTEGER DEFAULT 0)"
    )
    con.commit()
    con.close()


def get_tasks():
    con = sqlite3.connect(DB)
    rows = con.execute("SELECT id, title, done FROM tasks ORDER BY id").fetchall()
    con.close()
    return [{"id": r[0], "title": r[1], "done": bool(r[2])} for r in rows]
```

Таблица `tasks` содержит три поля: `id`, `title` (текст задачи) и `done` (0 или 1). `get_tasks()` читает все строки и превращает их в список словарей — так удобнее работать в шаблоне.

## Шаг 4. Шаблоны Jinja2

Шаблоны живут в папке `templates/`. Создай `templates/base.html` — общую рамку, и `templates/index.html` — содержимое главной страницы. В шаблонах используется синтаксис Jinja2: `{{ переменная }}` — вывод, `{% for ... %}` — цикл.

```html
<!doctype html>
<html>
<head><meta charset="utf-8"><title>ToDo</title></head>
<body>
  <h1>Мои задачи</h1>
  <ul>
    {% for task in tasks %}
      <li>
        {% if task.done %}<s>{{ task.title }}</s>{% else %}{{ task.title }}{% endif %}
      </li>
    {% endfor %}
  </ul>
</body>
</html>
```

## Шаг 5. Форма добавления

В HTML-форме метод `post` отправляет данные на сервер. Добавим форму в `index.html`:

```html
<form method="post" action="/add">
  <input type="text" name="title" placeholder="Новая задача" required>
  <button type="submit">Добавить</button>
</form>
```

А в `app.py` — маршрут, который принимает POST-запрос:

```python
from flask import request, redirect, url_for

@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"].strip()
    if title:
        con = sqlite3.connect(DB)
        con.execute("INSERT INTO tasks (title) VALUES (?)\ (title,))
        con.commit()
        con.close()
    return redirect(url_for("index"))
```

`request.form["title"]` — значение поля с именем `title`. `redirect(url_for("index"))` возвращает пользователя на главную. Знак `?` в SQL — это плейсхолдер: библиотека сама подставит значение безопасно, без инъекций.

## Шаг 6. Выполнение и удаление

Добавим два маршрута. Первый помечает задачу выполненной, второй удаляет её:

```python
@app.route("/done/<int:task_id>")
def done(task_id):
    con = sqlite3.connect(DB)
    con.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    con.commit()
    con.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete(task_id):
    con = sqlite3.connect(DB)
    con.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    con.commit()
    con.close()
    return redirect(url_for("index"))
```

Конвертер `<int:task_id>` превращает кусок URL в целое число. В шаблоне рядом с каждой задачей размести ссылки на эти адреса.

## Шаг 7. Запуск

Перед первым запуском вызови `init_db()`, затем:

```bash
python app.py
```

Открой http://127.0.0.1:5000 — приложение работает.

## Итог урока

Мы научились:

- создавать приложение Flask и маршруты;
- подключать SQLite и выполнять запросы;
- использовать шаблоны Jinja2 с циклами и условиями;
- принимать данные форм и делать редирект.

Теперь усовершенствуем проект.

<!--TASK-->
### Задача 1
Создай папку todo_app и внутри неё виртуальное окружение (python -m venv venv), активируй его и установи Flask командой pip install flask. Затем создай файл app.py: приложение Flask с маршрутом "/", который возвращает render_template("index.html", tasks=[]). Создай папку templates и шаблон index.html с заголовком «Мои задачи» и пустым списком. Ожидаемый результат: при запуске python app.py страница http://127.0.0.1:5000 показывает заголовок и пустой список.

### Задача 2
Добавь в app.py работу с SQLite: модуль sqlite3, константу DB = "tasks.db", функцию init_db(), которая создаёт таблицу tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, done INTEGER DEFAULT 0), и функцию get_tasks(), возвращающую список словарей. Вызови init_db() при старте и добавь пару задач вручную через sqlite3 или прямо в коде. В шаблоне выведи список через цикл {% for task in tasks %}. Ожидаемый результат: записи из базы отображаются на главной странице.

### Задача 3
Добавь в index.html форму: поле input с name="title" и placeholder, кнопку «Добавить», method="post", action="/add". В app.py создай маршрут "/add" с methods=["POST"]: читай request.form["title"], очищай от пробелов через strip() и, если строка не пустая, вставляй запись в таблицу через INSERT с плейсхолдером "?". После добавления верни пользователя на главную через redirect(url_for("index")). Ожидаемый результат: задача из формы появляется в списке на главной странице.

### Задача 4
Добавь два маршрута: "/done/<int:task_id>" — выполняет UPDATE tasks SET done = 1 WHERE id = ?, и "/delete/<int:task_id>" — выполняет DELETE FROM tasks WHERE id = ?, после чего оба делают редирект на главную. В шаблоне рядом с каждой задачей размести ссылки «✓» и «✕» на эти адреса, а выполненные задачи выводи зачёркнутыми через тег <s> внутри условия {% if task.done %}. Ожидаемый результат: клик по «✓» зачёркивает задачу, клик по «✕» удаляет её.

### Задача 5
Добавь фильтр по статусу: в шаблоне три ссылки — «Все» (?filter=), «Активные» (?filter=active), «Выполненные» (?filter=done). В функции index() читай request.args.get("filter") и передавай в get_tasks(filter_by), где в зависимости от значения добавляй WHERE done = 0 или WHERE done = 1. Добавь счётчик «Осталось: N» и ссылку «↺» рядом с выполненными задачами — маршрут "/undo/<int:task_id>", меняющий done обратно на 0. Ожидаемый результат: ссылки фильтруют список, счётчик обновляется.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Команда активации зависит от ОС: venv\Scripts\activate на Windows и source venv/bin/activate на macOS/Linux. Не забудь импортировать from flask import Flask, render_template и вызвать app.run() в конце файла, например внутри if __name__ == "__main__".

### Подсказка 2
Каждая функция базы открывает своё соединение и закрывает его. После изменений обязательно вызывай con.commit(), иначе они не сохранятся. В запросах используй плейсхолдер "?" и передавай значения кортежем. get_tasks() превращает строки в словари: {"id": r[0], "title": r[1], "done": bool(r[2])}.

### Подсказка 3
request.form["title"] возвращает строку из поля формы. Метод strip() убирает пробелы по краям — так пустая строка из одних пробелов не создаст задачу. Проверяй if title: перед вставкой. redirect и url_for импортируются из flask, а url_for("index") строит адрес по имени функции-обработчика.

### Подсказка 4
Конвертер <int:task_id> сам превращает сегмент URL в целое число и передаёт его в функцию. В шаблоне строй ссылки как href="/done/{{ task.id }}" и href="/delete/{{ task.id }}". Колонка done хранит 0 или 1, поэтому в условии используй {% if task.done %}, а в словаре из get_tasks() уже лежит bool.

### Подсказка 5
request.args.get("filter") без параметра в адресе вернёт None — значит, фильтр не задан. WHERE-условия строй только из захардкоженных строк ("done = 0", "done = 1"), никогда не подставляй туда ввод пользователя. Счётчик remaining посчитай через sum(1 for t in tasks if not t["done"]) и передай в шаблон.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Каркас приложения:

```python
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", tasks=[])


if __name__ == "__main__":
    app.run(debug=True)
```

Шаблон `templates/index.html`:

```html
<!doctype html>
<html>
<head><meta charset="utf-8"><title>ToDo</title></head>
<body>
  <h1>Мои задачи</h1>
  <ul></ul>
</body>
</html>
```

Виртуальное окружение создаётся командой python -m venv venv внутри папки проекта: оно изолирует установленные пакеты от системных, чтобы зависимости разных проектов не конфликтовали. После активации pip install flask ставит фреймворк только в это окружение. Flask(__name__) создаёт объект приложения, а декоратор @app.route("/") связывает корневой адрес с функцией index(). Внутри index() вызывается render_template("index.html", tasks=[]): Flask ищет шаблон в папке templates и подставляет данные. Сейчас список пуст, поэтому <ul> будет пустым. Блок if __name__ == "__main__" запускает встроенный сервер только при прямом запуске скрипта — при импорте app.py сервер не стартует.

### Разбор 2
Добавляем базу данных:

```python
import sqlite3

DB = "tasks.db"


def init_db():
    con = sqlite3.connect(DB)
    con.execute(
        "CREATE TABLE IF NOT EXISTS tasks ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "title TEXT NOT NULL,"
        "done INTEGER DEFAULT 0)"
    )
    con.commit()
    con.close()


def get_tasks():
    con = sqlite3.connect(DB)
    rows = con.execute("SELECT id, title, done FROM tasks ORDER BY id").fetchall()
    con.close()
    return [{"id": r[0], "title": r[1], "done": bool(r[2])} for r in rows]
```

SQLite хранит всю базу в одном файле tasks.db. sqlite3.connect(DB) открывает соединение; CREATE TABLE IF NOT EXISTS создаёт таблицу, только если её ещё нет. Поле id автоинкрементируется, title обязателен, а done по умолчанию 0. Так как это запись, нужен con.commit() — без него изменение не сохранится. get_tasks() читает все строки и превращает их в список словарей: bool(r[2]) переводит 0/1 в False/True для удобства в шаблоне. Для ручной вставки добавь:

```python
con = sqlite3.connect(DB)
con.execute("INSERT INTO tasks (title) VALUES (?)", ("Купить молоко",))
con.commit()
con.close()
```

А в index.html выведи задачи циклом: {% for task in tasks %} <li>{{ task.title }}</li> {% endfor %}.

### Разбор 3
Добавляем форму и маршрут добавления. В `templates/index.html`:

```html
<form method="post" action="/add">
  <input type="text" name="title" placeholder="Новая задача" required>
  <button type="submit">Добавить</button>
</form>
```

В `app.py`:

```python
from flask import request, redirect, url_for

@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"].strip()
    if title:
        con = sqlite3.connect(DB)
        con.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        con.commit()
        con.close()
    return redirect(url_for("index"))
```

Когда пользователь нажимает «Добавить», браузер отправляет POST-запрос на адрес /add. Декоратор с methods=["POST"] говорит Flask принимать на этом маршруте только POST — GET-запросы будут отклонены. request.form["title"] извлекает значение поля формы с именем title. Метод strip() убирает пробелы по краям: строка из одних пробелов станет пустой, и условие if title: не даст создать безымянную задачу. Вставка выполняется с плейсхолдером "?" — sqlite3 сам экранирует значение, что исключает SQL-инъекции. В конце redirect(url_for("index")) отправляет браузеру перенаправление на главную страницу, где обновлённый список уже покажет новую задачу.

### Разбор 4
Добавляем выполнение и удаление:

```python
@app.route("/done/<int:task_id>")
def done(task_id):
    con = sqlite3.connect(DB)
    con.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    con.commit()
    con.close()
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete(task_id):
    con = sqlite3.connect(DB)
    con.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    con.commit()
    con.close()
    return redirect(url_for("index"))
```

В шаблоне каждая задача получает ссылки:

```html
<li>
  {% if task.done %}<s>{{ task.title }}</s>{% else %}{{ task.title }}{% endif %}
  <a href="/done/{{ task.id }}">✓</a>
  <a href="/delete/{{ task.id }}">✕</a>
</li>
```

Конвертер <int:task_id> в маршруте заставляет Flask превращать сегмент URL в целое число и передавать его в функцию параметром task_id — если в адресе окажется не число, Flask вернёт ошибку 404, а не упадёт с исключением. Маршрут done выполняет UPDATE: меняет done на 1 только у строки с нужным id. Маршрут delete выполняет DELETE и убирает строку из таблицы. В шаблоне условие {% if task.done %} проверяет флаг: выполненные задачи оборачиваются в тег <s> (зачёркивание), а ссылки «✓» и «✕» ведут на соответствующие обработчики. Оба маршрута в конце делают редирект, чтобы список на главной обновился.

### Разбор 5
Полное приложение `app.py`:

```python
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB = "tasks.db"


def init_db():
    con = sqlite3.connect(DB)
    con.execute(
        "CREATE TABLE IF NOT EXISTS tasks ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "title TEXT NOT NULL,"
        "done INTEGER DEFAULT 0)"
    )
    con.commit()
    con.close()


def get_tasks(filter_by=None):
    query = "SELECT id, title, done FROM tasks"
    if filter_by == "active":
        query += " WHERE done = 0"
    elif filter_by == "done":
        query += " WHERE done = 1"
    query += " ORDER BY id"
    con = sqlite3.connect(DB)
    rows = con.execute(query).fetchall()
    con.close()
    return [{"id": r[0], "title": r[1], "done": bool(r[2])} for r in rows]


@app.route("/")
def index():
    filter_by = request.args.get("filter")
    tasks = get_tasks(filter_by)
    remaining = sum(1 for t in tasks if not t["done"])
    return render_template("index.html", tasks=tasks, remaining=remaining,
                           filter_by=filter_by)


@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"].strip()
    if title:
        con = sqlite3.connect(DB)
        con.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        con.commit()
        con.close()
    return redirect(url_for("index"))


@app.route("/done/<int:task_id>")
def done(task_id):
    con = sqlite3.connect(DB)
    con.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    con.commit()
    con.close()
    return redirect(url_for("index"))


@app.route("/undo/<int:task_id>")
def undo(task_id):
    con = sqlite3.connect(DB)
    con.execute("UPDATE tasks SET done = 0 WHERE id = ?", (task_id,))
    con.commit()
    con.close()
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete(task_id):
    con = sqlite3.connect(DB)
    con.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    con.commit()
    con.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
```

Шаблон `templates/index.html`:

```html
<!doctype html>
<html>
<head><meta charset="utf-8"><title>ToDo</title></head>
<body>
  <h1>Мои задачи</h1>
  <p>
    <a href="/?filter=">Все</a> |
    <a href="/?filter=active">Активные</a> |
    <a href="/?filter=done">Выполненные</a>
  </p>
  <p>Осталось: {{ remaining }}</p>
  <form method="post" action="/add">
    <input type="text" name="title" placeholder="Новая задача" required>
    <button type="submit">Добавить</button>
  </form>
  <ul>
    {% for task in tasks %}
      <li>
        {% if task.done %}<s>{{ task.title }}</s>{% else %}{{ task.title }}{% endif %}
        <a href="/done/{{ task.id }}">✓</a>
        <a href="/undo/{{ task.id }}">↺</a>
        <a href="/delete/{{ task.id }}">✕</a>
      </li>
    {% endfor %}
  </ul>
</body>
</html>
```

Функция get_tasks(filter_by) — единая точка чтения для всех случаев: параметр приходит из строки запроса, и от него зависит SQL-запрос. Ветки строятся только из захардкоженных строк, поэтому риска инъекций нет. В index() дополнительно считается remaining — сколько задач осталось невыполненными; он попадает в шаблон через render_template. Маршрут /undo/<int:task_id> симметричен /done/..., отличие только в значении done. В шаблоне ссылки с task.id ведут на соответствующие обработчики. Проверь: добавь несколько задач, выполни одну, переключи фильтры — списки меняются, счётчик «Осталось» уменьшается.
<!--/SOLUTION-->

<!--QUIZ-->
Зачем нужно виртуальное окружение?
- Чтобы ускорить работу компьютера
- Чтобы изолировать зависимости проекта от остальной системы
- Чтобы создать базу данных
- Чтобы компилировать код
* Правильный ответ: Чтобы изолировать зависимости проекта от остальной системы
Виртуальное окружение хранит пакеты проекта отдельно: разные проекты могут использовать разные версии библиотек без конфликтов.

Что делает декоратор @app.route("/add", methods=["POST"])?
- Создаёт новую таблицу в базе
- Связывает адрес /add с функцией и разрешает только POST-запросы
- Включает режим отладки
- Отправляет письмо пользователю
* Правильный ответ: Связывает адрес /add с функцией и разрешает только POST-запросы
Декоратор регистрирует маршрут: при обращении к /add методом POST Flask вызовет декорированную функцию.

Почему при вставке данных используют "?" вместо склеивания строк?
- Так короче писать
- Это защита от SQL-инъекций: значение экранируется
- Иначе база не сохранит данные
- Такой синтаксис нужен только для чисел
* Правильный ответ: Это защита от SQL-инъекций: значение экранируется
Плейсхолдер "?" передаёт значение отдельно от запроса, и библиотека безопасно подставляет его, не давая «склеить» вредоносный SQL.

Что возвращает request.form["title"]?
- Список всех полей формы
- Строку из поля формы с именем title
- Число полей в форме
- HTML-код формы
* Правильный ответ: Строку из поля формы с именем title
request.form собирает данные, отправленные формой методом POST, и обращение по ключу возвращает значение соответствующего поля.

Что делает redirect(url_for("index"))?
- Перезапускает сервер
- Отправляет браузеру перенаправление на главную страницу
- Печатает содержимое корзины
- Открывает панель администрирования
* Правильный ответ: Отправляет браузеру перенаправление на главную страницу
url_for("index") строит адрес по имени функции-обработчика, а redirect возвращает ответ с HTTP-кодом 302, по которому браузер переходит на этот адрес.

Что делает конвертер <int:task_id> в маршруте?
- Включает шифрование URL
- Превращает сегмент URL в целое число перед передачей в функцию
- Создаёт задачу с указанным номером
- Ограничивает число запросов
* Правильный ответ: Превращает сегмент URL в целое число перед передачей в функцию
Flask преобразует часть адреса по указанному типу и передаёт готовое значение параметром, а при нечисловом значении вернёт 404.

Какой синтаксис Jinja2 выводит значение переменной?
- {% print variable %}
- {{ переменная }}
- $переменная
- <variable>
* Правильный ответ: {{ переменная }}
Двойные фигурные скобки — это вывод значения в Jinja2, а {% ... %} используются для конструкций (циклы, условия).
<!--/QUIZ-->
