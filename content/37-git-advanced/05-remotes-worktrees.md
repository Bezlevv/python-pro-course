---
title: Remote-стратегии и worktree
summary: Как устроены удалённые репозитории, как правильно пушить и тянуть, зачем --force-with-lease, и как работать с несколькими рабочими копиями через worktree.
order: 5
duration: 40 мин
difficulty: advanced
tags: git, remote, fetch, pull, push, force-with-lease, worktree, GitHub flow
---

До сих пор мы работали локально. Но смысл Git — в совместной работе, а она начинается с **remote** — удалённых репозиториев, с которыми твой локальный обменивается коммитами. Понимание механики fetch/pull/push и правил работы с чужими ветками отличает «просто умеющего git» от инженера, которому можно доверить общую ветку.

## Что такое remote

`remote` — это просто именованная ссылка на другой репозиторий (обычно по https или ssh). По умолчанию главный называется `origin`:

```bash
git remote -v
# origin  https://github.com/user/project.git (fetch)
# origin  https://github.com/user/project.git (push)
git remote add team https://...team.../project.git
git remote get-url origin
git remote set-url origin https://новый/адрес.git
```

Для экспериментов можно использовать локальный путь — Git спокойно работает с `file://` и с директориями. Например, удалённый репозиторий делается «голым» (bare) — без рабочего дерева, только объекты и ссылки:

```bash
git init --bare project.git
```

## fetch vs pull vs push

- `git fetch` — скачивает объекты и ветки с remote, но **не трогает** твои локальные ветки. После fetch обновляются только `origin/*`.
- `git pull` = `fetch` + слияние текущей ветки с её upstream.
- `git push` — отправляет локальные коммиты в remote.

Точная картина после `git fetch`:

```bash
git fetch origin
git log --oneline origin/main   # то, что на remote
git log --oneline main          # то, что у тебя
```

## pull: три стратегии

`git pull` по умолчанию делает merge. Это создаёт «вилки» в истории. Стратегии:

| Команда | Поведение |
|---|---|
| `git pull` | fetch + merge (merge-коммит при расхождении) |
| `git pull --rebase` | fetch + rebase локальных коммитов поверх origin |
| `git pull --ff-only` | только fast-forward; если ветки разошлись — отказ |

Современная команда `git pull --rebase` — стандарт для ежедневной синхронизации: твои локальные коммиты аккуратно перекладываются поверх свежих чужих, история остаётся линейной. Можно закрепить поведение:

```bash
git config pull.rebase true
```

## push: upstream и «принудительность»

Первая отправка новой ветки:

```bash
git push -u origin feature/login
```

`-u` устанавливает upstream — связь локальной ветки с `origin/feature/login`. Дальше достаточно `git push`.

Обычный push работает только при **fast-forward**: Git откажется отправлять, если в remote есть коммиты, которых нет локально. Это защита от перезаписи.

Но иногда хочется переписать историю ветки (после rebase/squash). Тогда нужен `--force`. Голый `git push --force` опасен: он молча затирает чужие коммиты. Правильный вариант — `--force-with-lease`:

```bash
git push --force-with-lease origin feature/login
```

Он отправляет принудительно, но **только если** remote-ветка с тех пор не менялась: если кто-то успел запушить, push откажется. Это защита от перезаписи чужой работы.

## Рабочий процесс (GitHub Flow)

1. `git checkout -b feature/...` от актуального `main`;
2. маленькие коммиты с понятными сообщениями;
3. регулярно `git pull --rebase origin main` — чтобы не отставать;
4. push ветки, открытие Pull Request;
5. после ревью и правок (снова squash/amend) — `git push --force-with-lease`;
6. слияние в `main`.

## worktree: несколько рабочих копий

`git worktree` позволяет держать несколько рабочих деревьев из одного репозитория. Нужно, когда ты работаешь над фичей, а на `main` срочно нужно исправить баг — не переключаясь, не пряча незавершённое:

```bash
git worktree add ../hotfix -b hotfix/fix
```

Это создаст папку `../hotfix` с рабочим деревом на новой ветке `hotfix/fix`. Основной репозиторий продолжает жить своей жизнью. Посмотреть список:

```bash
git worktree list
git worktree remove ../hotfix
```

Один репозиторий, много рабочих деревьев — удобно при долгих задачах и при параллельной работе над двумя версиями кода.

<!--TASK-->
### Задача 1
Создай голый remote и разыграй цикл fetch/pull/push:

1. `git init --bare project.git` в отдельной папке.
2. В рабочей папке `git init`, добавь remote: `git remote add origin ../project.git`.
3. Сделай два коммита (например, `v1`, `v2`) и `git push -u origin main`.
4. Добавь третье изменение и снова запушь.
5. Выполни `git fetch origin`, затем сравни `git log --oneline origin/main` и `git log --oneline main` — они должны совпадать.

Ожидаемый результат: `git push -u origin main` выводит `main -> main` и `branch 'main' set up to track 'origin/main'`, а оба списка коммитов идентичны.

### Задача 2
Напиши pytest-тест `test_pull_rebase_linear.py`: смоделируй двух разработчиков с общим remote:

1. Голый репозиторий `origin`; первый рабочий каталог `alice` — коммит `A`, push в `origin`.
2. Второй рабочий каталог `bob` клонирует `origin` (`git clone origin bob`), делает коммит `B` (на `main`), но **не** пушит.
3. `alice` делает коммит `C` и пушит.
4. `bob` выполняет `git pull --rebase` и затем `git push`.
5. Проверь: в `bob` история линейна — `git log --oneline --graph main` не содержит символов вилок, и в ней три коммита: `A`, `C`, `B` (C раньше B).

Запусти `pytest test_pull_rebase_linear.py -v`: ожидаемый результат — `1 passed`.

### Задача 3
Напиши pytest-тест `test_force_with_lease.py`, который доказывает защиту `--force-with-lease`:

1. Голый `origin`; `alice` — коммит `A`, push.
2. `bob` клонирует, делает коммит и пушит — теперь в origin `B`.
3. `alice` (у которой в памяти всё ещё `origin/main` = `A`) переписывает свою историю (`git commit --amend`) и пытается `git push --force-with-lease origin main` — push должен быть **отклонён**.
4. После `git fetch` (обновление памяти) `git push --force-with-lease origin main` — должен пройти.

Запусти `pytest test_force_with_lease.py -v`: ожидаемый результат — `1 passed`.

### Задача 4
Поработай с worktree:

1. В репозитории из задачи 1 создай ветку `feature/pain` с одним коммитом.
2. Выполни `git worktree add ../fix -b hotfix/fix`.
3. В новой папке `../fix` измени файл, сделай коммит.
4. Проверь `git worktree list`: должно быть два рабочих дерева.
5. Выполни `git worktree remove ../fix` и убедись, что список снова содержит одно дерево.

Ожидаемый результат: перед удалением `git worktree list` показывает два пути: основной и `../fix`; после `remove` — один.

### Задача 5
Разберись со стратегией pull. В репозитории с расхождением веток (как в задаче 2, пункты 1–3):

1. Выполни `git pull --ff-only` — зафиксируй, что Git отказывается (fast-forward невозможен).
2. Выполни `git pull` (обычный) — появится merge-коммит; посмотри `git log --oneline --graph -5`.
3. Выполни `git reset --hard origin/main`, затем `git pull --rebase` — история должна стать линейной.

Ожидаемый результат: ты можешь объяснить разницу трёх выводов и знаешь, когда какую стратегию выбрать.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Пути к bare-репозиторию: `git remote add origin ../project.git` работает, если папки рядом. `git push -u origin main` — первый push настраивает upstream. После `git fetch origin` сравнение логов покажет, синхронизированы ли ветки.

### Подсказка 2
`git clone origin bob` создаёт папку `bob`. Чтобы у `bob` был свой коммит `B`, измени файл и закоммить (без push). `alice` пушит `C`. Потом в `bob`: `git pull --rebase` — rebase `B` поверх `origin/main`, затем `git push`. Проверка линейности: `git log --oneline --graph main` — в первом столбце должны отсутствовать `|/`-вилки, порядок сообщений A, C, B.

### Подсказка 3
`git commit --amend` меняет последний коммит (новый хэш). `--force-with-lease` сравнивает локальную «картинку» `origin/main` с реальной; пока она не обновлена (`git fetch`), push отклоняется. Ожидаемый код: первая попытка — `returncode != 0`, вторая (после fetch) — 0.

### Подсказка 4
`git worktree add ../fix -b hotfix/fix` — относительный путь считается от текущей папки. Перед `git worktree remove ../fix` убедись, что в этой папке нет незакоммиченных изменений: иначе Git откажется. `git worktree list` покажет строки: `<путь к основному репо> <ветка>`, затем `../fix hotfix/fix`.

### Подсказка 5
При расхождении `--ff-only` откажется: fast-forward невозможен. Обычный `git pull` создаст merge-коммит (вилка в графе). После `git reset --hard origin/main` и `git pull --rebase` локальные коммиты переложатся поверх `origin/main` — граф станет линейным. Для возврата на состояние после задачи 2 используй `git log` для поиска нужных sha.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Команды:

```bash
git init --bare project.git

mkdir work && cd work
git init
git remote add origin ../project.git
git config user.name "Тест"
git config user.email "test@example.com"

echo v1 > f.txt && git add f.txt && git commit -m "v1"
echo v2 > f.txt && git add f.txt && git commit -m "v2"
git push -u origin main

echo v3 > f.txt && git add f.txt && git commit -m "v3"
git push origin main

git fetch origin
git log --oneline origin/main
git log --oneline main
```

Разбор: `--bare` создаёт репозиторий без рабочего дерева — он принимает только push/fetch. `git push -u origin main` отправляет ветку и записывает upstream (связь main → origin/main). `fetch` обновляет копии remote-веток; после него `origin/main` и `main` совпадают. Обрати внимание: fetch не меняет локальную ветку — если бы мы «уехали» вперёд, лог показал бы расхождение. Именно поэтому fetch безопасен: его можно делать в любой момент.

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


def test_pull_rebase_keeps_history_linear():
    with tempfile.TemporaryDirectory() as tmp:
        origin = str(Path(tmp) / "origin.git")
        alice = str(Path(tmp) / "alice")
        bob = str(Path(tmp) / "bob")
        git("init", "--bare", origin)

        Path(alice).mkdir()
        git("init", cwd=alice)
        git("config", "user.name", "Alice", cwd=alice)
        git("config", "user.email", "alice@example.com", cwd=alice)
        git("remote", "add", "origin", origin, cwd=alice)
        commit_file(alice, "f.txt", "A\n", "A")
        git("push", "-u", "origin", "main", cwd=alice)

        git("clone", origin, bob)
        git("config", "user.name", "Bob", cwd=bob)
        git("config", "user.email", "bob@example.com", cwd=bob)
        commit_file(bob, "f.txt", "A\nB\n", "B")

        commit_file(alice, "f.txt", "A\nC\n", "C")
        git("push", "origin", "main", cwd=alice)

        git("pull", "--rebase", cwd=bob)
        git("push", "origin", "main", cwd=bob)

        graph = git("log", "--oneline", "--graph", "main", cwd=bob).stdout
        assert "|/" not in graph and "/" not in graph.splitlines()[1:]
        messages = git("log", "--format=%s", "main", cwd=bob).stdout
        assert messages.splitlines() == ["B", "C", "A"]
```

Разбор: оба «разработчика» делают коммиты поверх одинакового состояния. Без rebase у `bob` после `git pull` появился бы merge-коммит и вилка. С `--rebase` коммит `B` перекладывается поверх `origin/main` (который содержит `C`), после чего push проходит как fast-forward. Проверки: в графе нет вилок, порядок сообщений сверху вниз B, C, A. Это точная модель утреннего «pull --rebase + push» в команде. Запуск: `pytest test_pull_rebase_linear.py -v` → `1 passed`.

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


def test_force_with_lease_protects_remote():
    with tempfile.TemporaryDirectory() as tmp:
        origin = str(Path(tmp) / "origin.git")
        alice = str(Path(tmp) / "alice")
        bob = str(Path(tmp) / "bob")
        git("init", "--bare", origin)

        Path(alice).mkdir()
        git("init", cwd=alice)
        git("config", "user.name", "Alice", cwd=alice)
        git("config", "user.email", "alice@example.com", cwd=alice)
        git("remote", "add", "origin", origin, cwd=alice)
        commit_file(alice, "f.txt", "A\n", "A")
        git("push", "-u", "origin", "main", cwd=alice)

        git("clone", origin, bob)
        git("config", "user.name", "Bob", cwd=bob)
        git("config", "user.email", "bob@example.com", cwd=bob)
        commit_file(bob, "f.txt", "A\nB\n", "B")
        git("push", "origin", "main", cwd=bob)

        commit_file(alice, "f.txt", "A\nA2\n", "A2")
        git("commit", "--amend", "-m", "A2", cwd=alice)

        first = git("push", "--force-with-lease", "origin", "main",
                    cwd=alice, check=False)
        assert first.returncode != 0

        git("fetch", "origin", cwd=alice)
        second = git("push", "--force-with-lease", "origin", "main",
                     cwd=alice, check=False)
        assert second.returncode == 0
```

Разбор: у `alice` локальная «картинка» `origin/main` — всё ещё `A` (она не делала fetch после push Bob-а). `--force-with-lease` сравнивает эту картинку с реальным remote и видит `B` — отказывается. После `git fetch` (буфер обновлён) принудительная отправка проходит. Именно так переписывают историю своей ветки в PR: сначала fetch, потом `--force-with-lease`, и чужая работа никогда не затирается молча. Запуск: `pytest test_force_with_lease.py -v` → `1 passed`.

### Разбор 4
Команды:

```bash
git checkout -b feature/pain
echo pain > pain.txt && git add pain.txt && git commit -m "pain"
git worktree add ../fix -b hotfix/fix
cd ../fix
echo fix > fix.txt && git add fix.txt && git commit -m "fix"
cd ../work
git worktree list
git worktree remove ../fix
git worktree list
```

Разбор: `git worktree add` создаёт новую рабочую копию (папку) и привязывает её к новой ветке. Основной репозиторий и `../fix` — независимые рабочие деревья одного репозитория: коммиты в любом из них видны обоим (общая история). `git worktree list` показывает все деревья. `remove` требует чистого рабочего дерева — если там есть изменения, Git откажется (тогда `git worktree remove --force`). Worktree незаменим, когда нужно срочно исправить баг на другой ветке, не пряча текущую работу.

### Разбор 5
Последовательность (продолжение задачи 2):

```bash
git pull --ff-only
# fatal: Not possible to fast-forward, aborting.
git pull
# Merge made by the 'ort' strategy.
git log --oneline --graph -5
# *   Merge branch 'main' ...
# |\
# | * C
# * | B
# |/
# * A
git reset --hard origin/main
git pull --rebase
git log --oneline --graph -5
# * B
# * C
# * A
```

Разбор: `--ff-only` — консервативная защита: если ветки разошлись, он отказывается, не делая ничего неожиданного. Обычный `pull` делает merge — в истории появляется «вилка» и merge-коммит; это ок для публичных веток, но засоряет личную историю. `pull --rebase` перекладывает локальные коммиты поверх чужих — история линейна, и это лучший выбор для фича-веток. `reset --hard origin/main` — вспомогательное действие, чтобы откатить merge и начать «чистый» эксперимент. Три стратегии — три разных результата, и выбор зависит от того, чья это ветка: личная → rebase, общая → merge или ff-only.
<!--/SOLUTION-->

<!--QUIZ-->
Что такое remote в Git?
- Именованная ссылка на другой репозиторий
- Папка с резервными копиями
- Ветка в локальном репозитории
- Специальный тип коммита
* Правильный ответ: Именованная ссылка на другой репозиторий
remote хранит адрес (обычно https/ssh) и позволяет обмениваться коммитами.

Что делает git fetch?
- Скачивает объекты и ветки с remote, не трогая локальные ветки
- Немедленно сливает remote-ветку с локальной
- Отправляет локальные коммиты в remote
- Удаляет remote
* Правильный ответ: Скачивает объекты и ветки с remote, не трогая локальные ветки
После fetch обновляются только origin/*; локальные ветки остаются как были.

Что делает git pull --rebase?
- fetch + rebase локальных коммитов поверх origin
- fetch + merge
- Только fetch
- push + merge
* Правильный ответ: fetch + rebase локальных коммитов поверх origin
Локальные коммиты перекладываются поверх свежих чужих — история остаётся линейной.

Что делает git pull --ff-only?
- Отказывается, если fast-forward невозможен
- Всегда создаёт merge-коммит
- Удаляет локальные коммиты
- Принудительно переписывает историю
* Правильный ответ: Отказывается, если fast-forward невозможен
Если ветки разошлись, --ff-only аварийно останавливается, ничего не меняя.

Что делает -u в git push -u origin main?
- Устанавливает upstream: связь ветки с origin/main
- Отправляет принудительно
- Отправляет все ветки
- Создаёт remote
* Правильный ответ: Устанавливает upstream: связь ветки с origin/main
После -u дальнейшие git push работают без указания remote и ветки.

Чем --force-with-lease отличается от --force?
- Он сначала проверяет, что remote-ветка не менялась с последнего fetch
- Он работает только с bare-репозиториями
- Он не позволяет переписывать историю вообще
- Он требует явного подтверждения
* Правильный ответ: Он сначала проверяет, что remote-ветка не менялась с последнего fetch
Если кто-то успел запушить, --force-with-lease откажется, а голый --force затрёт чужую работу.

Что произойдёт при git push, если в remote есть коммиты, которых нет локально?
- Push откажется (не fast-forward)
- Push пройдёт с merge
- Push удалит чужие коммиты
- Push создаст новую ветку
* Правильный ответ: Push откажется (не fast-forward)
Обычный push требует fast-forward; иначе — отказ с подсказкой про force.

Что создаёт git worktree add ../fix -b hotfix/fix?
- Новую рабочую копию на новой ветке
- Клон целого репозитория
- Bare-репозиторий
- Новый remote
* Правильный ответ: Новую рабочую копию на новой ветке
Worktree добавляет ещё одно рабочее дерево того же репозитория на указанной ветке.

Как посмотреть все рабочие деревья?
- git worktree list
- git branch --trees
- git show --worktrees
- git trees --all
* Правильный ответ: git worktree list
Команда выводит пути и ветки всех рабочих деревьев.

Какой порядок действий правилен перед push фича-ветки после долгой работы?
- git pull --rebase origin main, затем push
- git push, затем pull
- git commit --amend, затем push --force
- git fetch только
* Правильный ответ: git pull --rebase origin main, затем push
Сначала синхронизируйся с main (rebase), чтобы история была линейной, потом пуши.
<!--/QUIZ-->
