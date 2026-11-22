---
title: Telegram bot: aiogram
summary: Bot token, handlers, states.
order: 2
duration: 50 min
difficulty: intermediate
tags: telegram, bot, aiogram
---

Bots automate conversations in Telegram.

## Token

Get from @BotFather.

## aiogram

```python
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

bot = Bot(token="TOKEN")
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Hello!")

@dp.message(F.text)
async def echo(message: Message):
    await message.answer(message.text)

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
```

## Lesson summary

Decorators + async handlers drive bots.

<!--TASK-->
### Task 1 — Setup
Create Bot and Dispatcher.

### Task 2 — Start
Handle /start.

### Task 3 — Echo
Echo any text.

### Task 4 — State
Add a simple state/command flow.

### Task 5 — Buttons
Send a button.

### Task 6 — Run
Start polling.

### Task 7 — Token
Where to get a token?
<!--/TASK-->

<!--HINT-->
### Hint 1
Bot.

### Hint 2
CommandStart.

### Hint 3
F.text.

### Hint 4
State.

### Hint 5
ReplyKeyboardMarkup.

### Hint 6
start_polling.

### Hint 7
BotFather.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from aiogram import Bot, Dispatcher
bot = Bot(token="TOKEN")
dp = Dispatcher()
```

### Solution 2
```python
from aiogram.filters import CommandStart
from aiogram.types import Message

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Hello!")
```

### Solution 3
```python
from aiogram import F

@dp.message(F.text)
async def echo(message: Message):
    await message.answer(message.text)
```

### Solution 4
```python
# Команда /name → ждём имя → ответ
# Реализуется через FSM (State) и memory storage
```

### Solution 5
```python
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Help")]
])
await message.answer("Menu", reply_markup=kb)
```

### Solution 6
```python
if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
```

### Solution 7
```python
# Токен выдаёт @BotFather: /newbot → токен
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a bot token?
- Secret key
- A user
- A chat
- None
* Correct answer: Secret key
BotFather.

What is aiogram?
- Bot framework
- A game
- A browser
- None
* Correct answer: Bot framework
Async.

What is a handler?
- Function for event
- A bot
- A token
- None
* Correct answer: Function for event
Decorator.

What is CommandStart?
- /start filter
- Any text
- A button
- None
* Correct answer: /start filter
Command.

What is F.text?
- Text filter
- Command
- Callback
- None
* Correct answer: Text filter
Magic.

What is answer?
- Sends message
- Receives
- Deletes
- None
* Correct answer: Sends message
Reply.

What is async?
- Non-blocking
- Blocking
- Sync
- None
* Correct answer: Non-blocking
Await.

What is polling?
- Listening updates
- Sending
- Stopping
- None
* Correct answer: Listening updates
Loop.

What is FSM?
- Finite state machine
- File system
- A filter
- None
* Correct answer: Finite state machine
States.

What is a keyboard?
- Buttons
- Text
- Reply
- None
* Correct answer: Buttons
UI.

What is a callback?
- Button action
- Message
- Token
- None
* Correct answer: Button action
Data.

What is @BotFather?
- Bot creation
- A user bot
- An API
- None
* Correct answer: Bot creation
Token.
<!--/QUIZ-->
