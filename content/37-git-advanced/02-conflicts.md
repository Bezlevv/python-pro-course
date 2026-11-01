---
title: Решение конфликтов
summary: Почему возникают конфликты, как читать маркеры <<<<<<<, =======, >>>>>>>, как разрешать их вручную, командами и автоматически через rerere.
order: 2
duration: 40 мин
difficulty: advanced
tags: git, конфликты, merge, rebase, rerere, mergetool
---

Конфликт — это не ошибка Git, а нормальное событие: две ветки изменили **одно и то же место** одного и того же файла, и Git не может сам решить, какой вариант правильный. Он честно останавливается и просит тебя выбрать. Умение быстро и спокойно разрешать конфликты — главный практический навык любого разработчика, работающего в команде.

## Как выглядит конфликт

Сценарий: на `main` и на `feature` оба изменили строку `VERSION` в `app.py`. При `git merge feature` или `git rebase main` Git сообщит:

```bash
CONFLICT (content): Merge conflict in app.py
Automatic merge failed; fix conflicts and then commit the result.
```

А в самом файле появятся маркеры:

```
<<<<<<< HEAD
VERSION = "1.1"
=======
VERSION = "1.2"
>>>>>>> feature
```

- `<<<<<<< HEAD` — начало конфликтующего блока, далее идёт **твоя** версия (в rebase `HEAD` — это ветка, которую перебазируют, то есть наша фича);
- `=======` — разделитель версий;
- `>>>>>>> feature` — конец блока, после него — версия из другой ветки.

Задача: оставить нужный вариант (или объединить оба), **удалить все три маркера** и сохранить файл.

## Как определить масштаб

Сначала смотрим, какие файлы затронуты:

```bash
git status          # раздел Unmerged paths
git diff            # изменения относительно индекса
```

`git status` пометит конфликтующие файлы статусом `UU` (both modified). Дальше открываем каждый файл и ищем маркеры. Если конфликтов много, удобно искать их вручную или через `git grep`:

```bash
git grep -n '^<<<<<<<'
```

## Способы разрешения

**1. Вручную.** Открываешь файл в редакторе, оставляешь нужное, убираешь маркеры, затем:

```bash
git add app.py
git commit          # для merge — завершает слияние
# или для rebase:
git rebase --continue
```

**2. Выбрать одну из версий целиком.** Уже зная, какая версия нужна, можно не редактировать файл:

```bash
git checkout --ours app.py     # взять нашу версию
git checkout --theirs app.py   # взять их версию
```

Внимание: при `merge` и `rebase` смысл `ours`/`theirs` **противоположный**:

| Операция | --ours | --theirs |
|---|---|---|
| git merge | ветка, где ты находишься (текущая) | вливаемя ветка |
| git rebase | ветка, которую перебазируют (результат) | база (main/upstream) |

Путаница здесь — источник половины испорченных решений. Правило: «ours — это та ветка, в которую сейчас вливаются изменения, то есть текущая; theirs — та, изменения которой вливаются».

**3. Визуальный инструмент.** `git mergetool` открывает настроенный инструмент (например, `meld`, `kdiff3`, `vimdiff`). Настройка:

```bash
git config merge.tool vimdiff
git mergetool
```

После использования инструмента не забудь `git add` и довести операцию до конца.

**4. Автозапоминание с rerere.** Rerere («reuse recorded resolution») запоминает, как ты разрешил конфликт, и при следующем возникновении **точно такого же** конфликта применяет решение автоматически. Включается глобально:

```bash
git config --global rerere.enabled true
```

Во время конфликта Git пишет `Recorded preimage for 'app.py'` — значит, решение запомнено. Полезно при частом rebase одной и той же ветки, где конфликты повторяются.

## Конфликты при rebase

При rebase конфликты обычно возникают на каждом коммите по отдельности: Git применяет коммиты по одному и после каждого может остановиться. Разрешил — `git rebase --continue`; хочешь попробовать снова с чистого листа — `git rebase --abort`; пропустить коммит — `git rebase --skip`. Важно: `git commit` при rebase **не** является завершением — только `--continue`.

## Как предотвращать конфликты

- Чаще синхронизируйся: `git pull --rebase` перед началом работы и перед PR.
- Делай маленькие коммиты и короткие фича-ветки — меньше вероятность задеть те же строки.
- Не смешивай в одном коммите переименование файла и правку его содержимого.
- Договаривайся о форматах файлов (порядок строк, стиль) — тогда «конфликты форматирования» не будут плодиться.

<!--TASK-->
### Задача 1
Создай временный репозиторий и воспроизведи конфликт вручную:

1. `git init`; настрой имя и почту.
2. Создай `config.py` со строкой `PORT = 8000`, закоммить.
3. Создай ветку `feature`; в ней поменяй на `PORT = 9000`, закоммить.
4. Вернись на `main`; поменяй на `PORT = 8080`, закоммить.
5. Выполни `git merge feature` — должен возникнуть конфликт.
6. Открой `config.py`, найди маркеры, оставь `PORT = 8080`, удали маркеры, выполни `git add config.py` и `git commit`.

Ожидаемый результат: `git status` показывает чистое дерево, в `config.py` нет ни одного маркера `<<<<<<<`, а `git log --oneline` содержит merge-коммит.

### Задача 2
Напиши pytest-тест `test_conflict_merge.py`, который проверяет «анатомию» конфликта:

1. Временный репозиторий: базовый коммит, ветка `feature` меняет строку, `main` меняет ту же строку.
2. `git merge feature` должен завершиться с ненулевым кодом возврата — проверь через `subprocess.run` без `check=True`.
3. Проверь, что в файле есть все три маркера `<<<<<<<`, `=======`, `>>>>>>>`.
4. Разреши конфликт: запиши в файл значение из `main`, удали маркеры, `git add`, `git commit`.
5. Проверь, что `git status` чистый и маркеров в файле больше нет.

Запусти `pytest test_conflict_merge.py -v`: ожидаемый результат — `1 passed`.

### Задача 3
Напиши pytest-тест `test_conflict_rebase_ours.py` про семантику `--ours`/`--theirs` при rebase:

1. Сценарий: `main` = `A`; ветка `feature` от `A` с коммитом `B` (меняет `VERSION = "1.1"`); затем на `main` коммит `D` (меняет ту же строку на `VERSION = "1.2"`).
2. `git rebase main` (на `feature`) — конфликт.
3. Выполни `git checkout --ours config.py`, затем `git add config.py`, `git rebase --continue`.
4. Проверь, что в итоговом `config.py` — `VERSION = "1.1"` (вариант ОС, ветки feature), а не `"1.2"`.

Запусти `pytest test_conflict_rebase_ours.py -v`: ожидаемый результат — `1 passed`.

### Задача 4
Разреши конфликт «как профи»: в репозитории из задачи 1 повтори шаги 1–5, но вместо ручного редактирования используй:

```bash
git checkout --theirs config.py
git add config.py
git commit
```

Затем проделай то же самое, но с `--ours`, и сравни содержимое файлов. В ответе запиши короткий вывод: какое значение оказалось в файле при `--ours` и какое при `--theirs` применительно к **merge** (не rebase). Ожидаемый результат: ты можешь объяснить, почему при merge `--ours` — это вариант текущей ветки (main), а `--theirs` — вариант вливаемой (feature).

### Задача 5
Включи rerere и убедись, что повторный конфликт разрешается сам:

1. `git config --global rerere.enabled true`.
2. Повтори сценарий задачи 1 (конфликт на `PORT`), разреши его **вручную** (оставь `PORT = 8080`), заверши merge.
3. Снова измени `PORT` в обеих ветках и попробуй merge ещё раз. Обрати внимание на сообщение `Resolved 'config.py' using previous resolution`.

Ожидаемый результат: при втором merge Git не останавливается или останавливается, но сразу применяет запомненное решение; в любом случае `config.py` содержит `PORT = 8080` без ручного вмешательства. Убедись, что `git config rerere.enabled` возвращает `true`.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Маркеры идут строго в порядке: `<<<<<<< HEAD`, затем `=======`, затем `>>>>>>> feature`. Оставь одну строку между маркерами и удали все три строки-маркера целиком, включая `<<<<<<<`, `=======` и `>>>>>>>`. После `git add` и `git commit` проверь `git grep -n '^<<<<<<<'` — вывод должен быть пустым.

### Подсказка 2
Без `check=True` `subprocess.run` вернёт объект с полем `returncode` — для конфликтующего merge он будет `1`. Маркеры проверяй чтением файла: `"<<<<<<< HEAD" in content`. Чтобы смоделировать «обе ветки меняют одну строку», пиши разные значения в одну и ту же строку файла в каждом коммите.

### Подсказка 3
При rebase `--ours` — это ветка, которую перебазируют (feature), `--theirs` — база (main). Значит, чтобы оставить вариант фичи, нужен именно `--ours`. После `git checkout --ours config.py` обязательно `git add config.py` и `git rebase --continue`, иначе Git не поймёт, что конфликт разрешён.

### Подсказка 4
Прочитай таблицу в теории: при `merge` `--ours` — текущая ветка (main), `--theirs` — вливаемя (feature). Не путай с rebase — там роли меняются. Выполни оба варианта в **разных** клонах или отмени первый merge через `git merge --abort` перед вторым опытом.

### Подсказка 5
После первого manual разрешения rerere сохранит «образ» конфликта и решение. Для второго эксперимента обязательно сделай конфликт **точно таким же** (те же строки, те же значения). Если второе слияние завершилось без остановки — значит, rerere сработал. Проверка настройки: `git config rerere.enabled`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Команды:

```bash
git init
git config user.name "Тест"
git config user.email "test@example.com"

echo 'PORT = 8000' > config.py
git add config.py && git commit -m "base: конфиг"

git checkout -b feature
sed -i 's/PORT = 8000/PORT = 9000/' config.py
git add config.py && git commit -m "feat: сменить порт"

git checkout main
sed -i 's/PORT = 8000/PORT = 8080/' config.py
git add config.py && git commit -m "fix: порт"

git merge feature
```

Git сообщит о конфликте. Открываем `config.py`:

```
<<<<<<< HEAD
PORT = 8080
=======
PORT = 9000
>>>>>>> feature
```

Оставляем `PORT = 8080` (вариант main), удаляем три строки-маркера:

```bash
git add config.py
git commit -m "merge: разрешить конфликт порта"
```

Почему это работает: Git не умеет сам решить, чей порт верный, — оба изменения лежат на одной строке. После редактирования файл снова «чистый», `git add` помечает конфликт разрешённым, а финальный `git commit` создаёт merge-коммит. Проверка: `git grep -n '^<<<<<<<'` ничего не печатает, `git status` показывает чистое рабочее дерево.

### Разбор 2
Решение:

```python
import subprocess
import tempfile
from pathlib import Path

import pytest


def git(*args, cwd, check=True):
    return subprocess.run(
        ["git", *args], cwd=cwd, check=check,
        capture_output=True, text=True,
    )


def commit_file(repo, name, content, message):
    (Path(repo) / name).write_text(content)
    git("add", name, cwd=repo)
    git("commit", "-m", message, cwd=repo)


def test_merge_conflict_anatomy():
    with tempfile.TemporaryDirectory() as repo:
        git("init", cwd=repo)
        git("config", "user.name", "Тест", cwd=repo)
        git("config", "user.email", "test@example.com", cwd=repo)

        commit_file(repo, "config.py", "PORT = 8000\n", "base")

        git("checkout", "-b", "feature", cwd=repo)
        commit_file(repo, "config.py", "PORT = 9000\n", "feat: порт")

        git("checkout", "main", cwd=repo)
        commit_file(repo, "config.py", "PORT = 8080\n", "fix: порт")

        result = git("merge", "feature", cwd=repo, check=False)
        assert result.returncode != 0

        content = (Path(repo) / "config.py").read_text()
        assert "<<<<<<< HEAD" in content
        assert "=======" in content
        assert ">>>>>>> feature" in content

        (Path(repo) / "config.py").write_text("PORT = 8080\n")
        git("add", "config.py", cwd=repo)
        git("commit", "-m", "merge: разрешить конфликт", cwd=repo)

        status = git("status", "--porcelain", cwd=repo).stdout
        assert status == ""
        content = (Path(repo) / "config.py").read_text()
        assert "<<<<<<<" not in content
```

Ключевое: `merge` вызывается с `check=False`, чтобы не падать на ненулевом коде — конфликт как раз и означает ненулевой `returncode`. Маркеры проверяются как обычный текст. Решение конфликта — запись одного из вариантов поверх всего файла, затем `add` и `commit`. Финальные проверки: `git status --porcelain` пустой (чистое дерево) и маркеров нет. Запуск: `pytest test_conflict_merge.py -v` → `1 passed`.

### Разбор 3
Решение:

```python
import subprocess
import tempfile
from pathlib import Path

import pytest


def git(*args, cwd, check=True):
    return subprocess.run(
        ["git", *args], cwd=cwd, check=check,
        capture_output=True, text=True,
    )


def commit_file(repo, name, content, message):
    (Path(repo) / name).write_text(content)
    git("add", name, cwd=repo)
    git("commit", "-m", message, cwd=repo)


def test_rebase_conflict_ours_is_feature():
    with tempfile.TemporaryDirectory() as repo:
        git("init", cwd=repo)
        git("config", "user.name", "Тест", cwd=repo)
        git("config", "user.email", "test@example.com", cwd=repo)

        commit_file(repo, "config.py", 'VERSION = "1.0"\n', "base")

        git("checkout", "-b", "feature", cwd=repo)
        commit_file(repo, "config.py", 'VERSION = "1.1"\n', "feat: 1.1")

        git("checkout", "main", cwd=repo)
        commit_file(repo, "config.py", 'VERSION = "1.2"\n', "feat: 1.2")

        git("checkout", "feature", cwd=repo)
        result = git("rebase", "main", cwd=repo, check=False)
        assert result.returncode != 0

        git("checkout", "--ours", "config.py", cwd=repo)
        git("add", "config.py", cwd=repo)
        git("rebase", "--continue", cwd=repo)

        content = (Path(repo) / "config.py").read_text()
        assert 'VERSION = "1.1"' in content
```

Разбор ключевого момента: при rebase Git накладывает коммиты `feature` поверх `main`. В момент конфликта `HEAD` — это «перебазируемая» ветка (`feature`, наш вариант), а `theirs` — база (`main`). Поэтому `--ours` оставляет `"1.1"` из фичи. Именно здесь путаются чаще всего: при merge было бы наоборот. Проверка утверждает `"1.1"` — это и доказывает, что тест понимает семантику. Запуск: `pytest test_conflict_rebase_ours.py -v` → `1 passed`.

### Разбор 4
Для merge верна таблица: `--ours` — текущая ветка (main), `--theirs` — вливаемя (feature). После `git checkout --theirs config.py` в файле будет `PORT = 9000` (из `feature`), после `git checkout --ours config.py` — `PORT = 8080` (из `main`). Итоговый комментарий: «при merge --ours берёт вариант текущей ветки (main), а --theirs — вариант вливаемой (feature); при rebase роли меняются: --ours — это перебазируемая ветка, --theirs — база». Эта асимметрия — следствие того, что у merge и rebase разные «текущие» ветки в интерпретации Git. Запомнив её, ты перестанешь ошибаться в выборе.

### Разбор 5
После включения `rerere.enabled` и ручного разрешения первого конфликта Git сохранил «образ» конфликта и решение. Повторный точно такой же конфликт Git узнаёт и применяет сохранённое решение, о чём пишет `Resolved 'config.py' using previous resolution`. Второй merge может вообще не остановиться — Git сразу подставит `PORT = 8080`. Это очень удобно при долгоживущих ветках, где одинаковые конфликты возникают при каждом rebase. Проверка: `git config rerere.enabled` → `true`. Оговорка: rerere запоминает решение по содержимому конфликтующих **хунков**, поэтому небольшие правки в соседних строках могут помешать «узнаванию» — это нормально.
<!--/SOLUTION-->

<!--QUIZ-->
Что означают маркеры <<<<<<< HEAD ... >>>>>>> feature в файле?
- Места, где Git не смог объединить варианты из двух веток
- Комментарии разработчиков
- Настройки форматирования
- Ошибки синтаксиса в коде
* Правильный ответ: Места, где Git не смог объединить варианты из двух веток
Git отмечает конфликтующие участки: сверху — твой вариант, снизу — вариант другой ветки.

Что нужно сделать с маркерами при разрешении конфликта?
- Оставить их в файле
- Удалить все три маркера и сохранить нужный вариант
- Превратить их в комментарии
- Переместить их в конец файла
* Правильный ответ: Удалить все три маркера и сохранить нужный вариант
Маркеры — служебная разметка: после выбора варианта их обязательно удаляют.

Какая команда завершает слияние после разрешения конфликта?
- git rebase --continue
- git commit (после git add)
- git merge --commit
- git checkout --commit
* Правильный ответ: git commit (после git add)
После git add разрешённых файлов обычный git commit создаёт merge-коммит. (Для rebase — только git rebase --continue.)

Что при git merge означает --ours?
- Вариант текущей ветки, в которую вливаются изменения
- Вариант вливаемой ветки
- Вариант из индекса
- Вариант из stash
* Правильный ответ: Вариант текущей ветки, в которую вливаются изменения
При merge --ours — текущая ветка (например, main), --theirs — вливаемя (feature). При rebase роли меняются.

Что при git rebase означает --theirs?
- Вариант перебазируемой ветки (feature)
- Вариант базы, поверх которой идёт rebase (main)
- Вариант из reflog
- Вариант из последнего коммита
* Правильный ответ: Вариант базы, поверх которой идёт rebase (main)
При rebase ours — ветка, которую перебазируют, theirs — база. Это противоположно merge.

Что делает rerere?
- Запоминает решения конфликтов и применяет их при повторе
- Удаляет все конфликты автоматически
- Отключает слияния
- Создаёт резервные копии файлов
* Правильный ответ: Запоминает решения конфликтов и применяет их при повторе
reuse recorded resolution: повторный одинаковый конфликт разрешается автоматически сохранённым решением.

Что произойдёт после git rebase --abort?
- Rebase отменится, ветка вернётся в исходное состояние
- Конфликт будет автоматически разрешён
- Будет создан merge-коммит
- Rebase продолжится с пропуском конфликта
* Правильный ответ: Rebase отменится, ветка вернётся в исходное состояние
--abort откатывает rebase целиком, возвращая ветку к состоянию до его начала.

Как проверить, что в репозитории не осталось маркеров конфликта?
- git grep -n '^<<<<<<<'
- git log --markers
- git diff --checkmarkers
- git status --markers
* Правильный ответ: git grep -n '^<<<<<<<'
Команда ищет строки, начинающиеся с маркера, по всем файлам дерева.

Какая команда открывает внешний инструмент сравнения?
- git mergetool
- git conflict --tool
- git diff --manual
- git merge --visual
* Правильный ответ: git mergetool
git mergetool запускает настроенный инструмент (meld, vimdiff и т. д.) для каждого конфликтующего файла.

Что из перечисленного снижает вероятность конфликтов?
- Частые git pull --rebase и маленькие коммиты
- Работа в одной ветке без pull
- Переименование файлов вместе с правкой содержимого
- Большие коммиты раз в месяц
* Правильный ответ: Частые git pull --rebase и маленькие коммиты
Маленькие коммиты и постоянная синхронизация уменьшают пересечение изменений в одних и тех же строках.
<!--/QUIZ-->
