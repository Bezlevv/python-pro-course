---
title: Django: project and apps
summary: Starting a project, creating apps, views, URLs and templates.
order: 7
duration: 45 min
difficulty: intermediate
tags: django, project, app, views
---

Django is a full-featured web framework.

## Start project

```bash
django-admin startproject myproject
cd myproject
python manage.py startapp shop
```

## Settings

Add "shop" to INSTALLED_APPS.

## First view

```python
# shop/views.py
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello")
```

## URL

```python
# shop/urls.py
from django.urls import path
from . import views

urlpatterns = [path("", views.index)]
```

## Include

```python
# myproject/urls.py
from django.urls import include, path

urlpatterns = [path("shop/", include("shop.urls"))]
```

## Run

```bash
python manage.py runserver
```

## Lesson summary

Django: project → app → view → URL; run with manage.py.

<!--TASK-->
### Task 1 — Start project
Create a project and an app; list the files.

### Task 2 — Register app
Add the app to INSTALLED_APPS.

### Task 3 — View
Write a view returning "Hello".

### Task 4 — URL
Create shop/urls.py and include it.

### Task 5 — Another view
Add /info returning "About".

### Task 6 — Run
Run server and check 200 on /shop/.

### Task 7 — Template
Render a simple template via render().
<!--/TASK-->

<!--HINT-->
### Hint 1
startproject, startapp.

### Hint 2
INSTALLED_APPS.

### Hint 3
HttpResponse.

### Hint 4
include("shop.urls").

### Hint 5
Add another path.

### Hint 6
python manage.py runserver.

### Hint 7
render(request, "index.html").
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```bash
django-admin startproject myproject
cd myproject
python manage.py startapp shop
```

### Solution 2
```python
INSTALLED_APPS = [..., "shop"]
```

### Solution 3
```python
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello")
```

### Solution 4
```python
# shop/urls.py
from django.urls import path
from . import views

urlpatterns = [path("", views.index)]
```
```python
# myproject/urls.py
urlpatterns = [path("shop/", include("shop.urls"))]
```

### Solution 5
```python
def info(request):
    return HttpResponse("About")
# path("info/", views.info)
```

### Solution 6
```bash
python manage.py runserver
# GET http://127.0.0.1:8000/shop/ → 200
```

### Solution 7
```python
from django.shortcuts import render

def index(request):
    return render(request, "index.html")
```
<!--/SOLUTION-->

<!--QUIZ-->
What does startproject create?
- Project package
- App
- DB
- Server
* Correct answer: Project package
Settings.

What does startapp create?
- An app
- Project
- DB
- Docs
* Correct answer: An app
Module.

What is a view?
- A function/class handling requests
- A URL
- A model
- A template
* Correct answer: A function/class handling requests
Logic.

What does HttpResponse do?
- Returns a response
- Renders
- Redirects
- Logs
* Correct answer: Returns a response
Raw.

What is a URLconf?
- URL patterns
- Settings
- Models
- Static
* Correct answer: URL patterns
Routing.

What does include do?
- Includes other URLconfs
- Imports
- Creates
- Deletes
* Correct answer: Includes other URLconfs
Modular.

What is INSTALLED_APPS?
- Registered apps
- URLs
- Views
- Middleware
* Correct answer: Registered apps
Config.

How to run the dev server?
- python manage.py runserver
- django run
- python app.py
- server.py
* Correct answer: python manage.py runserver
Standard.

What does render do?
- Renders a template
- Returns JSON
- Redirects
- Aborts
* Correct answer: Renders a template
With context.

Where do templates go?
- shop/templates/
- root
- static
- models
* Correct answer: shop/templates/
Convention.

What is path("", views.index)?
- A route
- A view
- A model
- A template
* Correct answer: A route
URL mapping.

What does manage.py hold?
- Commands
- Data
- Templates
- Static
* Correct answer: Commands
runserver, migrate.
<!--/QUIZ-->
