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
        con.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
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
**Задача.** Собери приложение целиком по шагам выше, затем добавь фильтр по статусу. Реализуй так:

1. На главной странице добавь три ссылки: «Все», «Активные», «Выполненные».
2. Эти ссылки должны вести на адреса вида `/?filter=active` и `/?filter=done`.
3. В функции `index()` читай параметр через `request.args.get("filter")` и передавай в запрос к базе соответствующий `WHERE`.
4. Рядом с выполненными задачами добавь ссылку «↺», которая делает задачу снова активной (меняет `done` обратно на 0).

Ожидаемый результат: переход по ссылке «Активные» показывает только невыполненные задачи, «Выполненные» — только выполненные, а «Все» — весь список. Счётчик задач на странице обновляется (например, «Осталось: N»).
<!--/TASK-->

<!--HINT-->
Параметры строки запроса читаются через `request.args.get("filter")`. Для разных фильтров строй разные SQL-запросы, например `WHERE done = 0` и `WHERE done = 1`. Ссылку «↺» сделай по аналогии с `/done/<int:task_id>`, только с `UPDATE tasks SET done = 0`.
<!--/HINT-->

<!--SOLUTION-->
Полное решение (файл `app.py`):

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

Разбор решения:

- `get_tasks(filter_by)` — одна функция для всех трёх случаев. Параметр `filter_by` приходит из строки запроса, и от него зависит SQL-запрос. Ветки строятся только из захардкоженных строк, поэтому никакого риска инъекций нет.
- В `index()` мы дополнительно считаем `remaining` — сколько задач осталось невыполненными. Он попадает в шаблон через `render_template`.
- Маршрут `/undo/<int:task_id>` симметричен `/done/...`, отличие только в значении поля `done`.
- В шаблоне ссылки по `task.id` ведут на соответствующие обработчики.

Проверь: добавь несколько задач, выполни одну, переключи фильтры — списки меняются, счётчик «Осталось» уменьшается.
<!--/SOLUTION-->
