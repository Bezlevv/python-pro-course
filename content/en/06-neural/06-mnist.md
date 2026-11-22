---
title: Training a network on MNIST
summary: Loading data, DataLoader, training/eval loops, accuracy.
order: 6
duration: 60 min
difficulty: advanced
tags: mnist, dataloader, training, accuracy
---

MNIST digits are the classic "hello world" of deep learning.

## Load data

```python
import torch
from torchvision import datasets, transforms

transform = transforms.ToTensor()
train_data = datasets.MNIST(root="./data", train=True, download=True, transform=transform)
test_data = datasets.MNIST(root="./data", train=False, download=True, transform=transform)
```

## DataLoader

```python
from torch.utils.data import DataLoader

train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
```

## Model

A small MLP outputs 10 classes.

## Training loop

```python
for images, labels in train_loader:
    images = images.view(images.size(0), -1)
    opt.zero_grad()
    loss = loss_fn(model(images), labels)
    loss.backward()
    opt.step()
```

## Evaluation

```python
correct = 0
total = 0
model.eval()
with torch.no_grad():
    for images, labels in test_loader:
        images = images.view(images.size(0), -1)
        preds = model(images).argmax(dim=1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)
accuracy = correct / total
```

## Lesson summary

MNIST + DataLoader + training/eval loops produce a working classifier.

<!--TASK-->
### Task 1 — Load
Load MNIST train and test datasets.

### Task 2 — Shapes
Print a sample image shape and label.

### Task 3 — DataLoader
Create a loader with batch 32.

### Task 4 — Model
Define an MLP with 10 outputs.

### Task 5 — Train epoch
Run one epoch over the loader.

### Task 6 — Evaluate
Compute accuracy on test data.

### Task 7 — Flatten
Explain images.view(batch, -1).
<!--/TASK-->

<!--HINT-->
### Hint 1
datasets.MNIST.

### Hint 2
image.shape, label.

### Hint 3
DataLoader.

### Hint 4
nn.Linear(784, ...); output 10.

### Hint 5
Loop over loader.

### Hint 6
no_grad; argmax.

### Hint 7
784 pixels vector.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from torchvision import datasets, transforms
transform = transforms.ToTensor()
train_data = datasets.MNIST(root="./data", train=True, download=True, transform=transform)
test_data = datasets.MNIST(root="./data", train=False, download=True, transform=transform)
```

### Solution 2
```python
image, label = train_data[0]
print(image.shape)   # torch.Size([1, 28, 28])
print(label)
```

### Solution 3
```python
from torch.utils.data import DataLoader
train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
```

### Solution 4
```python
import torch.nn as nn
import torch.nn.functional as F

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 128)
        self.fc2 = nn.Linear(128, 10)
    def forward(self, x):
        x = F.relu(self.fc1(x))
        return self.fc2(x)
```

### Solution 5
```python
import torch.optim as optim
model = MLP()
opt = optim.Adam(model.parameters(), lr=0.001)
loss_fn = nn.CrossEntropyLoss()

for images, labels in train_loader:
    images = images.view(images.size(0), -1)
    opt.zero_grad()
    loss = loss_fn(model(images), labels)
    loss.backward()
    opt.step()
```

### Solution 6
```python
test_loader = DataLoader(test_data, batch_size=64)
correct = total = 0
model.eval()
with torch.no_grad():
    for images, labels in test_loader:
        images = images.view(images.size(0), -1)
        preds = model(images).argmax(dim=1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)
print(correct / total)
```

### Solution 7
```python
# image [1,28,28] → плоский вектор [784]
# view(batch, -1) разворачивает каждую картинку
```
<!--/SOLUTION-->

<!--QUIZ-->
What is MNIST?
- Digit dataset
- Cats
- Text
- Audio
* Correct answer: Digit dataset
0-9.

What is DataLoader?
- Batched iteration
- Model
- Loss
- Metric
* Correct answer: Batched iteration
Efficient.

What is batch_size?
- Samples per batch
- Epochs
- Layers
- Features
* Correct answer: Samples per batch
32.

What does shuffle=True do?
- Randomizes order
- Sorts
- Skips
- None
* Correct answer: Randomizes order
Better training.

What is 784?
- 28*28 pixels
- Classes
- Layers
- Epochs
* Correct answer: 28*28 pixels
Flattened.

What is CrossEntropyLoss?
- Classification loss
- Regression
- MSE
- L1
* Correct answer: Classification loss
For classes.

What does argmax(dim=1) do?
- Picks best class
- Sums
- Losses
- Reshapes
* Correct answer: Picks best class
Prediction.

What is model.eval()?
- Evaluation mode
- Train mode
- Freeze
- None
* Correct answer: Evaluation mode
Disables dropout.

What is no_grad?
- No gradients
- Train
- Loss
- Backprop
* Correct answer: No gradients
For eval.

What is accuracy?
- correct/total
- Loss
- Epochs
- Batch
* Correct answer: correct/total
Metric.

What is an epoch?
- One full pass
- A batch
- A step
- A layer
* Correct answer: One full pass
Training.

What is preds == labels?
- Elementwise compare
- Loss
- Sum
- Plot
* Correct answer: Elementwise compare
Count correct.
<!--/QUIZ-->
