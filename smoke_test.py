#!/usr/bin/env python
"""
Смоук-тест платформы: проверяет, что все страницы курса отвечают 200.

Запуск:  python smoke_test.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'courseproj.settings')

import django

django.setup()

from django.test import Client

from learn.models import Lesson


def main():
    client = Client()
    paths = [
        '/',
        '/modules/',
        '/search/',
        '/search/?q=python',
        '/accounts/login/',
        '/register/',
    ]

    lessons = list(Lesson.objects.select_related('module').all())
    for lesson in lessons:
        paths.append(lesson.get_absolute_url())

    bad = []
    for path in paths:
        response = client.get(path)
        if response.status_code != 200:
            bad.append((path, response.status_code))

    print(f'Проверено страниц: {len(paths)} (из них уроков: {len(lessons)})')
    if bad:
        print('ОШИБКИ:')
        for path, status in bad:
            print(f'  {status} {path}')
        return 1
    print('OK: все страницы отвечают 200')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
