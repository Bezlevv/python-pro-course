---
title: NLP pipeline
summary: Tokenize, normalize, features.
order: 1
duration: 45 min
difficulty: intermediate
tags: nlp
---

NLP turns text into numbers.

## Pipeline

1. Tokenize;
2. Normalize (lowercase, lemmatize);
3. Features (BoW/TF-IDF);
4. Model.

## BoW

```python
from sklearn.feature_extraction.text import CountVectorizer

corpus = ["I love Python", "Python is great"]
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)
print(X.toarray())
```

## Lesson summary

Text → tokens → vectors → model.

<!--TASK-->
### Task 1 — Tokens
Split text.

### Task 2 — Lower
Normalize.

### Task 3 — BoW
CountVectorizer.

### Task 4 — TF-IDF
Build TF-IDF.

### Task 5 — Vocabulary
Show the vocabulary.

### Task 6 — Sparse
Explain sparse matrix.

### Task 7 — Pipeline
sklearn Pipeline.
<!--/TASK-->

<!--HINT-->
### Hint 1
split.

### Hint 2
lower.

### Hint 3
CountVectorizer.

### Hint 4
TfidfVectorizer.

### Hint 5
get_feature_names_out.

### Hint 6
Zeros.

### Hint 7
Pipeline.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
text = "I love Python"
tokens = text.lower().split()
```

### Solution 2
```python
tokens = [t.lower() for t in text.split()]
```

### Solution 3
```python
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(["I love Python", "Python is great"])
```

### Solution 4
```python
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer()
X = tfidf.fit_transform(corpus)
```

### Solution 5
```python
print(vectorizer.get_feature_names_out())
```

### Solution 6
```text
Матрица хранит только ненулевые значения —
экономия памяти
```

### Solution 7
```python
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB

pipe = Pipeline([
    ("vec", TfidfVectorizer()),
    ("clf", MultinomialNB()),
])
pipe.fit(X_train, y_train)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is tokenization?
- Splitting text
- Lowercase
- Vectors
- None
* Correct answer: Splitting text
Tokens.

What is normalization?
- Clean form
- Raw
- Vector
- None
* Correct answer: Clean form
Lower.

What is BoW?
- Word counts
- Vectors
- Models
- None
* Correct answer: Word counts
Bag.

What is TF-IDF?
- Weighted words
- Counts
- Tokens
- None
* Correct answer: Weighted words
Importance.

What is a corpus?
- Text collection
- One text
- A model
- None
* Correct answer: Text collection
Data.

What is a feature?
- Numeric representation
- Text
- Model
- None
* Correct answer: Numeric representation
Column.

What is sparse?
- Mostly zeros
- Dense
- Small
- None
* Correct answer: Mostly zeros
Efficient.

What is vocabulary?
- Unique words
- Text
- Counts
- None
* Correct answer: Unique words
Index.

What is Pipeline?
- Chained steps
- One step
- A model
- None
* Correct answer: Chained steps
sklearn.

What is fit?
- Trains
- Predicts
- Transforms
- None
* Correct answer: Trains
Learn.

What is transform?
- Converts
- Trains
- Predicts
- None
* Correct answer: Converts
Text→X.

What is a classifier?
- Labels text
- Tokenizes
- Vectorizes
- None
* Correct answer: Labels text
Naive Bayes.
<!--/QUIZ-->
