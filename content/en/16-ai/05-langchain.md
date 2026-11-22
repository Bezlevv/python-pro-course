---
title: LangChain: chains and tools
summary: Building LLM applications with LangChain: prompts, models, LCEL chains, structured output via Pydantic, and tools.
order: 5
duration: 45 min
difficulty: advanced
tags: langchain, lcel, pydantic, tools
---

Writing LLM API integration by hand is interesting, but for large projects you want reusable building blocks. **LangChain** is a framework that provides ready-made components: prompts, models, parsers, retrievers, tools. In this lesson, we'll build applications from them.

## Installation

```bash
pip install langchain langchain-openai
```

Components:

- `ChatOpenAI` — a wrapper over the LLM API;
- `ChatPromptTemplate` — prompt templates;
- `StrOutputParser` — extracts a string from the model's response;
- the `|` operator — connects components into a **chain** (LCEL).

## Your first chain

A chain is a pipeline: data enters on the left, passes through components, and exits on the right.

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a Python expert."),
    ("user", "{question}"),
])
chain = prompt | llm | StrOutputParser()

print(chain.invoke({"question": "What is a decorator?"}))
```

`chain.invoke({"question": ...})` goes through the pipeline: the template substitutes the question into the prompt, the model answers, and the parser extracts the text.

## What is LCEL

**LCEL** (LangChain Expression Language) is a way to describe chains with `|`. The expression `prompt | llm | parser` reads as "first the prompt, then the model, then the parser". Components are compatible if their interfaces match — this allows free combination.

## Structured output with Pydantic

Instead of "raw" text, you can get a ready Python object. To do this, describe a Pydantic model and use `with_structured_output`:

```python
from pydantic import BaseModel

class Review(BaseModel):
    rating: int
    pros: list[str]
    cons: list[str]

chain = prompt | llm.with_structured_output(Review)
obj = chain.invoke({"question": "Rate: Python is a convenient language, but setting up the environment can be painful."})
print(obj.rating, obj.pros, obj.cons)
```

The model will return JSON, and LangChain will validate it against the schema. A format error becomes an exception, not silent garbage.

## Tools

Tools are functions the model can call. They are declared with the `@tool` decorator:

```python
from langchain_core.tools import tool

@tool
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

llm_with_tools = llm.bind_tools([add_numbers])
```

Now the model itself decides when to call `add_numbers` and returns `tool_calls` with arguments.

## RAG with LangChain

LangChain can also build RAG chains: a retriever finds chunks, a prompt merges them with the question, and the model answers. A vector store connects with one line:

```python
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

store = InMemoryVectorStore.from_texts(chunks, embedding=OpenAIEmbeddings())
retriever = store.as_retriever(search_kwargs={"k": 2})
```

## Summary

You got acquainted with LangChain's basic blocks: prompts, models, parsers, LCEL chains, Pydantic output, tools, retrievers. Now you'll assemble real applications from them.

<!--TASK-->
### Task 1
Assemble your first chain: `ChatPromptTemplate` with the system message "You are a concise expert. Answer in at most two sentences", the model `ChatOpenAI(model="gpt-4o-mini")`, and `StrOutputParser`. Call the chain with the question "What is a virtual environment?" and print the result. Expected result: a string — a short answer.

### Task 2
Assemble a two-step chain: the first chain extracts the topic of the question (ask the model to return one word), the second writes a mini-article on that topic. Define two prompts and two subchains for this, and call them sequentially. Expected result: first the topic is printed, then an article of two or three sentences.

### Task 3
Create a Pydantic model `Order` with fields `product` (str), `quantity` (int), `price` (float). Use `with_structured_output(Order)` to extract an order from the phrase "Bought 2 keyboards for 3500 rubles". Print the object via `obj.model_dump()`. Expected result: dict `{"product": "keyboard", "quantity": 2, "price": 3500.0}`.

### Task 4
Declare with `@tool` a function `multiply(a: int, b: int) -> int` "Multiplies two numbers". Bind it via `llm.bind_tools([multiply])` and send the message "Calculate 7 times 6". Print `result.tool_calls` — a list of calls with the function name and arguments. Expected result: in tool_calls the name `multiply` and arguments `{"a": 7, "b": 6}`.

### Task 5
Assemble a mini-RAG with LangChain: create an `InMemoryVectorStore` with three chunks about Python (loops, lists, functions), get a retriever with `k=1`, build the chain `retriever | prompt | llm | parser`, where the prompt requires answering based on context. Ask "How to repeat an action many times?". Expected result: an answer grounded in the chunk about loops.

<!--/TASK-->

<!--HINT-->
### Hint 1
Don't forget to import `StrOutputParser`. The chain is assembled like this: `chain = prompt | llm | StrOutputParser()`, the call is `chain.invoke({"question": "..."})`.

### Hint 2
First prompt: "Extract the topic of the question in one word. Question: {question}". Second: "Write a mini-article (2–3 sentences) on the topic {topic}". Assemble the subchains as in task 1, then call the first one, get `topic`, and substitute it into the second.

### Hint 3
A Pydantic model inherits `BaseModel` from `pydantic`. The prompt must require JSON per the schema, for example: "Extract the order data in JSON format". The call: `llm.with_structured_output(Order)`.

### Hint 4
For `bind_tools` you need the `@tool` decorator and type annotations in the arguments. The result of `llm_with_tools.invoke(...)` is an AIMessage, which has a `tool_calls` attribute with a list of dicts.

### Hint 5
`InMemoryVectorStore.from_texts(chunks, embedding=OpenAIEmbeddings())` requires an API key: it uses OpenAI embeddings. Prompt: "Answer only based on context. Context: {context}. Question: {question}".
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a concise expert. Answer in at most two sentences."),
    ("user", "{question}"),
])
chain = prompt | llm | StrOutputParser()

print(chain.invoke({"question": "What is a virtual environment?"}))
```

Three components are glued into a chain. `ChatPromptTemplate.from_messages` takes a list of tuples (role, text) — the same role format as in chat completions. `StrOutputParser` turns an AIMessage into a string, so `invoke` returns a plain `str`. An LCEL chain can be reused: change the question and don't touch the rest. This is the framework's main advantage over manual integration.

### Solution 2
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

topic_prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract the topic of the question in one word."),
    ("user", "Question: {question}"),
])
article_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a technical writer."),
    ("user", "Write a mini-article (2–3 sentences) on the topic {topic}"),
])

topic_chain = topic_prompt | llm | StrOutputParser()
article_chain = article_prompt | llm | StrOutputParser()

topic = topic_chain.invoke({"question": "What is a function closure?"})
print("Topic:", topic)
print(article_chain.invoke({"topic": topic}))
```

This demonstrates a composable approach: small chains solve simple tasks, and the program orchestrates them. The first chain isolates the essence of the question, the second expands it into text. This is an example of a "multi-step" application: instead of one giant prompt — several small steps, each easy to test separately. Such design is easier to maintain.

### Solution 3
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

class Order(BaseModel):
    product: str
    quantity: int
    price: float

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract the order data and return JSON per the order schema."),
    ("user", "{text}"),
])
chain = prompt | llm.with_structured_output(Order)

obj = chain.invoke({"text": "Bought 2 keyboards for 3500 rubles"})
print(obj.model_dump())
```

`with_structured_output(Order)` is LangChain magic: the model is called in JSON mode and returns a dict that Pydantic validates into an `Order` object. If the `quantity` field turns out to be a string instead of a number, a validation exception occurs — no silent errors. This type checking is the main advantage over "raw" JSON. `model_dump()` turns the object back into a dict.

### Solution 4
```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers."""
    return a * b

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools([multiply])

result = llm_with_tools.invoke("Calculate 7 times 6")
print(result.tool_calls)
```

The model itself decides that a tool is needed for the computation. `bind_tools` passes the model the function descriptions (name, annotations, docstring). The model doesn't compute `7 * 6` in its head; it forms a call request: `{"name": "multiply", "arguments": {"a": 7, "b": 6}}`. Executing the call and returning the result is the job of code, not the model. Agents, which we'll cover in the next lesson, are built on exactly this mechanism.

### Solution 5
```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import InMemoryVectorStore

chunks = [
    "For and while loops allow you to repeat actions several times.",
    "Lists store many elements in a certain order.",
    "Functions group code and let you reuse it.",
]
store = InMemoryVectorStore.from_texts(chunks, embedding=OpenAIEmbeddings())
retriever = store.as_retriever(search_kwargs={"k": 1})

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer only based on context. If there is no answer — say so."),
    ("user", "Context: {context}\n\nQuestion: {question}"),
])
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

chain = (
    {"context": retriever, "question": lambda x: x["question"]}
    | prompt
    | llm
    | StrOutputParser()
)

print(chain.invoke({"question": "How to repeat an action many times?"}))
```

In LCEL, a retriever can be embedded right into the chain: it receives the question and returns context that gets substituted into the prompt. `OpenAIEmbeddings()` uses the OpenAI API for embeddings — the same key is needed. This is a full mini-RAG in four chain lines. If you replace the store with ChromaDB (via `Chroma` from `langchain_chroma`), you get a production variant — the chain structure won't change.

<!--/SOLUTION-->

<!--QUIZ-->
What does the | operator do in LCEL?
- Connects components into a chain
- Compares two values
- Multiplies matrices
* Correct answer: Connects components into a chain
prompt | llm | parser is a data-processing pipeline.

What is StrOutputParser for?
- To turn the model's response into a string
- To increase temperature
- To split text into chunks
* Correct answer: To turn the model's response into a string
It extracts text from an AIMessage.

What does with_structured_output(Order) return?
- A string with JSON
- An object of the Pydantic model Order
- A list of tokens
* Correct answer: An object of the Pydantic model Order
LangChain parses JSON and validates it into an object.

How does the model learn about the existence of a tool?
- Through bind_tools([...])
- By changing temperature
- Through an ordinary prompt
* Correct answer: Through bind_tools([...])
bind_tools passes the function descriptions to the model.

Where is the result of solving "Calculate 7 × 6" when using tools?
- In the model's answer text
- In tool_calls — a request to call the function
- In the dialogue history
* Correct answer: In tool_calls — a request to call the function
The model only requests the call; code computes it.

What does as_retriever() do for a vector store?
- Trains the model
- Turns the store into a search component for the chain
- Deletes documents
* Correct answer: Turns the store into a search component for the chain
The retriever finds the nearest texts and substitutes them into the prompt.

How do you invoke an LCEL chain with data?
- chain.run()
- chain.invoke({"question": ...})
- chain.execute()
* Correct answer: chain.invoke({"question": ...})
invoke takes a dict with values for the template variables (e.g., question).

Why is Pydantic validation better than "raw" JSON parsing?
- It works faster than any parser
- A format error becomes an exception, not silent garbage
- It cancels the model call
* Correct answer: A format error becomes an exception, not silent garbage
Schema validation catches wrong types and missing fields immediately.

<!--/QUIZ-->
