---
title: Project: blog with Django
summary: Posts, models, views, admin, templates.
order: 4
duration: 120 min
difficulty: advanced
tags: project, django, blog
---

Build a blog with Django.

## Plan

1. Project + app posts;
2. Model Post(title, content, created);
3. Views: list, detail;
4. Templates;
5. Admin.

## Model

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

## Lesson summary

Models + views + templates + admin = working blog.

<!--TASK-->
### Task 1 — App
Create app posts; register in settings.

### Task 2 — Model
Create Post with title, content, created.

### Task 3 — Migrate
Run migrations.

### Task 4 — Views
Write list and detail views.

### Task 5 — URLs
Route "" and "<int:pk>".

### Task 6 — Templates
Create list and detail templates.

### Task 7 — Admin
Register Post in admin.
<!--/TASK-->

<!--HINT-->
### Hint 1
startapp posts.

### Hint 2
Model fields.

### Hint 3
makemigrations + migrate.

### Hint 4
Post.objects.all(); get(pk=...).

### Hint 5
path.

### Hint 6
templates.

### Hint 7
admin.site.register.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```bash
python manage.py startapp posts
```
Add "posts" to INSTALLED_APPS.

### Solution 2
```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
```

### Solution 3
```bash
python manage.py makemigrations posts
python manage.py migrate
```

### Solution 4
```python
from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list(request):
    posts = Post.objects.all().order_by("-created")
    return render(request, "posts/list.html", {"posts": posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "posts/detail.html", {"post": post})
```

### Solution 5
```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("<int:pk>/", views.post_detail, name="post_detail"),
]
```

### Solution 6
```html
<!-- list.html -->
{% for post in posts %}
  <h2><a href="{% url 'post_detail' post.pk %}">{{ post.title }}</a></h2>
{% endfor %}
```
```html
<!-- detail.html -->
<h1>{{ post.title }}</h1>
<p>{{ post.content }}</p>
```

### Solution 7
```python
from django.contrib import admin
from .models import Post
admin.site.register(Post)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a blog post?
- Model with content
- A view
- A URL
- A template
* Correct answer: Model with content
Data.

What does auto_now_add do?
- Sets creation time
- Updates each save
- Deletes
- None
* Correct answer: Sets creation time
Immutable.

What does order_by do?
- Sorts queryset
- Filters
- Limits
- Creates
* Correct answer: Sorts queryset
-created.

What is get_object_or_404?
- Returns or 404
- Always 404
- List
- Create
* Correct answer: Returns or 404
Helper.

What is get?
- One object
- Many
- None
- All
* Correct answer: One object
Raise if missing.

What is render?
- Template output
- JSON
- Redirect
- Log
* Correct answer: Template output
HTML.

What is urlpatterns?
- Routes
- Models
- Settings
- Templates
* Correct answer: Routes
URLs.

What is {% url %}?
- Generates URL
- Reads
- Prints
- None
* Correct answer: Generates URL
Template tag.

What is admin?
- Management UI
- API
- Tests
- Static
* Correct answer: Management UI
/admin/.

What is INSTALLED_APPS?
- Registered apps
- URLs
- Views
- Models
* Correct answer: Registered apps
Config.

What is __str__?
- Display name
- Table
- Field
- None
* Correct answer: Display name
Admin.

What does migrate do?
- Applies migrations
- Creates app
- Views
- None
* Correct answer: Applies migrations
Schema.
<!--/QUIZ-->
