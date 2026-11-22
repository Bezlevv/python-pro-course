---
title: Auth: JWT and tokens
summary: Token flow, simplejwt.
order: 3
duration: 50 min
difficulty: advanced
tags: auth, jwt
---

APIs need to know who is calling.

## Token flow

1. POST /api/token/ with username/password;
2. Server returns access + refresh tokens;
3. Client sends `Authorization: Bearer <access>`.

## simplejwt

```python
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
]
```

## Protect

```python
from rest_framework.permissions import IsAuthenticated

class NotesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
```

## Lesson summary

JWT: obtain, send, refresh.

<!--TASK-->
### Task 1 — URLs
Add token endpoints.

### Task 2 — Obtain
Get a pair of tokens.

### Task 3 — Bearer
Send Authorization header.

### Task 4 — Refresh
Refresh an access token.

### Task 5 — Protect
Require auth on a view.

### Task 6 — Claims
What's inside a JWT?

### Task 7 — Store
Where to store tokens?
<!--/TASK-->

<!--HINT-->
### Hint 1
TokenObtainPairView.

### Hint 2
POST.

### Hint 3
Bearer.

### Hint 4
TokenRefreshView.

### Hint 5
IsAuthenticated.

### Hint 6
Payload.

### Hint 7
Memory.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
]
```

### Solution 2
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"a","password":"x"}'
# → {"access": "...", "refresh": "..."}
```

### Solution 3
```bash
curl http://localhost:8000/api/notes/ \
  -H "Authorization: Bearer <access>"
```

### Solution 4
```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"<refresh>"}'
```

### Solution 5
```python
from rest_framework.permissions import IsAuthenticated

class NotesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
```

### Solution 6
```python
# JWT содержит заголовок, payload (user_id, exp)
# и подпись — подделать нельзя
```

### Solution 7
```python
# В памяти приложения/мобильного клиента;
# НЕ в localStorage без защиты
```
<!--/SOLUTION-->

<!--QUIZ-->
What is JWT?
- JSON Web Token
- A password
- A session
- None
* Correct answer: JSON Web Token
Signed.

What is access?
- Short-lived token
- Long
- Refresh
- None
* Correct answer: Short-lived token
Auth.

What is refresh?
- Renews access
- Auths
- Logs out
- None
* Correct answer: Renews access
Long-lived.

What is Bearer?
- Auth scheme
- A token
- A header name
- None
* Correct answer: Auth scheme
Prefix.

What is payload?
- Claims
- Signature
- Header
- None
* Correct answer: Claims
Data.

What is exp?
- Expiration
- Extension
- Error
- None
* Correct answer: Expiration
Time.

What is a signature?
- Tamper proof
- Payload
- Header
- None
* Correct answer: Tamper proof
Secret.

What is IsAuthenticated?
- Login required
- Public
- Admin only
- None
* Correct answer: Login required
Permission.

What is 401?
- Unauthorized
- OK
- Created
- None
* Correct answer: Unauthorized
No token.

What is 403?
- Forbidden
- OK
- Created
- None
* Correct answer: Forbidden
No rights.

What is a refresh token?
- Longer-lived
- Shorter
- Same
- None
* Correct answer: Longer-lived
Renew.

Why JWT?
- Stateless
- Sessions
- Cookies only
- None
* Correct answer: Stateless
Scale.
<!--/QUIZ-->
