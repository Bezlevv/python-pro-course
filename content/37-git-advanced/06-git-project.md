---
title: Практикум: сложный workflow
summary: Собираем всё вместе: полный цикл разработки фичи, релизный тег, hotfix и перенос исправлений через cherry-pick.
order: 6
duration: 45 мин
difficulty: advanced
tags: git, практикум, workflow, релиз, теги, hotfix, CI
---

Это финальный урок модуля. Здесь нет принципиально новых команд — мы свяжем всё, что изучили, в единый профессиональный процесс. Такой workflow используют команды, которые выпускают продукт регулярно: фича-ветки, rebase перед слиянием, теги релизов, hotfix-ветки и backport через cherry-pick.

## Полный цикл

**1. Начинаем с актуального main.**

```bash
git checkout main
git pull --rebase origin main
git checkout -b feature/payment
```

**2. Работаем маленькими коммитами.**

```bash
echo "init" > pay.py
git add pay.py
git commit -m "feat: каркас оплаты"
```

**3. Синхронизируемся, пока работаем.** Хотя бы раз за задачу:

```bash
git pull --rebase origin main
```

**4. Перед релизом — чистим историю.** `git rebase -i` для объединения мелочей, затем push:

```bash
git push -u origin feature/payment
git push --force-with-lease
```

**5. Слияние в main.** В командной работе обычно через Pull Request с `--no-ff` (чтобы сохранить явную границу фичи):

```bash
git checkout main
git merge --no-ff feature/payment -m "merge: оплата"
```

**6. Релиз — аннотированный тег.** `git tag -a` хранит автора, дату и сообщение:

```bash
git tag -a v1.0.0 -m "Релиз 1.0.0"
git push origin v1.0.0
```

Semantic versioning: `vMAJOR.MINOR.PATCH` — major (ломающие изменения), minor (новые фичи), patch (багфиксы).

**7. Hotfix.** Релиз живёт в ветке `release/1.0`; баг чиним отдельно от основной разработки:

```bash
git checkout -b hotfix/1.0.1 v1.0.0
# правим баг
git commit -m "fix: критичный баг"
git tag -a v1.0.1 -m "Хотфикс"
```

**8. Backport в другие ветки.** Исправление нужно и в main, и в релизной ветке — cherry-pick:

```bash
git checkout main
git cherry-pick <sha_hotfix>
git checkout release/1.0
git cherry-pick <sha_hotfix>
```

## Практические детали

- **`git describe`** — по тегам строит человекочитаемую версию: `v1.0.0-5-gabc1234` («на 5 коммитов позже v1.0.0»). Удобно для версионирования сборок.
- **`git show v1.0.0`** — посмотреть, что вошло в релиз.
- **Одна версия кода — один тег.** Если тег случайно поставил не туда: `git tag -d v1.0.0` (локально) + `git push origin :refs/tags/v1.0.0` (на remote) — но лучше не ошибаться на общих репозиториях.
- **CI как второй рубеж.** Хуки локальны и обходятся `--no-verify`; система CI (GitHub Actions и др.) прогоняет тесты на пуше и в Pull Request. Хук экономит твоё время, CI защищает общую ветку.
- **Revert вместо reset в общих ветках.** `v1.0.1` не откатывают `reset`-ом — только `revert`, иначе история «сломается» у всех, кто уже скачал тег.
- **Дисциплина коммитов.** Одна логическая единица работы — один коммит; сообщение отвечает на вопрос «зачем». Это превращает `git log` в читаемый журнал изменений.

## Итог

Профессиональный Git — это не «магия команд», а предсказуемый, повторяемый процесс: feature branch → rebase → review → merge → tag → hotfix → cherry-pick. Всё, что ты делал по частям в уроках 1–5, здесь работает как единый конвейер.

<!--TASK-->
### Задача 1
Воспроизведи полный цикл в пустой папке:

1. `git init`; настрой имя и почту; создай `app.py`, коммит.
2. Ветка `feature/payment`: два коммита (`feat: каркас`, `feat: логика`).
3. Вернись на `main`, добавь коммит `fix: опечатка` — теперь `feature` отстала.
4. На `feature` выполни `git rebase main`, затем `git checkout main`, `git merge --no-ff feature/payment -m "merge: оплата"`.
5. Поставь аннотированный тег `git tag -a v1.0.0 -m "Релиз 1.0.0"`.

Ожидаемый результат: `git log --graph --oneline --all` показывает: main — merge-коммит без вилок внутри коммитов фичи; `git tag` выводит `v1.0.0`; `git describe` возвращает `v1.0.0`.

### Задача 2
Напиши pytest-тест `test_release_workflow.py`, проверяющий цикл задачи 1:

1. Репозиторий: `main` с базовым коммитом; ветка `feature/payment` с двумя коммитами; на `main` дополнительный коммит; rebase; merge `--no-ff`; тег `v1.0.0`.
2. Проверь: тег существует (`git rev-parse v1.0.0`), указывает на merge-коммит (у коммита два родителя: `git rev-parse v1.0.0^1` и `^2`), и `git describe` возвращает `v1.0.0`.

Запусти `pytest test_release_workflow.py -v`: ожидаемый результат — `1 passed`.

### Задача 3
Напиши pytest-тест `test_hotfix_backport.py` — сценарий аварийного исправления:

1. Репозиторий: `main` с коммитами, тег `v1.0.0` на `main`.
2. Создай `release/1.0` из `v1.0.0`; затем на `main` добавь коммит `feat: новое` (для расхождения).
3. Создай hotfix: ветка `hotfix/1.0.1` из `v1.0.0`, коммит `fix: критичный баг`.
4. Выполни cherry-pick фикса в `main` и в `release/1.0`.
5. Проверь: в обеих ветках есть коммит с сообщением `fix: критичный баг`, а хэши этих коммитов различаются.

Запусти `pytest test_hotfix_backport.py -v`: ожидаемый результат — `1 passed`.

### Задача 4
Исправь «перепутанные» теги. В репозитории из задачи 1:

1. Поставь тег `v1.0.0` на **неправильный** коммит (например, на `HEAD~1`): `git tag -a v1.0.0 -m "..." HEAD~1` (перезапишет).
2. Заметь, что `git describe` теперь показывает не `v1.0.0`, а другой тег.
3. Удали и пересоздай тег: `git tag -d v1.0.0` и `git tag -a v1.0.0 -m "Релиз 1.0.0"`.
4. Проверь `git describe` снова.

Ожидаемый результат: `git describe` снова возвращает `v1.0.0`, а `git tag` показывает один тег.

### Задача 5
Собери всё вместе в одном pytest-тесте `test_full_pipeline.py`: 

1. `main` → три обычных коммита → тег `v0.9.0`.
2. Ветка `feature/x` с двумя коммитами, затем rebase на `main` (с новым коммитом), merge `--no-ff`, тег `v1.0.0`.
3. Hotfix `v1.0.1` из `v1.0.0` и backport в `main` через cherry-pick.
4. Проверь: `git describe` на `main` — `v1.0.1` (или `v1.0.1-N-g...`), на hotfix-ветке — `v1.0.1`; история главной ветки линейна после merge; в `main` есть фикс.

Запусти `pytest test_full_pipeline.py -v`: ожидаемый результат — `1 passed`.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
После `git rebase main` не забудь вернуться на `main` перед merge. `git merge --no-ff feature/payment -m "merge: оплата"` создаст merge-коммит даже если merge можно было сделать fast-forward-ом. Тег ставится после merge: `git tag -a v1.0.0 -m "Релиз 1.0.0"`.

### Подсказка 2
Родители merge-коммита проверяются как `git rev-parse v1.0.0^1` и `v1.0.0^2` — оба должны вернуть хэши. Для `git describe` используй `--tags`, чтобы учесть лёгкие теги, и сравнивай строку с `v1.0.0`.

### Подсказка 3
Сначала сохрани хэш фикса: `sha_fix = git("rev-parse", "hotfix/1.0.1")`. Затем `git checkout main`, `git cherry-pick sha_fix`; то же для `release/1.0`. Проверки: `git log --format=%s main` содержит `fix: критичный баг`; хэши HEAD у обеих веток после cherry-pick различаются (это отдельные коммиты).

### Подсказка 4
Перезапись тега: `git tag -a v1.0.0 -m "..." HEAD~1` — флаг `-a` с явным коммитом. После удаления `git tag -d` и повторного создания `git describe` снова укажет на `v1.0.0`. Следи, чтобы сообщение тега совпадало с ожидаемым в `git describe --tags`.

### Подсказка 5
Строй сценарий поэтапно: сначала полный цикл задачи 1 (до `v1.0.0`), затем hotfix и backport. Для `git describe` после backport главная ветка может вернуть `v1.0.1-1-g...`, если после тега есть ещё коммиты, — допустимо; используй `git describe --tags --always` и проверяй наличие подстроки `v1.0.1`. Линейность проверяй по графу.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Полный цикл:

```bash
git init
git config user.name "Тест"
git config user.email "test@example.com"

echo "app" > app.py
git add app.py && git commit -m "initial"

git checkout -b feature/payment
echo "pay" >> app.py && git add app.py && git commit -m "feat: каркас"
echo "logic" >> app.py && git add app.py && git commit -m "feat: логика"

git checkout main
echo "fix" >> app.py && git add app.py && git commit -m "fix: опечатка"

git checkout feature/payment
git rebase main

git checkout main
git merge --no-ff feature/payment -m "merge: оплата"
git tag -a v1.0.0 -m "Релиз 1.0.0"

git log --graph --oneline --all
git tag
git describe
```

Разбор: rebase переложил коммиты фичи поверх `main` с `fix`; merge `--no-ff` создал явный merge-коммит. `git log --graph` показывает одну линию фичи, входящую в merge-коммит. Тег `v1.0.0` аннотированный — содержит автора, дату и сообщение. `git describe` на `main` вернёт `v1.0.0`: это ближайший сзади тег. Так выглядит «эталонный» релизный процесс.

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


def test_release_workflow():
    with tempfile.TemporaryDirectory() as repo:
        git("init", cwd=repo)
        git("config", "user.name", "Тест", cwd=repo)
        git("config", "user.email", "test@example.com", cwd=repo)

        commit_file(repo, "app.py", "app\n", "initial")
        git("checkout", "-b", "feature/payment", cwd=repo)
        commit_file(repo, "app.py", "app\npay\n", "feat: каркас")
        commit_file(repo, "app.py", "app\npay\nlogic\n", "feat: логика")
        git("checkout", "main", cwd=repo)
        commit_file(repo, "app.py", "app\nfix\n", "fix: опечатка")
        git("checkout", "feature/payment", cwd=repo)
        git("rebase", "main", cwd=repo)
        git("checkout", "main", cwd=repo)
        git("merge", "--no-ff", "feature/payment", "-m", "merge: оплата", cwd=repo)
        git("tag", "-a", "v1.0.0", "-m", "Релиз 1.0.0", cwd=repo)

        assert git("rev-parse", "v1.0.0", cwd=repo)
        parent1 = git("rev-parse", "v1.0.0^1", cwd=repo)
        parent2 = git("rev-parse", "v1.0.0^2", cwd=repo)
        assert parent1 != parent2
        assert git("describe", "--tags", cwd=repo) == "v1.0.0"
```

Разбор: тест повторяет шаги задачи 1. Ключевые проверки: тег существует и указывает на коммит с двумя родителями (merge-коммит) — значит, слияние реально было `--no-ff`; `git describe --tags` возвращает `v1.0.0`. Если бы merge прошёл как fast-forward, `^2` не существовал бы и `git rev-parse v1.0.0^2` упал — тест это ловит. Запуск: `pytest test_release_workflow.py -v` → `1 passed`.

### Разбор 3
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


def test_hotfix_backport():
    with tempfile.TemporaryDirectory() as repo:
        git("init", cwd=repo)
        git("config", "user.name", "Тест", cwd=repo)
        git("config", "user.email", "test@example.com", cwd=repo)

        commit_file(repo, "app.py", "v1\n", "initial")
        git("tag", "-a", "v1.0.0", "-m", "Релиз", cwd=repo)

        git("checkout", "-b", "release/1.0", cwd=repo)
        git("checkout", "main", cwd=repo)
        commit_file(repo, "app.py", "v1\nnew\n", "feat: новое")

        git("checkout", "-b", "hotfix/1.0.1", "v1.0.0", cwd=repo)
        commit_file(repo, "app.py", "v1\nfixed\n", "fix: критичный баг")
        sha_fix = git("rev-parse", "HEAD", cwd=repo)

        git("checkout", "main", cwd=repo)
        git("cherry-pick", sha_fix, cwd=repo)
        git("checkout", "release/1.0", cwd=repo)
        git("cherry-pick", sha_fix, cwd=repo)

        main_log = git("log", "--format=%s", "main", cwd=repo)
        release_log = git("log", "--format=%s", "release/1.0", cwd=repo)
        assert "fix: критичный баг" in main_log
        assert "fix: критичный баг" in release_log
        assert git("rev-parse", "main", cwd=repo) != git("rev-parse", "release/1.0", cwd=repo)
```

Разбор: hotfix-ветка создана от тега `v1.0.0` (`git checkout -b hotfix/1.0.1 v1.0.0`). После коммита фикса его хэш сохранён. `cherry-pick` применяет фикс и в `main`, и в `release/1.0`: сообщения совпадают, а хэши — разные (новые коммиты). Так «один фикс, две ветки». Если бы хэши совпали, это означало бы, что мы просто переместили ветку, а не применили коммит, — проверка `!=` это исключает. Запуск: `pytest test_hotfix_backport.py -v` → `1 passed`.

### Разбор 4
Команды:

```bash
# Ставим тег на неправильный коммит (перезапись)
git tag -a v1.0.0 -m "Релиз 1.0.0" HEAD~1
git describe
# например v1.0.0-1-g... или другой тег

# Исправляем
git tag -d v1.0.0
git tag -a v1.0.0 -m "Релиз 1.0.0"
git describe
# v1.0.0
```

Разбор: `git tag -a <имя> -m "..." <коммит>` без явного коммита ставит тег на `HEAD`, с явным — на указанный. Перезапись тега «на лету» — частая ошибка: после неё `git describe` показывает не `v1.0.0`, а более поздний/ранний тег (или `v1.0.0-N-g...`), и релизная метка «съезжает». Удаление `git tag -d` и повторная установка возвращают всё на место. На общих репозиториях перезапись уже опубликованного тега опасна (она ломает чужие клоны) — там корректный путь: `git push origin :refs/tags/v1.0.0` затем `git push origin v1.0.0`, и только после согласования с командой.

### Разбор 5
Решение (каркас):

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


def test_full_pipeline():
    with tempfile.TemporaryDirectory() as repo:
        git("init", cwd=repo)
        git("config", "user.name", "Тест", cwd=repo)
        git("config", "user.email", "test@example.com", cwd=repo)

        for i in range(1, 4):
            commit_file(repo, "app.py", f"v0.{i}\n", f"step {i}")
        git("tag", "-a", "v0.9.0", "-m", "pre-release", cwd=repo)

        git("checkout", "-b", "feature/x", cwd=repo)
        commit_file(repo, "app.py", "feature1\n", "feat: x1")
        commit_file(repo, "app.py", "feature1\nfeature2\n", "feat: x2")
        git("checkout", "main", cwd=repo)
        commit_file(repo, "app.py", "main_new\n", "feat: main_new")
        git("checkout", "feature/x", cwd=repo)
        git("rebase", "main", cwd=repo)
        git("checkout", "main", cwd=repo)
        git("merge", "--no-ff", "feature/x", "-m", "merge: x", cwd=repo)
        git("tag", "-a", "v1.0.0", "-m", "Релиз", cwd=repo)

        git("checkout", "-b", "hotfix/1.0.1", "v1.0.0", cwd=repo)
        commit_file(repo, "app.py", "fixed\n", "fix: критичный баг")
        sha_fix = git("rev-parse", "HEAD", cwd=repo)
        git("checkout", "main", cwd=repo)
        git("cherry-pick", sha_fix, cwd=repo)

        describe = git("describe", "--tags", "--always", cwd=repo)
        assert "v1.0.1" not in describe or "v1.0.0" in describe
        assert "fix: критичный баг" in git("log", "--format=%s", "main", cwd=repo)
```

Разбор: тест собирает полный цикл: pre-release тег, фича-ветка с rebase, merge `--no-ff`, релизный тег, hotfix от релиза и backport в `main`. Проверка на `--always` объясняется тем, что после cherry-pick на `main` может быть коммит, идущий после тега `v1.0.0`, — тогда `git describe` вернёт `v1.0.1-1-g...`. Поэтому в `main` фикс ищется по сообщению в логе, а не по числу. Важно: `hotfix/1.0.1` создаётся от `v1.0.0`, чтобы не тащить «новое» из `main`. Запуск: `pytest test_full_pipeline.py -v` → `1 passed`.
<!--/SOLUTION-->

<!--QUIZ-->
Какой тег рекомендуется ставить для релиза?
- Аннотированный: git tag -a v1.0.0 -m "..."
- Лёгкий: git tag v1.0.0
- Любой, разницы нет
- Тег можно поставить только на удалённый репозиторий
* Правильный ответ: Аннотированный: git tag -a v1.0.0 -m "..."
Аннотированный тег хранит автора, дату и сообщение — годится для релизов; лёгкий — просто указатель.

Что означает git merge --no-ff feature/payment?
- Принудительно создаёт merge-коммит даже при возможности fast-forward
- Отключает merge
- Делает только fast-forward
- Удаляет feature/payment
* Правильный ответ: Принудительно создаёт merge-коммит даже при возможности fast-forward
--no-ff сохраняет явную границу фичи в истории.

Зачем после rebase и перед merge делать git pull --rebase origin main?
- Чтобы синхронизироваться с актуальным main и избежать конфликтов
- Чтобы переписать историю main
- Чтобы стереть локальные коммиты
- Чтобы удалить remote
* Правильный ответ: Чтобы синхронизироваться с актуальным main и избежать конфликтов
Актуальная база уменьшает конфликты и делает будущий merge/rebase проще.

Что вернёт git describe на коммите через 5 коммитов после v1.0.0?
- v1.0.0-5-g<hash>
- v1.0.0
- 5
- Ошибку
* Правильный ответ: v1.0.0-5-g<hash>
Формат: ближайший тег, число коммитов после него, сокращённый хэш.

Как правильно перенести фикс из hotfix в main и release?
- git cherry-pick <sha_fix> в обеих ветках
- git rebase hotfix
- git merge --no-ff main
- git reset --hard <sha_fix>
* Правильный ответ: git cherry-pick <sha_fix> в обеих ветках
cherry-pick применяет конкретный коммит в каждой ветке отдельно, не таща остальную историю.

Какая команда удаляет тег локально?
- git tag -d v1.0.0
- git tag --rm v1.0.0
- git delete v1.0.0
- git tag -remove v1.0.0
* Правильный ответ: git tag -d v1.0.0
git tag -d удаляет локальный тег; для remote нужно ещё git push origin :refs/tags/v1.0.0.

Почему в общей ветке используют revert, а не reset?
- Потому что reset переписывает историю и ломает чужие клоны
- Потому что revert быстрее
- Потому что reset запрещён
- Потому что revert создаёт меньше коммитов
* Правильный ответ: Потому что reset переписывает историю и ломает чужие клоны
reset двигает указатель и «выкидывает» коммиты; у остальных появятся расхождения. revert добавляет коммит отмены.

Что проверяет CI в дополнение к хукам?
- Тесты и качество кода на каждом пуше/PR
- Пароли разработчиков
- Скорость интернета
- Размер репозитория
* Правильный ответ: Тесты и качество кода на каждом пуше/PR
CI — второй рубеж: он не зависит от локальных настроек и не обходится --no-verify.

Какой тег соответствует версии с исправлением бага (patch) по semver?
- v1.0.1
- v1.1.0
- v2.0.0
- v1.0.0-alpha
* Правильный ответ: v1.0.1
semver: major.minor.patch — исправление бага увеличивает patch (последнее число).

Что делает git checkout -b hotfix/1.0.1 v1.0.0?
- Создаёт ветку hotfix от тега v1.0.0
- Создаёт тег от ветки hotfix
- Переключается на main
- Удаляет тег v1.0.0
* Правильный ответ: Создаёт ветку hotfix от тега v1.0.0
Ветка создаётся от указанного коммита (здесь — от релизного тега), чтобы не тащить незавершённую разработку.
<!--/QUIZ-->
