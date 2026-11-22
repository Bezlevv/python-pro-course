---
title: SQL injection and protection
summary: How it works, parametrized queries.
order: 2
duration: 45 min
difficulty: advanced
tags: sql injection
---

SQL injection breaks queries via input.

## Vulnerable

```python
# НЕ ДЕЛАЙТЕ так:
cur.execute(f"SELECT * FROM users WHERE name = '{name}'")
```

If name is `' OR '1'='1` — all users leak.

## Safe: placeholders

```python
cur.execute("SELECT * FROM users WHERE name = ?", (name,))
```

## ORM

Django/ORM use parametrized queries automatically.

## Lesson summary

Always parametrize SQL.

<!--TASK-->
### Task 1 — Vulnerable
Show a vulnerable query (comment).

### Task 2 — Safe
Rewrite with a placeholder.

### Task 3 — Why
Why does injection work?

### Task 4 — ORM
Use ORM instead.

### Task 5 — Validate
Validate input types.

### Task 6 — Test
Test the injection attempt.

### Task 7 — Audit
How to check your code?
<!--/TASK-->

<!--HINT-->
### Hint 1
f-string.

### Hint 2
?.

### Hint 3
String concat.

### Hint 4
Django.

### Hint 5
int().

### Hint 6
SQLi test.

### Hint 7
Search.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
# Уязвимо:
cur.execute(f"SELECT * FROM users WHERE name = '{name}'")
# name = "' OR '1'='1" → все строки
```

### Solution 2
```python
cur.execute("SELECT * FROM users WHERE name = ?", (name,))
```

### Solution 3
```python
# Ввод склеивается с SQL как текст —
# кавычки ломают запрос
```

### Solution 4
```python
# Django:
User.objects.filter(username=name)
# запрос параметризован автоматически
```

### Solution 5
```python
user_id = int(request.GET.get("id"))
# ошибка при нечисловом значении
```

### Solution 6
```python
name = "' OR '1'='1"
rows = cur.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchall()
assert rows == []   # безопасно
```

### Solution 7
```text
Искать строки с f"SELECT ..." и конкатенацией;
заменять на параметры
```
<!--/SOLUTION-->

<!--QUIZ-->
What is SQL injection?
- Malicious input in SQL
- A bug
- A tool
- None
* Correct answer: Malicious input in SQL
Attack.

What is a placeholder?
- ? or %s
- Direct value
- f-string
- None
* Correct answer: ? or %s
Param.

What does `' OR '1'='1` do?
- Always true
- False
- Error
- None
* Correct answer: Always true
Bypass.

What is parametrization?
- Separating data
- Gluing
- Filtering
- None
* Correct answer: Separating data
Safe.

What is the f-string danger?
- Injects
- Safe
- Faster
- None
* Correct answer: Injects
Gluing.

What is an ORM?
- Auto-safe queries
- Raw SQL
- A server
- None
* Correct answer: Auto-safe queries
Django.

What is validation?
- Type checks
- SQL
- HTML
- None
* Correct answer: Type checks
int().

What is a login bypass?
- Auth skip
- Normal login
- Error
- None
* Correct answer: Auth skip
Injection.

What is escaping?
- Neutralizing text
- Gluing
- Deleting
- None
* Correct answer: Neutralizing text
Safe.

What is defense in depth?
- Several layers
- One layer
- None
- Always
* Correct answer: Several layers
Protection.

What is an audit?
- Code review
- Attack
- Test
- None
* Correct answer: Code review
Check.

What is the rule?
- Always parametrize
- Never
- Sometimes
- None
* Correct answer: Always parametrize
Golden.
<!--/QUIZ-->
