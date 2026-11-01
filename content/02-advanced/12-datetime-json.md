---
title: datetime и JSON
summary: Работа с датами и временем через datetime и обмен данными в формате JSON.
order: 12
duration: 25 мин
difficulty: intermediate
---

Почти любая программа работает с датами или обменивается структурированными данными. Модули `datetime` и `json` покрывают обе задачи.

## Модуль datetime

Основные типы: `date` (дата), `time` (время), `datetime` (и то и другое), `timedelta` (разница). Получить текущий момент:

```python
from datetime import datetime

now = datetime.now()
print(now)            # 2026-11-01 14:20:00.123456
print(now.year)       # 2026
print(now.month)      # 11
print(now.day)        # 1
```

## Форматирование и разбор строк

`strftime` превращает дату в строку по формату, `strptime` — наоборот:

```python
formatted = now.strftime("%d.%m.%Y %H:%M")
print(formatted)  # 01.11.2026 14:20

parsed = datetime.strptime("15.07.2025", "%d.%m.%Y")
print(parsed)  # 2025-07-15 00:00:00
```

Популярные директивы: `%Y` — год, `%m` — месяц, `%d` — день, `%H` — часы, `%M` — минуты.

## Арифметика: timedelta

Из дат можно вычитать и к ним прибавлять интервалы:

```python
from datetime import timedelta

tomorrow = now + timedelta(days=1)
delta = tomorrow - now
print(delta.total_seconds())  # 86400.0
```

## JSON: dumps и loads

JSON — текстовый формат обмена данными, понятный почти всем языкам. Python-объекты превращаются в JSON-строку через `dumps`, а обратно — через `loads`:

```python
import json

data = {"name": "Аня", "age": 25, "tags": ["python", "курс"]}
s = json.dumps(data, ensure_ascii=False, indent=2)
print(s)
```

`ensure_ascii=False` оставляет русские буквы как есть, `indent=2` придаёт читабельный вид.

## Файлы: dump и load

Для работы с файлами используются `dump` и `load`:

```python
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("data.json", encoding="utf-8") as f:
    restored = json.load(f)

print(restored["name"])  # Аня
```

## Нестандартные объекты

`datetime` не сериализуется в JSON напрямую — будет ошибка. Решение: переводить в ISO-строку `isoformat()` или передать `default=str` в `dumps`.

## Итог урока

Мы узнали:

- типы `datetime` и `timedelta`;
- `strftime`/`strptime` для форматирования;
- `json.dumps`/`json.loads` и `json.dump`/`json.load`;
- опции `ensure_ascii`, `indent`;
- почему `datetime` не сериализуется напрямую.

Закрепим практикой.

<!--TASK-->
**Задача.** Создай список событий — словарей с ключами `name` и `date` (дата в формате `"ГГГГ-ММ-ДД"`), например Новый год (2026-12-31), День рождения (2026-11-15), релиз проекта (2027-03-01). Сохрани список в файл `events.json` (с `ensure_ascii=False` и `indent=2`), затем прочитай его обратно, распарси даты через `date.fromisoformat` и для каждого события выведи строку вида `"Новый год: осталось 60 дн."` Количество дней считай от сегодняшней даты (`date.today()`) — оно зависит от дня запуска.
<!--/TASK-->

<!--HINT-->
Записывай и читай через `with open(..., encoding="utf-8")`. В цикле сравнивай `event_date - today` и бери `.days` из `timedelta`. Не перепутай `dump` (в файл) и `dumps` (в строку).
<!--/HINT-->

<!--SOLUTION-->
Решение:

```python
from datetime import date
import json

events = [
    {"name": "Новый год", "date": "2026-12-31"},
    {"name": "День рождения", "date": "2026-11-15"},
    {"name": "Релиз проекта", "date": "2027-03-01"},
]

with open("events.json", "w", encoding="utf-8") as f:
    json.dump(events, f, ensure_ascii=False, indent=2)

with open("events.json", encoding="utf-8") as f:
    loaded = json.load(f)

today = date.today()
for event in loaded:
    when = date.fromisoformat(event["date"])
    left = (when - today).days
    print(f"{event['name']}: осталось {left} дн.")
```

Что здесь происходит? Сначала `json.dump` сохраняет список словарей в файл: `ensure_ascii=False` сохраняет кириллицу, `indent=2` — красивое оформление. Затем `json.load` восстанавливает ровно тот же список. `date.fromisoformat` принимает строку вида `"2026-12-31"` и превращает её в объект `date`. Разность двух дат даёт `timedelta`, а свойство `.days` — целое число дней. Осталось подставить его в f-строку.

Пример вывода (при запуске 1 ноября 2026 года):

```
Новый год: осталось 60 дн.
День рождения: осталось 14 дн.
Релиз проекта: осталось 120 дн.
```

Такой пары «JSON для хранения + datetime для вычислений» хватает для множества реальных задач: напоминания, планы, ленты событий.
<!--/SOLUTION-->
