---
title: Jinja2 and forms in Flask
summary: Template syntax, loops, conditionals, forms and request data.
order: 5
duration: 45 min
difficulty: intermediate
tags: jinja2, flask, forms
---

Jinja2 is Flask's template engine; forms send data to the server.

## Template syntax

```html
<h1>{{ title }}</h1>
{% for item in items %}
  <p>{{ item }}</p>
{% endfor %}
```

## Flask + Jinja

```python
from flask import render_template, request

@app.route("/")
def index():
    return render_template("index.html", items=["a", "b"])
```

## Form

```html
<form method="post" action="/submit">
  <input name="name">
  <button>Send</button>
</form>
```

## Handling POST

```python
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    return f"Hello, {name}"
```

## Lesson summary

Jinja renders dynamic HTML; request.form reads submitted fields.

<!--TASK-->
### Task 1 — Variable
Render a template with title and display it.

### Task 2 — Loop
Loop over a list and print items.

### Task 3 — Condition
Add {% if %} to show different text.

### Task 4 — Form
Create a simple form in the template.

### Task 5 — Handle GET
Read request.args.get("q") and show it.

### Task 6 — Handle POST
Read request.form["name"] and greet.

### Task 7 — Template inheritance
Create base.html with a block and extend it.
<!--/TASK-->

<!--HINT-->
### Hint 1
{{ title }}.

### Hint 2
{% for item in items %} ... {% endfor %}.

### Hint 3
{% if condition %} ... {% else %} ... {% endif %}.

### Hint 4
<form method="post">.

### Hint 5
request.args.get("q").

### Hint 6
request.form["name"].

### Hint 7
{% block content %}; {% extends "base.html" %}.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```html
<h1>{{ title }}</h1>
```
```python
return render_template("index.html", title="Home")
```

### Solution 2
```html
{% for item in items %}
  <p>{{ item }}</p>
{% endfor %}
```

### Solution 3
```html
{% if user %}
  <p>Hello, {{ user }}</p>
{% else %}
  <p>Guest</p>
{% endif %}
```

### Solution 4
```html
<form method="post" action="/submit">
  <input name="name">
  <button>Send</button>
</form>
```

### Solution 5
```python
@app.route("/search")
def search():
    q = request.args.get("q")
    return f"Query: {q}"
```

### Solution 6
```python
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    return f"Hello, {name}"
```

### Solution 7
base.html:
```html
<html><body>{% block content %}{% endblock %}</body></html>
```
child:
```html
{% extends "base.html" %}
{% block content %}<h1>Child</h1>{% endblock %}
```
<!--/SOLUTION-->

<!--QUIZ-->
What is Jinja2?
- Template engine
- HTTP server
- CSS
- DB
* Correct answer: Template engine
For Flask.

How to print a variable?
- {{ var }}
- {% var %}
- {var}
- &var;
* Correct answer: {{ var }}
Expression.

How to write a loop?
- {% for x in xs %} ... {% endfor %}
- {{ for }}
- <for>
- for()
* Correct answer: {% for x in xs %} ... {% endfor %}
Template tag.

How to write a condition?
- {% if %} ... {% endif %}
- {{ if }}
- <if>
- if()
* Correct answer: {% if %} ... {% endif %}
Branch.

What is request.form?
- POST data
- GET args
- Headers
- JSON
* Correct answer: POST data
Form fields.

What is request.args?
- Query parameters
- POST data
- Headers
- Cookies
* Correct answer: Query parameters
?q=...

How to get a form field?
- request.form["name"]
- request.args["name"]
- request.body
- request.name
* Correct answer: request.form["name"]
By name.

What does render_template do?
- Renders with context
- Reads JSON
- Redirects
- Logs
* Correct answer: Renders with context
Template + vars.

What is template inheritance?
- Base + blocks
- Copy
- Include only
- None
* Correct answer: Base + blocks
extend/block.

What does {% block %} do?
- Defines a slot
- Loops
- Prints
- Imports
* Correct answer: Defines a slot
Overridable.

What method does a form use to submit?
- post/get
- only get
- put
- delete
* Correct answer: post/get
Usually post.

Where are templates placed?
- templates/
- static/
- root
- database
* Correct answer: templates/
Standard folder.
<!--/QUIZ-->
