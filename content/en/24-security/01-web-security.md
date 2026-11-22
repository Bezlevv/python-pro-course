---
title: Security basics for web apps
summary: Threats, HTTPS, headers.
order: 1
duration: 40 min
difficulty: intermediate
tags: security
---

Web apps face common attacks.

## Threats

- SQL injection;
- XSS;
- CSRF;
- Broken auth.

## Basics

- Always HTTPS;
- Hash passwords;
- Don't trust user input;
- Least privilege.

## Lesson summary

Know the attacks; apply defenses.

<!--TASK-->
### Task 1 — Threats
Name three attack types.

### Task 2 — HTTPS
Why HTTPS?

### Task 3 — Input
Why not trust input?

### Task 4 — Passwords
How to store passwords?

### Task 5 — Secrets
Where not to put secrets?

### Task 6 — Admin
Least privilege example.

### Task 7 — Updates
Why update dependencies?
<!--/TASK-->

<!--HINT-->
### Hint 1
SQLi.

### Hint 2
Encryption.

### Hint 3
Validate.

### Hint 4
Hash.

### Hint 5
Code.

### Hint 6
Roles.

### Hint 7
Patches.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```text
SQL-инъекция, XSS, CSRF, подбор паролей
```

### Solution 2
```text
HTTPS шифрует трафик — нельзя прочитать
пароли и данные в пути
```

### Solution 3
```text
Пользовательский ввод может быть вредоносным:
проверять и экранировать
```

### Solution 4
```text
Только хеш с солью (например, pbkdf2/argon2),
никогда — открытый текст
```

### Solution 5
```text
Не в коде, не в git, не в логи;
в переменных окружения/секрет-хранилище
```

### Solution 6
```text
Обычный пользователь не имеет прав админа;
роли выдают минимум нужного
```

### Solution 7
```text
Обновления закрывают известные уязвимости
зависимостей
```
<!--/SOLUTION-->

<!--QUIZ-->
What is SQL injection?
- Malicious SQL input
- A bug
- A tool
- None
* Correct answer: Malicious SQL input
Attack.

What is XSS?
- Script injection
- SQL
- CSRF
- None
* Correct answer: Script injection
Browser.

What is CSRF?
- Forged requests
- SQL
- XSS
- None
* Correct answer: Forged requests
Tokens.

What is HTTPS?
- Encrypted HTTP
- Plain
- Faster
- None
* Correct answer: Encrypted HTTP
TLS.

What is hashing?
- One-way transform
- Encryption
- Reversible
- None
* Correct answer: One-way transform
Passwords.

What is salt?
- Random addition
- Plain
- Key
- None
* Correct answer: Random addition
Unique.

What is a secret?
- Token/password
- Public info
- None
- Code
* Correct answer: Token/password
Protect.

What is least privilege?
- Minimum access
- Full
- None
- Always
* Correct answer: Minimum access
Roles.

What is validation?
- Input checks
- Rendering
- Logging
- None
* Correct answer: Input checks
Trust.

What is a dependency?
- External package
- Own code
- A user
- None
* Correct answer: External package
Update.

What is an exploit?
- Attack use
- Feature
- Test
- None
* Correct answer: Attack use
Vulnerability.

What is OWASP?
- Security knowledge base
- A framework
- A database
- None
* Correct answer: Security knowledge base
Top 10.
<!--/QUIZ-->
