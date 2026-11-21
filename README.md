# 🐍 PythonПро — платформа-курс по Python с нуля до Senior

Полноценное веб-приложение-курс: подробная теория, живые примеры, задачи с подсказками и разборами. Десять модулей — от объявления переменных до конкурентности, деплоя, нейросетей и собственных проектов.

## Возможности

- **103 урока** в 11 модулях: основы → продвинутый Python → стандартная библиотека → анализ данных → веб → нейросети → проекты → конкурентность → инструменты Senior → деплой → алгоритмы.
- **Минимум 5 задач на урок** — ручное написание кода (плюс 5+ вопросов викторины).
- **Теория + практика**: каждая задача имеет скрытую подсказку и полный разбор.
- **⚡ Песочница кода** прямо на странице урока: запуск Python на сервере с ограничениями (тайм-аут, запрет системных импортов). Проверка по «Ожидаемому выводу» или по **тест-кейсам** (ввод через stdin → ожидаемый вывод) — сравнивается результат, а не код: любое решение, дающее верный вывод, засчитывается.
- **📋 Экзамены по каждому модулю** (10 шт.): 10 вопросов, порог сдачи 80%.
- **✅ Викторины** с автопроверкой и объяснениями.
- **🏅 Достижения и серии** (как в Duolingo): 12 бейджей, стрик дней, «решил/прочитал» — раздельные отметки.
- **🎚️ Уровни и лидерборд**: XP (решения + достижения), 7 уровней от Новичка до Senior, публичная таблица лидеров.
- **💬 Комментарии** под уроками и **📝 личные заметки** с автосохранением.
- **📖 Справочник**: шпаргалки по синтаксису, частые ошибки, команды терминала, глоссарий.
- **🏆 Сертификат** об окончании курса (печать / сохранение в PDF).
- **🎨 Три темы**: тёмная, светлая, AMOLED.
- **🤖 Telegram-бот** (опционально): ежедневные напоминания, прогресс и уровень по никнейму.
- **Поиск** с фильтрами по сложности и тегам.
- **⬇ Скачивание примеров кода** (.py) и **экспорт прогресса** в CSV.
- **Тёмная/светлая тема**, адаптив, кнопка «Копировать» у кода, админ-панель.
- **Контент в Markdown**: файлы в `content/` — легко дополнять курс.
- **Готов к продакшену**: Docker, docker-compose (опционально PostgreSQL + Redis), Gunicorn, whitenoise, GitHub Actions CI, переменные окружения.

## Технологии

- Backend: **Django 5** + SQLite (+ Gunicorn/whitenoise для продакшена)
- Рендер уроков: **Markdown** (python-markdown)
- Фронтенд: чистый HTML/CSS/JS (без внешних CDN)
- Внутри курса изучаются: Flask, FastAPI, Django, Jinja2, Streamlit, pandas, NumPy, Matplotlib, scikit-learn, PyTorch, BeautifulSoup, SQLAlchemy, Docker, GitHub Actions, pytest, Git, **uv** и др.

## Быстрый старт

Требуется Python 3.10+.

```bash
git clone https://github.com/Bezlevv/python-pro-course.git
cd python-pro-course

pip install -r requirements.txt
python manage.py migrate
python manage.py load_content
python manage.py seed_achievements
python manage.py runserver
```

На Windows можно просто запустить `start.bat` — он сделает всё за вас.

Открой **http://127.0.0.1:8000/** — курс готов! 🎉

### Админка

```bash
python manage.py createsuperuser
```

Затем зайди на **http://127.0.0.1:8000/admin/**.

## Продакшен (Docker)

```bash
docker compose up --build
# полный стек (PostgreSQL + Redis):
# docker compose --profile full up --build
# или вручную: docker build -t pythonpro . && docker run -p 8000:8000 pythonpro
```

Переменные окружения — см. `.env.example` (DJANGO_SECRET_KEY, DJANGO_DEBUG, DJANGO_ALLOWED_HOSTS, DJANGO_DB_ENGINE / DJANGO_REDIS_URL). CI-пайплайн (тесты, валидация контента, смоук-тест) — в `.github/workflows/ci.yml`.

### Telegram-бот

```bash
set TG_BOT_TOKEN=123456:ABC...   # Windows
python bot/telegram_bot.py
```

Команды: `/start`, `/progress <ник>`, `/level <ник>`, `/stop`. По умолчанию шлёт напоминание ежедневно в 19:00 (`TG_BOT_REMIND_HOUR`).

## Как добавить урок

1. Создай файл `content/<модуль>/<номер>-<слаг>.md`.
2. Заполни front-matter (`title`, `summary`, `order`, `duration`, `difficulty`, `tags`).
3. Напиши теорию в Markdown, затем **минимум 5 задач** и `### Задача N`, подсказки `### Подсказка N` и разборы `### Разбор N` в блоках `<!--TASK-->`, `<!--HINT-->`, `<!--SOLUTION-->`, и **минимум 5 вопросов** викторины в `<!--QUIZ-->`.
4. Выполни `python manage.py load_content`.

Полная спецификация — в [`content/FORMAT.md`](content/FORMAT.md).

## Проверки

```bash
python manage.py check          # проверка проекта Django
python validate_content.py      # 5+ задач и 5+ вопросов на каждый урок
python smoke_test.py            # все страницы отвечают 200
python manage.py test           # юнит-тесты (22)
```

## Структура проекта

```
├── manage.py
├── smoke_test.py / validate_content.py
├── courseproj/            # настройки проекта
├── learn/                 # модели, вьюхи, загрузчик контента, песочница
├── content/               # уроки курса (Markdown)
├── templates/ static/     # шаблоны и стили
├── Dockerfile / docker-compose.yml
├── .github/workflows/ci.yml
└── requirements.txt
```

## Офлайн-версия (HTML / EXE)

Курс можно использовать без сервера и интернета:

- `python build_offline.py` → собирает **PythonPro-Course.html** (один файл + папка `offline_res/` с CodeMirror и Pyodide).
- `dist/PythonPro.exe` — самодостаточное приложение (собранное через PyInstaller): курс и все ресурсы внутри.

Возможности офлайн-версии:
- все 39 модулей, 340+ уроков; дерево + поиск;
- Python-песочница (Pyodide, браузерный CPython);
- редактор кода с подсветкой и автодополнением (CodeMirror);
- викторины с проверкой ответов;
- прогресс изучения и закладки (localStorage);
- личные заметки к урокам и экспорт прогресса (JSON);
- копирование примеров кода одной кнопкой;
- тёмная/светлая тема; навигация «предыдущий/следующий».

## Лицензия

Проект создан для обучения. Используйте свободно.
