---
title: JWT, authorization and security
summary: Tokens, hashing passwords, protecting endpoints, FastAPI/Django examples.
order: 12
duration: 50 min
difficulty: advanced
tags: jwt, auth, security
---

JWTs carry identity; secure apps hash passwords and protect endpoints.

## Password hashing

```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hash = pwd_context.hash("secret")
pwd_context.verify("secret", hash)   # True
```

## JWT

```python
import jwt
from datetime import datetime, timedelta, timezone

def create_token(user_id):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(hours=2),
    }
    return jwt.encode(payload, "SECRET", algorithm="HS256")

def read_token(token):
    return jwt.decode(token, "SECRET", algorithms=["HS256"])
```

## Protecting endpoints

```python
from fastapi import Depends, HTTPException

def get_current_user(token: str):
    try:
        return read_token(token)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401)
```

## Lesson summary

Hash passwords, sign JWTs, verify tokens; never store plaintext secrets.

<!--TASK-->
### Task 1 — Hash
Create a hashed password and verify it.

### Task 2 — Wrong password
Verify with a wrong password → False.

### Task 3 — Create token
Generate a JWT with sub and exp.

### Task 4 — Read token
Decode it and extract sub.

### Task 5 — Expired
Create a token with past exp and catch error.

### Task 6 — Secure endpoint
Write a helper requiring a valid token.

### Task 7 — Secrets advice
Explain why the secret is not stored in code.
<!--/TASK-->

<!--HINT-->
### Hint 1
pwd_context.hash(...).

### Hint 2
verify returns False.

### Hint 3
jwt.encode(payload, key, algorithm="HS256").

### Hint 4
jwt.decode(token, key, algorithms=["HS256"]).

### Hint 5
exp in the past → ExpiredSignatureError.

### Hint 6
Depends + try/except.

### Hint 7
Use env vars.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
h = pwd_context.hash("secret")
print(pwd_context.verify("secret", h))   # True
```

### Solution 2
```python
print(pwd_context.verify("wrong", h))   # False
```

### Solution 3
```python
import jwt
from datetime import datetime, timedelta, timezone

def create_token(user_id, secret="SECRET"):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(hours=2),
    }
    return jwt.encode(payload, secret, algorithm="HS256")

token = create_token(7)
```

### Solution 4
```python
payload = jwt.decode(token, "SECRET", algorithms=["HS256"])
print(payload["sub"])   # 7
```

### Solution 5
```python
payload = {"sub": "1", "exp": datetime.now(timezone.utc) - timedelta(hours=1)}
expired = jwt.encode(payload, "SECRET", algorithm="HS256")
try:
    jwt.decode(expired, "SECRET", algorithms=["HS256"])
except jwt.ExpiredSignatureError:
    print("expired")
```

### Solution 6
```python
from fastapi import HTTPException

def get_current_user(token: str):
    try:
        return jwt.decode(token, "SECRET", algorithms=["HS256"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### Solution 7
```python
# secret из окружения, не в коде:
import os
SECRET = os.environ.get("SECRET_KEY", "dev-only")
```
<!--/SOLUTION-->

<!--QUIZ-->
Why hash passwords?
- Protect stored secrets
- Speed
- Readability
- Size
* Correct answer: Protect stored secrets
One-way.

What is bcrypt?
- Slow hash for passwords
- JWT
- Symmetric cipher
- Salt only
* Correct answer: Slow hash for passwords
Cracking resistant.

What is JWT?
- JSON Web Token
- Password
- Session
- Cookie
* Correct answer: JSON Web Token
Signed claims.

What is payload?
- Claims data
- Signature
- Header
- Key
* Correct answer: Claims data
sub, exp.

What is exp?
- Expiration time
- Subject
- Issuer
- Audience
* Correct answer: Expiration time
When invalid.

What does create_token return?
- Signed token string
- Dict
- Hash
- None
* Correct answer: Signed token string
Encoded.

What does decode verify?
- Signature + expiration
- Only payload
- Password
- Role
* Correct answer: Signature + expiration
Integrity.

What raises ExpiredSignatureError?
- Past exp
- Bad signature
- No key
- None
* Correct answer: Past exp
Expired.

What is a 401?
- Unauthorized
- OK
- Forbidden
- Missing
* Correct answer: Unauthorized
Bad/absent token.

What is PyJWTError?
- JWT exception base
- A token
- A hash
- A header
* Correct answer: JWT exception base
Catch.

Where to keep the secret?
- Environment
- Code
- Readme
- Logs
* Correct answer: Environment
Never in code.

What does HS256 mean?
- HMAC-SHA256 signing
- Hash only
- Cipher
- Header
* Correct answer: HMAC-SHA256 signing
Algorithm.
<!--/QUIZ-->
