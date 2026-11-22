---
title: Layers: MVC, MVT, service layer
summary: Separation of concerns, structure.
order: 1
duration: 45 min
difficulty: intermediate
tags: architecture, mvc, mvt
---

Divide an app into layers with clear roles.

## MVC

- Model: data;
- View: display;
- Controller: input logic.

## MVT (Django)

- Model: data;
- View: logic/business;
- Template: display.

## Service layer

Business logic in services, not views/models.

## Lesson summary

Layers keep apps maintainable.

<!--TASK-->
### Task 1 — MVC
Label three MVC components.

### Task 2 — MVT
Label Django MVT.

### Task 3 — Service
Move logic into a service function.

### Task 4 — Why
Explain separation of concerns.

### Task 5 — Fat model
Problem with heavy models.

### Task 6 — Structure
Propose a project folder layout.

### Task 7 — Interface
Describe responsibilities to a beginner.
<!--/TASK-->

<!--HINT-->
### Hint 1
Model, View, Controller.

### Hint 2
Model, View, Template.

### Hint 3
services.py.

### Hint 4
Single responsibility.

### Hint 5
Hard to test.

### Hint 6
apps/services.

### Hint 7
Short.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
# MVC
# Model — данные (БД)
# View — отображение
# Controller — обработка ввода
```

### Solution 2
```python
# MVT (Django)
# Model — данные
# View — логика
# Template — отображение
```

### Solution 3
```python
# services.py
def create_order(user, items):
    total = sum(i.price for i in items)
    order = Order.objects.create(user=user, total=total)
    order.items.add(*items)
    return order
```

### Solution 4
```python
# Каждый слой отвечает за своё:
# данные, логика, представление — не смешиваются
```

### Solution 5
```python
# Толстые модели трудно тестировать
# и переиспользовать — логика разрастается
```

### Solution 6
```python
# app/
#   models.py
#   views.py
#   services.py
#   repositories.py
#   templates/
```

### Solution 7
```python
# View: принял запрос → вызвал сервис → отдал шаблон
# Service: делает бизнес-работу
# Model: хранит данные
```
<!--/SOLUTION-->

<!--QUIZ-->
What is MVC?
- Model-View-Controller
- My Very Code
- A framework
- None
* Correct answer: Model-View-Controller
Pattern.

What is Model?
- Data
- Display
- Input
- None
* Correct answer: Data
DB.

What is View?
- Display/logic
- Data
- Input
- None
* Correct answer: Display/logic
MVT.

What is Controller?
- Input logic
- Data
- Display
- None
* Correct answer: Input logic
MVC.

What is Template?
- Display
- Data
- Logic
- None
* Correct answer: Display
Django.

What is separation of concerns?
- Clear roles
- Mixing
- Speed
- None
* Correct answer: Clear roles
Maintainability.

What is a service layer?
- Business logic
- Data only
- Display
- None
* Correct answer: Business logic
Service.

Why layers?
- Easier to maintain
- Faster
- Required
- None
* Correct answer: Easier to maintain
Test.

What is a fat model?
- Too much logic
- Rich data
- Fast
- None
* Correct answer: Too much logic
Anti-pattern.

What is single responsibility?
- One job
- Many jobs
- None
- Fast
* Correct answer: One job
Principle.

What is an architecture?
- Overall structure
- A file
- A test
- None
* Correct answer: Overall structure
Design.

What is the dependency direction?
- High → low layers
- Low → high
- Random
- None
* Correct answer: High → low layers
Clean.
<!--/QUIZ-->
