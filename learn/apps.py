from django.apps import AppConfig
from django.db.models.signals import post_migrate


class LearnConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'learn'

    def ready(self):
        # Автовосстановление служебного суперпользователя после миграций
        post_migrate.connect(_ensure_admin_after_migrate, sender=self)


def _ensure_admin_after_migrate(sender, **kwargs):
    try:
        from .management.commands.ensure_admin import ensure_superuser
        ensure_superuser()
    except Exception:
        # Таблиц ещё может не быть или БД ещё не готова — пропускаем молча
        pass
