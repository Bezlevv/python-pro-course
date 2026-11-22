---
title: Exam: Neural Networks
summary: Test your machine learning knowledge: linear regression, gradient descent, PyTorch, neural networks, and MNIST.
order: 99
duration: 30 min
difficulty: advanced
tags: exam
exam: true
---

<!--QUIZ-->
Why does a neural network need a non-linear activation (for example, ReLU)?
- To reduce the number of network parameters
- Without it, a stack of linear layers stays linear and cannot model curved relationships
- To speed up data loading
- It is a syntax requirement of PyTorch
* Correct answer: Without it, a stack of linear layers stays linear and cannot model curved relationships
Non-linearity is what makes the network a universal approximator: without it, layer depth adds nothing new.

What is a loss function?
- A function that shows how much the model's predictions differ from the correct answers
- A function that generates training data
- The same thing as an optimizer
- A way to normalize images
* Correct answer: A function that shows how much the model's predictions differ from the correct answers
Loss is a number: the smaller it is, the better the model. Training is precisely about minimizing it.

How does gradient descent update weights?
- It changes the network architecture
- It computes the gradient of the loss function and takes a step in the direction of decreasing loss
- It splits the data into batches
- It increases the learning rate each epoch
* Correct answer: It computes the gradient of the loss function and takes a step in the direction of decreasing loss
The gradient shows the direction of steepest loss increase, so weights are shifted the opposite way.

What is the difference between mini-batch gradient descent and stochastic gradient descent?
- The choice of loss function
- The size of the sample used to compute the gradient: a subset of data versus a single example
- The learning rate
- There is no difference
* Correct answer: The size of the sample used to compute the gradient: a subset of data versus a single example
The stochastic variant takes one example per step; mini-batch takes a batch of examples (for example, 64). It's a trade-off between accuracy and speed.

How do you enable gradient computation for a tensor in PyTorch?
- tensor.requires_grad = True
- tensor.grad = True
- torch.gradient(tensor)
- It is always done automatically
* Correct answer: tensor.requires_grad = True
After that, autograd will remember the operations and be able to compute derivatives when backward() is called.

What does nn.Linear(784, 128) do?
- Creates a convolutional layer
- Creates a fully connected layer with 784 inputs and 128 outputs
- Reduces the image to 128 pixels
- Adds 784 layers of 128 neurons each
* Correct answer: Creates a fully connected layer with 784 inputs and 128 outputs
The layer has learnable weights and biases behind it; it turns a vector of 784 numbers into a vector of 128 numbers.

Why does the input layer of a network working with MNIST have 784 neurons?
- Because the dataset has 784 classes
- Because a 28×28 image is flattened into a vector of 784 pixels
- Because it is the standard number for all networks
- Because MNIST has 784 training examples
* Correct answer: Because a 28×28 image is flattened into a vector of 784 pixels
For a fully connected network, each image becomes a one-dimensional feature vector; nn.Flatten does this automatically.

What does F.cross_entropy(logits, labels) do?
- Compares predictions via argmax
- Applies softmax and computes the logarithmic loss
- Computes accuracy on the test set
- Normalizes image pixels
* Correct answer: Applies softmax and computes the logarithmic loss
Softmax is combined with the loss, so you don't need to apply it separately in the network, and the label is passed as an integer class index.

What is an epoch in neural network training?
- One weight update step
- A full pass over the entire training set
- One batch of data
- A pass over the test set only
* Correct answer: A full pass over the entire training set
An epoch ends when the model has seen every training example once. Training usually runs for several epochs.

Why evaluate the model on a separate test set?
- To speed up training
- To check how well the model generalizes to new data rather than just memorizing the training data
- To pick the batch size
- To update the weights after training
* Correct answer: To check how well the model generalizes to new data rather than just memorizing the training data
If training accuracy is high but test accuracy is low, that's overfitting: the model memorized the examples rather than the pattern.
<!--/QUIZ-->
