---
title: Hugging Face Transformers and LLM API
summary: Using pretrained models, pipelines and calling LLM APIs.
order: 10
duration: 45 min
difficulty: intermediate
tags: transformers, llm, api, huggingface
---

Transformers give access to powerful pretrained NLP models.

## Pipeline

```python
from transformers import pipeline

classifier = pipeline("sentiment-analysis")
print(classifier("I love Python!"))
```

## Generation

```python
generator = pipeline("text-generation", model="gpt2")
print(generator("Python is", max_length=20)[0]["generated_text"])
```

## LLM API

```python
import requests

resp = requests.post(
    "https://api.example.com/v1/chat/completions",
    headers={"Authorization": "Bearer TOKEN"},
    json={
        "model": "gpt-4",
        "messages": [{"role": "user", "content": "Hi"}],
    },
    timeout=30,
)
print(resp.json()["choices"][0]["message"]["content"])
```

## Lesson summary

Transformers pipelines simplify NLP; LLM APIs follow chat completion schemas.

<!--TASK-->
### Task 1 — Sentiment pipeline
Run sentiment-analysis pipeline on "This is great!".

### Task 2 — Zero-shot
Use zero-shot-classification to label a sentence.

### Task 3 — Generation
Generate a short text with a small model.

### Task 4 — Summarization
Summarize a long sentence with the summarization pipeline.

### Task 5 — API request
Write a function calling a chat completions API with a message.

### Task 6 — Error handling
Catch request errors and print a friendly message.

### Task 7 — Token note
Explain in a comment why system role sets behavior.
<!--/TASK-->

<!--HINT-->
### Hint 1
pipeline("sentiment-analysis").

### Hint 2
pipeline("zero-shot-classification", ...).

### Hint 3
pipeline("text-generation").

### Hint 4
pipeline("summarization").

### Hint 5
POST to /chat/completions.

### Hint 6
try/except around requests.

### Hint 7
system sets rules.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from transformers import pipeline
classifier = pipeline("sentiment-analysis")
print(classifier("This is great!"))
```

### Solution 2
```python
clf = pipeline("zero-shot-classification")
print(clf("Python is a language", candidate_labels=["programming", "food"]))
```

### Solution 3
```python
generator = pipeline("text-generation", model="gpt2")
out = generator("Once upon a time", max_length=20)
print(out[0]["generated_text"])
```

### Solution 4
```python
summ = pipeline("summarization")
text = "Python is a widely used language. " * 10
print(summ(text, max_length=20)[0]["summary_text"])
```

### Solution 5
```python
import requests

def chat(message):
    resp = requests.post(
        "https://api.example.com/v1/chat/completions",
        headers={"Authorization": "Bearer TOKEN"},
        json={
            "model": "gpt-4",
            "messages": [{"role": "user", "content": message}],
        },
        timeout=30,
    )
    return resp.json()["choices"][0]["message"]["content"]
```

### Solution 6
```python
try:
    print(chat("Hello"))
except requests.RequestException as e:
    print("API error:", e)
```

### Solution 7
```python
# system message sets assistant behavior/rules
# user messages are the actual input
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a pipeline?
- Ready-made model wrapper
- A model file
- An API
- A token
* Correct answer: Ready-made model wrapper
High-level.

Which task is sentiment-analysis?
- Emotion classification
- Translation
- QA
- Summarization
* Correct answer: Emotion classification
Positive/negative.

What is zero-shot classification?
- Classify unseen labels
- Fine-tuned
- Trained
- Random
* Correct answer: Classify unseen labels
No training.

What does text-generation do?
- Produces text
- Classifies
- Summarizes
- Translates
* Correct answer: Produces text
Continuation.

What is summarization?
- Shortens text
- Generates
- Translates
- Scores
* Correct answer: Shortens text
Key ideas.

What is a chat completion?
- An LLM response to messages
- A file
- A model
- A token
* Correct answer: An LLM response to messages
API call.

Which role sets behavior?
- system
- user
- assistant
- tool
* Correct answer: system
Instructions.

What is the Authorization header for?
- API key
- Content type
- Model
- Timeout
* Correct answer: API key
Bearer token.

What is requests.post for?
- Sending data
- Reading file
- Parsing
- Training
* Correct answer: Sending data
HTTP POST.

What does .json() do?
- Parses response JSON
- Sends
- Formats
- Saves
* Correct answer: Parses response JSON
Response body.

Where is the generated text?
- choices[0].message.content
- data["text"]
- response
- json
* Correct answer: choices[0].message.content
Standard schema.

Why timeout?
- Avoid hangs
- Security
- Speed
- Cache
* Correct answer: Avoid hangs
Request limit.
<!--/QUIZ-->
