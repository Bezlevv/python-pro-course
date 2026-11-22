---
title: Exam: observability and operations
summary: Final module assessment: structured logging, OpenTelemetry, Prometheus, Sentry, healthchecks.
order: 99
duration: 30 min
difficulty: advanced
exam: true
tags: exam, observability, logs, tracing, metrics, sentry, healthcheck
---

<!--QUIZ-->
What is a structured log?
- A text line with a time
- A record in a machine-readable format (JSON) with separate fields
- A log sorted by date
* Correct answer: A record in a machine-readable format (JSON) with separate fields
JSON logs allow filtering by fields and automatic processing.

Why is contextvars.ContextVar needed in logging?
- To store a value relevant to the current context (correlation id)
- To speed up logging
- To serialize records
* Correct answer: To store a value relevant to the current context (correlation id)
ContextVar isolates the value within a request and does not leak between requests.

What is a span in OpenTelemetry?
- One log line
- One step of an operation inside a trace
- A metric of request count
* Correct answer: One step of an operation inside a trace
Spans form a trace tree via parent-child links.

Which exporter is used for tracing tests?
- OTLPSpanExporter
- InMemorySpanExporter
- ConsoleSpanExporter
* Correct answer: InMemorySpanExporter
InMemorySpanExporter stores spans in memory without the network.

What does Counter do in Prometheus?
- Only increases
- Increases and decreases
- Counts a distribution of values
* Correct answer: Only increases
Counter is a monotonic counter (requests, errors, bytes).

Which metric type fits response time?
- Counter
- Histogram
- Gauge
* Correct answer: Histogram
A histogram gives a distribution and percentiles.

Why can't user_id be used as a Prometheus label?
- The name is too long
- Cardinality is unbounded — the number of series will explode
- Prometheus does not support such labels
* Correct answer: Cardinality is unbounded — the number of series will explode
Each combination of labels is a separate series; thousands of users = thousands of series.

What does before_send do in sentry-sdk?
- Sends the event earlier
- Modifies or drops the event before sending
- Changes the DSN
* Correct answer: Modifies or drops the event before sending
Returning None drops the event; returning event sends it.

What will happen if readiness returns 503?
- The container will restart
- Traffic will be withdrawn from the pod
- The application will stop
* Correct answer: Traffic will be withdrawn from the pod
Readiness does not restart the container — it removes the pod from rotation.

What is for: 10m for in an alert rule?
- To make the alert work faster
- So the alarm fires only after 10 minutes of continuous violation
- So the alert always stays silent
* Correct answer: So the alarm fires only after 10 minutes of continuous violation
for cuts off false positives from short-lived spikes.
<!--/QUIZ-->
