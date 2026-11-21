---
title: Django: models, ORM, admin, forms
summary: Defining models, migrations, querysets, admin registration and forms.
order: 8
duration: 60 min
difficulty: intermediate
tags: django, models, orm, forms
---

Django models describe tables; the ORM queries them in Python.

## Model

```python
# shop/models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
```

## Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## ORM

```python
Product.objects.all()
Product.objects.filter(price__lt=100)
Product.objects.create(name="Pen", price=10)
product.price
```

## Admin

```python
# shop/admin.py
from django.contrib import admin
from .models import Product

admin.site.register(Product)
```

## Forms

```python
from django import forms

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price"]
```

## Lesson summary

Models + migrations + ORM + admin + forms cover CRUD basics.

<!--TASK-->
### Task 1 — Model
Create a Product model with name and price.

### Task 2 — Migrate
Run makemigrations and migrate.

### Task 3 — ORM create
Create a product with objects.create.

### Task 4 — Filter
Query products cheaper than 100.

### Task 5 — Update
Change a product price and save.

### Task 6 — Delete
Delete a product and count remaining.

### Task 7 — Admin
Register the model in admin and mention the admin URL.
<!--/TASK-->

<!--HINT-->
### Hint 1
models.CharField/DecimalField.

### Hint 2
makemigrations; migrate.

### Hint 3
Product.objects.create(...).

### Hint 4
filter(price__lt=100).

### Hint 5
obj.price = ...; obj.save().

### Hint 6
obj.delete(); .count().

### Hint 7
admin.site.register(Product).
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
```

### Solution 2
```bash
python manage.py makemigrations
python manage.py migrate
```

### Solution 3
```python
Product.objects.create(name="Pen", price=10)
```

### Solution 4
```python
Product.objects.filter(price__lt=100)
```

### Solution 5
```python
p = Product.objects.get(name="Pen")
p.price = 12
p.save()
```

### Solution 6
```python
p.delete()
Product.objects.count()
```

### Solution 7
```python
from django.contrib import admin
from .models import Product
admin.site.register(Product)
# http://127.0.0.1:8000/admin/
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a model?
- A table definition
- A view
- A URL
- A form
* Correct answer: A table definition
Class.

What does CharField do?
- String field
- Integer
- Date
- Bool
* Correct answer: String field
Type.

What is a migration?
- Schema changes
- Data rows
- Logs
- Tests
* Correct answer: Schema changes
Versioned.

What does makemigrations do?
- Creates migrations
- Applies
- Deletes
- Shows
* Correct answer: Creates migrations
From models.

What does migrate do?
- Applies migrations
- Creates
- Deletes
- Tests
* Correct answer: Applies migrations
To DB.

What is Product.objects.all()?
- All rows
- One row
- None
- Table
* Correct answer: All rows
Queryset.

What does filter do?
- Selects matching rows
- Sorts
- Creates
- Deletes
* Correct answer: Selects matching rows
Conditions.

What does price__lt=100 mean?
- Less than 100
- Greater
- Equal
- Like
* Correct answer: Less than 100
Lookup.

What does objects.create do?
- Creates and saves a row
- Reads
- Deletes
- Updates
* Correct answer: Creates and saves a row
One step.

How to update?
- obj.save() after change
- objects.update only
- refresh
- delete
* Correct answer: obj.save() after change
Persist.

How to delete?
- obj.delete()
- remove()
- drop()
- del
* Correct answer: obj.delete()
Remove.

What is admin for?
- Web CRUD UI
- API
- Logs
- Tests
* Correct answer: Web CRUD UI
/admin/.
<!--/QUIZ-->
