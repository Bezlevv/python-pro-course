---
title: statsmodels: regressions and statistical tests
summary: Statistical modeling in Python: linear regression, inference about coefficients, residual diagnostics, and hypothesis testing.
order: 2
duration: 40 min
difficulty: advanced
tags: statsmodels, regression, statistical tests
---

In the previous lesson we learned to solve mathematical problems numerically. But in data we are interested in something else: how quantities are related, how strong the relationship is, and whether it can be trusted. The library `statsmodels` is the standard for statistical modeling in Python: it builds regressions, outputs p-values, confidence intervals, and diagnostic tests. Installation: `pip install statsmodels`.

## Synthetic data

To see whether the model works "correctly", let's generate data with a known relationship: y = 2 + 3x + noise.

```python
import numpy as np

rng = np.random.default_rng(42)
x = rng.uniform(0, 10, 200)
y = 2 + 3 * x + rng.normal(0, 1, 200)
```

We know the true solution: intercept 2, slope 3. The regression should recover these numbers approximately.

## First regression: statsmodels.api.OLS

The main interface is `statsmodels.api`. The `OLS` model (ordinary least squares) is assembled from a feature matrix and a response vector, and `fit()` trains it:

```python
import statsmodels.api as sm

X = sm.add_constant(x)      # add a column of ones — the intercept
model = sm.OLS(y, X)
results = model.fit()

print(results.params)        # [intercept, slope]
print(results.rsquared)      # proportion of explained variance
```

`add_constant` is required if we want a free term: without it the regression will go through the origin. Result fields: `params` — coefficients, `bse` — their standard errors, `pvalues` — p-values, `conf_int()` — confidence intervals.

## Report: results.summary()

A nice text report is printed with a single call:

```python
print(results.summary())
```

The table contains coefficients, standard errors, t-statistics, p-values, R², and the F-test of the model as a whole. Reading such a report is a basic analyst skill.

## Formula interface

For complex models, an R-style formula syntax is more convenient:

```python
import pandas as pd
from statsmodels.formula.api import ols

df = pd.DataFrame({"x": x, "y": y})
model = ols("y ~ x", data=df).fit()
print(model.params)
```

The string `"y ~ x"` reads as "y is explained by x". For multiple features: `"y ~ x1 + x2"`, for interactions: `"y ~ x1 * x2"`. Inside a pandas DataFrame, categorical columns are automatically converted to dummy variables.

## Statistical tests: hypothesis testing

statsmodels can not only estimate but also test hypotheses. The key object is the p-value: the probability of obtaining the same or a more extreme statistic value if the null hypothesis is true. The usual threshold is 0.05.

Let's check that the regression residuals are normally distributed — this is a prerequisite for the tests:

```python
from statsmodels.stats.diagnostic import jarque_bera

jb_stat, jb_pvalue = jarque_bera(results.resid)
print(jb_stat, jb_pvalue)
```

If the p-value is greater than 0.05, we do not reject the normality of the residuals.

To compare the means of two samples there is the t-test (it can be taken from `scipy.stats`):

```python
from scipy.stats import ttest_ind

a = rng.normal(0, 1, 100)
b = rng.normal(0.5, 1, 100)
t_stat, p_value = ttest_ind(a, b)
print(t_stat, p_value)   # p_value < 0.05 — the means differ
```

## Prediction

A trained model can predict on new data:

```python
X_new = sm.add_constant(np.array([1.0, 5.0, 9.0]))
pred = results.predict(X_new)
print(pred)
```

`predict` takes a matrix with the same number of columns (including the constant). For the `ols` result it is simpler to pass a DataFrame with the needed columns.

## Diagnostics

Good analysis does not end with the coefficients. Things checked:

- significance of coefficients: p-values in `pvalues`;
- goodness of fit: R², adjusted R² (`rsquared_adj`);
- residuals: plots of `results.resid`, the Jarque–Bera test for normality, the Breusch–Pagan test for heteroskedasticity (`het_breuschpagan`);
- influential observations: `results.get_influence()`.

This is the foundation of statistical inference: a model is not just numbers, but a tool for testing hypotheses about the world.

<!--TASK-->
### Task 1
Generate data with a known relationship: x from a uniform distribution on [0, 10], y = 5 + 2x + noise (normal, σ = 1), seed 2024. Fit a linear regression via `sm.OLS` with `sm.add_constant`. Print two lines: the coefficients (`results.params`) and R² (`results.rsquared`). Run the program: the slope should be close to 2, the intercept — to 5, and R² — above 0.9.

### Task 2
Using the same dataset, build a model via the formula interface `statsmodels.formula.api.ols("y ~ x", data=df)`. Print the following values: `params` (coefficients), `pvalues` (p-values), and `rsquared`. Make sure the p-value for x is less than 0.05 — meaning the relationship is statistically significant.

### Task 3
After fitting the OLS model, compute the residuals (`results.resid`). Check their normality with the Jarque–Bera test: `jarque_bera(results.resid)`. Print the statistic and p-value. Run the program several times with different seeds and observe: usually the p-value is greater than 0.05, i.e., the normality of residuals is not rejected.

### Task 4
Create a file `regression.py` with a function `fit_line(x, y)` that fits an OLS regression of y on x (with a constant) and returns a tuple `(intercept, slope)` — the coefficients in the order `(params[0], params[1])`. Then create `test_regression.py`: on noise-free data y = 2x + 1 (x = np.arange(5)) the test checks that `intercept` and `slope` differ from 1 and 2 by less than 1e-6. Run pytest.

### Task 5
In the file `test_regression2.py` write two tests for the function `fit_line` from `regression.py`. First: on noisy data (seed 7, x from uniform(0, 10), y = 3 + 4x + N(0, 1)) the test checks that the slope `slope` lies between 3.5 and 4.5. Second: on the same data the test checks that the p-value for the coefficient of x (from `results.pvalues[1]`) is less than 0.05. For this, `fit_line` must also return the full model result — change the return value to `(results, intercept, slope)` and fix the test from task 4.
<!--/TASK-->

<!--HINT-->
### Hint 1
Don't forget `sm.add_constant(x)` — without it there will be no intercept and the coefficients will be distorted. `results.params` is a NumPy array of two numbers; you can print it as is. Add noise via `rng.normal(0, 1, n)`.

### Hint 2
Formula interface: `from statsmodels.formula.api import ols`, then `model = ols("y ~ x", data=df).fit()`. `df` is a pandas DataFrame with columns `x` and `y`. The names in the formula must match the column names.

### Hint 3
`jarque_bera` is imported from `statsmodels.stats.diagnostic` and takes a one-dimensional array of residuals. The function returns a tuple: `(statistic, pvalue)`. Unpack it into two variables and print.

### Hint 4
Inside `fit_line`: `X = sm.add_constant(x)`, `results = sm.OLS(y, X).fit()`, return `(results.params[0], results.params[1])`. In the test compare via `abs(intercept - 1) < 1e-6` and `abs(slope - 2) < 1e-6`.

### Hint 5
The second test needs access to `results.pvalues`. Return from `fit_line` the tuple `(results, intercept, slope)`, then unpack three values in the tests. In the first test use `assert 3.5 < slope < 4.5`; in the second — `assert results.pvalues[1] < 0.05`. Don't forget to fix the test from task 4 for three values.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
import numpy as np
import statsmodels.api as sm

rng = np.random.default_rng(2024)
x = rng.uniform(0, 10, 200)
y = 5 + 2 * x + rng.normal(0, 1, 200)

X = sm.add_constant(x)
results = sm.OLS(y, X).fit()
print(results.params)
print(results.rsquared)
```

Result (approximately):

```
[5.04 1.99]
0.978
```

What's happening here? We know the true coefficients: intercept 5, slope 2. The method of least squares recovers them from a noisy sample, and the estimates are very close to the truth. R² ≈ 0.978 means the model explains almost 98% of the variability of y — the rest is noise. The larger the sample and the smaller σ, the more accurate the estimates.

### Solution 2
Solution:

```python
import numpy as np
import pandas as pd
from statsmodels.formula.api import ols

rng = np.random.default_rng(2024)
x = rng.uniform(0, 10, 200)
y = 5 + 2 * x + rng.normal(0, 1, 200)
df = pd.DataFrame({"x": x, "y": y})

model = ols("y ~ x", data=df).fit()
print(model.params)
print(model.pvalues)
print(model.rsquared)
```

Result (approximately):

```
Intercept    5.04
x            1.99
dtype: float64
Intercept    1.23e-62
x            3.41e-89
dtype: float64
0.978
```

What's happening here? The formula model builds the same regression, but with convenient syntax. The p-value for x is on the order of 1e-89, far below 0.05: the relationship is statistically significant. Note: in the formula result the coefficients live in `params` with the names `Intercept` and `x`, not by array indices (though you can also access them by index).

### Solution 3
Solution:

```python
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.diagnostic import jarque_bera

rng = np.random.default_rng(7)
x = rng.uniform(0, 10, 200)
y = 2 + 3 * x + rng.normal(0, 1, 200)

results = sm.OLS(y, sm.add_constant(x)).fit()
stat, pvalue = jarque_bera(results.resid)
print(stat, pvalue)
```

Result (approximately):

```
1.52 0.468
```

What's happening here? Residuals are the deviations of the model's predictions from the actual y; if the model is correct, the residuals resemble noise and are normally distributed. The Jarque–Bera statistic tests normality: when p > 0.05 we do not reject it. Here p ≈ 0.47, so the normality of residuals does not contradict the data. This is an important prerequisite for coefficient confidence intervals.

### Solution 4
File `regression.py`:

```python
import numpy as np
import statsmodels.api as sm

def fit_line(x, y):
    results = sm.OLS(y, sm.add_constant(x)).fit()
    return results.params[0], results.params[1]
```

File `test_regression.py`:

```python
import numpy as np
from regression import fit_line

def test_exact_line():
    x = np.arange(5, dtype=float)
    y = 2 * x + 1
    intercept, slope = fit_line(x, y)
    assert abs(intercept - 1) < 1e-6
    assert abs(slope - 2) < 1e-6
```

Result: `1 passed`. What's happening here? If the data lie exactly on a line, the method of least squares recovers it to computational precision. Such a test verifies the model implementation without random effects.

### Solution 5
Update `fit_line` to return the full result:

```python
def fit_line(x, y):
    results = sm.OLS(y, sm.add_constant(x)).fit()
    return results, results.params[0], results.params[1]
```

File `test_regression2.py`:

```python
import numpy as np
from regression import fit_line

def test_slope_in_range():
    rng = np.random.default_rng(7)
    x = rng.uniform(0, 10, 200)
    y = 3 + 4 * x + rng.normal(0, 1, 200)
    results, intercept, slope = fit_line(x, y)
    assert 3.5 < slope < 4.5

def test_slope_significant():
    rng = np.random.default_rng(7)
    x = rng.uniform(0, 10, 200)
    y = 3 + 4 * x + rng.normal(0, 1, 200)
    results, intercept, slope = fit_line(x, y)
    assert results.pvalues[1] < 0.05
```

Result: `2 passed`. What's happening here? The true slope is 4, and the estimate from a noisy sample falls into the interval [3.5, 4.5] with a huge margin. The p-value of 1e-90 says: the probability that the true slope is zero is negligible — the relationship is significant. Don't forget to update the test from task 4: now `fit_line` returns three values.
<!--/SOLUTION-->

<!--QUIZ-->
Why is sm.add_constant(x) needed before sm.OLS?
- To add a column of ones — the regression intercept
- To get rid of missing values
- To normalize features
- To speed up training
* Correct answer: To add a column of ones — the regression intercept
Without the constant the model passes through the origin, and the intercept is not estimated.

What is stored in results.params?
- The regression coefficients
- The residuals
- Standard errors
- Predictions
* Correct answer: The regression coefficients
params is the vector of coefficient estimates (intercept and slopes).

What does a p-value below 0.05 mean?
- The relationship is statistically significant
- The model is exactly correct
- There is no noise
- The coefficient is zero with 95% probability
* Correct answer: The relationship is statistically significant
A small p-value is strong evidence against the null hypothesis of a zero coefficient.

Which interface allows writing ols("y ~ x", data=df)?
- The formula syntax of statsmodels.formula.api
- scipy.optimize
- Matplotlib
- NumPy
* Correct answer: The formula syntax of statsmodels.formula.api
The formula "y ~ x" describes the relationship in R style.

What does R² show?
- The proportion of variance of y explained by the model
- The average prediction error
- The number of observations
- The model's p-value
* Correct answer: The proportion of variance of y explained by the model
R² goes from 0 to 1: the closer to 1, the better the model explains the data.

Which test checks the normality of residuals?
- jarque_bera
- ttest_ind
- quad
- minimize
* Correct answer: jarque_bera
jarque_bera from statsmodels.stats.diagnostic checks normality based on skewness and kurtosis.

What does results.predict(X_new) do?
- Predicts y for new observations
- Retrains the model
- Prints a report
- Computes residuals
* Correct answer: Predicts y for new observations
predict takes a feature matrix of the same dimensionality and returns predicted values.

What is the ttest_ind test for?
- For comparing the means of two samples
- For finding roots
- For integration
- For interpolation
* Correct answer: For comparing the means of two samples
The t-test checks the hypothesis about the equality of means of two independent samples.

What will OLS return on noise-free data y = 2x + 1?
- Exactly 1 and 2 (to machine precision)
- Approximate values
- An error
- Zero
* Correct answer: Exactly 1 and 2 (to machine precision)
The method of least squares on exact linear data recovers the true coefficients.

How to get confidence intervals for the coefficients?
- results.conf_int()
- results.summary()
- results.predict()
- results.resid
* Correct answer: results.conf_int()
conf_int() returns a matrix of confidence intervals for all coefficients.
<!--/QUIZ-->
