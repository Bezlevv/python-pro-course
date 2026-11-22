---
title: Project: ToDo manager with Flask
summary: CRUD app with SQLite, routes and templates.
order: 2
duration: 90 min
difficulty: intermediate
tags: project, flask, sqlite, todo
---

Build a working task manager.

## Plan

1. Flask app;
2. SQLite storage;
3. Routes: list, add, done, delete;
4. Templates with loops and forms.

## Skeleton

```python
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB = "tasks.db"

def get_tasks():
    con = sqlite3.connect(DB)
    rows = con.execute("SELECT id, title, done FROM tasks").fetchall()
    con.close()
    return [{"id": r[0], "title": r[1], "done": bool(r[2])} for r in rows]
```

## Lesson summary

Full CRUD: database + routes + templates.

<!--TASK-->
### Task 1 — Init DB
Create the tasks table.

### Task 2 — List
Route "/" shows tasks.

### Task 3 — Add
POST /add inserts a task.

### Task 4 — Done
Route /done/<id> toggles.

### Task 5 — Delete
Route /delete/<id> removes.

### Task 6 — Template
Render with a loop and form.

### Task 7 — Test
Add and list tasks via test client.
<!--/TASK-->

<!--HINT-->
### Hint 1
CREATE TABLE IF NOT EXISTS.

### Hint 2
index.html with list.

### Hint 3
request.form["title"].

### Hint 4
UPDATE tasks SET done=1.

### Hint 5
DELETE FROM tasks.

### Hint 6
{% for %} and form.

### Hint 7
client.get/post.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
def init_db():
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        done INTEGER DEFAULT 0
    )""")
    con.commit()
    con.close()
```

### Solution 2
```python
@app.route("/")
def index():
    return render_template("index.html", tasks=get_tasks())
```

### Solution 3
```python
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

### Solution 4
```python
@app.route("/done/<int:task_id>")
def done(task_id):
    con = sqlite3.connect(DB)
    con.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    con.commit(); con.close()
    return redirect(url_for("index"))
```

### Solution 5
```python
@app.route("/delete/<int:task_id>")
def delete(task_id):
    con = sqlite3.connect(DB)
    con.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    con.commit(); con.close()
    return redirect(url_for("index"))
```

### Solution 6
```html
<form method="post" action="/add">
  <input name="title" placeholder="New task" required>
  <button>Add</button>
</form>
{% for task in tasks %}
  <li>{{ task.title }} <a href="/done/{{ task.id }}">✓</a>
  <a href="/delete/{{ task.id }}">✕</a></li>
{% endfor %}
```

### Solution 7
```python
client = app.test_client()
r = client.post("/add", data={"title": "Buy milk"})
assert r.status_code == 302
```
<!--/SOLUTION-->

<!--QUIZ-->
What is CRUD?
- Create Read Update Delete
- Copy
- Code
- None
* Correct answer: Create Read Update Delete
Operations.

What stores the app?
- SQLite
- Files
- Memory only
- JSON
* Correct answer: SQLite
Permanent.

What method adds?
- POST
- GET
- PUT
- DELETE
* Correct answer: POST
Create.

What does redirect do?
- Sends back to list
- Renders
- Errors
- None
* Correct answer: Sends back to list
After action.

What is a placeholder?
- ? in SQL
- %
- #
- Value
* Correct answer: ? in SQL
Parameter.

What does int: mean in a route?
- Converts to int
- String
- Float
- None
* Correct answer: Converts to int
Converter.

What is task_done?
- Boolean flag
- Title
- Id
- Text
* Correct answer: Boolean flag
Done state.

What is a template loop?
- {% for task in tasks %}
- {{ task }}
- <li>
- form
* Correct answer: {% for task in tasks %}
Renders list.

What is request.form?
- POST fields
- Query
- Headers
- JSON
* Correct answer: POST fields
Form.

Why commit?
- Persist changes
- Read
- Close
- None
* Correct answer: Persist changes
Save.

What is index?
- Main route
- DB
- Model
- Test
* Correct answer: Main route
"/".

What does .strip() do?
- Removes spaces
- Lowercases
- Splits
- None
* Correct answer: Removes spaces
Clean title.
<!--/QUIZ-->
