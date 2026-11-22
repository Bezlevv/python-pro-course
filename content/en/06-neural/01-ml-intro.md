---
title: What is machine learning
summary: ML types, features, labels, datasets, train/test idea.
order: 1
duration: 40 min
difficulty: intermediate
tags: ml, machine learning, features, labels
---

Machine learning lets programs learn patterns from data instead of explicit rules.

## Types

- Supervised: labeled data (classification, regression);
- Unsupervised: no labels (clustering);
- Reinforcement: reward-based.

## Terms

- Features (X): inputs;
- Labels (y): answers;
- Dataset: collection of examples.

## Example

```python
# Features: hours studied, past score
X = [[2, 70], [3, 60], [5, 90]]
# Label: exam result
y = [60, 55, 95]
```

## Train/test

We split data: train a model on one part, test on the other.

## Lesson summary

ML learns from data; features/labels are the core vocabulary.

<!--TASK-->
### Task 1 — Types
Describe supervised/unsupervised/reinforcement in comments.

### Task 2 — Features
Create a small feature matrix for 3 students.

### Task 3 — Labels
Create corresponding labels.

### Task 4 — Dataset
Combine into a list of tuples.

### Task 5 — Split idea
Explain why we hold out test data.

### Task 6 — Classification example
Give 3 examples of classification.

### Task 7 — Regression example
Give 3 examples of regression.
<!--/TASK-->

<!--HINT-->
### Hint 1
Labeled vs unlabeled.

### Hint 2
X = [[...], [...], [...]].

### Hint 3
y = [...] same length.

### Hint 4
list(zip(X, y)).

### Hint 5
Evaluate on unseen.

### Hint 6
Spam, image, sentiment.

### Hint 7
Price, temperature, demand.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
# Supervised: есть ответы (метки)
# Unsupervised: ответов нет, ищем структуру
# Reinforcement: агент учится на наградах
```

### Solution 2
```python
X = [
    [2, 70],   # часы, прошлый балл
    [3, 60],
    [5, 90],
]
```

### Solution 3
```python
y = [60, 55, 95]
```

### Solution 4
```python
dataset = list(zip(X, y))
print(dataset)
```

### Solution 5
```python
# Тест на невиданных данных показывает реальное качество
```

### Solution 6
```python
# Спам/не спам, кошка/собака, позитив/негатив
```

### Solution 7
```python
# Цена квартиры, температура, спрос
```
<!--/SOLUTION-->

<!--QUIZ-->
What is supervised learning?
- Labeled data
- No labels
- Rewards
- Clustering
* Correct answer: Labeled data
Teacher.

What are features?
- Inputs
- Outputs
- Labels
- Models
* Correct answer: Inputs
X.

What are labels?
- Answers/outputs
- Inputs
- Features
- Data
* Correct answer: Answers/outputs
y.

What is a dataset?
- Collection of examples
- A model
- An algorithm
- A metric
* Correct answer: Collection of examples
Data.

What is classification?
- Discrete categories
- Numbers
- Clusters
- Rewards
* Correct answer: Discrete categories
Labels.

What is regression?
- Continuous values
- Categories
- Clusters
- Text
* Correct answer: Continuous values
Numbers.

Why split train/test?
- Evaluate on unseen
- Faster
- Required
- Memory
* Correct answer: Evaluate on unseen
Generalization.

What is unsupervised learning?
- Patterns without labels
- Labeled
- Supervised
- Reinforcement
* Correct answer: Patterns without labels
Clustering.

What is a model?
- Learned function
- Data
- Feature
- Label
* Correct answer: Learned function
Maps X→y.

What is an example?
- One row
- A column
- A model
- Label only
* Correct answer: One row
(X, y).

What is overfitting?
- Memorizes training, fails test
- Generalizes
- Slow
- None
* Correct answer: Memorizes training, fails test
Bad.

What is accuracy?
- Fraction correct
- Speed
- Size
- Loss
* Correct answer: Fraction correct
Metric.
<!--/QUIZ-->
