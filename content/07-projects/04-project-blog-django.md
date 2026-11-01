---
title: Проект: блог на Django
summary: Собираем полноценный сайт-блог: модели и миграции, админка, страницы статей, форма добавления публикации.
order: 4
duration: 120 мин
difficulty: advanced
---

Привет! Django — самый мощный веб-фреймворк Python: он уже включает админку, базу данных, систему форм и защиту. В этом проекте мы соберём на нём блог: сайт, где автор публикует статьи, а читатели их просматривают.

## О проекте

Архитектура Django называется MVT: Model (модель — данные), View (представление — логика), Template (шаблон — разметка). Наш блог будет иметь:

- модель `Post` — статья (заголовок, текст, дата);
- админку, где можно управлять статьями;
- главную страницу со списком статей;
- страницу отдельной статьи;
- форму добавления новой статьи.

## План сборки

1. Создать проект и приложение.
2. Описать модель `Post` и сделать миграции.
3. Зарегистрировать модель в админке.
4. Создать представления и маршруты.
5. Написать шаблоны.
6. Добавить форму создания статьи.
7. Запустить сервер и проверить.

## Шаг 1. Проект и приложение

```bash
pip install django
django-admin startproject blog_project
cd blog_project
python manage.py startapp posts
```

Появится папка проекта `blog_project` и приложение `posts`. Приложение — это модуль со своей моделью, представлениями и шаблонами. Добавим `posts` в `INSTALLED_APPS` в `blog_project/settings.py`:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "posts",
]
```

## Шаг 2. Модель Post

Откроем `posts/models.py` и опишем модель:

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

`CharField` — короткая строка, `TextField` — длинный текст, `DateTimeField(auto_now_add=True)` — дата создания, проставляется автоматически. Теперь создадим таблицу в базе:

```bash
python manage.py makemigrations posts
python manage.py migrate
```

`makemigrations` готовит изменения, `migrate` применяет их к базе (по умолчанию это SQLite-файл).

## Шаг 3. Админка

Зарегистрируем модель в `posts/admin.py`:

```python
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```

Создадим суперпользователя и запустим сервер:

```bash
python manage.py createsuperuser
python manage.py runserver
```

Зайди на http://127.0.0.1:8000/admin/, войди и добавь пару статей — они появятся в базе.

## Шаг 4. Представления и маршруты

Используем классово-базовые представления: `ListView` для списка и `DetailView` для одной статьи. В `posts/views.py`:

```python
from django.views.generic import ListView, DetailView
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    ordering = ["-created_at"]

class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
```

Создадим `posts/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
]
```

И подключим его в главном `blog_project/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("posts.urls")),
]
```

## Шаг 5. Шаблоны

Создай папку `posts/templates/posts/` и файлы `post_list.html` и `post_detail.html`:

```html
<!doctype html>
<html>
<head><meta charset="utf-8"><title>Мой блог</title></head>
<body>
  <h1>Мой блог</h1>
  {% for post in posts %}
    <h2><a href="{% url 'post_detail' post.pk %}">{{ post.title }}</a></h2>
    <p>{{ post.created_at|date:"d.m.Y" }}</p>
  {% empty %}
    <p>Статей пока нет.</p>
  {% endfor %}
</body>
</html>
```

Тег `{% url 'post_detail' post.pk %}` генерирует ссылку по имени маршрута — это надёжнее, чем писать URL руками.

## Шаг 6. Форма создания статьи

Создадим форму на основе модели (`posts/forms.py`):

```python
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "body"]
```

Представление-создание и маршрут:

```python
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import PostForm

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"
    success_url = reverse_lazy("post_list")
```

```python
path("new/", views.PostCreateView.as_view(), name="post_create"),
```

Шаблон `post_form.html` с формой:

```html
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Опубликовать</button>
</form>
```

`{% csrf_token %}` — обязательная защита от подделки запросов, встроенная в Django.

## Итог урока

Мы научились:

- создавать проект и приложение Django;
- описывать модели и выполнять миграции;
- пользоваться админкой;
- строить представления на классах;
- создавать формы и шаблоны.

<!--TASK-->
**Задача.** Собери блог по шагам, затем добавь категории:

1. Создай модель `Category` с полем `name` и связью «один ко многим» с `Post` (поле типа `models.ForeignKey(Category, on_delete=models.CASCADE, related_name="posts", null=True, blank=True)`).
2. Выполни миграции и зарегистрируй `Category` в админке.
3. На странице списка статей рядом с заголовком выводи название категории.
4. Добавь страницу `GET /category/<slug:category_slug>/` — список статей выбранной категории.

Ожидаемый результат: в админке можно создавать категории и привязывать статьи; клик по категории открывает страницу только со статьями этой категории.
<!--/TASK-->

<!--HINT-->
Для страницы категории используй `ListView` с переопределённым методом `get_queryset`, фильтрующим по слагу. Ссылку на категорию строй через `{% url 'posts_by_category' post.category.slug %}`. Не забудь добавить поле `slug` в модель `Category` (`SlugField`) и выполнить миграции.
<!--/HINT-->

<!--SOLUTION-->
Полное решение дополнений.

`posts/models.py`:

```python
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name="posts", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

Команды:

```bash
python manage.py makemigrations posts
python manage.py migrate
```

`posts/admin.py`:

```python
from django.contrib import admin
from .models import Post, Category

admin.site.register(Post)
admin.site.register(Category)
```

`posts/views.py`:

```python
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Post, Category
from .forms import PostForm

class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    ordering = ["-created_at"]

class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"
    success_url = reverse_lazy("post_list")

class PostsByCategoryView(ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs["category_slug"])
        return category.posts.all().order_by("-created_at")
```

`posts/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("new/", views.PostCreateView.as_view(), name="post_create"),
    path("category/<slug:category_slug>/",
         views.PostsByCategoryView.as_view(), name="posts_by_category"),
]
```

Обновлённый `templates/posts/post_list.html`:

```html
<!doctype html>
<html>
<head><meta charset="utf-8"><title>Мой блог</title></head>
<body>
  <h1>Мой блог</h1>
  <p><a href="{% url 'post_create' %}">Новая статья</a></p>
  {% for post in posts %}
    <h2><a href="{% url 'post_detail' post.pk %}">{{ post.title }}</a></h2>
    {% if post.category %}
      <p>Категория: <a href="{% url 'posts_by_category' post.category.slug %}">{{ post.category.name }}</a></p>
    {% endif %}
    <p>{{ post.created_at|date:"d.m.Y" }}</p>
    <p>{{ post.body|truncatewords:30 }}</p>
  {% empty %}
    <p>Статей пока нет.</p>
  {% endfor %}
</body>
</html>
```

Разбор:

- `Category` получила поле `slug` для красивых URL. `ForeignKey(..., related_name="posts")` позволяет из объекта категории доставать её статьи через `category.posts.all()`.
- `PostsByCategoryView` переопределяет `get_queryset`: берёт категорию по слагу из URL (`self.kwargs["category_slug"]`) и возвращает только её статьи.
- В шаблоне для каждой статьи выводится ссылка на категорию; если категории нет — блок `{% if post.category %}` пропускается.
- После изменения моделей обязательно выполни `makemigrations` и `migrate`, иначе Django будет ругаться на отсутствие таблицы.
<!--/SOLUTION-->
