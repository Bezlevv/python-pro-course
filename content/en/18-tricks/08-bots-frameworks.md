---
title: Bot Frameworks: aiogram and discord.py
summary: Modern libraries for Telegram and Discord bots: routers, keyboards, states, error handling.
order: 8
duration: 55 min
difficulty: intermediate
tags: telegram, discord, aiogram, bots, keyboards
---

You can write a simple Telegram bot with raw HTTP requests, but it's more convenient to use frameworks: `aiogram` (Telegram, asynchronous) and `discord.py` (Discord). They take over updates, routing, and markup.

## Why aiogram

- Asynchronicity on asyncio;
- Routers (Router) instead of giant if-chains;
- Ready-made keyboards and inline buttons;
- FSM (finite state machines).

## Structure of an aiogram Bot

```python
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer("Hi!")
```

## Discord Bot

```python
import discord
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.content.startswith("!ping"):
        await message.channel.send("pong")
```

## FSM: States

For a "question → answer" dialog, StateGroup is used: `state.set_state(...)`, then a handler in the state.

## Lesson Summary

Frameworks make bots modular and asynchronous; the choice between aiogram and discord.py depends on the platform.

```mermaid
flowchart LR
    A["Telegram API"] --> B["aiogram"]
    B --> C["Router + F"]
    C --> D["Inline buttons"]
    D --> E["FSM dialogs"]
```


## Practical Application

Bots automate support, games, reminders, and integrations. aiogram suits scalable asynchronous bots with FSM dialogs; discord.py — for communities and game projects. Both libraries have developed routers and ready-made markup. Being able to assemble a bot in one evening is a useful skill for both pet projects and production.


When developing bots, it's important to remember security: keep the token in an environment variable, not in code; validate user input; rate-limit commands. It's convenient to test bot logic by extracting handlers into plain functions and checking them directly, without the real API.


<!--TASK-->
### Task 1 — aiogram Greeting
Create a minimal aiogram bot with a /start handler. Add a comment: what token and launch commands are needed.

### Task 2 — Text Reply
Use F.text to filter commands: on the message "hi" reply "And hi to you!". Test the logic by calling the handler with a stub message.

### Task 3 — Keyboard
Add a ReplyKeyboardMarkup with "Fact" and "Joke" buttons. Handle presses — send the corresponding text.

### Task 4 — Inline Buttons
Create an inline keyboard with callback data (quiz:yes / quiz:no). Handle CallbackQuery and answer the callback.

### Task 5 — FSM: Name
Implement a two-step dialog: ask for the name, save it in state, then age, then output the summary. Describe the set_state commands.

### Task 6 — Discord: Echo Bot
Write a discord.py bot: on !ping respond pong, on !hello — a greeting. Describe intents configuration.

### Task 7 — Error Handling
In aiogram, add an exception handler for any exceptions (log and the reply "An error occurred"). Describe what the user sees.
<!--/TASK-->

<!--HINT-->
### Hint 1
Bot(token), Dispatcher(), router via dp.include_router(router); dp.run_polling(bot).

### Hint 2
F.text == "hi" — text filter.

### Hint 3
ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Fact")).

### Hint 4
InlineKeyboardMarkup; callback_data in CallbackQuery; answer_callback_query.

### Hint 5
class Form(StatesGroup): name = State(); age = State() — set and read via state.

### Hint 6
intents.message_content = True to read messages.

### Hint 7
dp.errors.register(handler) — global interception.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message

router = Router()

@router.message()
async def echo(message: Message):
    await message.answer("Hi!")

async def main():
    bot = Bot(token="TOKEN")
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
```
To launch, you need a BotFather token and asyncio.run(main()).

### Solution 2
```python
from aiogram import F

@router.message(F.text.lower() == "hi")
async def hello(message: Message):
    await message.answer("And hi to you!")
```
Filters narrow the queue of handlers.

### Solution 3
```python
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kb = ReplyKeyboardMarkup(resize_keyboard=True,
                         keyboard=[[KeyboardButton(text="Fact")]])

@router.message(F.text == "Fact")
async def fact(message: Message):
    await message.answer("Python was created in 1991.")
```
Buttons simplify input.

### Solution 4
```python
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram import F

ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Yes", callback_data="quiz:yes")],
])

@router.callback_query(F.data == "quiz:yes")
async def yes(cq: CallbackQuery):
    await cq.message.answer("Correct!")
    await cq.answer()
```
Callback buttons don't send a message; they send a callback.

### Solution 5
```python
from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    name = State()
    age = State()

@router.message(F.text == "/start")
async def ask_name(message: Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer("What's your name?")

@router.message(Form.name)
async def got_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.answer("How old are you?")
```
FSM stores dialog data between steps.

### Solution 6
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
        await message.channel.send("Hi!")
```
intents.message_content enables reading text.

### Solution 7
```python
import logging

@dp.errors.register()
async def error_handler(event, exception):
    logging.exception(exception)
    # if there's a chance to reply — send:
    # await event.message.answer("An error occurred")
```
The global handler logs and doesn't crash the bot.
<!--/SOLUTION-->

<!--QUIZ-->
What does aiogram provide?
- An async wrapper for the Telegram Bot API
- Only HTTP requests
- Synchronous calls
- GUI
* Correct answer: An async wrapper for the Telegram Bot API
Dispatcher and Router simplify handling.

What is a Router?
- An object for grouping message handlers
- A button type
- A message format
- A database
* Correct answer: An object for grouping message handlers
Modular handlers.

What is F.text?
- A filter for message text
- A file format
- A send function
- A keyboard type
* Correct answer: A filter for message text
It lets you choose a handler.

What is an inline button?
- A button inside a message with callback_data
- A button below the input field
- Only a link
- A pause button
* Correct answer: A button inside a message with callback_data
It doesn't send a message; it triggers a callback.

What is FSM?
- Finite state machines
- A file system
- A message format
- Fast search
* Correct answer: Finite state machines
A dialog with several steps.

How do you save data between FSM steps?
- state.update_data(...)
- message.data
- bot.store
- session.save
* Correct answer: state.update_data(...)
Data is placed into the state.

What does discord.py need to read messages?
- intents.message_content = True
- intents.guilds
- token
- permissions
* Correct answer: intents.message_content = True
Intents grant access to content.

What does answer_callback_query do?
- Confirms the callback receipt
- Sends a photo
- Deletes the message
- Closes the chat
* Correct answer: Confirms the callback receipt
Without an answer, the button "hangs".

What is a global error handler for?
- So the bot doesn't crash on exceptions
- To speed up
- To log only the start
- To disable the bot
* Correct answer: So the bot doesn't crash on exceptions
Exceptions are intercepted and logged.

Which library is used for Discord?
- discord.py
- aiogram
- telebot
- vk_api
* Correct answer: discord.py
A popular framework for Discord bots.
What does Dispatcher do?
- Distributes updates to handlers
- Writes to the DB
- Draws keyboards
- Sends photos
* Correct answer: Distributes updates to handlers
Event routing.

What is callback_data?
- A button label string for a handler
- The button text
- A chat identifier
- A message format
* Correct answer: A button label string for a handler
The handler is chosen by it.


<!--/QUIZ-->
