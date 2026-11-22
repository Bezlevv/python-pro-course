---
title: Flask: Blueprints and app structure
summary: Modular apps with Blueprints and application factories.
order: 21
duration: 50 min
difficulty: advanced
tags: flask, blueprints, structure
---

Blueprints organize a growing Flask app into modules.

## Blueprint

```python
from flask import Blueprint

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login")
def login():
    return "Login"
```

## Register

```python
app.register_blueprint(auth_bp)
```

URL becomes /auth/login.

## Factory

```python
def create_app():
    app = Flask(__name__)
    from .blueprints.auth import auth_bp
    app.register_blueprint(auth_bp)
    return app
```

## Structure

```
app/
  __init__.py      # create_app
  blueprints/
    auth.py
    shop.py
  templates/
  static/
```

## Lesson summary

Blueprints + factory make large Flask apps maintainable.

<!--TASK-->
### Task 1 — Blueprint
Create auth_bp with url_prefix="/auth".

### Task 2 — Register
Register it and test /auth/login.

### Task 3 — url_for
Use url_for("auth.login") in a redirect.

### Task 4 — Factory
Write create_app with config and registration.

### Task 5 — Error handler
Add an errorhandler to a blueprint.

### Task 6 — Static
Serve static via url_for('static', ...).

### Task 7 — Structure
Create the recommended folder structure.
<!--/TASK-->

<!--HINT-->
### Hint 1
Blueprint("auth", __name__, url_prefix="/auth").

### Hint 2
app.register_blueprint(auth_bp).

### Hint 3
url_for("auth.login").

### Hint 4
def create_app(): ...

### Hint 5
@auth_bp.errorhandler(404).

### Hint 6
url_for('static', filename='style.css').

### Hint 7
app/blueprints/...
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from flask import Blueprint

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login")
def login():
    return "Login"
```

### Solution 2
```python
app.register_blueprint(auth_bp)
# GET /auth/login → 200
```

### Solution 3
```python
from flask import redirect, url_for

@app.route("/go")
def go():
    return redirect(url_for("auth.login"))
```

### Solution 4
```python
def create_app(config=None):
    app = Flask(__name__)
    if config:
        app.config.update(config)
    from .blueprints.auth import auth_bp
    app.register_blueprint(auth_bp)
    return app
```

### Solution 5
```python
@auth_bp.errorhandler(404)
def not_found(e):
    return "Not found", 404
```

### Solution 6
```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
```

### Solution 7
```
app/
  __init__.py
  blueprints/
    auth.py
    shop.py
  templates/
  static/
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a Blueprint?
- A modular app section
- A model
- A template
- A plugin
* Correct answer: A modular app section
Routes.

What is url_prefix?
- Path prefix
- URL name
- Host
- Method
* Correct answer: Path prefix
/auth.

How to register?
- app.register_blueprint(bp)
- app.add(bp)
- bp.register(app)
- attach
* Correct answer: app.register_blueprint(bp)
Method.

What is url_for("auth.login")?
- Builds URL
- Opens
- Logs
- Renders
* Correct answer: Builds URL
By endpoint.

What is a factory?
- create_app() function
- A model
- A URL
- A test
* Correct answer: create_app() function
App builder.

Why factories?
- Testability/config
- Speed
- Memory
- None
* Correct answer: Testability/config
Multiple instances.

What does errorhandler do?
- Handles errors
- Routes
- Logs
- Renders
* Correct answer: Handles errors
In blueprint.

Where is static served from?
- app/static/
- templates
- blueprints
- root
* Correct answer: app/static/
folder.

What is the blueprint name?
- First argument
- url_prefix
- __name__
- path
* Correct answer: First argument
"auth".

Can multiple blueprints coexist?
- Yes
- No
- One only
- Two
* Correct answer: Yes
Modular.

What does include_router resemble in FastAPI?
- Blueprint registration
- Models
- Tests
- Static
* Correct answer: Blueprint registration
Similar.

What breaks URL building?
- Using hardcoded paths
- url_for
- Blueprints
- Factory
* Correct answer: Using hardcoded paths
Use url_for.
<!--/QUIZ-->
