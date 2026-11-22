---
title: Linear regression from scratch
summary: Hypothesis, loss, normal equation, gradient descent intuition.
order: 2
duration: 50 min
difficulty: advanced
tags: regression, gradient, loss
---

Linear regression models y as a linear function of features.

## Hypothesis

```python
# y = w * x + b
def predict(x, w, b):
    return w * x + b
```

## Loss

Mean squared error:

```python
def mse(y_true, y_pred):
    return sum((a - b) ** 2 for a, b in zip(y_true, y_pred)) / len(y_true)
```

## Gradient descent

Update weights toward lower loss:

```python
def step(x, y, w, b, lr):
    n = len(x)
    dw = sum(2 * (predict(xi, w, b) - yi) * xi for xi, yi in zip(x, y)) / n
    db = sum(2 * (predict(xi, w, b) - yi) for xi, yi in zip(x, y)) / n
    return w - lr * dw, b - lr * db
```

## Lesson summary

A model, a loss, and gradient steps make linear regression.

<!--TASK-->
### Task 1 — Predict
Implement predict(x, w, b) and test with w=2, b=1.

### Task 2 — MSE
Compute MSE for two small vectors.

### Task 3 — Gradient
Compute dw and db formulas on tiny data.

### Task 4 — One step
Update w, b with lr=0.01 once.

### Task 5 — Loop
Run 100 steps and print final w, b.

### Task 6 — Compare
Compare predictions with actual y.

### Task 7 — From sklearn
Fit LinearRegression and print coefficients.
<!--/TASK-->

<!--HINT-->
### Hint 1
return w * x + b.

### Hint 2
Sum of squared differences / n.

### Hint 3
Partial derivatives.

### Hint 4
w - lr * dw.

### Hint 5
for _ in range(100).

### Hint 6
zip predictions with y.

### Hint 7
sklearn.linear_model.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
def predict(x, w, b):
    return w * x + b

print(predict(3, 2, 1))   # 7
```

### Solution 2
```python
def mse(y_true, y_pred):
    return sum((a - b) ** 2 for a, b in zip(y_true, y_pred)) / len(y_true)

print(mse([3, 5], [2, 6]))   # 0.5
```

### Solution 3
```python
x = [1, 2, 3]
y = [2, 4, 6]
w = b = 0.0
n = len(x)
dw = sum(2 * (predict(xi, w, b) - yi) * xi for xi, yi in zip(x, y)) / n
db = sum(2 * (predict(xi, w, b) - yi) for xi, yi in zip(x, y)) / n
print(dw, db)
```

### Solution 4
```python
lr = 0.01
w = w - lr * dw
b = b - lr * db
print(w, b)
```

### Solution 5
```python
for _ in range(100):
    dw = sum(2 * (predict(xi, w, b) - yi) * xi for xi, yi in zip(x, y)) / n
    db = sum(2 * (predict(xi, w, b) - yi) for xi, yi in zip(x, y)) / n
    w -= lr * dw
    b -= lr * db
print(w, b)   # около 2 и 0
```

### Solution 6
```python
preds = [predict(xi, w, b) for xi in x]
print(preds)
```

### Solution 7
```python
from sklearn.linear_model import LinearRegression
import numpy as np

X = np.array(x).reshape(-1, 1)
model = LinearRegression().fit(X, y)
print(model.coef_, model.intercept_)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is the hypothesis in linear regression?
- y = w*x + b
- y = x²
- sigmoid
- tree
* Correct answer: y = w*x + b
Linear form.

What are w and b?
- Weight and bias
- Data
- Labels
- Errors
* Correct answer: Weight and bias
Parameters.

What is MSE?
- Mean squared error
- Max error
- Median
- Accuracy
* Correct answer: Mean squared error
Loss.

What does gradient descent do?
- Reduces loss stepwise
- Increases
- Solves exactly
- Plots
* Correct answer: Reduces loss stepwise
Optimize.

What is lr?
- Learning rate
- Label rate
- Length
- Loss
* Correct answer: Learning rate
Step size.

Why sum of squares?
- Smooth, differentiable
- Fast
- Exact
- None
* Correct answer: Smooth, differentiable
Gradients.

What does dw represent?
- Derivative w.r.t. w
- Weight
- Loss
- Bias
* Correct answer: Derivative w.r.t. w
Gradient.

What is a derivative?
- Rate of change
- Loss
- Prediction
- Data
* Correct answer: Rate of change
Slope.

How many steps usually?
- Many iterations
- One
- Zero
- Depends only
* Correct answer: Many iterations
Until convergence.

What happens with high lr?
- Diverges
- Converges fast
- Nothing
- Accuracy
* Correct answer: Diverges
Overshoots.

What does sklearn fit do?
- Learns parameters
- Predicts
- Plots
- Scores
* Correct answer: Learns parameters
coef_.

What is overfitting in regression?
- Complex model memorizes
- Simple works
- None
- Great
* Correct answer: Complex model memorizes
Bad test.
<!--/QUIZ-->
