---
title: WebSockets and background tasks
summary: Real-time connections and Celery/RQ for async processing.
order: 14
duration: 50 min
difficulty: advanced
tags: websockets, celery, rq, background
---

WebSockets give real-time two-way communication; queues run background jobs.

## WebSocket basics

```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"echo: {data}")
```

## Why queues

HTTP is synchronous; heavy tasks should run in background workers.

## Celery

```python
from celery import Celery

app = Celery("tasks", broker="redis://localhost:6379/0")

@app.task
def send_email(to):
    # heavy work
    return f"sent to {to}"
```

Run worker: `celery -A tasks worker`.

## RQ

```python
from redis import Redis
from rq import Queue

q = Queue(connection=Redis())
q.enqueue(send_email, "a@test.ru")
```

## Lesson summary

WebSockets for real-time; Celery/RQ offload long tasks.

<!--TASK-->
### Task 1 — WebSocket echo
Implement an echo WebSocket endpoint.

### Task 2 — Client
Write a small WebSocket test client.

### Task 3 — Celery task
Define a task and note the worker command.

### Task 4 — Enqueue
Enqueue a task in Celery.

### Task 5 — RQ queue
Use RQ to enqueue a function.

### Task 6 — Broker
Explain why a broker like Redis is needed.

### Task 7 — Poll vs push
Compare long polling with WebSockets.
<!--/TASK-->

<!--HINT-->
### Hint 1
@ app.websocket("/ws").

### Hint 2
websockets.connect.

### Hint 3
@app.task.

### Hint 4
task.delay(...).

### Hint 5
Queue(connection=Redis()) + enqueue.

### Hint 6
Keeps jobs.

### Hint 7
Push = low latency.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"echo: {data}")
```

### Solution 2
```python
import asyncio
import websockets

async def main():
    async with websockets.connect("ws://localhost:8000/ws") as ws:
        await ws.send("hi")
        print(await ws.recv())

asyncio.run(main())
```

### Solution 3
```python
from celery import Celery

app = Celery("tasks", broker="redis://localhost:6379/0")

@app.task
def send_email(to):
    return f"sent to {to}"
```
Run: `celery -A tasks worker`.

### Solution 4
```python
send_email.delay("a@test.ru")
```

### Solution 5
```python
from redis import Redis
from rq import Queue

q = Queue(connection=Redis())
q.enqueue(send_email, "a@test.ru")
```

### Solution 6
```python
# Broker хранит задачи между вебом и воркерами
```

### Solution 7
```python
# WebSocket: сервер сам шлёт данные (push)
# Long polling: клиент периодически спрашивает
```
<!--/SOLUTION-->

<!--QUIZ-->
What are WebSockets?
- Two-way persistent connection
- HTTP GET
- Polling
- FTP
* Correct answer: Two-way persistent connection
Real-time.

What does receive_text do?
- Awaits a message
- Sends
- Closes
- Opens
* Correct answer: Awaits a message
Receive.

What does send_text do?
- Sends a message
- Receives
- Closes
- Accepts
* Correct answer: Sends a message
Echo.

What is a broker?
- Message store
- Worker
- App
- DB
* Correct answer: Message store
Redis.

What is Celery?
- Async task queue
- ORM
- Server
- Template
* Correct answer: Async task queue
Python.

How to run a worker?
- celery -A tasks worker
- python worker
- run tasks
- celery start
* Correct answer: celery -A tasks worker
CLI.

What does .delay do?
- Enqueues a task
- Runs synchronously
- Deletes
- Sleeps
* Correct answer: Enqueues a task
Async.

What is RQ?
- Simple Redis queue
- A DB
- A server
- A template
* Correct answer: Simple Redis queue
RQ.

What does enqueue do?
- Adds a job
- Removes
- Runs now
- Blocks
* Correct answer: Adds a job
To queue.

Why background tasks?
- Don't block responses
- Faster
- Smaller
- Logs
* Correct answer: Don't block responses
UX.

What is long polling?
- Client polls repeatedly
- Server pushes
- New protocol
- Cache
* Correct answer: Client polls repeatedly
Inefficient.

What is push?
- Server sends updates
- Client asks
- Periodic
- None
* Correct answer: Server sends updates
WebSocket.
<!--/QUIZ-->
