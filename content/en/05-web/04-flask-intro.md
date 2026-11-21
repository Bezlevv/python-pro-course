---
title: Flask: first app
summary: Routes, methods, rendering templates, request data.
order: 4
duration: 40 min
difficulty: intermediate
tags: flask, routes, app
---

Flask is a lightweight Python web framework.

## Minimal app

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello!"

if __name__ == "__main__":
    app.run(debug=True)
```

## Routes

```python
@app.route("/about")
def about():
    return "About"

@app.route("/user/<name>")
def user(name):
    return f"Hi, {name}"
```

## Methods

```python
@app.route("/submit", methods=["POST"])
def submit():
    return "Saved"
```

## Templates

```python
from flask import render_template

@app.route("/")
def index():
    return render_template("index.html", name="Anna")
```

## Lesson summary

Flask maps URLs to functions; templates render HTML.

<!--TASK-->
### Task 1 — Hello
Create the minimal app; run it and check "/".

### Task 2 — Route
Add "/about" returning text.

### Task 3 — Variable route
Add "/user/<name>" greeting.

### Task 4 — Converters
Add "/sum/<int:a>/<int:b>" printing the sum.

### Task 5 — POST method
Add a route accepting POST only.

### Task 6 — Redirect
Add a route that redirects to "/".

### Task 7 — Template
Create index.html and render it with a variable.
<!--/TASK-->

<!--HINT-->
### Hint 1
app = Flask(__name__); @app.route("/").

### Hint 2
@app.route("/about").

### Hint 3
@app.route("/user/<name>").

### Hint 4
<int:a> converter.

### Hint 5
methods=["POST"].

### Hint 6
redirect(url_for("index")).

### Hint 7
render_template("index.html", name=...).
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello!"

if __name__ == "__main__":
    app.run(debug=True)
```

### Solution 2
```python
@app.route("/about")
def about():
    return "About"
```

### Solution 3
```python
@app.route("/user/<name>")
def user(name):
    return f"Hi, {name}"
```

### Solution 4
```python
@app.route("/sum/<int:a>/<int:b>")
def s(a, b):
    return str(a + b)
```

### Solution 5
```python
@app.route("/submit", methods=["POST"])
def submit():
    return "Saved"
```

### Solution 6
```python
from flask import redirect, url_for

@app.route("/go")
def go():
    return redirect(url_for("index"))
```

### Solution 7
```python
from flask import render_template

@app.route("/")
def index():
    return render_template("index.html", name="Anna")
```
<!--/SOLUTION-->

<!--QUIZ-->
What creates a Flask app?
- Flask(__name__)
- Flask()
- app = App
- new Flask
* Correct answer: Flask(__name__)
Standard.

What does @app.route do?
- Maps URL to function
- Creates DB
- Renders
- Imports
* Correct answer: Maps URL to function
Decorator.

What does def index() return?
- Response text
- HTML only
- JSON
- None
* Correct answer: Response text
Any string.

How to get a path variable?
- <name> in route
- request.args
- path()
- params
* Correct answer: <name> in route
Converter.

What does <int:a> do?
- Converts to int
- Leaves string
- Errors
- Filters
* Correct answer: Converts to int
Type converter.

How to limit methods?
- methods=["POST"]
- post=True
- method="POST"
- include
* Correct answer: methods=["POST"]
Route option.

What does render_template do?
- Renders an HTML template
- Returns JSON
- Redirects
- Reads file
* Correct answer: Renders an HTML template
With context.

What does redirect do?
- Sends a redirect
- Renders
- Aborts
- Logs
* Correct answer: Sends a redirect
302.

What is url_for?
- Generates URL by endpoint
- Opens
- Parses
- None
* Correct answer: Generates URL by endpoint
By function name.

What does app.run do?
- Starts the server
- Stops
- Tests
- Compiles
* Correct answer: Starts the server
Development.

What is debug=True?
- Auto-reload + errors
- Production
- Disabled
- Printer
* Correct answer: Auto-reload + errors
Dev mode.

Where do templates live?
- templates/ folder
- static/
- root
- anywhere
* Correct answer: templates/ folder
Default.
<!--/QUIZ-->
