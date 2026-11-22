---
title: XSS, CSRF, secure headers
summary: Script injection, forged requests, headers.
order: 3
duration: 50 min
difficulty: advanced
tags: xss, csrf
---

Browser-side attacks need browser-side defenses.

## XSS

User input rendered as HTML runs scripts.

```python
# безопасно: экранировать вывод
from django.utils.html import escape
safe = escape(user_input)
```

## CSRF

Forged forms from other sites.

Django CSRF tokens block this.

## Headers

- Content-Security-Policy;
- X-Content-Type-Options: nosniff;
- X-Frame-Options: DENY.

## Lesson summary

Escape output, tokens, and headers.

<!--TASK-->
### Task 1 — XSS
Explain the risk.

### Task 2 — Escape
Escape output.

### Task 3 — CSRF
Explain the protection.

### Task 4 — Token
Where does Django put the token?

### Task 5 — Headers
List three secure headers.

### Task 6 — CSP
Describe Content-Security-Policy.

### Task 7 — Test
Check your own app.
<!--/TASK-->

<!--HINT-->
### Hint 1
Script.

### Hint 2
escape.

### Hint 3
Form.

### Hint 4
Form.

### Hint 5
CSP.

### Hint 6
Sources.

### Hint 7
Headers.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```text
Если ввод пользователя вставляется в HTML
как есть, злоумышленник может выполнить скрипт
```

### Solution 2
```python
from django.utils.html import escape
safe = escape(user_input)
# или использовать автоэкранирование шаблонов
```

### Solution 3
```text
CSRF: чужой сайт отправляет форму от имени
пользователя. Токен в форме подтверждает,
что запрос с вашего сайта
```

### Solution 4
```text
Django кладёт csrfmiddlewaretoken в формы
и проверяет его при POST
```

### Solution 5
```text
Content-Security-Policy
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
```

### Solution 6
```text
CSP ограничивает, откуда можно грузить
скрипты/стили: script-src 'self'
```

### Solution 7
```text
curl -I https://example.com — смотреть заголовки;
проверить, что нет echo без экранирования
```
<!--/SOLUTION-->

<!--QUIZ-->
What is XSS?
- Script injection
- SQL
- CSRF
- None
* Correct answer: Script injection
Browser.

What is escaping?
- Neutralizing
- Executing
- Gluing
- None
* Correct answer: Neutralizing
Safe.

What is CSRF?
- Forged request
- Script
- SQL
- None
* Correct answer: Forged request
Token.

What is a token?
- Random check
- Password
- Cookie only
- None
* Correct answer: Random check
CSRF.

What is CSP?
- Content policy
- Certificate
- Cache
- None
* Correct answer: Content policy
Header.

What is nosniff?
- No MIME sniff
- Sniff
- Cache
- None
* Correct answer: No MIME sniff
Header.

What is DENY?
- No framing
- Allow
- Same
- None
* Correct answer: No framing
X-Frame.

What is script-src?
- Allowed scripts
- Styles
- Images
- None
* Correct answer: Allowed scripts
CSP.

What is a header?
- HTTP metadata
- Body
- URL
- None
* Correct answer: HTTP metadata
Response.

What is autoescape?
- Template default
- Off
- Optional
- None
* Correct answer: Template default
Django.

What is a cookie?
- Stored data
- Script
- SQL
- None
* Correct answer: Stored data
Session.

What is the defense?
- Escape + token + headers
- One only
- None
- Always
* Correct answer: Escape + token + headers
Layers.
<!--/QUIZ-->
