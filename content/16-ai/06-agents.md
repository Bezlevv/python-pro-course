---
title: Агенты: планирование и вызов инструментов
summary: Как устроены агенты: цикл планирования и действий, вызов инструментов (function calling) и реализация собственного агента на Python.
order: 6
duration: 50 мин
difficulty: advanced
tags: агенты, react, function calling, инструменты
---

Обычная LLM-программа — это «вопрос → ответ». Но настоящий **агент** действует: он планирует, вызывает функции, смотрит на результат и решает, что делать дальше. В этом уроке ты построишь собственного агента на чистом Python.

## Что такое агент

Агент — это программа, где модель управляет циклом: **план → действие → наблюдение**. Модель решает, какой инструмент вызвать, код исполняет вызов, а результат (наблюдение) возвращается модели. Цикл повторяется, пока задача не решена.

Такой подход называют **ReAct** (Reasoning + Acting): модель рассуждает и действует по очереди. Схема:

1. Пользователь даёт задачу;
2. Модель либо отвечает сразу, либо решает вызвать инструмент;
3. Код исполняет инструмент и возвращает результат;
4. Шаги 2–3 повторяются до ответа.

## Формат вызова инструментов

API chat completions поддерживает поле `tools` — описания функций. Описание составляется по JSON-схеме:

```python
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Выполняет арифметическое выражение.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string",
                                   "description": "Пример: '2+3*4'"}
                },
                "required": ["expression"],
            },
        },
    }
]
```

Модель в ответе может вернуть `tool_calls` — список запросов на вызов:

```json
{"name": "calculate", "arguments": "{\"expression\": \"2+3*4\"}"}
```

## Исполнение вызова

Код обязан сам выполнить функцию и вернуть результат модели в виде сообщения с ролью `tool`:

```python
import json

def calculate(expression: str) -> str:
    # ВАЖНО: не применяй eval к непроверенному вводу!
    return str(eval(expression, {"__builtins__": {}}, {}))

# для каждого вызова:
result = calculate(json.loads(call["function"]["arguments"])["expression"])
messages.append({
    "role": "tool",
    "tool_call_id": call["id"],
    "content": result,
})
```

`eval` — опасная функция, её используют только в учебных примерах. В продакшне вычисляй выражения безопасным парсером или через `operator`-модуль.

## Полный цикл агента

Соберём всё в единый цикл:

```python
messages = [{"role": "user", "content": "Посчитай 2+3*4"}]

for step in range(5):
    resp = requests.post(..., json={
        "model": "gpt-4o-mini",
        "messages": messages,
        "tools": TOOLS,
    })
    message = resp.json()["choices"][0]["message"]
    messages.append(message)

    if not message.get("tool_calls"):
        print("Финальный ответ:", message["content"])
        break

    for call in message["tool_calls"]:
        fn_name, fn_args = call["function"]["name"], json.loads(call["function"]["arguments"])
        result = FUNCTIONS[fn_name](**fn_args)
        messages.append({"role": "tool", "tool_call_id": call["id"], "content": result})
```

Каждая итерация добавляет сообщения в историю — модель видит результаты и планирует следующий шаг.

## Безопасность и ограничения

- **Максимум итераций** — всегда. Иначе агент зациклится, и счёт за API вырастет.
- **Белый список функций** — вызывай только известные имена из `FUNCTIONS`.
- **Валидация аргументов** — проверяй типы перед исполнением.
- **Human-in-the-loop** — для опасных действий (отправка писем, платежи) запрашивай подтверждение человека.

## Итог

Ты узнал: что такое агент и цикл ReAct; как описать инструменты в формате `tools`; как исполнять `tool_calls` и возвращать результат модели; какие ограничения нужны для безопасной работы. Теперь построим агента.

<!--TASK-->
### Задача 1
Составь список `TOOLS` с описанием инструмента `get_current_time`: функция без аргументов, возвращает текущее время. Опиши параметры пустым объектом `{"type": "object", "properties": {}}`. Напечатай `TOOLS` через `json.dumps` с отступами. Ожидаемый результат: валидный JSON с name = get_current_time.

### Задача 2
Отправь запрос к модели с сообщением «Сколько сейчас времени?» и `tools=TOOLS` (из задачи 1). Распечатай `tool_calls` из ответа. Ожидаемый результат: список с вызовом `get_current_time` и пустыми аргументами.

### Задача 3
Напиши функцию `get_current_time() -> str`, которая возвращает `datetime.now().strftime("%H:%M")`. Затем выполни `tool_call` из задачи 2: распарси JSON, вызови функцию, добавь сообщение с ролью `tool` в `messages` и напечатай его. Ожидаемый результат: сообщение роли tool с текущим временем.

### Задача 4
Собери полный цикл агента с инструментом `calculate` (выражения вида `2+3*4`). Задай вопрос «Посчитай 2+3*4» и позволь агенту крутить цикл до 5 шагов. Печатай на каждом шаге, есть ли tool_calls. Ожидаемый результат: в конце — финальный текстовый ответ с числом 14.

### Задача 5
Расширь агента: добавь второй инструмент `get_weather(city)` (возвращает строку с температурой, можно просто `"20°C"` для любого города). Спроси «Какая погода в Москве? И посчитай 5*8». Проверь, что агент вызывает оба инструмента по очереди и в конце отвечает текстом. Добавь защиту: если имя функции неизвестно — не вызывать, а печатать «Неизвестный инструмент». Ожидаемый результат: агент завершился максимум за 5 шагов и дал ответ.

<!--/TASK-->

<!--HINT-->
### Подсказка 1
Формат: `{"type": "function", "function": {"name": ..., "description": ..., "parameters": ...}}`. Для функции без аргументов: `"parameters": {"type": "object", "properties": {}}`.

### Подсказка 2
После запроса поле ответа `choices[0].message.tool_calls` — список. У каждого элемента есть `function.name` и `function.arguments` (строка с JSON). Если поле отсутствует — модель решила ответить текстом.

### Подсказка 3
Импортируй `datetime`; `json.loads(call["function"]["arguments"])` даст словарь аргументов (у нас пустой). Сообщение tool: `{"role": "tool", "tool_call_id": call["id"], "content": result}` — `tool_call_id` обязателен и должен совпадать с id вызова.

### Подсказка 4
Заведи словарь `FUNCTIONS = {"calculate": calculate}` и вызывай `FUNCTIONS[fn_name](**args)`. Итерации ограничь `for step in range(5)`, а выход — когда в `message` нет `tool_calls`.

### Подсказка 5
Добавь в `FUNCTIONS` вторую функцию и в `TOOLS` — второе описание. Перед вызовом проверяй `if fn_name not in FUNCTIONS` — печатай предупреждение и пропускай. Для проверки порядка инструментов выведи имена вызываемых функций на каждом шаге.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
```python
import json

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Возвращает текущее время в формате ЧЧ:ММ.",
            "parameters": {"type": "object", "properties": {}},
        },
    }
]
print(json.dumps(TOOLS, ensure_ascii=False, indent=2))
```

Schema `parameters` — обязательное поле даже для функций без аргументов: пустой объект `{"type": "object", "properties": {}}` означает «никаких аргументов». `json.dumps` с `indent=2` удобен для проверки структуры. Именно этот JSON уходит в запрос как `tools` — модель «увидит» функцию и сможет решить, когда её вызвать. Описание `description` важно: модель опирается на него при выборе инструмента.

### Разбор 2
```python
import os
import json
import requests

resp = requests.post(
    "https://api.openai.com/v1/chat/completions",
    headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
    json={
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "Сколько сейчас времени?"}],
        "tools": TOOLS,
    },
    timeout=60,
)
resp.raise_for_status()
message = resp.json()["choices"][0]["message"]
print(json.dumps(message.get("tool_calls"), ensure_ascii=False, indent=2))
```

Модель понимает: для ответа на вопрос о времени нужна функция. В `tool_calls` придёт вызов с именем `get_current_time` и аргументами `{}`. Обрати внимание: модель не знает, который час, — она лишь запрашивает вызов. Это и есть делегирование: «думает» модель, а «делает» наш код. Если `tool_calls` отсутствует, значит, модель решила ответить текстом — такой случай тоже надо уметь обрабатывать.

### Разбор 3
```python
from datetime import datetime
import json

def get_current_time() -> str:
    return datetime.now().strftime("%H:%M")

# допустим, call — элемент из tool_calls
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

Функция `get_current_time` — обычный Python-код, без LLM. Мы распарсили JSON-аргументы (`{}`), вызвали функцию и упаковали результат в сообщение роли `tool`. Обязательное поле `tool_call_id` связывает результат с конкретным вызовом — иначе модель не поймёт, к какому запросу относится наблюдение. После этого сообщение добавляется в `messages`, и цикл может продолжиться.

### Разбор 4
```python
import os
import json
import requests

TOOLS = [{"type": "function", "function": {
    "name": "calculate",
    "description": "Выполняет арифметическое выражение.",
    "parameters": {"type": "object", "properties": {
        "expression": {"type": "string", "description": "Пример: '2+3*4'"}
    }, "required": ["expression"]},
}}]

def calculate(expression: str) -> str:
    # ТОЛЬКО для учебного примера. Не используй eval в проде!
    return str(eval(expression, {"__builtins__": {}}, {}))

FUNCTIONS = {"calculate": calculate}
messages = [{"role": "user", "content": "Посчитай 2+3*4"}]

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
        print("Финальный ответ:", message["content"])
        break

    for call in message["tool_calls"]:
        fn_name = call["function"]["name"]
        fn_args = json.loads(call["function"]["arguments"])
        result = FUNCTIONS[fn_name](**fn_args)
        messages.append({"role": "tool", "tool_call_id": call["id"], "content": result})
```

Это полноценный агент: модель видит задачу, вызывает `calculate("2+3*4")`, получает `"14"`, и на следующей итерации уже отвечает текстом. Цикл ограничен 5 шагами — защита от зацикливания. Обрати внимание на порядок: сообщение модели с `tool_calls` тоже должно попасть в историю до tool-сообщений. Так мы реализовали базовый ReAct-цикл на чистом Python.

### Разбор 5
```python
TOOLS = [ ...calculate..., {"type": "function", "function": {
    "name": "get_weather",
    "description": "Возвращает температуру в городе.",
    "parameters": {"type": "object", "properties": {
        "city": {"type": "string", "description": "Название города"}
    }, "required": ["city"]},
}}]

def get_weather(city: str) -> str:
    return f"{city}: 20°C"

FUNCTIONS = {"calculate": calculate, "get_weather": get_weather}
messages = [{"role": "user",
             "content": "Какая погода в Москве? И посчитай 5*8"}]

for step in range(5):
    # ... тот же запрос, что и в разборе 4 ...
    if not message.get("tool_calls"):
        print("Финальный ответ:", message["content"])
        break
    for call in message["tool_calls"]:
        fn_name = call["function"]["name"]
        if fn_name not in FUNCTIONS:
            print("Неизвестный инструмент:", fn_name)
            continue
        fn_args = json.loads(call["function"]["arguments"])
        result = FUNCTIONS[fn_name](**fn_args)
        print(f"Вызов {fn_name} -> {result}")
        messages.append({"role": "tool", "tool_call_id": call["id"], "content": result})
```

Агент сам решит, что для двух подзадач нужны два разных инструмента, и вызовет их по очереди. Проверка `if fn_name not in FUNCTIONS` — критическая защита: если модель «вспомнит» несуществующую функцию, мы не упадём, а предупредим. В реальных агентах добавляют ещё валидацию типов аргументов и перехват исключений внутри функции — ошибка исполнения тоже должна вернуться модели как наблюдение, чтобы она могла скорректировать план.

<!--/SOLUTION-->

<!--QUIZ-->
Что такое цикл ReAct?
- Чередование рассуждения и действия до решения задачи
- Однократный запрос к модели
- Способ ускорить обучение
* Правильный ответ: Чередование рассуждения и действия до решения задачи
Модель планирует, код исполняет, результат возвращается модели.

Где модель «просит» вызвать функцию?
- В поле tool_calls ответа
- В обычном тексте ответа
- В заголовке запроса
* Правильный ответ: В поле tool_calls ответа
tool_calls содержит имена функций и их аргументы.

Что обязательно должно быть в tool-сообщении?
- tool_call_id, совпадающий с вызовом
- Текст «выполнено»
- Новый tools-список
* Правильный ответ: tool_call_id, совпадающий с вызовом
По id модель связывает результат с конкретным запросом.

Зачем ограничивать число итераций агента?
- Чтобы модель не устала
- Чтобы избежать зацикливания и лишних расходов
- Чтобы ускорить первый ответ
* Правильный ответ: Чтобы избежать зацикливания и лишних расходов
Без лимита агент может бесконечно вызывать инструменты.

Какая функция в уроке использовалась с предупреждением об опасности?
- datetime.now()
- eval()
- requests.post()
* Правильный ответ: eval()
eval исполняет произвольный код — её нельзя применять к непроверенному вводу.

Что делает проверка `if fn_name not in FUNCTIONS`?
- Ускоряет агента
- Защищает от вызова несуществующих функций
- Добавляет функцию в словарь
* Правильный ответ: Защищает от вызова несуществующих функций
Неизвестные имена пропускаются с предупреждением.
<!--/QUIZ-->
