---
title: Message Queues
summary: Why queues are needed, exchange models (work queue, pub/sub), brokers, delivery guarantees, duplicate handling, and dead letters.
order: 5
duration: 45 min
difficulty: advanced
tags: queues, rabbitmq, kafka, pub/sub, brokers, retry, dead letter
---

A message queue is a buffer between a producer and a consumer. The producer puts a message into the queue, and the consumer takes it out and processes it. The main benefit is **loose coupling**: the producer doesn't know who will process the message or when, and doesn't wait for an answer. This lets you spread out load spikes, survive consumer downtime, and scale handlers independently.

## Work queue

The simplest model: several consumers compete for messages — each message is received by exactly one consumer (competing consumers). A classic example is sending emails or processing images: a producer publishes tasks, and workers process them in parallel.

In Python you can show the idea with the standard `queue.Queue` and threads:

```python
import threading
import queue
import time

jobs = queue.Queue()
for i in range(5):
    jobs.put(f"task {i}")

def worker(worker_id):
    while not jobs.empty():
        try:
            job = jobs.get_nowait()
        except queue.Empty:
            return
        print(f"Worker {worker_id} took: {job}")
        time.sleep(0.1)
        jobs.task_done()

threads = [threading.Thread(target=worker, args=(n,)) for n in (1, 2)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

Here you already see the essence of a work queue: tasks are distributed among threads, and each consumer takes the next free one.

## Brokers: RabbitMQ and Kafka

In real systems the queue lives in a **broker** — a separate service. RabbitMQ is a classic broker supporting exchange models: direct queues, exchanges with routing, pub/sub. Kafka is a distributed log: messages are stored as a stream of events, consumers read them at their own pace and can re-read history. Kafka is ideal for event buses and analytics; RabbitMQ is ideal for tasks and work queues.

An example of sending to RabbitMQ via the `pika` library (install with `pip install pika`):

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="tasks")
channel.basic_publish(exchange="", routing_key="tasks", body="Hello, queue!")
connection.close()
```

## Pub/Sub

In the pub/sub model, a message is received by **all** subscribers of a topic, not one. This is needed for events: "order created" should be heard by the warehouse, analytics, and notifications alike. In RabbitMQ this is done with `fanout` or `topic` exchanges, and Kafka topics work on the same principle.

## Delivery guarantees

Guarantees are the most important topic of queues:

- **At-most-once**: a message may be lost (no acknowledgments).
- **At-least-once**: a message will be delivered, but possibly several times — the receiver must be idempotent.
- **Exactly-once**: exactly once — implemented by combining mechanisms, always expensive and not always achievable.

In practice the standard is at-least-once + an idempotent handler: repeated deliveries are safe because the handler can recognize duplicates (by message id).

## Dead letters and retry

If processing fails, the message must not be lost. The strategy is **retry with backoff**: repeat with an increasing delay, and after N attempts put the message into a **dead-letter queue** for manual review. It's like the circuit breaker in microservices, but at the message level.

## Consumer idempotency

A consumer must be able to process the same message twice without harm. A simple technique is remembering the IDs of processed messages:

```python
processed = set()

def handle(message):
    if message["id"] in processed:
        return
    processed.add(message["id"])
    print(f"Processed: {message['id']}")
```

We'll develop this technique in the tasks.

<!--TASK-->
### Task 1
Write a program with `queue.Queue` and threads: put 6 numbers (1..6) into the queue, create two workers that take a number, print `Worker N took: X` and "work" for `time.sleep(0.05)`. Wait for completion with `join()`. Expected result: 6 lines on screen with tasks distributed between the two workers (the exact distribution may vary, but each number is processed exactly once).

### Task 2
Implement retry with backoff and a dead queue. Write a function `process_with_retry(job, attempts=3, base_delay=0.05)` that tries to process a task; if the handler raises an exception, it retries with a delay `base_delay * 2 ** attempt`, and after the attempts are exhausted returns the tuple `(False, job)` — a "dead letter" marker. Test it on a task that always fails. Expected output: `Dead letter: {'id': 1}` after three attempts.

### Task 3
Make a consumer idempotent. Write a class `IdempotentConsumer` that stores a set of processed IDs and has a method `process(message)` (message is a dict with an `id` key) that prints `Processed: {id}` only for new messages, and `Duplicate: {id}` for repeated ones. Verify: process a message with id=1 twice and with id=2 once. Expected output: `Processed: 1`, `Duplicate: 1`, `Processed: 2`.

### Task 4
Implement a mini pub/sub in pure Python. The class `Broker` has a dict `subscribers: dict[str, list[callable]]`, methods `subscribe(topic, callback)` and `publish(topic, message)` that calls all of the topic's callbacks. Subscribe two handlers to the topic `"order.created"` (they print `Warehouse received: ...` and `Analytics received: ...`), publish the message `{"order_id": 7}`. Then publish to an unoccupied topic — nothing should print. Expected output: two lines for order 7.

### Task 5
Improve the work queue: each worker, via `queue.Queue` with `task_done()`, prints `Done: {job}` after processing, and the main program waits for `join()` and prints `All tasks done` only when the queue is empty. Use `queue.Queue` and `threading.Thread`. Expected output: `Done: ...` lines for each of the 4 tasks and the final line `All tasks done`.
<!--/TASK-->

<!--HINT-->
### Hint 1
Use `jobs.get_nowait()` and handle `queue.Empty`. Start threads via the constructor `threading.Thread(target=worker, args=(n,))`, then `start()` and `join()`. The list of numbers is `list(range(1, 7))`, put them with `put`.

### Hint 2
The handler is a function that always raises `RuntimeError`. In a loop `range(attempts)` wrap the call in try/except: on success `(True, job)`, on exception — `time.sleep(base_delay * 2 ** attempt)`, and after the loop — `(False, job)`. Print the tuple: `print(f"Dead letter: {job}")`.

### Hint 3
In `process` check `if message["id"] in self.processed` — print `Duplicate: ...`; otherwise add to `self.processed` and print `Processed: ...`. Create one instance and call `process` three times.

### Hint 4
In `publish` fetch the callback list with `self.subscribers.get(topic, [])` and call each: `callback(message)`. In `subscribe` use `setdefault(topic, []).append(callback)`.

### Hint 5
The worker in a loop takes a task via `get_nowait()`, prints `Done: {job}`, calls `jobs.task_done()`. After starting the threads, the main program calls `jobs.join()` and prints `All tasks done`. Don't forget `import queue`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
import threading
import queue
import time

jobs = queue.Queue()
for i in range(1, 7):
    jobs.put(i)

def worker(worker_id):
    while True:
        try:
            job = jobs.get_nowait()
        except queue.Empty:
            return
        print(f"Worker {worker_id} took: {job}")
        time.sleep(0.05)
        jobs.task_done()

threads = [threading.Thread(target=worker, args=(n,)) for n in (1, 2)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

Example output:

```
Worker 1 took: 1
Worker 2 took: 2
Worker 1 took: 3
Worker 2 took: 4
Worker 1 took: 5
Worker 2 took: 6
```

What's happening here? `queue.Queue` is thread-safe: threads compete for tasks, and each task goes to exactly one worker. `task_done()` tells the queue that a task is processed — this will be useful in task five for `join()`.

### Solution 2
Solution:

```python
import time

def always_fails(job):
    raise RuntimeError("failure")

def process_with_retry(job, attempts=3, base_delay=0.05):
    for attempt in range(attempts):
        try:
            always_fails(job)
            return (True, job)
        except Exception:
            if attempt == attempts - 1:
                return (False, job)
            time.sleep(base_delay * 2 ** attempt)

job = {"id": 1}
success, job = process_with_retry(job)
print(f"Dead letter: {job}" if not success else "Success")
```

Output: `Dead letter: {'id': 1}`. What's happening here? The function makes three attempts with delays of 0.05 s, 0.1 s and 0.2 s. Since `always_fails` always raises, after the third attempt it returns `(False, job)` — a dead-letter marker. In a real system such a message is moved to a separate queue for manual analysis rather than lost.

### Solution 3
Solution:

```python
class IdempotentConsumer:
    def __init__(self):
        self.processed = set()

    def process(self, message):
        if message["id"] in self.processed:
            print(f"Duplicate: {message['id']}")
            return
        self.processed.add(message["id"])
        print(f"Processed: {message['id']}")

consumer = IdempotentConsumer()
consumer.process({"id": 1})
consumer.process({"id": 1})
consumer.process({"id": 2})
```

Output:

```
Processed: 1
Duplicate: 1
Processed: 2
```

What's happening here? The set `processed` stores the IDs of already processed messages. A repeated delivery of the message with id=1 is recognized and ignored — that's idempotency, the key to safe at-least-once mode.

### Solution 4
Solution:

```python
class Broker:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, topic, callback):
        self.subscribers.setdefault(topic, []).append(callback)

    def publish(self, topic, message):
        for callback in self.subscribers.get(topic, []):
            callback(message)

broker = Broker()
broker.subscribe("order.created", lambda m: print(f"Warehouse received: {m['order_id']}"))
broker.subscribe("order.created", lambda m: print(f"Analytics received: {m['order_id']}"))

broker.publish("order.created", {"order_id": 7})
broker.publish("other.topic", {"order_id": 999})
```

Output:

```
Warehouse received: 7
Analytics received: 7
```

What's happening here? In pub/sub every subscriber of a topic receives every message. Publishing to an unoccupied topic calls no callbacks because the subscriber list is empty. This is a minimal but fully working broker for understanding the idea.

### Solution 5
Solution:

```python
import threading
import queue

jobs = queue.Queue()
for i in range(4):
    jobs.put(i)

def worker(worker_id):
    while True:
        try:
            job = jobs.get_nowait()
        except queue.Empty:
            return
        print(f"Done: {job}")
        jobs.task_done()

threads = [threading.Thread(target=worker, args=(n,)) for n in (1, 2)]
for t in threads:
    t.start()

jobs.join()
print("All tasks done")
```

Output (order may differ):

```
Done: 0
Done: 1
Done: 2
Done: 3
All tasks done
```

What's happening here? `jobs.join()` blocks the main program until all tasks are processed (each `task_done()` decrements the internal counter). Only when the queue is empty and all threads have finished does `All tasks done` print. This guarantees the program doesn't exit before processing is complete.
<!--/SOLUTION-->

<!--QUIZ-->
What is a work queue?
- A queue where each message is received by exactly one consumer
- A queue where all consumers receive all messages
- A database
- A task list in Excel
* Correct answer: A queue where each message is received by exactly one consumer
Consumers compete: a message goes to one of them (competing consumers).

How does pub/sub differ from a work queue?
- The message is received by all subscribers of the topic
- The message is deleted immediately
- There are no subscribers
- They are the same
* Correct answer: The message is received by all subscribers of the topic
Each subscriber gets a copy of the event.

Which delivery mode requires an idempotent handler?
- At-most-once
- At-least-once
- Fast delivery
- None
* Correct answer: At-least-once
A message may arrive several times, so repeated processing must be harmless.

Why is a dead queue needed?
- To store messages that couldn't be processed after all attempts
- To speed up delivery
- To delete all messages
- To store logs
* Correct answer: To store messages that couldn't be processed after all attempts
Dead letters are reviewed manually or replayed later.

What does queue.Queue.task_done() do?
- Marks a task as processed
- Deletes the queue
- Creates a task
- Puts a task at the front
* Correct answer: Marks a task as processed
task_done() decrements the internal counter that join() relies on.

What is the key difference between Kafka and RabbitMQ?
- Kafka is a distributed event log; RabbitMQ is a queue broker with exchanges
- Kafka writes files to disk faster
- They are synonyms
- RabbitMQ can't store messages
* Correct answer: Kafka is a distributed event log; RabbitMQ is a queue broker with exchanges
Kafka is more for event streams; RabbitMQ for work queues and routing.

What is an exchange in RabbitMQ?
- A router that directs messages into queues according to rules
- The queue itself
- A consumer
- A message
* Correct answer: A router that directs messages into queues according to rules
A publisher sends a message to an exchange, which distributes it into queues.

What happens if a consumer crashes after receiving a message but before acknowledging it (ack)?
- The message returns to the queue and is delivered again
- The message is lost forever
- The queue stops
- The message is deleted
* Correct answer: The message returns to the queue and is delivered again
Without an ack the broker considers the message undelivered and retries delivery.
<!--/QUIZ-->
