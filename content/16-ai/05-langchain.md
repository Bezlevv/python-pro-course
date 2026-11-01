---
title: LangChain: цепи и инструменты
summary: Сборка LLM-приложений с LangChain: промпты, модели, цепи LCEL, структурированный вывод через Pydantic и инструменты.
order: 5
duration: 45 мин
difficulty: advanced
tags: langchain, lcel, pydantic, инструменты
---

Писать интеграцию с LLM API вручную — интересно, но для больших проектов хочется переиспользуемых «кирпичиков». **LangChain** — это фреймворк, который даёт заранее готовые компоненты: промпты, модели, парсеры, ретриверы, инструменты. В этом уроке мы соберём из них приложения.

## Установка

```bash
pip install langchain langchain-openai
```

Компоненты:

- `ChatOpenAI` — обёртка над LLM API;
- `ChatPromptTemplate` — шаблоны промптов;
- `StrOutputParser` — достаёт строку из ответа модели;
- оператор `|` — соединяет компоненты в **цепь** (LCEL).

## Первая цепь

Цепь (chain) — конвейер: данные входят слева, проходят через компоненты, выходят справа.

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
prompt = ChatPromptTemplate.from_messages([
    ("system", "Ты — эксперт по Python."),
    ("user", "{question}"),
])
chain = prompt | llm | StrOutputParser()

print(chain.invoke({"question": "Что такое декоратор?"}))
```

`chain.invoke({"question": ...})` проходит по конвейеру: шаблон подставляет вопрос в промпт, модель отвечает, парсер достаёт текст.

## Что такое LCEL

**LCEL** (LangChain Expression Language) — способ описывать цепи через `|`. Запись `prompt | llm | parser` читается как «сначала промпт, потом модель, потом парсер». Компоненты совместимы, если интерфейс совпадает — это позволяет комбинировать их свободно.

## Структурированный вывод через Pydantic

Вместо «сырого» текста можно получить готовый Python-объект. Для этого описывают Pydantic-модель и используют `with_structured_output`:

```python
from pydantic import BaseModel

class Review(BaseModel):
    rating: int
    pros: list[str]
    cons: list[str]

chain = prompt | llm.with_structured_output(Review)
obj = chain.invoke({"question": "Оцени: Python — удобный язык, но настройка окружения бывает мучительной."})
print(obj.rating, obj.pros, obj.cons)
```

Модель вернёт JSON, а LangChain провалидирует его по схеме. Ошибка формата станет исключением, а не тихим мусором.

## Инструменты

Инструменты (tools) — функции, которые модель может вызвать. Объявляются декоратором `@tool`:

```python
from langchain_core.tools import tool

@tool
def add_numbers(a: int, b: int) -> int:
    """Складывает два числа."""
    return a + b

llm_with_tools = llm.bind_tools([add_numbers])
```

Теперь модель сама решит, когда вызвать `add_numbers`, и вернёт `tool_calls` с аргументами.

## RAG на LangChain

LangChain умеет строить и RAG-цепи: ретривер находит чанки, промпт объединяет их с вопросом, модель отвечает. Векторное хранилище подключается одной строкой:

```python
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

store = InMemoryVectorStore.from_texts(chunks, embedding=OpenAIEmbeddings())
retriever = store.as_retriever(search_kwargs={"k": 2})
```

## Итог

Ты познакомился с базовыми блоками LangChain: промпты, модели, парсеры, цепи LCEL, Pydantic-вывод, инструменты, ретриверы. Теперь соберишь из них настоящие приложения.

<!--TASK-->
### Задача 1
Собери первую цепь: `ChatPromptTemplate` с системным сообщением «Ты — краткий эксперт. Отвечай максимум двумя предложениями», модель `ChatOpenAI(model="gpt-4o-mini")` и `StrOutputParser`. Вызови цепь с вопросом «Что такое виртуальное окружение?» и напечатай результат. Ожидаемый результат: строка — короткий ответ.

### Задача 2
Собери двухшаговую цепь: первая цепь извлекает тему вопроса (проси модель вернуть одно слово), вторая — пишет мини-статью на эту тему. Для этого определи два промпта и две подцепи, вызови последовательно. Ожидаемый результат: сначала печатается тема, затем статья из двух-трёх предложений.

### Задача 3
Создай Pydantic-модель `Order` с полями `product` (str), `quantity` (int), `price` (float). Используй `with_structured_output(Order)`, чтобы извлечь заказ из фразы «Купил 2 клавиатуры по 3500 рублей». Напечатай объект через `obj.model_dump()`. Ожидаемый результат: словарь `{"product": "клавиатура", "quantity": 2, "price": 3500.0}`.

### Задача 4
Объяви через `@tool` функцию `multiply(a: int, b: int) -> int` «Умножает два числа». Привяжи её через `llm.bind_tools([multiply])` и отправь сообщение «Посчитай 7 умножить на 6». Напечатай `result.tool_calls` — список вызовов с именем функции и аргументами. Ожидаемый результат: в tool_calls имя `multiply` и аргументы `{"a": 7, "b": 6}`.

### Задача 5
Собери мини-RAG на LangChain: создай `InMemoryVectorStore` с тремя чанками о Python (циклы, списки, функции), получи ретривер с `k=1`, собери цепь `retriever | prompt | llm | parser`, где промпт требует отвечать по контексту. Задай вопрос «Как повторить действие много раз?». Ожидаемый результат: ответ, основанный на чанке про циклы.

<!--/TASK-->

<!--HINT-->
### Подсказка 1
Не забудь импортировать `StrOutputParser`. Цепь собирается так: `chain = prompt | llm | StrOutputParser()`, вызов — `chain.invoke({"question": "..."})`.

### Подсказка 2
Первый промпт: «Выдели тему вопроса одним словом. Вопрос: {question}». Второй: «Напиши мини-статью (2–3 предложения) на тему {topic}». Подцепи собери как в задаче 1, а потом вызови первую, получи `topic`, и подставь её во вторую.

### Подсказка 3
Pydantic-модель наследует `BaseModel` из `pydantic`. Промпт должен требовать JSON по схеме, например: «Извлеки данные заказа в формате JSON». Вызов: `llm.with_structured_output(Order)`.

### Подсказка 4
Для `bind_tools` нужен `@tool`-декоратор, а в аргументах — аннотации типов. Результат `llm_with_tools.invoke(...)` — AIMessage, у которой есть атрибут `tool_calls` со списком словарей.

### Подсказка 5
`InMemoryVectorStore.from_texts(chunks, embedding=OpenAIEmbeddings())` требует API-ключ: он использует эмбеддинги OpenAI. Промпт: «Отвечай только на основе контекста. Контекст: {context}. Вопрос: {question}».
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
prompt = ChatPromptTemplate.from_messages([
    ("system", "Ты — краткий эксперт. Отвечай максимум двумя предложениями."),
    ("user", "{question}"),
])
chain = prompt | llm | StrOutputParser()

print(chain.invoke({"question": "Что такое виртуальное окружение?"}))
```

Три компонента склеены в цепь. `ChatPromptTemplate.from_messages` принимает список кортежей (роль, текст) — это тот же формат ролей, что и в chat completions. `StrOutputParser` превращает AIMessage в строку, поэтому `invoke` возвращает обычный `str`. LCEL-цепь можно переиспользовать: менять вопрос — и не трогать остальное. Это главное преимущество фреймворка перед ручной интеграцией.

### Разбор 2
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

topic_prompt = ChatPromptTemplate.from_messages([
    ("system", "Выдели тему вопроса одним словом."),
    ("user", "Вопрос: {question}"),
])
article_prompt = ChatPromptTemplate.from_messages([
    ("system", "Ты — технический писатель."),
    ("user", "Напиши мини-статью (2–3 предложения) на тему {topic}"),
])

topic_chain = topic_prompt | llm | StrOutputParser()
article_chain = article_prompt | llm | StrOutputParser()

topic = topic_chain.invoke({"question": "Что такое замыкание функции?"})
print("Тема:", topic)
print(article_chain.invoke({"topic": topic}))
```

Здесь показан композируемый подход: маленькие цепи решают простые задачи, а программа оркестрирует их. Первая цепь вычленяет суть вопроса, вторая разворачивает её в текст. Это пример «многошагового» приложения: вместо одного гигантского промпта — несколько маленьких шагов, каждый из которых легко тестировать отдельно. Такой дизайн проще поддерживать.

### Разбор 3
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
    ("system", "Извлеки данные заказа и верни JSON по схеме заказа."),
    ("user", "{text}"),
])
chain = prompt | llm.with_structured_output(Order)

obj = chain.invoke({"text": "Купил 2 клавиатуры по 3500 рублей"})
print(obj.model_dump())
```

`with_structured_output(Order)` — магия LangChain: модель вызывается в режиме JSON и возвращает словарь, который Pydantic валидирует в объект `Order`. Если поле `quantity` окажется строкой вместо числа, возникнет исключение валидации — тихих ошибок не будет. Такая проверка типов — главное преимущество перед «сырым» JSON. `model_dump()` превращает объект обратно в словарь.

### Разбор 4
```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Умножает два числа."""
    return a * b

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools([multiply])

result = llm_with_tools.invoke("Посчитай 7 умножить на 6")
print(result.tool_calls)
```

Модель сама решает, что для вычисления нужен инструмент. `bind_tools` передаёт модели описания функций (имя, аннотации, docstring). Модель не вычисляет `7 * 6` в голове, а формирует запрос на вызов: `{"name": "multiply", "arguments": {"a": 7, "b": 6}}`. Выполнить вызов и вернуть результат — задача кода, а не модели. Именно на этом механизме строятся агенты, которыми займёмся в следующем уроке.

### Разбор 5
```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import InMemoryVectorStore

chunks = [
    "Циклы for и while позволяют повторять действия несколько раз.",
    "Списки хранят много элементов в определённом порядке.",
    "Функции группируют код и позволяют переиспользовать его.",
]
store = InMemoryVectorStore.from_texts(chunks, embedding=OpenAIEmbeddings())
retriever = store.as_retriever(search_kwargs={"k": 1})

prompt = ChatPromptTemplate.from_messages([
    ("system", "Отвечай только на основе контекста. Если ответа нет — так и скажи."),
    ("user", "Контекст: {context}\n\nВопрос: {question}"),
])
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

chain = (
    {"context": retriever, "question": lambda x: x["question"]}
    | prompt
    | llm
    | StrOutputParser()
)

print(chain.invoke({"question": "Как повторить действие много раз?"}))
```

В LCEL ретривер можно встроить прямо в цепь: он получит вопрос и вернёт контекст, который подставится в промпт. `OpenAIEmbeddings()` использует API OpenAI для эмбеддингов — нужен тот же ключ. Это полноценный мини-RAG в четыре строки цепи. Если заменить хранилище на ChromaDB (через `Chroma` из `langchain_chroma`), получится продакшн-вариант — структура цепи не изменится.

<!--/SOLUTION-->

<!--QUIZ-->
Что делает оператор | в LCEL?
- Соединяет компоненты в цепь
- Сравнивает два значения
- Умножает матрицы
* Правильный ответ: Соединяет компоненты в цепь
prompt | llm | parser — конвейер обработки данных.

Для чего нужен StrOutputParser?
- Чтобы превратить ответ модели в строку
- Чтобы увеличить температуру
- Чтобы разбить текст на чанки
* Правильный ответ: Чтобы превратить ответ модели в строку
Он достаёт текст из AIMessage.

Что возвращает with_structured_output(Order)?
- Строку с JSON
- Объект Pydantic-модели Order
- Список токенов
* Правильный ответ: Объект Pydantic-модели Order
LangChain парсит JSON и валидирует его в объект.

Как модель узнаёт о существовании инструмента?
- Через bind_tools([...])
- Через смену температуры
- Через обычный промпт
* Правильный ответ: Через bind_tools([...])
bind_tools передаёт описания функций модели.

Где находится результат решения «Посчитай 7 × 6» при использовании инструментов?
- В тексте ответа модели
- В tool_calls — запросе на вызов функции
- В истории диалога
* Правильный ответ: В tool_calls — запросе на вызов функции
Модель лишь запрашивает вызов; вычисляет его код.

Что делает as_retriever() у векторного хранилища?
- Обучает модель
- Превращает хранилище в компонент поиска для цепи
- Удаляет документы
* Правильный ответ: Превращает хранилище в компонент поиска для цепи
Ретривер находит ближайшие тексты и подставляет их в промпт.
<!--/QUIZ-->
