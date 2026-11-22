---
title: Probability and statistics in Python
summary: scipy.stats distributions, NumPy random generation, descriptive statistics, the central limit theorem, and hypothesis testing.
order: 3
duration: 35 min
difficulty: intermediate
tags: probability, statistics, scipy.stats
---

Statistics is the science of drawing conclusions from data under uncertainty. Python provides two powerful toolkits for this: the NumPy random number generator (`numpy.random`) for simulations and `scipy.stats` for theoretical distributions and tests. In this lesson we will combine them.

## Random numbers: numpy.random

The modern way to generate randomness is a generator object with an explicit seed:

```python
import numpy as np

rng = np.random.default_rng(42)
a = rng.normal(0, 1, 1000)      # 1000 numbers from N(0, 1)
b = rng.uniform(0, 1, 1000)     # 1000 numbers from U(0, 1)
c = rng.integers(1, 7, size=12) # 12 dice rolls (1..6)
```

The seed `42` fixes the sequence: with the same seed and the same calls, the results repeat. This is critical for reproducible experiments.

## Descriptive statistics

Simple metrics help make sense of a sample:

```python
print(a.mean(), a.std(), np.median(a))
print(np.percentile(a, [25, 50, 75]))
```

`scipy.stats` has the `describe` function that collects everything at once:

```python
from scipy.stats import describe

res = describe(a)
print(res.nobs, res.mean, res.variance)
print(res.skewness, res.kurtosis)
```

## Distributions: scipy.stats

Each theoretical model has a class with four key methods:

- `pdf(x)` — density (for continuous) or `pmf(k)` — point probability (for discrete);
- `cdf(x)` — cumulative distribution function: P(X ≤ x);
- `ppf(q)` — inverse function: quantile;
- `interval(0.95)` — confidence interval.

Example: for a standard normal variable:

```python
from scipy.stats import norm

print(norm.cdf(1.96))          # ≈ 0.975
print(norm.ppf(0.975))         # ≈ 1.96
print(norm.interval(0.95))     # (-1.96, 1.96)
```

The binomial distribution — the number of successes in n trials:

```python
from scipy.stats import binom

# probability of exactly 3 successes out of 10 with p = 0.5
print(binom.pmf(3, 10, 0.5))
# probability of at least 8 successes
print(1 - binom.cdf(7, 10, 0.5))
```

The Poisson distribution models the number of events in a fixed time interval: `poisson.pmf(k, mu)`.

## Central limit theorem

If you take samples and average them, the means approach a normal distribution — whatever the original distribution is. Let's check:

```python
rng = np.random.default_rng(0)
means = [rng.uniform(0, 1, 30).mean() for _ in range(2000)]
print(np.std(means))   # ≈ σ / √n = (1/√12) / √30 ≈ 0.0527
```

The standard deviation of the means decreases as 1/√n — this explains why larger samples give more accurate estimates.

## Hypothesis testing: the t-test

A hypothesis is a statement about a distribution parameter, for example "the mean is 0". The t-test compares a sample mean with a hypothetical value:

```python
from scipy.stats import ttest_1samp

sample = rng.normal(0.3, 1, 100)
t_stat, p_value = ttest_1samp(sample, 0)
print(t_stat, p_value)   # p < 0.05 — we reject "the mean is 0"
```

A p-value is the probability of obtaining the same statistic if the hypothesis is true. If p < 0.05, it is customary to reject the hypothesis; if greater — there is not enough data to conclude.

## Discrete and continuous distributions

It is important to distinguish the two families. For discrete distributions (binomial, Poisson) the variable takes separate values, and the probability of each point is given by `pmf` — the probability mass function. For continuous ones (normal, uniform) the value is any real number, the probability of a single point is zero, so the density `pdf` is used and probabilities only through intervals: `cdf(b) - cdf(a)`. This is the difference between `binom.pmf(3, 10, 0.5)` — "exactly 3 successes" — and `norm.cdf(1.96)`: "no more than 1.96". Don't confuse these methods: taking `pdf` for a discrete distribution is a common beginner mistake.

It is also useful to know that distributions have numeric characteristics obtainable via class methods: `mean()`, `var()`, `std()`. For the binomial distribution they match the formulas n·p, n·p·(1−p), and their square root. In the following lessons we will use these characteristics to verify simulations: if the mean of a simulated sample diverges strongly from `binom.mean(n, p)`, there is an error in the data generation.

All this is the foundation: next we will build simulations on top of it and test real data.

<!--TASK-->
### Task 1
Using `np.random.default_rng(7)`, generate a sample of 5000 numbers from a normal distribution with mean 3 and standard deviation 2 (`rng.normal(3, 2, 5000)`). Print the sample mean and standard deviation (methods `mean()` and `std()`). Run the program: the mean should be close to 3, and the standard deviation close to 2.

### Task 2
Compute the following probabilities for a standard normal variable Z via `scipy.stats.norm` and print them one per line: 1) P(Z ≤ 0) — `norm.cdf(0)`; 2) P(Z ≤ 1.96); 3) P(−1.96 ≤ Z ≤ 1.96) — via the difference of cdfs; 4) the quantile `norm.ppf(0.975)`. Run the program and make sure the first value is exactly 0.5, and the second and fourth match (≈ 0.975 and ≈ 1.96).

### Task 3
A coin is tossed 10 times. Compute with `scipy.stats.binom` and print: 1) the probability of exactly 5 heads — `binom.pmf(5, 10, 0.5)`; 2) the probability of at least 8 heads — `1 - binom.cdf(7, 10, 0.5)`; 3) the expected number of heads — `binom.mean(10, 0.5)`. Run: the first value ≈ 0.246, the second ≈ 0.0547, the third is exactly 5.0.

### Task 4
Verify the central limit theorem. Create a file `clt_lab.py` with a function `sample_means_std(n_samples=2000, sample_size=30, seed=0)`: it generates the specified number of samples of `sample_size` numbers from U(0, 1) via `np.random.default_rng(seed)` and returns the standard deviation of their means. Print the result for the default values. Then create `test_clt_lab.py` with two tests: the first checks that the value lies between 0.045 and 0.06 (theoretical — (1/√12)/√30 ≈ 0.0527); the second — that calling again with the same seed gives exactly the same result. Run pytest.

### Task 5
Create a file `stats_lab.py` with a function `ttest_shift(mean_shift, seed)`: it generates a sample of 100 numbers `rng.normal(mean_shift, 1, 100)` via `np.random.default_rng(seed)` and returns the p-value from `scipy.stats.ttest_1samp(sample, 0)`. Then create `test_stats_lab.py` with two tests: with `mean_shift=0` the p-value should be greater than 0.05; with `mean_shift=0.5` — less than 0.05. Run pytest.
<!--/TASK-->

<!--HINT-->
### Hint 1
A NumPy array has `mean()` and `std()` methods that compute over the whole sample. The generator is created once: `rng = np.random.default_rng(7)`.

### Hint 2
`norm.cdf(x)` returns the probability P(Z ≤ x). For the interval [−1.96, 1.96] take the difference: `norm.cdf(1.96) - norm.cdf(-1.96)`. `norm.ppf(0.975)` is the inverse CDF function.

### Hint 3
`binom.pmf(k, n, p)` is the probability of exactly k successes; `binom.cdf(k, n, p)` is the probability of no more than k successes. "At least 8" is 1 − P(≤ 7). The method `binom.mean(n, p)` returns n·p.

### Hint 4
Inside the function create the generator via `np.random.default_rng(seed)` and the list of means via a list comprehension: `[rng.uniform(0, 1, sample_size).mean() for _ in range(n_samples)]`. The standard deviation is `np.std(...)`. In the test use `assert 0.045 < sample_means_std() < 0.06` and `assert sample_means_std(seed=7) == sample_means_std(seed=7)`.

### Hint 5
`ttest_1samp` returns a tuple `(t_stat, p_value)` — return the p_value. In the test: `assert ttest_shift(0, 1) > 0.05` and `assert ttest_shift(0.5, 1) < 0.05`. Different seeds should not affect the conclusion.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
import numpy as np

rng = np.random.default_rng(7)
sample = rng.normal(3, 2, 5000)
print(sample.mean())
print(sample.std())
```

Result (approximately):

```
2.99
1.99
```

What's happening here? The empirical characteristics of a large sample converge to the distribution parameters: mean → 3, standard deviation → 2. The discrepancy of hundredths is a normal statistical fluctuation: the larger the sample, the smaller it is.

### Solution 2
Solution:

```python
from scipy.stats import norm

print(norm.cdf(0))
print(norm.cdf(1.96))
print(norm.cdf(1.96) - norm.cdf(-1.96))
print(norm.ppf(0.975))
```

Result:

```
0.5
0.9750021048517795
0.950004209703559
1.959963984540054
```

What's happening here? cdf accumulates probability to the left of a point: for a symmetric distribution P(Z ≤ 0) = 0.5. The value 1.96 is a well-known threshold: between ±1.96 lies 95% of the mass of the normal distribution. The quantile `ppf(0.975)` returns exactly the number to the left of which 97.5% of the probability lies — and that is 1.96. The inverse `ppf` and forward `cdf` functions are mutually inverse.

### Solution 3
Solution:

```python
from scipy.stats import binom

print(binom.pmf(5, 10, 0.5))
print(1 - binom.cdf(7, 10, 0.5))
print(binom.mean(10, 0.5))
```

Result:

```
0.24609375
0.0546875
5.0
```

What's happening here? pmf(5, 10, 0.5) = C(10,5) / 2¹⁰ = 252 / 1024 ≈ 0.246 — the probability of exactly half heads. The probability of "at least 8" is the sum pmf(8) + pmf(9) + pmf(10) = (45 + 10 + 1) / 1024 ≈ 0.0547. The expectation of a binomial variable is n·p = 5. Note the difference between pmf (probability of a specific point) and cdf (probability of "no more than").

### Solution 4
File `clt_lab.py`:

```python
import numpy as np

def sample_means_std(n_samples=2000, sample_size=30, seed=0):
    rng = np.random.default_rng(seed)
    means = [rng.uniform(0, 1, sample_size).mean() for _ in range(n_samples)]
    return np.std(means)

print(sample_means_std())
```

File `test_clt_lab.py`:

```python
from clt_lab import sample_means_std

def test_clt_std_in_range():
    assert 0.045 < sample_means_std() < 0.06

def test_reproducible():
    assert sample_means_std(seed=7) == sample_means_std(seed=7)
```

Result: `2 passed`. What's happening here? The means of samples of size 30 from U(0, 1) are almost normally distributed (central limit theorem), and their standard deviation is the standard error σ/√n. For the uniform distribution σ = 1/√12 ≈ 0.2887, so the theoretical value — 0.2887/√30 ≈ 0.0527 — fits the tolerance [0.045, 0.06] perfectly. The second test checks reproducibility: the seed fixes the sequence, so two calls give a bitwise identical result. This is how simulations become testable code.

### Solution 5
File `stats_lab.py`:

```python
import numpy as np
from scipy.stats import ttest_1samp

def ttest_shift(mean_shift, seed):
    rng = np.random.default_rng(seed)
    sample = rng.normal(mean_shift, 1, 100)
    t_stat, p_value = ttest_1samp(sample, 0)
    return p_value
```

File `test_stats_lab.py`:

```python
from stats_lab import ttest_shift

def test_no_shift_not_significant():
    assert ttest_shift(0, 1) > 0.05

def test_shift_significant():
    assert ttest_shift(0.5, 1) < 0.05
```

Result: `2 passed`. What's happening here? With a true mean of 0 the null hypothesis is true, and the p-value is almost always greater than 0.05 — the test does not see an effect where there is none. With a mean of 0.5 (a shift of half a standard deviation) the test confidently rejects the hypothesis: p < 0.05. That is what honest hypothesis testing looks like: the p-value is not "the probability that the hypothesis is true", but a measure of how incompatible the data are with it.
<!--/SOLUTION-->

<!--QUIZ-->
Which class from scipy.stats describes the normal distribution?
- norm
- binom
- poisson
- uniform
* Correct answer: norm
norm provides pdf, cdf, ppf, and interval methods for the normal distribution.

What does norm.cdf(x) return?
- The probability P(Z ≤ x)
- The density at point x
- A quantile
- A random number
* Correct answer: The probability P(Z ≤ x)
cdf is the cumulative distribution function: the probability that the variable does not exceed x.

What does norm.cdf(0) equal for a standard normal variable?
- 0.5
- 0
- 1
- 0.95
* Correct answer: 0.5
The distribution is symmetric about zero, so exactly half the mass lies to the left of zero.

Why is a seed needed for np.random.default_rng?
- To reproducibly repeat generation
- To speed up computations
- To remove repeating numbers
- To change the distribution
* Correct answer: To reproducibly repeat generation
With the same seed, the sequence of random numbers repeats.

What does the binomial distribution describe?
- The number of successes in n independent trials
- The time between events
- A continuous variable
- A measurement error
* Correct answer: The number of successes in n independent trials
binom models the number of successes with a fixed probability p in each trial.

How to compute the probability of "at least 8 successes out of 10"?
- 1 - binom.cdf(7, 10, 0.5)
- binom.cdf(8, 10, 0.5)
- binom.pmf(8, 10, 0.5)
- 1 - binom.pmf(8, 10, 0.5)
* Correct answer: 1 - binom.cdf(7, 10, 0.5)
"At least 8" is the complement of "no more than 7".

What does the central limit theorem state?
- Sample means tend to a normal distribution
- Any data is normally distributed
- Variance is always finite
- The mean equals the median
* Correct answer: Sample means tend to a normal distribution
Regardless of the original distribution, means over large samples are nearly normal.

How does the standard error decrease as the sample size n grows?
- As 1/√n
- As 1/n
- Linearly
- It does not decrease
* Correct answer: As 1/√n
The standard deviation of the mean is σ/√n — to halve the error, you need to quadruple the sample.

What does ttest_1samp return?
- A tuple (t-statistic, p-value)
- Only the p-value
- A set of quantiles
- A confidence interval
* Correct answer: A tuple (t-statistic, p-value)
ttest_1samp returns two quantities: the test statistic and the p-value.

At what p-value is it customary to reject the null hypothesis?
- p < 0.05
- p > 0.05
- p = 0.5
- p > 0.95
* Correct answer: p < 0.05
The 0.05 threshold is the standard significance level in science.
<!--/QUIZ-->
