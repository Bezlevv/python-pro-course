---
title: Forms: client-side and server-side validation
summary: All input field types, the label/input pairing, browser-based client-side validation, and server-side validation in Python.
order: 2
duration: 45 min
difficulty: intermediate
tags: html, forms, validation, flask, pytest
---

In this lesson you will learn to create forms — from a simple input field to full validation that prevents junk data from being saved. Remember the main rule right away: **client-side validation is user convenience; server-side validation is data security**. Browser checks can be bypassed in a second, so the server must re-check everything.

## Form anatomy

A form is a `<form>`. It has two key attributes:

- `action` — where to send the data (the handler URL);
- `method` — how to send it: `get` (parameters in the URL) or `post` (data in the request body). For forms with personal data, almost always `post`.

Every field must have a `<label>` connected to the field via `for` and `id`. This is an accessibility requirement: clicking the label focuses the field, and the screen reader announces the label before the field.

```html
<form action="/register" method="post">
    <label for="name">Name</label>
    <input id="name" name="name" type="text" required>

    <label for="email">Email</label>
    <input id="email" name="email" type="email" required>

    <button type="submit">Sign up</button>
</form>
```

## Input field types

The `type` attribute doesn't just change the field's look — the browser also enables format checks and the right on-screen keyboard on phones:

| Type | What it gives |
|---|---|
| `text` | plain text |
| `email` | checks that the value looks like an email |
| `password` | masks characters |
| `number` | digits with up/down steppers |
| `tel` | telephone keypad |
| `url` | checks that it is a URL |
| `date` | date picker from a calendar |
| `search` | a search field with a clear button |
| `checkbox` | a checkbox |
| `radio` | choose one from a group |
| `range` | a slider |
| `file` | file picker |
| `color` | color picker |

For choosing from a list use `<select>` with `<option>`; for multi-line text use `<textarea>`:

```html
<label for="city">City</label>
<select id="city" name="city">
    <option value="msk">Moscow</option>
    <option value="spb">Saint Petersburg</option>
</select>

<label for="comment">Comment</label>
<textarea id="comment" name="comment" rows="4"></textarea>
```

## Client-side validation

The browser can validate data before submission. Main attributes:

- `required` — the field is mandatory;
- `minlength` / `maxlength` — string length;
- `min` / `max` — number range;
- `step` — number step;
- `pattern` — a regular expression the string must match;
- `autocomplete` — browser hints (`name`, `email`, `current-password`, and others).

```html
<label for="phone">Phone</label>
<input id="phone" name="phone" type="tel"
       placeholder="+7 XXX XXX-XX-XX"
       pattern="\+7\s[0-9]{3}\s[0-9]{3}-[0-9]{2}-[0-9]{2}"
       required>
```

The browser highlights invalid fields and blocks submission. You can style the states via the pseudo-classes `:invalid` and `:valid`, and disable the built-in check with the `novalidate` attribute — for example, if your own script validates the form.

## Server-side validation

Client-side checking is only the first line of defense. Imagine someone sent a request directly, bypassing the browser. So the server must check everything. Here is a minimal Flask handler that returns errors to the template:

```python
from flask import Flask, render_template, request

app = Flask(__name__)

def validate_registration(data):
    errors = {}
    if not data.get("name") or len(data["name"].strip()) < 2:
        errors["name"] = "The name must be at least 2 characters long."
    if not data.get("email") or "@" not in data["email"]:
        errors["email"] = "Please enter a valid email."
    return errors

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        errors = validate_registration(request.form)
        if not errors:
            return "Thank you for registering!", 200
        return render_template("register.html", errors=errors,
                               data=request.form)
    return render_template("register.html", errors={}, data={})
```

And in the template, errors are displayed next to the fields. By the way, this is exactly where Jinja2 enters the picture — you'll explore it in detail in lesson five, but you can already use the basic output:

```html
{% for field, message in errors.items() %}
    <p class="error">{{ field }}: {{ message }}</p>
{% endfor %}
```

Note: we keep the values the user entered (`data`) and put them back into the fields — so the person doesn't lose data because of one error. Never output errors or data without escaping: the template engine must be configured with `autoescape`, otherwise user text (e.g., `<script>`) will execute on your page — that's an XSS vulnerability.

## Form checklist

- Every field has a `<label>` with `for` = the field's `id`.
- `post` method for state-changing data.
- `required`, `type`, `pattern`, `minlength` — on the fields that need them.
- The server re-checks all data.
- Errors are written in plain language; values are not lost.
- No output without escaping.

Now let's put it all into practice: we'll build a registration form, add checks, and write tests for both the markup and the server logic.

<!--TASK-->
### Task 1
Create `registration.html` with a registration form. The form must contain:

- `<form>` with `action="/register"` and `method="post"`;
- a "Name" field — `type="text"`;
- an "Email" field — `type="email"`;
- a "Password" field — `type="password"`;
- a "Date of birth" field — `type="date"`;
- a `<select>` "City" with three options (e.g., Moscow, Saint Petersburg, Kazan);
- a group of radio buttons "Gender" (male/female/other) inside `<fieldset>` with `<legend>`;
- a "I agree to the terms" checkbox (as on old-school websites: consent is required);
- a `<textarea>` "Comment";
- a submit button.

Every field must have a `<label>` linked via `for`/`id`. Save and open in a browser — make sure all field types render correctly.

### Task 2
Add client-side validation to the form from task 1:

- name: `required`, `minlength="2"`, `autocomplete="name"`;
- email: `required`, `type="email"`, `autocomplete="email"`;
- password: `required`, `minlength="8"`, `autocomplete="new-password"`;
- a phone field (add a new `type="tel"` field): `pattern="\+7\s[0-9]{3}\s[0-9]{3}-[0-9]{2}-[0-9]{2}"` and `placeholder="+7 900 123-45-67"`;
- the consent checkbox: `required`;
- limit the date of birth with `max="2010-12-31"` (older than 15).

Check in the browser: try submitting an empty form, a wrong email, and a wrong phone — the browser should show hints and not submit.

### Task 3
Write a pytest test `test_form_structure.py` that checks the form markup from task 2. The test must cover:

- the form has `method="post"` and `action="/register"`;
- for every `<input>` field there is a linked `<label>` (for matches id);
- the email field has type `email` and `required`;
- the password has `minlength`;
- the consent checkbox has `required`;
- the phone field has a `pattern` attribute.

Use `BeautifulSoup`. Expected result: all checks pass, run with `python -m pytest test_form_structure.py`.

### Task 4
Write a Python function `validate_registration(data)` (the implementation may come from the theory) and a small Flask app `app.py` with a `/register` route that: renders the form on `GET`; runs validation on `POST`; returns "Thank you for registering!" if there are no errors; otherwise renders `register.html` with errors and preserved values.

Create the `register.html` template (in `templates/`) that outputs the form and an error block: `<p class="error">` for each field with an error. Test manually: run `flask --app app run`, open `http://127.0.0.1:5000/register`, submit an empty form — you'll see errors; submit valid data — you'll see the thanks message.

### Task 5
Write pytest tests for the server part from task 4. Create `test_server.py`:

- a parametrized test for `validate_registration`: an empty dict, a name shorter than 2 characters, an email without `@`, valid data — check which errors are returned;
- a render test: render `register.html` via jinja2 with errors `{"email": "Please enter a valid email."}` and check with `BeautifulSoup` that the HTML contains `<p class="error">` with that text;
- a safe-output test: pass a field value with an HTML tag (e.g., `<script>alert(1)</script>`) into the template and check that the rendered text contains no live `<script>` tag (i.e., it is escaped).

Expected result: all tests pass.
<!--/TASK-->

<!--HINT-->
### Hint 1
Each field starts with `<label for="unique-id">`, and `<input>` must have the same `id`. For the radio group, wrap the buttons in `<fieldset><legend>Gender</legend>...</fieldset>`. Use one name `name="gender"` for all radio buttons — that's how the browser knows they are one group.

### Hint 2
Don't forget that `pattern` takes a **regular expression**, and spaces in it matter. In an HTML attribute, the backslash is written as-is: `pattern="\+7\s[0-9]{3}\s..."`. For the date limit use `max` in YYYY-MM-DD format.

### Hint 3
Loop over all inputs: `for field in soup.find_all("input"):`. For each, find the `label` via `soup.find("label", attrs={"for": field.get("id")})`. Special case: the `type="checkbox"` field with `name="agree"`. Use `field.get("required") is not None` and `field.get("minlength")`.

### Hint 4
The validation function returns an error dict: key — field name, value — error text. Note that `request.form` is a "field name → value" dict. In the template, iterate over errors with `{% for field, message in errors.items() %}`. Return the render as `render_template("register.html", errors=errors, data=request.form)`.

### Hint 5
For rendering without running a server, use jinja2 directly: `from jinja2 import Environment, FileSystemLoader; env = Environment(loader=FileSystemLoader("templates"), autoescape=True)`. Escaping check: `assert "<script>" not in html` — keeping in mind that jinja2 with autoescape will output `&lt;script&gt;`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Example form:

```html
<form action="/register" method="post">
    <label for="name">Name</label>
    <input id="name" name="name" type="text">

    <label for="email">Email</label>
    <input id="email" name="email" type="email">

    <label for="password">Password</label>
    <input id="password" name="password" type="password">

    <label for="birth">Date of birth</label>
    <input id="birth" name="birth" type="date">

    <label for="city">City</label>
    <select id="city" name="city">
        <option value="msk">Moscow</option>
        <option value="spb">Saint Petersburg</option>
        <option value="kzn">Kazan</option>
    </select>

    <fieldset>
        <legend>Gender</legend>
        <label><input type="radio" name="gender" value="male"> Male</label>
        <label><input type="radio" name="gender" value="female"> Female</label>
        <label><input type="radio" name="gender" value="other"> Other</label>
    </fieldset>

    <label><input type="checkbox" name="agree"> I agree to the terms</label>

    <label for="comment">Comment</label>
    <textarea id="comment" name="comment" rows="4"></textarea>

    <button type="submit">Submit</button>
</form>
```

What is happening here? Labels are linked to fields via `for`/`id` — that's why clicking the label text puts the cursor into the field. Radio buttons share one name `name="gender"`, so the browser treats them as a single group: only one can be selected. `<fieldset>` and `<legend>` group them visually and semantically. Submission goes via `post` to `/register` — the right choice for registration data.

### Solution 2
Adding validation attributes:

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

What is happening here? `required` blocks submission of an empty field; `minlength` checks string length; `type="email"` enables the format check; `pattern` requires the phone to match the regular expression `\+7\s[0-9]{3}\s[0-9]{3}-[0-9]{2}-[0-9]{2}` — that's the `+7 900 123-45-67` format; `max="2010-12-31"` forbids picking a birth date "younger" than 15; `autocomplete` turns on browser hints.

### Solution 3
`test_form_structure.py`:

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
            continue  # radio buttons are wrapped in labels
        label = soup.find("label", attrs={"for": field.get("id")})
        assert label is not None, f"No label for field {field.get('name')}"


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

What is happening here? We load the HTML into BeautifulSoup and check attributes. We deliberately skip radio buttons — they are wrapped in `<label>` entirely and don't need a separate label. All other fields must have one: if no `label` with a matching `for` is found, `assert` fails with a clear message naming the problematic field.

### Solution 4
`app.py`:

```python
from flask import Flask, render_template, request

app = Flask(__name__)


def validate_registration(data):
    errors = {}
    name = data.get("name", "").strip()
    if len(name) < 2:
        errors["name"] = "The name must be at least 2 characters long."
    email = data.get("email", "").strip()
    if "@" not in email or "." not in email:
        errors["email"] = "Please enter a valid email."
    if len(data.get("password", "")) < 8:
        errors["password"] = "The password must be at least 8 characters long."
    return errors


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        errors = validate_registration(request.form)
        if not errors:
            return "Thank you for registering!", 200
        return render_template("register.html", errors=errors,
                               data=request.form)
    return render_template("register.html", errors={}, data={})
```

`templates/register.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Registration</title></head>
<body>
    <h1>Registration</h1>
    {% for field, message in errors.items() %}
        <p class="error">{{ field }}: {{ message }}</p>
    {% endfor %}
    <form action="/register" method="post">
        <label for="name">Name</label>
        <input id="name" name="name" type="text"
               value="{{ data.get('name', '') }}">
        <label for="email">Email</label>
        <input id="email" name="email" type="email"
               value="{{ data.get('email', '') }}">
        <label for="password">Password</label>
        <input id="password" name="password" type="password">
        <button type="submit">Submit</button>
    </form>
</body>
</html>
```

What is happening here? `validate_registration` returns an error dict: key — field name, value — text. In the handler, `GET` renders an empty form, `POST` validates and either returns the thanks message or renders the template with errors. Cycles print errors in the template, and `data` values are put back into the fields' `value` — the user doesn't lose data.

### Solution 5
`test_server.py`:

```python
import pytest
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

from app import validate_registration


@pytest.mark.parametrize("data, expected", [
    ({}, {"name", "email", "password"}),
    ({"name": "A", "email": "a@b.ru", "password": "12345678"},
     {"name"}),
    ({"name": "Anna", "email": "not-email", "password": "12345678"},
     {"email"}),
    ({"name": "Anna", "email": "a@b.ru", "password": "12345678"},
     set()),
])
def test_validate_registration(data, expected):
    assert set(validate_registration(data)) == expected


def test_register_template_renders_errors():
    env = Environment(loader=FileSystemLoader("templates"),
                      autoescape=True)
    template = env.get_template("register.html")
    html = template.render(errors={"email": "Please enter a valid email."},
                           data={})
    soup = BeautifulSoup(html, "html.parser")
    error = soup.find("p", class_="error")
    assert error is not None
    assert "Please enter a valid email." in error.get_text()


def test_template_escapes_user_input():
    env = Environment(loader=FileSystemLoader("templates"),
                      autoescape=True)
    template = env.get_template("register.html")
    html = template.render(errors={}, data={"name": "<script>alert(1)</script>"})
    assert "<script>" not in html
    assert "&lt;script&gt;" in html
```

What is happening here? The parametrized test covers four scenarios: completely empty data (errors on all three fields), too-short name, invalid email, and valid data (no errors). The render test creates a jinja2 environment with `autoescape=True` and checks that the error lands in `<p class="error">`. The last test proves safety: a value with an HTML tag is escaped into `&lt;script&gt;`, and no live tag appears in the output.
<!--/SOLUTION-->

<!--QUIZ-->
Which HTTP method is usually used to submit a registration form?
- get
- post
- put
* Correct answer: post
Form data that changes state is sent with the post method.

How is an input field connected to its label?
- Through the for and id attributes
- They just need to sit next to each other
- Through the name attribute
* Correct answer: Through the for and id attributes
The for on label must match the field's id — that's how the connection is made.

Which field type enables email address format checking?
- text
- email
- password
* Correct answer: email
type="email" makes the browser check that the value looks like an email.

What does the pattern attribute do?
- Specifies a password template
- Sets a regular expression to validate the value
- Turns on browser hints
* Correct answer: Sets a regular expression to validate the value
pattern checks the string against a regular expression.

Why is server-side validation needed if client-side exists?
- To speed up the browser
- Because client-side checks can be bypassed — the server must re-check
- It isn't needed
* Correct answer: Because client-side checks can be bypassed — the server must re-check
Browser checks are easy to bypass, so server-side validation is essential.

Which attribute prevents submitting an empty field?
- placeholder
- required
- readonly
* Correct answer: required
required makes the field mandatory.

What is an XSS vulnerability?
- A vulnerability caused by inserting user text into HTML without escaping
- An error in CSS styles
- Slow page loading
* Correct answer: A vulnerability caused by inserting user text into HTML without escaping
If input isn't escaped, a user can inject a foreign script.

Which tag groups radio buttons with a heading?
- div
- fieldset + legend
- group
* Correct answer: fieldset + legend
fieldset groups fields, and legend gives them a heading.

What does type="date" do?
- Shows a calendar to pick a date
- Turns the field into text
- Changes nothing
* Correct answer: Shows a calendar to pick a date
A date field opens a calendar and returns a value in YYYY-MM-DD format.

What does autocomplete="email" do?
- Fills the field with the previously entered email
- Checks the email format
- Hides the field
* Correct answer: Fills the field with the previously entered email
autocomplete turns on browser hints and autofill.
<!--/QUIZ-->
