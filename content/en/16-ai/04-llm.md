---
title: LLM: prompts and API usage
summary: What LLMs are, prompt design, API calls.
order: 4
duration: 45 min
difficulty: intermediate
tags: llm, prompt, api
---

Large language models generate text from prompts.

## Prompt design

- Be specific;
- Give context;
- Ask for a format.

Example:

```text
Summarize the text below in 3 bullet points:
<text>
```

## API

```python
import openai

client = openai.OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

## Lesson summary

Clear prompts and API calls power LLM apps.

<!--TASK-->
### Task 1 — Prompt
Write a prompt for a summary.

### Task 2 — Format
Ask for JSON output.

### Task 3 — Call
Make a chat completion call.

### Task 4 — Extract
Get the text from the response.

### Task 5 — System role
Use a system message.

### Task 6 — Temperature
Explain temperature.

### Task 7 — Hallucination
Define and mitigate.
<!--/TASK-->

<!--HINT-->
### Hint 1
Specific.

### Hint 2
JSON.

### Hint 3
chat.completions.

### Hint 4
choices[0].

### Hint 5
System.

### Hint 6
Randomness.

### Hint 7
Grounding.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```text
Summarize the text below in 3 bullet points:
<text>
```

### Solution 2
```text
Answer as JSON: {"answer": "..."}
```

### Solution 3
```python
import openai
client = openai.OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello!"}],
)
```

### Solution 4
```python
text = response.choices[0].message.content
```

### Solution 5
```python
messages=[
    {"role": "system", "content": "You are a helpful tutor."},
    {"role": "user", "content": "Explain floats."},
]
```

### Solution 6
```python
# temperature: 0 — детерминированно, 1 — разнообразно
# для фактов лучше низкая
```

### Solution 7
```python
# Галлюцинация — уверенный, но ложный ответ.
# Митигация: контекст, факты, проверка
```
<!--/SOLUTION-->

<!--QUIZ-->
What is an LLM?
- Large language model
- A database
- A browser
- None
* Correct answer: Large language model
Text.

What is a prompt?
- Instruction
- Output
- Model
- None
* Correct answer: Instruction
Input.

What is a system message?
- Role setting
- User text
- Output
- None
* Correct answer: Role setting
Tutor.

What is temperature?
- Randomness
- Speed
- Size
- None
* Correct answer: Randomness
Sampling.

What is hallucination?
- False confident answer
- True answer
- Error
- None
* Correct answer: False confident answer
Risk.

What is a completion?
- Generated text
- Prompt
- Model
- None
* Correct answer: Generated text
Response.

What is a choice?
- Candidate answer
- A prompt
- A role
- None
* Correct answer: Candidate answer
List.

What is the API?
- Interface to service
- A model
- A prompt
- None
* Correct answer: Interface to service
openai.

What is grounding?
- Anchoring to facts
- Hallucination
- Prompt
- None
* Correct answer: Anchoring to facts
Mitigation.

What is a role?
- user/system/assistant
- A model
- A token
- None
* Correct answer: user/system/assistant
Message.

What is token?
- Text unit
- A prompt
- An API
- None
* Correct answer: Text unit
Count.

What is the best prompt?
- Specific and clear
- Vague
- Short only
- None
* Correct answer: Specific and clear
Effective.
<!--/QUIZ-->
