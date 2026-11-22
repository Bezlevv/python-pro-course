---
title: Microservices vs monolith
summary: Trade-offs, service boundaries, data.
order: 4
duration: 45 min
difficulty: advanced
tags: architecture, microservices
---

Choose the right deployment architecture.

## Monolith

One app serving everything.

- Simpler, easier to test and deploy;
- Scales as a whole.

## Microservices

Many small services.

- Independent scale and teams;
- Distributed complexity, network failures.

## When

Start monolith; split when pain is real.

## Lesson summary

Monolith first; microservices when justified.

<!--TASK-->
### Task 1 — Monolith
List two benefits.

### Task 2 — Micro
List two benefits.

### Task 3 — Pain
When to split?

### Task 4 — Boundaries
How to find service boundaries?

### Task 5 — Data
Per-service database idea.

### Task 6 — Failure
Network failure handling.

### Task 7 — Choose
Which for a startup MVP?
<!--/TASK-->

<!--HINT-->
### Hint 1
Simple.

### Hint 2
Scale.

### Hint 3
Pain.

### Hint 4
Domains.

### Hint 5
Own db.

### Hint 6
Retry.

### Hint 7
Monolith.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
# Проще разрабатывать и тестировать
# Один деплой, одна кодовая база
```

### Solution 2
```python
# Независимое масштабирование сервисов
# Отдельные команды и релизы
```

### Solution 3
```python
# Когда монолит мешает: скорость релизов,
# размер команды, узкие места масштабирования
```

### Solution 4
```python
# Границы по бизнес-доменам:
# пользователи, заказы, платежи
```

### Solution 5
```python
# У каждого сервиса своя БД —
# слабая связность, нет общих таблиц
```

### Solution 6
```python
# Ретраи, таймауты, circuit breaker,
# очередь задач при недоступности
```

### Solution 7
```python
# Для MVP — монолит: быстрее и дешевле;
# микро-разбиение начнёт, когда появится боль
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a monolith?
- One app
- Many small
- A DB
- None
* Correct answer: One app
All in one.

What is microservices?
- Many small apps
- One app
- A library
- None
* Correct answer: Many small apps
Independent.

What is a benefit of monolith?
- Simplicity
- Isolation
- Scale
- None
* Correct answer: Simplicity
Easy start.

What is a benefit of micro?
- Independent scale
- Simplicity
- One codebase
- None
* Correct answer: Independent scale
Teams.

What is a boundary?
- Domain edge
- A file
- A test
- None
* Correct answer: Domain edge
Orders.

What is per-service DB?
- Own database
- Shared
- One
- None
* Correct answer: Own database
Decoupling.

What is a timeout?
- Failure limit
- Success
- Retry
- None
* Correct answer: Failure limit
Wait.

What is a retry?
- Repeats request
- Stops
- Caches
- None
* Correct answer: Repeats request
Resilience.

What is a circuit breaker?
- Stops cascading
- Opens always
- A wire
- None
* Correct answer: Stops cascading
Fail fast.

What is MVP?
- Minimum viable product
- Most valuable
- Micro
- None
* Correct answer: Minimum viable product
Start.

Which for MVP?
- Monolith
- Microservices
- Both
- None
* Correct answer: Monolith
Speed.

What is distributed complexity?
- Network issues
- Simpler
- Local
- None
* Correct answer: Network issues
Trade-off.
<!--/QUIZ-->
