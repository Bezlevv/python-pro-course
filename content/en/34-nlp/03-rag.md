---
title: LLM apps: RAG
summary: Retrieval-Augmented Generation.
order: 3
duration: 55 min
difficulty: advanced
tags: rag, llm
---

RAG grounds LLM answers in your documents.

## Flow

1. Split documents into chunks;
2. Embed and store them;
3. On a question: find relevant chunks;
4. Put chunks + question into the prompt.

## Sketch

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")
chunks = ["Python is a language.", "Django is a web framework."]
chunk_vecs = model.encode(chunks)

def ask(question):
    q_vec = model.encode([question])
    scores = cosine_similarity(q_vec, chunk_vecs)[0]
    best = chunks[scores.argmax()]
    prompt = f"Question: {question}\nContext: {best}\nAnswer:"
    # → отправить prompt в LLM
    return prompt
```

## Lesson summary

Retrieve → augment → generate.

<!--TASK-->
### Task 1 — Chunks
Split a text.

### Task 2 — Embed
Embed chunks.

### Task 3 — Retrieve
Find the best chunk.

### Task 4 — Prompt
Build the prompt.

### Task 5 — Why
Why RAG?

### Task 6 — Store
Where to store vectors?

### Task 7 — Update
What if docs change?
<!--/TASK-->

<!--HINT-->
### Hint 1
Split.

### Hint 2
encode.

### Hint 3
Similarity.

### Hint 4
Context.

### Hint 5
Facts.

### Hint 6
Vector DB.

### Hint 7
Re-embed.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
text = """Python is popular. Django is a web framework.
FastAPI is also a framework."""
chunks = text.split(". ")
```

### Solution 2
```python
chunk_vecs = model.encode(chunks)
```

### Solution 3
```python
q_vec = model.encode([question])
scores = cosine_similarity(q_vec, chunk_vecs)[0]
best = chunks[scores.argmax()]
```

### Solution 4
```python
prompt = f"Question: {question}\nContext: {best}\nAnswer:"
```

### Solution 5
```text
RAG добавляет факты из ваших документов —
ответы точнее и проверяемы
```

### Solution 6
```text
Векторные БД: Chroma, FAISS, Qdrant, pgvector
```

### Solution 7
```text
Документы меняются — пере-эмбеддинг
и обновление векторного индекса
```
<!--/SOLUTION-->

<!--QUIZ-->
What is RAG?
- Retrieval-Augmented Generation
- A model
- A database
- None
* Correct answer: Retrieval-Augmented Generation
Grounding.

What is a chunk?
- Text piece
- Full doc
- Vector
- None
* Correct answer: Text piece
Split.

What is retrieval?
- Finding relevant
- Generating
- Embedding
- None
* Correct answer: Finding relevant
Search.

What is augment?
- Adding context
- Removing
- Generating
- None
* Correct answer: Adding context
Prompt.

What is a vector DB?
- Similarity search
- SQL
- Files
- None
* Correct answer: Similarity search
Chroma.

What is FAISS?
- Vector index
- A model
- A browser
- None
* Correct answer: Vector index
Facebook.

What is similarity?
- Closeness
- Length
- Count
- None
* Correct answer: Closeness
Cosine.

What is a prompt?
- Instruction
- Output
- Chunk
- None
* Correct answer: Instruction
Question.

What is grounding?
- Facts
- Hallucination
- Random
- None
* Correct answer: Facts
RAG.

What is hallucination?
- False answer
- True
- Verified
- None
* Correct answer: False answer
Risk.

What is the top-k?
- Best chunks count
- All
- Zero
- None
* Correct answer: Best chunks count
3.

What is the benefit?
- Accurate answers
- Slow
- Required
- None
* Correct answer: Accurate answers
Your docs.
<!--/QUIZ-->
