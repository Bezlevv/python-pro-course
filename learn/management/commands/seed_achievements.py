"""
Команда: python manage.py seed_achievements

Создаёт/обновляет список достижений (бейджей). Запускать после load_content.
"""

from django.core.management.base import BaseCommand

from learn.models import Achievement, Lesson, Module

BASE_ACHIEVEMENTS = [
    # slug, title, description, icon, kind, threshold, order
    ('first_step', 'Первый шаг', 'Реши первую задачу курса', '🌱', 'lessons_count', 1, 1),
    ('ten_lessons', 'Десяточка', 'Реши 10 уроков', '🚶', 'lessons_count', 10, 2),
    ('quarter', 'Четверть пути', 'Реши 25 уроков', '🥉', 'lessons_count', 25, 3),
    ('half', 'Половина курса', 'Реши 40 уроков', '🥈', 'lessons_count', 40, 4),
    ('marathon', 'Марафонец', 'Реши 60 уроков', '🥇', 'lessons_count', 60, 5),
    ('streak_3', 'Три дня подряд', 'Занимайся 3 дня подряд', '🔥', 'streak_days', 3, 7),
    ('streak_7', 'Неделя огня', 'Серия из 7 дней', '⚡', 'streak_days', 7, 8),
    ('streak_30', 'Месяц без остановки', 'Серия из 30 дней', '🌋', 'streak_days', 30, 9),
    ('module_1', 'Первая вершина', 'Заверши первый модуль', '⛰️', 'modules_complete', 1, 10),
    ('module_3', 'Три модуля', 'Заверши 3 модуля', '🏔️', 'modules_complete', 3, 11),
]


class Command(BaseCommand):
    help = 'Создаёт достижения курса'

    def handle(self, *args, **options):
        total_lessons = Lesson.objects.count() or 1
        total_modules = Module.objects.count() or 1
        achievements = BASE_ACHIEVEMENTS + [
            ('full_course', 'Мастер Python', 'Реши все уроки курса', '👑', 'lessons_count', total_lessons, 6),
            ('all_modules', 'Покоритель курса', 'Заверши все модули', '🗻', 'modules_complete', total_modules, 12),
        ]
        created = updated = 0
        for slug, title, desc, icon, kind, threshold, order in achievements:
            _, was_created = Achievement.objects.update_or_create(
                slug=slug,
                defaults={
                    'title': title,
                    'description': desc,
                    'icon': icon,
                    'kind': kind,
                    'threshold': threshold,
                    'order': order,
                },
            )
            if was_created:
                created += 1
            else:
                updated += 1
        self.stdout.write(self.style.SUCCESS(
            f'Достижения: создано {created}, обновлено {updated}.'
        ))
