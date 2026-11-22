---
title: Project: neural network for digit recognition
summary: Train a CNN on MNIST and predict custom digits.
order: 6
duration: 120 min
difficulty: advanced
tags: project, cnn, mnist
---

Build a complete digit-recognition model.

## Plan

1. Load MNIST;
2. Define a CNN;
3. Train several epochs;
4. Evaluate;
5. Predict one image.

## Skeleton

```python
import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

transform = transforms.ToTensor()
train_data = datasets.MNIST(root="./data", train=True, download=True, transform=transform)
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
```

## Lesson summary

A CNN trained on MNIST recognizes digits.

<!--TASK-->
### Task 1 — Load
Load MNIST train/test.

### Task 2 — Model
Define SimpleCNN.

### Task 3 — Train
Train for 3 epochs.

### Task 4 — Evaluate
Compute test accuracy.

### Task 5 — Predict
Predict the first test image.

### Task 6 — Save
Save model state_dict.

### Task 7 — Load
Load and predict again.
<!--/TASK-->

<!--HINT-->
### Hint 1
datasets.MNIST.

### Hint 2
Conv + Pool + Linear.

### Hint 3
Loop epochs.

### Hint 4
argmax accuracy.

### Hint 5
model(image).

### Hint 6
torch.save.

### Hint 7
torch.load.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
test_data = datasets.MNIST(root="./data", train=False, download=True, transform=transform)
test_loader = DataLoader(test_data, batch_size=64)
```

### Solution 2
```python
class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, 3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.fc = nn.Linear(16 * 14 * 14, 10)
    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = x.view(x.size(0), -1)
        return self.fc(x)
```

### Solution 3
```python
model = SimpleCNN()
opt = torch.optim.Adam(model.parameters(), lr=0.001)
loss_fn = nn.CrossEntropyLoss()

for epoch in range(3):
    for images, labels in train_loader:
        opt.zero_grad()
        loss = loss_fn(model(images), labels)
        loss.backward()
        opt.step()
```

### Solution 4
```python
correct = total = 0
model.eval()
with torch.no_grad():
    for images, labels in test_loader:
        preds = model(images).argmax(1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)
print(correct / total)
```

### Solution 5
```python
image, label = test_data[0]
pred = model(image.unsqueeze(0)).argmax(1).item()
print(pred, label)
```

### Solution 6
```python
torch.save(model.state_dict(), "model.pth")
```

### Solution 7
```python
model2 = SimpleCNN()
model2.load_state_dict(torch.load("model.pth"))
model2.eval()
```
<!--/SOLUTION-->

<!--QUIZ-->
What is MNIST?
- Digits dataset
- Text
- Cats
- Audio
* Correct answer: Digits dataset
0-9.

What is a CNN?
- Convolutional network
- Linear
- Recurrent
- Random
* Correct answer: Convolutional network
Images.

What does state_dict do?
- Model weights
- Data
- Loss
- Optimizer
* Correct answer: Model weights
Save.

What is torch.save?
- Serializes
- Loads
- Trains
- Plots
* Correct answer: Serializes
To file.

What is argmax(1)?
- Best class per row
- Sum
- Max value
- None
* Correct answer: Best class per row
Prediction.

What is epochs?
- Full passes
- Batches
- Layers
- Steps
* Correct answer: Full passes
Iterations.

What is eval mode?
- Disables training-only
- Faster
- Loss
- None
* Correct answer: Disables training-only
Dropout off.

What is no_grad?
- No gradients
- Train
- Optimize
- None
* Correct answer: No gradients
For inference.

What is reshape?
- view(batch, -1)
- Copy
- Sum
- None
* Correct answer: view(batch, -1)
Flatten.

Why 10 outputs?
- Digits 0-9
- Classes 10? yes
- Batch
- Pixels
* Correct answer: Digits 0-9
Outputs.

What is CrossEntropy?
- Classification loss
- MSE
- L1
- None
* Correct answer: Classification loss
For labels.

How to load weights?
- load_state_dict
- import
- fit
- save
* Correct answer: load_state_dict
Restore.
<!--/QUIZ-->
