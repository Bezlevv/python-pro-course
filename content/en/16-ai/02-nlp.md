---
title: NLTK and spaCy: text processing
summary: Tokenization, stemming, POS, entities.
order: 2
duration: 50 min
difficulty: intermediate
tags: nlp, nltk, spacy
---

NLP libraries process human language.

## NLTK

```python
import nltk
nltk.download("punkt")
from nltk.tokenize import word_tokenize
tokens = word_tokenize("Hello, world!")
```

## spaCy

```python
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple bought a company in London.")
for token in doc:
    print(token.text, token.pos_)
for ent in doc.ents:
    print(ent.text, ent.label_)
```

## Lesson summary

Tokenize, normalize, extract structure.

<!--TASK-->
### Task 1 — Tokenize
Split a sentence into tokens.

### Task 2 — Lowercase
Normalize tokens.

### Task 3 — Stopwords
Remove stop words.

### Task 4 — Stemming
Stem words.

### Task 5 — POS
Tag parts of speech with spaCy.

### Task 6 — Entities
Extract named entities.

### Task 7 — Lemmas
Use lemmatization.
<!--/TASK-->

<!--HINT-->
### Hint 1
word_tokenize.

### Hint 2
lower().

### Hint 3
stopwords.

### Hint 4
PorterStemmer.

### Hint 5
token.pos_.

### Hint 6
doc.ents.

### Hint 7
token.lemma_.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from nltk.tokenize import word_tokenize
tokens = word_tokenize("Hello, world!")
print(tokens)   # ['Hello', ',', 'world', '!']
```

### Solution 2
```python
tokens = [t.lower() for t in tokens]
```

### Solution 3
```python
from nltk.corpus import stopwords
stop = set(stopwords.words("english"))
clean = [t for t in tokens if t.lower() not in stop]
```

### Solution 4
```python
from nltk.stem import PorterStemmer
ps = PorterStemmer()
print(ps.stem("running"))   # run
```

### Solution 5
```python
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("Alice runs quickly.")
for token in doc:
    print(token.text, token.pos_)
```

### Solution 6
```python
doc = nlp("Apple bought a company in London.")
for ent in doc.ents:
    print(ent.text, ent.label_)
# Apple ORG, London GPE
```

### Solution 7
```python
for token in doc:
    print(token.lemma_)
# run, quick
```
<!--/SOLUTION-->

<!--QUIZ-->
What is tokenization?
- Splitting text
- Translating
- Sorting
- None
* Correct answer: Splitting text
Tokens.

What is a token?
- A word/punctuation
- A sentence
- A doc
- None
* Correct answer: A word/punctuation
Unit.

What is stemming?
- Rough reduction
- Full grammar
- Translation
- None
* Correct answer: Rough reduction
run.

What is lemmatization?
- Dictionary base
- Rough cut
- Same
- None
* Correct answer: Dictionary base
Precise.

What are stopwords?
- Common filler words
- Rare words
- Numbers
- None
* Correct answer: Common filler words
the, and.

What is POS?
- Part of speech
- Point of sale
- A token
- None
* Correct answer: Part of speech
noun/verb.

What is an entity?
- Named object
- A word
- A token
- None
* Correct answer: Named object
ORG/GPE.

What is spaCy?
- NLP library
- A browser
- A database
- None
* Correct answer: NLP library
Fast.

What is NLTK?
- NLP toolkit
- A game
- A database
- None
* Correct answer: NLP toolkit
Classic.

What is a corpus?
- Text collection
- One word
- A model
- None
* Correct answer: Text collection
Data.

What is lowercase?
- Normalization
- Stemming
- Entities
- None
* Correct answer: Normalization
Clean.

What is a pipeline?
- Steps: tokenize → tag → parse
- One step
- A loop
- None
* Correct answer: Steps: tokenize → tag → parse
nlp().
<!--/QUIZ-->
