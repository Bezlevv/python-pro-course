---
title: Exam: Natural Language Processing
summary: Final check of the NLP module: preprocessing, spaCy/NLTK, sentiment, classification, summarization, QA systems.
order: 99
duration: 30 min
difficulty: advanced
exam: true
tags: nlp, exam
---

<!--QUIZ-->
What is lemmatization?
- Bringing a word to its dictionary form (lemma)
- Chopping off endings without a dictionary
- Removing stopwords
* Correct answer: Bringing a word to its dictionary form (lemma)
Lemmatization uses a dictionary and part of speech, unlike stemming.

Which stemmer class in NLTK supports multiple languages, including Russian?
- SnowballStemmer("russian")
- PorterStemmer()
- WordNetLemmatizer()
* Correct answer: SnowballStemmer("russian")
PorterStemmer only handles English; Snowball provides stemmers for many languages, including Russian.

What does nltk.word_tokenize("Hello, world!") return?
- ['Hello', ',', 'world', '!']
- ['Hello,', 'world!']
- ['Hello', 'world']
* Correct answer: ['Hello', ',', 'world', '!']
nltk separates punctuation into its own tokens.

How do you get a token's lemma in spaCy?
- token.lemma_
- token.text
- token.pos_
* Correct answer: token.lemma_
token.lemma_ is the dictionary form; token.pos_ is the part of speech.

What is NER in spaCy?
- Named entity recognition: names, organizations, locations
- A neural network for classification
- A summarization method
* Correct answer: Named entity recognition: names, organizations, locations
NER finds entities in doc.ents and their types in ent.label_.

What is compound in VADER?
- An aggregate sentiment score from -1 to +1
- The number of words in the text
- The share of positive words
* Correct answer: An aggregate sentiment score from -1 to +1
By compound, a text is classified as positive, negative, or neutral.

What does TfidfVectorizer do?
- Turns texts into a matrix of weighted features
- Trains a classifier
- Splits text into sentences
* Correct answer: Turns texts into a matrix of weighted features
TF-IDF weights words by frequency in the document and rarity in the corpus.

Why is train_test_split needed?
- To evaluate the model on data it hasn't seen
- To increase the amount of data
- To speed up vectorization
* Correct answer: To evaluate the model on data it hasn't seen
A held-out set gives an honest quality estimate.

What is extractive summarization?
- Selecting existing sentences of the text for the summary
- Generating a new short text
- Translating text into another language
* Correct answer: Selecting existing sentences of the text for the summary
The extractive method assembles a summary from the original text's sentences.

How does a retrieval QA system find an answer?
- It finds the most similar question in the base by cosine similarity of vectors
- It randomly picks an answer from the base
- It generates an answer without a knowledge base
* Correct answer: It finds the most similar question in the base by cosine similarity of vectors
The TF-IDF vectors of questions are compared with the query, and the maximum is selected.
<!--/QUIZ-->
