---
title: reflog, bisect и восстановление
summary: Как Git хранит «страховку» из всех перемещений HEAD, как вернуть удалённые коммиты и ветки, как найти первый сломавший код коммит бинарным поиском.
order: 3
duration: 40 мин
difficulty: advanced
tags: git, reflog, bisect, восстановление, revert, reset, fsck
---

Git почти никогда не уничтожает коммиты мгновенно. У него есть «страховочная сетка»: `reflog` (журнал перемещений `HEAD`), висячие объекты и `fsck`. А `git bisect` помогает найти коммит, который сломал поведение, — с помощью бинарного поиска. Эти три инструмента превращают «катастрофу» (удалил ветку, откатил не то) в рутинную пятиминутную операцию.

## reflog: журнал перемещений HEAD

`reflog` — это локальный журнал, в который Git записывает **каждое** изменение указателя `HEAD`: коммиты, checkout, reset, merge, rebase, cherry-pick. Записи живут примерно 90 дней (настраивается через `gc.reflogExpire`).

```bash
git reflog
```

Пример вывода:

```
a1b2c3d HEAD@{0}: commit: feat: добавить логин
e4f5a6b HEAD@{1}: rebase (finish): returning to refs/heads/feature
e4f5a6b HEAD@{2}: rebase (start): checkout main
...
```

Правая колонка — действия, левая — куда указывал `HEAD`, а `HEAD@{1}` — «состояние HEAD на один шаг назад». Такая нотация работает в любой команде, ожидающей коммит:

```bash
git reset --hard HEAD@{1}    # вернуться на один шаг назад
git checkout HEAD@{2}        # посмотреть состояние два шага назад
git cherry-pick HEAD@{3}     # применить коммит из прошлого
```

## Восстановление удалённой ветки

Удалил ветку `git branch -D feature`? Не паникуй: она всё ещё есть в reflog.

```bash
git reflog | grep feature
# b2c3d4e5 HEAD@{4}: checkout: moving from feature to main
git checkout -b feature b2c3d4e5
```

Мы создали ветку заново из коммита, на который она указывала. Аналогично восстанавливается «потерянный» rebase: после `git rebase -i` старая версия ветки осталась в reflog как `HEAD@{n}` до rebase.

## reset, revert и восстановление файлов

- `git reset --hard <sha>` — жёсткий откат: и индекс, и рабочее дерево становятся как в коммите `<sha>`. Опасно, если в рабочем дереве есть несохранённые правки — они пропадут. Но сам коммит остаётся в reflog.
- `git reset --soft <sha>` — передвигает только `HEAD`; изменения остаются в индексе.
- `git reset --mixed <sha>` (по умолчанию) — передвигает `HEAD` и индекс, но не трогает рабочее дерево.
- `git revert <sha>` — создаёт **новый** коммит, отменяющий изменения `<sha>`. Безопасен для публичной истории: никто ничего не переписывает.

Правило выбора: публичная история — только `revert`; личная неопубликованная — можно `reset`. Вернуть отдельный файл к состоянию коммита:

```bash
git restore --source=HEAD~1 app.py
```

## fsck и висячие объекты

Коммиты, на которые ничто не ссылается (ни ветка, ни reflog), называются висячими (dangling). Если reflog уже почистили, их можно найти так:

```bash
git fsck --lost-found
# dangling commit a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8
```

`git fsck --lost-found` к тому же кладёт потерянные объекты в `.git/lost-found/`, откуда их можно достать `git show`-ом.

## bisect: бинарный поиск виновника

`git bisect` — это автоматизированная игра «холодно-горячо». Ты говоришь «этот коммит хороший, а этот плохой», а Git методом деления пополам находит первый коммит, после которого поведение сломалось.

```bash
git bisect start
git bisect bad HEAD          # текущее состояние плохое
git bisect good v1.0.0       # известный хороший коммит
```

Git переключит `HEAD` на коммит посередине. На нём ты проверяешь поведение (например, запускаешь тест) и говоришь:

```bash
git bisect good   # на этом коммите всё ещё хорошо
git bisect bad    # на этом коммите уже плохо
```

Так, логарифмически, за ~10 шагов из 1000 коммитов находится первый плохой. Автоматически — скриптом:

```bash
git bisect run pytest test_regression.py
```

Скрипт должен возвращать 0 (хорошо) или ненулевой код (плохо). В конце — `git bisect reset`, чтобы вернуться на исходную ветку.

<!--TASK-->
### Задача 1
Создай временный репозиторий с пятью коммитами и «случайно потеряй» ветку, затем верни её через reflog:

1. `git init`; настрой имя и почту; создай файл с пятью изменениями по одному коммиту (например, `v1`…`v5`).
2. На `v5` создай ветку `experiment`, добавь ещё два коммита (`v6`, `v7`).
3. Вернись на `main` и удали ветку `git branch -D experiment`.
4. Найди её коммит в `git reflog` и восстанови ветку `git checkout -b experiment <sha>`.

Ожидаемый результат: `git log --oneline experiment` показывает коммиты `v7`, `v6`, `v5` сверху вниз, а `git branch` снова показывает `experiment`.

### Задача 2
Напиши pytest-тест `test_reflog_restore.py`:

1. Временный репозиторий: коммит `A`, затем ветка `feature` с коммитами `B`, `C`.
2. Перейди на `main`, удали ветку `git branch -D feature`.
3. Считай `git reflog`, найди строку с `feature` и забери хэш (последний элемент строки).
4. Создай ветку заново и проверь: `git log --oneline feature` содержит `C` и `B`.

Запусти `pytest test_reflog_restore.py -v`: ожидаемый результат — `1 passed`.

### Задача 3
Напиши pytest-тест `test_bisect_finds_bad.py`: смоделируй регрессию и найди её bisect-ом:

1. Репозиторий: 6 коммитов подряд, в каждом файл `calc.py` содержит строку вида `RESULT = 1`, `RESULT = 2`, … `RESULT = 6` (один коммит на значение, файл перезаписывается целиком).
2. Напиши скрипт `check.sh`, который возвращает 0, если в файле `RESULT < 5`, иначе 1.
3. Запусти `git bisect start`, `git bisect bad HEAD`, `git bisect good HEAD~5`, затем `git bisect run ./check.sh`.
4. После завершения проверь, что `git show HEAD` содержит `RESULT = 5` (первый «плохой» коммит). Затем выполни `git bisect reset`.

Запусти `pytest test_bisect_finds_bad.py -v`: ожидаемый результат — `1 passed`.

### Задача 4
Сравни `revert` и `reset` на публичной истории. В репозитории из задачи 1:

1. Выполни `git revert` последнего коммита `main` и посмотри `git log --oneline -3`: должен появиться новый коммит отмены.
2. Затем вернись на одну позицию назад через `git reset --hard HEAD~1` и снова посмотри лог.

Ожидаемый результат: ты можешь объяснить разницу: `revert` добавляет коммит и не трогает историю, а `reset` передвигает ветку, «выбрасывая» коммит из истории. Запиши вывод обоих логов в блокнот — он пригодится на экзамене.

### Задача 5
Восстанови «потерявшийся» после `reset --hard` коммит. Сценарий:

1. Сделай три коммита. Выполни `git reset --hard HEAD~2` — строго передвинется, два коммита «исчезнут».
2. Найди их в `git reflog` (записи `HEAD@{1}`, `HEAD@{2}`).
3. Верни ветку на место через `git reset --hard HEAD@{1}`.

Ожидаемый результат: `git log --oneline` снова показывает все три коммита, а `git status` — чистое дерево.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
В `git reflog` найди строку с `checkout: moving from experiment to main` — хэш в её начале и есть последний коммит ветки. Команда `git checkout -b experiment <sha>` пересоздаст ветку с этого места.

### Подсказка 2
Reflog — это текст: `git reflog` в хелпере возвращает stdout. Ищи строку с подстрокой `feature`, разбей её по пробелам, первый элемент — хэш. Восстановление: `git checkout -b feature <sha>`; затем `git log --format=%s feature`.

### Подсказка 3
Файл `check.sh` обязательно сделай исполняемым: `os.chmod(path, 0o755)`. Внутри — `#!/bin/sh` и `grep -q 'RESULT = 5' calc.py && exit 1 || exit 0` (или проверка через python). `git bisect run` требует, чтобы скрипт в `cwd` репозитория. После run — `git bisect reset` обязателен, иначе тест оставит репозиторий в состоянии bisect.

### Подсказка 4
`git revert HEAD` создаёт коммит с сообщением `Revert "..."` — история растёт. `git reset --hard HEAD~1` в этой же точке удалит коммит revert (но не исходный коммит — он останется ниже по истории). Сравни длины логов и количество коммитов.

### Подсказка 5
Сразу после `git reset --hard HEAD~2` выполни `git reflog`: там будут `HEAD@{0}` (текущее состояние) и `HEAD@{1}` (предыдущее, с потерянными коммитами). `git reset --hard HEAD@{1}` вернёт ветку на место. Если прошло много времени и запись вымылась — используй `git fsck --lost-found`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Шаги:

```bash
git init
git config user.name "Тест"
git config user.email "test@example.com"

for i in 1 2 3 4 5; do echo "v$i" > file.txt; git add file.txt; git commit -m "v$i"; done

git checkout -b experiment
echo v6 > file.txt && git add file.txt && git commit -m "v6"
echo v7 > file.txt && git add file.txt && git commit -m "v7"

git checkout main
git branch -D experiment

git reflog | grep experiment
# b2c3d4e5 HEAD@{4}: checkout: moving from experiment to main
git checkout -b experiment b2c3d4e5
git log --oneline experiment
```

Строка `checkout: moving from experiment to main` — момент, когда мы ушли с ветки; её хэш — верхушка `experiment`. Пересоздание ветки из этого коммита возвращает всю её историю: `v7`, `v6`, `v5`. Почему это работает: ветка — просто указатель на коммит; пока коммит жив (в reflog или как висячий), ветку можно воссоздать. `git branch -D` удаляет только указатель, не данные. Те же приёмы работают для rebase и merge: состояние до операции всегда в reflog.

### Разбор 2
Решение:

```python
import subprocess
import tempfile
from pathlib import Path

import pytest


def git(*args, cwd):
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True,
        capture_output=True, text=True,
    ).stdout.strip()


def commit_file(repo, name, content, message):
    (Path(repo) / name).write_text(content)
    git("add", name, cwd=repo)
    git("commit", "-m", message, cwd=repo)


def test_reflog_restores_deleted_branch():
    with tempfile.TemporaryDirectory() as repo:
        git("init", cwd=repo)
        git("config", "user.name", "Тест", cwd=repo)
        git("config", "user.email", "test@example.com", cwd=repo)

        commit_file(repo, "f.txt", "A\n", "A")
        git("checkout", "-b", "feature", cwd=repo)
        commit_file(repo, "f.txt", "A\nB\n", "B")
        commit_file(repo, "f.txt", "A\nB\nC\n", "C")

        git("checkout", "main", cwd=repo)
        git("branch", "-D", "feature", cwd=repo)

        reflog = git("reflog", cwd=repo)
        line = next(l for l in reflog.splitlines() if "feature" in l)
        sha = line.split()[0]

        git("checkout", "-b", "feature", sha, cwd=repo)
        messages = git("log", "--format=%s", "feature", cwd=repo)
        assert "C" in messages and "B" in messages
```

Разбор: `git branch -D feature` удаляет только указатель. В reflog остаётся запись о переходе `moving from feature to main`; её хэш — верхушка ветки. `git checkout -b feature <sha>` воссоздаёт указатель, и история `B`, `C` снова доступна. Ошибки, которые можно допустить: не найти строку (если до checkout было ещё действие — ищи `checkout: moving from feature`), или взять не тот хэш (первый элемент строки). Запуск: `pytest test_reflog_restore.py -v` → `1 passed`.

### Разбор 3
Решение:

```python
import os
import subprocess
import tempfile
from pathlib import Path

import pytest


def git(*args, cwd):
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True,
        capture_output=True, text=True,
    ).stdout.strip()


def commit_file(repo, name, content, message):
    (Path(repo) / name).write_text(content)
    git("add", name, cwd=repo)
    git("commit", "-m", message, cwd=repo)


def test_bisect_finds_bad_commit():
    with tempfile.TemporaryDirectory() as repo:
        git("init", cwd=repo)
        git("config", "user.name", "Тест", cwd=repo)
        git("config", "user.email", "test@example.com", cwd=repo)

        for i in range(1, 7):
            commit_file(repo, "calc.py", f"RESULT = {i}\n", f"step {i}")

        script = Path(repo) / "check.sh"
        script.write_text("#!/bin/sh\ngrep -q 'RESULT = 5' calc.py && exit 1 || exit 0\n")
        os.chmod(script, 0o755)

        git("bisect", "start", cwd=repo)
        git("bisect", "bad", "HEAD", cwd=repo)
        git("bisect", "good", "HEAD~5", cwd=repo)
        git("bisect", "run", "./check.sh", cwd=repo)

        head = git("show", "HEAD", "--format=%s", "--no-patch", cwd=repo)
        assert head == "step 5"

        git("bisect", "reset", cwd=repo)
```

Разбор: скрипт возвращает 1 (плохо) при `RESULT = 5` и 0 (хорошо) при меньших значениях. `git bisect run` последовательно проверяет средние коммиты: сначала `step 3` (хорошо), затем `step 5` (плохо), затем `step 4`, и локализует первый плохой — `step 5`. Важно: `git bisect reset` в конце обязателен — без него тест оставил бы репозиторий в состоянии bisect, и последующие команды упали бы. Проверка через `git show HEAD --format=%s` показывает имя коммита, на котором остановился bisect. Запуск: `pytest test_bisect_finds_bad.py -v` → `1 passed`.

### Разбор 4
До операций лог: `v7`, `v6`, …, `v1`. После `git revert HEAD`:

```
Revert "v7"
v7
v6
...
```

Появился новый коммит-«антипод», история не переписывалась. После `git reset --hard HEAD~1` этот коммит revert исчез — ветка снова смотрит на `v7`, но `v7` и `v6` на месте: `reset` сдвинул указатель, а коммиты остались в reflog. Итог: `revert` безопасен для публичной истории (все видят, что отменено), `reset` подходит только для личной неопубликованной истории. На практике: случайно влил фичу в `main` — `git revert` (не переписывай общую историю); в своей ветке накосячил — `git reset --hard`.

### Разбор 5
Команды:

```bash
echo 1 > f.txt && git add f.txt && git commit -m "one"
echo 2 > f.txt && git add f.txt && git commit -m "two"
echo 3 > f.txt && git add f.txt && git commit -m "three"

git reset --hard HEAD~2   # теперь лог показывает только "one"
git reflog
# HEAD@{0}: reset: moving to HEAD~2
# HEAD@{1}: commit: three
# HEAD@{2}: commit: two
git reset --hard HEAD@{1}
git log --oneline
# three, two, one
```

Разбор: `git reset --hard HEAD~2` передвинул ветку на два коммита назад — `two` и `three` отвязались, но не исчезли: они в reflog. `HEAD@{1}` — состояние до reset, то есть верхушка с `three`. `git reset --hard HEAD@{1}` восстанавливает всё. Мораль: даже после жёсткого reset коммиты живы ~90 дней, и почти любой «потерянный» коммит возвращается. Памятка: при работе с чужими репозиториями `reset --hard` чужой истории не исправит — там только `revert`.
<!--/SOLUTION-->

<!--QUIZ-->
Что хранит git reflog?
- Только удалённые ветки
- Историю всех перемещений HEAD: коммиты, checkout, reset, merge, rebase
- Содержимое всех файлов
- Пароли и ключи доступа
* Правильный ответ: Историю всех перемещений HEAD: коммиты, checkout, reset, merge, rebase
Каждое изменение указателя HEAD фиксируется в reflog с меткой времени и описанием действия.

Сколько примерно дней живут записи reflog по умолчанию?
- 7 дней
- 90 дней
- 365 дней
- Навсегда
* Правильный ответ: 90 дней
По умолчанию записи reflog истекают через ~90 дней (настройка gc.reflogExpire).

Как обозначается состояние HEAD «на один шаг назад»?
- HEAD~1
- HEAD@{1}
- HEAD-1
- HEAD^1
* Правильный ответ: HEAD@{1}
Нотация HEAD@{n} — n-й шаг назад по reflog. HEAD~1 — первый родитель по истории коммитов.

Какая команда удаляет ветку, но оставляет её коммиты в reflog?
- git branch -d feature
- git branch -D feature
- git branch --delete-all feature
- git diff --delete feature
* Правильный ответ: git branch -D feature
-D удаляет ветку принудительно; коммиты остаются доступны через reflog и могут быть восстановлены.

Какая команда возвращает ветку к более раннему состоянию и при этом создаёт новый коммит?
- git reset --hard
- git revert
- git checkout
- git rebase
* Правильный ответ: git revert
revert создаёт новый коммит, отменяющий изменения указанного, не переписывая историю.

Что делает git reset --hard <sha>?
- Передвигает HEAD и индекс, но не трогает рабочее дерево
- Передвигает HEAD, индекс и рабочее дерево к <sha>
- Копирует <sha> в новую ветку
- Создаёт коммит отмены
* Правильный ответ: Передвигает HEAD, индекс и рабочее дерево к <sha>
--hard жёстко синхронизирует все три области с коммитом; несохранённые правки пропадут.

Что возвращает git fsck --lost-found?
- Список висячих (dangling) объектов, на которые никто не ссылается
- Список всех веток репозитория
- Список настроенных remote
- Список конфликтующих файлов
* Правильный ответ: Список висячих (dangling) объектов, на которые никто не ссылается
Коммиты без ссылок ищутся через fsck; их можно восстановить по хэшу.

Что делает git bisect run ./check.sh?
- Автоматически прогоняет скрипт на средних коммитах, пока не найдёт первый «плохой»
- Запускает скрипт один раз на текущем коммите
- Ищет скрипты в репозитории
- Сравнивает два коммита
* Правильный ответ: Автоматически прогоняет скрипт на средних коммитах, пока не найдёт первый «плохой»
Скрипт должен возвращать 0 для «хороших» коммитов и ненулевой код для «плохих».

Какую команду нужно выполнить после завершения bisect?
- git bisect reset
- git bisect end
- git bisect finish
- git bisect stop
* Правильный ответ: git bisect reset
reset возвращает HEAD на исходную ветку и выходит из режима bisect.

Какая команда вернёт отдельный файл к состоянию из коммита?
- git restore --source=HEAD~1 app.py
- git checkout --all
- git reset --soft file
- git revert --file app.py
* Правильный ответ: git restore --source=HEAD~1 app.py
git restore с --source берёт содержимое файла из указанного коммита.
<!--/QUIZ-->
