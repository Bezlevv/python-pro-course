---
title: Embeddings and transformers
summary: Word2Vec, BERT, sentence vectors.
order: 2
duration: 55 min
difficulty: advanced
tags: embeddings, transformers
---

Embeddings capture meaning.

## Word embeddings

Words → dense vectors with meaning.

## Sentence embeddings

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
vec = model.encode("Python is fun")
print(vec.shape)
```

## Similarity

```python
from sklearn.metrics.pairwise import cosine_similarity

a = model.encode("I love Python")
b = model.encode("Programming is great")
print(cosine_similarity([a], [b])[0][0])
```

## Lesson summary

Embeddings make text comparable.

<!--TASK-->
### Task 1 — Model
Load SentenceTransformer.

### Task 2 — Encode
Encode a sentence.

### Task 3 — Shape
Print the vector size.

### Task 4 — Similarity
Compare two sentences.

### Task 5 — Transformer
What is BERT?

### Task 6 — Context
Why contextual embeddings?

### Task 7 — Use
Name two applications.
<!--/TASK-->

<!--HINT-->
### Hint 1
SentenceTransformer.

### Hint 2
encode.

### Hint 3
shape.

### Hint 4
cosine.

### Hint 5
Pre-trained.

### Hint 6
Meaning.

### Hint 7
Search.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
```

### Solution 2
```python
vec = model.encode("Python is fun")
```

### Solution 3
```python
print(vec.shape)   # (384,)
```

### Solution 4
```python
from sklearn.metrics.pairwise import cosine_similarity

a = model.encode("I love Python")
b = model.encode("Programming is great")
print(cosine_similarity([a], [b])[0][0])
```

### Solution 5
```text
BERT — предобученная нейросеть-трансформер,
которая понимает контекст слов
```

### Solution 6
```text
Одно и то же слово получает разные векторы
в разных контекстах («банк» — деньги/река)
```

### Solution 7
```text
Поиск по смыслу, классификация, кластеризация,
чат-боты, суммаризация
```
<!--/SOLUTION-->

<!--QUIZ-->
What is an embedding?
- Vector of meaning
- Word
- Model
- None
* Correct answer: Vector of meaning
Dense.

What is a transformer?
- Model architecture
- A loop
- A vector
- None
* Correct answer: Model architecture
BERT.

What is BERT?
- Pre-trained model
- A dataset
- A token
- None
* Correct answer: Pre-trained model
Context.

What is encode?
- Text → vector
- Vector → text
- Train
- None
* Correct answer: Text → vector
Transform.

What is cosine similarity?
- Angle closeness
- Distance
- Count
- None
* Correct answer: Angle closeness
1 = same.

What is context?
- Surrounding words
- One word
- Vector
- None
* Correct answer: Surrounding words
Meaning.

What is dimension?
- Vector size
- Word
- Context
- None
* Correct answer: Vector size
384.

What is pre-trained?
- Already trained
- From scratch
- Random
- None
* Correct answer: Already trained
Transfer.

What is fine-tuning?
- Further training
- Fresh
- Fixed
- None
* Correct answer: Further training
Task.

What is similarity?
- Semantic closeness
- Length
- Count
- None
* Correct answer: Semantic closeness
Compare.

What is a use case?
- Application
- Model
- Vector
- None
* Correct answer: Application
Search.

What is dense?
- Many non-zero
- Sparse
- Zero
- None
* Correct answer: Many non-zero
Meaning.
<!--/QUIZ-->
