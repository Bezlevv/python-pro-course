---
title: System Design
summary: What a system design interview consists of: requirements, load estimation, components, caching, queues, databases, and rate limiting.
order: 4
duration: 50 min
difficulty: advanced
tags: system design, architecture, scalability, cache, redis, queues
---

System design is designing the architecture of a service that will withstand real-world load. At the interview you'll get a task like "design a URL shortener service", and the interviewer watches not exact numbers but your line of thinking: can you gather requirements, estimate scale, and make sound decisions.

## Answer framework

A good answer proceeds step by step:

1. **Requirements**: functional (what the system does) and non-functional (how many users, what latency, availability).
2. **Scale estimation**: how many requests per second (QPS), how much data to store, what traffic is needed.
3. **High-level design**: components (client, load balancer, servers, DB, cache, queues) and the request flow.
4. **Details**: storage, caching, rate limiting, fault tolerance.
5. **Optimizations**: what the bottleneck is and how to remove it.

## Key concepts

- **Scalability**: horizontal (adding machines) and vertical (making one machine more powerful).
- **Availability and consistency**: the CAP theorem says a distributed system cannot simultaneously guarantee consistency (C), availability (A), and partition tolerance (P). In practice, P is almost always chosen, and between C and A it's a trade-off.
- **Load balancer** distributes requests across servers.
- **CDN** — a network that delivers static content (images, CSS, JS) closer to the user.
- **Cache** (Redis) keeps frequently read data in memory — reads are tens of times faster than from a DB.
- **Queues** (RabbitMQ, Kafka) decouple components: the system doesn't crash if a consumer service is temporarily unavailable.
- **Databases**: SQL (PostgreSQL, MySQL) — transactions, complex queries, relations; NoSQL (MongoDB, Cassandra) — flexible schemas, horizontal scaling.
- **Sharding** — splitting data across several servers by a key (for example, by user_id).
- **Replication** — data copies (primary — secondaries) for fault tolerance.
- **Rate limiting** — limiting the number of requests (anti-spam, overload protection).

## Common mistakes

- Staying silent and waiting for the interviewer to ask a question.
- Diving into details of one component immediately, forgetting the big picture.
- Naming technologies without explaining why they're needed.
- Ignoring failures: "what if the server dies?" is a mandatory question.

## Example: a URL shortener service

The request flow: client → load balancer → application server → Redis cache (check) → DB. A short code is generated when the link is created and stored along with the long URL; when the link is visited, the server finds the long URL and returns a redirect. Popular links are cached, so hot visits don't hammer the DB.

## Summary

System design is a trainable skill. Walk through the "requirements → estimation → diagram → details" plan on three or four examples, and you'll learn to speak this language confidently.

<!--TASK-->
### Task 1
Estimate the scale for a URL shortener service. Suppose there are 10 million daily active users (DAU), 20% of them create at least one link a day, and each active user makes on average 10 link visits a day. Calculate: how many new links are created per second on average (with 100,000 seconds per day), how many visits per second on average, how many links accumulate in a year, and what storage volume is needed if one record takes about 200 bytes. Show all the calculations.

### Task 2
Design a component-level diagram of a URL shortener service. Describe in text (or as a diagram made of text blocks) the client, load balancer, application server, cache, and database, then describe two flows: creating a new link and visiting a short link. For each component, state its role in one sentence.

### Task 3
Choose a database type for the URL shortener: PostgreSQL or MongoDB. Justify the choice on four points: data structure, access pattern, transactions, scaling. Describe the table/collection schema: what fields a link record will have, and what index is needed for the most frequent query.

### Task 4
Design a rate limiting mechanism for the service API: a limit of 10 requests per second per user. Compare three algorithms: fixed window, sliding window, and token bucket. Choose one, describe its implementation in Redis, and explain what happens when the limit is exceeded.

### Task 5
Design caching for short-link visits. Describe what to store in Redis (key — value, TTL), the update strategy when a link is deleted, and estimate the hit ratio simply: suppose 20% of links account for 80% of visits, and they all fit in the cache. How many requests out of 100 will hit the DB with caching?

<!--/TASK-->

<!--HINT-->
### Hint 1
Calculate step by step: first how many links are created per day (10 million × 20%), then divide by 100,000 seconds. Visits: 10 million × 10 visits, divide by 100,000. Yearly accumulation is the daily count × 365. Volume is the number of records × 200 bytes — don't forget to convert to megabytes/gigabytes.

### Hint 2
Draw the request flow in words: the client goes to the load balancer, which hands the request to one of the application servers. The server first checks the cache and only goes to the DB on a miss. When creating a link, the server generates a short code, saves the record to the DB, and puts it in the cache. On a visit, it reads the cache, on a miss the DB, then returns a redirect.

### Hint 3
Link data is a rigid structure: short code (unique), long URL, creation date, visit counter. The access pattern is point reads by key. Transactions are needed on insert with uniqueness checking. Think about an index on the short code: it should be unique. Mongo would also work, but justify why PostgreSQL is more reliable for a transactional insert.

### Hint 4
Fixed window is simple but allows 20 requests at the moment the window changes. Sliding window is more precise: it accounts for exact request times. Token bucket allows short bursts: the bucket holds N tokens, each request takes one, and the bucket refills at N/10 tokens per second. In Redis it's convenient to store a counter with a TTL equal to the window length and use INCR + EXPIRE.

### Hint 5
The cache key will be the short code, the value the long URL, and the TTL, say, 24 hours so deleted links don't hang forever. If 20% of links account for 80% of visits and all fit in Redis, then 80 of 100 visits hit the cache, and only 20 go to the DB. Count percentages, not absolute numbers.

<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
DAU = 10_000_000
percent_creators = 0.20
transitions_per_active = 10
seconds_per_day = 100_000
record_size = 200

links_per_day = DAU * percent_creators            # 2 million links per day
links_per_sec = links_per_day / seconds_per_day   # 20 links/sec
transitions_per_sec = DAU * transitions_per_active / seconds_per_day  # 1000 transitions/sec
links_per_year = links_per_day * 365              # 730 million links
storage_per_year = links_per_year * record_size    # 146 billion bytes = 146 GB
print(f"New links per second: {links_per_sec:.0f}")
print(f"Transitions per second: {transitions_per_sec:.0f}")
print(f"Links per year: {links_per_year:,}")
print(f"Storage per year: {storage_per_year / 1e9:.1f} GB")
```

Output:

```
New links per second: 20
Transitions per second: 1000
Links per year: 730,000,000
Storage per year: 146.0 GB
```

What's going on here? We estimate orders of magnitude, not exact numbers: 20 links per second is trivial for any DB, and 1,000 transitions per second is an average load a single modern server handles. The main takeaway for the interview: the bottleneck is not the DB but code accuracy and caching. These estimates show you think in scale — that's the essence of design problems.

### Solution 2
Diagram:

```
Client (browser)
   │
   ▼
Load balancer (NGINX, HAProxy)
   │
   ▼
Application server (FastAPI/Django)
   │                    │
   ├──► Redis cache ◄────┘
   │       │
   │       └──► PostgreSQL database
   └──► PostgreSQL database
```

Creating a link: the client sends a POST with a long URL → load balancer → the application server generates a short code → inserts a record into PostgreSQL → puts the code and URL into Redis. Visiting: the client opens a short link → the server first looks for the code in Redis → on a miss reads PostgreSQL → returns a 302 redirect to the long URL.

What's going on here? Components are separated by responsibility: the load balancer distributes load, the application holds the logic, Redis speeds up reads, PostgreSQL is the source of truth. This is called high-level design: you showed the big picture without drowning in details and described the two main flows. Next, the interviewer will drill into whatever they want.

### Solution 3
Choose PostgreSQL. Justification:

1. **Data structure** — rigid: short code, long URL, creation date, counter. A tabular schema fits perfectly; fields don't change from record to record.
2. **Access pattern** — point reads by a unique key (short code). PostgreSQL supports a unique index, giving O(log n) search.
3. **Transactions** — creating a link must be atomic: insert with uniqueness checking of the code. PostgreSQL guarantees ACID.
4. **Scaling** — you can start with one replica, and as you grow, shard by code hash or switch to read replicas.

Table schema:

```sql
CREATE TABLE links (
    code VARCHAR(10) PRIMARY KEY,
    url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT now(),
    clicks BIGINT DEFAULT 0
);
```

What's going on here? Choosing a DB is a debate: both options work. The key to a good answer is justifying through requirements: a rigid schema, transactions, and point access pull toward PostgreSQL. A unique index on `code` answers the most frequent query (visiting a link). Such an answer shows you pick the tool for the task, not by fashion.

### Solution 4
Choice: token bucket. Implementation in Redis:

```python
import redis, time

r = redis.Redis()

def allow_request(user_id, bucket_size=10, refill=10, window=1):
    key = f"tb:{user_id}"
    # INCR increments the counter, EXPIRE sets a TTL on the window
    token = r.incr(key)
    if token == 1:
        r.expire(key, window)
    return token <= bucket_size
```

Algorithm descriptions:

- **Fixed window**: a counter per second. Simple, but at the window boundary a user can send 20 requests in a row (10 at the end of one second and 10 at the start of the next).
- **Sliding window**: we store request timestamps and count those falling within the last second. More precise, but more expensive in memory.
- **Token bucket**: a bucket of 10 tokens; each request takes a token, and the bucket refills at 10 tokens per second. Allows short bursts but smooths the average load.

When the limit is exceeded, the server returns HTTP 429 Too Many Requests with a `Retry-After` header. What's going on here? We chose token bucket for its flexibility (bursts) and simple implementation with `INCR` + `EXPIRE`. At the interview it's important to explain not only "what" but "why", and to mention behavior on exceeding the limit.

### Solution 5
Solution:

- Redis key: `link:{short_code}` → value: long URL; TTL: 24 hours.
- Update strategy: when a link is deleted, the application also deletes the record from Redis; when created, it puts it in the cache immediately. TTL protects against "stuck" keys if a deletion is missed.
- Hit ratio: 20% of links account for 80% of visits. If all these hot links fit in the cache, then of 100 visits, 80 are served by Redis, and 20 requests go to the DB. That reduces DB load 5-fold.

What's going on here? Caching hits exactly the hot spot: one Redis cuts 80% of traffic away from the DB. The miss probability drops further with "lazy" reads: on a miss, load the value from the DB and put it into the cache. At the interview, be sure to ask yourself: "what happens on a Redis restart?" — the answer: the DB will survive the misses while the cache warms up, and peak load is handled by request distribution.

<!--/SOLUTION-->

<!--QUIZ-->
What does the CAP theorem state?
- A distributed system cannot simultaneously guarantee consistency, availability, and partition tolerance
- Every system must be consistent
- Databases cannot be distributed
- Availability matters most
* Correct answer: A distributed system cannot simultaneously guarantee consistency, availability, and partition tolerance
CAP is about trade-offs: only two of the three properties are achievable at once.

What is a CDN for?
- To deliver static content closer to the user
- To store the entire database
- To balance load between servers
- To process payments
* Correct answer: To deliver static content closer to the user
A CDN caches images, CSS, and JS on servers worldwide, reducing latency.

Why are message queues needed?
- To decouple components and survive temporary service unavailability
- To speed up database reads
- To store static files
- To generate short links
* Correct answer: To decouple components and survive temporary service unavailability
Queues let processing be deferred: a message waits until the consumer is available again.

What is sharding?
- Splitting data across several servers by a key
- Copying data to a backup server
- Merging tables
- Optimizing SQL queries
* Correct answer: Splitting data across several servers by a key
Sharding distributes data horizontally, letting storage scale.

What code does a server return when a rate limit is exceeded?
- 429 Too Many Requests
- 200 OK
- 404 Not Found
- 500 Internal Server Error
* Correct answer: 429 Too Many Requests
Code 429 tells the client it exceeded the request limit.

Why cache frequently read data?
- Memory reads are orders of magnitude faster than DB reads
- To save on licenses
- To simplify the database schema
- To avoid writing indexes
* Correct answer: Memory reads are orders of magnitude faster than DB reads
A cache like Redis keeps data in RAM, so responses arrive in milliseconds.

What does a load balancer do?
- Distributes incoming requests across several servers
- Stores data copies
- Encrypts traffic
- Serves DNS requests
* Correct answer: Distributes incoming requests across several servers
A load balancer improves availability and scalability by routing traffic to healthy nodes.

What is horizontal scaling?
- Adding new servers instead of making one more powerful
- Increasing the power of a single machine
- Switching to another database
- Reducing load
* Correct answer: Adding new servers instead of making one more powerful
Horizontal scaling usually requires sharding and distributed state.

<!--/QUIZ-->
