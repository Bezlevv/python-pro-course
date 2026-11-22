---
title: Data Streaming
summary: Stream processing: event generators, windowed aggregates, Kafka concepts (topics, partitions, consumer groups), and mini-processors.
order: 6
duration: 40 min
difficulty: advanced
tags: streaming, kafka, generators, windows, events
---

## Batch and Stream Processing

So far we've read data entirely or in pieces from files. That's batch processing: the data already exists; we read it, computed, got a result. But there's a class of tasks where data arrives continuously: service logs, sensor telemetry, web app clicks, financial transactions. Waiting for "the end of the file" is pointless — there isn't one. That's where streaming comes in: processing a stream of events as they arrive.

## A Stream as a Generator

In Python, a stream is any iterable — often an infinite generator:

```python
import itertools, random

def sensor_stream():
    while True:
        yield {"sensor": random.choice(["t1", "t2"]), "temp": random.uniform(15, 30)}

stream = sensor_stream()
for event in itertools.islice(stream, 5):
    print(event)
```

We don't know and don't want to know how many events there will be. `itertools.islice` takes the first 5 — and the stream doesn't leak into memory.

## Event Processing

An event is usually a dictionary. Typical operations:

- map — transform an event (add a field, round);
- filter — discard unneeded ones;
- aggregate — accumulate statistics;
- window — group by a time window.

The simplest processor:

```python
def parse_event(line: str) -> dict:
    ev = {}
    for part in line.split("|"):
        key, _, value = part.partition("=")
        ev[key] = value
    return ev

print(parse_event("ts=2024-01-01T00:00:01Z|city=moscow|temp=23.5"))
# {'ts': '2024-01-01T00:00:01Z', 'city': 'moscow', 'temp': '23.5'}
```

## Windowed Aggregates

The most common streaming question: "what's the average temperature over the last 10 seconds?" This needs windows — sliding segments. A classic implementation with `collections.deque`:

```python
from collections import deque

class WindowAvg:
    def __init__(self, size: int):
        self.size = size
        self.window = deque()

    def push(self, value: float):
        self.window.append(value)
        if len(self.window) > self.size:
            self.window.popleft()
        if len(self.window) == self.size:
            return sum(self.window) / self.size
        return None

avg = WindowAvg(3)
for v in [10, 20, 30, 40]:
    print(avg.push(v))   # None, None, 20.0, 30.0
```

`deque` keeps exactly `size` latest elements in memory, so memory doesn't grow with the stream length.

## Kafka: a Distributed Message Broker

When there are many events and several processors, you need a delivery system. The industry standard is Apache Kafka. Basic concepts:

- Topic — a named stream of messages;
- Partitions — a topic is cut into pieces; each partition is an ordered queue;
- Offset — the number of a message inside a partition;
- Consumer group — a set of processes that read a topic together: each message is processed by exactly one group member;
- Delivery semantics: at-most-once (may lose messages), at-least-once (may duplicate), exactly-once (exactly once — the most expensive).

The Python client is `confluent_kafka`:

```python
from confluent_kafka import Producer, Consumer

producer = Producer({"bootstrap.servers": "localhost:9092"})
producer.produce("events", value=b'{"temp": 23.5}')
producer.flush()
```

```python
consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "analytics",
    "auto.offset.reset": "earliest",
})
consumer.subscribe(["events"])
while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print("Error:", msg.error())
        continue
    print(msg.value().decode())
```

To run such code you need a working broker — there isn't one in the sandbox, so we model streams locally and use the Kafka code as a blueprint for real infrastructure.

## Mini-Batching

Another approach is mini-batching: accumulate events for a short time (for example, 1 second) and process them in a batch. It's the golden middle between pure streams and batches: processing in batches is more efficient, while latency stays small. Now practice.

<!--TASK-->
### Task 1
Create a file `stream_intro.py`. Write a generator `event_stream()` that infinitely yields dictionary events: `{"id": number, "city": random city, "temp": random temperature from 15 to 30}`. Use `itertools.islice` to take the first 10 events and print them. Then transform the stream: add a `fahrenheit` field to each event using the formula `temp * 9/5 + 32`, with a generator expression, and print the first 3 results.

### Task 2
Implement the `WindowAvg` class from the theory in `stream_utils.py` (task 4 will test it). Then write a script: create `WindowAvg(5)`, feed it the numbers from 1 to 10 (via `push`), print all returned values. Verify that the first four returns are `None`, and the fifth is `3.0` (the mean of 1..5).

### Task 3
Write a class `CityAggregator` in `stream_utils.py`: the `handle(event)` method takes an event with `city` and `temp` fields and accumulates statistics per city; the `result()` method returns a dictionary `{city: average_temperature}`. Then write a script that feeds the aggregator three events — "moscow" with temperature 20, "moscow" with 30, and "spb" with 10 — and prints the result: `{"moscow": 25.0, "spb": 10.0}`.

### Task 4
Write pytest tests for `WindowAvg` and `parse_event`. In `test_stream_utils.py` check: (1) `WindowAvg(3)` on [10, 20, 30, 40] returns `[None, None, 20.0, 30.0]`; (2) `WindowAvg(2)` on [1, 2, 3] returns `[None, 1.5, 2.5]`; (3) `parse_event` correctly parses the line `ts=...|city=moscow|temp=23.5`; (4) `parse_event("")` returns `{}`. Run pytest.

### Task 5
Write pytest tests for `CityAggregator`. In `test_stream_utils.py` check: (1) on the three events from task 3 the result equals `{"moscow": 25.0, "spb": 10.0}`; (2) an empty aggregator returns `{}`; (3) after adding one more "moscow" event with temperature 35, the average for moscow should become 28.333... (use `pytest.approx`); (4) an event without a `temp` field is ignored (doesn't raise an exception). Run pytest and get a green run.
<!--/TASK-->

<!--HINT-->
### Hint 1
A generator with an infinite `while True` + `yield`. For the number use a counter variable. `itertools.islice(stream, 10)` — the first 10. Transformation: `({"fahrenheit": e["temp"] * 9/5 + 32, **e} for e in stream)` then `islice(..., 3)`.

### Hint 2
`deque(maxlen=size)` — you don't need to check the length by hand: on overflow the oldest element falls out by itself. Return `None` while the length is less than `size`, otherwise the mean.

### Hint 3
Store `{city: [sum, count]}` in a dictionary. In `handle` update the sum and the counter. In `result` compute the mean for each city. Ignore events without `city` or `temp`.

### Hint 4
In the `WindowAvg` test simply collect the results of the `push` calls into a list and compare with the expected value. For `parse_event("")` — the loop over `"".split("|")` gives `[""]`, and `partition("=")` returns `("", "", "")` — you need to handle the empty string via `if not part: continue`.

### Hint 5
`pytest.approx(28.333, abs=0.01)` for floating-point precision. For ignoring an event without `temp` — in `handle` check `if "temp" not in event: return`. Add a test with such an event to make sure no exception is raised.
<!--/HINT-->

<!--SOLUTION-->
### Walkthrough 1
Solution:

```python
import itertools
import random

def event_stream():
    i = 0
    while True:
        yield {"id": i, "city": random.choice(["moscow", "spb", "kazan"]),
               "temp": round(random.uniform(15, 30), 1)}
        i += 1

stream = event_stream()
for e in itertools.islice(stream, 10):
    print(e)

with_fahrenheit = ({"fahrenheit": round(e["temp"] * 9 / 5 + 32, 1), **e}
                   for e in event_stream())
for e in itertools.islice(with_fahrenheit, 3):
    print(e)
```

Output: ten dictionary events, then three events with an extra `fahrenheit` field. What's happening here? `event_stream` is an infinite generator: memory isn't spent storing all events. `itertools.islice` "cuts" the stream. The generator expression transforms each event on the fly — this is the analog of map in streaming. Note the order `{"fahrenheit": ..., **e}`: it puts `fahrenheit` first in the dictionary.

### Walkthrough 2
Solution:

```python
from collections import deque

class WindowAvg:
    def __init__(self, size: int):
        self.size = size
        self.window = deque(maxlen=size)

    def push(self, value: float):
        self.window.append(value)
        if len(self.window) == self.size:
            return sum(self.window) / self.size
        return None

avg = WindowAvg(5)
for v in range(1, 11):
    print(avg.push(v))
```

Output: `None, None, None, None, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0`. What's happening here? `deque(maxlen=5)` automatically discards the oldest element on overflow — the code becomes simpler. The window "warms up": until 5 values have accumulated there is no mean, so `None` is returned. Starting from the 5th element we see the rolling mean of the last five numbers. Such a class is a typical fragment of any windowed aggregator.

### Walkthrough 3
Solution:

```python
class CityAggregator:
    def __init__(self):
        self.stats = {}

    def handle(self, event: dict):
        if "city" not in event or "temp" not in event:
            return
        city = event["city"]
        s = self.stats.setdefault(city, [0.0, 0])
        s[0] += event["temp"]
        s[1] += 1

    def result(self) -> dict:
        return {city: total / n for city, (total, n) in self.stats.items()}

agg = CityAggregator()
agg.handle({"city": "moscow", "temp": 20.0})
agg.handle({"city": "moscow", "temp": 30.0})
agg.handle({"city": "spb", "temp": 10.0})
print(agg.result())
```

Output: `{'moscow': 25.0, 'spb': 10.0}`. What's happening here? The aggregator accumulates the sum and count for each city. `setdefault(city, [0.0, 0])` creates an entry at the city's first appearance. `result()` computes the means at the moment of the call. This is an example of stateful processing: the state lives in the object and is updated with every event.

### Walkthrough 4
Solution:

```python
import pytest
from stream_utils import WindowAvg, parse_event

def test_window_avg_size_3():
    avg = WindowAvg(3)
    assert [avg.push(v) for v in [10, 20, 30, 40]] == [None, None, 20.0, 30.0]

def test_window_avg_size_2():
    avg = WindowAvg(2)
    assert [avg.push(v) for v in [1, 2, 3]] == [None, 1.5, 2.5]

def test_parse_event():
    event = parse_event("ts=2024-01-01T00:00:01Z|city=moscow|temp=23.5")
    assert event == {"ts": "2024-01-01T00:00:01Z", "city": "moscow", "temp": "23.5"}

def test_parse_event_empty():
    assert parse_event("") == {}
```

What's happening here? The first two tests check the window's boundary behavior: before it's filled — `None`, then the mean of the last `size` values. The `parse_event` test checks line parsing, and an empty string returns an empty dictionary (this requires handling empty parts in `parse_event`: `parts = [p for p in line.split("|") if p]`). Such tests catch regressions when refactoring the parser.

### Walkthrough 5
Solution:

```python
import pytest
from stream_utils import CityAggregator

def test_aggregator_basic():
    agg = CityAggregator()
    agg.handle({"city": "moscow", "temp": 20.0})
    agg.handle({"city": "moscow", "temp": 30.0})
    agg.handle({"city": "spb", "temp": 10.0})
    assert agg.result() == {"moscow": 25.0, "spb": 10.0}

def test_aggregator_empty():
    assert CityAggregator().result() == {}

def test_aggregator_updates():
    agg = CityAggregator()
    agg.handle({"city": "moscow", "temp": 20.0})
    agg.handle({"city": "moscow", "temp": 30.0})
    agg.handle({"city": "moscow", "temp": 35.0})
    assert agg.result()["moscow"] == pytest.approx(28.333, abs=0.01)

def test_aggregator_ignores_bad_event():
    agg = CityAggregator()
    agg.handle({"city": "moscow"})   # no temp
    agg.handle({"temp": 10.0})       # no city
    assert agg.result() == {}
```

What's happening here? The first test is the reference from task 3. The second is the empty state. The third checks mean recomputation when new events arrive: `(20 + 30 + 35) / 3 = 28.333...`, and for floating point we use `pytest.approx`. The fourth makes sure "broken" events are ignored rather than raising an exception — important for the robustness of stream processors against dirty data. Run: `pytest test_stream_utils.py -v`.
<!--/SOLUTION-->

<!--QUIZ-->
What is streaming?
- Processing a continuous stream of events as they arrive
- Reading a whole file
- Batch SQL processing
* Correct answer: Processing a continuous stream of events as they arrive
Streaming works with infinite streams, not with ready files.

What does an event generator return?
- One event per iteration
- All events at once
- A file with events
* Correct answer: One event per iteration
Generators yield events lazily, saving memory.

How do you take the first 10 events from an infinite stream?
- itertools.islice(stream, 10)
- stream[:10]
- list(stream)[:10]
* Correct answer: itertools.islice(stream, 10)
islice works with generators; slice works only with sequences.

What does collections.deque(maxlen=5) do?
- Keeps at most 5 latest elements, evicting old ones
- Sorts elements
- Forbids adding more than 5 elements
* Correct answer: Keeps at most 5 latest elements, evicting old ones
This is the ideal structure for a sliding window.

What is a window in streaming?
- A segment of the stream over which an aggregate is computed
- An event type
- A buffer on disk
* Correct answer: A segment of the stream over which an aggregate is computed
A window defines which events participate in aggregation.

What is a topic in Kafka?
- A named stream of messages
- A cluster of servers
- A data format
* Correct answer: A named stream of messages
A topic is a message queue read by consumers.

What is a partition in Kafka?
- A part of a topic — an ordered queue of messages
- A copy of a topic
- A broker server
* Correct answer: A part of a topic — an ordered queue of messages
Partitions allow scaling reads.

What is a consumer group?
- A set of processes reading a topic together: each message is processed by one member
- A single reading process
- A group of topics
* Correct answer: A set of processes reading a topic together: each message is processed by one member
This splits the load among consumers.

Which delivery semantics guarantees no losses?
- at-least-once
- at-most-once
- best-effort
* Correct answer: at-least-once
With at-least-once a message is delivered at least once, but duplicates are possible.

What is an offset?
- The number of a message inside a partition
- The size of a message
- The read speed
* Correct answer: The number of a message inside a partition
An offset lets a consumer resume reading from the right place.

<!--/QUIZ-->
