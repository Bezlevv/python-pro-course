---
title: AI basics: what is ML
summary: Data, models, training vs inference.
order: 1
duration: 40 min
difficulty: beginner
tags: ai, ml
---

Machine learning learns patterns from data.

## Key terms

- Data: examples (features + labels);
- Model: function that predicts;
- Training: fitting model to data;
- Inference: predictions on new data.

## Types

Supervised, unsupervised, reinforcement.

## Python

```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X, y)          # обучение
pred = model.predict(X_new)  # inference
```

## Lesson summary

ML = data + model + training + inference.

<!--TASK-->
### Task 1 — Terms
Define model, training, inference.

### Task 2 — Data
Give an example dataset structure.

### Task 3 — Fit
Train LinearRegression.

### Task 4 — Predict
Predict on new data.

### Task 5 — Types
Name three ML types.

### Task 6 — Features
What is a feature?

### Task 7 — Label
What is a label?
<!--/TASK-->

<!--HINT-->
### Hint 1
Function.

### Hint 2
Table.

### Hint 3
fit.

### Hint 4
predict.

### Hint 5
Supervised.

### Hint 6
Column.

### Hint 7
Answer.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
# Model — функция, которая предсказывает по признакам
# Training — подбор параметров по данным
# Inference — применение модели к новым данным
```

### Solution 2
```python
# X: [[площадь], [площадь], ...] — признаки
# y: [цена, цена, ...] — целевое значение
```

### Solution 3
```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X, y)
```

### Solution 4
```python
pred = model.predict([[75]])
```

### Solution 5
```python
# Supervised — с ответами
# Unsupervised — без ответов
# Reinforcement — через награды
```

### Solution 6
```python
# Признак (feature) — измеримая характеристика объекта
# например, площадь квартиры
```

### Solution 7
```python
# Метка (label) — правильный ответ для примера
# например, цена квартиры
```
<!--/SOLUTION-->

<!--QUIZ-->
What is ML?
- Learning from data
- Programming rules
- A database
- None
* Correct answer: Learning from data
Patterns.

What is a model?
- Predictive function
- Data
- A label
- None
* Correct answer: Predictive function
Function.

What is training?
- Fitting to data
- Predicting
- Cleaning
- None
* Correct answer: Fitting to data
fit().

What is inference?
- New predictions
- Training
- Data
- None
* Correct answer: New predictions
predict().

What is a feature?
- Input characteristic
- Answer
- Model
- None
* Correct answer: Input characteristic
X.

What is a label?
- Correct answer
- Input
- Feature
- None
* Correct answer: Correct answer
y.

What is supervised?
- With labels
- Without
- Neither
- None
* Correct answer: With labels
Answers.

What is unsupervised?
- Without labels
- With
- Same
- None
* Correct answer: Without labels
Clusters.

What is a dataset?
- Example collection
- One model
- A function
- None
* Correct answer: Example collection
Rows.

What is sklearn?
- ML library
- A game
- A database
- None
* Correct answer: ML library
Python.

What is LinearRegression?
- Regression model
- Classifier
- Clustering
- None
* Correct answer: Regression model
Continuous.

What is predict?
- Applies model
- Trains
- Cleans
- None
* Correct answer: Applies model
Inference.
<!--/QUIZ-->
