---
title: Production launch: Gunicorn and Nginx
summary: WSGI server, static files, proxy setup.
order: 3
duration: 50 min
difficulty: advanced
tags: gunicorn, nginx, production
---

Serve Python apps in production properly.

## Gunicorn

```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 3 app:app
```

## Why Gunicorn

Django/Flask dev servers are not production-ready; Gunicorn handles concurrency.

## Nginx

```nginx
server {
  listen 80;
  location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
  }
  location /static/ {
    alias /app/static/;
  }
}
```

## Lesson summary

Gunicorn runs the app; Nginx proxies and serves static.

<!--TASK-->
### Task 1 — Run gunicorn
Write the command for 3 workers.

### Task 2 — Workers
Explain --workers.

### Task 3 — Static
Why Nginx serves static?

### Task 4 — Proxy
Write a basic Nginx config.

### Task 5 — Headers
Add X-Real-IP.

### Task 6 — Restart
Explain nginx -s reload.

### Task 7 — Compare
Compare dev server vs gunicorn.
<!--/TASK-->

<!--HINT-->
### Hint 1
gunicorn app:app.

### Hint 2
Processes.

### Hint 3
Speed.

### Hint 4
server block.

### Hint 5
proxy_set_header.

### Hint 6
Reload.

### Hint 7
Production.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```bash
gunicorn --bind 0.0.0.0:8000 --workers 3 app:app
```

### Solution 2
```python
# --workers — число процессов-воркеров
# ~2-4 × ядра CPU
```

### Solution 3
```python
# Nginx отдаёт статику быстрее, не нагружая Python
```

### Solution 4
```nginx
server {
  listen 80;
  location / {
    proxy_pass http://127.0.0.1:8000;
  }
}
```

### Solution 5
```nginx
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header Host $host;
```

### Solution 6
```bash
nginx -t          # проверить конфиг
nginx -s reload   # применить без простоя
```

### Solution 7
```python
# Flask dev: одиночный процесс, для разработки
# Gunicorn: многопроцессный, для продакшена
```
<!--/SOLUTION-->

<!--QUIZ-->
What is Gunicorn?
- WSGI server
- A web framework
- A proxy
- None
* Correct answer: WSGI server
Python.

What is WSGI?
- Interface standard
- A server
- A framework
- None
* Correct answer: Interface standard
App-server.

What are workers?
- Processes
- Threads only
- Requests
- None
* Correct answer: Processes
Concurrency.

What does --bind do?
- Host:port
- Workers
- Timeout
- None
* Correct answer: Host:port
Address.

What is Nginx?
- Web server/proxy
- WSGI
- Framework
- None
* Correct answer: Web server/proxy
Front.

What does proxy_pass do?
- Forwards requests
- Serves static
- Blocks
- None
* Correct answer: Forwards requests
Backend.

Why Nginx static?
- Faster
- Required
- Python-only
- None
* Correct answer: Faster
Offload.

What is listen 80?
- Port
- Host
- Path
- None
* Correct answer: Port
HTTP.

What is reload?
- Reapplies config
- Restarts all
- Stops
- None
* Correct answer: Reapplies config
No downtime.

Why not Flask dev server?
- Not production-safe
- Fast
- Good
- None
* Correct answer: Not production-safe
Single process.

What is a reverse proxy?
- Nginx before app
- App before
- DB
- None
* Correct answer: Nginx before app
Architecture.

What is a header?
- Metadata
- Body
- Code
- None
* Correct answer: Metadata
X-Real-IP.
<!--/QUIZ-->
