---
title: Prometheus and Grafana
summary: Exporters, queries, dashboards.
order: 2
duration: 50 min
difficulty: advanced
tags: prometheus, grafana
---

Prometheus collects metrics; Grafana shows them.

## Python metrics

```python
from prometheus_client import Counter, start_http_server
import time

REQUESTS = Counter("http_requests_total", "Requests")
start_http_server(8000)

while True:
    REQUESTS.inc()
    time.sleep(1)
```

## PromQL

```promql
rate(http_requests_total[5m])
```

## Grafana

Add Prometheus as data source, build panels.

## Lesson summary

Expose metrics → scrape → visualize.

<!--TASK-->
### Task 1 — Counter
Create and increment a Counter.

### Task 2 — Server
Start the metrics server.

### Task 3 — Histogram
Track request durations.

### Task 4 — PromQL
Rate query.

### Task 5 — Source
Connect Grafana.

### Task 6 — Panel
Build a panel.

### Task 7 — Alert
Set an alert rule.
<!--/TASK-->

<!--HINT-->
### Hint 1
Counter.

### Hint 2
start_http_server.

### Hint 3
Histogram.

### Hint 4
rate().

### Hint 5
Data source.

### Hint 6
Query.

### Hint 7
Threshold.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from prometheus_client import Counter
REQUESTS = Counter("http_requests_total", "Requests")
REQUESTS.inc()
```

### Solution 2
```python
from prometheus_client import start_http_server
start_http_server(8000)
# http://localhost:8000/metrics
```

### Solution 3
```python
from prometheus_client import Histogram
REQUEST_TIME = Histogram("request_duration_seconds", "Request time")
REQUEST_TIME.observe(0.05)
```

### Solution 4
```promql
rate(http_requests_total[5m])
```

### Solution 5
```text
Grafana → Configuration → Data sources →
Prometheus → URL: http://localhost:9090
```

### Solution 6
```text
New dashboard → Add panel → выбрать PromQL-запрос
→ сохранить
```

### Solution 7
```text
Alert rule: avg(rate(...)) > 5 за 5 минут
→ уведомление
```
<!--/SOLUTION-->

<!--QUIZ-->
What is Prometheus?
- Metrics system
- Logs
- Traces
- None
* Correct answer: Metrics system
Scrape.

What is a Counter?
- Increasing total
- Gauge
- Histogram
- None
* Correct answer: Increasing total
Requests.

What is a Gauge?
- Current value
- Total
- Distribution
- None
* Correct answer: Current value
CPU.

What is a Histogram?
- Durations
- Count
- Value
- None
* Correct answer: Durations
Buckets.

What is start_http_server?
- Exposes metrics
- Collects
- Plots
- None
* Correct answer: Exposes metrics
/metrics.

What is PromQL?
- Query language
- SQL
- Python
- None
* Correct answer: Query language
rate.

What is rate?
- Per-second
- Total
- Max
- None
* Correct answer: Per-second
Over time.

What is a data source?
- Metrics origin
- Panel
- Alert
- None
* Correct answer: Metrics origin
Prometheus.

What is a panel?
- Chart block
- Query
- Source
- None
* Correct answer: Chart block
Dashboard.

What is an alert?
- Condition
- Metric
- Panel
- None
* Correct answer: Condition
Notify.

What is scrape?
- Periodic fetch
- Push
- Plot
- None
* Correct answer: Periodic fetch
Endpoint.

What is a target?
- Endpoint
- Query
- Panel
- None
* Correct answer: Endpoint
App.
<!--/QUIZ-->
