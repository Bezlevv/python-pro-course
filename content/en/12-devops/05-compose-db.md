---
title: Docker Compose: database + app
summary: Services, volumes, depends_on, health checks.
order: 5
duration: 45 min
difficulty: advanced
tags: docker, compose, postgres
---

Compose runs multi-service stacks with one command.

## docker-compose.yml

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - db_data:/var/lib/postgresql/data
  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
volumes:
  db_data:
```

## Up

```bash
docker compose up -d
docker compose logs -f
docker compose down
```

## Lesson summary

Compose wires services, storage, and networks.

<!--TASK-->
### Task 1 — Compose file
Create db + app services.

### Task 2 — Environment
Set POSTGRES_PASSWORD.

### Task 3 — Volume
Persist DB data.

### Task 4 — depends_on
Start db before app.

### Task 5 — Ports
Expose app port 8000.

### Task 6 — Up/down
Run compose up and down.

### Task 7 — Logs
View service logs.
<!--/TASK-->

<!--HINT-->
### Hint 1
services:.

### Hint 2
environment:.

### Hint 3
volumes:.

### Hint 4
depends_on:.

### Hint 5
ports:.

### Hint 6
docker compose up -d.

### Hint 7
docker compose logs.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```yaml
services:
  db:
    image: postgres:16
  app:
    build: .
    ports:
      - "8000:8000"
```

### Solution 2
```yaml
db:
  image: postgres:16
  environment:
    POSTGRES_PASSWORD: secret
    POSTGRES_DB: mydb
```

### Solution 3
```yaml
db:
  volumes:
    - db_data:/var/lib/postgresql/data
volumes:
  db_data:
```

### Solution 4
```yaml
app:
  depends_on:
    - db
```

### Solution 5
```yaml
app:
  ports:
    - "8000:8000"
```

### Solution 6
```bash
docker compose up -d
docker compose down
```

### Solution 7
```bash
docker compose logs -f app
```
<!--/SOLUTION-->

<!--QUIZ-->
What is compose?
- Multi-container tool
- Single container
- A database
- None
* Correct answer: Multi-container tool
YAML.

What is a service?
- One container
- A volume
- A network
- None
* Correct answer: One container
Definition.

What is a volume?
- Persistent storage
- Memory
- Port
- None
* Correct answer: Persistent storage
Data.

What is depends_on?
- Start order
- Network
- Volume
- None
* Correct answer: Start order
db first.

What is image:?
- Prebuilt image
- Build
- Volume
- None
* Correct answer: Prebuilt image
postgres.

What is build:?
- Build from Dockerfile
- Pull
- Copy
- None
* Correct answer: Build from Dockerfile
Local.

What is ports:?
- host:container
- Volumes
- Env
- None
* Correct answer: host:container
Expose.

What is up -d?
- Background start
- Foreground
- Stop
- None
* Correct answer: Background start
Detached.

What is down?
- Stops containers
- Deletes image
- Builds
- None
* Correct answer: Stops containers
Cleanup.

What is logs -f?
- Follow logs
- One-time
- Clear
- None
* Correct answer: Follow logs
Live.

What is environment:?
- Env vars
- Ports
- Volumes
- None
* Correct answer: Env vars
Config.

What is POSTGRES_PASSWORD?
- DB password
- Host
- Port
- None
* Correct answer: DB password
Postgres.
<!--/QUIZ-->
