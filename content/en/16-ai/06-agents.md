---
title: Agents: planning and tool calls
summary: How agents work: the planning-and-acting loop, tool calls (function calling), and implementing your own agent in Python.
order: 6
duration: 50 min
difficulty: advanced
tags: agents, react, function calling, tools
---

An ordinary LLM program is "question → answer". But a real **agent** acts: it plans, calls functions, looks at the result, and decides what to do next. In this lesson, you'll build your own agent in pure Python.

## What is an agent

An agent is a program where the model drives a loop: **plan → act → observe**. The model decides which tool to call, the code executes the call, and the result (observation) is returned to the model. The loop repeats until the task is solved.

This approach is called **ReAct** (Reasoning + Acting): the model reasons and acts in turn. The scheme:

1. The user gives a task;
2. The model either answers immediately or decides to call a tool;
3. The code executes the tool and returns the result;
4. Steps 2–3 repeat until the answer.

## Tool call format

The chat completions API supports the `tools` field — function descriptions. A description is written per the JSON schema:

```python
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluates an arithmetic expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string",
                                   "description": "Example: '2+3*4'"}
                },
                "required": ["expression"],
            },
        },
    }
]
```

The model may return `tool_calls` in its response — a list of call requests:

```json
{"name": "calculate", "arguments": "{\"expression\": \"2+3*4\"}"}
```

## Executing a call

The code must execute the function itself and return the result to the model as a message with the `tool` role:

```python
import json

def calculate(expression: str) -> str:
    # IMPORTANT: do not apply eval to untrusted input!
    return str(eval(expression, {"__builtins__": {}}, {}))

# for each call:
result = calculate(json.loads(call["function"]["arguments"])["expression"])
messages.append({
    "role": "tool",
    "tool_call_id": call["id"],
    "content": result,
})
```

`eval` is a dangerous function; it is used only in educational examples. In production, evaluate expressions with a safe parser or the `operator` module.

## The full agent loop

Let's put it all into a single loop:

```python
messages = [{"role": "user", "content": "Calculate 2+3*4"}]

for step in range(5):
    resp = requests.post(..., json={
        "model": "gpt-4o-mini",
        "messages": messages,
        "tools": TOOLS,
    })
    message = resp.json()["choices"][0]["message"]
    messages.append(message)

    if not message.get("tool_calls"):
        print("Final answer:", message["content"])
        break

    for call in message["tool_calls"]:
        fn_name, fn_args = call["function"]["name"], json.loads(call["function"]["arguments"])
        result = FUNCTIONS[fn_name](**fn_args)
        messages.append({"role": "tool", "tool_call_id": call["id"], "content": result})
```

Each iteration adds messages to the history — the model sees the results and plans the next step.

## Safety and limitations

- **Maximum iterations** — always. Otherwise the agent loops forever, and the API bill grows.
- **Function whitelist** — call only known names from `FUNCTIONS`.
- **Argument validation** — check types before execution.
- **Human-in-the-loop** — for dangerous actions (sending emails, payments), ask for human confirmation.

## Summary

You learned: what an agent and the ReAct loop are; how to describe tools in the `tools` format; how to execute `tool_calls` and return the result to the model; what limitations are needed for safe operation. Now let's build an agent.

<!--TASK-->
### Task 1
Compose a list `TOOLS` with a description of the tool `get_current_time`: a function with no arguments that returns the current time. Describe parameters as an empty object `{"type": "object", "properties": {}}`. Print `TOOLS` via `json.dumps` with indentation. Expected result: valid JSON with name = get_current_time.

### Task 2
Send a request to the model with the message "What time is it now?" and `tools=TOOLS` (from task 1). Print `tool_calls` from the response. Expected result: a list with a `get_current_time` call and empty arguments.

### Task 3
Write a function `get_current_time() -> str` that returns `datetime.now().strftime("%H:%M")`. Then execute the `tool_call` from task 2: parse the JSON, call the function, add a message with the `tool` role to `messages`, and print it. Expected result: a tool-role message with the current time.

### Task 4
Assemble a full agent loop with the `calculate` tool (expressions like `2+3*4`). Ask "Calculate 2+3*4" and let the agent loop up to 5 steps. Print at each step whether there are tool_calls. Expected result: at the end — a final text answer with the number 14.

### Task 5
Extend the agent: add a second tool `get_weather(city)` (returns a string with the temperature, e.g., simply "20°C" for any city). Ask "What's the weather in Moscow? And calculate 5*8". Verify that the agent calls both tools in turn and finally answers with text. Add protection: if the function name is unknown — don't call it, print "Unknown tool" instead. Expected result: the agent finishes in at most 5 steps and gives an answer.

<!--/TASK-->

<!--HINT-->
### Hint 1
Format: `{"type": "function", "function": {"name": ..., "description": ..., "parameters": ...}}`. For a function with no arguments: `"parameters": {"type": "object", "properties": {}}`.

### Hint 2
After the request, the response field `choices[0].message.tool_calls` is a list. Each element has `function.name` and `function.arguments` (a string with JSON). If the field is absent — the model decided to answer with text.

### Hint 3
Import `datetime`; `json.loads(call["function"]["arguments"])` gives a dict of arguments (empty for us). The tool message: `{"role": "tool", "tool_call_id": call["id"], "content": result}` — `tool_call_id` is required and must match the call's id.

### Hint 4
Create a dict `FUNCTIONS = {"calculate": calculate}` and call `FUNCTIONS[fn_name](**args)`. Limit iterations with `for step in range(5)`, and exit when `message` has no `tool_calls`.

### Hint 5
Add a second function to `FUNCTIONS` and a second description to `TOOLS`. Before calling, check `if fn_name not in FUNCTIONS` — print a warning and skip. To check the order of tools, print the names of the called functions at each step.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import json

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Returns the current time in HH:MM format.",
            "parameters": {"type": "object", "properties": {}},
        },
    }
]
print(json.dumps(TOOLS, ensure_ascii=False, indent=2))
```

The `parameters` schema is mandatory even for functions without arguments: an empty object `{"type": "object", "properties": {}}` means "no arguments". `json.dumps` with `indent=2` is convenient for inspecting the structure. This is exactly the JSON that goes into the request as `tools` — the model "sees" the function and can decide when to call it. The `description` matters: the model relies on it when choosing a tool.

### Solution 2
```python
import os
import json
import requests

resp = requests.post(
    "https://api.openai.com/v1/chat/completions",
    headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
    json={
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "What time is it now?"}],
        "tools": TOOLS,
    },
    timeout=60,
)
resp.raise_for_status()
message = resp.json()["choices"][0]["message"]
print(json.dumps(message.get("tool_calls"), ensure_ascii=False, indent=2))
```

The model understands that a function is needed to answer the time question. `tool_calls` will contain a call with the name `get_current_time` and arguments `{}`. Note: the model doesn't know what time it is — it only requests a call. This is delegation: the model "thinks", and our code "does". If `tool_calls` is absent, the model decided to answer with text — such a case should also be handled.

### Solution 3
```python
from datetime import datetime
import json

def get_current_time() -> str:
    return datetime.now().strftime("%H:%M")

# suppose call is an element from tool_calls
call = message["tool_calls"][0]
fn_args = json.loads(call["function"]["arguments"])
result = get_current_time(**fn_args)

messages.append({
    "role": "tool",
    "tool_call_id": call["id"],
    "content": result,
})
print(messages[-1])
```

The `get_current_time` function is ordinary Python code, no LLM. We parsed the JSON arguments (`{}`), called the function, and packed the result into a `tool`-role message. The required `tool_call_id` field ties the result to a specific call — otherwise the model won't understand which request the observation belongs to. After that, the message is added to `messages`, and the loop can continue.

### Solution 4
```python
import os
import json
import requests

TOOLS = [{"type": "function", "function": {
    "name": "calculate",
    "description": "Evaluates an arithmetic expression.",
    "parameters": {"type": "object", "properties": {
        "expression": {"type": "string", "description": "Example: '2+3*4'"}
    }, "required": ["expression"]},
}}]

def calculate(expression: str) -> str:
    # ONLY for the educational example. Do not use eval in production!
    return str(eval(expression, {"__builtins__": {}}, {}))

FUNCTIONS = {"calculate": calculate}
messages = [{"role": "user", "content": "Calculate 2+3*4"}]

for step in range(5):
    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
        json={"model": "gpt-4o-mini", "messages": messages, "tools": TOOLS},
        timeout=60,
    )
    resp.raise_for_status()
    message = resp.json()["choices"][0]["message"]
    messages.append(message)

    if not message.get("tool_calls"):
        print("Final answer:", message["content"])
        break

    for call in message["tool_calls"]:
        fn_name = call["function"]["name"]
        fn_args = json.loads(call["function"]["arguments"])
        result = FUNCTIONS[fn_name](**fn_args)
        messages.append({"role": "tool", "tool_call_id": call["id"], "content": result})
```

This is a full agent: the model sees the task, calls `calculate("2+3*4")`, gets `"14"`, and on the next iteration already answers with text. The loop is limited to 5 steps — protection against infinite looping. Note the order: the model's message with `tool_calls` must also enter the history before the tool messages. This is how we implemented a basic ReAct loop in pure Python.

### Solution 5
```python
TOOLS = [ ...calculate..., {"type": "function", "function": {
    "name": "get_weather",
    "description": "Returns the temperature in a city.",
    "parameters": {"type": "object", "properties": {
        "city": {"type": "string", "description": "City name"}
    }, "required": ["city"]},
}}]

def get_weather(city: str) -> str:
    return f"{city}: 20°C"

FUNCTIONS = {"calculate": calculate, "get_weather": get_weather}
messages = [{"role": "user",
             "content": "What's the weather in Moscow? And calculate 5*8"}]

for step in range(5):
    # ... the same request as in solution 4 ...
    if not message.get("tool_calls"):
        print("Final answer:", message["content"])
        break
    for call in message["tool_calls"]:
        fn_name = call["function"]["name"]
        if fn_name not in FUNCTIONS:
            print("Unknown tool:", fn_name)
            continue
        fn_args = json.loads(call["function"]["arguments"])
        result = FUNCTIONS[fn_name](**fn_args)
        print(f"Call {fn_name} -> {result}")
        messages.append({"role": "tool", "tool_call_id": call["id"], "content": result})
```

The agent itself decides that two subtasks need two different tools and calls them in turn. The check `if fn_name not in FUNCTIONS` is critical protection: if the model "recalls" a nonexistent function, we don't crash but warn. Real agents also add argument type validation and exception handling inside the function — an execution error should also return to the model as an observation so it can adjust the plan.

<!--/SOLUTION-->

<!--QUIZ-->
What is the ReAct loop?
- Alternating reasoning and acting until the task is solved
- A single request to the model
- A way to speed up training
* Correct answer: Alternating reasoning and acting until the task is solved
The model plans, code executes, the result is returned to the model.

Where does the model "ask" to call a function?
- In the tool_calls field of the response
- In the plain text of the response
- In the request header
* Correct answer: In the tool_calls field of the response
tool_calls contains function names and their arguments.

What must be in a tool message?
- tool_call_id matching the call
- The text "done"
- A new tools list
* Correct answer: tool_call_id matching the call
By the id, the model ties the result to a specific request.

Why limit the number of agent iterations?
- So the model doesn't get tired
- To avoid infinite loops and extra costs
- To speed up the first answer
* Correct answer: To avoid infinite loops and extra costs
Without a limit, the agent could call tools endlessly.

Which function in the lesson was used with a warning about danger?
- datetime.now()
- eval()
- requests.post()
* Correct answer: eval()
eval executes arbitrary code — it must not be applied to untrusted input.

What does the check `if fn_name not in FUNCTIONS` do?
- Speeds up the agent
- Protects against calling nonexistent functions
- Adds a function to the dict
* Correct answer: Protects against calling nonexistent functions
Unknown names are skipped with a warning.

What is human-in-the-loop (HITL) in agents?
- The agent's ability to work offline
- Human confirmation before dangerous actions (payments, sending emails)
- A way to speed up the agent loop
* Correct answer: Human confirmation before dangerous actions (payments, sending emails)
For irreversible or risky actions, the agent stops and waits for a human decision.

What should the code do after the model returns tool_calls?
- Just print the model's answer
- Execute the corresponding functions and return the results to the model via tool messages
- Restart the request without tools
* Correct answer: Execute the corresponding functions and return the results to the model via tool messages
This way the agent gets observations and continues the planning loop.

<!--/QUIZ-->
