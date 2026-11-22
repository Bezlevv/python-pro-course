---
title: Exam: Modern AI
summary: Final exam for the "Modern AI" module.
order: 99
duration: 30 min
difficulty: advanced
exam: true
---

<!--QUIZ-->
Which HTTP method and endpoint are used to send a chat request to an LLM API?
- GET /v1/models
- POST /v1/chat/completions
- PUT /v1/completions
* Correct answer: POST /v1/chat/completions
Chat completions create generation, so POST is used.

Which message role sets the model's behavior (tone and rules)?
- user
- system
- assistant
* Correct answer: system
The system message describes the boundaries and style of answers.

What happens if you set temperature = 0?
- Answers become almost deterministic
- The model starts answering faster
- Answers become more random
* Correct answer: Answers become almost deterministic
Zero temperature means choosing the most likely token.

What is a few-shot prompt?
- A prompt with input-output examples
- A prompt without a system message
- A prompt with maximum temperature
* Correct answer: A prompt with input-output examples
Examples set the pattern the model follows.

How is semantic similarity of embeddings measured?
- Text length
- Cosine similarity
- Number of tokens
* Correct answer: Cosine similarity
The cosine of the angle between vectors reflects the closeness of meanings.

What are embeddings for in the RAG pipeline?
- For finding relevant document fragments
- For encrypting text
- For reducing API cost
* Correct answer: For finding relevant document fragments
Vectors find chunks close in meaning to the query.

What is chunking?
- Splitting a document into fragments for indexing
- Encrypting a document
- Training a model on a document
* Correct answer: Splitting a document into fragments for indexing
Chunks are units of search and context in RAG.

What does the | operator do in LCEL (LangChain)?
- Connects components into a chain
- Extracts JSON from the response
- Sets the model's temperature
* Correct answer: Connects components into a chain
prompt | llm | parser is a processing pipeline.

Why use with_structured_output(Pydantic model) in LangChain?
- To get a validated structured object
- To speed up the request
- To add tools
* Correct answer: To get a validated structured object
The model answers with JSON that is validated against the schema.

What happens in the agent loop after getting tool_calls?
- The code executes the calls and returns the results to the model
- The model immediately prints the answer
- The user enters data again
* Correct answer: The code executes the calls and returns the results to the model
Results are added as tool messages, and the loop continues.
<!--/QUIZ-->
