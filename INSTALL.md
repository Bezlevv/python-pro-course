# 📦 Инструкция по запуску курса «PythonПро»

Этот пакет — полный исходный код платформы-курса PythonПро:
31 модуль, 253 урока, викторины, автопроверка кода, экзамены,
достижения, сертификат, телеграм-бот, Docker-конфигурация.

---

## Оглавление

1. [Требования](#1-требования)
2. [Быстрый старт на Windows](#2-быстрый-старт-на-windows)
3. [Запуск вручную (Windows / macOS / Linux)](#3-запуск-вручную)
4. [Запуск через Docker](#4-запуск-через-docker)
5. [Админ-панель](#5-админ-панель)
6. [Добавление/редактирование уроков](#6-добавление-редактирование-уроков)
7. [Проверки проекта](#7-проверки-проекта)
8. [Telegram-бот (опционально)](#8-telegram-бот-опционально)
9. [Возможные проблемы](#9-возможные-проблемы)

---

## 1. Требования

- **Python 3.10+** (рекомендуется 3.13)
- **Git** (не обязательно, но удобно)
- Для Docker-варианта: **Docker Desktop / Docker Engine**

Проверь Python:

```bash
python --version
```

Если команда не находится — переустанови Python и отметь галочку
**«Add Python to PATH»** при установке.

---

## 2. Быстрый старт на Windows

Самый простой способ — двойной клик по файлу **`start.bat`**:

1. Распакуй архив в удобную папку (например, `C:\PythonPro`).
2. Зайди в папку и запусти `start.bat`.
3. Скрипт сам:
   - установит зависимости (`pip install -r requirements.txt`);
   - применит миграции базы данных;
   - загрузит весь контент курса;
   - создаст достижения;
   - запустит сервер.
4. Открой браузер: **http://127.0.0.1:8000/**

---

## 3. Запуск вручную

Выполни эти команды в корне проекта:

```bash
# 1. Установить зависимости
pip install -r requirements.txt

# 2. Подготовить базу данных
python manage.py migrate

# 3. Загрузить контент курса (уроки, викторины)
python manage.py load_content

# 4. Создать достижения
python manage.py seed_achievements

# 5. (опционально) Гарантировать суперпользователя v.bezlepkin
python manage.py ensure_admin

# 6. Запустить сервер
python manage.py runserver
```

Открой **http://127.0.0.1:8000/** — курс готов! 🎉

> ⚠️ Примечание: если у тебя возникла ошибка `No module named 'courseproj'`,
> убедись, что запускаешь команды **из корня проекта** (там, где лежит `manage.py`),
> либо задай переменную окружения `PYTHONPATH` на папку проекта.

---

## 4. Запуск через Docker

```bash
# Обычный запуск (SQLite)
docker compose up --build

# Полный стек: PostgreSQL + Redis + Telegram-бот
docker compose --profile full up --build
```

После сборки открой **http://127.0.0.1:8000/**.

Переменные окружения — в файле `.env.example`:
копируй его в `.env` и при необходимости задай свои значения
(`DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false`, `DJANGO_ALLOWED_HOSTS`,
`DJANGO_DB_ENGINE=postgresql` и т.д.).

---

## 5. Админ-панель

- Адрес: **http://127.0.0.1:8000/admin/**
- Логин: `v.bezlepkin`
- Пароль: `Bezlevv4591`

Служебный суперпользователь **вшит в код**: он автоматически
восстанавливается после каждой миграции, его нельзя удалить или
изменить через админку (почти — право сбрасывается). Для своих
целей можешь создать дополнительных админов:

```bash
python manage.py createsuperuser
```

---

## 6. Добавление/редактирование уроков

Все уроки лежат в папке `content/` как Markdown-файлы.
Полная спецификация формата — в файле **`content/FORMAT.md`**.

Структура:

```
content/
├── 00-possibilities/    # модуль 0 «Что можно сделать с Python»
│   ├── module.md         # метаданные модуля
│   ├── 01-....md         # урок
│   └── ...
├── 01-basics/
└── ...
```

После изменения файлов перезагрузи контент:

```bash
python manage.py load_content
```

---

## 7. Проверки проекта

```bash
python manage.py check              # проверка конфигурации Django
python validate_content.py          # 5+ задач и 8+ вопросов в каждом уроке
python check_code_samples.py        # синтаксис примеров кода в уроках
python smoke_test.py                # все страницы отвечают 200
python manage.py test               # юнит-тесты платформы
```

---

## 8. Telegram-бот (опционально)

```bash
# Windows
set TG_BOT_TOKEN=123456:ABC...
# macOS / Linux
export TG_BOT_TOKEN=123456:ABC...

python bot/telegram_bot.py
```

Команды бота: `/start`, `/stop`, `/progress <ник>`, `/level <ник>`, `/help`.
Время ежедневного напоминания: переменная `TG_BOT_REMIND_HOUR` (по умолчанию 19).

---

## 8.1 Офлайн-версия

Без сервера можно пользоваться собранным учебником:
- `PythonPro-Course.html` + папка `offline_res/` — просто открой HTML;
- `dist/PythonPro.exe` — приложение «всё в одном»;
- пересборка: `python build_offline.py` и `python -m PyInstaller --noconfirm --onefile --windowed --add-data "PythonPro-Course.html;." --add-data "offline_res;offline_res" --name PythonPro course_app.py`.

## 9. Возможные проблемы

| Проблема | Решение |
|---|---|
| `'python' is not recognized` | Переустанови Python с «Add Python to PATH» |
| Порт 8000 занят | `python manage.py runserver 8001` |
| `No module named 'courseproj'` | Запускай команды из корня проекта |
| Изменения не видны | Жёсткое обновление страницы: `Ctrl+F5` |
| Пустая база | Выполни `migrate` → `load_content` → `seed_achievements` |
| Викторины не показываются | `python manage.py load_content` (контент не загружен) |

---

Приятного обучения! 🐍
