---
title: PyTorch for images
summary: Tensors, transforms, CNN.
order: 3
duration: 55 min
difficulty: advanced
tags: pytorch, cnn
---

PyTorch builds image models.

## Tensor

```python
import torch
img = torch.rand(3, 224, 224)   # C, H, W
```

## CNN

```python
import torch.nn as nn

model = nn.Sequential(
    nn.Conv2d(3, 16, kernel_size=3),
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Flatten(),
    nn.Linear(16 * 111 * 111, 10),
)
```

## Transforms

```python
from torchvision import transforms

tf = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])
```

## Lesson summary

Tensors → conv layers → flatten → classify.

<!--TASK-->
### Task 1 — Tensor
Create a random image tensor.

### Task 2 — Conv
Add a conv layer.

### Task 3 — Pool
Max pool.

### Task 4 — Flatten
Flatten.

### Task 5 — Linear
Output layer.

### Task 6 — Transform
Resize + ToTensor.

### Task 7 — Batch
Explain batch dimension.
<!--/TASK-->

<!--HINT-->
### Hint 1
torch.rand.

### Hint 2
Conv2d.

### Hint 3
MaxPool2d.

### Hint 4
Flatten.

### Hint 5
Linear.

### Hint 6
Compose.

### Hint 7
N.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import torch
img = torch.rand(3, 224, 224)
print(img.shape)   # torch.Size([3, 224, 224])
```

### Solution 2
```python
conv = nn.Conv2d(3, 16, kernel_size=3)
out = conv(img.unsqueeze(0))
```

### Solution 3
```python
pool = nn.MaxPool2d(2)
```

### Solution 4
```python
flat = nn.Flatten()
```

### Solution 5
```python
fc = nn.Linear(16 * 111 * 111, 10)
```

### Solution 6
```python
from torchvision import transforms
tf = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])
```

### Solution 7
```python
# Пакет (batch): тензор размера N×C×H×W
# где N — число изображений
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a tensor?
- N-dim array
- Image only
- A list
- None
* Correct answer: N-dim array
torch.

What is C×H×W?
- Channels, height, width
- Size
- Batch
- None
* Correct answer: Channels, height, width
Order.

What is Conv2d?
- Convolution layer
- Pool
- Linear
- None
* Correct answer: Convolution layer
Filters.

What is a kernel?
- Filter size
- Image
- Class
- None
* Correct answer: Filter size
3×3.

What is ReLU?
- Activation
- Loss
- Optimizer
- None
* Correct answer: Activation
Nonlinear.

What is MaxPool2d?
- Downsampling
- Upsampling
- Conv
- None
* Correct answer: Downsampling
2.

What is Flatten?
- 1D vector
- 2D
- Dropout
- None
* Correct answer: 1D vector
Linear.

What is Linear?
- Fully connected
- Conv
- Pool
- None
* Correct answer: Fully connected
Output.

What is a transform?
- Preprocessing
- Training
- Loading
- None
* Correct answer: Preprocessing
ToTensor.

What is Resize?
- Scales image
- Converts
- Flattens
- None
* Correct answer: Scales image
224.

What is a batch?
- Group
- One
- Layer
- None
* Correct answer: Group
N.

What is training?
- Fitting weights
- Predicting
- Loading
- None
* Correct answer: Fitting weights
Loss.
<!--/QUIZ-->
