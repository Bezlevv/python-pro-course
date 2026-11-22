---
title: RAG: augmenting context
summary: The RAG pipeline: splitting documents into chunks, indexing embeddings in ChromaDB, retrieving relevant fragments, and generating an answer with context.
order: 4
duration: 45 min
difficulty: advanced
tags: rag, chromadb, embeddings, search, llm
---

Language models are trained on data with a fixed cutoff date. Ask "GPT-4o" about yesterday's events — and it either errs or admits it doesn't know. But what if you give the model _your_ documents? That's exactly what **RAG** does — Retrieval-Augmented Generation, generation augmented with context.

## The problem

An LLM's knowledge base is limited. Your company has fresh documents, knowledge bases, and internal instructions that the model hasn't seen. The solution is not to retrain the model but to feed it the needed fragments at request time. It's cheaper, faster, and always up to date.

## The RAG scheme

The pipeline consists of three phases:

1. **Indexing** — split documents into fragments (**chunks**), get their embeddings, and put them into a vector database;
2. **Retrieval** — find the `k` closest chunks for the user's query;
3. **Generation** — hand the chunks to the model as context along with the question.

Install ChromaDB and sentence-transformers:

```bash
pip install chromadb sentence-transformers
```

## Phase 1. Indexing

Chunking means splitting text into fragments. It must be done at paragraph and sentence boundaries, otherwise you cut a thought in half. A minimal variant:

```python
def chunk_text(text, size=200):
    words = text.split()
    return [" ".join(words[i:i + size]) for i in range(0, len(words), size)]
```

Now indexing in ChromaDB:

```python
import chromadb
from sentence_transformers import SentenceTransformer

encoder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
client = chromadb.Client()
collection = client.get_or_create_collection("docs")

chunks = chunk_text(doc_text)
collection.add(
    ids=[f"c{i}" for i in range(len(chunks))],
    embeddings=encoder.encode(chunks).tolist(),
    documents=chunks,
)
```

## Phase 2. Retrieval

ChromaDB can search by vectors:

```python
query = "How to install Python on Windows?"
results = collection.query(
    query_embeddings=encoder.encode([query]).tolist(),
    n_results=2,
)
for doc in results["documents"][0]:
    print(doc)
```

## Phase 3. Generation

Now let's put it all together — pass the found chunks to the model as context:

```python
context = "\n".join(results["documents"][0])
prompt = f"""
Answer ONLY based on the provided context.
If the context has no answer, say: "There is no answer in the context."

Context:
{context}

Question: {query}
"""
```

The system prompt "answer only based on context" is critically important: without it, the model will start hallucinating.

## How to improve RAG

- **Smarter chunking**: overlapping chunks, splitting by paragraphs.
- **Hybrid search**: vector + keyword (BM25).
- **Reranking**: re-sorting the found results with a stronger model.
- **Metadata**: store the source and page so you can cite.
- **Relevance checking**: discard chunks that are too far by a similarity threshold.

## Summary

You learned the RAG scheme: indexing → retrieval → generation. Next, you'll build a working pipeline on ChromaDB and train it.

<!--TASK-->
### Task 1
Write a function `chunk_text(text, size=40)` that splits text into chunks of `size` words without breaking words (simple splitting by spaces). Take some text about Python (for example, a paragraph from the documentation) and output the number of chunks and the first chunk in full. Expected result: chunks contain no cut-off words.

### Task 2
Create a ChromaDB collection `my_docs` and put three chunks about Python (loops, lists, functions) into it with `SentenceTransformer` embeddings. Check that the collection has three items: print `collection.count()`. Expected result: the number 3.

### Task 3
Write a function `retrieve(query, k=2)` that takes a query, searches the `my_docs` collection for the two closest chunks, and returns their texts as a list. Test with the query "how to iterate over items one by one". Expected result: the list contains the chunk about loops (and possibly the neighboring one).

### Task 4
Assemble a full RAG pipeline: the function `rag_answer(query)` finds chunks via `retrieve`, builds a system prompt with context and question, sends a request to the LLM API, and returns the model's answer. Test with the question from task 3. Expected result: an answer grounded in the chunk text.

### Task 5
Run an experiment: ask the same question twice — without context (a plain request to the model) and via `rag_answer`. Print both answers. Expected result: the answer with context contains details from the chunks, while the answer without context contains generic words.

<!--/TASK-->

<!--HINT-->
### Hint 1
`text.split()` splits by spaces; group with a list comprehension `[" ".join(words[i:i+size]) for i in range(0, len(words), size)]`. Don't forget the empty-text case — return `[]`.

### Hint 2
`collection.add(ids=[...], embeddings=encoder.encode(chunks).tolist(), documents=chunks)` — ids must be strings and unique. The number of items is checked via `collection.count()`.

### Hint 3
Use `collection.query(query_embeddings=encoder.encode([query]).tolist(), n_results=k)`. The result lives in `results["documents"][0]` — a list of texts in decreasing order of similarity.

### Hint 4
Build the context as `"\n".join(hits)`, insert it into the prompt with the instruction "Answer ONLY based on context". Then send a request to `https://api.openai.com/v1/chat/completions`, as in lesson 1.

### Hint 5
For the answer without context, send the question as an ordinary user message with the same system prompt. For the answer with context, use `rag_answer`. Print both with a separator.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
def chunk_text(text, size=40):
    words = text.split()
    return [" ".join(words[i:i + size]) for i in range(0, len(words), size)]

text = ("Python is a high-level programming language with dynamic typing. "
        "It supports several paradigms: procedural, object-oriented, "
        "and functional. Thanks to its simple syntax, Python is often used "
        "as a first language for learning programming.")
chunks = chunk_text(text)
print("Chunks:", len(chunks))
print(chunks[0])
```

The function takes all words and groups them by `size`. Words are never broken because we split by spaces, not by characters. That's enough for a simple prototype. In production, chunking is more complex: paragraphs and sentences are considered, and overlap is used so a thought isn't "cut" between chunks — otherwise search may miss the needed fragment.

### Solution 2
```python
import chromadb
from sentence_transformers import SentenceTransformer

encoder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
client = chromadb.Client()
collection = client.get_or_create_collection("my_docs")

chunks = [
    "For and while loops allow you to repeat actions several times.",
    "Lists store many elements in a certain order.",
    "Functions group code and let you reuse it.",
]
collection.add(
    ids=["c0", "c1", "c2"],
    embeddings=encoder.encode(chunks).tolist(),
    documents=chunks,
)
print(collection.count())  # 3
```

`chromadb.Client()` creates a built-in (in-memory) database — nothing extra to install. `collection.add` takes three parallel lists: `ids`, `embeddings`, and `documents`. We compute embeddings in advance with sentence-transformers and pass them as `.tolist()` — ChromaDB accepts Python lists, not NumPy arrays. `collection.count()` returns the number of items — handy for self-checking.

### Solution 3
```python
def retrieve(query, k=2):
    results = collection.query(
        query_embeddings=encoder.encode([query]).tolist(),
        n_results=k,
    )
    return results["documents"][0]

print(retrieve("how to iterate over items one by one"))
```

ChromaDB itself finds the nearest neighbors by cosine similarity and returns `documents` — a list of texts sorted in decreasing order of similarity. The first will be the chunk about loops: "iterate over items one by one" is literally a loop. The second will most likely be lists. This is the heart of RAG: search not by letters but by meaning.

### Solution 4
```python
import os
import requests

def rag_answer(query):
    hits = retrieve(query)
    context = "\n".join(hits)
    system = ("You are an assistant that answers based on documents. "
              "Answer ONLY based on the provided context. "
              "If the context has no answer, say: \"There is no answer in the context.\"")
    user = f"Context:\n{context}\n\nQuestion: {query}"
    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.2,
        },
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

print(rag_answer("how to iterate over items one by one"))
```

The key line is the system prompt forbidding answers outside the context. It turns the model from a "know-it-all" into a careful executor that doesn't make things up. Temperature 0.2 keeps answers stable. Such a pipeline is easy to scale: replace the documents and the knowledge base changes without retraining the model.

### Solution 5
```python
def plain_answer(query):
    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": query}],
            "temperature": 0.2,
        },
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

q = "how to iterate over items one by one"
print("WITHOUT CONTEXT:")
print(plain_answer(q))
print("WITH CONTEXT:")
print(rag_answer(q))
```

The answer without context will be generic: "you can use a for loop...". The answer with context will take wording from our chunks, e.g., "repeat actions several times". The difference clearly shows the value of RAG: we got an answer grounded in a specific document rather than the model's general knowledge. This is exactly how corporate chatbots that "know" internal company regulations are built.

<!--/SOLUTION-->

<!--QUIZ-->
What is RAG?
- A method of training a model on new data
- Generating an answer augmented with context from documents
- A way to encrypt texts
* Correct answer: Generating an answer augmented with context from documents
RAG feeds the model relevant fragments at request time.

Why is chunking needed?
- To reduce the file size
- To split a document into fragments for indexing
- To speed up model training
* Correct answer: To split a document into fragments for indexing
Chunks are indexed, and search runs over them.

Which phase is NOT part of the basic RAG pipeline?
- Indexing
- Retrieving relevant chunks
- Retraining the model
* Correct answer: Retraining the model
RAG doesn't require retraining — the model stays the same.

What does collection.query() do in ChromaDB?
- Deletes the collection
- Finds the vectors closest to the query
- Prints the list of documents
* Correct answer: Finds the vectors closest to the query
query returns the closest chunks by vector similarity.

Why does the RAG system prompt say "Answer only based on context"?
- So the model answers faster
- So the model doesn't hallucinate beyond the documents
- So context doesn't take up space
* Correct answer: So the model doesn't hallucinate beyond the documents
The ban on "free" answers keeps the model within the documents.

Which chunk will be found for the query "how to repeat an action several times"?
- About loops
- About functions
- About lists
* Correct answer: About loops
Loops literally repeat actions — semantic similarity is maximal.

Why store metadata (source, page) in RAG?
- To reduce the number of chunks
- To be able to cite the source in the answer
- To speed up model loading
* Correct answer: To be able to cite the source in the answer
Metadata lets you reference a specific document and page.

What is hybrid search in RAG?
- Search only by exact word match
- Combining vector search and keyword search (e.g., BM25)
- Image search
* Correct answer: Combining vector search and keyword search (e.g., BM25)
Hybrid captures both meaning and exact terms, improving retrieval quality.

<!--/QUIZ-->
