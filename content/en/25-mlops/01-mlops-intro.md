---
title: MLOps basics
summary: Lifecycle, reproducibility, tracking.
order: 1
duration: 40 min
difficulty: advanced
tags: mlops
---

MLOps operationalizes machine learning.

## Lifecycle

Data → training → evaluation → deployment → monitoring.

## Goals

- Reproducible experiments;
- Versioned data/models;
- Automated pipelines.

## Lesson summary

MLOps = ML + engineering practices.

<!--TASK-->
### Task 1 — Lifecycle
List the stages.

### Task 2 — Reproducible
Why pin versions?

### Task 3 — Tracking
What to log in experiments?

### Task 4 — Data versioning
Why store data versions?

### Task 5 — Deployment
Ways to serve a model.

### Task 6 — Monitoring
What to monitor?

### Task 7 — CI/CD
How does CI fit?
<!--/TASK-->

<!--HINT-->
### Hint 1
Data.

### Hint 2
Same results.

### Hint 3
Metrics.

### Hint 4
Repro.

### Hint 5
API.

### Hint 6
Drift.

### Hint 7
Tests.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```text
Сбор данных → обучение → оценка
→ деплой → мониторинг
```

### Solution 2
```text
Версии библиотек, данных и кода фиксируются —
эксперимент можно повторить
```

### Solution 3
```text
Гиперпараметры, метрики, датасет, версия кода,
время, конфиг
```

### Solution 4
```text
Данные меняются — модель надо переобучать
на той же версии, что и при оценке
```

### Solution 5
```text
REST API, batch-инференс, on-device,
встроенный сервис
```

### Solution 6
```text
Точность на живых данных, задержка,
дрейф данных, ошибки
```

### Solution 7
```text
CI проверяет код и тесты; CD запускает
пайплайн обучения при изменениях
```
<!--/SOLUTION-->

<!--QUIZ-->
What is MLOps?
- ML engineering
- Only training
- Only deploy
- None
* Correct answer: ML engineering
Ops.

What is the lifecycle?
- Stages
- One step
- A model
- None
* Correct answer: Stages
Data→monitor.

What is reproducibility?
- Same results
- Random
- New
- None
* Correct answer: Same results
Versions.

What is tracking?
- Logging runs
- Deploying
- Training
- None
* Correct answer: Logging runs
Metrics.

What is a metric?
- Quality number
- Data
- Model
- None
* Correct answer: Quality number
Accuracy.

What is drift?
- Data change
- Same
- Error
- None
* Correct answer: Data change
Monitor.

What is serving?
- Using model
- Training
- Cleaning
- None
* Correct answer: Using model
API.

What is batch?
- Bulk processing
- Real-time
- One
- None
* Correct answer: Bulk processing
Offline.

What is latency?
- Delay
- Speed
- Accuracy
- None
* Correct answer: Delay
Time.

What is a pipeline?
- Automated flow
- One stage
- A file
- None
* Correct answer: Automated flow
Steps.

What is versioning?
- Snapshots
- Latest only
- None
- Always
* Correct answer: Snapshots
Repro.

What is monitoring?
- Watching live
- Deploying
- Training
- None
* Correct answer: Watching live
Prod.
<!--/QUIZ-->
