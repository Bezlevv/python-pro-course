---
title: Neural networks: basics and PyTorch
summary: Neurons, layers, training loop.
order: 3
duration: 50 min
difficulty: advanced
tags: nn, pytorch
---

Neural nets learn complex functions.

## Neuron

Inputs × weights + bias → activation.

## PyTorch

```python
import torch
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(2, 16),
    nn.ReLU(),
    nn.Linear(16, 1),
)
loss_fn = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters())
```

## Loop

```python
for epoch in range(100):
    pred = model(X)
    loss = loss_fn(pred, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```

## Lesson summary

Layers + loss + gradient descent.

<!--TASK-->
### Task 1 — Model
Create a 2-layer MLP.

### Task 2 — Loss
Choose MSE for regression.

### Task 3 — Optimizer
Create Adam.

### Task 4 — Loop
Run 100 epochs.

### Task 5 — Backward
Explain backward().

### Task 6 — Tensor
Create a tensor.

### Task 7 — Batch
Explain batches.
<!--/TASK-->

<!--HINT-->
### Hint 1
nn.Sequential.

### Hint 2
MSELoss.

### Hint 3
Adam.

### Hint 4
For.

### Hint 5
Gradients.

### Hint 6
torch.tensor.

### Hint 7
Groups.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import torch.nn as nn
model = nn.Sequential(
    nn.Linear(2, 16),
    nn.ReLU(),
    nn.Linear(16, 1),
)
```

### Solution 2
```python
loss_fn = nn.MSELoss()
```

### Solution 3
```python
optimizer = torch.optim.Adam(model.parameters())
```

### Solution 4
```python
for epoch in range(100):
    pred = model(X)
    loss = loss_fn(pred, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```

### Solution 5
```python
# backward() считает градиенты потерь
# по всем параметрам сети
```

### Solution 6
```python
import torch
t = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
print(t.shape)   # torch.Size([2, 2])
```

### Solution 7
```python
# Данные делят на группы (batch):
# стабильнее градиенты и эффективнее GPU
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a neuron?
- weight × input + bias
- A layer
- A loss
- None
* Correct answer: weight × input + bias
Unit.

What is a layer?
- Group of neurons
- A tensor
- An epoch
- None
* Correct answer: Group of neurons
Linear.

What is ReLU?
- Activation
- Loss
- Optimizer
- None
* Correct answer: Activation
max(0,x).

What is a loss?
- Error measure
- A weight
- An input
- None
* Correct answer: Error measure
MSE.

What is an optimizer?
- Updates weights
- Computes loss
- Loads data
- None
* Correct answer: Updates weights
Adam.

What is backward?
- Gradients
- Forward
- Data
- None
* Correct answer: Gradients
Backprop.

What is step?
- Applies update
- Loads
- Eval
- None
* Correct answer: Applies update
Optimizer.

What is zero_grad?
- Clears gradients
- Sets zero data
- Stops
- None
* Correct answer: Clears gradients
Reset.

What is epoch?
- Full pass
- One batch
- A layer
- None
* Correct answer: Full pass
Loop.

What is a tensor?
- N-dim array
- A list
- A class
- None
* Correct answer: N-dim array
torch.

What is the parameter?
- Learnable weight
- Input
- Label
- None
* Correct answer: Learnable weight
Model.

What is training?
- Minimizing loss
- Predicting
- Loading
- None
* Correct answer: Minimizing loss
Gradient.
<!--/QUIZ-->
