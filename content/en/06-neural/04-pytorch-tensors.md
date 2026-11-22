---
title: PyTorch: tensors and autograd
summary: Creating tensors, operations, gradients and simple optimization.
order: 4
duration: 50 min
difficulty: advanced
tags: pytorch, tensors, autograd
---

PyTorch provides tensors and automatic differentiation.

## Tensors

```python
import torch

x = torch.tensor([1.0, 2.0, 3.0])
y = x * 2
print(x + y)
```

## Autograd

```python
x = torch.tensor(3.0, requires_grad=True)
y = x ** 2
y.backward()
print(x.grad)   # 6.0
```

## Manual gradient step

```python
x = torch.tensor(10.0, requires_grad=True)
lr = 0.1
for _ in range(50):
    loss = x ** 2
    loss.backward()
    with torch.no_grad():
        x -= lr * x.grad
    x.grad.zero_()
print(x.item())
```

## Lesson summary

Tensors + autograd simplify training loops.

<!--TASK-->
### Task 1 — Tensor
Create a tensor and compute x*2 + 1.

### Task 2 — Shape
Create a 2x3 tensor and print shape.

### Task 3 — Grad
Compute derivative of x² at x=4.

### Task 4 — Chain
y = x³ + 2x; find grad at x=2.

### Task 5 — Loop
Optimize x for f=x² for 100 steps.

### Task 6 — zero_
Explain why grad.zero_() is needed.

### Task 7 — no_grad
Explain the role of torch.no_grad().
<!--/TASK-->

<!--HINT-->
### Hint 1
torch.tensor([1.0, 2.0]).

### Hint 2
torch.zeros(2, 3).

### Hint 3
requires_grad=True; backward().

### Hint 4
x.grad.

### Hint 5
Same as before.

### Hint 6
Accumulates.

### Hint 7
Skip graph.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import torch
x = torch.tensor([1.0, 2.0, 3.0])
print(x * 2 + 1)
```

### Solution 2
```python
m = torch.zeros(2, 3)
print(m.shape)
```

### Solution 3
```python
x = torch.tensor(4.0, requires_grad=True)
y = x ** 2
y.backward()
print(x.grad)   # 8.0
```

### Solution 4
```python
x = torch.tensor(2.0, requires_grad=True)
y = x ** 3 + 2 * x
y.backward()
print(x.grad)   # 3*4+2 = 14
```

### Solution 5
```python
x = torch.tensor(10.0, requires_grad=True)
for _ in range(100):
    loss = x ** 2
    loss.backward()
    with torch.no_grad():
        x -= 0.1 * x.grad
    x.grad.zero_()
print(x.item())
```

### Solution 6
```python
# Градиенты накапливаются; zero_() сбрасывает перед шагом
```

### Solution 7
```python
# no_grad отключает построение графа — для обновления параметров
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a tensor?
- Multi-dim array
- A list
- A function
- A loss
* Correct answer: Multi-dim array
Like numpy.

What is requires_grad?
- Tracks gradients
- Disables
- Faster
- None
* Correct answer: Tracks gradients
For autograd.

What does backward() do?
- Computes gradients
- Forwards
- Prints
- Resets
* Correct answer: Computes gradients
Backprop.

Where is the gradient?
- x.grad
- x.value
- loss.grad
- y.grad
* Correct answer: x.grad
Attribute.

What is autograd?
- Automatic differentiation
- A dataset
- A model
- A loss
* Correct answer: Automatic differentiation
PyTorch.

Why zero_()?
- Accumulation reset
- Speed
- Loss
- None
* Correct answer: Accumulation reset
Before next step.

What is no_grad?
- Disables gradient tracking
- Slows
- Errors
- None
* Correct answer: Disables gradient tracking
For updates.

What does item() do?
- Python number
- Tensor
- Loss
- None
* Correct answer: Python number
Scalar.

What is a tensor shape?
- Dimensions
- Values
- Grad
- Data
* Correct answer: Dimensions
Tuple.

What is torch.zeros?
- Tensor of zeros
- Ones
- Random
- Range
* Correct answer: Tensor of zeros
Tensor.

What is a scalar tensor?
- 0-dim tensor
- 1D
- 2D
- None
* Correct answer: 0-dim tensor
Single value.

Why torch in ML?
- GPU + autograd
- SQL
- HTML
- None
* Correct answer: GPU + autograd
Deep learning.
<!--/QUIZ-->
