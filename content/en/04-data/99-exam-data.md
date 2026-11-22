---
title: Exam: Data Analysis
summary: Test your data analysis knowledge: NumPy, Pandas, data cleaning, Matplotlib, Seaborn, and scikit-learn.
order: 99
duration: 30 min
difficulty: advanced
tags: exam
exam: true
---

<!--QUIZ-->
What does (np.array([1, 2, 3]) + 1) output?
- [1, 2, 3, 1]
- [2, 3, 4]
- An error
- [[2], [3], [4]]
* Correct answer: [2, 3, 4]
NumPy array operations are applied element-wise to all values at once.

How many numbers does np.linspace(0, 1, 5) return?
- 4
- 5
- 6
- 10
* Correct answer: 5
linspace creates the specified number of evenly spaced numbers, including both endpoints of the range.

Which DataFrame method shows the first 5 rows?
- df.first()
- df.head()
- df.top()
- df.begin()
* Correct answer: df.head()
df.head() returns the first 5 rows of the table by default.

How do you check where a DataFrame has missing values?
- df.nan()
- df.isna()
- df.zeros()
- df.empty()
* Correct answer: df.isna()
df.isna() returns a table of True/False: True marks where a value is missing.

What does df.dropna() do?
- Removes columns with missing values
- Removes rows with missing values
- Fills missing values with zeros
- Changes nothing
* Correct answer: Removes rows with missing values
dropna() removes rows that have at least one missing value.

Which call builds a line chart?
- plt.bar(x, y)
- plt.plot(x, y)
- plt.scatter(x, y)
- plt.hist(y)
* Correct answer: plt.plot(x, y)
plt.plot connects the points with a line — the classic line chart.

What does plt.show() do?
- Saves the chart to a file
- Displays the created charts in a window
- Closes all windows
- Clears the figure
* Correct answer: Displays the created charts in a window
Without plt.show(), the chart won't appear on screen in regular scripts.

How is Seaborn's interface related to Pandas?
- It works only with plain lists
- It accepts a DataFrame directly for statistical plots
- It requires conversion to NumPy
- It is incompatible with Python
* Correct answer: It accepts a DataFrame directly for statistical plots
Seaborn is built on top of Matplotlib and accepts a DataFrame, for example: sns.countplot(data=df, x="city").

How do you read a table from a CSV file into a DataFrame?
- pd.read_csv("data.csv")
- pd.open("data.csv")
- pd.from_csv("data.csv")
- pd.load("data.csv")
* Correct answer: pd.read_csv("data.csv")
pd.read_csv is the main way to load tabular data from CSV.

Which call splits data into training and test sets?
- train_test_split(X, y, test_size=0.2)
- split_data(X, y, 0.2)
- divide(X, y, 0.2)
- model.split(X, y, 0.2)
* Correct answer: train_test_split(X, y, test_size=0.2)
train_test_split from scikit-learn randomly splits the data: 80% for training and 20% for validation.
<!--/QUIZ-->
