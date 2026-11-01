---
title: venv, pip, requirements.txt
summary: Изолированное окружение для каждого проекта: создание, активация, установка пакетов и фиксация зависимостей.
order: 13
duration: 20 мин
difficulty: intermediate
---

Если ставить все пакеты прямо в системный Python, версии разных проектов начнут конфликтовать: один потребует Django 4, другой — Django 5. Виртуальное окружение (venv) — это изолированная копия Python для конкретного проекта.

## Зачем это нужно

- **Изоляция версий.** У каждого проекта свои пакеты, они не мешают друг другу.
- **Чистота системы.** В системный Python попадает только то, что действительно нужно всем.
- **Воспроизводимость.** Файл `requirements.txt` позволяет воссоздать окружение на другой машине.

## Создание окружения

Выполни в папке проекта:

```bash
python -m venv .venv
```

Появляется папка `.venv` со своим интерпретатором и утилитами. Пока окружение не активировано, ты пользуешься системным Python.

## Активация

Windows (PowerShell):

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

После активации в начале приглашения терминала появится `(.venv)`.

## Проверяем

```bash
python --version
which python   # macOS/Linux
where python   # Windows
```

Путь должен указывать внутрь `.venv`.

## pip

`pip` — менеджер пакетов. Основные команды:

```bash
pip install requests
pip list
pip show requests
```

Установленные пакеты попадают только в текущее окружение.

## requirements.txt

Чтобы воспроизвести окружение на другой машине, зафиксируй зависимости:

```bash
pip freeze > requirements.txt
```

Файл содержит строки вида `requests==2.32.3`. Восстановление окружения на новой машине:

```bash
pip install -r requirements.txt
```

## Что происходит «под капотом»

Когда ты устанавливаешь пакет внутри окружения, он попадает в папку `.venv/Lib/site-packages` (на Windows) или `.venv/lib/pythonX.Y/site-packages` (на macOS/Linux). Системный Python при этом не трогается. Именно поэтому одно и то же имя пакета может иметь разные версии в разных проектах: каждое окружение хранит свою копию. Если чувствуешь, что окружение «сломалось» — проще создать новое, чем чинить старое.

## Деактивация

```bash
deactivate
```

Окружение можно удалить, просто стерев папку `.venv`.

## Итог урока

Мы узнали:

- зачем нужны виртуальные окружения;
- `python -m venv .venv` и активацию;
- основные команды pip;
- `pip freeze > requirements.txt` и установку из файла;
- `deactivate`.

Закрепим практикой.

<!--TASK-->
**Задача.** Создай для нового проекта `my_project` виртуальное окружение, активируй его, установи пакет `requests`, убедись, что он установлен (команда `pip show requests` покажет версию), затем создай файл `requirements.txt` командой `pip freeze > requirements.txt` и выведи его содержимое. Ожидаемый результат: в терминале виден промпт `(.venv)`, `pip list` показывает `requests` с версией, а в файле `requirements.txt` есть строка `requests==...`.
<!--/TASK-->

<!--HINT-->
Сначала `cd my_project`, затем `python -m venv .venv`. Активация на Windows: `.venv\Scripts\activate`, на macOS/Linux: `source .venv/bin/activate`. Проверить содержимое файла можно командой `type requirements.txt` (Windows) или `cat requirements.txt`.
<!--/HINT-->

<!--SOLUTION-->
Полная последовательность команд (для Windows; на macOS/Linux отличаются только активация и просмотр файла):

```bash
mkdir my_project
cd my_project
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install requests
pip show requests
pip freeze > requirements.txt
# Windows:
type requirements.txt
# macOS/Linux:
# cat requirements.txt
```

Разбор шагов. `python -m venv .venv` создаёт папку `.venv` — собственную копию интерпретатора. Без активации `pip install` ставил бы пакеты в системный Python; после активации команды `python` и `pip` берутся из `.venv`. `pip install requests` скачивает пакет в окружение, `pip show requests` показывает метаданные, включая версию. `pip freeze` перечисляет все установленные пакеты с версиями, а `> requirements.txt` сохраняет вывод в файл — так мы фиксируем зависимости.

Ожидаемый вид `requirements.txt` (порядок строк может отличаться):

```
requests==2.32.3
urllib3==2.2.3
certifi==2024.8.30
charset-normalizer==3.3.2
idna==3.8
```

На другой машине окружение восстанавливается так: `python -m venv .venv`, активация, затем `pip install -r requirements.txt`. Проект готов к работе в той же конфигурации. Когда проект не нужен — просто `deactivate` и удали папку `.venv`.
<!--/SOLUTION-->
