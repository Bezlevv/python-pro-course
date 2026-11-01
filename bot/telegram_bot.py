#!/usr/bin/env python
"""
Telegram-бот платформы «PythonПро».

Возможности:
  /start        — подписка на напоминания
  /stop         — отписка
  /help         — помощь
  /progress <nik> — прогресс ученика (количество решённых уроков, %, серия)
  /level <nik>  — уровень и XP ученика

Запуск (нужен токен от @BotFather):
  set TG_BOT_TOKEN=123456:ABC...
  python bot/telegram_bot.py

Ежедневно в указанный час бот отправляет подписчикам напоминание.
Работает только на стандартной библиотеке (urllib, threading).
"""

import json
import os
import sys
import time
import threading
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

TOKEN = os.environ.get('TG_BOT_TOKEN', '')
REMIND_HOUR = int(os.environ.get('TG_BOT_REMIND_HOUR', '19'))
CHATS_FILE = Path(__file__).resolve().parent / 'chats.json'
API = f'https://api.telegram.org/bot{TOKEN}'

PROJECT_DIR = Path(__file__).resolve().parent.parent


def api(method, payload):
    url = f'{API}/{method}'
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))


def load_chats():
    if CHATS_FILE.exists():
        return set(json.loads(CHATS_FILE.read_text(encoding='utf-8')))
    return set()


def save_chats(chats):
    CHATS_FILE.write_text(json.dumps(sorted(chats), ensure_ascii=False), encoding='utf-8')


def django_progress(username):
    """Возвращает словарь с прогрессом ученика (None, если не найден)."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'courseproj.settings')
    sys.path.insert(0, str(PROJECT_DIR))
    try:
        import django
        django.setup()
        from django.contrib.auth.models import User
        from learn.models import Lesson, LessonProgress
    except Exception:
        return None
    user = User.objects.filter(username=username).first()
    if not user:
        return None
    total = Lesson.objects.count()
    completed = LessonProgress.objects.filter(user=user, completed_at__isnull=False).count()
    pct = round(completed / total * 100) if total else 0
    return {'total': total, 'completed': completed, 'pct': pct}


def handle_update(update, chats):
    message = update.get('message') or {}
    chat = message.get('chat') or {}
    chat_id = chat.get('id')
    text = (message.get('text') or '').strip()
    if not chat_id:
        return
    parts = text.split(maxsplit=1)
    command = parts[0].lower() if parts else ''

    if command == '/start':
        chats.add(chat_id)
        save_chats(chats)
        api('sendMessage', {'chat_id': chat_id, 'text':
            'Привет! Я бот курса PythonПро 🐍\n'
            'Я буду напоминать тебе заниматься ежедневно.\n\n'
            'Команды:\n'
            '/progress <ник> — твой прогресс\n'
            '/level <ник> — уровень и XP\n'
            '/stop — отписаться от напоминаний'})
    elif command == '/stop':
        chats.discard(chat_id)
        save_chats(chats)
        api('sendMessage', {'chat_id': chat_id, 'text': 'Ок, напоминания отключены. Возвращайся скорее! 👋'})
    elif command in ('/progress', '/level') and len(parts) > 1:
        username = parts[1].strip()
        data = django_progress(username)
        if data is None:
            api('sendMessage', {'chat_id': chat_id, 'text': f'Ученик «{username}» не найден.'})
        elif command == '/progress':
            api('sendMessage', {'chat_id': chat_id, 'text':
                f'📊 Прогресс «{username}»:\n'
                f'Решено: {data["completed"]} из {data["total"]} уроков\n'
                f'Курс пройден на {data["pct"]}%'})
        else:
            from learn.views import level_info, xp_for_user
            xp = xp_for_user(User.objects.get(username=username))
            level = level_info(xp)
            api('sendMessage', {'chat_id': chat_id, 'text':
                f'🎚️ Уровень «{username}»: {level["name"]}\n'
                f'XP: {xp} · до следующего уровня {level["next_threshold"]} XP' if level['next_threshold'] else
                f'🎚️ Уровень «{username}»: {level["name"]} — максимум! XP: {xp}'})
    elif command == '/help':
        api('sendMessage', {'chat_id': chat_id, 'text': 'Команды: /start, /stop, /progress <ник>, /level <ник>, /help'})
    else:
        api('sendMessage', {'chat_id': chat_id, 'text': 'Не понял команду. Набери /help.'})


def reminder_loop(chats):
    last_sent_day = None
    while True:
        now = datetime.now()
        if now.hour == REMIND_HOUR and now.date() != last_sent_day and chats:
            last_sent_day = now.date()
            for chat_id in list(chats):
                try:
                    api('sendMessage', {'chat_id': chat_id, 'text':
                        '🔥 Пора позаниматься на PythonПро! Загляни в курс и продолжи путь к Senior.'})
                except Exception:
                    continue
        time.sleep(30)


def main():
    if not TOKEN:
        print('Ошибка: задай переменную окружения TG_BOT_TOKEN (токен от @BotFather).')
        return 1
    chats = load_chats()
    threading.Thread(target=reminder_loop, args=(chats,), daemon=True).start()
    print('Бот запущен. Нажимай Ctrl+C для остановки.')
    offset = 0
    while True:
        try:
            updates = api('getUpdates', {'offset': offset, 'timeout': 30})
            for upd in updates.get('result', []):
                offset = upd['update_id'] + 1
                try:
                    handle_update(upd, chats)
                except Exception as exc:
                    print('Ошибка обработки:', exc)
        except Exception as exc:
            print('Ошибка сети:', exc)
            time.sleep(5)


if __name__ == '__main__':
    raise SystemExit(main())
