---
title: scikit-learn: learning pipeline
summary: Train/test split, models, metrics, preprocessors and pipelines.
order: 6
duration: 45 min
difficulty: intermediate
tags: sklearn, ml, train_test_split, metrics
---

scikit-learn provides classic machine learning tools.

## Split

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
```

## Model

```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
pred = model.predict(X_test)
```

## Metrics

```python
from sklearn.metrics import mean_squared_error, accuracy_score
```

## Preprocessing

```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X = scaler.fit_transform(X)
```

## Pipeline

```python
from sklearn.pipeline import Pipeline
pipe = Pipeline([("scale", StandardScaler()), ("model", LinearRegression())])
```

## Lesson summary

Sklearn: split → preprocess → fit → predict → evaluate.

<!--TASK-->
### Task 1 — Generate data
Create X, y: y = 2*X + noise (numpy).

### Task 2 — Split
Split into train/test 80/20; print shapes.

### Task 3 — Fit
Train LinearRegression and print coefficients.

### Task 4 — Predict
Predict on test data; print first 5 predictions.

### Task 5 — Metric
Compute mean_squared_error between truth and predictions.

### Task 6 — Scale
Apply StandardScaler and show mean ~0.

### Task 7 — Pipeline
Combine scaler + model in a Pipeline and fit.
<!--/TASK-->

<!--HINT-->
### Hint 1
y = 2*X + np.random.randn(...).

### Hint 2
train_test_split(...).

### Hint 3
model.coef_.

### Hint 4
model.predict(X_test).

### Hint 5
mean_squared_error(y_test, pred).

### Hint 6
scaler.mean_ near 0.

### Hint 7
Pipeline([...]).
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import numpy as np
X = np.random.rand(100, 1) * 10
y = 2 * X[:, 0] + np.random.randn(100)
```

### Solution 2
```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
print(X_train.shape, X_test.shape)
```

### Solution 3
```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
print(model.coef_)
```

### Solution 4
```python
pred = model.predict(X_test)
print(pred[:5])
```

### Solution 5
```python
from sklearn.metrics import mean_squared_error
print(mean_squared_error(y_test, pred))
```

### Solution 6
```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print(X_scaled.mean(axis=0))
```

### Solution 7
```python
from sklearn.pipeline import Pipeline
pipe = Pipeline([("scale", StandardScaler()), ("model", LinearRegression())])
pipe.fit(X_train, y_train)
print(pipe.predict(X_test)[:3])
```
<!--/SOLUTION-->

<!--QUIZ-->
What does train_test_split do?
- Splits data
- Scales
- Fits
- Evaluates
* Correct answer: Splits data
Train/test sets.

What is test_size?
- Fraction of test data
- Train size
- Seed
- Metric
* Correct answer: Fraction of test data
0.2 = 20%.

What does model.fit do?
- Trains the model
- Predicts
- Scores
- Splits
* Correct answer: Trains the model
Learns.

What does predict do?
- Produces outputs
- Trains
- Evaluates
- Scales
* Correct answer: Produces outputs
Inference.

What is mean_squared_error?
- A regression metric
- Accuracy
- F1
- Split
* Correct answer: A regression metric
Error.

What does StandardScaler do?
- Normalizes features
- Splits
- Predicts
- Plots
* Correct answer: Normalizes features
Zero mean, unit variance.

What is a Pipeline?
- Chain of steps
- A list
- A model
- A metric
* Correct answer: Chain of steps
Preprocess + model.

What is X?
- Features matrix
- Target
- Metric
- Split
* Correct answer: Features matrix
Inputs.

What is y?
- Target vector
- Features
- Test
- Model
* Correct answer: Target vector
Labels.

Why use random_state?
- Reproducibility
- Speed
- Memory
- Plot
* Correct answer: Reproducibility
Same split.

What does coef_ contain?
- Model weights
- Predictions
- Errors
- Data
* Correct answer: Model weights
Coefficients.

Which is classic regression?
- LinearRegression
- KMeans
- PCA
- Cross_val
* Correct answer: LinearRegression
Supervised.
<!--/QUIZ-->
