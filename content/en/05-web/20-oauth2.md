---
title: OAuth2: authorization flows and integrations
summary: Authorization code, PKCE, client credentials, refresh tokens, security.
order: 20
duration: 60 min
difficulty: advanced
tags: oauth2, openid, tokens
---

OAuth2 lets users authorize apps without sharing passwords.

## Roles

Resource owner (user), client (app), authorization server, resource server.

## Authorization code flow

1. Redirect user to /authorize?client_id=...&redirect_uri=...;
2. User approves → server redirects with ?code=...;
3. Client exchanges code for tokens at /token.

## PKCE

Public clients send code_verifier and code_challenge to prevent interception.

## Client credentials

Server-to-server: client_id + client_secret → token directly.

## Refresh tokens

Short-lived access tokens + refresh token to renew.

## Security

Use state to prevent CSRF; keep redirect_uri exact; store secrets in env.

## Lesson summary

OAuth2 flows: authorization code, PKCE, client credentials; refresh tokens.

<!--TASK-->
### Task 1 — Roles
List the four roles in a comment.

### Task 2 — Flow steps
Write the three steps of authorization code in a comment.

### Task 3 — PKCE
Generate code_verifier and code_challenge via hashlib/base64.

### Task 4 — Token request
Write a function to POST the token request.

### Task 5 — Refresh
Implement refresh token request.

### Task 6 — State
Explain why state is needed.

### Task 7 — Client credentials
Write a helper to request client-credentials tokens.
<!--/TASK-->

<!--HINT-->
### Hint 1
Owner, client, AS, RS.

### Hint 2
authorize → code → token.

### Hint 3
sha256 of verifier → base64url.

### Hint 4
requests.post(url, data={...}).

### Hint 5
grant_type=refresh_token.

### Hint 6
CSRF.

### Hint 7
grant_type=client_credentials.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
# Resource owner (user), client (app),
# authorization server, resource server
```

### Solution 2
```python
# 1. redirect to /authorize
# 2. user approves, server redirects with ?code=
# 3. client exchanges code at /token
```

### Solution 3
```python
import base64
import hashlib
import secrets

verifier = secrets.token_urlsafe(64)
challenge = base64.urlsafe_b64encode(
    hashlib.sha256(verifier.encode()).digest()
).rstrip(b"=").decode()
```

### Solution 4
```python
import requests

def exchange_code(code, redirect_uri, client_id):
    return requests.post(
        "https://server/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
        },
        timeout=30,
    ).json()
```

### Solution 5
```python
def refresh_token(refresh, client_id):
    return requests.post(
        "https://server/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh,
            "client_id": client_id,
        },
        timeout=30,
    ).json()
```

### Solution 6
```python
# state защищает от CSRF: сервер возвращает его обратно
```

### Solution 7
```python
def client_credentials(client_id, client_secret):
    return requests.post(
        "https://server/token",
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
        timeout=30,
    ).json()
```
<!--/SOLUTION-->

<!--QUIZ-->
What does OAuth2 solve?
- Auth without sharing passwords
- Encryption
- Speed
- Caching
* Correct answer: Auth without sharing passwords
Delegated.

What is a resource owner?
- The user
- The app
- Server
- Token
* Correct answer: The user
Owner.

What is an authorization code?
- Temporary code
- Access token
- Password
- Client
* Correct answer: Temporary code
Exchanged.

What is PKCE?
- Proof Key for Code Exchange
- Password
- Token
- Server
* Correct answer: Proof Key for Code Exchange
Public clients.

What is code_verifier?
- Random secret string
- Token
- Code
- User
* Correct answer: Random secret string
PKCE.

What is a refresh token?
- Renews access token
- Password
- Code
- Client
* Correct answer: Renews access token
Long-lived.

What is client credentials flow?
- Server-to-server
- User
- Browser
- Implicit
* Correct answer: Server-to-server
No user.

What is state?
- CSRF protection
- Token
- Password
- Server
* Correct answer: CSRF protection
Random value.

What is a redirect_uri?
- Registered callback
- Token endpoint
- API
- User
* Correct answer: Registered callback
Must match.

What is an access token?
- Credential for API
- Password
- Code
- Client
* Correct answer: Credential for API
Short-lived.

What grant_type is for refresh?
- refresh_token
- password
- code
- implicit
* Correct answer: refresh_token
Grant.

Why keep secrets in env?
- Avoid leaks
- Speed
- Readability
- None
* Correct answer: Avoid leaks
Security.
<!--/QUIZ-->
