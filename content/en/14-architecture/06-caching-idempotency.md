---
title: Caching and Idempotency
summary: Caching strategies (cache-aside, TTL, write-through), protection against stampedes and avalanches, idempotent operations and idempotency keys.
order: 6
duration: 45 min
difficulty: advanced
tags: cache, idempotency, ttl, cache-aside, stampede, retry
---

Caching and idempotency are two techniques that make systems fast and reliable under load. The first speeds up reads; the second protects against double payments and repeated requests.

## Caching: the cache-aside pattern

The most common pattern is **cache-aside** (lazy caching): first look in the cache; if it's there (hit) — return it; if not (miss) — read from the database, put it in the cache, and return it. In Python it's easy to demonstrate with a dict as the "cache":

```python
import time

class Cache:
    def __init__(self, ttl=5.0):
        self.store = {}
        self.ttl = ttl

    def get(self, key):
        item = self.store.get(key)
        if item is None:
            return None
        value, expires_at = item
        if time.time() > expires_at:
            del self.store[key]
            return None
        return value

    def set(self, key, value):
        self.store[key] = (value, time.time() + self.ttl)
```

TTL (time-to-live) guarantees that data expires even without explicit invalidation.

The cache-aside scheme for a database:

```python
def get_user(user_id, cache, db):
    key = f"user:{user_id}"
    cached = cache.get(key)
    if cached is not None:
        return cached
    row = db.get(user_id)          # heavy query
    if row is not None:
        cache.set(key, row)
    return row
```

## Write-through and write-back

Besides cache-aside there are write strategies. **Write-through**: on a database write, immediately write to the cache too — the cache is always fresh, but writes are more expensive. **Write-back**: write only to the cache and flush to the database asynchronously — fast, but there's a risk of losing data on a crash. For most cases cache-aside + TTL is enough.

## Stampede and avalanche

- **Cache stampede**: a key expires, and dozens of requests fall through to the database at once. Fixed with "single flight" — only one thread goes to the database, the rest wait for its result.
- **Cache avalanche**: massive simultaneous key expiration — all requests hit the database. Fixed with TTL jitter (a small random deviation) and pre-warming.

Single flight in a single process is simply a lock:

```python
import threading

lock = threading.Lock()
inflight = {}

def get_or_load(key, load):
    with lock:
        if key in inflight:
            return inflight[key]
        inflight[key] = load()
    return inflight[key]
```

(In multi-process systems, distributed locks are used, e.g., on Redis.)

## Idempotency

An idempotent operation is one that can be performed several times with the same result as performing it once. In HTTP these are `GET`, `PUT`, `DELETE`. But `POST` (creation) is not idempotent: a double click on the "Pay" button creates two payments.

The solution is an **idempotency key**: the client sends a unique `Idempotency-Key` in the header; the server remembers the key and the result of the first processing, and for a repeated request with the same key returns the stored result:

```python
class IdempotentHandler:
    def __init__(self):
        self.results = {}

    def handle(self, key, operation):
        if key in self.results:
            return self.results[key], "repeat"
        result = operation()
        self.results[key] = result
        return result, "first"
```

Duplicates can also be recognized by a business attribute (e.g., `order_id` in the request body), but a key is the most general mechanism. The main rule: the key must be unique for a logical operation, and responses must be stored long enough to cover the window of repeated requests.

<!--TASK-->
### Task 1
Implement cache-aside with TTL. Write a class `Cache` (as in the theory) and a function `get_user(user_id, cache, db)`, where `db` is a "database" dict of users. The first request should go to the database (print `DB: user 1`), the second from the cache (print `Cache: user 1`). To verify, put the user `{1: {"name": "Anya"}}` into `db`. Expected output: first the line `DB: user 1`, then `Cache: user 1`.

### Task 2
Implement cache stampede protection (single flight). Write a function `single_flight(key, load, lock, inflight)`, where `inflight` is an "in-flight" dict and `lock` is a `threading.Lock()`. The function should: if `key` is already in `inflight` — return its result; otherwise run `load()` (prints `Loading...`), save the result and return it. Call it twice with the same key — `Loading...` must print exactly once. Expected output: `Loading...` and `42` twice (lines: `Loading...`, `Result: 42`, `Result: 42`).

### Task 3
Make a write-through cache. The class `WriteThroughCache` takes `cache` and `db`; method `set(key, value)` writes to both the database and the cache; method `get(key)` reads from the cache. Verify: `set("user:1", {"name": "Anya"})`, then `get("user:1")`, then check directly that the value is in `db`. Expected output: `From cache: {'name': 'Anya'}` and `In DB: {'name': 'Anya'}`.

### Task 4
Implement an idempotent payment handler. The class `PaymentHandler` with a key in the style of `IdempotentHandler` (as in the theory): method `charge(key, amount)` returns the tuple `(result, tag)`, where `tag` is `"first"` or `"repeat"`. Both calls with the same key must return the same result (e.g., `{"status": "ok", "amount": 100}`), but the second call's tag is `"repeat"`. Expected output: `first`, `repeat`.

### Task 5
Implement a cache with TTL jitter to protect against avalanches. The class `JitterCache` inherits from `Cache` from task 1, but in `set` adds a random number from 0 to `jitter` (0.5) to the TTL. Write a check: create a cache with `ttl=1.0`, `jitter=0.5`, put a key and print `store[key]` — the value should be stored with an `expires_at` greater than `time.time()`, and the difference between `expires_at` and `time.time()` should be between 1.0 and 1.5. Expected output: `True` (range check).
<!--/TASK-->

<!--HINT-->
### Hint 1
In `get_user` print `DB: user {user_id}` before accessing `db` and `Cache: user {user_id}` on a hit. Store data in `db`, and in `cache` — only after the first read. Don't forget `import time` for TTL.

### Hint 2
`single_flight` should work like this: `with lock: if key in inflight: return inflight[key]`; otherwise `result = load(); with lock: inflight[key] = result; return result`. The lambda `load` prints `Loading...` and returns 42. The second call should return 42 without loading again.

### Hint 3
Method `set` immediately writes to `cache.store[key]` (can be without TTL) and to `db[key]`. Method `get` returns `self.cache.get(key)`. To check the database, print `db` directly.

### Hint 4
In `charge` check `if key in self.results: return self.results[key], "repeat"`; otherwise perform the payment (just return a dict), store it in `self.results[key]` and return `(result, "first")`.

### Hint 5
In `set` override: `expires_at = time.time() + self.ttl + random.uniform(0, self.jitter)`. Check: `now = time.time()`; extract `expires_at` from `cache.store["k"]`; print `1.0 <= expires_at - now <= 1.5`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
import time

class Cache:
    def __init__(self, ttl=5.0):
        self.store = {}
        self.ttl = ttl

    def get(self, key):
        item = self.store.get(key)
        if item is None:
            return None
        value, expires_at = item
        if time.time() > expires_at:
            del self.store[key]
            return None
        return value

    def set(self, key, value):
        self.store[key] = (value, time.time() + self.ttl)

def get_user(user_id, cache, db):
    key = f"user:{user_id}"
    cached = cache.get(key)
    if cached is not None:
        print(f"Cache: {key}")
        return cached
    print(f"DB: {key}")
    row = db.get(user_id)
    if row is not None:
        cache.set(key, row)
    return row

db = {1: {"name": "Anya"}}
cache = Cache()
get_user(1, cache, db)
get_user(1, cache, db)
```

Output:

```
DB: user 1
Cache: user 1
```

What's happening here? The first call misses the cache, reads the database and puts the result into the cache. The second hits the cache. So the database gets only one heavy query instead of two — that's the essence of cache-aside.

### Solution 2
Solution:

```python
import threading

lock = threading.Lock()
inflight = {}

def single_flight(key, load, lock, inflight):
    with lock:
        if key in inflight:
            return inflight[key]
    result = load()
    with lock:
        inflight[key] = result
    return result

def load():
    print("Loading...")
    return 42

r1 = single_flight("user:1", load, lock, inflight)
r2 = single_flight("user:1", load, lock, inflight)
print(f"Result: {r1}")
print(f"Result: {r2}")
```

Output:

```
Loading...
Result: 42
Result: 42
```

What's happening here? The first call runs `load()` once; the second finds the key in `inflight` and immediately returns the stored result. Even if 50 requests arrive at once after a cache expiration, only one hits the database — that's stampede protection.

### Solution 3
Solution:

```python
class WriteThroughCache:
    def __init__(self, cache, db):
        self.cache = cache
        self.db = db

    def set(self, key, value):
        self.cache.store[key] = (value, float("inf"))
        self.db[key] = value

    def get(self, key):
        return self.cache.get(key)

db = {}
cache = Cache()
wt = WriteThroughCache(cache, db)
wt.set("user:1", {"name": "Anya"})
print(f"From cache: {wt.get('user:1')}")
print(f"In DB: {db['user:1']}")
```

Output:

```
From cache: {'name': 'Anya'}
In DB: {'name': 'Anya'}
```

What's happening here? Write-through writes to both places at once: the cache is always fresh after a write, and the database doesn't diverge from the cache. The cost — each write costs a database write plus a cache write.

### Solution 4
Solution:

```python
class PaymentHandler:
    def __init__(self):
        self.results = {}

    def charge(self, key, amount):
        if key in self.results:
            return self.results[key], "repeat"
        result = {"status": "ok", "amount": amount}
        self.results[key] = result
        return result, "first"

handler = PaymentHandler()
print(handler.charge("pay-42", 100)[1])
print(handler.charge("pay-42", 100)[1])
```

Output:

```
first
repeat
```

What's happening here? The first call performs the payment and stores the result under the key `pay-42`. The second with the same key doesn't charge again but returns the same result with the tag `repeat`. This protects against double payment on network retries or a double click.

### Solution 5
Solution:

```python
import time
import random

class JitterCache(Cache):
    def __init__(self, ttl=5.0, jitter=0.5):
        super().__init__(ttl)
        self.jitter = jitter

    def set(self, key, value):
        self.store[key] = (value, time.time() + self.ttl + random.uniform(0, self.jitter))

cache = JitterCache(ttl=1.0, jitter=0.5)
cache.set("k", "v")
expires_at = cache.store["k"][1]
now = time.time()
print(1.0 <= expires_at - now <= 1.5)
```

Output: `True`. What's happening here? Each key gets its own slightly different lifetime: keys expire not simultaneously but "smeared" across an interval. This reduces the chance of an avalanche, when all keys expire at once and the database takes a hit from all requests simultaneously.
<!--/SOLUTION-->

<!--QUIZ-->
What happens on a cache miss in cache-aside?
- An error is returned
- Data is read from the database and put into the cache
- The cache is cleared
- The request is ignored
* Correct answer: Data is read from the database and put into the cache
After reading from the database, the result is stored in the cache with a TTL.

Why is TTL needed?
- So keys expire automatically
- To speed up writes
- To forbid reads
- To find keys
* Correct answer: So keys expire automatically
TTL guarantees that stale data doesn't live forever.

What is a cache stampede?
- All keys expire at the same time
- Many requests fall through to the database at once after a key expires
- A slow network
- A bug in the code
* Correct answer: Many requests fall through to the database at once after a key expires
Single flight helps against this — only one thread loads the data.

Which HTTP method is idempotent?
- POST
- GET
- PATCH (generally no)
- None
* Correct answer: GET
GET, PUT and DELETE can safely be repeated; POST can't.

What does an idempotency key do?
- Lets the server recognize a repeated request and return the stored result
- Encrypts the request
- Speeds up the database
- Changes the HTTP method
* Correct answer: Lets the server recognize a repeated request and return the stored result
A repeated payment with the same key doesn't charge twice.

How do you protect against an avalanche?
- Add jitter to TTL and pre-warm keys
- Remove the cache entirely
- Increase the database tenfold
- Disable TTL
* Correct answer: Add jitter to TTL and pre-warm keys
Keys expire at staggered times, and the database load is spread out.

What is a cache avalanche?
- Massive key expiration, when all the load falls on the database at once
- A single cache miss
- Cache memory overflow
- A slow network
* Correct answer: Massive key expiration, when all the load falls on the database at once
TTL jitter, key pre-warming, and a fallback cache save you from avalanches.

What is a write-through cache?
- On write, data is immediately written to both the cache and the database
- Data is written only to the database
- Data is written only to the cache
- The cache updates once a minute
* Correct answer: On write, data is immediately written to both the cache and the database
Write-through guarantees cache freshness but makes writes more expensive.
<!--/QUIZ-->
