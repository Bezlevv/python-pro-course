---
title: Observability basics
summary: Logs, metrics, traces.
order: 1
duration: 40 min
difficulty: advanced
tags: observability
---

Observability shows what the system does.

## Three pillars

- Logs: events;
- Metrics: numbers over time;
- Traces: request paths.

## Tools

Prometheus + Grafana, OpenTelemetry, Sentry.

## Lesson summary

Logs + metrics + traces = full picture.

<!--TASK-->
### Task 1 — Logs
Define.

### Task 2 — Metrics
Define.

### Task 3 — Traces
Define.

### Task 4 — Tools
Name two tools.

### Task 5 — Why
Why not only logs?

### Task 6 — Alert
Alert example.

### Task 7 — Start
Where to start?
<!--/TASK-->

<!--HINT-->
### Hint 1
Events.

### Hint 2
Numbers.

### Hint 3
Path.

### Hint 4
Prometheus.

### Hint 5
Context.

### Hint 6
Threshold.

### Hint 7
Centralize.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```text
Логи — записи событий с временем и уровнем
```

### Solution 2
```text
Метрики — числовые показатели: ошибки,
задержки, нагрузка
```

### Solution 3
```text
Трейсы — путь запроса через сервисы
с таймингами
```

### Solution 4
```text
Prometheus + Grafana, OpenTelemetry, Sentry, ELK
```

### Solution 5
```text
Логи без метрик не отвечают «как много»;
без трейсов — «где именно»
```

### Solution 6
```text
«Error rate > 5% за 5 минут» → уведомление
```

### Solution 7
```text
Начать со сбора логов и основных метрик
(ошибки, время ответа), затем добавить трейсы
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a log?
- Event record
- Number
- Path
- None
* Correct answer: Event record
Time.

What is a metric?
- Measurement
- Event
- Trace
- None
* Correct answer: Measurement
Numbers.

What is a trace?
- Request path
- Event
- Metric
- None
* Correct answer: Request path
Spans.

What is Prometheus?
- Metrics collector
- Logger
- Browser
- None
* Correct answer: Metrics collector
TSDB.

What is Grafana?
- Dashboards
- Logs
- Traces
- None
* Correct answer: Dashboards
Charts.

What is a dashboard?
- Visual panel
- Alert
- Log
- None
* Correct answer: Visual panel
Grafana.

What is an alert?
- Threshold trigger
- Log
- Metric
- None
* Correct answer: Threshold trigger
Notify.

What is latency?
- Delay
- Error
- Load
- None
* Correct answer: Delay
Time.

What is error rate?
- Failures %
- Success
- Load
- None
* Correct answer: Failures %
Health.

What is OpenTelemetry?
- Standard
- A database
- A browser
- None
* Correct answer: Standard
Traces.

What is a span?
- Trace segment
- Log
- Metric
- None
* Correct answer: Trace segment
Service.

What is the goal?
- Understanding
- Speed
- Style
- None
* Correct answer: Understanding
Debug.
<!--/QUIZ-->
