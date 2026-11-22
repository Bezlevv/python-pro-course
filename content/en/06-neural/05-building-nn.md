---
title: Building a neural network with PyTorch
summary: nn.Module, layers, activation, forward, training loop.
order: 5
duration: 60 min
difficulty: advanced
tags: pytorch, nn, network, forward
---

PyTorch makes neural networks modular.

## Define model

```python
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(2, 4)
        self.fc2 = nn.Linear(4, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        return self.fc2(x)
```

## Training loop

```python
import torch.optim as optim

model = Net()
opt = optim.SGD(model.parameters(), lr=0.01)
loss_fn = nn.MSELoss()

for epoch in range(100):
    pred = model(X)
    loss = loss_fn(pred, y)
    opt.zero_grad()
    loss.backward()
    opt.step()
```

## Lesson summary

Define layers in __init__, forward computes output, optimizer updates.

<!--TASK-->
### Task 1 — Linear
Create nn.Linear(3, 1) and apply to a tensor.

### Task 2 — Model
Define a 2→4→1 network.

### Task 3 — Forward
Call model(x) and check shape.

### Task 4 — MSELoss
Compute loss between prediction and target.

### Task 5 — Optimizer
Create SGD optimizer.

### Task 6 — Loop
Train on small data for 50 epochs.

### Task 7 — ReLU
Explain where F.relu is applied.
<!--/TASK-->

<!--HINT-->
### Hint 1
nn.Linear(in, out).

### Hint 2
nn.Module subclass.

### Hint 3
model(x).

### Hint 4
nn.MSELoss()(pred, y).

### Hint 5
optim.SGD.

### Hint 6
zero_grad; backward; step.

### Hint 7
Between layers.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import torch
import torch.nn as nn

lin = nn.Linear(3, 1)
x = torch.randn(4, 3)
print(lin(x).shape)   # [4, 1]
```

### Solution 2
```python
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(2, 4)
        self.fc2 = nn.Linear(4, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        return self.fc2(x)
```

### Solution 3
```python
model = Net()
out = model(torch.randn(8, 2))
print(out.shape)   # [8, 1]
```

### Solution 4
```python
loss_fn = nn.MSELoss()
loss = loss_fn(out, torch.randn(8, 1))
print(loss.item())
```

### Solution 5
```python
import torch.optim as optim
opt = optim.SGD(model.parameters(), lr=0.01)
```

### Solution 6
```python
X = torch.randn(20, 2)
y = (X[:, 0] + X[:, 1]).unsqueeze(1)

for _ in range(50):
    opt.zero_grad()
    loss = loss_fn(model(X), y)
    loss.backward()
    opt.step()
print(loss.item())
```

### Solution 7
```python
# ReLU добавляет нелинейность между слоями:
# F.relu(fc1(x)), затем fc2
```
<!--/SOLUTION-->

<!--QUIZ-->
What does nn.Module give?
- Base for models
- Data
- Loss
- Optimizer
* Correct answer: Base for models
Subclass.

What is nn.Linear?
- Fully connected layer
- Conv
- Dropout
- ReLU
* Correct answer: Fully connected layer
Weights.

What is forward?
- Computes output
- Trains
- Losses
- Optimizes
* Correct answer: Computes output
Propagation.

What is F.relu?
- Activation
- Loss
- Layer
- Optimizer
* Correct answer: Activation
Nonlinearity.

What is an optimizer?
- Updates weights
- Loss
- Data
- Model
* Correct answer: Updates weights
SGD.

What is loss_fn?
- Objective
- Data
- Model
- Layer
* Correct answer: Objective
MSE.

What does zero_grad do?
- Clears gradients
- Steps
- Computes
- Prints
* Correct answer: Clears gradients
Before backward.

What does opt.step do?
- Updates parameters
- Resets
- Losses
- Predicts
* Correct answer: Updates parameters
Gradient step.

What is epoch?
- Full pass over data
- One step
- A layer
- A loss
* Correct answer: Full pass over data
Iteration.

What is a parameter?
- Weight/bias
- Loss
- Data
- Prediction
* Correct answer: Weight/bias
Learnable.

What is the input shape for Linear(2, 4)?
- (..., 2)
- (..., 4)
- (2, 4)
- any
* Correct answer: (..., 2)
Last dim 2.

What is a batch?
- Multiple samples
- One sample
- Model
- Loss
* Correct answer: Multiple samples
Together.
<!--/QUIZ-->
