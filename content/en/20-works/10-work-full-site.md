---
title: Independent Work: A Full Website from Scratch
summary: A capstone full-cycle work: choosing a stack (Flask or Django), a DB schema, a data model, authentication, pages and Jinja2 templates, CSS flex/grid with responsiveness, JS interactivity (fetch), pytest tests, and deployment via Docker/Gunicorn.
order: 10
duration: 360 min
difficulty: advanced
tags: flask, django, fastapi, html, css, javascript, sql, docker
---

This is the course's final independent work: you will build a full website from scratch — from an empty folder to a working application in Docker. All the studied topics come together here: a web framework, databases and ORM, Jinja2 HTML templates, CSS layout, client-side JavaScript, automated tests, and deployment. The work is designed for 6 hours (it can be split into several sittings), and each stage ends with a working program — don't move on until the previous one is verified.

## Problem statement

You need to develop a **personal blog**: a user can register, log in, create posts, and edit and delete their own entries. Other users can read posts and leave comments. Comments and "likes" work through JavaScript `fetch` requests without reloading the page. All data is stored in a SQL database via ORM. The project is covered by pytest tests and packaged into a Docker container with Gunicorn.

What you will learn: choose a stack for a task and make architectural decisions, design a database schema and describe it in ORM, implement authentication and route protection, assemble an interface from templates, build responsive layouts, add JS interactivity, and take the product to deployment.

## Requirements

- **Stack:** Flask + SQLAlchemy (or Django with its own ORM). Justify the choice in `README.md`: why this framework, what its limitations are, and what you'd choose for another project.
- **Database:** SQLite for development; three tables (models): `User`, `Post`, `Comment` with correct relationships (user → posts, user → comments, post → comments).
- **Authentication:** registration, login, logout; passwords stored hashed; access to creating/editing/deleting posts — only for the author.
- **Pages and Jinja2 templates:** a base template with inheritance, a main page with a post list, a post page, login/registration forms, a post creation form, an author panel (editing/deleting).
- **CSS:** variables, a flexible flex header, a grid of post cards, media queries for mobile devices.
- **JavaScript (fetch):** posting a comment and "liking" a post without reloading the page, updating the DOM from the server response (JSON).
- **pytest tests:** at least 10 tests: pages, authentication, post CRUD, the API for comments/likes.
- **Deployment:** a Dockerfile, running via Gunicorn, `docker-compose.yml` (app + database), verifying that the container starts and the site opens.
- Only standard libraries and tools studied in the course; readable code with comments, runnable per the instructions in `README.md`.

## Work stages

Each stage is a task with its own result. After finishing a stage, run the app and verify it in the browser before moving on.

<!--TASK-->
### Task 1
Choose a stack and create the project skeleton. Study both options: Flask + SQLAlchemy and Django. Make a decision (for example, Flask — if you want to control every component; Django — if you value a ready admin panel and built-in authentication) and justify it in `README.md`. Create the project structure: folders `templates`, `static`, `app` (or `core`) with modules, a configuration file (for example, `config.py`), an entry point (`app.py` or `manage.py`), a virtual environment, and a `requirements.txt` file. Start the server and verify that a test page «Блог» opens at `http://127.0.0.1:5000/` without errors. Expected result: the project starts with one command, and an empty main page opens in the browser.

### Task 2
Design the database schema and describe the models. Draw (in text or on paper) the schema: table `User` (id, username, email, password_hash), `Post` (id, title, content, created_at, author_id → User.id), `Comment` (id, text, created_at, post_id → Post.id, author_id → User.id). Specify relationship types: one-to-many (user → posts, user → comments) and many-to-one (comment → post). Describe models via ORM: for Flask — SQLAlchemy, for Django — models in `models.py`. Create the tables in the database (migration or `create_all`) and add `debug=True` to the configuration during development. Verify table creation with the `sqlite3` command or via the Django shell.

### Task 3
Implement authentication: registration, login, logout. For Flask use the Flask-Login extension (or write session logic yourself) and password hashing (werkzeug `generate_password_hash`). For Django use the built-in `auth` system. Create registration and login pages with forms; on successful login redirect to the main page; on error show a message. Protect the post creation route: if the user is not logged in — redirect to the login page. Check: register a user, log out, log in again, try logging in with a wrong password.

### Task 4
Create pages and Jinja2 templates for post CRUD. Build a base template `base.html` with inheritance: a header with navigation (Главная, Войти/Выйти, Новый пост), `<main>` with a `content` block, a footer. Implement pages: main (a list of posts as cards), post view (text, author, date, comment block), post creation (form), editing and deleting (author only). Use `{% for %}` loops, `{% if %}` conditions, and a `datetime` or `strftime` filter for dates. Test the full cycle: create a post, edit it, delete it, and verify that other users' posts cannot be edited.

### Task 5
Style the site: CSS with flex/grid and responsiveness, then add JS interactivity. In `static/style.css`, describe variables in `:root`, a flex header, a grid of post cards with `grid-template-columns: repeat(auto-fit, minmax(260px, 1fr))`, and media queries for screens up to 768px (menu in a column, grid in one column). Then add interactivity: (1) sending a comment via `fetch` POST to `/api/comments` — the comment appears in the list without reloading; (2) a "Like" button on a post — `fetch` POST to `/api/posts/<id>/like`, the server returns the new like count, and the button changes text and state. Handle errors (the server returned 401/500 — show a message). Verify in the browser and in mobile DevTools mode.

### Task 6
Write pytest tests and wrap the project in Docker. Create `test_app.py` (or `tests/`): at least 10 tests — page statuses (main, post, login form), registration and login (success and wrong password), author post creation/editing/deletion, the ban on editing by another user, the comments API (POST, GET), the likes API. Run `pytest -v` and get all tests green. Then prepare deployment: a Dockerfile (Python image, install dependencies, run Gunicorn with 2 workers), `docker-compose.yml` (web service + database; for SQLite one service is enough, for PostgreSQL two), `.dockerignore`. Build the image, run the container, and verify the site is accessible and all functions work.

<!--/TASK-->

<!--HINT-->
### Hint 1
For Flask, the structure can be: `app.py`, `config.py`, `models.py`, `routes.py`, and the folders `templates/` and `static/`. For Django — a standard project via `django-admin startproject` and `startapp`. In `requirements.txt`, pin exact versions (freeze with `pip freeze > requirements.txt`). Check startup after every major edit.

### Hint 2
In SQLAlchemy, a one-to-many relationship is set with `db.relationship()` and `db.ForeignKey()`: in the `Post` model, `author_id = db.Column(db.Integer, db.ForeignKey("user.id"))`, and in `User` — `posts = db.relationship("Post", backref="author")`. In Django — `ForeignKey` and `related_name`. Be sure to set `ondelete="CASCADE"` (in Django — `on_delete=models.CASCADE`) so deleting a user deletes their posts.

### Hint 3
In Flask: store `user_id` in the session (`session["user_id"] = user.id`) or use Flask-Login with `login_user()` and the `@login_required` decorator. Hash passwords: `generate_password_hash(password)` on registration and `check_password_hash(hash, password)` on login — never store passwords in plain text. In Django: `django.contrib.auth` with `authenticate()` and `login()`.

### Hint 4
Make `base.html` with `{% block title %}` and `{% block content %}` blocks. For author-only access: in the edit route compare `post.author_id == current_user.id` (in Django — `request.user == post.author`), otherwise return 403 or redirect. Use `url_for` (Flask) or `{% url %}` (Django) for links — so paths won't be duplicated.

### Hint 5
For a comment fetch request: `fetch("/api/comments", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ post_id, text }) })`. For the like similarly. The server must return JSON with the result (for example, `{"likes": 12}`). Don't forget `event.preventDefault()` in the form handler and `try/catch` for errors. Check the CSS grid in DevTools by switching screen widths.

### Hint 6
For Flask tests use `TestClient` and a temporary database (for example, `tempfile` or `:memory:`). For Django — `TestCase` with `self.client`. API test: send `client.post("/api/comments", json={...})` and check the status and response body. Dockerfile: `FROM python:3.12-slim`, `WORKDIR /app`, `COPY requirements.txt .`, `RUN pip install -r requirements.txt`, `COPY . .`, `CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app:app"]`. In `docker-compose.yml`, map port 8000:8000.

<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Stack choice. For a beginner who wants control over components, Flask is simpler: you assemble models, routes, authentication, and sessions yourself and see every step. Django provides a ready admin panel, built-in auth, and ORM, but its structure is more complex and "magical". For this project, Flask + SQLAlchemy makes sense: the app is small, and you can explain every line of code. Project skeleton:

```
blog/
├── app.py
├── config.py
├── models.py
├── routes.py
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── post.html
│   ├── login.html
│   ├── register.html
│   └── new_post.html
└── static/
    └── style.css
```

`app.py` creates the app, loads configuration, and registers a blueprint of routes. Run — `python app.py`. Check that the page opens; if there is an error, read the traceback — it names the file and line.

### Solution 2
DB schema: relationships. A user has many posts; a post belongs to one user — a one-to-many relationship. Likewise user → comments. A post has many comments; a comment belongs to one post. In SQLAlchemy:

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)
    comments = db.relationship("Comment", backref="author", lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    comments = db.relationship("Comment", backref="post", lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
```

`backref` lets you write `post.author.username` or `post.comments` — objects are fetched automatically, without manual queries. Create the tables with `db.create_all()` and verify via `sqlite3 blog.db ".tables"` — three tables should appear.

### Solution 3
Authentication. On registration, we hash the password:

```python
password_hash = generate_password_hash(form.password.data)
user = User(username=form.username.data, email=form.email.data, password_hash=password_hash)
db.session.add(user)
db.session.commit()
```

On login: `check_password_hash(user.password_hash, form.password.data)`. Hashing matters because the database can fall into the wrong hands — and a hash cannot be turned back into a password. After successful login we save `session["user_id"] = user.id`. Route protection: the `login_required` decorator checks whether `user_id` is in the session; if not — redirect to `/login`. Note the check order: first check that a user with that name exists, then whether the password matches. This way we don't reveal which field was wrong.

### Solution 4
CRUD and templates. In `base.html`, define blocks and common navigation: logo «PythonПро» (or the blog's name), links `Главная`, `Новый пост`, and depending on `current_user` — `Войти` or `Выйти`. Child templates inherit `base.html` and fill only blocks. Post list:

```html
{% for post in posts %}
  <article class="card">
    <h2><a href="{{ url_for('post', post_id=post.id) }}">{{ post.title }}</a></h2>
    <p>{{ post.content[:200] }}...</p>
    <small>{{ post.author.username }} · {{ post.created_at.strftime('%d.%m.%Y') }}</small>
  </article>
{% else %}
  <p>Пока нет постов.</p>
{% endfor %}
```

Creation route: `@app.route("/new", methods=["GET", "POST"])` with `@login_required`; on POST — save the post with `author_id=current_user.id` and redirect to the post page. Editing and deleting: before the action check `if post.author_id != current_user.id: abort(403)`. This is how the "only the author can change" rule is implemented.

### Solution 5
CSS and JS. In CSS, set the grid: `.posts { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; }` — cards wrap to new rows by themselves when the window narrows. Media query: `@media (max-width: 768px) { .nav { flex-direction: column; } .posts { grid-template-columns: 1fr; } }`. JS for the like:

```javascript
async function likePost(postId, button) {
  const response = await fetch(`/api/posts/${postId}/like`, { method: "POST" });
  if (!response.ok) {
    alert("Нужно войти в систему");
    return;
  }
  const data = await response.json();
  button.textContent = `❤ ${data.likes}`;
}
```

Comment: a `submit` handler with `event.preventDefault()`, `FormData`, `fetch` POST, then `createElement("li")` and `appendChild`. Important: the backend must return JSON (for example, `jsonify`), not HTML — so JS gets clean data and builds the markup itself. No page reload happens.

### Solution 6
Tests. An example test in Flask:

```python
def test_login_success(client):
    client.post("/register", data={"username": "anya", "email": "a@test.ru", "password=[redacted]})
    r = client.post("/login", data={"username": "anya", "password=[redacted]})
    assert r.status_code == 302  # редирект на главную
    assert "Выйти".encode() in client.get("/").data
```

For API: `r = client.post("/api/comments", json={"post_id": 1, "text": "Привет"})` → check 201 and the JSON response. For tests use a separate test database (for example, `sqlite:///:memory:` via `TESTING = True` in configuration). Docker: `python:3.12-slim` image, install dependencies, copy code, CMD with Gunicorn. `docker-compose.yml`:

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
```

Build and run: `docker compose up --build`, then open `http://localhost:8000`. If the container doesn't start, look at `docker compose logs web` — the reason is there. After verification, don't forget to remove or rebuild the container: the code inside it is fixed at build time.

<!--/SOLUTION-->

<!--QUIZ-->
What is the relationship between the Post and Comment models in this project?
- One-to-many: a post has many comments
- Many-to-many
- One-to-one
* Correct answer: One-to-many: a post has many comments
A post has many comments, each comment belongs to one post: Comment has the foreign key post_id.

Why are passwords stored as hashes rather than in plain text?
- So that a database leak doesn't allow recovering passwords
- So passwords take less space
- To speed up login
* Correct answer: So that a database leak doesn't allow recovering passwords
A hash is a one-way transformation: recovering a password from it is practically impossible.

What does @login_required (Flask) or the logic with session["user_id"] do?
- Lets only authenticated users through; redirects the rest to login
- Encrypts all routes
- Creates a new user
* Correct answer: Lets only authenticated users through; redirects the rest to login
The decorator checks whether a user is in the session and protects the route from guests.

Where is the right to edit a post checked?
- In the edit route: post.author_id == current_user.id
- In the template
- In the database
* Correct answer: In the edit route: post.author_id == current_user.id
Permission checks happen in the request handler on the server, not in the template.

Which CSS code creates a responsive grid of cards?
- grid-template-columns: repeat(auto-fit, minmax(260px, 1fr))
- display: flex; flex-direction: row
- position: absolute; top: 0
* Correct answer: grid-template-columns: repeat(auto-fit, minmax(260px, 1fr))
repeat(auto-fit, minmax(...)) adapts the number of columns to the screen width itself.

What does preventDefault() do in a JS form submit handler?
- Cancels the page reload
- Sends the form to the server
- Clears the form
* Correct answer: Cancels the page reload
Without it the browser reloads the page, and the JS update of the comment list won't work.

With which method does JS send a POST request with JSON to its API?
- fetch(url, { method: "POST", headers: {...}, body: JSON.stringify(...) })
- sendJSON(url, data)
- POST(url, JSON.stringify(...))
* Correct answer: fetch(url, { method: "POST", headers: {...}, body: JSON.stringify(...) })
fetch with the method, headers, and body options is the standard way to make POST requests in a browser.

Which command does Gunicorn use to run a Flask app from a Dockerfile?
- gunicorn -w 2 -b 0.0.0.0:8000 app:app
- python app.py
- npm start
* Correct answer: gunicorn -w 2 -b 0.0.0.0:8000 app:app
Gunicorn is the production WSGI server; -w is the worker count, -b is the address and port.

What does the pytest test with client.post("/login", data={...}) and assert r.status_code == 302 check?
- That a redirect happens after successful login
- That the password is stored in plain text in the database
- That the page doesn't exist
* Correct answer: That a redirect happens after successful login
Code 302 is the redirect the server returns after successful login.

Why does docker-compose.yml need a database service?
- So data is stored separately from the app and survives container restarts
- To speed up the browser
- To reduce the image size
* Correct answer: So data is stored separately from the app and survives container restarts
A database in a separate container (or volume) doesn't lose data when the app is rebuilt.
<!--/QUIZ-->

## Assessment criteria (22 points)

| Criterion | Points |
|---|---|
| Stack choice, justification in README, project skeleton, startup | 2 |
| DB schema: three models, relationships, foreign keys, migrations | 3 |
| ORM data model and database work | 3 |
| Authentication: registration, login, logout, hashing, route protection | 3 |
| Pages and Jinja2 templates: inheritance, post list, CRUD, author rights | 3 |
| CSS styling: variables, flex, grid, responsiveness | 2 |
| JS interactivity: fetch comments and likes without reload | 2 |
| pytest tests: at least 10, all green | 2 |
| Deployment: Dockerfile, Gunicorn, docker-compose, site works in the container | 2 |

Passing grade — from 16 points.

## What to submit

- The whole project code (without the virtual environment and database) in an archive or repository.
- `README.md` with the stack justification, startup instructions, and a function list.
- Configuration files: `requirements.txt` (or `pyproject.toml`), `Dockerfile`, `docker-compose.yml`.
- All tests green: `pytest -v` output (screenshot or text log).
- Screenshots: main page, post page with comments, mobile version (DevTools), Docker container startup log.
- A comment at the top of `README.md`: what worked out, what difficulties there were, what you would add next.
- The quiz for this work on the platform (10 questions).
