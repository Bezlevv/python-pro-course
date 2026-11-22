---
title: Password hashing and auth
summary: Argon2, bcrypt, session safety.
order: 4
duration: 45 min
difficulty: advanced
tags: hashing, auth
---

Never store plaintext passwords.

## Hash

```python
from passlib.hash import argon2

hash_value = argon2.hash("secret")
print(argon2.verify("secret", hash_value))   # True
```

## Why

Hash is one-way; with salt, same passwords differ.

## Sessions

Use secure cookies, HttpOnly, expiry.

## Lesson summary

Slow salted hashes + secure sessions.

<!--TASK-->
### Task 1 — Hash
Hash a password.

### Task 2 — Verify
Verify correctly/incorrectly.

### Task 3 — Salt
Explain why salt.

### Task 4 — Slow hash
Why deliberately slow?

### Task 5 — Session
Secure cookie flags.

### Task 6 — Reset
What if a hash leaks?

### Task 7 — Django
How does Django store passwords?
<!--/TASK-->

<!--HINT-->
### Hint 1
argon2.hash.

### Hint 2
verify.

### Hint 3
Uniqueness.

### Hint 4
Brute force.

### Hint 5
HttpOnly.

### Hint 6
Change.

### Hint 7
PBKDF2.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from passlib.hash import argon2
hash_value = argon2.hash("secret")
```

### Solution 2
```python
argon2.verify("secret", hash_value)     # True
argon2.verify("wrong", hash_value)      # False
```

### Solution 3
```text
Соль — случайная добавка: одинаковые пароли
дают разные хеши; радужные таблицы не работают
```

### Solution 4
```text
Медленный хеш (argon2/bcrypt) делает
перебор паролей дорогим
```

### Solution 5
```text
HttpOnly, Secure, SameSite=Lax/Strict,
срок действия
```

### Solution 6
```text
При утечке — немедленно сбросить пароли
и заставить сменить
```

### Solution 7
```text
Django хранит PBKDF2/SHA256 с солью;
количество итераций настраивается
```
<!--/SOLUTION-->

<!--QUIZ-->
What is hashing?
- One-way transform
- Encryption
- Encoding
- None
* Correct answer: One-way transform
Irreversible.

Why salt?
- Different hashes
- Same hashes
- Faster
- None
* Correct answer: Different hashes
Rainbow.

What is argon2?
- Slow hash
- Fast hash
- Cipher
- None
* Correct answer: Slow hash
Modern.

What is verify?
- Checks password
- Hashes
- Encrypts
- None
* Correct answer: Checks password
Compare.

What is brute force?
- Trying all
- One try
- Guess only
- None
* Correct answer: Trying all
Attack.

What is HttpOnly?
- JS can't read
- Open
- Required
- None
* Correct answer: JS can't read
Cookie.

What is Secure?
- HTTPS only
- Any
- None
- Always
* Correct answer: HTTPS only
Cookie.

What is SameSite?
- CSRF defense
- Hash
- Salt
- None
* Correct answer: CSRF defense
Cookie.

What is a session?
- Signed-in state
- Password
- Hash
- None
* Correct answer: Signed-in state
Cookie.

What is PBKDF2?
- Django default
- Plain
- Salt only
- None
* Correct answer: Django default
Hash.

What is a leak?
- Data exposure
- Feature
- Test
- None
* Correct answer: Data exposure
Incident.

What is the rule?
- Never plaintext
- Sometimes
- Always plain
- None
* Correct answer: Never plaintext
Hash.
<!--/QUIZ-->
