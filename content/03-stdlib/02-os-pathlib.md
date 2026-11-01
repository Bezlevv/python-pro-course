---
title: os, pathlib, shutil
summary: Работа с файлами и папками: современные классы Path, системные функции os и копирование с shutil.
order: 2
duration: 35 мин
difficulty: intermediate
---

Почти любая настоящая программа работает с файлами: читает настройки, сохраняет результаты, сортирует скачанные файлы. В стандартной библиотеке за это отвечают три родственных модуля: `pathlib` (современный, объектный подход к путям), `os` (низкоуровневые системные операции) и `shutil` (копирование и перемещение). В этом уроке разберёмся, когда что использовать.

## pathlib: пути как объекты

Модуль `pathlib` появился в Python 3.4 и стал стандартом де-факто: вместо строк с путями ты работаешь с объектами `Path`. Это удобно: можно не думать о том, Windows у пользователя или Linux — разделители подставит сам Python.

Основные операции:

```python
from pathlib import Path

current = Path.cwd()        # текущая папка
home = Path.home()          # домашняя папка
print(current)
print(home)
```

Пути объединяются через `/`, а не через конкатенацию строк:

```python
data_dir = Path("data")
data_dir.mkdir(parents=True, exist_ok=True)  # создать папку

file_path = data_dir / "notes.txt"           # data/notes.txt
file_path.write_text("Первая заметка\n", encoding="utf-8")
print(file_path.read_text(encoding="utf-8")) # Первая заметка
```

У объекта `Path` есть полезные свойства: `name` (имя файла), `stem` (имя без расширения), `suffix` (расширение), `parent` (родительская папка):

```python
p = Path("reports/2024/summary.txt")
print(p.name)     # summary.txt
print(p.stem)     # summary
print(p.suffix)   # .txt
print(p.parent)   # reports/2024
```

Проверки и поиск файлов:

```python
p = Path("data/notes.txt")
print(p.exists())                       # True
print(p.is_file(), p.is_dir())          # True False

for path in Path("data").iterdir():     # все элементы папки
    print(path.name)

for md in Path(".").rglob("*.md"):      # рекурсивный поиск
    print(md)
```

## os: системный уровень

Модуль `os` — «старый» способ работать с файловой системой и окружением. Он всё ещё нужен для системных вещей: переменные окружения, `os.walk` для рекурсивного обхода, низкоуровневые операции.

```python
import os

print(os.getcwd())                 # текущая папка
print(os.listdir("."))             # список имён в папке
print(os.environ.get("USER", "unknown"))  # переменная окружения

os.makedirs("tmp/a/b", exist_ok=True)  # создать вложенные папки

for root, dirs, files in os.walk("content"):
    print(root, len(files))        # обход всего дерева
```

Общее правило: для путей и файлов предпочитай `pathlib`, а `os` используй там, где нужны переменные окружения или тонкий контроль над системой.

## shutil: копирование и перемещение

Модуль `shutil` копирует, перемещает и удаляет файлы и папки целиком:

```python
import shutil

shutil.copy2("data/notes.txt", "data/notes_copy.txt")  # копия с метаданными
shutil.move("data/notes_copy.txt", "data/backup.txt")   # переместить/переименовать
print(shutil.disk_usage("."))   # свободное место на диске

# shutil.rmtree("tmp")          # удалить папку целиком (осторожно!)
```

`rmtree` и `copytree` — опасные операции: не запускай их на важных данных без проверки.

## Итог урока

Мы разобрали три модуля: `pathlib` для удобной работы с путями (`Path`, `/`, `glob`, `suffix`), `os` для системного уровня (`getcwd`, `environ`, `walk`) и `shutil` для копирования и перемещения. Теперь соберём из них полезный скрипт.

<!--TASK-->
**Задача.** Напиши скрипт `organize.py`, который приводит в порядок «захламлённую» папку:

1. Рядом со скриптом создай папку `downloads` и положи в неё несколько файлов разных типов: `photo.png`, `wallpaper.jpg`, `readme.txt`, `book.pdf`, `song.mp3` (содержимое не важно — файлы могут быть пустыми);
2. Скрипт создаёт в `downloads` подпапки `images`, `docs`, `audio`;
3. Перемещает каждый файл по расширению: `.png`/`.jpg`/`.jpeg` → `images`, `.txt`/`.pdf`/`.docx` → `docs`, `.mp3`/`.wav` → `audio`;
4. Выводит отчёт: `Куда перемещён файл X -> папка Y`.

Ожидаемый результат: в `downloads` появились три подпапки, каждый файл лежит в своей, а на экране — отчёт о перемещении каждого файла.
<!--/TASK-->

<!--HINT-->
Обойди файлы через `Path("downloads").iterdir()` и отсеивай подпапки через `path.is_file()`. Сопоставь `path.suffix.lower()` с нужной категорией через словарь. Перед перемещением создай целевую папку: `mkdir(parents=True, exist_ok=True)`. Перемещай через `shutil.move(path, target_dir / path.name)`.
<!--/HINT-->

<!--SOLUTION-->
Одно из возможных решений:

```python
import shutil
from pathlib import Path

BASE = Path("downloads")

CATEGORIES = {
    ".png": "images", ".jpg": "images", ".jpeg": "images",
    ".txt": "docs", ".pdf": "docs", ".docx": "docs",
    ".mp3": "audio", ".wav": "audio",
}

for item in BASE.iterdir():
    if not item.is_file():
        continue
    folder_name = CATEGORIES.get(item.suffix.lower())
    if folder_name is None:
        print(f"Пропускаем {item.name}: неизвестное расширение")
        continue
    target_dir = BASE / folder_name
    target_dir.mkdir(parents=True, exist_ok=True)
    destination = shutil.move(item, target_dir / item.name)
    print(f"Куда перемещён файл {item.name} -> {destination}")
```

Результат:

```
Куда перемещён файл photo.png -> downloads\images\photo.png
Куда перемещён файл wallpaper.jpg -> downloads\images\wallpaper.jpg
Куда перемещён файл readme.txt -> downloads\docs\readme.txt
Куда перемещён файл book.pdf -> downloads\docs\book.pdf
Куда перемещён файл song.mp3 -> downloads\audio\song.mp3
```

Разбор шагов. `BASE.iterdir()` возвращает все элементы папки по одному; `is_file()` отсеивает подпапки, чтобы не пытаться перемещать их самих. Словарь `CATEGORIES` связывает расширение (в нижнем регистре — на случай `JPG`) с именем категории, а `get` со значением по умолчанию `None` безопасно обрабатывает незнакомые расширения. Перед перемещением мы создаём целевую подпапку: `mkdir(..., exist_ok=True)` не падает, если она уже существует. Наконец, `shutil.move` переносит файл и возвращает путь назначения — его мы и печатаем. Обрати внимание: объекты `Path` можно свободно передавать в `shutil.move` — библиотека сама преобразует их в строки.
<!--/SOLUTION-->
