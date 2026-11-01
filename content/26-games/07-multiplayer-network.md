---
title: Сетевая игра: клиент-сервер
summary: Пишем сетевую игру: сокеты TCP, сервер на selectors, сообщения JSON, клиент на pygame, обработка отключений и реконнектов.
order: 7
duration: 90 мин
difficulty: advanced
tags: сеть, socket, pygame, мультиплеер
---

Привет! Ты добрался до самого коварного раздела курса — сетей. До сих пор все твои игры жили внутри одного процесса: спрайты, события, логика — всё в одной программе. Но настоящие многопользовательские игры устроены иначе. У них есть **сервер** — программа, которая хранит состояние мира и решает, что в нём происходит, — и **клиенты** — программы на компьютерах игроков, которые показывают мир и собирают нажатия клавиш. Игра превращается в распределённую систему, и вся сложность переезжает в передачу данных по сети.

## Сокеты: фундамент сетевых программ

**Сокет** (socket) — это «дверь» в сеть: интерфейс, через который программа отправляет и получает байты. В Python сокет создаётся одной строкой:

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

`AF_INET` означает, что мы работаем по протоколу IPv4, а `SOCK_STREAM` — что используем **TCP**: надёжный потоковый протокол. Адрес сокета — пара «IP-адрес + порт». Сервер **привязывается** к адресу (`bind`), начинает **слушать** (`listen`), затем **принимает** входящие соединения (`accept`). Клиент **подключается** (`connect`). После установки соединения обе стороны обмениваются данными через `send`/`recv`.

Вот минимальный эхо-сервер, который принимает одно соединение и возвращает каждую строку обратно:

```python
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("127.0.0.1", 5555))
server.listen(1)
print("Сервер запущен на 127.0.0.1:5555")

conn, addr = server.accept()
print("Подключился:", addr)

while True:
    data = conn.recv(1024)
    if not data:
        break
    print("Получено:", data.decode("utf-8"))
    conn.sendall(data)

conn.close()
server.close()
```

`127.0.0.1` — это «сам себе» (loopback). Клиент:

```python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5555))
client.sendall("Привет, сервер!".encode("utf-8"))
answer = client.recv(1024)
print("Ответ:", answer.decode("utf-8"))
client.close()
```

Обрати внимание: по сети передаются **байты**, поэтому строки кодируются через `.encode("utf-8")` и раскодируются через `.decode("utf-8")`. `recv(1024)` читает не «строку», а кусок потока размером до 1024 байт — разделять сообщения придётся нам самим.

## TCP против UDP

`SOCK_STREAM` — TCP, а `SOCK_DGRAM` — UDP. Это две главные модели транспорта.

| Свойство | TCP | UDP |
|---|---|---|
| Доставка | гарантированная, с повторами | без гарантий, «выстрелил и забыл» |
| Порядок | строго соблюдается | может нарушаться |
| Соединение | устанавливается до передачи | не устанавливается |
| Скорость | ниже (накладные расходы) | выше |
| Применение | игры, чаты, HTTP, файлы | стриминг, VoIP, быстрые аркады |

Пакет UDP — это независимый датаграмма: `sendto`/`recvfrom`, без `connect`/`accept`. Для нашего урока берём TCP: он проще в отладке и не «теряет» ходы в игре.

## Много клиентов: selectors

Проблема эхо-сервера: `accept()` и `recv()` **блокируют** поток — пока сервер ждёт данных от одного клиента, остальные стоят в очереди. Решение — неблокирующие сокеты и мультиплексирование через модуль `selectors`: мы регистрируем все сокеты, а функция `select()` сообщает, какие из них готовы к чтению.

```python
import selectors
import socket

class RelayServer:
    """Ретранслятор: пересылает каждую строку всем остальным клиентам."""

    def __init__(self, host="127.0.0.1", port=5555):
        self.sel = selectors.DefaultSelector()
        self.conns = {}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen()
        self.server.setblocking(False)
        self.sel.register(self.server, selectors.EVENT_READ, self._accept)

    def _accept(self, sock):
        conn, addr = sock.accept()
        conn.setblocking(False)
        self.conns[conn] = addr
        self.sel.register(conn, selectors.EVENT_READ, self._read)
        print("Подключился:", addr)

    def _read(self, conn):
        try:
            data = conn.recv(4096)
        except OSError:
            data = b""
        if data:
            for other in self.conns:
                if other is not conn and other.fileno() != -1:
                    try:
                        other.sendall(data)
                    except OSError:
                        pass
        else:
            self.sel.unregister(conn)
            conn.close()
            self.conns.pop(conn, None)
            print("Клиент отключился")

    def run(self):
        while True:
            for key, _ in self.sel.select():
                key.data(key.fileobj)

if __name__ == "__main__":
    RelayServer().run()
```

`select()` возвращает список «событий»; для каждого мы вызываем обработчик — `_accept` для слушающего сокета и `_read` для клиентского. Так один поток обслуживает сотни соединений.

## Сериализация сообщений: JSON

По сети ходят байты, а нам нужны структуры данных. **Сериализация** — превращение объекта в байты и обратно. Удобный формат — JSON: он встроен в Python, читается людьми и любым другим языком.

Договоримся о простом протоколе: **каждое сообщение — одна строка JSON, завершающаяся переносом строки `\n`**. Перенос — это разделитель, позволяющий понять, где заканчивается одно сообщение и начинается следующее.

```python
import json

def encode_message(obj):
    """Объект -> байты JSON с символом переноса строки."""
    return json.dumps(obj, ensure_ascii=False).encode("utf-8") + b"\n"

def decode_messages(buffer):
    """Разбирает буфер на список сообщений; возвращает (сообщения, остаток)."""
    messages = []
    while True:
        line, sep, rest = buffer.partition(b"\n")
        if not sep:
            break
        messages.append(json.loads(line.decode("utf-8")))
        buffer = rest
    return messages, buffer
```

Почему именно `partition` и «остаток»? Потому что `recv()` может принести кусок сообщения или сразу несколько. Функция возвращает неразобранный хвост, и сервер хранит его между вызовами. Такой паттерн называется **буферизация потока**.

## Серверная логика игры

В многопользовательской игре сервер — **авторитетный**: он один хранит состояние мира, и клиенты лишь присылают свои намерения (куда двигаться), а сервер решает, что произошло на самом деле. Это защищает от читерства и даёт всем игрокам один и тот же мир.

Напишем логику простой игры «Ловец монет»: игроки двигаются по арене, монета появляется в случайном месте, и тот, кто дотронулся до неё, получает очко — а монета появляется заново.

```python
import math
import random

ARENA_W, ARENA_H = 800, 600
PLAYER_RADIUS = 15
COIN_RADIUS = 20

class Game:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)   # seed делает игру детерминированной
        self.players = {}
        self.coin = self._spawn_coin()
        self.next_id = 1

    def _spawn_coin(self):
        return {"x": round(self.rng.uniform(0, ARENA_W), 1),
                "y": round(self.rng.uniform(0, ARENA_H), 1)}

    def handle_join(self, name):
        pid = self.next_id
        self.next_id += 1
        self.players[pid] = {"name": name or "Аноним",
                             "x": round(self.rng.uniform(0, ARENA_W), 1),
                             "y": round(self.rng.uniform(0, ARENA_H), 1),
                             "score": 0}
        return pid

    def handle_move(self, pid, x, y):
        player = self.players.get(pid)
        if player is None:
            return False
        # ограничиваем координаты ареной:
        # клиент не может «убежать» за границы мира
        player["x"] = max(0.0, min(float(x), ARENA_W))
        player["y"] = max(0.0, min(float(y), ARENA_H))
        dx = player["x"] - self.coin["x"]
        dy = player["y"] - self.coin["y"]
        if math.hypot(dx, dy) < PLAYER_RADIUS + COIN_RADIUS:
            player["score"] += 1
            self.coin = self._spawn_coin()
        return True

    def handle_quit(self, pid):
        return self.players.pop(pid, None) is not None

    def snapshot(self):
        return {"players": [{"id": pid, **p} for pid, p in self.players.items()],
                "coin": self.coin}
```

Обрати внимание на детали: `seed` для `random.Random` делает поведение воспроизводимым (это спасёт нас при написании тестов), а координаты округляются, чтобы JSON был компактнее. Игровой сервер объединяет эту логику с сетевым слоем на `selectors`: на `join` — создаёт игрока и шлёт `welcome` + рассылку состояния, на `move` — обновляет позицию и рассылает новое состояние всем, на разрыв соединения — удаляет игрока и уведомляет остальных. Структуру такого сервера ты соберёшь в задаче 4.

## Клиент на pygame

Клиент живёт в обычном игровом цикле pygame. Ключевой приём — **неблокирующий сокет**: `settimeout(0.0)` заставляет `recv()` мгновенно возвращать управление, если данных нет, вместо того чтобы замораживать игру. Тогда цикл выглядит так: обработали события (window close, клавиши) → попробовали прочитать входящие сообщения → отправили своё намерение → отрисовали кадр.

```python
import json
import socket
import pygame

HOST, PORT = "127.0.0.1", 5555
W, H = 800, 600

class Net:
    def __init__(self):
        self.sock = None
        self.my_id = None
        self.players = {}
        self.coin = None

    def connect_and_join(self, name):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2.0)
        sock.connect((HOST, PORT))
        sock.settimeout(0.0)                 # дальше — неблокирующий режим
        sock.sendall(json.dumps({"type": "join", "name": name},
                                ensure_ascii=False).encode("utf-8") + b"\n")
        self.sock = sock

    def update(self):
        if self.sock is None:
            return
        try:
            data = self.sock.recv(4096)
        except BlockingIOError:
            return                              # данных пока нет — не проблема
        except OSError:
            self.drop()
            return
        if not data:
            self.drop()                         # сервер закрыл соединение
            return
        for line in data.split(b"\n"):
            if not line:
                continue
            msg = json.loads(line.decode("utf-8"))
            kind = msg["type"]
            if kind == "welcome":
                self.my_id = msg["id"]
                self.players = {p["id"]: p for p in msg["players"]}
                self.coin = msg["coin"]
            elif kind == "state":
                self.players = {p["id"]: p for p in msg["players"]}
                self.coin = msg["coin"]

    def send_move(self, x, y):
        if self.sock is None:
            return
        try:
            self.sock.sendall(json.dumps({"type": "move", "x": x, "y": y})
                              .encode("utf-8") + b"\n")
        except OSError:
            self.drop()

    def drop(self):
        if self.sock is not None:
            self.sock.close()
            self.sock = None
            self.my_id = None
```

Урок здесь такой: сеть никогда не останавливает игру. Если данных нет — рисуем следующий кадр; если соединение порвалось — переходим в режим переподключения.

## Обработка отключений и реконнектов

Отключение видно по `recv()`, вернувшему `b""` (противоположная сторона закрыла соединение), или по исключению `ConnectionResetError`/`BrokenPipeError` при отправке. Сервер должен немедленно освободить ресурсы: `unregister`, `close`, удалить игрока из состояния и разослать обновлённое состояние — иначе «мёртвые» клиенты навсегда зависнут в его памяти, а игроки будут видеть призраков.

Клиент же должен **переживать** разрыв. Схема реконнекта:

1. Заметили разрыв → `drop()`, ставим флаг «не подключены».
2. В игровом цикле раз в несколько секунд пробуем `connect_and_join()` заново.
3. При успехе — отправляем `join` ещё раз (он идемпотентен: сервер просто создаст нового игрока), и игра продолжается.
4. Между попытками — **бэкфф**: пауза, которая растёт с каждой неудачей (2 с, 4 с, 8 с…), чтобы не долбить сервер при его отсутствии.

```python
import time

last_attempt = 0.0
while True:
    if net.sock is None:
        now = time.monotonic()
        if now - last_attempt > 2.0:
            last_attempt = now
            try:
                net.connect_and_join("Витя")
                print("Подключено!")
            except OSError:
                print("Сервер недоступен, пробуем снова...")
    # ... игровой цикл: update(), отрисовка, обработка событий ...
```

Теперь закрепим теорию на практике — от эхо-сервера до полноценной сетевой игры с тестами.

<!--TASK-->
### Задача 1
Создай два файла: `echo_server.py` и `echo_client.py`. Сервер должен привязываться к адресу `127.0.0.1:5555`, принимать ровно одно соединение, затем в цикле читать данные через `recv(1024)` и отправлять их обратно с помощью `sendall`, пока клиент не закроет соединение. Клиент должен подключиться, отправить по очереди три сообщения: `Привет!`, `Эхо-сервер работает` и `Пока!`, после каждого — дождаться ответа и напечатать его в формате `Ответ: ...`. Запусти сначала сервер, затем клиент. Ожидаемый вывод клиента:

```
Ответ: Привет!
Ответ: Эхо-сервер работает
Ответ: Пока!
```

Убедись, что сервер печатает каждое полученное сообщение и корректно завершается после закрытия соединения.

### Задача 2
Напиши многопользовательский чат-ретранслятор. Сервер `relay_server.py` на `selectors` должен принимать неограниченное число клиентов и пересылать каждую полученную строку всем остальным подключённым клиентам (включая и не отправляя обратно отправителю). Клиент `relay_client.py` должен работать в двух «нитях»: отдельный поток читает входящие сообщения из сокета и печатает их, а главный поток через `input()` читает строки с клавиатуры и отправляет их на сервер. Команда `/exit` — завершает клиент. Проверь работу на двух одновременно запущенных клиентах: строка, введённая в одном окне, должна появиться в другом. В коде используй реальные API `selectors.DefaultSelector`, `register`/`unregister`, `EVENT_READ`.

### Задача 3
Создай модуль `protocol.py` с двумя функциями: `encode_message(obj)` — превращает объект в байты JSON с завершающим `\n` (параметр `ensure_ascii=False`), и `decode_messages(buffer)` — принимает буфер байтов и возвращает кортеж `(messages, rest)`, где `messages` — список разобранных сообщений, а `rest` — неразобранный остаток. Затем создай файл тестов `test_protocol.py` с использованием pytest и напиши минимум пять тестов: (1) круговая проверка «закодировали — раскодировали — получили тот же dict»; (2) кириллица в имени не ломается; (3) несколько сообщений в одном буфере разбираются по одному; (4) неполное сообщение без `\n` остаётся в остатке, а сообщений не возвращается; (5) битый JSON вызывает `json.JSONDecodeError`. Запусти `python -m pytest test_protocol.py -v` — все тесты должны пройти.

### Задача 4
Напиши игровой сервер «Ловец монет» и тесты к нему через настоящие сокеты. Создай `game.py` (класс `Game` из теории) и `gameserver.py` — сервер на `selectors`, который: на `join` создаёт игрока, шлёт ему `welcome` (с `id`, `players`, `coin`) и рассылает `state` всем; на `move` обновляет позицию и рассылает `state`; при закрытии соединения удаляет игрока и рассылает обновлённый `state`; на битый JSON отвечает сообщением `{"type": "error", ...}`. Затем напиши `test_gameserver.py` на pytest: поднимай сервер в фоновом потоке на порту `0` (эфимерный порт), подключайся обычными сокетами и проверяй: (1) после `join` приходит `welcome` с верным `id` и одним игроком; (2) если двинуться точно в монету, счёт игрока станет 1; (3) битый JSON приводит к сообщению `error`; (4) после закрытия соединения одного из двух игроков второй получает `state` с одним игроком; (5) движение за границы арены «зажимается» внутри неё.

### Задача 5
Напиши полностью играбельный клиент `client.py` на pygame для игры «Ловец монет». Клиент подключается к серверу из задачи 4: при старте отправляет `join`, затем каждый кадр отправляет `move` с координатами курсора мыши. Рисуй арену 800×600: монету жёлтым кругом, своего игрока синим, чужих — красным; сверху слева выводи счёт всех игроков. Ключевое требование: обработай обрыв связи — если сокет закрылся или произошла ошибка, клиент не должен падать, а каждые 2 секунды должен пытаться переподключиться (реконнект) и снова отправлять `join`; при успехе печатай `Подключено!` и продолжай игру. Закрытие окна — штатный выход с корректным закрытием сокета.

<!--/TASK-->

<!--HINT-->
### Подсказка 1
Не забудь, что по сети ходят байты: кодируй строки через `.encode("utf-8")`, а полученные байты раскодируй через `.decode("utf-8")`. Условие выхода из цикла сервера — `if not data: break`, ведь при закрытии соединения `recv()` возвращает пустые байты `b""`. Перед повторным запуском сервера, если порт занят, используй `setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)` — это позволит сразу перезапустить сервер.

### Подсказка 2
Сервер хранит словарь `self.conns` со всеми клиентскими сокетами: в `_accept` добавляй новое соединение, в `_read` при `data` рассылай её всем, кроме отправителя, а при `not data` делай `sel.unregister(conn)`, `conn.close()` и удаляй из словаря. В клиенте функция потока чтения должна иметь цикл `while True` с `recv` (остановка, когда `recv` вернёт пустые байты); запускай её как `threading.Thread(..., daemon=True)`, чтобы поток не мешал завершению программы.

### Подсказка 3
Помни про сигнатуру: `decode_messages` должна возвращать кортеж `(messages, rest)` — это нужно, чтобы сервер мог хранить остаток между приходами данных. Для теста неполного сообщения нарежь закодированное сообщение срезом `[:10]` — без `\n` оно не должно разбираться. Битый JSON проще всего получить так: `b"{this is not json}\n"`, а для проверки исключения используй `pytest.raises(json.JSONDecodeError)` с `import json`.

### Подсказка 4
Логику и сеть нужно тестировать по-разному. Для сетевых тестов поднимай сервер порту `0`: после `start()` читай реальный порт из `server.port`. Напиши помощник `receive_messages(sock, buffer)`, который копит байты, пока не наберётся хотя бы одно полное сообщение (по `\n`), и возвращает список сообщений и остаток — он понадобится, потому что `welcome` и `state` приходят вперемешку. В тесте «монета собрана» двигай игрока точно в координаты монеты из `welcome` (расстояние станет нулевым — сбор гарантирован). Детерминированность обеспечь seed'ом: `GameServer(seed=42)`.

### Подсказка 5
Неблокирующий режим: после `connect` вызови `sock.settimeout(0.0)`, а `recv` оберни в `try/except BlockingIOError` — это и есть «данных нет». Для реконнекта храни время последней попытки (`time.monotonic()`) и, если `net.sock is None` и прошло минимум 2 секунды, пробуй `connect_and_join()` снова. Не забудь, что `pygame.mouse.get_pos()` возвращает координаты курсора, а для вывода счёта используй `pygame.font.SysFont(None, 28)` и `render(...)`.

<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Файл `echo_server.py`:

```python
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("127.0.0.1", 5555))
server.listen(1)
print("Сервер запущен на 127.0.0.1:5555")

conn, addr = server.accept()
print("Подключился:", addr)

while True:
    data = conn.recv(1024)
    if not data:
        break
    print("Получено:", data.decode("utf-8"))
    conn.sendall(data)

conn.close()
server.close()
print("Сервер завершил работу")
```

Файл `echo_client.py`:

```python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5555))

for message in ["Привет!", "Эхо-сервер работает", "Пока!"]:
    client.sendall(message.encode("utf-8"))
    answer = client.recv(1024)
    print("Ответ:", answer.decode("utf-8"))

client.close()
```

Разберём по шагам. Сервер создаёт сокет, привязывается к адресу и начинает слушать. `accept()` блокирует программу, пока не придёт клиент, и возвращает пару `(conn, addr)` — отдельный сокет для общения именно с этим клиентом и его адрес. Дальше цикл: `recv(1024)` читает до 1024 байт. Когда клиент закрывает соединение, `recv()` возвращает `b""` — пустой объект, который считается ложным, поэтому `if not data: break` завершает цикл. Важно, что текст кодируется в байты UTF-8 (`encode`) и раскодируется обратно (`decode`). `sendall` гарантирует отправку всех байтов (в отличие от `send`, который может отправить лишь часть). Порядок запуска: сначала сервер, потом клиент; иначе клиент получит `ConnectionRefusedError`.

### Разбор 2
Файл `relay_server.py`:

```python
import selectors
import socket

class RelayServer:
    def __init__(self, host="127.0.0.1", port=5555):
        self.sel = selectors.DefaultSelector()
        self.conns = {}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen()
        self.server.setblocking(False)
        self.sel.register(self.server, selectors.EVENT_READ, self._accept)

    def _accept(self, sock):
        conn, addr = sock.accept()
        conn.setblocking(False)
        self.conns[conn] = addr
        self.sel.register(conn, selectors.EVENT_READ, self._read)
        print("Подключился:", addr)

    def _read(self, conn):
        try:
            data = conn.recv(4096)
        except OSError:
            data = b""
        if data:
            for other in self.conns:
                if other is not conn:
                    try:
                        other.sendall(data)
                    except OSError:
                        pass
        else:
            self.sel.unregister(conn)
            conn.close()
            self.conns.pop(conn, None)
            print("Клиент отключился")

    def run(self):
        while True:
            for key, _ in self.sel.select():
                key.data(key.fileobj)

if __name__ == "__main__":
    RelayServer().run()
```

Файл `relay_client.py`:

```python
import socket
import threading

def read_loop(sock):
    while True:
        try:
            data = sock.recv(4096)
        except OSError:
            break
        if not data:
            break
        print(data.decode("utf-8"), end="")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 5555))
threading.Thread(target=read_loop, args=(sock,), daemon=True).start()

try:
    while True:
        line = input("Вы: ")
        if line == "/exit":
            break
        sock.sendall((line + "\n").encode("utf-8"))
finally:
    sock.close()
```

Суть решения — вынос блокирующих операций из одного потока. Сервер делает сокеты неблокирующими и передаёт их под надзор `selectors`: `select()` каждую итерацию говорит, какие сокеты готовы к чтению. Готов слушающий сокет — значит, пришёл новый клиент (`_accept`). Готов клиентский — значит, есть данные (`_read`). В `_read` данные рассылаются всем остальным соединениям, а при `b""` сокет снимается с регистрации и закрывается — это и есть корректная обработка отключения. В клиенте поток чтения занимается только `recv` и печатью, а главный поток — только `input()` и отправкой. `daemon=True` важен: поток-демон умрёт вместе с главным потоком, не заблокировав выход из программы.

### Разбор 3
Файл `protocol.py`:

```python
import json

def encode_message(obj):
    return json.dumps(obj, ensure_ascii=False).encode("utf-8") + b"\n"

def decode_messages(buffer):
    messages = []
    while True:
        line, sep, rest = buffer.partition(b"\n")
        if not sep:
            break
        messages.append(json.loads(line.decode("utf-8")))
        buffer = rest
    return messages, buffer
```

Файл `test_protocol.py`:

```python
import json
import pytest
from protocol import encode_message, decode_messages

def test_round_trip():
    msg = {"type": "move", "x": 12.5, "y": -3.0}
    messages, rest = decode_messages(encode_message(msg))
    assert messages == [msg]
    assert rest == b""

def test_cyrillic_preserved():
    messages, _ = decode_messages(encode_message({"type": "join", "name": "Витя"}))
    assert messages[0]["name"] == "Витя"

def test_several_messages_in_one_buffer():
    buf = encode_message({"type": "a"}) + encode_message({"type": "b"})
    messages, rest = decode_messages(buf)
    assert [m["type"] for m in messages] == ["a", "b"]
    assert rest == b""

def test_partial_message_left_in_buffer():
    buf = encode_message({"type": "a"})[:10]
    messages, rest = decode_messages(buf)
    assert messages == []
    assert rest == buf

def test_bad_json_raises():
    with pytest.raises(json.JSONDecodeError):
        decode_messages(b"{this is not json}\n")

def test_newline_terminated():
    raw = encode_message({"type": "move", "x": 1, "y": 2})
    assert raw.endswith(b"\n")
    assert json.loads(raw[:-1])["type"] == "move"
```

Почему это работает? `encode_message` превращает dict в строку JSON без экранирования кириллицы (`ensure_ascii=False`) и добавляет `\n` — разделитель сообщений. `decode_messages` использует `partition(b"\n")`, который всегда возвращает кортеж из трёх частей: текст до разделителя, сам разделитель и остаток. Если разделителя нет (`sep == b""`), значит, сообщение неполное — выходим и возвращаем остаток. Это ключевой приём для потоковой передачи: `recv()` не обязан приносить сообщение целиком или ровно по одному за раз. Тесты проверяют все важные обещания контракта: круговая проверка, выживание кириллицы, пакетирование нескольких сообщений, неполный хвост и реакция на мусор. Запуск: `python -m pytest test_protocol.py -v`. Обрати внимание, что тесты не требуют сети — они проверяют чистую логику, и это правильный подход: чем больше проверено без сети, тем меньше сюрпризов в сетевых тестах.

### Разбор 4
Файл `game.py` — класс `Game` из теории (полный код приведён в разделе «Серверная логика игры»). Файл `gameserver.py`:

```python
import json
import selectors
import socket
import threading
import time

from game import Game

class GameServer:
    def __init__(self, host="127.0.0.1", port=5555, seed=None):
        self.game = Game(seed=seed)
        self.host = host
        self.port = port
        self.sel = selectors.DefaultSelector()
        self.sockets = set()
        self.buffers = {}
        self.player_ids = {}
        self._thread = None
        self._running = False
        self.server = None

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.port = self.server.getsockname()[1]   # реальный порт (важно при port=0)
        self.server.listen()
        self.server.setblocking(False)
        self.sel.register(self.server, selectors.EVENT_READ, self._accept)
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=1.0)
        self.sel.close()
        if self.server is not None:
            try:
                self.server.close()
            except OSError:
                pass
        for sock in list(self.sockets):
            try:
                sock.close()
            except OSError:
                pass

    def _loop(self):
        while self._running:
            try:
                events = self.sel.select(timeout=0.1)
            except OSError:
                break
            for key, _ in events:
                key.data(key.fileobj)

    def _accept(self, sock):
        conn, _ = sock.accept()
        conn.setblocking(False)
        self.sel.register(conn, selectors.EVENT_READ, self._read)
        self.sockets.add(conn)
        self.buffers[conn] = b""

    def _send(self, conn, obj):
        payload = json.dumps(obj, ensure_ascii=False).encode("utf-8") + b"\n"
        try:
            conn.sendall(payload)
        except OSError:
            self._drop(conn)

    def _broadcast(self, obj):
        for conn in list(self.sockets):
            self._send(conn, obj)

    def _read(self, conn):
        try:
            data = conn.recv(4096)
        except OSError:
            data = b""
        if not data:
            self._drop(conn)
            return
        self.buffers[conn] += data
        while True:
            line, sep, rest = self.buffers[conn].partition(b"\n")
            if not sep:
                break
            self.buffers[conn] = rest
            try:
                msg = json.loads(line.decode("utf-8"))
            except ValueError:
                self._send(conn, {"type": "error", "message": "Не удалось разобрать JSON"})
                continue
            self._handle(conn, msg)

    def _handle(self, conn, msg):
        mtype = msg.get("type")
        if mtype == "join":
            pid = self.game.handle_join(msg.get("name"))
            self.player_ids[conn] = pid
            self._send(conn, {"type": "welcome", "id": pid, **self.game.snapshot()})
            self._broadcast_state()
        elif mtype == "move":
            pid = self.player_ids.get(conn)
            if pid is not None:
                self.game.handle_move(pid, msg.get("x", 0), msg.get("y", 0))
                self._broadcast_state()
        elif mtype == "quit":
            self._drop(conn)

    def _drop(self, conn):
        try:
            self.sel.unregister(conn)
        except Exception:
            pass
        self.sockets.discard(conn)
        self.buffers.pop(conn, None)
        pid = self.player_ids.pop(conn, None)
        if pid is not None:
            self.game.handle_quit(pid)
            self._broadcast_state()
        try:
            conn.close()
        except OSError:
            pass

    def _broadcast_state(self):
        self._broadcast({"type": "state", **self.game.snapshot()})

if __name__ == "__main__":
    srv = GameServer()
    srv.start()
    print("Сервер запущен, ждём игроков... (Ctrl+C для остановки)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        srv.stop()
```

Файл `test_gameserver.py`:

```python
import json
import socket
import pytest

from gameserver import GameServer

def make_connection(server):
    return socket.create_connection(("127.0.0.1", server.port), timeout=2)

def receive_messages(sock, buffer, limit=20):
    messages = []
    for _ in range(limit):
        while b"\n" in buffer:
            line, _, buffer = buffer.partition(b"\n")
            messages.append(json.loads(line.decode("utf-8")))
        if messages:
            return messages, buffer
        chunk = sock.recv(4096)
        if not chunk:
            raise RuntimeError("Соединение закрыто")
        buffer += chunk
    raise TimeoutError("Не дождались сообщений")

def send(sock, obj):
    sock.sendall(json.dumps(obj, ensure_ascii=False).encode("utf-8") + b"\n")

@pytest.fixture
def server():
    srv = GameServer(port=0, seed=42)
    srv.start()
    yield srv
    srv.stop()

def test_join_returns_welcome(server):
    sock = make_connection(server)
    send(sock, {"type": "join", "name": "Витя"})
    messages, _ = receive_messages(sock, b"")
    welcome = next(m for m in messages if m["type"] == "welcome")
    assert welcome["id"] == 1
    assert welcome["players"][0]["name"] == "Витя"
    sock.close()

def test_pick_up_coin_increases_score(server):
    sock = make_connection(server)
    send(sock, {"type": "join", "name": "Витя"})
    messages, buffer = receive_messages(sock, b"")
    welcome = next(m for m in messages if m["type"] == "welcome")
    coin = welcome["coin"]
    send(sock, {"type": "move", "x": coin["x"], "y": coin["y"]})
    for _ in range(10):
        messages, buffer = receive_messages(sock, buffer)
        states = [m for m in messages if m["type"] == "state"]
        if any(s["players"][0]["score"] == 1 for s in states):
            break
    else:
        pytest.fail("Монета не была собрана")
    sock.close()

def test_garbage_json_causes_error(server):
    sock = make_connection(server)
    sock.sendall(b"{this is not json}\n")
    messages, _ = receive_messages(sock, b"")
    assert any(m["type"] == "error" for m in messages)
    sock.close()

def test_disconnect_removes_player(server):
    sock1 = make_connection(server)
    send(sock1, {"type": "join", "name": "Первый"})
    receive_messages(sock1, b"")
    sock2 = make_connection(server)
    send(sock2, {"type": "join", "name": "Второй"})
    messages, buffer = receive_messages(sock2, b"")
    assert any(len(m["players"]) == 2 for m in messages if m["type"] == "state")
    sock1.close()
    for _ in range(20):
        messages, buffer = receive_messages(sock2, buffer)
        if any(m["type"] == "state" and len(m["players"]) == 1 for m in messages):
            break
    else:
        pytest.fail("Отключение игрока не обработано")
    sock2.close()

def test_move_outside_arena_is_clamped(server):
    sock = make_connection(server)
    send(sock, {"type": "join", "name": "Витя"})
    messages, buffer = receive_messages(sock, b"")
    send(sock, {"type": "move", "x": 99999, "y": -99999})
    for _ in range(10):
        messages, buffer = receive_messages(sock, buffer)
        states = [m for m in messages if m["type"] == "state"]
        if states:
            player = states[-1]["players"][0]
            assert player["x"] == 800
            assert player["y"] == 0
            break
    else:
        pytest.fail("Не получили state после move")
    sock.close()
```

Это и есть тесты серверной логики через настоящие сокеты. Ключевые решения: порт `0` заставляет ОС выбрать свободный порт, а после `start()` мы читаем его из `server.port`, — значит, тесты не конфликтуют ни с чем на машине. `seed=42` делает позиции игроков и монеты фиксированными, поэтому тест «собрал монету» детерминирован: мы движемся точно в координаты монеты, расстояние ноль — сбор гарантирован. Помощник `receive_messages` имитирует реальное сетевое поведение: сообщения приходят пачками и вперемешку (`welcome` + `state`), поэтому мы копим буфер и вытаскиваем по `\n`. Сервер запускается в потоке-демоне, а фикстура гарантирует остановку даже при падении теста. Тест отключения закрывает сокет `sock1` и ждёт, пока `sock2` увидит `state` с одним игроком, — так проверяется, что сервер не оставляет «призраков». Запуск: `python -m pytest test_gameserver.py -v`.

### Разбор 5
Файл `client.py`:

```python
import json
import socket
import time

import pygame

HOST, PORT = "127.0.0.1", 5555
W, H = 800, 600
PLAYER_COLOR = (60, 120, 255)
OTHERS_COLOR = (230, 80, 80)
COIN_COLOR = (255, 200, 50)
BG_COLOR = (20, 20, 30)

class Net:
    def __init__(self):
        self.sock = None
        self.my_id = None
        self.players = {}
        self.coin = None

    def connect_and_join(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2.0)
        sock.connect((HOST, PORT))
        sock.settimeout(0.0)
        sock.sendall(json.dumps({"type": "join", "name": "Витя"},
                                ensure_ascii=False).encode("utf-8") + b"\n")
        self.sock = sock

    def update(self):
        if self.sock is None:
            return
        try:
            data = self.sock.recv(4096)
        except BlockingIOError:
            return
        except OSError:
            self.drop()
            return
        if not data:
            self.drop()
            return
        for line in data.split(b"\n"):
            if not line:
                continue
            try:
                msg = json.loads(line.decode("utf-8"))
            except ValueError:
                continue
            kind = msg["type"]
            if kind == "welcome":
                self.my_id = msg["id"]
                self.players = {p["id"]: p for p in msg["players"]}
                self.coin = msg["coin"]
            elif kind == "state":
                self.players = {p["id"]: p for p in msg["players"]}
                self.coin = msg["coin"]

    def send_move(self, x, y):
        if self.sock is None:
            return
        try:
            self.sock.sendall(json.dumps({"type": "move", "x": x, "y": y})
                              .encode("utf-8") + b"\n")
        except OSError:
            self.drop()

    def drop(self):
        if self.sock is not None:
            try:
                self.sock.close()
            except OSError:
                pass
            self.sock = None
            self.my_id = None

def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Ловец монет")
    font = pygame.font.SysFont(None, 28)
    clock = pygame.time.Clock()

    net = Net()
    last_attempt = 0.0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if net.sock is None:
            now = time.monotonic()
            if now - last_attempt > 2.0:
                last_attempt = now
                try:
                    net.connect_and_join()
                    print("Подключено!")
                except OSError:
                    print("Сервер недоступен, пробуем снова...")
        else:
            net.update()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            net.send_move(mouse_x, mouse_y)

        screen.fill(BG_COLOR)
        if net.coin is not None:
            pygame.draw.circle(screen, COIN_COLOR,
                               (int(net.coin["x"]), int(net.coin["y"])), 20)
        for pid, player in net.players.items():
            color = PLAYER_COLOR if pid == net.my_id else OTHERS_COLOR
            pygame.draw.circle(screen, color,
                               (int(player["x"]), int(player["y"])), 15)
        y = 10
        for pid, player in sorted(net.players.items()):
            label = font.render(f"{player['name']}: {player['score']}",
                                True, (255, 255, 255))
            screen.blit(label, (10, y))
            y += 30

        pygame.display.flip()
        clock.tick(60)

    if net.sock is not None:
        net.sock.close()
    pygame.quit()

if __name__ == "__main__":
    main()
```

Здесь три важных блока. **Сеть в игровом цикле.** Сокет после `connect` переводится в неблокирующий режим (`settimeout(0.0)`), поэтому `recv` либо возвращает данные, либо бросает `BlockingIOError`, который мы молча пропускаем. Игра никогда не зависает в ожидании сети: каждый кадр мы читаем всё, что пришло, отправляем позицию курсора и рисуем. **Обработка отключений.** Если `recv` вернул `b""` или возникла `OSError` — значит, соединение умерло: вызываем `drop()`, который закрывает сокет и обнуляет `my_id`. **Реконнект.** Когда `net.sock is None`, главный цикл раз в 2 секунды (`time.monotonic()`) пробует `connect_and_join()` заново. При успехе сервер снова пришлёт `welcome`, `my_id` восстановится, и игра продолжится. Сообщение `join` идемпотентно — сервер просто создаст нового игрока, поэтому повторная регистрация безопасна. Отдельно отмечу `try/except` вокруг `json.loads` для каждого сообщения: не дадим одному битому пакету убить клиент. Финальный штрих — при закрытии окна сокет корректно закрывается, а `pygame.quit()` освобождает ресурсы.

<!--/SOLUTION-->

<!--QUIZ-->
Что создаёт вызов socket.socket(socket.AF_INET, socket.SOCK_STREAM)?
- TCP-сокет (потоковый)
- UDP-сокет (датаграммный)
- Файловый дескриптор
* Правильный ответ: TCP-сокет (потоковый)
SOCK_STREAM означает надёжный потоковый протокол TCP.

Какой метод сервера принимает новое подключение и возвращает (соединение, адрес)?
- accept()
- bind()
- connect()
* Правильный ответ: accept()
accept() блокирует выполнение, пока не появится клиент, и возвращает пару (conn, addr).

Чем TCP отличается от UDP?
- TCP надёжен и сохраняет порядок, UDP быстрее, но без гарантий
- TCP быстрее и без гарантий
- UDP гарантирует доставку и порядок
* Правильный ответ: TCP надёжен и сохраняет порядок, UDP быстрее, но без гарантий
TCP переотправляет потерянные пакеты и собирает их по порядку; UDP просто шлёт датаграммы.

Для чего в сервере используется модуль selectors?
- Чтобы обслуживать несколько неблокирующих сокетов в одном потоке
- Чтобы шифровать данные
- Чтобы сжимать картинки
* Правильный ответ: Чтобы обслуживать несколько неблокирующих сокетов в одном потоке
select() сообщает, какие сокеты готовы к чтению, и один обработчик обслуживает всех клиентов.

Почему для сообщений между клиентом и сервером удобен JSON?
- Это встроенный модуль, формат читается людьми и другими языками, легко превращается в dict
- Потому что JSON бинарный и очень быстрый
- Потому что JSON сам передаёт данные по сети
* Правильный ответ: Это встроенный модуль, формат читается людьми и другими языками, легко превращается в dict
json.dumps превращает dict в строку, json.loads — обратно; формат понятен любому языку.

Зачем каждое JSON-сообщение оканчивается символом переноса строки \n?
- Чтобы можно было определить границы сообщений при потоковой передаче
- Чтобы уменьшить размер пакета
- Для красоты вывода
* Правильный ответ: Чтобы можно было определить границы сообщений при потоковой передаче
recv() приносит произвольные куски потока; \n служит разделителем сообщений.

Что означает, когда recv() возвращает пустые байты b""?
- Противоположная сторона закрыла соединение
- Данных пока нет, нужно подождать
- Произошла сетевая ошибка
* Правильный ответ: Противоположная сторона закрыла соединение
При корректном закрытии соединения recv() возвращает b"" — это сигнал отключения.

Почему игровая логика должна жить на сервере, а не на клиентах?
- Так у всех игроков единое состояние мира и меньше возможностей для читерства
- Так графика работает быстрее
- Тогда не нужен интернет
* Правильный ответ: Так у всех игроков единое состояние мира и меньше возможностей для читерства
Авторитетный сервер сам решает, что произошло, и рассылает результат всем.

Что делает socket.settimeout(0.0) на клиенте pygame?
- Переводит сокет в неблокирующий режим, чтобы игра не зависала в ожидании сети
- Включает шифрование трафика
- Увеличивает скорость передачи
* Правильный ответ: Переводит сокет в неблокирующий режим, чтобы игра не зависала в ожидании сети
recv() сразу возвращает управление (бросая BlockingIOError при отсутствии данных), и игровой цикл продолжается.

Что такое бэкфф (backoff) при реконнекте?
- Пауза перед повторной попыткой подключения, часто растущая при неудачах
- Способ сжатия игрового кадра
- Название игрового режима
* Правильный ответ: Пауза перед повторной попыткой подключения, часто растущая при неудачах
Бэкфф не даёт клиенту «долбить» недоступный сервер и делает повторные попытки мягче.
<!--/QUIZ-->
