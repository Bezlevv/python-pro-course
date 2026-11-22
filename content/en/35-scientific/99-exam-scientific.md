---
title: Exam: Scientific computing
summary: Test your knowledge of the "Scientific computing" module: SciPy, statsmodels, probability, Monte Carlo simulations, signals, and optimization.
order: 99
duration: 30 min
difficulty: advanced
tags: exam
exam: true
---

<!--QUIZ-->
Which SciPy submodule is responsible for optimization?
- scipy.optimize
- scipy.integrate
- scipy.interpolate
- scipy.stats
* Correct answer: scipy.optimize
minimize, curve_fit, and linprog live in scipy.optimize.

What does quad return?
- A tuple (integral value, error estimate)
- Only the integral value
- An array of points
- The integrand function
* Correct answer: A tuple (integral value, error estimate)
quad returns the value and an estimate of the absolute error.

What does a p-value below 0.05 mean in regression?
- The coefficient is statistically significant
- The model is wrong
- The residuals are normal
- R² is high
* Correct answer: The coefficient is statistically significant
A small p-value is evidence against the null hypothesis of a zero coefficient.

What is sm.add_constant(x) for?
- For adding an intercept to the regression
- For removing missing values
- For normalization
- For speed
* Correct answer: For adding an intercept to the regression
Without a column of ones the model passes through the origin.

How does the error of a Monte Carlo estimate decrease?
- As 1/√N
- As 1/N
- Exponentially
- It does not decrease
* Correct answer: As 1/√N
To halve the error you need to quadruple N.

Why fix the seed in simulations?
- For reproducibility of results
- For speed
- For reducing the error
- For switching to other distributions
* Correct answer: For reproducibility of results
The same seed gives the same sequence of random numbers.

What does numpy.fft.fft do?
- Decomposes a signal into frequencies
- Averages a signal
- Filters noise
- Finds peaks
* Correct answer: Decomposes a signal into frequencies
FFT turns a signal into a spectrum — complex amplitudes of frequencies.

Which filter passes frequencies below a threshold?
- A low-pass filter
- A high-pass filter
- A band-pass filter
- A notch filter
* Correct answer: A low-pass filter
btype="low" in butter means a low-pass filter.

What does scipy.optimize.linprog solve?
- Linear programming
- Nonlinear optimization
- Curve fitting
- Global optimization
* Correct answer: Linear programming
linprog minimizes a linear function under linear constraints.

What does curve_fit return?
- A tuple (popt, pcov)
- Only popt
- The number of iterations
- A list of residuals
* Correct answer: A tuple (popt, pcov)
popt is the optimal model parameters, pcov is the covariance matrix.
<!--/QUIZ-->
