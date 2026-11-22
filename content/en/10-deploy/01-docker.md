---
title: Docker for Python applications
summary: Images, Dockerfile, containers, docker-compose.
order: 1
duration: 45 min
difficulty: intermediate
tags: docker, containers, dockerfile
---

Docker packages apps with their environment.

## Dockerfile

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## Build and run

```bash
docker build -t myapp .
docker run -p 8000:8000 myapp
```

## Compose

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
```

```bash
docker compose up
```

## Lesson summary

Dockerfile defines an image; compose orchestrates services.

<!--TASK-->
### Task 1 — Dockerfile
Write a minimal Dockerfile for a Python app.

### Task 2 — Build
Build and view the image.

### Task 3 — Run
Run the container with a port map.

### Task 4 — Compose
Define a service and start it.

### Task 5 — Copy order
Explain why COPY requirements first.

### Task 6 — Layers
Explain image layers.

### Task 7 — .dockerignore
Describe what it should ignore.
<!--/TASK-->

<!--HINT-->
### Hint 1
FROM python.

### Hint 2
docker build.

### Hint 3
docker run -p.

### Hint 4
docker-compose.yml.

### Hint 5
Layer caching.

### Hint 6
Order matters.

### Hint 7
__pycache__, .venv.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### Solution 2
```bash
docker build -t myapp .
docker images | grep myapp
```

### Solution 3
```bash
docker run -p 8000:8000 myapp
```

### Solution 4
```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
```
```bash
docker compose up
```

### Solution 5
```python
# COPY requirements отдельно — зависимости кэшируются слоем
# при изменении кода pip не переустанавливается
```

### Solution 6
```python
# Каждая инструкция — слой; неизменённые слои переиспользуются
```

### Solution 7
```dockerignore
__pycache__/
.venv/
*.pyc
```
<!--/SOLUTION-->

<!--QUIZ-->
What is an image?
- Immutable snapshot
- A container
- A process
- None
* Correct answer: Immutable snapshot
Template.

What is a container?
- Running image
- An image
- A file
- None
* Correct answer: Running image
Instance.

What is FROM?
- Base image
- A command
- A label
- None
* Correct answer: Base image
Start.

What is WORKDIR?
- Working directory
- A file
- A port
- None
* Correct answer: Working directory
cd.

What is CMD?
- Default command
- Build
- Copy
- None
* Correct answer: Default command
Run.

What is docker build?
- Creates image
- Runs
- Removes
- None
* Correct answer: Creates image
From Dockerfile.

What is docker run?
- Starts container
- Builds
- Stops
- None
* Correct answer: Starts container
Run.

What is -p?
- Port mapping
- Path
- Python
- None
* Correct answer: Port mapping
host:container.

What is compose?
- Multi-container setup
- A single container
- A file
- None
* Correct answer: Multi-container setup
YAML.

What is a layer?
- Build step result
- A container
- An image
- None
* Correct answer: Build step result
Cached.

Why requirements first?
- Cache dependencies
- Speed run
- Style
- None
* Correct answer: Cache dependencies
Efficiency.

What is .dockerignore?
- Excludes files
- Includes
- Copies
- None
* Correct answer: Excludes files
Build context.
<!--/QUIZ-->
