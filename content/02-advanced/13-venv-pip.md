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
### Задача 1
Создай для нового проекта `my_project` виртуальное окружение, активируй его, установи пакет `requests`, убедись, что он установлен (команда `pip show requests` покажет версию), затем создай файл `requirements.txt` командой `pip freeze > requirements.txt` и выведи его содержимое. Ожидаемый результат: в терминале виден промпт `(.venv)`, `pip list` показывает `requests` с версией, а в файле `requirements.txt` есть строка `requests==...`.

### Задача 2
В окружении проекта `my_project` (из предыдущей задачи или созданном заново) установи конкретную версию пакета: `pip install requests==2.31.0`. Затем выполни `pip show requests` и убедись, что версия равна 2.31.0. Выведи её через команду `pip show requests | findstr Version` (Windows) или `pip show requests | grep Version` (macOS/Linux). Ожидаемый результат: в выводе команды строка `Version: 2.31.0`.

### Задача 3
Создай два разных проекта `proj_a` и `proj_b`, в каждом — своё виртуальное окружение. В `proj_a` установи `requests==2.31.0`, в `proj_b` — `requests==2.32.3`. В каждом окружении выполни `pip show requests` и сравни версии. Ожидаемый результат: в `proj_a` версия 2.31.0, в `proj_b` — 2.32.3, при этом они не влияют друг на друга (изоляция).

### Задача 4
Создай файл `requirements.txt` со строками:

```
requests==2.32.3
certifi>=2024.0.0
```

Затем создай новое окружение `fresh_env`, активируй его и установи зависимости командой `pip install -r requirements.txt`. Проверь через `pip freeze`, что `requests` установлен версии 2.32.3. Ожидаемый результат: установка прошла без ошибок, а `pip freeze` содержит `requests==2.32.3`.

### Задача 5
В окружении из задачи 1 (или новом) выполни полную очистку: деактивируй окружение (`deactivate`), удали папку `.venv` (команда `rmdir /s /q .venv` на Windows или `rm -rf .venv` на macOS/Linux), затем убедись, что папки больше нет (команда `dir` на Windows или `ls -la` на macOS/Linux). Ожидаемый результат: промпт без `(.venv)`, папка `.venv` отсутствует, команды `python` и `pip` снова указывают на системный Python.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Сначала `cd my_project`, затем `python -m venv .venv`. Активация на Windows: `.venv\Scripts\activate`, на macOS/Linux: `source .venv/bin/activate`. Проверить содержимое файла можно командой `type requirements.txt` (Windows) или `cat requirements.txt`.

### Подсказка 2
Точная версия ставится так: `pip install requests==2.31.0`. Если она уже установлена с другой версией, pip сам переустановит нужную. Запомни: знак `|` в командах Windows называется «pipe» и работает в PowerShell так же, как в Linux.

### Подсказка 3
Создавай окружения отдельно: `python -m venv .venv` внутри каждой папки. Активация в каждом терминале — своя. Внимательно следи, в каком окружении ты находишься: промпт `(.venv)` подскажет. Если версии в `pip show` совпадают — проверь, не забыл ли активировать второе окружение.

### Подсказка 4
Помни: `pip install -r requirements.txt` читает файл и ставит все перечисленные пакеты. Если файл лежит не в текущей папке, укажи путь. `pip freeze` покажет все установленные версии — ищи в выводе `requests==2.32.3`.

### Подсказка 5
После `deactivate` команда `python` снова укажет на системный интерпретатор — проверь это через `where python` (Windows) или `which python`. Удалять папку `.venv` можно из любой папки проекта, но сначала выйди из окружения: иначе папка будет занята.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
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

На другой машине окружение восстанавливается так: `python -m venv .venv`, активация, затем `pip install -r requirements.txt`. Проект готов к работе в той же конфигурации.

### Разбор 2
Команды:

```bash
cd my_project
.venv\Scripts\activate        # Windows
# source .venv/bin/activate    # macOS/Linux

pip install requests==2.31.0
pip show requests | findstr Version    # Windows
# pip show requests | grep Version     # macOS/Linux
```

Здесь `pip install requests==2.31.0` устанавливает не последнюю, а именно указанную версию. Если в окружении уже стояла другая, pip переустановит 2.31.0. `pip show requests` выводит блок метаданных пакета, среди которых строка `Version: 2.31.0`. Конвейер `| findstr Version` (или `grep Version`) оставляет только эту строку — так удобнее читать результат в длинных выводах. Ожидаемый вывод:

```
Version: 2.31.0
```

Фиксация версий важна для воспроизводимости: сборка на другой машине должна использовать ту же версию, иначе поведение программы может отличаться.

### Разбор 3
Команды (для Windows; на macOS/Linux заменяй активацию на `source .venv/bin/activate`):

```bash
mkdir proj_a proj_b
cd proj_a
python -m venv .venv
.venv\Scripts\activate
pip install requests==2.31.0
pip show requests | findstr Version

cd ..\proj_b
python -m venv .venv
.venv\Scripts\activate
pip install requests==2.32.3
pip show requests | findstr Version
```

Два окружения — два независимых мира. Пакет `requests` в `proj_a` установлен версии 2.31.0, в `proj_b` — 2.32.3, и они не пересекаются: у каждого своя папка `site-packages` внутри `.venv`. Системный Python вообще не затрагивается. Ожидаемые выводы:

```
Version: 2.31.0
```

и

```
Version: 2.32.3
```

Именно эта изоляция позволяет держать рядом проекты с конфликтующими зависимостями — например, старый на Django 4 и новый на Django 5.

### Разбор 4
Команды:

```bash
mkdir fresh_env
cd fresh_env
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate    # macOS/Linux

# создаём файл, например через блокнот или echo
echo requests==2.32.3> requirements.txt
echo certifi>=2024.0.0>> requirements.txt

pip install -r requirements.txt
pip freeze
```

`pip install -r requirements.txt` читает файл и устанавливает каждую перечисленную зависимость. Ограничение `certifi>=2024.0.0` означает «не ниже указанной версии». В `pip freeze` мы увидим точно установленные версии, включая `requests==2.32.3`:

```
certifi==2024.8.30
charset-normalizer==3.3.2
idna==3.8
requests==2.32.3
urllib3==2.2.3
```

Файл `requirements.txt` — это «рецепт» окружения: он позволяет воспроизвести его на любой машине одной командой, поэтому его хранят в системе контроля версий вместе с кодом.

### Разбор 5
Команды:

```bash
deactivate
# Windows:
rmdir /s /q .venv
dir
# macOS/Linux:
# rm -rf .venv
# ls -la
```

`deactivate` выводит из окружения: промпт теряет префикс `(.venv)`, а `python` и `pip` снова указывают на системный интерпретатор. Папка `.venv` — это обычная папка, поэтому её можно удалить: `rmdir /s /q .venv` (Windows) или `rm -rf .venv` (macOS/Linux). После этого `dir` (или `ls -la`) не показывает `.venv` — окружение полностью исчезло, а проектные файлы остались нетронутыми.

Ожидаемый результат:

```
Папка .venv отсутствует; промпт без (.venv).
```

Поскольку всё окружение живёт внутри одной папки, «пересоздать» его проще, чем чинить: удалил `.venv` — и создай новое. Это ещё одно преимущество venv.
<!--/SOLUTION-->

<!--QUIZ-->
Что создаёт команда python -m venv .venv?
- файл с зависимостями
- виртуальное окружение в папке .venv
- устанавливает все пакеты из интернета
- новую версию Python
* Правильный ответ: виртуальное окружение в папке .venv
В папке .venv оказывается собственная копия интерпретатора и pip.

Зачем нужны виртуальные окружения?
- чтобы ускорить Python
- чтобы изолировать зависимости разных проектов друг от друга
- чтобы обойти лицензии пакетов
- чтобы уменьшить размер проекта
* Правильный ответ: чтобы изолировать зависимости разных проектов друг от друга
У каждого проекта свои версии пакетов, и они не конфликтуют.

Что выводит pip freeze?
- список всех пакетов в интернете
- список установленных пакетов с точными версиями
- только те пакеты, которые требуют обновления
- версию pip
* Правильный ответ: список установленных пакетов с точными версиями
Вывод вида requests==2.32.3 сохраняют в requirements.txt.

Как установить все пакеты из файла requirements.txt?
- pip install requirements.txt
- pip install -r requirements.txt
- pip freeze -r requirements.txt
- pip download -r requirements.txt
* Правильный ответ: pip install -r requirements.txt
Флаг -r говорит pip читать список из файла.

Что появится в начале приглашения терминала после активации окружения?
- (venv)
- (python)
- (pip)
- ничего не изменится
* Правильный ответ: (venv)
Префикс (.venv) — признак активного окружения.

Как выйти из виртуального окружения?
- python -m venv --exit
- deactivate
- exit venv
- pip uninstall venv
* Правильный ответ: deactivate
Команда deactivate возвращает системный Python и pip.
<!--/QUIZ-->
