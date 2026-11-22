---
title: Embeddings and vector databases
summary: What embeddings are, how to compute semantic similarity of texts, the sentence-transformers library, and the principles of vector databases.
order: 3
duration: 40 min
difficulty: advanced
tags: embeddings, sentence-transformers, cosine similarity, vector databases
---

A computer doesn't understand the meaning of words. But to search "by meaning" rather than by letters, you need a way to turn text into numbers that preserve semantics. This problem is solved by **embeddings**.

## What is an embedding

An embedding is a vector of numbers (for example, 384 or 1536 numbers) that encodes the meaning of a text. The key property: texts that are similar in meaning have vectors that are **close in space** (small distance), while different ones are far apart. Embeddings are produced by special models — encoders.

Install the library:

```bash
pip install sentence-transformers
```

## Your first embedding with sentence-transformers

The `sentence-transformers` library provides ready-made models that understand hundreds of languages:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

texts = ["I love Python", "I like programming"]
vectors = model.encode(texts)
print(vectors.shape)  # (2, 384) — 2 texts of 384 numbers
```

Each of the 384 vector elements is a coordinate in multidimensional space. By itself a coordinate means nothing, but together they describe the position of the text.

## Cosine similarity

The similarity of vectors is measured with **cosine similarity** — the cosine of the angle between the vectors. The value ranges from -1 to 1: 1 — same direction (very similar), 0 — perpendicular, -1 — opposite:

```python
import numpy as np

def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

print(cosine_similarity(vectors[0], vectors[1]))  # close to 1
```

The closer the result is to 1, the closer the meaning. This is the mathematical foundation of semantic search.

## Nearest neighbor search

With a simple list of texts, search can be done by hand:

```python
def search(query, corpus, k=3):
    q_vec = model.encode([query])[0]
    scores = [(cosine_similarity(q_vec, model.encode([t])[0]), t) for t in corpus]
    scores.sort(key=lambda x: x[0], reverse=True)
    return scores[:k]
```

For real volumes, such brute force is too slow — specialized structures are needed.

## Vector databases

A **vector database** stores vectors and can quickly find nearest neighbors. Technologies optimize search with special indexes (for example, HNSW). The most popular options:

- **ChromaDB** — lightweight, embeddable, convenient for Python projects;
- **FAISS** (Facebook AI Similarity Search) — a high-performance library from Meta;
- also: Qdrant, Weaviate, Milvus, pgvector for PostgreSQL.

Working with them in Python is uniform: you add documents with embeddings, then query with a `query` and get the nearest items. We'll work with ChromaDB in detail in the RAG lesson.

## Batch processing and normalization

Encode texts in batches — it's many times faster than one by one: `model.encode(texts)` accepts a list. Many models can **normalize** vectors (length = 1), which simplifies the cosine formula to a dot product — this speeds up computations.

## Summary

You learned: what embeddings are and why they're needed; how to get them via `sentence-transformers`; how to measure semantic similarity with the cosine measure; which tools provide fast vector search. Next — practice.

<!--TASK-->
### Task 1
Using `SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")`, get embeddings of two phrases: "I love programming in Python" and "Python is my favorite language". Print their shape and cosine similarity. Expected result: shape `(2, 384)` and similarity above 0.9.

### Task 2
Given a list of five phrases: "The cat is sleeping on the sofa", "The dog is running in the park", "I ordered a pizza", "The cat is meowing loudly", "Birds sing in the morning". Find the phrase closest to the query "pet" and print it together with its similarity value. Expected result: the phrase about the cat with the highest score.

### Task 3
Write a function `semantic_search(query, corpus, k=3)` that returns the top-k phrases from the corpus with their similarity to the query. Take a corpus of eight sentences about Python (variables, loops, functions, lists, dictionaries, classes, exceptions, decorators). Test with the query "how to store a lot of data in one variable". Expected result: the top contains phrases about lists and dictionaries.

### Task 4
Write a function `normalize(vector)` that divides a vector by its length (Euclidean norm). Show that cosine similarity between normalized vectors equals their dot product: compute both ways for one pair of vectors and print both numbers.

### Task 5
Compare two ways of searching the corpus from task 3: exact substring matching (e.g., `"list" in text`) and semantic search via embeddings. For the query "machine for moving", show the results of both ways. Expected result: substring search finds nothing, while semantic search finds the most meaningfully similar phrases.

<!--/TASK-->

<!--HINT-->
### Hint 1
Load the model once: `model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")`. Then `vectors = model.encode(["...", "..."])` and look at `vectors.shape`. Compute cosine similarity via `np.dot` and `np.linalg.norm`.

### Hint 2
Encode the query and all five phrases with one `model.encode()` call. Compute the similarity between the query vector and each vector in the list, find the maximum via `max(scores)`.

### Hint 3
The function should encode the query, then compute similarity for each text in the corpus, sort in descending order, and return `[:k]`. For a list of `(score, text)` tuples, sorting with `reverse=True` gives the needed order.

### Hint 4
The norm of a Euclidean vector is `np.linalg.norm(v)`. After division, the length becomes 1. The dot product of two normalized vectors equals cosine similarity, because the denominator of the formula becomes 1.

### Hint 5
For substring search, use the simple condition `if q.lower() in text.lower()`. Then run `semantic_search` from task 3 with the same query and compare the lists.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
texts = ["I love programming in Python", "Python is my favorite language"]
vectors = model.encode(texts)

print("Shape:", vectors.shape)

def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

print("Similarity:", cosine_similarity(vectors[0], vectors[1]))
```

The shape `(2, 384)` means: two vectors of 384 dimensions. The model `paraphrase-multilingual-MiniLM-L12-v2` is a compact multilingual one (supports Russian), and its vectors have 384 numbers. The phrases are almost identical in meaning, so the cosine similarity will be above 0.9. If we compared "I love Python" and "It's raining today", the similarity would be noticeably lower. It's this property that makes embeddings a tool for search by meaning.

### Solution 2
```python
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
corpus = [
    "The cat is sleeping on the sofa",
    "The dog is running in the park",
    "I ordered a pizza",
    "The cat is meowing loudly",
    "Birds sing in the morning",
]
query = "pet"

q_vec = model.encode([query])[0]
vectors = model.encode(corpus)

def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

scores = [(cosine_similarity(q_vec, v), text) for v, text in zip(vectors, corpus)]
best_score, best_text = max(scores)
print(best_text, best_score)
```

We encode the corpus with one call — it's faster and cleaner than a loop of separate calls. Then we compute the similarity to the query for each vector. The phrases "The cat is sleeping on the sofa" and "The cat is meowing loudly" will get the highest scores, because cats are pets. Note: "The dog is running in the park" is also close, but usually a bit lower — a dog is also a pet, everything depends on the specific model.

### Solution 3
```python
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

corpus = [
    "Variables store values in memory",
    "Loops let you repeat actions",
    "Functions group code and are reused",
    "Lists store many elements in order",
    "Dictionaries store key-value pairs",
    "Classes describe objects with data and methods",
    "Exceptions handle errors",
    "Decorators change the behavior of functions",
]

def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def semantic_search(query, corpus, k=3):
    q_vec = model.encode([query])[0]
    vectors = model.encode(corpus)
    scores = [(cosine_similarity(q_vec, v), text) for v, text in zip(vectors, corpus)]
    scores.sort(key=lambda x: x[0], reverse=True)
    return scores[:k]

for score, text in semantic_search("how to store a lot of data in one variable", corpus):
    print(round(score, 3), text)
```

The phrase about lists and dictionaries will be on top, since both "store a lot of data". Descending sort is easy with `sort(key=lambda x: x[0], reverse=True)`. This is a minimal semantic search implementation: it works on small volumes but already shows the idea. For thousands and millions of documents, such brute force becomes slow — that's where vector DBs with indexes take over.

### Solution 4
```python
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
a, b = model.encode(["I love Python", "I like programming"])

def normalize(v):
    return v / np.linalg.norm(v)

a_n, b_n = normalize(a), normalize(b)
cos_orig = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
cos_normalized = np.dot(a_n, b_n)

print("Cosine (ordinary):", cos_orig)
print("Dot product of normalized:", cos_normalized)
```

After normalization, each vector's length is 1, so the denominator of the cosine formula becomes 1, leaving only the dot product. The two numbers will match up to floating-point error. Why is this needed? Vector databases and search engines store normalized vectors — then one multiplication replaces division, which noticeably speeds up search on large arrays.

### Solution 5
```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
corpus = [
    "Variables store values in memory",
    "Loops let you repeat actions",
    "Functions group code and are reused",
    "Lists store many elements in order",
    "Dictionaries store key-value pairs",
    "Classes describe objects with data and methods",
    "Exceptions handle errors",
    "Decorators change the behavior of functions",
]
query = "machine for moving"

substring_hits = [t for t in corpus if query.lower() in t.lower()]
print("Substring search:", substring_hits)

def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

q_vec = model.encode([query])[0]
vectors = model.encode(corpus)
scores = [(cosine_similarity(q_vec, v), t) for v, t in zip(vectors, corpus)]
scores.sort(key=lambda x: x[0], reverse=True)
print("Semantic top-3:", [(t, round(s, 3)) for s, t in scores[:3]])
```

Substring search returns an empty list: the corpus has no words "machine" or "moving". Semantic search, however, understands that "machine for moving" is close in meaning to "Loops let you repeat actions" (a machine is a loop, an iteration) and to "Variables store values" (a program moves from variable to variable). This difference is the main argument for embeddings: they capture meaning, not literal matches.

<!--/SOLUTION-->

<!--QUIZ-->
What is a text embedding?
- A number showing the length of the text
- A vector of numbers encoding the meaning of the text
- A string of characters
* Correct answer: A vector of numbers encoding the meaning of the text
An embedding turns text into a multidimensional point that is close for similar meanings.

How is semantic similarity of vectors measured?
- Cosine similarity
- Text length
- Number of common letters
* Correct answer: Cosine similarity
The cosine of the angle between vectors: the closer to 1, the more similar the texts.

Which library is most convenient for getting embeddings in Python?
- sentence-transformers
- requests
- matplotlib
* Correct answer: sentence-transformers
It provides ready-made encoder models with the encode() method.

Why are vector databases needed?
- To store texts in files
- For fast nearest-vector search
- For compiling Python
* Correct answer: For fast nearest-vector search
They use indexes (e.g., HNSW) to find neighbors without full scan.

What does normalizing vectors give?
- Turns text into numbers
- Makes the vector length equal to 1, simplifying cosine
- Halves the number of dimensions
* Correct answer: Makes the vector length equal to 1, simplifying cosine
After normalization, similarity equals the dot product — it's faster.

Which vector will be closest to the embedding of the phrase "I adore Python"?
- "It's rainy weather today"
- "I really like programming in Python"
- "I need to buy bread"
* Correct answer: "I really like programming in Python"
Semantic closeness determines the closeness of vectors.

What dimensionality do the embeddings of the model paraphrase-multilingual-MiniLM-L12-v2 have?
- 128
- 384
- 1536
* Correct answer: 384
This multilingual model outputs vectors of 384 numbers.

Why is scanning all vectors a poor fit for large corpora?
- Because vectors take too much memory even in a list
- Because you need to compare the query with every vector, which is O(n) operations
- Because embeddings cannot be compared pairwise
* Correct answer: Because you need to compare the query with every vector, which is O(n) operations
For millions of documents, full scan is too slow — that's why vector DBs with indexes like HNSW are used.

<!--/QUIZ-->
