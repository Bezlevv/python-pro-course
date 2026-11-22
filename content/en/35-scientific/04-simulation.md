---
title: Simulations: Monte Carlo
summary: How to estimate integrals and probabilities with random trials: 1/√N convergence, seeds, reproducibility, and simple ways to reduce variance.
order: 4
duration: 40 min
difficulty: advanced
tags: simulations, Monte Carlo, randomness
---

The Monte Carlo method is a universal numerical technique: instead of an exact formula, we repeatedly play out randomness and average the result. It saves the day where analytical derivation is impossible: complex integrals, risk models, particle physics, finance. The name refers to the Monte Carlo casino — randomness lies at the heart of the method.

## The idea: estimation as an average

Suppose we want to estimate a quantity that is the expectation of some function of a random variable. If we can generate a sample X₁, …, X_N, the estimate is the ordinary mean:

```
(1/N) · Σ f(Xᵢ)
```

By the law of large numbers, the mean converges to the expectation as N → ∞. The convergence rate is 1/√N: to halve the error, you need to quadruple the number of trials.

## Estimating π

A classic example: throw points into the square [0,1]² and count what fraction lands in a quarter circle. The area of a quarter circle is π/4, so π ≈ 4 · (hits / total):

```python
import numpy as np

def estimate_pi(n, seed=0):
    rng = np.random.default_rng(seed)
    x = rng.uniform(0, 1, n)
    y = rng.uniform(0, 1, n)
    inside = (x**2 + y**2) <= 1
    return 4 * inside.mean()

print(estimate_pi(100_000))
```

In `x**2 + y**2 <= 1` — a vectorized comparison: NumPy computes the mask for all points at once, and `inside.mean()` is the fraction of ones. The result is about 3.14, and the larger n, the closer to π.

## Monte Carlo integration

The same technique computes any integrals. ∫₀^π sin(x) dx = 2. A random point U from U(0, π), then the estimate is the mean of f(U)·(π − 0):

```python
def mc_integral_sin(n, seed=0):
    rng = np.random.default_rng(seed)
    u = rng.uniform(0, np.pi, n)
    return np.sin(u).mean() * np.pi

print(mc_integral_sin(100_000))  # ≈ 2.0
```

Multiplying by the interval length is the key step: the mean of f(U) estimates the "average height", and multiplying by the length gives the area. The error is on the order of (b−a)·σ/√N.

## Seeds and reproducibility

Simulations must be reproducible. `default_rng(seed)` gives a deterministic sequence: the same seed → the same result. This allows writing tests: functions with a fixed seed return the same numbers.

## Not only integrals: event probabilities

Monte Carlo also estimates probabilities. What is the probability that the sum of two dice equals 7? Theory says 6/36 = 1/6 ≈ 0.1667. Let's play out 10,000 pairs:

```python
def prob_sum_seven(n, seed=0):
    rng = np.random.default_rng(seed)
    a = rng.integers(1, 7, n)
    b = rng.integers(1, 7, n)
    return ((a + b) == 7).mean()

print(prob_sum_seven(10_000))
```

`rng.integers(1, 7, n)` generates integers from 1 to 6 inclusive (the right end is excluded). The estimate will fluctuate around 1/6.

## How to improve accuracy

The main way is more trials, but there are also "free" techniques:

- **Stratification / Latin hypercubes**: cover the region uniformly instead of chaotic throws;
- **Antithetic variates**: use pairs of U and 1−U, which reduce the spread;
- **Control variates**: subtract from the function a "near-integral" that is computed analytically.

In practice, it is most often enough to just increase N and watch the seed.

## Error estimation

The error of a Monte Carlo estimate can be assessed experimentally: it equals the standard deviation of the sample mean, i.e., σ_f/√N, where σ_f is the standard deviation of the values f(X). This gives a practical rule: to get three significant digits, you need about a million trials, and for six — a billion. From this also comes the "compare with the theoretical answer" technique: if you have an exact value (like π or 2 for the sine integral), always cross-check the estimate against it. If the discrepancy is larger than the expected error — look for a bug in the simulation, not in the math.

Another useful consequence: a Monte Carlo estimate is itself a random variable, so it is good to accompany it with a confidence interval (for example, ±1.96·σ/√N). In the exercises we will limit ourselves to a point estimate and tolerance checks, but in real projects the interval is a mandatory part of the result.

## When Monte Carlo is indispensable

There are problems where random trials are the only practical way to get an answer. Let's name the main ones: high-dimensional integrals (with 50 variables, grid methods require 50-dimensional grids — impossible, while Monte Carlo is independent of dimensionality); problems with parameter uncertainty (portfolio risks, structural reliability); complex stochastic systems (queues, epidemics, market processes). In all three cases the price of the solution is only computation time, which grows slowly, as 1/√N.

## Where it is applied

Risk assessment and Value-at-Risk in finance, traffic modeling in networks, radiation physics, optimization of complex systems. The recipe is one: express the answer as an expectation, play out randomness, average. Now let's practice.

<!--TASK-->
### Task 1
Write a function `estimate_pi(n, seed)` in the file `montecarlo.py` that estimates π by the Monte Carlo method: it throws n random points into the square [0, 1]² and returns 4 · the fraction of points inside the quarter circle (formula `x**2 + y**2 <= 1`). Call it with n = 100,000 and seed 42, print the result. Run: the number should be between 3.13 and 3.15.

### Task 2
Write a function `mc_integral_sin(n, seed)` that estimates ∫₀^π sin(x) dx by the Monte Carlo method and returns the estimate. Call it with n = 100,000, seed 1 and print the result. The true value is 2.0; make sure the result differs from 2 by less than 0.05.

### Task 3
Write a function `prob_sum_seven(n, seed)` that simulates n throws of two dice (`rng.integers(1, 7, n)`) and returns an estimate of the probability of a sum of 7. Call it with n = 10,000, seed 5 and print the result. Compare with the theoretical value 1/6 ≈ 0.1667 — the discrepancy should be less than 0.02.

### Task 4
Create a file `test_montecarlo.py`. First test: `estimate_pi(100_000, 42)` returns a value between 3.13 and 3.15. Second test (reproducibility): `estimate_pi(50_000, 7)` gives exactly the same result when called again with the same seed. Run pytest.

### Task 5
In the same file `test_montecarlo.py` add a convergence check: let `small = abs(mc_integral_sin(500, 1) - 2.0)`, and `large = abs(mc_integral_sin(50_000, 1) - 2.0)`. The test checks that `large < small`. Also add a test that `prob_sum_seven(50_000, 3)` differs from 1/6 by less than 0.01. Run pytest — all four tests should pass.
<!--/TASK-->

<!--HINT-->
### Hint 1
Create the generator once inside the function: `rng = np.random.default_rng(seed)`. Arrays x and y — via `rng.uniform(0, 1, n)`. The fraction of hits is given by `inside.mean()` — the mean method of a boolean array.

### Hint 2
The mean `np.sin(u).mean()` is multiplied by the interval length `np.pi`. Don't forget to create the uniform array exactly on [0, π]: `rng.uniform(0, np.pi, n)`.

### Hint 3
`rng.integers(1, 7, n)` returns integers from 1 to 6. Compute the sum as `a + b`, and the fraction of desired sums as `((a + b) == 7).mean()`.

### Hint 4
Write tests like `def test_pi_in_range(): assert 3.13 < estimate_pi(100_000, 42) < 3.15`. For reproducibility: `assert estimate_pi(50_000, 7) == estimate_pi(50_000, 7)`.

### Hint 5
In the convergence test wrap `abs(...)` around each call. For the dice sum: `assert abs(prob_sum_seven(50_000, 3) - 1/6) < 0.01`. Remember: the seeds in the tests are fixed so the results don't "float".
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
File `montecarlo.py`:

```python
import numpy as np

def estimate_pi(n, seed):
    rng = np.random.default_rng(seed)
    x = rng.uniform(0, 1, n)
    y = rng.uniform(0, 1, n)
    inside = (x**2 + y**2) <= 1
    return 4 * inside.mean()

print(estimate_pi(100_000, 42))
```

Result (approximately):

```
3.14152
```

What's happening here? A point (x, y) in the square [0,1]² falls into the quarter circle if x² + y² ≤ 1. The fraction of such points estimates the ratio of areas — π/4. Multiplying by 4 gives an estimate of π. With 100,000 points the error is on the order of 0.005 — hence the tolerance 3.13…3.15: it is several times wider than the actual spread.

### Solution 2
Add to `montecarlo.py`:

```python
def mc_integral_sin(n, seed):
    rng = np.random.default_rng(seed)
    u = rng.uniform(0, np.pi, n)
    return np.sin(u).mean() * np.pi
```

Call:

```python
print(mc_integral_sin(100_000, 1))
```

Result (approximately):

```
1.99929
```

What's happening here? The estimate of the integral is the mean of the function at random points multiplied by the interval length. The error is ~ (b−a)·σ_f/√N: at N = 100,000 it is about 0.003, far below the tolerance of 0.05. Interestingly, the method does not use derivatives — only function values.

### Solution 3
Add:

```python
def prob_sum_seven(n, seed):
    rng = np.random.default_rng(seed)
    a = rng.integers(1, 7, n)
    b = rng.integers(1, 7, n)
    return ((a + b) == 7).mean()
```

Call:

```python
print(prob_sum_seven(10_000, 5))
```

Result (approximately):

```
0.1664
```

What's happening here? Of the 36 equally likely outcomes of six-sided dice, six give a sum of 7: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1). The estimate over 10,000 pairs (0.1664) differs from 1/6 = 0.1667 by only 0.0003. The method estimates probabilities the same way as integrals — through frequencies.

### Solution 4
File `test_montecarlo.py`:

```python
from montecarlo import estimate_pi

def test_pi_in_range():
    assert 3.13 < estimate_pi(100_000, 42) < 3.15

def test_pi_reproducible():
    assert estimate_pi(50_000, 7) == estimate_pi(50_000, 7)
```

Result: `2 passed`. What's happening here? The first test checks substantive accuracy: the estimate of π with 100,000 points will almost surely be between 3.13 and 3.15. The second test checks reproducibility: with a fixed seed the second call gives a bitwise identical result. Without a seed the test would be nondeterministic — and that is the main reason to always fix the seed in simulations.

### Solution 5
Extend `test_montecarlo.py`:

```python
from montecarlo import mc_integral_sin, prob_sum_seven

def test_convergence():
    small = abs(mc_integral_sin(500, 1) - 2.0)
    large = abs(mc_integral_sin(50_000, 1) - 2.0)
    assert large < small

def test_dice_probability():
    assert abs(prob_sum_seven(50_000, 3) - 1/6) < 0.01
```

Result: `4 passed`. What's happening here? The convergence test shows the main property of the method: the larger N, the smaller the error. With 50,000 points the error will almost surely be smaller than with 500. The dice sum probability test checks the frequency estimate: with 50,000 trials the deviation from 1/6 practically never exceeds 0.01. This is how simulations become testable code.
<!--/SOLUTION-->

<!--QUIZ-->
What is the essence of the Monte Carlo method?
- Repeatedly playing out randomness and averaging
- Solving equations analytically
- Trying all variants
- Using function derivatives
* Correct answer: Repeatedly playing out randomness and averaging
The estimate is the mean of the function values over random points.

How does the error of a Monte Carlo estimate decrease?
- As 1/√N
- As 1/N
- Exponentially
- It does not decrease
* Correct answer: As 1/√N
To halve the error, you need to quadruple N.

How to estimate π by the Monte Carlo method?
- 4 · the fraction of points inside the quarter circle
- 2 · the fraction of points inside the circle
- π · the fraction of points
- 1/4 · the fraction of points
* Correct answer: 4 · the fraction of points inside the quarter circle
The quarter circle area is π/4 of the square area.

Why is a seed needed in simulations?
- For reproducibility of results
- For speed
- For reducing the error
- For switching to other distributions
* Correct answer: For reproducibility of results
The seed fixes the sequence of random numbers.

How to estimate the integral ∫₀^π sin(x) dx by the Monte Carlo method?
- The mean of sin(U) · π, where U is from U(0, π)
- The mean of sin(U)
- The sum of sin(U)
- π · the sum of sin(U)
* Correct answer: The mean of sin(U) · π, where U is from U(0, π)
Multiplying by the interval length turns the mean into the area.

What does rng.integers(1, 7, n) return?
- Integers from 1 to 6 inclusive
- Integers from 1 to 7 inclusive
- Real numbers from 1 to 7
- Integers from 0 to 6
* Correct answer: Integers from 1 to 6 inclusive
The right end 7 is not included in the range.

What is the theoretical probability of a sum of 7 on two dice?
- 1/6
- 1/12
- 1/36
- 1/2
* Correct answer: 1/6
Six of 36 outcomes give a sum of 7.

What does (x**2 + y**2) <= 1 do in NumPy?
- Creates an array of boolean values
- Returns a single number
- Computes an integral
- Rounds numbers
* Correct answer: Creates an array of boolean values
The comparison is applied elementwise to all points at once.

Which technique reduces the variance of an estimate?
- Using antithetic variates
- Decreasing N
- Removing the seed
- Using a smaller interval
* Correct answer: Using antithetic variates
Pairs of U and 1−U compensate each other, reducing the spread.

Why does the same seed give the same result?
- The sequence of random numbers is deterministic
- The seed speeds up computations
- The seed changes the distribution
- The seed disables randomness
* Correct answer: The sequence of random numbers is deterministic
Default_rng(seed) generates a fixed sequence.
<!--/QUIZ-->
