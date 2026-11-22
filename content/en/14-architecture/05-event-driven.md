---
title: Event-driven architecture
summary: Events, queues, producers/consumers.
order: 5
duration: 45 min
difficulty: advanced
tags: events, queue, architecture
---

Components communicate via events.

## Key ideas

- Producer: sends events;
- Consumer: reacts;
- Queue/broker: decouples them.

## Python example

```python
from collections import deque

class Broker:
    def __init__(self):
        self.subscribers = []
    def subscribe(self, fn):
        self.subscribers.append(fn)
    def publish(self, event):
        for fn in self.subscribers:
            fn(event)

broker = Broker()
broker.subscribe(lambda e: print("order:", e))
broker.publish({"type": "order_created", "id": 1})
```

## Benefits

Decoupling, scalability, async processing.

## Lesson summary

Events decouple producers from consumers.

<!--TASK-->
### Task 1 — Broker
Implement a simple broker.

### Task 2 — Producer
Publish two events.

### Task 3 — Consumer
Subscribe and log.

### Task 4 — Queue
Use deque as an in-memory queue.

### Task 5 — Why
List two benefits.

### Task 6 — Trade-off
One downside.

### Task 7 — Real
Name a real message broker.
<!--/TASK-->

<!--HINT-->
### Hint 1
Subscribers.

### Hint 2
publish.

### Hint 3
subscribe.

### Hint 4
deque.

### Hint 5
Decoupling.

### Hint 6
Consistency.

### Hint 7
RabbitMQ.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
class Broker:
    def __init__(self):
        self.subscribers = []
    def subscribe(self, fn):
        self.subscribers.append(fn)
    def publish(self, event):
        for fn in self.subscribers:
            fn(event)
```

### Solution 2
```python
broker.publish({"type": "order_created", "id": 1})
broker.publish({"type": "payment_done", "id": 1})
```

### Solution 3
```python
broker.subscribe(lambda e: print("got", e["type"]))
```

### Solution 4
```python
from collections import deque
q = deque()
q.append({"type": "email", "to": "a@b.c"})
event = q.popleft()
```

### Solution 5
```python
# Слабая связность производителей и потребителей
# Лёгкое масштабирование потребителей
```

### Solution 6
```python
# Сложнее гарантировать консистентность:
# событие может потеряться/задержаться
```

### Solution 7
```python
# RabbitMQ, Kafka, Redis Streams, SQS
```
<!--/SOLUTION-->

<!--QUIZ-->
What is an event?
- A signal
- A table
- A class
- None
* Correct answer: A signal
Fact.

What is a producer?
- Sends events
- Receives
- Stores
- None
* Correct answer: Sends events
Source.

What is a consumer?
- Reacts to events
- Sends
- Creates
- None
* Correct answer: Reacts to events
Listener.

What is a broker?
- Middleman
- Database
- Endpoint
- None
* Correct answer: Middleman
Queue.

What is publish?
- Sends event
- Subscribes
- Deletes
- None
* Correct answer: Sends event
Broadcast.

What is subscribe?
- Registers interest
- Sends
- Ignores
- None
* Correct answer: Registers interest
Callback.

What is the benefit?
- Decoupling
- Coupling
- Speed only
- None
* Correct answer: Decoupling
Flexibility.

What is a queue?
- Pending events
- Instant
- A table
- None
* Correct answer: Pending events
Order.

What is RabbitMQ?
- Message broker
- Database
- Framework
- None
* Correct answer: Message broker
Real.

What is asynchronous?
- Non-blocking
- Instant
- Same
- None
* Correct answer: Non-blocking
Later.

What is a downside?
- Consistency
- Speed
- Simplicity
- None
* Correct answer: Consistency
Harder.

What is decoupling?
- Independent parts
- Joined
- Slower
- None
* Correct answer: Independent parts
Design.
<!--/QUIZ-->
