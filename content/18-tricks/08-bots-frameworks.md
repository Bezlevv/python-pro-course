---
title: Каркасы ботов: aiogram и discord.py
summary: Современные библиотеки для Telegram- и Discord-ботов: роутеры, клавиатуры, состояния, обработка ошибок.
order: 8
duration: 55 мин
difficulty: intermediate
tags: telegram, discord, aiogram, боты, клавиатуры
---

Написать простого Telegram-бота можно через чистые HTTP-запросы, но удобнее пользоваться фреймворками: `aiogram` (Telegram, асинхронный) и `discord.py` (Discord). Они берут на себя обновления, маршрутизацию и разметку.

## Почему aiogram

- Асинхронность на asyncio;
- Роутеры (Router) вместо огромных if-цепочек;
- Готовые клавиатуры и inline-кнопки;
- FSM (конечные автоматы состояния).

## Структура aiogram-бота

```python
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer("Привет!")
```

## Дискорд-бот

```python
import discord
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.content.startswith("!ping"):
        await message.channel.send("pong")
```

## FSM: состояния

Для диалога «вопрос → ответ» используют StateGroup: `state.set_state(...)`, затем обработчик в состоянии.

## Итог урока

Фреймворки делают ботов модульными и асинхронными; выбор между aiogram и discord.py зависит от платформы.

```mermaid
flowchart LR
    A["Telegram API"] --> B["aiogram"]
    B --> C["Router + F"]
    C --> D["Inline-кнопки"]
    D --> E["FSM диалоги"]
```


## Практическое применение

Боты автоматизируют поддержку, игры, напоминания и интеграции. aiogram подходит для масштабируемых асинхронных ботов с FSM-диалогами; discord.py — для сообществ и игровых проектов. Обе библиотеки имеют развитые роутеры и готовые разметки. Умение собрать бота за вечер — полезный навык и для пет-проектов, и для продакшена.


При разработке ботов важно помнить о безопасности: токен храните в переменной окружения, а не в коде; валидируйте ввод пользователя; ограничивайте частоту команд (rate limit). Тестировать логику бота удобно, вынося обработчики в обычные функции и проверяя их напрямую, без реального API.


<!--TASK-->
### Задача 1 — Приветствие aiogram
Создай минимального бота aiogram с обработчиком /start. Добавь комментарий: какие токен и команды запуска нужны.

### Задача 2 — Ответ на текст
С помощью F.text отфильтруй команды: при сообщении «привет» отвечай «И тебе привет!». Проверь логику через вызов обработчика с сообщением-заглушкой.

### Задача 3 — Клавиатура
Добавь ReplyKeyboardMarkup с кнопками «Факт» и «Шутка». Обработай нажатия — отправь соответствующий текст.

### Задача 4 — Inline-кнопки
Создай inline-клавиатуру с callback-данными (quiz:yes / quiz:no). Обработай CallbackQuery и ответь на callback.

### Задача 5 — FSM: имя
Реализуй двухшаговый диалог: спроси имя, сохрани в state, потом возраст, затем выведи итог. Опиши команды set_state.

### Задача 6 — Discord: эхо-бот
Напиши discord.py-бота: на !ping отвечает pong, на !hello — приветствие. Опиши настройку intents.

### Задача 7 — Обработка ошибок
В aiogram добавь exception handler для любых исключений (log и ответ «Произошла ошибка»). Опиши, что видит пользователь.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Bot(token), Dispatcher(), router посредством dp.include_router(router); dp.run_polling(bot).

### Подсказка 2
F.text == "привет" — фильтр текста.

### Подсказка 3
ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Факт")).

### Подсказка 4
InlineKeyboardMarkup; callback_data в CallbackQuery; answer_callback_query.

### Подсказка 5
class Form(StatesGroup): name = State(); age = State() — задать и читать через state.

### Подсказка 6
intents.message_content = True для чтения сообщений.

### Подсказка 7
dp.errors.register(handler) — глобальный перехват.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
```python
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message

router = Router()

@router.message()
async def echo(message: Message):
    await message.answer("Привет!")

async def main():
    bot = Bot(token="TOKEN")
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
```
Для запуска нужен токен BotFather и asyncio.run(main()).

### Разбор 2
```python
from aiogram import F

@router.message(F.text.lower() == "привет")
async def hello(message: Message):
    await message.answer("И тебе привет!")
```
Фильтры сужают очередь обработчиков.

### Разбор 3
```python
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kb = ReplyKeyboardMarkup(resize_keyboard=True,
                         keyboard=[[KeyboardButton(text="Факт")]])

@router.message(F.text == "Факт")
async def fact(message: Message):
    await message.answer("Python создан в 1991 году.")
```
Кнопки упрощают ввод.

### Разбор 4
```python
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram import F

ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да", callback_data="quiz:yes")],
])

@router.callback_query(F.data == "quiz:yes")
async def yes(cq: CallbackQuery):
    await cq.message.answer("Верно!")
    await cq.answer()
```
Callback-кнопки не отправляют сообщение, а шлют callback.

### Разбор 5
```python
from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    name = State()
    age = State()

@router.message(F.text == "/start")
async def ask_name(message: Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer("Как тебя зовут?")

@router.message(Form.name)
async def got_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.answer("Сколько тебе лет?")
```
FSM хранит данные диалога между шагами.

### Разбор 6
```python
import discord

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!ping"):
        await message.channel.send("pong")
    if message.content.startswith("!hello"):
        await message.channel.send("Привет!")
```
intents.message_content включает чтение текста.

### Разбор 7
```python
import logging

@dp.errors.register()
async def error_handler(event, exception):
    logging.exception(exception)
    # если есть возможность ответить — отправляем:
    # await event.message.answer("Произошла ошибка")
```
Глобальный обработчик логирует и не роняет бота.
<!--/SOLUTION-->

<!--QUIZ-->
Что даёт aiogram?
- Асинхронную обвязку для Telegram Bot API
- Только HTTP-запросы
- Синхронные вызовы
- GUI
* Правильный ответ: Асинхронную обвязку для Telegram Bot API
Dispatcher и Router упрощают обработку.

Что такое Router?
- Объект для группировки обработчиков сообщений
- Тип кнопки
- Формат сообщения
- База данных
* Правильный ответ: Объект для группировки обработчиков сообщений
Модульные обработчики.

Что такое F.text?
- Фильтр текста сообщения
- Формат файла
- Функция отправки
- Тип клавиатуры
* Правильный ответ: Фильтр текста сообщения
Позволяет выбирать обработчик.

Что такое inline-кнопка?
- Кнопка внутри сообщения с callback_data
- Кнопка под полем ввода
- Только ссылка
- Кнопка паузы
* Правильный ответ: Кнопка внутри сообщения с callback_data
Она не отправляет сообщение, а вызывает callback.

Что такое FSM?
- Конечные автоматы состояний
- Файловая система
- Формат сообщений
- Быстрый поиск
* Правильный ответ: Конечные автоматы состояний
Диалог с несколькими шагами.

Как сохранить данные между шагами FSM?
- state.update_data(...)
- message.data
- bot.store
- session.save
* Правильный ответ: state.update_data(...)
Данные кладутся в состояние.

Что нужно для discord.py, чтобы читать сообщения?
- intents.message_content = True
- intents.guilds
- token
- permissions
* Правильный ответ: intents.message_content = True
Интенты разрешают доступ к контенту.

Что делает answer_callback_query?
- Подтверждает получение callback
- Отправляет фото
- Удаляет сообщение
- Закрывает чат
* Правильный ответ: Подтверждает получение callback
Без ответа кнопка «висит».

Для чего глобальный error handler?
- Чтобы бот не падал при исключениях
- Чтобы ускорить
- Чтобы логировать только старт
- Чтобы отключить бота
* Правильный ответ: Чтобы бот не падал при исключениях
Исключения перехватываются и логируются.

Какая библиотека используется для Discord?
- discord.py
- aiogram
- telebot
- vk_api
* Правильный ответ: discord.py
Популярный фреймворк для Discord-ботов.
Что делает Dispatcher?
- Распределяет обновления по обработчикам
- Пишет в БД
- Рисует клавиатуры
- Отправляет фото
* Правильный ответ: Распределяет обновления по обработчикам
Маршрутизация событий.

Что такое callback_data?
- Строка-метка кнопки для обработчика
- Текст кнопки
- Идентификатор чата
- Формат сообщения
* Правильный ответ: Строка-метка кнопки для обработчика
По ней выбирается обработчик.


<!--/QUIZ-->
