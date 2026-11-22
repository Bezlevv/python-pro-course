---
title: Gradient descent
summary: Intuition, learning rate, local minima, stochastic variants.
order: 3
duration: 50 min
difficulty: advanced
tags: gradient descent, optimization, learning rate
---

Gradient descent iteratively moves parameters toward lower loss.

## Idea

Loss is a surface; we step downhill using gradients.

## Update

```python
w = w - lr * grad_w
b = b - lr * grad_b
```

## Learning rate

Too small: slow; too large: diverge.

## Variants

- Batch: full data per step;
- Stochastic (SGD): one sample at a time;
- Mini-batch: small subsets.

## Lesson summary

Gradient descent minimizes loss by following derivatives.

<!--TASK-->
### Task 1 — Simple function
Minimize f(x) = x² by gradient steps: x -= lr * 2*x.

### Task 2 — Converge
Run 50 steps from x=10 and print x.

### Task 3 — Learning rate
Try lr=0.1 vs 1.1 and compare.

### Task 4 — Loss history
Save loss each step and print first/last.

### Task 5 — Local minima
Explain with a sketch: f(x)=x⁴ - x² has two minima.

### Task 6 — SGD idea
Describe stochastic vs batch in comments.

### Task 7 — Practical advice
Write 3 tips for choosing lr.
<!--/TASK-->

<!--HINT-->
### Hint 1
f'(x)=2x.

### Hint 2
x = 10; loop.

### Hint 3
Compare.

### Hint 4
losses list.

### Hint 5
Two valleys.

### Hint 6
Subset vs all.

### Hint 7
Try 0.01, decay, visualize.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
x = 10.0
lr = 0.1
for _ in range(50):
    grad = 2 * x
    x -= lr * grad
print(x)   # около 0
```

### Solution 2
```python
x = 10.0
for _ in range(50):
    x -= 0.1 * 2 * x
print(x)
```

### Solution 3
```python
# lr=0.1: плавно к 0
# lr=1.1: расходится
```

### Solution 4
```python
x = 10.0
losses = []
for _ in range(50):
    x -= 0.1 * 2 * x
    losses.append(x ** 2)
print(losses[0], losses[-1])
```

### Solution 5
```python
# f(x)=x**4 - x**2 имеет два локальных минимума:
# градиентный спуск может попасть в любой
```

### Solution 6
```python
# Batch: градиент по всем данным
# SGD: по одному примеру (больше шума)
# Mini-batch: компромисс
```

### Solution 7
```python
# 1) Пробуй lr = 0.01, 0.001
# 2) Уменьшай lr со временем (decay)
# 3) Смотри на график loss
```
<!--/SOLUTION-->

<!--QUIZ-->
What does gradient descent minimize?
- Loss
- Accuracy
- Data
- Speed
* Correct answer: Loss
Objective.

What is the gradient?
- Derivative direction
- Loss
- Parameter
- Data
* Correct answer: Derivative direction
Slope.

What is too large lr?
- Divergence
- Slow
- Perfect
- None
* Correct answer: Divergence
Overshoot.

What is too small lr?
- Slow convergence
- Fast
- Error
- Optimal
* Correct answer: Slow convergence
Many steps.

What is SGD?
- Stochastic gradient descent
- Slow gradient
- Simple
- Super
* Correct answer: Stochastic gradient descent
One sample.

What is mini-batch?
- Small subsets
- All data
- One
- Zero
* Correct answer: Small subsets
Compromise.

What is a local minimum?
- Lowest nearby point
- Global best
- Maximum
- None
* Correct answer: Lowest nearby point
May be suboptimal.

What is the update rule?
- w = w - lr * grad
- w = w + lr
- w = grad
- w = 0
* Correct answer: w = w - lr * grad
Standard.

What is a loss curve?
- Loss vs iterations
- Accuracy
- Data
- Model
* Correct answer: Loss vs iterations
Diagnostic.

Why visualize loss?
- See convergence
- Speed
- None
- Style
* Correct answer: See convergence
Debug.

What is the derivative of x²?
- 2x
- x
- 2
- x²
* Correct answer: 2x
Gradient.

What does convergence mean?
- Parameters stabilize
- Error
- Start
- Loop
* Correct answer: Parameters stabilize
Done.
<!--/QUIZ-->
