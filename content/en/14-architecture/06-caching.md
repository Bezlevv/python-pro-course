---
title: Caching and strategies
summary: Cache-Aside, TTL, invalidation.
order: 6
duration: 40 min
difficulty: advanced
tags: caching, ttl
---

Caching stores hot data close to the app.

## Cache-Aside

```python
import time

cache = {}
TTL = 60

def get_user(user_id):
    now = time.time()
    entry = cache.get(user_id)
    if entry and now - entry["ts"] < TTL:
        return entry["data"]
    data = load_from_db(user_id)   # долго
    cache[user_id] = {"data": data, "ts": now}
    return data
```

## Strategies

- Cache-Aside: app manages cache;
- Write-Through: write to cache + db;
- TTL: expiry.

## Lesson summary

Cache hot reads; keep TTL and invalidation.

<!--TASK-->
### Task 1 — Dict cache
Implement get_user with cache.

### Task 2 — TTL
Add expiry checking.

### Task 3 — Invalidate
Delete on update.

### Task 4 — Hit/miss
Count hits and misses.

### Task 5 — Why
Why cache?

### Task 6 — Stale
Explain stale data.

### Task 7 — Key
Design cache keys.
<!--/TASK-->

<!--HINT-->
### Hint 1
dict.

### Hint 2
time.

### Hint 3
pop.

### Hint 4
Counters.

### Hint 5
Speed.

### Hint 6
Old.

### Hint 7
f"user:{id}".
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
cache = {}
def get_user(user_id):
    if user_id in cache:
        return cache[user_id]
    data = load_from_db(user_id)
    cache[user_id] = data
    return data
```

### Solution 2
```python
import time
TTL = 60
def get_user(user_id):
    now = time.time()
    entry = cache.get(user_id)
    if entry and now - entry["ts"] < TTL:
        return entry["data"]
    data = load_from_db(user_id)
    cache[user_id] = {"data": data, "ts": now}
    return data
```

### Solution 3
```python
def update_user(user_id, data):
    save_to_db(user_id, data)
    cache.pop(user_id, None)   # инвалидация
```

### Solution 4
```python
hits = misses = 0
if entry and fresh:
    hits += 1
else:
    misses += 1
```

### Solution 5
```python
# Повторные запросы отдаются мгновенно,
# снижается нагрузка на БД
```

### Solution 6
```python
# Stale: кэш хранит устаревшие данные
# после обновления в БД (нужна инвалидация)
```

### Solution 7
```python
# f"user:{id}" — по сущности
# f"feed:{user_id}:{page}" — по комплексу
```
<!--/SOLUTION-->

<!--QUIZ-->
What is caching?
- Storing hot data
- Deleting
- Sorting
- None
* Correct answer: Storing hot data
Fast.

What is a cache hit?
- Found in cache
- Miss
- Error
- None
* Correct answer: Found in cache
Fast.

What is a miss?
- Not found
- Found
- Error
- None
* Correct answer: Not found
Load.

What is TTL?
- Time to live
- Total time
- Test
- None
* Correct answer: Time to live
Expiry.

What is invalidation?
- Removing stale
- Adding
- Sorting
- None
* Correct answer: Removing stale
Update.

What is stale?
- Outdated
- Fresh
- Empty
- None
* Correct answer: Outdated
Problem.

What is Cache-Aside?
- App manages cache
- DB manages
- None
- Always
* Correct answer: App manages cache
Pattern.

What is the benefit?
- Lower latency
- Higher cost
- Complexity
- None
* Correct answer: Lower latency
Load.

What is a key?
- Identifier
- Value
- Type
- None
* Correct answer: Identifier
user:1.

What is hot data?
- Frequently read
- Rare
- New
- None
* Correct answer: Frequently read
Cache.

What is Redis?
- Cache store
- Database
- Framework
- None
* Correct answer: Cache store
In-memory.

What is write-through?
- Writes to cache + db
- Cache only
- Db only
- None
* Correct answer: Writes to cache + db
Strategy.
<!--/QUIZ-->
