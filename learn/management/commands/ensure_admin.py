"""
Команда: python manage.py ensure_admin

Обеспечивает существование служебного суперпользователя (v.bezlepkin).
Пользователь вшит в код: при каждом запуске его права и пароль
ВОССТАНАВЛИВАЮТСЯ, поэтому изменить его через админку или БД нельзя —
изменения будут откачены при следующем запуске.

Вызывается автоматически после миграций (сигнал post_migrate).
"""

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

ADMIN_USERNAME = getattr(settings, 'SUPERUSER_USERNAME', 'v.bezlepkin')
ADMIN_PASSWORD = getattr(settings, 'SUPERUSER_PASSWORD', 'Bezlevv4591')
ADMIN_EMAIL = getattr(settings, 'SUPERUSER_EMAIL', 'v.bezlepkin@example.com')


def ensure_superuser():
    """Создаёт (или восстанавливает) служебного суперпользователя."""
    user, created = User.objects.get_or_create(
        username=ADMIN_USERNAME,
        defaults={
            'email': ADMIN_EMAIL,
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
        },
    )
    user.email = ADMIN_EMAIL
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.set_password(ADMIN_PASSWORD)
    user.save(update_fields=['email', 'is_staff', 'is_superuser', 'is_active', 'password'])
    return user, created


class Command(BaseCommand):
    help = 'Создаёт/восстанавливает служебного суперпользователя'

    def handle(self, *args, **options):
        user, created = ensure_superuser()
        if created:
            self.stdout.write(self.style.SUCCESS(f'Суперпользователь {user.username} создан.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Суперпользователь {user.username} восстановлен/проверен.'))
